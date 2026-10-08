"""Contract network to pandapower, Newton-Raphson load flow, contract result.

Every unit or base conversion below cites the pandapower 3.5.6 documentation
page that defines the pandapower side of the mapping. Contract conventions are
defined in docs/specs/network.md.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
from qe_core import Diagnostic, Outcome, validate
from qe_core.project import validate_network
from qe_core.provenance import hash_inputs, provenance
from qe_core.validation import diagnostic

import pandapower as pp

SOLVER_NAME = "pandapower"
DOCS = "https://pandapower.readthedocs.io/en/v3.5.6"


class LoadflowInputError(ValueError):
    """Raised by run_loadflow_file when the inputs cannot be solved at all.

    The diagnostics name the element and field at fault. Non-convergence is not
    an input error: it returns a result with converged=false.
    """

    def __init__(self, diagnostics: list[Diagnostic]):
        self.diagnostics = diagnostics
        super().__init__("; ".join(
            f"{d.code} {d.element_ref or {}}: {d.message}" for d in diagnostics))


def _preflight(network, request):
    errors = validate_network(network) + validate(request, "power/loadflow-request")
    if errors:
        return errors
    if request.get("initialization", "flat") != "flat":
        errors.append(diagnostic("UNSUPPORTED_INITIALIZATION", "No compatible prior result was supplied",
                                 "request", request["request_id"], "initialization"))
    for gen in network["generators"]:
        if gen.get("q_min_mvar", -math.inf) > gen.get("q_max_mvar", math.inf):
            errors.append(diagnostic("GENERATOR_Q_RANGE", "q_min_mvar must not exceed q_max_mvar",
                                     "generators", gen["generator_id"], "q_min_mvar"))
    buses = {b["bus_id"]: b for b in network["buses"]}
    sources = {g["bus_id"] for g in network["external_grids"]}
    generators = {g["bus_id"] for g in network["generators"]}
    adjacency = {b: set() for b in buses}
    for kind, ends in (("lines", ("from_bus", "to_bus")), ("transformers", ("hv_bus", "lv_bus"))):
        for item in network[kind]:
            a, b = (item[k] for k in ends)
            identifier = item["line_id" if kind == "lines" else "transformer_id"]
            adjacency[a].add(b)
            adjacency[b].add(a)
            if a == b:
                errors.append(diagnostic("SELF_LOOP", "Branch endpoints must differ", kind, identifier, ends[1]))
            if kind == "lines" and buses[a]["vn_kv"] != buses[b]["vn_kv"]:
                errors.append(diagnostic("VOLTAGE_BASE", "Lines require equal endpoint voltage bases",
                                         kind, identifier, "to_bus"))
            if kind == "lines" and item["r_ohm_per_km"] == 0 and item["x_ohm_per_km"] == 0:
                errors.append(diagnostic("UNSUPPORTED_IMPEDANCE", "Zero series impedance is unsupported",
                                         kind, identifier, "x_ohm_per_km"))
            # pandapower derives x_k = sqrt(vk^2 - vkr^2) >= 0 (elements/trafo.html,
            # Impedance Values), so a capacitive or zero transformer reactance
            # cannot be represented.
            if kind == "transformers" and item["x_pu"] <= 0:
                errors.append(diagnostic("UNSUPPORTED_IMPEDANCE", "Transformer reactance must be positive",
                                         kind, identifier, "x_pu"))
    pending = set(buses)
    while pending:
        component, queue = set(), [next(iter(pending))]
        while queue:
            bus = queue.pop()
            if bus not in component:
                component.add(bus)
                queue.extend(adjacency[bus] - component)
        pending -= component
        if len(component & sources) != 1:
            errors.append(diagnostic("SLACK_COUNT", "Each connected component needs exactly one external-grid bus",
                                     "network", network["network_id"], "external_grids"))
    if len(sources) != len(network["external_grids"]):
        errors.append(diagnostic("DUPLICATE_CONTROL", "Only one external grid per bus is supported",
                                 "network", network["network_id"], "external_grids"))
    if len(generators) != len(network["generators"]):
        errors.append(diagnostic("DUPLICATE_CONTROL", "Only one generator per bus is supported",
                                 "network", network["network_id"], "generators"))
    for bus in buses.values():
        expected = "slack" if bus["bus_id"] in sources else "pv" if bus["bus_id"] in generators else "pq"
        if bus["bus_type"] != expected or bus["bus_id"] in sources & generators:
            errors.append(diagnostic("BUS_CONTROL", f"Bus type must match source controls ({expected})",
                                     "buses", bus["bus_id"], "bus_type"))
    return errors


def _model_notes(network):
    """Diagnostics for contract fields this adapter reads but does not apply."""
    notes = []

    def note(code, message, kind, identifier, field, severity):
        notes.append(Diagnostic(code, message, {"element_type": kind, "element_id": identifier,
                                                "field": field}, severity))

    # CC-1 fields describe a separate fault study, not load-flow controls.
    for kind, id_field, fields in (
        ("external_grids", "external_grid_id", ("s_sc_max_mva", "s_sc_min_mva", "rx_max", "rx_min")),
        ("generators", "generator_id", ("sn_mva", "vn_kv", "xdss_pu", "rdss_ohm", "cos_phi",
                                       "voltage_control_range_percent", "power_station_transformer_id")),
        ("lines", "line_id", ("end_temperature_celsius",)),
        ("transformers", "transformer_id", ("power_station_unit", "oltc")),
    ):
        for element in network[kind]:
            for field in fields:
                if field in element:
                    note("STUDY_ONLY_FIELD", "Short-circuit input is not used by load flow",
                         kind, element[id_field], field, "info")

    for bus in network["buses"]:
        for field in ("vm_pu", "va_degree"):
            if field in bus:
                note("REFERENCE_NOT_INITIALIZATION",
                     "Stored bus value is reference data; the solve uses a flat start",
                     "buses", bus["bus_id"], field, "info")
    for gen in network["generators"]:
        for field in ("p_min_mw", "p_max_mw"):
            if field in gen:
                note("LIMIT_NOT_ENFORCED", "Fixed active-power dispatch does not enforce this operating limit",
                     "generators", gen["generator_id"], field, "warning")
    for trafo in network["transformers"]:
        note("TRANSFORMER_MODEL",
             "Series impedance and ideal ratio only; the contract has no magnetizing branch, so pfe_kw=0 and i0_percent=0",
             "transformers", trafo["transformer_id"], "magnetizing", "info")
    for shunt in network["shunts"]:
        note("SHUNT_MODEL",
             "Shunt is a constant admittance: its power is specified at nominal voltage and scales with V^2",
             "shunts", shunt["shunt_id"], "q_mvar", "info")
    return notes


def _convert(network):
    # net.sn_mva is the system per-unit base S_N (about/units.html).
    net = pp.create_empty_network(sn_mva=network["base_mva"])
    buses = {b["bus_id"]: pp.create_bus(net, vn_kv=b["vn_kv"], name=b.get("name", b["bus_id"]))
             for b in network["buses"]}
    for line in network["lines"]:
        # elements/line.html, Electric Model: pi model with total shunt
        # Y = j*2*pi*f*c_nf_per_km*1e-9*length_km, split equally between ends.
        # The contract gives B per km in microsiemens at study frequency, so
        # C[nF/km] = B[uS/km] * 1e-6 / (2*pi*f) * 1e9 = B * 1e3 / (2*pi*f).
        # The frequency cancels, so the default net.f_hz is harmless.
        c_nf = line.get("b_us_per_km", 0) * 1e3 / (2 * math.pi * net.f_hz)
        # elements/line.html, Result Parameters:
        # loading_percent = i_ka / (max_i_ka * df * parallel) * 100.
        # With no rating the loading is NaN and is reported as null.
        pp.create_line_from_parameters(net, buses[line["from_bus"]], buses[line["to_bus"]],
            length_km=line["length_km"], r_ohm_per_km=line["r_ohm_per_km"],
            x_ohm_per_km=line["x_ohm_per_km"], c_nf_per_km=c_nf, g_us_per_km=0.0,
            max_i_ka=line.get("max_current_ka", float("nan")), name=line["line_id"])
    for trafo in network["transformers"]:
        # elements/trafo.html, Impedance Values: z_k = vk_percent/100 and
        # r_k = vkr_percent/100, both on the transformer rating sn_mva and
        # referred to the LV side (Z_ref = vn_lv_kv^2 / sn_mva). The contract
        # r_pu and x_pu use the same bases, so vkr% = 100*r_pu and
        # vk% = 100*|r_pu + j*x_pu|; pandapower recovers x_k = sqrt(z_k^2 - r_k^2).
        # elements/trafo.html, Tap Changer (Ratio): n_tap = 1 + (tap_pos -
        # tap_neutral) * tap_step_percent/100 multiplies the HV reference
        # voltage when tap_side="hv". tap_pos=1 and tap_neutral=0 give
        # n_tap = tap_ratio, which multiplies the nominal turns ratio as the
        # contract specifies, while the impedance stays on the LV side.
        # elements/trafo.html, Transformer Ratio: with voltage angles enabled the
        # complex ratio is n * exp(j*shift_degree*pi/180), so the LV angle lags
        # the HV angle by shift_degree at no load.
        pp.create_transformer_from_parameters(net, buses[trafo["hv_bus"]], buses[trafo["lv_bus"]],
            sn_mva=trafo["sn_mva"], vn_hv_kv=trafo["vn_hv_kv"], vn_lv_kv=trafo["vn_lv_kv"],
            vkr_percent=100 * trafo["r_pu"], vk_percent=100 * math.hypot(trafo["r_pu"], trafo["x_pu"]),
            pfe_kw=0, i0_percent=0, shift_degree=trafo.get("phase_shift_degree", 0),
            tap_side="hv", tap_neutral=0, tap_pos=1,
            tap_step_percent=100 * (trafo.get("tap_ratio", 1) - 1), tap_changer_type="Ratio",
            name=trafo["transformer_id"])
    # elements/load.html: loads use the consumer system, positive p_mw and q_mvar
    # are consumption, the same sign convention as the contract.
    for load in network["loads"]:
        pp.create_load(net, buses[load["bus_id"]], p_mw=load["p_mw"], q_mvar=load["q_mvar"],
                       name=load["load_id"])
    # elements/gen.html: a voltage-controlled (PV) generator with fixed p_mw.
    for gen in network["generators"]:
        pp.create_gen(net, buses[gen["bus_id"]], p_mw=gen["p_mw"], vm_pu=gen["vm_setpoint_pu"],
                      min_q_mvar=gen.get("q_min_mvar", float("nan")),
                      max_q_mvar=gen.get("q_max_mvar", float("nan")), name=gen["generator_id"])
    # elements/ext_grid.html: the slack reference with voltage magnitude and angle.
    for grid in network["external_grids"]:
        pp.create_ext_grid(net, buses[grid["bus_id"]], vm_pu=grid["vm_setpoint_pu"],
                           va_degree=grid["va_setpoint_degree"], name=grid["external_grid_id"])
    # elements/shunt.html, Electric Model: p_mw + j*q_mvar is the power at
    # v = 1 pu, so y_shunt = S_ref / S_N in per unit; positive is consumption,
    # matching the contract "power at nominal bus voltage".
    for shunt in network["shunts"]:
        pp.create_shunt(net, buses[shunt["bus_id"]], p_mw=shunt["p_mw"], q_mvar=shunt["q_mvar"],
                        name=shunt["shunt_id"])
    return net


def _mismatch(net):
    """Largest P/Q residual of the PV and PQ equations at the last iterate, in MVA.

    pandapower 3.5.6 pypower/newtonpf.py forms F from V*conj(Ybus*V) - Sbus.
    """
    internal = net._ppc["internal"]
    voltage = internal["V"]
    mismatch = voltage * np.conj(internal["Ybus"] @ voltage) - internal["Sbus"]
    pv, pq = internal["pv"], internal["pq"]
    residual = np.r_[mismatch[pv].real, mismatch[pq].real, mismatch[pq].imag]
    return float(np.max(np.abs(residual), initial=0) * net.sn_mva)


def _not_converged(network, request, iterations, mismatch_mva):
    return diagnostic(
        "NON_CONVERGENCE",
        f"Newton-Raphson did not reach {request['tolerance_mva']:g} MVA within {iterations} iterations "
        f"(largest mismatch {mismatch_mva:.6g} MVA). Likely causes: load beyond the network's transfer "
        "limit (voltage collapse), generator or slack setpoints that cannot be met, extreme tap ratios, "
        "very high R/X or near-zero impedance branches, or too few iterations.",
        "network", network["network_id"], "convergence")


def solve(network: dict, request: dict, input_hash: str | None = None) -> Outcome[dict]:
    """Solve and return an Outcome; value is None only when the inputs are unsolvable."""
    errors = _preflight(network, request)
    if errors:
        return Outcome(diagnostics=errors)
    notes = _model_notes(network)
    try:
        net = _convert(network)
        converged = True
        try:
            # powerflow/ac.html: runpp options. Flat start, polar NR, voltage
            # angles on so phase shifts apply, reactive limits trigger PV to PQ
            # switching, constant-power loads only. See powerflow/ac.html,
            # enforce_q_lims: additional NR solves fix Q at the declared bound.
            pp.runpp(net, algorithm="nr", init="flat", calculate_voltage_angles=True,
                     max_iteration=request["max_iterations"], tolerance_mva=request["tolerance_mva"],
                     trafo_model="pi", enforce_q_lims=True, voltage_depend_loads=False,
                     check_connectivity=False, numba=False)
        except pp.LoadflowNotConverged:
            converged = False
        iterations = int(net._ppc["iterations"])
        mismatch = _mismatch(net)
        if not math.isfinite(mismatch):
            # The contract needs a finite number; report the largest float and
            # say so rather than invent a value.
            notes.append(diagnostic("NONFINITE_ITERATE",
                                    "The last Newton-Raphson iterate is not finite; largest_mismatch_mva reports "
                                    "the largest representable float", "network", network["network_id"],
                                    "convergence"))
            mismatch = sys.float_info.max
        if not converged:
            notes.append(_not_converged(network, request, iterations, mismatch))
        buses, branches = [], []
        if converged:
            for i, gen in enumerate(network["generators"]):
                q = float(net.res_gen.loc[i, "q_mvar"])
                for field in ("q_min_mvar", "q_max_mvar"):
                    if field in gen and math.isclose(q, gen[field], rel_tol=0, abs_tol=1e-8):
                        voltage = float(net.res_gen.loc[i, "vm_pu"])
                        notes.append(Diagnostic("GENERATOR_Q_LIMIT",
                            f"Generator at {field}={gen[field]:g} Mvar; actual Q={q:.12g} Mvar. "
                            f"Reactive capability limits voltage control: actual voltage {voltage:.12g} pu, "
                            f"setpoint {gen['vm_setpoint_pu']:g} pu (PV to PQ when constrained).",
                            {"element_type": "generators", "element_id": gen["generator_id"],
                             "field": field}, "warning"))
                        break
            for i, bus in enumerate(network["buses"]):
                row = net.res_bus.loc[i]
                buses.append({"bus_id": bus["bus_id"], "vm_pu": float(row.vm_pu), "va_degree": float(row.va_degree)})
            # elements/line.html and elements/trafo.html, Result Parameters:
            # p_*_mw and q_*_mvar are flows into the branch at each terminal,
            # pl_mw and ql_mvar are the losses.
            for kind, table, ends in (("line", net.res_line, ("from", "to")),
                                      ("transformer", net.res_trafo, ("hv", "lv"))):
                for i, item in enumerate(network["lines" if kind == "line" else "transformers"]):
                    row = table.loc[i]
                    loading = float(row.loading_percent)
                    branches.append({"branch_id": item[kind + "_id"], "branch_type": kind,
                        "p_from_mw": float(row[f"p_{ends[0]}_mw"]), "q_from_mvar": float(row[f"q_{ends[0]}_mvar"]),
                        "p_to_mw": float(row[f"p_{ends[1]}_mw"]), "q_to_mvar": float(row[f"q_{ends[1]}_mvar"]),
                        "p_loss_mw": float(row.pl_mw), "q_loss_mvar": float(row.ql_mvar),
                        "loading_pct": loading if math.isfinite(loading) else None})
        result = {"schema_version": "0.1.0", "result_id": request["request_id"] + "-pandapower",
                  "network_id": network["network_id"], "bus_results": buses, "branch_results": branches,
                  "convergence": {"converged": converged, "iterations": iterations,
                                  "largest_mismatch_mva": mismatch},
                  "diagnostics": [d.to_dict() for d in notes],
                  "provenance": provenance(SOLVER_NAME, pp.__version__,
                                           input_hash or hash_inputs({"network": network, "request": request}))}
        problems = validate(result, "power/loadflow-result")
        if problems:
            return Outcome(diagnostics=problems)
        return Outcome(result, notes)
    except (ValueError, TypeError, KeyError, ArithmeticError, np.linalg.LinAlgError) as exc:
        return Outcome(diagnostics=[*notes, diagnostic("SOLVER_FAILURE", str(exc), "network",
                                                       network["network_id"], "solver")])


def run_loadflow_file(network_path: str | Path, request: dict) -> dict:
    """Solve a network file and return a contract loadflow-result.

    Same signature and result shape as qe_power.textbook.run_loadflow_file:
    provenance hashes the exact network file bytes. A non-converging case
    returns converged=false with a NON_CONVERGENCE diagnostic. Inputs that cannot
    be solved at all raise LoadflowInputError (a ValueError) with diagnostics.
    """
    path = Path(network_path)
    try:
        data = path.read_bytes()
        network = json.loads(data)
    except (OSError, ValueError, UnicodeError) as exc:
        raise LoadflowInputError([diagnostic("INPUT_READ", str(exc), "file", path.name, "content")]) from exc
    outcome = solve(network, request, hashlib.sha256(data).hexdigest())
    if outcome.value is None:
        raise LoadflowInputError(outcome.diagnostics)
    return outcome.value
