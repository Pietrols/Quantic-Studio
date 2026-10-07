from __future__ import annotations

import math

import numpy as np
from qe_core import Diagnostic, Outcome, validate
from qe_core.project import validate_network
from qe_core.provenance import hash_inputs, provenance
from qe_core.validation import diagnostic

import pandapower as pp


def _preflight(network, request):
    errors = validate_network(network) + validate(request, "power/loadflow-request")
    if errors:
        return errors
    if request.get("initialization", "flat") != "flat":
        errors.append(diagnostic("UNSUPPORTED_INITIALIZATION", "No compatible prior result was supplied",
                                 "request", request["request_id"], "initialization"))
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
                errors.append(diagnostic("VOLTAGE_BASE", "Lines require equal endpoint voltage bases", kind, identifier, "to_bus"))
            r, x = (item["r_ohm_per_km"], item["x_ohm_per_km"]) if kind == "lines" else (item["r_pu"], item["x_pu"])
            if r == 0 and x == 0 or kind == "transformers" and x <= 0:
                errors.append(diagnostic("UNSUPPORTED_IMPEDANCE", "Zero impedance or nonpositive transformer reactance is unsupported", kind, identifier, "impedance"))
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
            errors.append(diagnostic("SLACK_COUNT", "Each connected component needs exactly one external-grid bus", "network", network["network_id"], "external_grids"))
    if len(sources) != len(network["external_grids"]):
        errors.append(diagnostic("DUPLICATE_CONTROL", "Only one external grid per bus is supported", "network", network["network_id"], "external_grids"))
    if len(generators) != len(network["generators"]):
        errors.append(diagnostic("DUPLICATE_CONTROL", "Only one generator per bus is supported", "network", network["network_id"], "generators"))
    for bus in buses.values():
        expected = "slack" if bus["bus_id"] in sources else "pv" if bus["bus_id"] in generators else "pq"
        if bus["bus_type"] != expected or bus["bus_id"] in sources & generators:
            errors.append(diagnostic("BUS_CONTROL", f"Bus type must match source controls ({expected})", "bus", bus["bus_id"], "bus_type"))
    return errors


def _convert(network):
    net = pp.create_empty_network(sn_mva=network["base_mva"])
    buses = {b["bus_id"]: pp.create_bus(net, vn_kv=b["vn_kv"], name=b.get("name", b["bus_id"])) for b in network["buses"]}
    for line in network["lines"]:
        # pandapower Line / Electric Model: B = 2*pi*f*C. The internal
        # frequency cancels; contract B is already evaluated at study frequency.
        c_nf = line.get("b_us_per_km", 0) * 1000 / (2 * math.pi * net.f_hz)
        pp.create_line_from_parameters(net, buses[line["from_bus"]], buses[line["to_bus"]],
            length_km=line["length_km"], r_ohm_per_km=line["r_ohm_per_km"],
            x_ohm_per_km=line["x_ohm_per_km"], c_nf_per_km=c_nf,
            max_i_ka=line.get("max_current_ka", float("nan")), name=line["line_id"])
    for trafo in network["transformers"]:
        # pandapower Transformer / Electric Model and docs/specs/network.md:
        # vkr%=100*r_pu; vk%=100*abs(r_pu+j*x_pu), on transformer rating.
        pp.create_transformer_from_parameters(net, buses[trafo["hv_bus"]], buses[trafo["lv_bus"]],
            sn_mva=trafo["sn_mva"], vn_hv_kv=trafo["vn_hv_kv"], vn_lv_kv=trafo["vn_lv_kv"],
            vkr_percent=100*trafo["r_pu"], vk_percent=100*math.hypot(trafo["r_pu"], trafo["x_pu"]),
            pfe_kw=0, i0_percent=0, shift_degree=trafo.get("phase_shift_degree", 0),
            tap_side="hv", tap_neutral=0, tap_pos=1,
            tap_step_percent=100*(trafo.get("tap_ratio", 1)-1), tap_changer_type="Ratio",
            name=trafo["transformer_id"])
    for load in network["loads"]:
        pp.create_load(net, buses[load["bus_id"]], p_mw=load["p_mw"], q_mvar=load["q_mvar"])
    for gen in network["generators"]:
        pp.create_gen(net, buses[gen["bus_id"]], p_mw=gen["p_mw"], vm_pu=gen["vm_setpoint_pu"])
    for grid in network["external_grids"]:
        pp.create_ext_grid(net, buses[grid["bus_id"]], vm_pu=grid["vm_setpoint_pu"], va_degree=grid["va_setpoint_degree"])
    for shunt in network["shunts"]:
        pp.create_shunt(net, buses[shunt["bus_id"]], p_mw=shunt["p_mw"], q_mvar=shunt["q_mvar"])
    return net


