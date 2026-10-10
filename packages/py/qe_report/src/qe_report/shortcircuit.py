"""Markdown fault report; no solver or standard constants are recomputed here."""
from __future__ import annotations

from .loadflow import _fmt, _table


def render_shortcircuit_report(*, project_name, network, request, result):
    out = [f"# Three-phase short-circuit study: {project_name}", "",
           f"Status: **{result['status'].upper()}**", "",
           "Unavailable values are shown as n/a, not zero. Partial or failed studies "
           "must not be treated as complete equipment-duty verification.", "",
           "Ik'' is initial symmetrical RMS current, ip is instantaneous peak current, "
           "and Ith is equivalent thermal RMS current. All currents are in kA. "
           "No breaker rating, clearing time or pass/fail limit is inferred.", "",
           "## Request and assumptions", ""]
    out += _table(["Input", "Value"], [
        ["Network", network["network_id"]], ["Fault", result["fault_type"]],
        ["Cases", ", ".join(request["cases"])],
        ["Fault duration (s)", str(result["fault_duration_s"])],
        ["Frequency (Hz)", str(result["frequency_hz"])],
        ["LV tolerance (%)", str(result["lv_tolerance_percent"])],
    ])
    out += ["", *[f"- {a}" for a in result["assumptions"]], "",
            "## Equipment inputs", "",
            "Transformer r/x are pu on its own rated MVA and LV kV, not on the system base. "
            "Machine xdss uses its own rated MVA/kV; machine rdss is ohms. "
            "External-grid fault strength is three-phase MVA. Missing data are not defaults.", ""]
    for kind, key in (("external_grids", "external_grid_id"), ("transformers", "transformer_id"),
                      ("lines", "line_id"), ("generators", "generator_id")):
        out += [f"### {kind.replace('_', ' ').title()}", ""]
        rows = [[e[key], field, str(value)] for e in network[kind]
                for field, value in e.items() if field != key]
        out += _table(["Element", "Field", "Input"], rows) if rows else ["None."]
        out.append("")
    nominal = {b["bus_id"]: b["vn_kv"] for b in network["buses"]}
    for case in result["case_results"]:
        out += [f"## {case['case'].title()}imum case: {case['status'].upper()}", ""]
        out += _table(["Bus", "Nominal kV", "Voltage factor c", "Ik'' (kA RMS)",
                       "ip (kA peak)", "Ith (kA RMS)"], [
            [b["bus_id"], _fmt(nominal[b["bus_id"]], 3), _fmt(b["voltage_factor"], 3),
             _fmt(b["ikss_ka"], 6), _fmt(b["ip_ka"], 6), _fmt(b["ith_ka"], 6)]
            for b in case["bus_results"]])
        out += ["", "### Case diagnostics", ""]
        out += _diagnostics(case["diagnostics"])
        out.append("")
    out += ["## Study diagnostics", "", *_diagnostics(result["diagnostics"]), "", "## Provenance", ""]
    out += _table(["Item", "Value"], [[k, str(v)] for k, v in result["provenance"].items()])
    out += ["", f"Request: {request['request_id']}. Result: {result['result_id']}.", "",
            "The input SHA-256 covers canonical network and request content, including "
            "case, duration, frequency and LV tolerance.", ""]
    return "\n".join(out)


def _diagnostics(items):
    if not items:
        return ["None."]
    rows = []
    for item in items:
        ref = item.get("element_ref") or {}
        rows.append([item["severity"], item["code"],
                     f"{ref.get('element_type', '')}:{ref.get('element_id', '')}.{ref.get('field', '')}",
                     item["message"].replace("\n", " ")])
    return _table(["Severity", "Code", "Element / field", "Message"], rows)
