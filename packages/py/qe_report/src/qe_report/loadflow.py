"""Render a contract-shaped load-flow result as a readable Markdown study report.

The report is a pure function of its inputs: the network, the request, the result
and the voltage limits. It performs no engineering calculation beyond sums and
unit conversions of values already present in those inputs, so every number in
the report can be traced back to the solver output or the network data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

MESSAGE_LIMIT = 160


@dataclass(frozen=True)
class VoltageLimits:
    """Acceptable steady-state bus voltage band in per unit."""

    vmin_pu: float = 0.95
    vmax_pu: float = 1.05

    def __post_init__(self) -> None:
        if not 0 < self.vmin_pu < self.vmax_pu:
            raise ValueError("Voltage limits must satisfy 0 < vmin_pu < vmax_pu")

    def flag(self, vm_pu: float) -> str:
        if vm_pu < self.vmin_pu:
            return "LOW"
        if vm_pu > self.vmax_pu:
            return "HIGH"
        return "ok"


def _fmt(value: float | None, digits: int = 4) -> str:
    if value is None:
        return "n/a"
    return f"{value:.{digits}f}"


def _table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines += ["| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |" for row in rows]
    return lines


def _branch_ends(network: dict[str, Any]) -> dict[str, tuple[str, str]]:
    ends = {line["line_id"]: (line["from_bus"], line["to_bus"]) for line in network["lines"]}
    ends.update(
        {trafo["transformer_id"]: (trafo["hv_bus"], trafo["lv_bus"])
         for trafo in network["transformers"]}
    )
    return ends


def source_outputs(network: dict[str, Any], result: dict[str, Any]) -> list[dict[str, Any]]:
    """Back-calculate what each source bus had to supply, from the solved branch flows.

    Power balance at bus k (Kirchhoff's current law in power form):
        S_source,k = sum(S_into_branches_leaving_k) + S_load,k + S_shunt,k * |V_k|^2
    p_from/q_from is the power entering a branch at its From bus, p_to/q_to at its To
    bus, so both already point away from the bus they are reported at. Shunt power
    is specified at nominal voltage, so it scales with |V|^2 (constant impedance).
    """
    vm = {bus["bus_id"]: bus["vm_pu"] for bus in result["bus_results"]}
    ends = _branch_ends(network)
    p_out: dict[str, float] = {}
    q_out: dict[str, float] = {}
    for branch in result["branch_results"]:
        if branch["branch_id"] not in ends:
            continue
        from_bus, to_bus = ends[branch["branch_id"]]
        p_out[from_bus] = p_out.get(from_bus, 0.0) + branch["p_from_mw"]
        q_out[from_bus] = q_out.get(from_bus, 0.0) + branch["q_from_mvar"]
        p_out[to_bus] = p_out.get(to_bus, 0.0) + branch["p_to_mw"]
        q_out[to_bus] = q_out.get(to_bus, 0.0) + branch["q_to_mvar"]
    for load in network["loads"]:
        p_out[load["bus_id"]] = p_out.get(load["bus_id"], 0.0) + load["p_mw"]
        q_out[load["bus_id"]] = q_out.get(load["bus_id"], 0.0) + load["q_mvar"]
    for shunt in network["shunts"]:
        v2 = vm.get(shunt["bus_id"], 1.0) ** 2
        p_out[shunt["bus_id"]] = p_out.get(shunt["bus_id"], 0.0) + shunt["p_mw"] * v2
        q_out[shunt["bus_id"]] = q_out.get(shunt["bus_id"], 0.0) + shunt["q_mvar"] * v2

    sources: list[dict[str, Any]] = []
    for grid in network["external_grids"]:
        bus = grid["bus_id"]
        sources.append({"source_id": grid["external_grid_id"], "kind": "grid", "bus_id": bus,
                        "p_mw": p_out.get(bus, 0.0), "q_mvar": q_out.get(bus, 0.0),
                        "q_min_mvar": None, "q_max_mvar": None, "shared_bus": False})
    grid_buses = {grid["bus_id"] for grid in network["external_grids"]}
    by_bus: dict[str, list[dict[str, Any]]] = {}
    for gen in network["generators"]:
        by_bus.setdefault(gen["bus_id"], []).append(gen)
    for bus, gens in by_bus.items():
        if bus in grid_buses:
            continue  # the grid absorbs the balance at a shared bus; no per-unit split
        q_min = [g.get("q_min_mvar") for g in gens]
        q_max = [g.get("q_max_mvar") for g in gens]
        sources.append({
            "source_id": ", ".join(g["generator_id"] for g in gens), "kind": "generator",
            "bus_id": bus, "p_mw": p_out.get(bus, 0.0), "q_mvar": q_out.get(bus, 0.0),
            "q_min_mvar": None if None in q_min else sum(q_min),
            "q_max_mvar": None if None in q_max else sum(q_max),
            "shared_bus": len(gens) > 1,
        })
    for source in sources:
        flag = "ok"
        if source["q_min_mvar"] is not None and source["q_mvar"] < source["q_min_mvar"]:
            flag = "BELOW Q MIN"
        if source["q_max_mvar"] is not None and source["q_mvar"] > source["q_max_mvar"]:
            flag = "ABOVE Q MAX"
        source["q_check"] = flag
    return sources


def summarise(
    network: dict[str, Any], result: dict[str, Any], limits: VoltageLimits
) -> dict[str, Any]:
    """Collect the headline figures used by the summary section and by callers."""
    vn_kv = {bus["bus_id"]: bus["vn_kv"] for bus in network["buses"]}
    violations = [
        bus for bus in result["bus_results"] if limits.flag(bus["vm_pu"]) != "ok"
    ]
    loads_p = sum(load["p_mw"] for load in network["loads"])
    loads_q = sum(load["q_mvar"] for load in network["loads"])
    loss_p = sum(branch["p_loss_mw"] for branch in result["branch_results"])
    loss_q = sum(branch["q_loss_mvar"] for branch in result["branch_results"])
    vm = [bus["vm_pu"] for bus in result["bus_results"]]
    sources = source_outputs(network, result)
    return {
        "sources": sources,
        "q_limit_breaches": [s for s in sources if s["q_check"] != "ok"],
        "converged": result["convergence"]["converged"],
        "bus_count": len(result["bus_results"]),
        "branch_count": len(result["branch_results"]),
        "load_p_mw": loads_p,
        "load_q_mvar": loads_q,
        "loss_p_mw": loss_p,
        "loss_q_mvar": loss_q,
        "loss_pct_of_load": (100.0 * loss_p / loads_p) if loads_p else None,
        "vm_min_pu": min(vm) if vm else None,
        "vm_max_pu": max(vm) if vm else None,
        "violations": violations,
        "vn_kv": vn_kv,
    }


def render_loadflow_report(
    *,
    project_name: str,
    network: dict[str, Any],
    request: dict[str, Any],
    result: dict[str, Any],
    limits: VoltageLimits | None = None,
) -> str:
    """Return the full Markdown report for one load-flow run."""
    limits = limits or VoltageLimits()
    facts = summarise(network, result, limits)
    convergence = result["convergence"]
    provenance = result["provenance"]
    status = "CONVERGED" if facts["converged"] else "NOT CONVERGED: results are not valid"

    out: list[str] = [f"# Load-flow study: {project_name}", ""]

    out += ["## 1. Summary", ""]
    out += _table(
        ["Item", "Value"],
        [
            ["Status", status],
            ["Network", result["network_id"]],
            ["Solver", f"{provenance['solver_name']} {provenance['solver_version']}"],
            ["Buses / branches", f"{facts['bus_count']} / {facts['branch_count']}"],
            ["Total load", f"{_fmt(facts['load_p_mw'], 3)} MW, {_fmt(facts['load_q_mvar'], 3)} Mvar"],
            ["Total series losses",
             f"{_fmt(facts['loss_p_mw'], 4)} MW, {_fmt(facts['loss_q_mvar'], 4)} Mvar"],
            ["Losses as % of load", _fmt(facts["loss_pct_of_load"], 2) + " %"
             if facts["loss_pct_of_load"] is not None else "n/a"],
            ["Voltage range", f"{_fmt(facts['vm_min_pu'])} to {_fmt(facts['vm_max_pu'])} pu"],
            ["Buses outside limits", str(len(facts["violations"]))],
            ["Sources outside reactive limits", str(len(facts["q_limit_breaches"]))],
        ],
    )
    out.append("")
    if facts["q_limit_breaches"]:
        names = ", ".join(s["source_id"] for s in facts["q_limit_breaches"])
        out += [
            f"> **Warning:** to hold their voltage setpoints, these sources must supply "
            f"reactive power outside their stated limits: {names} (see section 4). The solver does not enforce "
            "generator reactive limits, so this operating point is not achievable as "
            "specified. Revise the setpoint, the limits or the network before relying on "
            "these results.",
            "",
        ]

    out += ["## 2. Assumptions", ""]
    out += [
        "- Balanced three-phase steady state, solved as a positive-sequence (single-line) model.",
        f"- System base: {network['base_mva']} MVA. Per-unit voltages use each bus's nominal kV.",
        f"- Convergence tolerance: {request['tolerance_mva']} MVA; "
        f"iteration limit: {request['max_iterations']}.",
        f"- Initialisation: {request.get('initialization', 'flat')}.",
        f"- Acceptable voltage band: {limits.vmin_pu} to {limits.vmax_pu} pu "
        "(set with --vmin and --vmax).",
        "- Losses are the sum of line and transformer series losses reported by the solver. "
        "Shunt consumption is not counted as a loss.",
        "- Generator reactive power limits are checked by this report, not enforced by the "
        "solver: a PV bus holds its voltage setpoint whatever reactive power that needs.",
        "",
    ]

    out += ["## 3. Bus voltages", ""]
    rows = []
    for bus in result["bus_results"]:
        kv = facts["vn_kv"].get(bus["bus_id"])
        rows.append([
            bus["bus_id"],
            _fmt(kv, 2) if kv is not None else "n/a",
            _fmt(bus["vm_pu"]),
            _fmt(bus["vm_pu"] * kv, 3) if kv is not None else "n/a",
            _fmt(bus["va_degree"], 3),
            limits.flag(bus["vm_pu"]),
        ])
    out += _table(["Bus", "Nominal kV", "V (pu)", "V (kV)", "Angle (deg)", "Check"], rows)
    out.append("")

    out += ["## 4. Sources", ""]
    out.append("Back-calculated from the solved branch flows by power balance at each source "
               "bus. Positive values are supplied into the network.")
    out.append("")
    rows = []
    for source in facts["sources"]:
        limits_text = "n/a"
        if source["q_min_mvar"] is not None or source["q_max_mvar"] is not None:
            limits_text = f"{_fmt(source['q_min_mvar'], 3)} to {_fmt(source['q_max_mvar'], 3)}"
        rows.append([
            source["source_id"], source["kind"], source["bus_id"],
            _fmt(source["p_mw"]), _fmt(source["q_mvar"]), limits_text, source["q_check"],
        ])
    out += _table(["Source", "Kind", "Bus", "P (MW)", "Q (Mvar)", "Q limits (Mvar)", "Check"],
                  rows)
    out.append("")

    out += ["## 5. Branch flows", ""]
    out.append("Positive P flows from the From bus into the branch. For transformers, From is "
               "the HV side.")
    out.append("")
    ends = _branch_ends(network)
    rows = []
    for branch in result["branch_results"]:
        from_bus, to_bus = ends.get(branch["branch_id"], ("?", "?"))
        rows.append([
            branch["branch_id"], branch["branch_type"], from_bus, to_bus,
            _fmt(branch["p_from_mw"]), _fmt(branch["q_from_mvar"]),
            _fmt(branch["p_to_mw"]), _fmt(branch["q_to_mvar"]),
            _fmt(branch["p_loss_mw"]), _fmt(branch["q_loss_mvar"]),
            _fmt(branch["loading_pct"], 1),
        ])
    out += _table(
        ["Branch", "Type", "From", "To", "P from (MW)", "Q from (Mvar)", "P to (MW)",
         "Q to (Mvar)", "P loss (MW)", "Q loss (Mvar)", "Loading (%)"],
        rows,
    )
    out.append("")

    out += ["## 6. Losses", ""]
    out.append(f"Total series losses: **{_fmt(facts['loss_p_mw'], 4)} MW** and "
               f"**{_fmt(facts['loss_q_mvar'], 4)} Mvar**.")
    out.append("")

    out += ["## 7. Convergence", ""]
    out += _table(
        ["Item", "Value"],
        [
            ["Converged", "yes" if convergence["converged"] else "no"],
            ["Iterations", str(convergence["iterations"])],
            ["Largest remaining mismatch", f"{convergence['largest_mismatch_mva']:.3e} MVA"],
            ["Tolerance", f"{request['tolerance_mva']} MVA"],
        ],
    )
    out.append("")

    out += ["## 8. Diagnostics", ""]
    if result["diagnostics"]:
        rows = []
        for item in result["diagnostics"]:
            message = item["message"]
            if len(message) > MESSAGE_LIMIT:
                message = message[:MESSAGE_LIMIT] + " ... (full text in results.json)"
            rows.append([item["severity"], item["code"], message])
        out += _table(["Severity", "Code", "Message"], rows)
    else:
        out.append("None.")
    out.append("")

    out += ["## 9. Provenance", ""]
    out += _table(
        ["Item", "Value"],
        [
            ["Solver", provenance["solver_name"]],
            ["Solver version", provenance["solver_version"]],
            ["Input SHA-256", f"`{provenance['input_hash_sha256']}`"],
            ["Run time (UTC)", provenance["timestamp"]],
            ["Request", request["request_id"]],
            ["Result", result["result_id"]],
        ],
    )
    out.append("")
    return "\n".join(out)
