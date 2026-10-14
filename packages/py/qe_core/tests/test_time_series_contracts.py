"""Original CC-4 dimensional/time/state reference tables; no solver-generated values.

FMI 3.0.2 sections 2.3/2.4/4.2.2.1 motivate the operations. The exact-grid
restrictions and expected traces are our independently authored subset oracle.
"""

import copy
import json
import subprocess
from pathlib import Path

import pytest
from qe_core import validate
from qe_core.time_series import (
    units_compatible,
    validate_signal,
    validate_time_series,
    validate_time_step,
    validate_time_stepped_request,
    validate_time_stepped_result,
)

ROOT = Path(__file__).resolve().parents[4]


def signal(kind="real", unit="W", causality="output"):
    return {
        "schema_version": "0.1.0",
        "signal_id": "power",
        "model_id": "model",
        "name": "Power",
        "data_type": kind,
        "unit": unit,
        "causality": causality,
    }


def cell(value=20):
    return {"value": value, "status": "valid", "diagnostics": []}


def note(code="UNAVAILABLE", severity="warning"):
    return {
        "code": code,
        "severity": severity,
        "message": "Authored test condition",
        "element_ref": {
            "element_type": "signal",
            "element_id": "power",
            "field": "value",
        },
    }


def series():
    return {
        "schema_version": "0.1.0",
        "series_id": "series",
        "time_axis": {"kind": "elapsed", "unit": "s"},
        "sampling": "instant",
        "signals": [signal()],
        "samples": [{"time": t, "values": {"power": cell()}} for t in (0, 0.01, 0.02)],
        "diagnostics": [],
    }


def request():
    return {
        "schema_version": "0.1.0",
        "request_id": "request",
        "study_id": "study",
        "model_id": "model",
        "time_axis": {"kind": "elapsed", "unit": "s"},
        "clock": "fixed_ms",
        "start_time_s": 0,
        "stop_time_s": 0.02,
        "step_size_s": 0.01,
        "signals": [signal()],
        "input_series_file": "data.json",
    }


def packet(
    op="initialise", before="instantiated", after="initialized", current=0, target=0
):
    return {
        "schema_version": "0.1.0",
        "session_id": "session",
        "operation": op,
        "state_before": before,
        "state_after": after,
        "current_time_s": current,
        "requested_time_s": target,
        "reached_time_s": target,
        "status": "success",
        "inputs": {},
        "outputs": {},
        "diagnostics": [],
    }


def result():
    steps = [
        packet(),
        packet("step_to", "initialized", "running", 0, 0.01),
        packet("step_to", "running", "running", 0.01, 0.02),
    ]
    return {
        "schema_version": "0.1.0",
        "result_id": "result",
        "request_id": "request",
        "study_id": "study",
        "model_id": "model",
        "status": "complete",
        "requested_end_time_s": 0.02,
        "reached_time_s": 0.02,
        "series": series(),
        "steps": steps,
        "working": [
            {
                "equation": "E = P * duration",
                "source": {
                    "citation": "Authored constant-power reference",
                    "locator": "20 W for 0.02 s; original dimensional derivation",
                },
                "substitutions": {
                    "P": {"value": 20, "unit": "W"},
                    "duration": {"value": 0.02, "unit": "s"},
                },
                "result": {"value": 0.4, "unit": "J"},
            }
        ],
        "model_versions": {"model": "0.1.0"},
        "input_files": [
            {"path": "model.json", "role": "model", "sha256": "0" * 64},
            {"path": "request.json", "role": "request", "sha256": "1" * 64},
        ],
        "provenance": {
            "solver_name": "authored-reference",
            "solver_version": "1",
            "input_hash_sha256": "2" * 64,
            "timestamp": "2026-10-14T00:00:00Z",
        },
        "diagnostics": [],
    }


def codes(problems):
    return {p.code for p in problems}


def test_positive_schema_and_independent_time_trace():
    for data, kind in [
        (signal(), "common/signal"),
        (series(), "common/time-series"),
        (packet(), "common/time-step"),
        (request(), "studies/time-stepped-request"),
        (result(), "studies/time-stepped-result"),
    ]:
        assert not validate(data, kind)
        assert data == json.loads(json.dumps(data))
    assert not validate_time_series(series())
    assert not validate_time_stepped_request(request())
    assert not validate_time_stepped_result(result(), request=request())


@pytest.mark.parametrize(
    "left,right,expected",
    [
        ("W", "kW", True),
        ("ms", "s", True),
        ("K", "degC", True),
        ("W", "J", False),
        ("W/m^2", "W", False),
        ("missing", "s", False),
    ],
)
def test_dimensions_are_not_guessed(left, right, expected):
    assert units_compatible(left, right) is expected


