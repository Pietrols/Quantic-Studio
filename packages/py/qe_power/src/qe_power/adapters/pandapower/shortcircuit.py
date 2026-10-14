"""Balanced bolted fault studies through pandapower's equivalent voltage source.

References are the 3.5.6 pages shortcircuit/{ikss,ip,ith,branch_elements,
voltage_source,run}.html. Source discrepancies are deliberately unavailable,
as approved by Peter on 2026-10-10, not resolved by guessing standard values.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from qe_core import Diagnostic, Outcome, validate
from qe_core.project import validate_network
from qe_core.provenance import hash_inputs, provenance
from qe_core.validation import diagnostic

import pandapower as pp
from pandapower.pypower.idx_bus import BASE_KV
from pandapower.pypower.idx_bus_sc import C_MAX, C_MIN, KAPPA, R_EQUIV, X_EQUIV
from pandapower.shortcircuit import calc_sc

CURRENTS = ("ikss_ka", "ip_ka", "ith_ka")
SQRT3 = math.sqrt(3)
# Agreement required between our hand arithmetic and the engine (relative).
TRACE_TOLERANCE = 1e-9


class ShortcircuitInputError(ValueError):
    """Malformed documents, as opposed to valid but unavailable calculations."""

    def __init__(self, diagnostics):
        self.diagnostics = diagnostics
        super().__init__("; ".join(d.message for d in diagnostics))


def _components(network):
    adjacency = {b["bus_id"]: set() for b in network["buses"]}
    for kind, ends in (("lines", ("from_bus", "to_bus")),
                       ("transformers", ("hv_bus", "lv_bus"))):
        for item in network[kind]:
            a, b = (item[k] for k in ends)
            adjacency[a].add(b)
            adjacency[b].add(a)
    pending = set(adjacency)
    while pending:
        component, queue = set(), [min(pending)]
        while queue:
            bus = queue.pop()
            if bus not in component:
                component.add(bus)
                queue.extend(adjacency[bus] - component)
        pending -= component
        sub = {k: network[k] for k in ("schema_version", "network_id", "base_mva")}
        sub["buses"] = [b for b in network["buses"] if b["bus_id"] in component]
        for kind, endpoint in (("lines", "from_bus"), ("transformers", "hv_bus"),
                               ("external_grids", "bus_id"), ("generators", "bus_id"),
                               ("loads", "bus_id"), ("shunts", "bus_id")):
            sub[kind] = [e for e in network[kind] if e[endpoint] in component]
        yield sub


def _factor(bus, case, request):
    # ikss.html voltage table and v3.5.6 build_bus._add_c_to_ppc.
    # Exactly 1 kV has no explicit boundary in the printed table: diagnose it.
    if bus["vn_kv"] == 1 or (case == "min" and bus["vn_kv"] < 1
                            and request["lv_tolerance_percent"] == 10):
        return None
    if bus["vn_kv"] < 1:
        return (1.05 if request["lv_tolerance_percent"] == 6 else 1.1) if case == "max" else 0.95
    return 1.1 if case == "max" else 1.0


def _impedance(r, x):
    return {"r_ohm": r, "x_ohm": x}


def _source_entry(network, request, case):
    """Impedance of the single fault-current source, in ohms at its own bus.

    External grid (Kasikci 2002, eq. 8.1 p. 48): Z_Q = c U_nQ^2 / S''_kQ,
    R_Q = Z_Q (R/X) / sqrt(1 + (R/X)^2), X_Q = Z_Q / sqrt(1 + (R/X)^2).
    Synchronous generator (Kasikci eq. 9.3 p. 76; Das eq. 8.11):
    K_G = (U_n / U_rG) c_max / (1 + x''_d sin phi_rG), Z_GK = K_G (R_G + j X''_d),
    with X''_d = x''_d U_rG^2 / S_rG. pandapower applies K_G with c_max in both cases.
    """
    buses = {b["bus_id"]: b for b in network["buses"]}
    for grid in network["external_grids"]:
        un = buses[grid["bus_id"]]["vn_kv"]
        c = _factor(buses[grid["bus_id"]], case, request)
        s_sc, rx = grid[f"s_sc_{case}_mva"], grid[f"rx_{case}"]
        z = c * un ** 2 / s_sc
        r, x = z * rx / math.hypot(1, rx), z / math.hypot(1, rx)
        return grid["bus_id"], {"element_type": "external_grids", "element_id": grid["external_grid_id"],
                                "inputs": {"c": c, "un_kv": un, "s_sc_mva": s_sc, "rx": rx},
                                **_impedance(r, x)}
    for gen in network["generators"]:
        bus = buses[gen["bus_id"]]
        c_max = _factor(bus, "max", request)
        sin_phi = math.sqrt(max(0.0, 1 - gen["cos_phi"] ** 2))
        xd_ohm = gen["xdss_pu"] * gen["vn_kv"] ** 2 / gen["sn_mva"]
        k_g = bus["vn_kv"] / gen["vn_kv"] * c_max / (1 + gen["xdss_pu"] * sin_phi)
        return gen["bus_id"], {"element_type": "generators", "element_id": gen["generator_id"],
                               "inputs": {"un_kv": bus["vn_kv"], "vn_kv": gen["vn_kv"], "sn_mva": gen["sn_mva"],
                                          "xdss_pu": gen["xdss_pu"], "rdss_ohm": gen["rdss_ohm"],
                                          "cos_phi": gen["cos_phi"], "c_max": c_max, "k_g": k_g},
                               **_impedance(k_g * gen["rdss_ohm"], k_g * xd_ohm)}
    raise ValueError("Component has no fault-current source")


def _branch_entry(kind, item, network, request, case):
    """Series impedance of one branch in ohms on its own side.

    Line: Z_L = (r' + j x') l, with the temperature factor applied to R in the
    minimum case. Transformer (Kasikci eq. 9.14 p. 79), on its LV side:
    Z_T = (r + j x) U_rLV^2 / S_rT, multiplied by K_T = 0.95 c_max / (1 + 0.6 x_T)
    in the maximum case, where c_max is that of the LV bus.
    """
    if kind == "lines":
        factor = 1.0
        return {"element_type": "lines", "element_id": item["line_id"],
                "inputs": {"length_km": item["length_km"], "r_ohm_per_km": item["r_ohm_per_km"],
                           "x_ohm_per_km": item["x_ohm_per_km"], "temperature_factor": factor},
                **_impedance(item["r_ohm_per_km"] * item["length_km"] * factor,
                             item["x_ohm_per_km"] * item["length_km"])}
    buses = {b["bus_id"]: b for b in network["buses"]}
    c_max_lv = _factor(buses[item["lv_bus"]], "max", request)
    k_t = 0.95 * c_max_lv / (1 + 0.6 * item["x_pu"]) if case == "max" else 1.0
    base = item["vn_lv_kv"] ** 2 / item["sn_mva"]
    return {"element_type": "transformers", "element_id": item["transformer_id"],
            "inputs": {"sn_mva": item["sn_mva"], "vn_hv_kv": item["vn_hv_kv"], "vn_lv_kv": item["vn_lv_kv"],
                       "r_pu": item["r_pu"], "x_pu": item["x_pu"], "c_max_lv": c_max_lv, "k_t": k_t},
            **_impedance(k_t * item["r_pu"] * base, k_t * item["x_pu"] * base)}


def _radial_chains(network, request, case):
    """For each bus of a single-source radial component, the series elements
    between source and bus, each referred to that bus's side by the squared rated
    transformer ratios crossed on the way (Kasikci eq. 8.2 p. 48: Z referred by 1/t_r^2)."""
    adjacency = {b["bus_id"]: [] for b in network["buses"]}
    for line in network["lines"]:
        adjacency[line["from_bus"]].append(("lines", line, line["to_bus"]))
        adjacency[line["to_bus"]].append(("lines", line, line["from_bus"]))
    for trafo in network["transformers"]:
        adjacency[trafo["hv_bus"]].append(("transformers", trafo, trafo["lv_bus"]))
        adjacency[trafo["lv_bus"]].append(("transformers", trafo, trafo["hv_bus"]))
    source_bus, source = _source_entry(network, request, case)
    chains = {source_bus: [{**source, "referral_factor": 1.0}]}
    queue = [source_bus]
    while queue:
        here = queue.pop()
        for kind, item, there in adjacency[here]:
            if there in chains:
                continue
            entries = [dict(e) for e in chains[here]]
            own = _branch_entry(kind, item, network, request, case)
            if kind == "transformers":
                rated = {item["hv_bus"]: item["vn_hv_kv"], item["lv_bus"]: item["vn_lv_kv"]}
                ratio2 = (rated[there] / rated[here]) ** 2
                for entry in entries:
                    entry["referral_factor"] *= ratio2
                own["referral_factor"] = 1.0 if there == item["lv_bus"] else (item["vn_hv_kv"] / item["vn_lv_kv"]) ** 2
            else:
                own["referral_factor"] = 1.0
            chains[there] = [*entries, own]
            queue.append(there)
    for entries in chains.values():
        for entry in entries:
            entry["r_referred_ohm"] = entry["r_ohm"] * entry["referral_factor"]
            entry["x_referred_ohm"] = entry["x_ohm"] * entry["referral_factor"]
    return chains


def _close(a, b):
    return abs(a - b) <= TRACE_TOLERANCE * max(abs(a), abs(b))


def _issues(network, request, case):
    issues = []
    buses = {b["bus_id"]: b for b in network["buses"]}

    def problem(code, message, kind, item, field):
        identifier = item["bus_id" if kind == "buses" else kind[:-1] + "_id"]
        issues.append(diagnostic(code, message, kind, identifier, field))

    if not network["external_grids"] and not network["generators"]:
        issues.append(diagnostic("DISCONNECTED_BUS", "Component has no fault-current source",
                                 "network", network["network_id"], "sources"))
    for bus in network["buses"]:
        if _factor(bus, case, request) is None:
            problem("VOLTAGE_FACTOR_UNAVAILABLE",
                    "Disputed LV minimum factor at 10% tolerance, or undocumented exact 1-kV boundary; "
                    "this connected component is unavailable", "buses", bus, "vn_kv")
    for grid in network["external_grids"]:
        for field in (f"s_sc_{case}_mva", f"rx_{case}"):
            if field not in grid:
                problem("MISSING_FAULT_DATA", "Explicit grid fault input is required",
                        "external_grids", grid, field)
        if grid.get("s_sc_min_mva", 0) > grid.get("s_sc_max_mva", math.inf):
            problem("FAULT_LEVEL_RANGE", "Minimum grid fault level exceeds maximum",
                    "external_grids", grid, "s_sc_min_mva")
    for line in network["lines"]:
        if line["from_bus"] == line["to_bus"]:
            problem("SELF_LOOP", "Branch endpoints must differ", "lines", line, "to_bus")
        if buses[line["from_bus"]]["vn_kv"] != buses[line["to_bus"]]["vn_kv"]:
            problem("VOLTAGE_BASE", "Line endpoints require equal nominal voltage", "lines", line, "to_bus")
        if line["x_ohm_per_km"] <= 0:
            problem("UNSUPPORTED_IMPEDANCE", "Inductive positive line reactance is required",
                    "lines", line, "x_ohm_per_km")
        if case == "min":
            if "end_temperature_celsius" not in line:
                problem("MISSING_FAULT_DATA", "Minimum fault requires explicit final conductor temperature",
                        "lines", line, "end_temperature_celsius")
            elif line["end_temperature_celsius"] != 20:
                problem("TEMPERATURE_CORRECTION_UNAVAILABLE",
                        "Documentation uses 0.04/K; pinned implementation uses 0.004/K. "
                        "Only explicit 20 C (unit correction) is supported pending verification",
                        "lines", line, "end_temperature_celsius")
    for trafo in network["transformers"]:
        if case == "min":
            problem("TRANSFORMER_CORRECTION_UNAVAILABLE",
                    "Public KT page omits the case distinction; pinned implementation applies KT only "
                    "to maximum faults. Minimum transformer correction needs a verified source",
                    "transformers", trafo, "correction")
        if trafo["hv_bus"] == trafo["lv_bus"]:
            problem("SELF_LOOP", "Branch endpoints must differ", "transformers", trafo, "lv_bus")
        if trafo["x_pu"] <= 0:
            problem("UNSUPPORTED_IMPEDANCE", "Positive transformer reactance is required",
                    "transformers", trafo, "x_pu")
        if trafo.get("power_station_unit") or trafo.get("oltc"):
            problem("STATION_MODEL_UNAVAILABLE", "Power-station/OLTC corrections are not verified in this slice",
                    "transformers", trafo, "power_station_unit" if trafo.get("power_station_unit") else "oltc")
    gen_buses = set()
    for gen in network["generators"]:
        for field in ("sn_mva", "vn_kv", "xdss_pu", "rdss_ohm", "cos_phi", "voltage_control_range_percent"):
            if field not in gen:
                problem("MISSING_FAULT_DATA", "Explicit synchronous-machine fault input is required",
                        "generators", gen, field)
        if gen["bus_id"] in gen_buses:
            problem("GENERATOR_MODEL_UNAVAILABLE", "Multiple synchronous machines on one bus are not verified",
                    "generators", gen, "bus_id")
        gen_buses.add(gen["bus_id"])
        if gen.get("power_station_transformer_id"):
            problem("STATION_MODEL_UNAVAILABLE", "Associated station correction is not verified",
                    "generators", gen, "power_station_transformer_id")
        # voltage_source.html prints the inverse voltage ratio to the pinned
        # ppc_conversion._add_gen_sc_z_kg_ks. Both agree at equal ratings and pg=0.
        if gen.get("vn_kv", buses[gen["bus_id"]]["vn_kv"]) != buses[gen["bus_id"]]["vn_kv"]:
            problem("GENERATOR_CORRECTION_UNAVAILABLE", "Generator and bus rated-voltage ratios disagree in sources",
                    "generators", gen, "vn_kv")
        if gen.get("voltage_control_range_percent", 0) != 0:
            problem("GENERATOR_CORRECTION_UNAVAILABLE", "Nonzero generator voltage-range correction lacks agreed reference",
                    "generators", gen, "voltage_control_range_percent")
    return issues


def _convert(network, request, case):
    net = pp.create_empty_network(sn_mva=network["base_mva"], f_hz=request["frequency_hz"])
    buses = {b["bus_id"]: pp.create_bus(net, vn_kv=b["vn_kv"], name=b["bus_id"])
             for b in network["buses"]}
    for grid in network["external_grids"]:
        pp.create_ext_grid(net, buses[grid["bus_id"]], name=grid["external_grid_id"],
                           **{k: grid[k] for k in (f"s_sc_{case}_mva", f"rx_{case}")})
    for line in network["lines"]:
        # branch_elements.html: series ohms, no line shunt admittance in SC.
        pp.create_line_from_parameters(net, buses[line["from_bus"]], buses[line["to_bus"]],
            length_km=line["length_km"], r_ohm_per_km=line["r_ohm_per_km"],
            x_ohm_per_km=line["x_ohm_per_km"], c_nf_per_km=0, max_i_ka=float("nan"),
            name=line["line_id"], endtemp_degree=line.get("end_temperature_celsius", float("nan")))
    for trafo in network["transformers"]:
        # Own-rating pu -> percent, corrected by KT inside calc_sc. Nominal
        # ratio is intentional: branch_elements.html ignores tap positions.
        pp.create_transformer_from_parameters(net, buses[trafo["hv_bus"]], buses[trafo["lv_bus"]],
            sn_mva=trafo["sn_mva"], vn_hv_kv=trafo["vn_hv_kv"], vn_lv_kv=trafo["vn_lv_kv"],
            vk_percent=100 * math.hypot(trafo["r_pu"], trafo["x_pu"]),
            vkr_percent=100 * trafo["r_pu"], pfe_kw=0, i0_percent=0,
            shift_degree=trafo.get("phase_shift_degree", 0), power_station_unit=False,
            name=trafo["transformer_id"])
    for gen in network["generators"]:
        # elements/gen.html: sn and vn define the machine base, rdss is ohms.
        pp.create_gen(net, buses[gen["bus_id"]], p_mw=gen["p_mw"], vm_pu=gen["vm_setpoint_pu"],
            name=gen["generator_id"], pg_percent=gen["voltage_control_range_percent"],
            **{k: gen[k] for k in ("sn_mva", "vn_kv", "xdss_pu", "rdss_ohm", "cos_phi")})
    return net, buses


def _status(rows):
    available = [r[k] is not None for r in rows for k in CURRENTS]
    return "success" if all(available) else "partial" if any(available) else "failed"


def _unavailable(row, notes, code, reason, fields=CURRENTS):
    for field in fields:
        row[field] = None
        notes.append(diagnostic(code, reason, "buses", row["bus_id"], field))
    if row.get("ikss_ka") is None:
        row["trace"] = None


def _calculate_component(network, request, case):
    notes = _issues(network, request, case)
    rows = [{"bus_id": b["bus_id"], "voltage_factor": _factor(b, case, request),
             **dict.fromkeys(CURRENTS), "trace": None} for b in network["buses"]]
    nominal = {b["bus_id"]: b["vn_kv"] for b in network["buses"]}
    for row in rows:
        if row["voltage_factor"] is None:
            _unavailable(row, notes, "VOLTAGE_FACTOR_UNAVAILABLE", "No agreed voltage factor for this condition",
                         ("voltage_factor",))
    if notes:
        reason = "; ".join(dict.fromkeys(n.message for n in notes))
        for row in rows:
            _unavailable(row, notes, "FAULT_INPUT_UNAVAILABLE", reason)
        return rows, notes
    source_count = len(network["external_grids"]) + len(network["generators"])
    radial = len(network["lines"]) + len(network["transformers"]) == len(rows) - 1 and source_count == 1
    # No numerical claim of far-from-generator behavior in any component
    # containing a synchronous machine. Ik'' remains independently useful.
    far = not network["generators"]
    duties = radial and far
    try:
        net, buses = _convert(network, request, case)
        calc_sc(net, fault="3ph", case=case, lv_tol_percent=request["lv_tolerance_percent"],
                ip=duties, ith=duties and request["frequency_hz"] == 50,
                tk_s=request["fault_duration_s"], topology="radial" if radial else "auto",
                r_fault_ohm=0, x_fault_ohm=0, check_connectivity=True, use_pre_fault_voltage=False)
        chains = _radial_chains(network, request, case) if radial else {}
        base_mva = float(net._ppc["baseMVA"])
        for row in rows:
            index = buses[row["bus_id"]]
            actual = net.res_bus_sc.loc[index]
            ppc_index = net._pd2ppc_lookups["bus"][index]
            applied = float(net._ppc["bus"][ppc_index, C_MAX if case == "max" else C_MIN])
            if not math.isclose(applied, row["voltage_factor"], rel_tol=0, abs_tol=1e-12):
                _unavailable(row, notes, "ENGINE_FACTOR_MISMATCH", "Engine factor differs from verified reference",
                             ("voltage_factor", *CURRENTS))
                continue
            ikss = float(actual.ikss_ka)
            if not math.isfinite(ikss) or ikss <= 0:
                _unavailable(row, notes, "NONFINITE_FAULT_RESULT", "Source-connected bus lacks positive finite Ik''")
                continue
            row["ikss_ka"] = ikss
            # Worked calculation: Thevenin impedance at the fault bus in ohms,
            # Ik'' = c U_n / (sqrt(3) |Z_k|) (Kasikci section 11.2 p. 92). For a radial
            # component our own element sum must agree with the engine.
            base_kv = float(net._ppc["bus"][ppc_index, BASE_KV])
            z_engine = complex(float(net._ppc["bus"][ppc_index, R_EQUIV]),
                               float(net._ppc["bus"][ppc_index, X_EQUIV])) * base_kv ** 2 / base_mva
            elements = chains.get(row["bus_id"], [])
            z_k = complex(sum(e["r_referred_ohm"] for e in elements),
                          sum(e["x_referred_ohm"] for e in elements)) if elements else z_engine
            un = nominal[row["bus_id"]]
            c = row["voltage_factor"]
            if (elements and not (_close(z_k.real, z_engine.real) and _close(z_k.imag, z_engine.imag))) \
                    or not _close(c * un / (SQRT3 * abs(z_k)), ikss):
                _unavailable(row, notes, "TRACE_MISMATCH",
                             "Hand-summed impedance or c*Un/(sqrt(3)|Zk|) disagrees with the engine")
                continue
            row["trace"] = {"un_kv": un, "voltage_factor": c, "source_voltage_kv": c * un / SQRT3,
                            "impedance_basis": "radial-sum" if elements else "engine-thevenin",
                            "elements": elements, "zk_r_ohm": z_k.real, "zk_x_ohm": z_k.imag,
                            "zk_ohm": abs(z_k), "rx_ratio": z_k.real / z_k.imag if z_k.imag > 0 else None,
                            "kappa": None, "kappa_method": None, "m": None, "n": None}
            if not duties:
                _unavailable(row, notes, "NEAR_GENERATOR_DUTY" if not far else "MESH_DUTY_UNAVAILABLE",
                    "Far-from-generator duties cannot be established" if not far else
                    "Peak/thermal reference verified only for a radial component with one source",
                    ("ip_ka", "ith_ka"))
                continue
            row["ip_ka"] = float(actual.ip_ka)
            # kappa = 1.02 + 0.98 exp(-3 R/X), ip = kappa sqrt(2) Ik'' (Kasikci eqs. 11.22, 11.23 p. 98).
            kappa = 1.02 + 0.98 * math.exp(-3 * row["trace"]["rx_ratio"])
            if not (_close(kappa, float(net._ppc["bus"][ppc_index, KAPPA]))
                    and _close(kappa * math.sqrt(2) * ikss, row["ip_ka"])):
                _unavailable(row, notes, "TRACE_MISMATCH", "kappa or ip disagrees with the hand equation",
                             ("ip_ka", "ith_ka"))
                continue
            row["trace"].update(kappa=kappa, kappa_method="radial")
            if request["frequency_hz"] != 50:
                _unavailable(row, notes, "THERMAL_FREQUENCY_UNAVAILABLE", "Pinned thermal implementation hardcodes 50 Hz",
                             ("ith_ka",))
            elif float(net._ppc["bus"][ppc_index, KAPPA]) > 1.99:
                # currents._calc_ith sets m=0 here, unlike the printed equation.
                _unavailable(row, notes, "THERMAL_FACTOR_UNAVAILABLE", "Engine m=0 shortcut at kappa>1.99 lacks agreed reference",
                             ("ith_ka",))
            else:
                row["ith_ka"] = float(actual.ith_ka)
                # ith.html: stable evaluation detects cancellation in the
                # engine's exp(...)-1 for extremely short declared durations.
                kappa = float(net._ppc["bus"][ppc_index, KAPPA])
                a = math.log(kappa - 1)
                duration = request["fault_duration_s"]
                m = math.expm1(4 * 50 * duration * a) / (2 * 50 * duration * a)
                reference = ikss * math.sqrt(1 + m)
                if not math.isclose(row["ith_ka"], reference, rel_tol=1e-10, abs_tol=1e-10):
                    _unavailable(row, notes, "THERMAL_EQUATION_MISMATCH",
                                 "Engine thermal duty disagrees with stable documented equation", ("ith_ka",))
                else:
                    # Ith = Ik'' sqrt(m + n), n = 1 far from generators (Kasikci eqs. 13.1, 13.2 p. 117).
                    row["trace"].update(m=m, n=1.0)
            for field in ("ip_ka", "ith_ka"):
                if row[field] is not None and (not math.isfinite(row[field]) or row[field] < 0):
                    _unavailable(row, notes, "NONFINITE_FAULT_RESULT", "Duty is not a finite nonnegative magnitude", (field,))
    except (ValueError, TypeError, KeyError, ArithmeticError, UserWarning, np.linalg.LinAlgError) as exc:
        for row in rows:
            _unavailable(row, notes, "SOLVER_FAILURE", str(exc))
    return rows, notes


def solve_shortcircuit(network: dict, request: dict) -> Outcome[dict]:
    errors = validate_network(network) + validate(request, "power/shortcircuit-request")
    if errors:
        return Outcome(diagnostics=errors)
    notes = []
    for kind, key in (("loads", "load_id"), ("shunts", "shunt_id")):
        for item in network[kind]:
            notes.append(Diagnostic("NEGLECTED_OPERATING_ELEMENT",
                "Loads/shunts have no contribution in the equivalent-voltage-source method; "
                "motor or converter contributions are not represented by this contract",
                {"element_type": kind, "element_id": item[key], "field": "model"}, "warning"))
    for trafo in network["transformers"]:
        if "tap_ratio" in trafo:
            notes.append(Diagnostic("NOMINAL_TRANSFORMER_RATIO", "Fault model uses nominal ratio, ignores load-flow tap position",
                {"element_type": "transformers", "element_id": trafo["transformer_id"], "field": "tap_ratio"}, "info"))
    cases = []
    for case in request["cases"]:
        rows, case_notes = [], []
        for component in _components(network):
            values, issues = _calculate_component(component, request, case)
            rows.extend(values)
            case_notes.extend(issues)
        order = {b["bus_id"]: i for i, b in enumerate(network["buses"])}
        rows.sort(key=lambda row: order[row["bus_id"]])
        cases.append({"case": case, "status": _status(rows), "bus_results": rows,
                      "diagnostics": [d.to_dict() for d in case_notes]})
    statuses = [c["status"] for c in cases]
    result = {"schema_version": "0.3.0", "result_id": request["request_id"] + "-pandapower",
        "network_id": network["network_id"], **{k: request[k] for k in
            ("fault_type", "fault_duration_s", "frequency_hz", "lv_tolerance_percent")},
        "status": "success" if all(s == "success" for s in statuses) else
                  "failed" if all(s == "failed" for s in statuses) else "partial",
        "case_results": cases,
        "assumptions": [
            "Balanced bolted three-phase positive-sequence equivalent-voltage-source method; no pre-fault load flow.",
            "Maximum transformer KT=0.95*cmax_LV/(1+0.6*xT), on its own rating; minimum transformer duties unavailable pending case-basis verification.",
            "Nominal transformer ratio; no magnetizing or branch shunt admittance.",
            "Grid strength and R/X are explicit per case; operating setpoints and loads/shunts do not define fault contribution.",
            "Currents are kA: initial symmetrical RMS Ik'', instantaneous peak ip, equivalent thermal RMS Ith for the requested duration.",
            "Peak/thermal verified only for radial single-source components without synchronous generators; n=1.",
            "Disputed LV minimum at 10% tolerance and exact 1-kV boundary block affected connected components.",
            "Minimum line correction supported only at explicit 20 C; 60-Hz Ith and kappa>1.99 thermal shortcut are unavailable.",
            "Synchronous Ik'' limited to equal machine/bus rated voltages and explicit zero voltage-control range; station corrections unavailable.",
            "Null means unavailable, never safe zero. IEC 60909-0 is not supplied; no independent standards certification.",
        ], "diagnostics": [d.to_dict() for d in notes],
        "provenance": provenance("pandapower", pp.__version__, hash_inputs({"network": network, "request": request}))}
    problems = validate(result, "power/shortcircuit-result")
    if problems:
        return Outcome(diagnostics=problems)
    all_notes = [*notes, *(Diagnostic(**d) for c in cases for d in c["diagnostics"])]
    return Outcome(result, all_notes)


def run_shortcircuit_file(network_path: str | Path, request: dict) -> dict:
    path = Path(network_path)
    try:
        network = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        raise ShortcircuitInputError([diagnostic("INPUT_READ", str(exc), "file", path.name, "content")]) from exc
    outcome = solve_shortcircuit(network, request)
    if outcome.value is None:
        raise ShortcircuitInputError(outcome.diagnostics)
    return outcome.value
