"""Verify duty meanings and visibility of unavailable engineering results."""
import json
from pathlib import Path

from qe_power.adapters.pandapower import solve_shortcircuit
from qe_report import render_shortcircuit_report

EXAMPLE = Path(__file__).resolve().parents[4] / "examples/shortcircuit"


def test_report_keeps_case_diagnostics_and_source_inputs():
    network = json.loads((EXAMPLE / "network.json").read_text())
    request = json.loads((EXAMPLE / "shortcircuit-request.json").read_text())
    # A machine makes the component near-to-generator: Ik'' available, ip and Ith withheld.
    network["buses"][1]["bus_type"] = "pv"
    network["generators"] = [{"generator_id": "g1", "bus_id": "lv", "p_mw": 1, "vm_setpoint_pu": 1, "sn_mva": 10, "vn_kv": 20,
         "xdss_pu": 0.2, "rdss_ohm": 0.4, "cos_phi": 0.8, "voltage_control_range_percent": 0}]
    result = solve_shortcircuit(network, request).value
    report = render_shortcircuit_report(project_name="Original feeder", network=network,
                                       request=request, result=result)
    for term in ("PARTIAL", "Maximum", "Minimum", "instantaneous peak", "thermal RMS",
                 "20", "s_sc_max_mva", "end_temperature_celsius", "n/a", "not zero",
                 "NEAR_GENERATOR_DUTY", "buses:lv.ith_ka", "no independent standards certification"):
        assert term in report
    for case in result["case_results"]:
        for bus in case["bus_results"]:
            assert f"{bus['ikss_ka']:.6f}" in report
    assert result["provenance"]["input_hash_sha256"] in report