@pytest.mark.parametrize(
    "kind,unit,value",
    [("boolean", "1", True), ("integer", "1", 4), ("real", "degC", 12.5)],
)
def test_signal_value_types(kind, unit, value):
    data = series()
    data["signals"] = [signal(kind, unit)]
    for row in data["samples"]:
        row["values"]["power"] = cell(value)
    assert not validate_time_series(data)


@pytest.mark.parametrize(
    "kind,value",
    [
        ("integer", True),
        ("integer", 1.5),
        ("boolean", 1),
        ("real", True),
        ("real", None),
    ],
)
def test_no_signal_type_coercion(kind, value):
    data = series()
    data["signals"] = [signal(kind, "1")]
    data["samples"][0]["values"]["power"] = cell(value)
    assert "SIGNAL_TYPE" in codes(validate_time_series(data))


def test_units_ids_and_alignment():
    assert validate_signal(signal("boolean", "s"))
    assert validate_signal(signal(unit="made_up_unit"))
    data = series()
    data["signals"].append(copy.deepcopy(data["signals"][0]))
    assert "DUPLICATE_SIGNAL" in codes(validate_time_series(data))
    data = series()
    data["samples"][0]["values"]["other"] = cell()
    assert "SIGNAL_ALIGNMENT" in codes(validate_time_series(data))
    data = series()
    data["samples"][0]["values"] = {}
    assert "SIGNAL_ALIGNMENT" in codes(validate_time_series(data))


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -float("inf")])
def test_finite_numbers(bad):
    data = series()
    data["samples"][0]["values"]["power"] = cell(bad)
    assert "NONFINITE" in codes(validate_time_series(data))
    data = request()
    data["step_size_s"] = bad
    assert validate_time_stepped_request(data)


def test_missing_and_invalid_are_diagnostic_null_not_zero():
    for state in ["missing", "invalid"]:
        data = series()
        c = data["samples"][1]["values"]["power"]
        c.update(value=None, status=state, diagnostics=[note()])
        assert not validate_time_series(data)
        c["value"] = 0
        assert "MISSING_VALUE" in codes(validate_time_series(data))
        c.update(value=None, diagnostics=[])
        assert "MISSING_VALUE" in codes(validate_time_series(data))


@pytest.mark.parametrize("bad", [0, -0.01, "2026-10-14T00:00:00Z"])
def test_repeated_backwards_and_mixed_time_axes(bad):
    data = series()
    data["samples"][1]["time"] = bad
    assert validate_time_series(data)


def test_intervals_and_utc_origin():
    data = series()
    data["sampling"] = "interval_mean"
    data["samples"] = data["samples"][:2]
    for i, row in enumerate(data["samples"]):
        row["end_time"] = (i + 1) / 100
    assert not validate_time_series(data)
    data["samples"][1]["time"] = 0.005
    assert "TIME_ALIGNMENT" in codes(validate_time_series(data))
    data = series()
    data["time_axis"] = {"kind": "utc", "unit": "s", "origin": "2026-10-14T00:00:00Z"}
    for row, t in zip(
        data["samples"],
        [
            "2026-10-14T00:00:00Z",
            "2026-10-14T00:00:00.010Z",
            "2026-10-14T00:00:00.020Z",
        ],
    ):
        row["time"] = t
    assert not validate_time_series(data)
    data["samples"][0]["time"] = "2026-10-13T23:59:59Z"
    assert validate_time_series(data)
    data["samples"][0]["time"] = "2026-10-14T00:00:00+02:00"
    assert validate_time_series(data)


@pytest.mark.parametrize(
    "change",
    [
        {"stop_time_s": 0},
        {"stop_time_s": 0.025},
        {"step_size_s": 0.0005},
        {"start_time_s": 0.0001},
    ],
)
def test_exact_fixed_clock(change):
    data = request()
    data.update(change)
    assert "TIME_GRID" in codes(validate_time_stepped_request(data))


@pytest.mark.parametrize(
    "op,before,after",
    [
        ("initialise", "instantiated", "initialized"),
        ("set_inputs", "initialized", "initialized"),
        ("get_outputs", "running", "running"),
        ("terminate", "running", "terminated"),
        ("reset", "error", "instantiated"),
    ],
)
def test_independent_lifecycle_table(op, before, after):
    assert not validate_time_step(packet(op, before, after))


