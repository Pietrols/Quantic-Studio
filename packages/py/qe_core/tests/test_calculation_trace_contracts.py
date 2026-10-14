"""CC-7: additive result versions; archived versions keep validating."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from qe_core import validate

REPO = Path(__file__).resolve().parents[4]


def _short_circuit_v2():
    return {"schema_version": "0.2.0", "result_id": "r", "network_id": "n", "fault_type": "3ph",
            "fault_duration_s": 1, "frequency_hz": 50, "lv_tolerance_percent": 6, "status": "success",
            "case_results": [{"case": "max", "status": "success", "diagnostics": [], "bus_results": [
                {"bus_id": "b", "voltage_factor": 1.1, "ikss_ka": 1.0, "ip_ka": 2.0, "ith_ka": 1.1}]}],
            "assumptions": ["a"], "diagnostics": [],
            "provenance": {"solver_name": "s", "solver_version": "1", "input_hash_sha256": "0" * 64,
                           "timestamp": "2026-10-14T00:00:00Z"}}


def _trace():
    return {"un_kv": 20, "voltage_factor": 1.1, "source_voltage_kv": 12.7, "impedance_basis": "engine-thevenin",
            "elements": [], "zk_r_ohm": 0.1, "zk_x_ohm": 1.0, "zk_ohm": 1.005, "rx_ratio": 0.1,
            "kappa": 1.75, "kappa_method": "radial", "m": 0.03, "n": 1}


def test_archived_shortcircuit_result_still_validates_and_is_byte_identical():
    assert validate(_short_circuit_v2(), "power/shortcircuit-result") == []
    archived = (REPO / "contracts/v0.2/power/shortcircuit-result.schema.json").read_text()
    assert json.loads(archived)["$id"].endswith("0.2.0:power:shortcircuit-result")


def test_new_shortcircuit_result_accepts_trace_and_rejects_trace_without_current():
    value = _short_circuit_v2()
    value["schema_version"] = "0.3.0"
    value["case_results"][0]["bus_results"][0]["trace"] = _trace()
    assert validate(value, "power/shortcircuit-result") == []
    bad = copy.deepcopy(value)
    bad["status"] = bad["case_results"][0]["status"] = "failed"
    row = bad["case_results"][0]["bus_results"][0]
    row.update(ikss_ka=None, ip_ka=None, ith_ka=None)
    bad["case_results"][0]["diagnostics"] = [
        {"code": "X", "message": "m", "severity": "error",
         "element_ref": {"element_type": "buses", "element_id": "b", "field": f}}
        for f in ("ikss_ka", "ip_ka", "ith_ka")]
    assert any(d.code == "SCHEMA_INVALID" for d in validate(bad, "power/shortcircuit-result"))
    row["trace"] = None
    assert validate(bad, "power/shortcircuit-result") == []


def test_trace_is_not_allowed_in_the_archived_version():
    value = _short_circuit_v2()
    value["case_results"][0]["bus_results"][0]["trace"] = _trace()
    assert validate(value, "power/shortcircuit-result") != []


def test_motorstart_versions():
    current = json.loads((REPO / "contracts/power/motorstart-result.schema.json").read_text())
    archived = json.loads((REPO / "contracts/v0.3/power/motorstart-result.schema.json").read_text())
    assert current["properties"]["schema_version"] == {"const": "0.4.0"}
    assert archived["properties"]["schema_version"] == {"const": "0.3.0"}
    assert "motor_trace" in current["properties"] and "motor_trace" not in archived["properties"]
