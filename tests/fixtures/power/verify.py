from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class VerificationSummary:
    max_bus_mismatch_pu: float
    generation_mw: float
    load_mw: float
    shunt_consumption_mw: float
    network_losses_mw: float
    reported_losses_mw: float
    energy_balance_error_mw: float


def _stamp_series_branch(
    ybus: list[list[complex]],
    from_index: int,
    to_index: int,
    admittance_pu: complex,
    tap: complex = 1.0 + 0.0j,
    charging_pu: float = 0.0,
) -> None:
    ybus[from_index][from_index] += admittance_pu / (abs(tap) ** 2) + 0.5j * charging_pu
    ybus[from_index][to_index] -= admittance_pu / tap.conjugate()
    ybus[to_index][from_index] -= admittance_pu / tap
    ybus[to_index][to_index] += admittance_pu + 0.5j * charging_pu


def _network_admittance(network: dict[str, Any]) -> tuple[list[list[complex]], dict[str, int]]:
    buses = network["buses"]
    bus_indices = {bus["bus_id"]: index for index, bus in enumerate(buses)}
    if len(bus_indices) != len(buses):
        raise AssertionError("Network bus IDs must be unique")

    ybus = [[0j for _ in buses] for _ in buses]
    base_mva = network["base_mva"]

    for line in network["lines"]:
        from_index = bus_indices[line["from_bus"]]
        to_index = bus_indices[line["to_bus"]]
        from_kv = buses[from_index]["vn_kv"]
        to_kv = buses[to_index]["vn_kv"]
        if not math.isclose(from_kv, to_kv, rel_tol=0.0, abs_tol=1e-12):
            raise AssertionError(f"Line {line['line_id']} joins unlike voltage bases")
        z_base_ohm = from_kv**2 / base_mva
        impedance_pu = complex(
            line["r_ohm_per_km"] * line["length_km"],
            line["x_ohm_per_km"] * line["length_km"],
        ) / z_base_ohm
        if impedance_pu == 0:
            raise AssertionError(f"Line {line['line_id']} has zero series impedance")
        admittance_pu = 1 / impedance_pu
        charging_us = line.get("b_us_per_km", 0.0) * line["length_km"]
        y_base_siemens = base_mva / (from_kv**2)
        charging_pu = charging_us * 1e-6 / y_base_siemens
        _stamp_series_branch(ybus, from_index, to_index, admittance_pu, charging_pu=charging_pu)

    for transformer in network["transformers"]:
        hv_index = bus_indices[transformer["hv_bus"]]
        lv_index = bus_indices[transformer["lv_bus"]]
        if not math.isclose(
            buses[hv_index]["vn_kv"], transformer["vn_hv_kv"], rel_tol=0.0, abs_tol=1e-9
        ):
            raise AssertionError(f"Transformer {transformer['transformer_id']} HV base mismatch")
        if not math.isclose(
            buses[lv_index]["vn_kv"], transformer["vn_lv_kv"], rel_tol=0.0, abs_tol=1e-9
        ):
            raise AssertionError(f"Transformer {transformer['transformer_id']} LV base mismatch")
        impedance_pu = complex(transformer["r_pu"], transformer["x_pu"])
        impedance_pu *= base_mva / transformer["sn_mva"]
        if impedance_pu == 0:
            raise AssertionError(f"Transformer {transformer['transformer_id']} has zero impedance")
        admittance_pu = 1 / impedance_pu
        ratio = transformer.get("tap_ratio", 1.0)
        shift = math.radians(transformer.get("phase_shift_degree", 0.0))
        tap = ratio * cmath.exp(1j * shift)
        _stamp_series_branch(ybus, hv_index, lv_index, admittance_pu, tap=tap)

    return ybus, bus_indices


