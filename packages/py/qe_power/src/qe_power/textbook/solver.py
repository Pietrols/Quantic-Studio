from __future__ import annotations

import cmath
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from qe_core import validate

SOLVER_NAME = "quantic-textbook-newton-raphson"
SOLVER_VERSION = "0.1.0"


def _diagnostic(code: str, severity: str, message: str, element_ref: dict[str, str] | None = None) -> dict[str, Any]:
    return {
        "code": code,
        "severity": severity,
        "message": message,
        "element_ref": element_ref,
    }


def _validate_input(value: dict[str, Any], schema_name: str) -> None:
    diagnostics = validate(value, schema_name)
    if diagnostics:
        messages = "; ".join(
            f"{item.element_ref or {}}: {item.message}" for item in diagnostics
        )
        raise ValueError(f"Invalid {schema_name} input: {messages}")


def _network_matrices(network: dict[str, Any]) -> tuple[np.ndarray, dict[str, int]]:
    buses = network["buses"]
    bus_indices = {bus["bus_id"]: index for index, bus in enumerate(buses)}
    if len(bus_indices) != len(buses):
        raise ValueError("Network bus_id values must be unique")

    bus_count = len(buses)
    ybus = np.zeros((bus_count, bus_count), dtype=np.complex128)
    base_mva = network["base_mva"]

    # See the learning note section "Build the bus admittance matrix".
    # Line base conversion is Zbase = Vbase_LL^2 / Sbase, then Zpu = Zohm / Zbase.
    # The nominal-pi line model adds half of total charging susceptance at each end.
    for line in network["lines"]:
        from_index = bus_indices[line["from_bus"]]
        to_index = bus_indices[line["to_bus"]]
        from_kv = buses[from_index]["vn_kv"]
        to_kv = buses[to_index]["vn_kv"]
        if not math.isclose(from_kv, to_kv, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError(f"Line {line['line_id']} joins buses on different voltage bases")
        impedance_base_ohm = from_kv**2 / base_mva
        impedance_pu = complex(
            line["r_ohm_per_km"] * line["length_km"],
            line["x_ohm_per_km"] * line["length_km"],
        ) / impedance_base_ohm
        if impedance_pu == 0:
            raise ValueError(f"Line {line['line_id']} has zero series impedance")
        series_admittance_pu = 1.0 / impedance_pu
        charging_siemens = line.get("b_us_per_km", 0.0) * 1e-6 * line["length_km"]
        admittance_base_siemens = base_mva / (from_kv**2)
        charging_pu = charging_siemens / admittance_base_siemens
        ybus[from_index, from_index] += series_admittance_pu + 0.5j * charging_pu
        ybus[to_index, to_index] += series_admittance_pu + 0.5j * charging_pu
        ybus[from_index, to_index] -= series_admittance_pu
        ybus[to_index, from_index] -= series_admittance_pu

    # See the learning note section "Build the bus admittance matrix".
    # Off-nominal transformer stamp for tap a on the high-voltage side:
    # Yff=y/|a|^2, Yft=-y/conj(a), Ytf=-y/a, Ytt=y.
    for transformer in network["transformers"]:
        hv_index = bus_indices[transformer["hv_bus"]]
        lv_index = bus_indices[transformer["lv_bus"]]
        if not math.isclose(
            buses[hv_index]["vn_kv"], transformer["vn_hv_kv"], rel_tol=0.0, abs_tol=1e-9
        ):
            raise ValueError(f"Transformer {transformer['transformer_id']} HV voltage base mismatch")
        if not math.isclose(
            buses[lv_index]["vn_kv"], transformer["vn_lv_kv"], rel_tol=0.0, abs_tol=1e-9
        ):
            raise ValueError(f"Transformer {transformer['transformer_id']} LV voltage base mismatch")
        impedance_pu = complex(transformer["r_pu"], transformer["x_pu"])
        impedance_pu *= base_mva / transformer["sn_mva"]
        if impedance_pu == 0:
            raise ValueError(f"Transformer {transformer['transformer_id']} has zero impedance")
        series_admittance_pu = 1.0 / impedance_pu
        tap_ratio = transformer.get("tap_ratio", 1.0)
        phase_shift = math.radians(transformer.get("phase_shift_degree", 0.0))
        tap = tap_ratio * cmath.exp(1j * phase_shift)
        ybus[hv_index, hv_index] += series_admittance_pu / (abs(tap) ** 2)
        ybus[hv_index, lv_index] -= series_admittance_pu / tap.conjugate()
        ybus[lv_index, hv_index] -= series_admittance_pu / tap
        ybus[lv_index, lv_index] += series_admittance_pu

    # Shunts are constant admittances, not constant power injections.
    # docs/specs/network.md: "Shunt values are specified as power at nominal bus
    # voltage, with positive values denoting consumption."
    # A shunt y = G + jB draws I = y V, so it consumes S = V conj(I) = conj(y) |V|^2.
    # At |V| = 1 pu, conj(y) = (p_mw + j q_mvar) / base_mva, so the diagonal stamp is
    # y = (p_mw - j q_mvar) / base_mva. A capacitor (q_mvar < 0) gives B > 0.
    for shunt in network["shunts"]:
        index = bus_indices[shunt["bus_id"]]
        ybus[index, index] += complex(shunt["p_mw"], -shunt["q_mvar"]) / base_mva

    return ybus, bus_indices


def _specified_power(network: dict[str, Any], bus_indices: dict[str, int]) -> tuple[np.ndarray, np.ndarray]:
    base_mva = network["base_mva"]
    specified_p_pu = np.zeros(len(bus_indices), dtype=np.float64)
    specified_q_pu = np.zeros(len(bus_indices), dtype=np.float64)
    generator_buses: set[str] = set()

    for generator in network["generators"]:
        bus_id = generator["bus_id"]
        specified_p_pu[bus_indices[bus_id]] += generator["p_mw"] / base_mva
        generator_buses.add(bus_id)
    for load in network["loads"]:
        index = bus_indices[load["bus_id"]]
        specified_p_pu[index] -= load["p_mw"] / base_mva
        specified_q_pu[index] -= load["q_mvar"] / base_mva
    # Shunts are not specified power: they are stamped into the Y-bus diagonal in
    # _network_matrices, so their power varies with |V|^2.

    return specified_p_pu, specified_q_pu


def _initial_voltage(network: dict[str, Any], bus_indices: dict[str, int]) -> tuple[np.ndarray, list[int], list[int]]:
    buses = network["buses"]
    slack_grids = network["external_grids"]
    if len(slack_grids) != 1:
        raise ValueError("A load-flow network must contain exactly one external grid")
    slack_id = slack_grids[0]["bus_id"]
    slack_index = bus_indices[slack_id]
    slack_bus = buses[slack_index]
    if slack_bus["bus_type"] != "slack":
        raise ValueError(f"External grid {slack_grids[0]['external_grid_id']} must connect to a slack bus")

    voltage_magnitudes = np.ones(len(buses), dtype=np.float64)
    voltage_angles = np.zeros(len(buses), dtype=np.float64)
    voltage_magnitudes[slack_index] = slack_grids[0]["vm_setpoint_pu"]
    voltage_angles[slack_index] = math.radians(slack_grids[0]["va_setpoint_degree"])
    pv_buses: set[int] = set()

    generator_setpoints: dict[str, list[float]] = {}
    for generator in network["generators"]:
        generator_setpoints.setdefault(generator["bus_id"], []).append(generator["vm_setpoint_pu"])
    for bus in buses:
        bus_id = bus["bus_id"]
        index = bus_indices[bus_id]
        if bus["bus_type"] == "slack":
            if bus_id != slack_id:
                raise ValueError(f"Slack bus {bus_id} has no matching external grid")
        elif bus["bus_type"] == "pv":
            setpoints = generator_setpoints.get(bus_id, [])
            if not setpoints:
                raise ValueError(f"PV bus {bus_id} has no generator voltage setpoint")
            if any(not math.isclose(value, setpoints[0], rel_tol=0.0, abs_tol=1e-12) for value in setpoints):
                raise ValueError(f"PV bus {bus_id} has conflicting generator voltage setpoints")
            voltage_magnitudes[index] = setpoints[0]
            pv_buses.add(index)
        elif "vm_pu" in bus:
            voltage_magnitudes[index] = bus["vm_pu"]
        if bus["bus_type"] != "slack" and "va_degree" in bus:
            voltage_angles[index] = math.radians(bus["va_degree"])

    angle_bus_indices = [index for index in range(len(buses)) if index != slack_index]
    pq_bus_indices = [
        index for index, bus in enumerate(buses) if bus["bus_type"] == "pq"
    ]
    if pv_buses.intersection(pq_bus_indices):
        raise ValueError("A bus cannot be both PV and PQ")
    return voltage_magnitudes * np.exp(1j * voltage_angles), angle_bus_indices, pq_bus_indices


def _calculate_power(ybus: np.ndarray, voltage: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # See the learning note section "Calculate bus power from voltage".
    # Complex power injection equation: S_i = V_i * conj(sum_j(Y_ij * V_j)).
    calculated = voltage * np.conjugate(ybus @ voltage)
    return calculated.real, calculated.imag


def _mismatch_vector(
    p_calculated: np.ndarray,
    q_calculated: np.ndarray,
    p_specified: np.ndarray,
    q_specified: np.ndarray,
    angle_bus_indices: list[int],
    pq_bus_indices: list[int],
) -> np.ndarray:
    # See the learning note section "Form the mismatch vector".
    # Newton residual is specified injection minus calculated injection at each constrained bus.
    p_mismatch = p_specified[angle_bus_indices] - p_calculated[angle_bus_indices]
    q_mismatch = q_specified[pq_bus_indices] - q_calculated[pq_bus_indices]
    return np.concatenate((p_mismatch, q_mismatch))


def _build_jacobian(
    ybus: np.ndarray,
    voltage: np.ndarray,
    p_calculated: np.ndarray,
    q_calculated: np.ndarray,
    angle_bus_indices: list[int],
    pq_bus_indices: list[int],
) -> np.ndarray:
    # See the learning note section "Construct the explicit Jacobian".
    # Polar power equations are P_i=sum(V_i V_k (G_ik cos(theta_ik)+B_ik sin(theta_ik)))
    # and Q_i=sum(V_i V_k (G_ik sin(theta_ik)-B_ik cos(theta_ik))).
    # The four Jacobian blocks below are the derivatives of those equations.
    bus_count = len(voltage)
    angle_columns = {bus_index: column for column, bus_index in enumerate(angle_bus_indices)}
    voltage_columns = {
        bus_index: len(angle_bus_indices) + column
        for column, bus_index in enumerate(pq_bus_indices)
    }
    q_row_offset = len(angle_bus_indices)
    jacobian = np.zeros(
        (len(angle_bus_indices) + len(pq_bus_indices), len(angle_bus_indices) + len(pq_bus_indices)),
        dtype=np.float64,
    )
    magnitudes = np.abs(voltage)
    angles = np.angle(voltage)
    conductance = ybus.real
    susceptance = ybus.imag
    p_rows = {bus_index: row for row, bus_index in enumerate(angle_bus_indices)}
    q_rows = {
        bus_index: q_row_offset + row for row, bus_index in enumerate(pq_bus_indices)
    }

    for bus_index in range(bus_count):
        for other_index in range(bus_count):
            angle_difference = angles[bus_index] - angles[other_index]
            g_value = conductance[bus_index, other_index]
            b_value = susceptance[bus_index, other_index]
            cosine = math.cos(angle_difference)
            sine = math.sin(angle_difference)

            if bus_index in p_rows and other_index in angle_columns:
                if bus_index == other_index:
                    derivative = -q_calculated[bus_index] - b_value * magnitudes[bus_index] ** 2
                else:
                    derivative = magnitudes[bus_index] * magnitudes[other_index] * (
                        g_value * sine - b_value * cosine
                    )
                jacobian[p_rows[bus_index], angle_columns[other_index]] = derivative

            if bus_index in p_rows and other_index in voltage_columns:
                if bus_index == other_index:
                    derivative = p_calculated[bus_index] / magnitudes[bus_index] + g_value * magnitudes[bus_index]
                else:
                    derivative = magnitudes[bus_index] * (g_value * cosine + b_value * sine)
                jacobian[p_rows[bus_index], voltage_columns[other_index]] = derivative

            if bus_index in q_rows and other_index in angle_columns:
                if bus_index == other_index:
                    derivative = p_calculated[bus_index] - g_value * magnitudes[bus_index] ** 2
                else:
                    derivative = -magnitudes[bus_index] * magnitudes[other_index] * (
                        g_value * cosine + b_value * sine
                    )
                jacobian[q_rows[bus_index], angle_columns[other_index]] = derivative

            if bus_index in q_rows and other_index in voltage_columns:
                if bus_index == other_index:
                    derivative = q_calculated[bus_index] / magnitudes[bus_index] - b_value * magnitudes[bus_index]
                else:
                    derivative = magnitudes[bus_index] * (g_value * sine - b_value * cosine)
                jacobian[q_rows[bus_index], voltage_columns[other_index]] = derivative

    return jacobian


def _branch_results(network: dict[str, Any], bus_indices: dict[str, int], voltage: np.ndarray) -> list[dict[str, Any]]:
    # See the learning note section "Calculate branch flows and losses".
    # Terminal complex power is S_terminal = V_terminal * conj(I_terminal) * Sbase.
    base_mva = network["base_mva"]
    buses = network["buses"]
    results: list[dict[str, Any]] = []

    for line in network["lines"]:
        from_index = bus_indices[line["from_bus"]]
        to_index = bus_indices[line["to_bus"]]
        voltage_base_kv = buses[from_index]["vn_kv"]
        impedance_base_ohm = voltage_base_kv**2 / base_mva
        impedance_pu = complex(
            line["r_ohm_per_km"] * line["length_km"],
            line["x_ohm_per_km"] * line["length_km"],
        ) / impedance_base_ohm
        series_admittance_pu = 1.0 / impedance_pu
        charging_siemens = line.get("b_us_per_km", 0.0) * 1e-6 * line["length_km"]
        charging_base_siemens = base_mva / (voltage_base_kv**2)
        charging_pu = charging_siemens / charging_base_siemens
        from_current_pu = series_admittance_pu * (voltage[from_index] - voltage[to_index])
        from_current_pu += 0.5j * charging_pu * voltage[from_index]
        to_current_pu = series_admittance_pu * (voltage[to_index] - voltage[from_index])
        to_current_pu += 0.5j * charging_pu * voltage[to_index]
        from_power_mva = voltage[from_index] * from_current_pu.conjugate() * base_mva
        to_power_mva = voltage[to_index] * to_current_pu.conjugate() * base_mva
        current_base_ka = base_mva / (math.sqrt(3.0) * voltage_base_kv)
        current_rating_ka = line.get("max_current_ka")
        loading_pct = None
        if current_rating_ka is not None:
            maximum_current_ka = max(abs(from_current_pu), abs(to_current_pu)) * current_base_ka
            loading_pct = maximum_current_ka / current_rating_ka * 100.0
        results.append(
            {
                "branch_id": line["line_id"],
                "branch_type": "line",
                "p_from_mw": from_power_mva.real,
                "q_from_mvar": from_power_mva.imag,
                "p_to_mw": to_power_mva.real,
                "q_to_mvar": to_power_mva.imag,
                "p_loss_mw": from_power_mva.real + to_power_mva.real,
                "q_loss_mvar": from_power_mva.imag + to_power_mva.imag,
                "loading_pct": loading_pct,
            }
        )

    for transformer in network["transformers"]:
        hv_index = bus_indices[transformer["hv_bus"]]
        lv_index = bus_indices[transformer["lv_bus"]]
        impedance_pu = complex(transformer["r_pu"], transformer["x_pu"])
        impedance_pu *= base_mva / transformer["sn_mva"]
        series_admittance_pu = 1.0 / impedance_pu
        tap_ratio = transformer.get("tap_ratio", 1.0)
        phase_shift = math.radians(transformer.get("phase_shift_degree", 0.0))
        tap = tap_ratio * cmath.exp(1j * phase_shift)
        hv_current_pu = series_admittance_pu / (abs(tap) ** 2) * voltage[hv_index]
        hv_current_pu -= series_admittance_pu / tap.conjugate() * voltage[lv_index]
        lv_current_pu = -series_admittance_pu / tap * voltage[hv_index]
        lv_current_pu += series_admittance_pu * voltage[lv_index]
        hv_power_mva = voltage[hv_index] * hv_current_pu.conjugate() * base_mva
        lv_power_mva = voltage[lv_index] * lv_current_pu.conjugate() * base_mva
        loading_pct = max(abs(hv_power_mva), abs(lv_power_mva)) / transformer["sn_mva"] * 100.0
        results.append(
            {
                "branch_id": transformer["transformer_id"],
                "branch_type": "transformer",
                "p_from_mw": hv_power_mva.real,
                "q_from_mvar": hv_power_mva.imag,
                "p_to_mw": lv_power_mva.real,
                "q_to_mvar": lv_power_mva.imag,
                "p_loss_mw": hv_power_mva.real + lv_power_mva.real,
                "q_loss_mvar": hv_power_mva.imag + lv_power_mva.imag,
                "loading_pct": loading_pct,
            }
        )

    return results


def run_loadflow(
    network: dict[str, Any],
    request: dict[str, Any],
    input_hash_sha256: str,
) -> dict[str, Any]:
    """Solve a balanced load flow with polar Newton-Raphson and return the contract result."""
    _validate_input(network, "power/network")
    _validate_input(request, "power/loadflow-request")
    if len(input_hash_sha256) != 64 or any(
        character not in "0123456789abcdefABCDEF" for character in input_hash_sha256
    ):
        raise ValueError("input_hash_sha256 must contain exactly 64 hexadecimal characters")
    if request.get("initialization", "flat") != "flat":
        raise ValueError("Only flat initialization is supported by this solver")

    ybus, bus_indices = _network_matrices(network)
    p_specified, q_specified = _specified_power(network, bus_indices)
    voltage, angle_bus_indices, pq_bus_indices = _initial_voltage(network, bus_indices)
    tolerance_pu = request["tolerance_mva"] / network["base_mva"]
    max_iterations = request["max_iterations"]
    mismatch_history: list[float] = []
    converged = False
    iteration_count = 0
    singular_message: str | None = None

    for iteration_count in range(max_iterations + 1):
        p_calculated, q_calculated = _calculate_power(ybus, voltage)
        mismatch = _mismatch_vector(
            p_calculated,
            q_calculated,
            p_specified,
            q_specified,
            angle_bus_indices,
            pq_bus_indices,
        )
        largest_mismatch_pu = float(np.max(np.abs(mismatch))) if mismatch.size else 0.0
        mismatch_history.append(largest_mismatch_pu)
        if largest_mismatch_pu < tolerance_pu:
            converged = True
            break
        if iteration_count == max_iterations:
            break

        jacobian = _build_jacobian(
            ybus,
            voltage,
            p_calculated,
            q_calculated,
            angle_bus_indices,
            pq_bus_indices,
        )
        try:
            # Newton step: J(x_k) * delta_x = specified_minus_calculated_mismatch.
            correction = np.linalg.solve(jacobian, mismatch)
        except np.linalg.LinAlgError as error:
            singular_message = str(error)
            break

        angle_correction = correction[: len(angle_bus_indices)]
        magnitude_correction = correction[len(angle_bus_indices) :]
        voltage_angles = np.angle(voltage)
        voltage_magnitudes = np.abs(voltage)
        voltage_angles[angle_bus_indices] += angle_correction
        voltage_magnitudes[pq_bus_indices] += magnitude_correction
        voltage = voltage_magnitudes * np.exp(1j * voltage_angles)

    p_calculated, q_calculated = _calculate_power(ybus, voltage)
    mismatch = _mismatch_vector(
        p_calculated,
        q_calculated,
        p_specified,
        q_specified,
        angle_bus_indices,
        pq_bus_indices,
    )
    largest_mismatch_pu = float(np.max(np.abs(mismatch))) if mismatch.size else 0.0
    if not mismatch_history or mismatch_history[-1] != largest_mismatch_pu:
        mismatch_history.append(largest_mismatch_pu)
    if largest_mismatch_pu < tolerance_pu:
        converged = True

    buses = network["buses"]
    diagnostics = [
        _diagnostic(
            "ITERATION_MISMATCH_HISTORY",
            "info",
            "mismatch_history_pu=" + json.dumps(mismatch_history, separators=(",", ":")),
        )
    ]
    if singular_message is not None:
        diagnostics.append(
            _diagnostic(
                "SINGULAR_JACOBIAN",
                "error",
                f"Newton-Raphson Jacobian could not be solved: {singular_message}",
            )
        )
    if not converged and singular_message is None:
        diagnostics.append(
            _diagnostic(
                "NON_CONVERGENCE",
                "error",
                f"Mismatch remained {largest_mismatch_pu:.12g} pu after {iteration_count} iterations",
            )
        )

    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "schema_version": "0.1.0",
        "result_id": f"{request['request_id']}-result",
        "network_id": network["network_id"],
        "bus_results": [
            {
                "bus_id": bus["bus_id"],
                "vm_pu": float(abs(voltage[index])),
                "va_degree": float(math.degrees(cmath.phase(voltage[index]))),
            }
            for index, bus in enumerate(buses)
        ],
        "branch_results": _branch_results(network, bus_indices, voltage),
        "convergence": {
            "converged": converged,
            "iterations": iteration_count,
            "largest_mismatch_mva": largest_mismatch_pu * network["base_mva"],
        },
        "diagnostics": diagnostics,
        "provenance": {
            "solver_name": SOLVER_NAME,
            "solver_version": SOLVER_VERSION,
            "input_hash_sha256": input_hash_sha256.lower(),
            "timestamp": timestamp,
        },
    }


def run_loadflow_file(network_path: str | Path, request: dict[str, Any]) -> dict[str, Any]:
    """Load a network file and bind the result provenance to its exact bytes."""
    path = Path(network_path)
    input_bytes = path.read_bytes()
    network = json.loads(input_bytes)
    input_hash_sha256 = hashlib.sha256(input_bytes).hexdigest()
    return run_loadflow(network, request, input_hash_sha256)