def test_step_lifecycle_failure_reset_and_direction():
    data = packet("step_to", "instantiated", "running", 0, 0.01)
    assert "LIFECYCLE" in codes(validate_time_step(data))
    data = packet("step_to", "initialized", "running", 0.01, 0.01)
    assert "TIME_ADVANCE" in codes(validate_time_step(data))
    data = packet("step_to", "running", "error", 0.01, 0.02)
    data.update(
        status="failed", reached_time_s=0.01, diagnostics=[note(severity="error")]
    )
    assert not validate_time_step(data)
    reset = packet("reset", "error", "instantiated", 0.01, 0)
    assert not validate_time_step(reset, previous=data)
    reset["session_id"] = "other"
    assert "STEP_SEQUENCE" in codes(validate_time_step(reset, previous=data))
    data = packet("set_inputs", "running", "running")
    data["inputs"] = {"power": cell()}
    assert "SIGNAL_ALIGNMENT" in codes(validate_time_step(data, signals=[signal()]))


def test_result_complete_partial_failed_and_coverage():
    data = result()
    data.update(status="partial", reached_time_s=0.01, diagnostics=[note()])
    data["steps"] = data["steps"][:2]
    data["series"]["samples"] = data["series"]["samples"][:2]
    assert not validate_time_stepped_result(data, request=request())
    data["status"] = "complete"
    assert validate_time_stepped_result(data, request=request())
    data = result()
    data["series"]["samples"].pop(1)
    assert "RESULT_COVERAGE" in codes(
        validate_time_stepped_result(data, request=request())
    )
    data = result()
    data["series"]["samples"][0]["values"]["power"].update(
        value=None, status="missing", diagnostics=[note()]
    )
    assert validate_time_stepped_result(data, request=request())
    data = result()
    data["series"]["samples"][0]["time"] = "bad"
    assert validate_time_stepped_result(data)  # diagnostic, not a parser exception
    data = result()
    data["steps"][1]["current_time_s"] = 0.001
    assert "STEP_SEQUENCE" in codes(validate_time_stepped_result(data))
    data = result()
    data.update(status="failed", reached_time_s=0, diagnostics=[note(severity="error")])
    data["steps"] = [packet()]
    data["steps"][0].update(
        status="failed", state_after="error", diagnostics=[note(severity="error")]
    )
    data["series"]["samples"] = []
    assert not validate_time_stepped_result(data, request=request())


def test_version_binding_and_provenance():
    data = result()
    data["request_id"] = "other"
    assert "RESULT_BINDING" in codes(
        validate_time_stepped_result(data, request=request())
    )
    for path in ["/etc/input", "../input", "C:\\input"]:
        data = result()
        data["input_files"][0]["path"] = path
        assert "INPUT_PROVENANCE" in codes(validate_time_stepped_result(data))
    data = result()
    data["input_files"][1]["path"] = "model.json"
    assert "INPUT_PROVENANCE" in codes(validate_time_stepped_result(data))
    data = series()
    data["schema_version"] = "9.0.0"
    assert validate_time_series(data)


def test_existing_contract_bytes_and_power_types_preserved():
    # Compare against this approved CC's base, not a self-generated snapshot.
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", "334cd63", "contracts"],
        cwd=ROOT,
        text=True,
    ).splitlines()
    paths += [
        "packages/ts/contracts/src/generated.ts",
        "packages/ts/contracts/src/legacy.ts",
    ]
    for path in paths:
        before = subprocess.check_output(["git", "show", f"334cd63:{path}"], cwd=ROOT)
        assert (ROOT / path).read_bytes() == before, path


def test_extreme_time_and_malformed_optional_context_produce_diagnostics():
    data = request()
    data.update(clock="fixed_s", stop_time_s=1e300, step_size_s=1e-300)
    assert validate_time_stepped_request(data)
    assert validate_time_stepped_result(result(), request={})
    data = request()
    data["input_series_file"] = "../data.json"
    assert "REQUEST_PATH" in codes(validate_time_stepped_request(data))
    data = packet("get_outputs", "instantiated", "error")
    data.update(status="failed", diagnostics=[note(severity="error")])
    assert not validate_time_step(data)


def test_utc_precision_and_initialization_cannot_hide_time():
    data = series()
    data["time_axis"] = {
        "kind": "utc",
        "unit": "s",
        "origin": "2026-10-14T00:00:00.0000009Z",
    }
    assert validate_time_series(data)
    data = result()
    data["steps"] = [packet(target=0.02)]
    assert "STEP_SEQUENCE" in codes(
        validate_time_stepped_result(data, request=request())
    )
    data = result()
    data["series"]["signals"][0]["unit"] = "kW"
    assert "SIGNAL_ALIGNMENT" in codes(
        validate_time_stepped_result(data, request=request())
    )
