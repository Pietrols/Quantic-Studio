"""Original synthetic contract fixture; seed never computes PV power."""

import json
import subprocess
import sys

from qe_core.stepping import run_fixed
from qe_core.time_series import validate_time_stepped_result
from qe_pv import UnavailablePVEngine


def test_seed_is_unavailable_with_true_failed_trace(tmp_path):
    ports = [
        {
            "schema_version": "0.1.0",
            "signal_id": sid,
            "model_id": "pv",
            "name": sid,
            "data_type": "real",
            "unit": unit,
            "causality": direction,
        }
        for sid, unit, direction in [("irr", "W/m^2", "input"), ("ac", "W", "output")]
    ]
    req = {
        "schema_version": "0.1.0",
        "request_id": "yield",
        "study_id": "study",
        "model_id": "pv",
        "time_axis": {"kind": "elapsed", "unit": "s"},
        "clock": "fixed_s",
        "start_time_s": 0,
        "stop_time_s": 1,
        "step_size_s": 1,
        "signals": ports,
        "input_series_file": "data.json",
    }
    data = {
        "schema_version": "0.1.0",
        "series_id": "synthetic",
        "time_axis": req["time_axis"],
        "sampling": "interval_mean",
        "signals": [ports[0]],
        "samples": [
            {
                "time": 0,
                "end_time": 1,
                "values": {
                    "irr": {"value": 1000, "status": "valid", "diagnostics": []}
                },
            }
        ],
        "diagnostics": [],
    }
    for name, payload in [
        ("model", {"schema_version": "0.1.0"}),
        ("request", req),
        ("data", data),
    ]:
        (tmp_path / (name + ".json")).write_text(json.dumps(payload))
    result = run_fixed(
        req,
        UnavailablePVEngine(ports),
        project_root=tmp_path,
        model_file="model.json",
        request_file="request.json",
        model_version="0.1.0",
    )
    assert not result.ok and {d.code for d in result.diagnostics} == {
        "ENGINE_UNAVAILABLE"
    }
    assert (
        result.value["status"] == "failed" and result.value["series"]["samples"] == []
    )
    assert result.reached_time_s == 0 and result.requested_time_s == 1
    assert not validate_time_stepped_result(result.value, request=req)


def test_seed_does_not_import_numerical_library():
    subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; import qe_pv; assert 'pvlib' not in sys.modules",
        ],
        check=True,
    )