def verify_loadflow_result(
    network: dict[str, Any],
    result: dict[str, Any],
    mismatch_tolerance_pu: float = 1e-8,
) -> VerificationSummary:
    """Check specified-bus power balance and reported active-loss balance."""
    base_mva = network["base_mva"]
    ybus, bus_indices = _network_admittance(network)
    bus_results = result["bus_results"]
    bus_result_by_id = {item["bus_id"]: item for item in bus_results}
    if len(bus_result_by_id) != len(bus_results) or set(bus_result_by_id) != set(bus_indices):
        raise AssertionError("Result bus IDs must exactly match network bus IDs")

    voltages = [
        bus_result_by_id[bus["bus_id"]]["vm_pu"]
        * cmath.exp(1j * math.radians(bus_result_by_id[bus["bus_id"]]["va_degree"]))
        for bus in network["buses"]
    ]
    calculated_powers: list[complex] = []
    for row_index, voltage in enumerate(voltages):
        current_pu = sum(
            ybus[row_index][column_index] * other_voltage
            for column_index, other_voltage in enumerate(voltages)
        )
        calculated_powers.append(voltage * current_pu.conjugate())

    generation_p_by_bus = {bus_id: 0.0 for bus_id in bus_indices}
    generator_buses: set[str] = set()
    for generator in network["generators"]:
        generation_p_by_bus[generator["bus_id"]] += generator["p_mw"]
        generator_buses.add(generator["bus_id"])

    load_p_by_bus = {bus_id: 0.0 for bus_id in bus_indices}
    load_q_by_bus = {bus_id: 0.0 for bus_id in bus_indices}
    for load in network["loads"]:
        load_p_by_bus[load["bus_id"]] += load["p_mw"]
        load_q_by_bus[load["bus_id"]] += load["q_mvar"]

    shunt_p_by_bus = {bus_id: 0.0 for bus_id in bus_indices}
    shunt_q_by_bus = {bus_id: 0.0 for bus_id in bus_indices}
    for shunt in network["shunts"]:
        shunt_p_by_bus[shunt["bus_id"]] += shunt["p_mw"]
        shunt_q_by_bus[shunt["bus_id"]] += shunt["q_mvar"]

    slack_ids = {grid["bus_id"] for grid in network["external_grids"]}
    max_bus_mismatch_pu = 0.0
    for bus in network["buses"]:
        bus_id = bus["bus_id"]
        if bus_id in slack_ids or bus["bus_type"] == "slack":
            continue
        index = bus_indices[bus_id]
        specified_p_pu = (
            generation_p_by_bus[bus_id] - load_p_by_bus[bus_id] - shunt_p_by_bus[bus_id]
        ) / base_mva
        p_mismatch_pu = calculated_powers[index].real - specified_p_pu
        max_bus_mismatch_pu = max(max_bus_mismatch_pu, abs(p_mismatch_pu))

        if bus["bus_type"] == "pq" and bus_id not in generator_buses:
            specified_q_pu = -(load_q_by_bus[bus_id] + shunt_q_by_bus[bus_id]) / base_mva
            q_mismatch_pu = calculated_powers[index].imag - specified_q_pu
            max_bus_mismatch_pu = max(max_bus_mismatch_pu, abs(q_mismatch_pu))

    if max_bus_mismatch_pu >= mismatch_tolerance_pu:
        raise AssertionError(
            f"Maximum specified-bus mismatch {max_bus_mismatch_pu:.12g} pu is not below "
            f"{mismatch_tolerance_pu:.12g} pu"
        )

    generation_mw = sum(
        calculated_powers[bus_indices[bus["bus_id"]]].real * base_mva
        + load_p_by_bus[bus["bus_id"]]
        + shunt_p_by_bus[bus["bus_id"]]
        for bus in network["buses"]
    )
    load_mw = sum(load_p_by_bus.values())
    shunt_consumption_mw = sum(shunt_p_by_bus.values())
    network_losses_mw = sum(power.real for power in calculated_powers) * base_mva

    network_branches = {
        branch["line_id"] for branch in network["lines"]
    } | {branch["transformer_id"] for branch in network["transformers"]}
    result_branches = {branch["branch_id"]: branch for branch in result["branch_results"]}
    if len(result_branches) != len(result["branch_results"]) or set(result_branches) != network_branches:
        raise AssertionError("Result branch IDs must exactly match network branch IDs")

    reported_losses_mw = 0.0
    for branch in result_branches.values():
        terminal_loss_mw = branch["p_from_mw"] + branch["p_to_mw"]
        if not math.isclose(terminal_loss_mw, branch["p_loss_mw"], rel_tol=0.0, abs_tol=1e-8 * base_mva):
            raise AssertionError(f"Branch {branch['branch_id']} loss differs from terminal power sum")
        reported_losses_mw += branch["p_loss_mw"]

    energy_balance_error_mw = generation_mw - load_mw - shunt_consumption_mw - reported_losses_mw
    energy_tolerance_mw = mismatch_tolerance_pu * base_mva
    if abs(energy_balance_error_mw) >= energy_tolerance_mw:
        raise AssertionError(
            f"Generation minus load and shunts differs from branch losses by "
            f"{energy_balance_error_mw:.12g} MW"
        )
    if not math.isclose(network_losses_mw, reported_losses_mw, rel_tol=0.0, abs_tol=energy_tolerance_mw):
        raise AssertionError(
            f"Y-bus active losses {network_losses_mw:.12g} MW differ from reported "
            f"branch losses {reported_losses_mw:.12g} MW"
        )

    return VerificationSummary(
        max_bus_mismatch_pu=max_bus_mismatch_pu,
        generation_mw=generation_mw,
        load_mw=load_mw,
        shunt_consumption_mw=shunt_consumption_mw,
        network_losses_mw=network_losses_mw,
        reported_losses_mw=reported_losses_mw,
        energy_balance_error_mw=energy_balance_error_mw,
    )