def _mismatch(net):
    # P/Q residual on PV/PQ equations, in MVA, using the engine's last iterate.
    # pandapower 3.5.6 pypower/newtonpf.py: F from V*conj(Ybus*V)-Sbus.
    internal = net._ppc["internal"]
    voltage = internal["V"]
    mismatch = voltage * np.conj(internal["Ybus"] @ voltage) - internal["Sbus"]
    pv, pq = internal["pv"], internal["pq"]
    residual = np.r_[mismatch[pv].real, mismatch[pq].real, mismatch[pq].imag]
    value = float(np.max(np.abs(residual), initial=0) * net.sn_mva)
    if not math.isfinite(value):
        raise ValueError("Last power mismatch is not finite")
    return value


def solve(network: dict, request: dict, input_hash: str | None = None) -> Outcome[dict]:
    errors = _preflight(network, request)
    if errors:
        return Outcome(diagnostics=errors)
    notes = []
    for bus in network["buses"]:
        for field in ("vm_pu", "va_degree"):
            if field in bus:
                notes.append(Diagnostic("REFERENCE_NOT_INITIALIZATION", "Stored bus values are reference data; flat initialization requested",
                    {"element_type": "bus", "element_id": bus["bus_id"], "field": field}, "info"))
    for gen in network["generators"]:
        for field in ("p_min_mw", "p_max_mw", "q_min_mvar", "q_max_mvar"):
            if field in gen:
                notes.append(Diagnostic("LIMIT_NOT_ENFORCED", "Unconstrained load flow does not enforce this operating limit",
                    {"element_type": "generator", "element_id": gen["generator_id"], "field": field}, "warning"))
    if network["transformers"]:
        notes.append(Diagnostic("TRANSFORMER_MODEL", "Series impedance and ideal ratio model; no magnetizing branch is specified by contract", severity="info"))
    try:
        net = _convert(network)
        converged = True
        try:
            pp.runpp(net, algorithm="nr", init="flat", calculate_voltage_angles=True,
                     max_iteration=request["max_iterations"], tolerance_mva=request["tolerance_mva"],
                     trafo_model="pi", enforce_q_lims=False, check_connectivity=False, numba=False)
        except pp.LoadflowNotConverged:
            converged = False
            notes.append(diagnostic("LOADFLOW_NOT_CONVERGED", "Newton-Raphson iteration limit reached; inspect loading, impedances, controls and initial conditions",
                                    "network", network["network_id"], "convergence"))
        mismatch = _mismatch(net)
        buses, branches = [], []
        if converged:
            for i, bus in enumerate(network["buses"]):
                row = net.res_bus.loc[i]
                buses.append({"bus_id": bus["bus_id"], "vm_pu": float(row.vm_pu), "va_degree": float(row.va_degree)})
            for kind, table, ends in (("line", net.res_line, ("from", "to")),
                                      ("transformer", net.res_trafo, ("hv", "lv"))):
                for i, item in enumerate(network["lines" if kind == "line" else "transformers"]):
                    row = table.loc[i]
                    loading = float(row.loading_percent)
                    branches.append({"branch_id": item[kind+"_id"], "branch_type": kind,
                        "p_from_mw": float(row[f"p_{ends[0]}_mw"]), "q_from_mvar": float(row[f"q_{ends[0]}_mvar"]),
                        "p_to_mw": float(row[f"p_{ends[1]}_mw"]), "q_to_mvar": float(row[f"q_{ends[1]}_mvar"]),
                        "p_loss_mw": float(row.pl_mw), "q_loss_mvar": float(row.ql_mvar),
                        "loading_pct": loading if math.isfinite(loading) else None})
        result = {"schema_version": "0.1.0", "result_id": request["request_id"]+"-pandapower",
                  "network_id": network["network_id"], "bus_results": buses, "branch_results": branches,
                  "convergence": {"converged": converged, "iterations": int(net._ppc["iterations"]),
                                  "largest_mismatch_mva": mismatch},
                  "diagnostics": [d.to_dict() for d in notes],
                  "provenance": provenance("pandapower", pp.__version__, input_hash or hash_inputs({"network": network, "request": request}))}
        problems = validate(result, "power/loadflow-result")
        if problems:
            return Outcome(diagnostics=problems)
        return Outcome(result, notes)
    except (ValueError, TypeError, KeyError, ArithmeticError, np.linalg.LinAlgError) as exc:
        return Outcome(diagnostics=[*notes, diagnostic("SOLVER_FAILURE", str(exc), "network", network["network_id"], "solver")])
