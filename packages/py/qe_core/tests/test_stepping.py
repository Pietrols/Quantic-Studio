"""Independent authored CC-4 runtime oracle: no external engineering engine.

Mean test device: y = 2*x W per interval; [1, 2, 3] W => [2, 4, 6] W.
Scan test device: increment count iff input is true on each 10 ms step;
[true,false,true] => count snapshots [0,1,1,2]. FMI 3.0.2 motivates the
lifecycle only; these mock equations/order/expected traces are original.
"""

import copy
import hashlib
import json
from decimal import Decimal

import pytest
from qe_core.stepping import (
    EngineError,
    EngineStep,
    Quantity,
    RunLimits,
    Session,
    run_fixed,
)
from qe_core.time_series import validate_time_step, validate_time_stepped_result
from qe_core.validation import diagnostic


def signal(sid, unit="W", kind="real", direction="input"):
    return {
        "schema_version": "0.1.0",
        "signal_id": sid,
        "model_id": "device",
        "name": sid,
        "unit": unit,
        "data_type": kind,
        "causality": direction,
    }


def request(*, scan=False, start=0):
    return {
        "schema_version": "0.1.0",
        "request_id": "run",
        "study_id": "study",
        "model_id": "device",
        "time_axis": {"kind": "elapsed", "unit": "s"},
        "clock": "fixed_ms" if scan else "fixed_s",
        "start_time_s": start,
        "stop_time_s": start + 0.03,
        "step_size_s": 0.01,
        "input_series_file": "data.json",
        "signals": [
            signal("x", "1" if scan else "W", "boolean" if scan else "real"),
            signal("y", "1" if scan else "W", "integer" if scan else "real", "output"),
        ],
    }


def series(req, values=None, unit=None):
    port = copy.deepcopy(req["signals"][0])
    if unit:
        port["unit"] = unit
    return {
        "schema_version": "0.1.0",
        "series_id": "inputs",
        "time_axis": req["time_axis"],
        "sampling": "interval_mean",
        "signals": [port],
        "samples": [
            {
                "time": float(Decimal(str(req["start_time_s"])) + Decimal("0.01") * i),
                "end_time": float(
                    Decimal(str(req["start_time_s"])) + Decimal("0.01") * (i + 1)
                ),
                "values": {"x": {"value": v, "status": "valid", "diagnostics": []}},
            }
            for i, v in enumerate(values or [1, 2, 3])
        ],
        "diagnostics": [],
    }


class MockEngine:
    solver_name = "authored-mock"
    solver_version = "1"
    output_sampling = "interval_mean"

    def __init__(self, signals, *, scan=False, fail=None):
        self.signals = copy.deepcopy(signals)
        self.calls = []
        self.scan = scan
        self.output_sampling = "instant" if scan else "interval_mean"
        self.fail = fail
        self.value = 0
        self.image = {}
        self.current = Decimal(0)

    def _call(self, name, value=None):
        self.calls.append((name, value))
        if self.fail == name or (
            self.fail == "second-step"
            and name == "step_to"
            and value == Decimal("0.02")
        ):
            raise EngineError(
                [
                    diagnostic(
                        "MOCK_FAIL",
                        "Original injected failure",
                        "device",
                        "device",
                        name,
                    )
                ]
            )

    def initialise(self, t):
        self._call("initialise", t)
        self.current = t
        self.value = 0

    def set_inputs(self, values):
        self._call("set_inputs", copy.deepcopy(values))
        self.image.update(values)

    def step_to(self, t):
        self._call("step_to", t)
        self.current = t
        if self.scan:
            self.value += int(self.image["x"].value)
        else:
            self.value = 2 * self.image["x"].value
        working = (
            []
            if self.scan
            else [
                {
                    "equation": "y=2*x",
                    "source": {
                        "citation": "Original mock definition",
                        "locator": "test_stepping.py module oracle",
                    },
                    "substitutions": {
                        "x": {
                            "value": self.image["x"].value,
                            "unit": self.image["x"].unit,
                        }
                    },
                    "result": {"value": self.value, "unit": "W"},
                }
            ]
        )
        return EngineStep(t, working)

    def get_outputs(self):
        self._call("get_outputs")
        return {"y": Quantity(self.value, "1" if self.scan else "W")}

    def terminate(self):
        self._call("terminate")

    def reset(self):
        self._call("reset")
        self.current = Decimal(0)
        self.value = 0
        self.image = {}


def write_inputs(root, req, data=None, wrapper=False):
    root.mkdir(exist_ok=True)
    (root / "model.json").write_text(json.dumps({"schema_version": "0.1.0", "gain": 2}))
    (root / "request.json").write_text(
        json.dumps(
            {"metadata": "retained wrapper", "execution": req} if wrapper else req
        )
    )
    (root / "data.json").write_text(json.dumps(data or series(req)))


def run(root, req, engine, **kwargs):
    return run_fixed(
        req,
        engine,
        project_root=root,
        model_file="model.json",
        request_file="request.json",
        model_version="mock-model-1",
        timestamp="2026-10-14T00:00:00Z",
        **kwargs,
    )


def codes(outcome):
    return {d.code for d in outcome.diagnostics}


def test_mean_grid_and_independent_trace(tmp_path):
    req = request()
    write_inputs(tmp_path, req)
    engine = MockEngine(req["signals"])
    result = run(tmp_path, req, engine)
    assert result.ok, result.diagnostics
    value = result.value
    assert [r["values"]["y"]["value"] for r in value["series"]["samples"]] == [2, 4, 6]
    assert [(r["time"], r["end_time"]) for r in value["series"]["samples"]] == [
        (0, 0.01),
        (0.01, 0.02),
        (0.02, 0.03),
    ]
    assert [p["operation"] for p in value["steps"]] == [
        "initialise",
        "set_inputs",
        "step_to",
        "get_outputs",
        "set_inputs",
        "step_to",
        "get_outputs",
        "set_inputs",
        "step_to",
        "get_outputs",
        "terminate",
    ]
    assert result.requested_time_s == result.reached_time_s == 0.03
    assert not validate_time_stepped_result(value, request=req)
    assert [w["result"]["value"] for w in value["working"]] == [2, 4, 6]


def test_handwritten_scan_snapshots(tmp_path):
    req = request(scan=True)
    write_inputs(tmp_path, req, series(req, [True, False, True]))
    result = run(
        tmp_path, req, MockEngine(req["signals"], scan=True), sampling="instant"
    )
    assert result.ok, result.diagnostics
    assert [r["values"]["y"]["value"] for r in result.value["series"]["samples"]] == [
        0,
        1,
        1,
        2,
    ]
    assert [r["values"]["x"]["value"] for r in result.value["series"]["samples"]] == [
        True,
        True,
        False,
        True,
    ]
    assert [r["time"] for r in result.value["series"]["samples"]] == [
        0,
        0.01,
        0.02,
        0.03,
    ]
    assert not validate_time_stepped_result(result.value, request=req)


@pytest.mark.parametrize("op", ["set_inputs", "get_outputs", "step_to", "terminate"])
def test_invalid_order_does_not_call_engine(op):
    req = request()
    engine = MockEngine(req["signals"])
    session = Session(engine, req["signals"])
    outcome = (
        getattr(session, op)({"x": Quantity(1, "W")})
        if op == "set_inputs"
        else getattr(session, op)(0.01)
        if op == "step_to"
        else getattr(session, op)()
    )
    assert "LIFECYCLE" in codes(outcome)
    assert session.current == 0 and session.state == "error" and not engine.calls
    assert not validate_time_step(outcome.value, signals=req["signals"])
    assert session.reset().ok
    assert session.state == "instantiated" and session.initialise(0).ok


def test_reset_new_lifecycle_and_rejected_rollback():
    req = request()
    session = Session(MockEngine(req["signals"]), req["signals"])
    assert session.initialise(0).ok
    assert session.set_inputs({"x": Quantity(1, "W")}).ok
    assert session.step_to(0.01).ok
    assert "TIME_ADVANCE" in codes(session.step_to(0))
    assert session.current == Decimal("0.01")
    assert session.reset().ok
    assert session.current == 0 and session.inputs == {} and session.working == []
    assert session.initialise(1).ok
    assert session.terminate().ok
    assert session.state == "terminated"
    assert not session.get_outputs().ok


@pytest.mark.parametrize(
    "quantity",
    [
        Quantity(True, "W"),
        Quantity(float("nan"), "W"),
        Quantity(1, "A"),
        Quantity(1, "unknown_unit"),
        1,
    ],
)
def test_bad_types_and_units_are_diagnostics(quantity):
    req = request()
    engine = MockEngine(req["signals"])
    session = Session(engine, req["signals"])
    assert session.initialise(0).ok
    assert "SIGNAL_VALUE" in codes(session.set_inputs({"x": quantity}))
    assert [name for name, _ in engine.calls] == ["initialise"]


def test_compatible_units_and_offsets_are_explicit(tmp_path):
    req = request()
    write_inputs(tmp_path, req, series(req, [1, 2, 3], unit="kW"))
    result = run(tmp_path, req, MockEngine(req["signals"]))
    assert result.ok, result.diagnostics
    assert [r["values"]["x"]["value"] for r in result.value["series"]["samples"]] == [
        1000,
        2000,
        3000,
    ]
    assert [r["values"]["y"]["value"] for r in result.value["series"]["samples"]] == [
        2000,
        4000,
        6000,
    ]
    req["signals"][0]["unit"] = "degC"
    engine = MockEngine(req["signals"])
    engine.signals[0]["unit"] = "K"
    session = Session(engine, req["signals"])
    assert session.initialise(0).ok
    assert session.set_inputs({"x": Quantity(25, "degC")}).ok
    assert engine.image["x"].unit == "K" and engine.image["x"].value == pytest.approx(
        298.15
    )
    assert session.steps[-1]["inputs"]["x"]["value"] == 25


@pytest.mark.parametrize(
    "case", ["wrong-unit", "wrong-model", "wrong-direction", "missing-port", "coupled"]
)
def test_invalid_ports_or_coupling_do_not_execute(tmp_path, case):
    req = request()
    engine = MockEngine(req["signals"])
    if case == "wrong-unit":
        engine.signals[0]["unit"] = "A"
    elif case == "wrong-model":
        engine.signals[0]["model_id"] = "another-model"
    elif case == "wrong-direction":
        engine.signals[0]["causality"] = "output"
    elif case == "missing-port":
        engine.signals.pop()
    else:
        req["couplings"] = [{"source": "other", "destination": "device"}]
    write_inputs(tmp_path, req)
    outcome = run(tmp_path, req, engine)
    assert not outcome.ok and outcome.value is None and not engine.calls


def test_engine_failures_keep_reached_time_and_valid_prefix(tmp_path):
    req = request()
    write_inputs(tmp_path, req)
    result = run(tmp_path, req, MockEngine(req["signals"], fail="second-step"))
    assert not result.ok and "MOCK_FAIL" in codes(result)
    assert result.value["status"] == "partial"
    assert result.requested_time_s == 0.03 and result.reached_time_s == 0.01
    assert [r["values"]["y"]["value"] for r in result.value["series"]["samples"]] == [2]
    assert (
        result.steps[-1]["requested_time_s"] == 0.02
        and result.steps[-1]["reached_time_s"] == 0.01
    )
    assert not validate_time_stepped_result(result.value, request=req)


@pytest.mark.parametrize("failure", ["initialise", "get_outputs", "terminate"])
def test_failure_at_each_boundary_is_contract_valid(tmp_path, failure):
    req = request()
    write_inputs(tmp_path, req)
    result = run(tmp_path, req, MockEngine(req["signals"], fail=failure))
    assert "MOCK_FAIL" in codes(result)
    assert not validate_time_stepped_result(result.value, request=req)
    assert result.steps[-1]["state_after"] == "error"


def test_nonzero_start_failed_initialization_never_forges_time(tmp_path):
    req = request(start=1)
    write_inputs(tmp_path, req)
    result = run(tmp_path, req, MockEngine(req["signals"], fail="initialise"))
    assert (
        result.value is None
        and result.reached_time_s == 0
        and result.requested_time_s == 1.03
    )
    assert "RESULT_UNREPRESENTABLE" in codes(result)
    assert (
        result.steps[0]["requested_time_s"] == 1
        and result.steps[0]["reached_time_s"] == 0
    )
    assert not validate_time_step(result.steps[0], signals=req["signals"])


@pytest.mark.parametrize(
    "failure", ["early", "nan", "no-confirmation", "bad-working", "bad-output"]
)
def test_engine_contract_breaches_are_diagnostics(tmp_path, failure):
    req = request()
    write_inputs(tmp_path, req)
    engine = MockEngine(req["signals"])
    if failure == "early":
        engine.step_to = lambda t: EngineStep(t - Decimal("0.005"))
    elif failure == "nan":
        engine.step_to = lambda t: EngineStep(Decimal("NaN"))
    elif failure == "no-confirmation":
        engine.step_to = lambda t: None
    elif failure == "bad-working":
        engine.step_to = lambda t: EngineStep(t, [{"equation": "unsubstantiated"}])
    else:
        engine.get_outputs = lambda: {"y": Quantity(1, "A")}
    result = run(tmp_path, req, engine)
    assert not result.ok and result.diagnostics
    assert not validate_time_stepped_result(result.value, request=req)


@pytest.mark.parametrize("case", ["gap", "missing", "invalid"])
def test_unavailable_input_does_not_become_zero(tmp_path, case):
    req = request()
    data = series(req)
    if case == "gap":
        data["samples"].pop(1)
    else:
        data["samples"][1]["values"]["x"] = {
            "value": None,
            "status": case,
            "diagnostics": [
                {
                    "code": "AUTHORED_UNAVAILABLE",
                    "severity": "warning",
                    "message": "Original absent input",
                    "element_ref": {
                        "element_type": "signal",
                        "element_id": "x",
                        "field": "value",
                    },
                }
            ],
        }
    write_inputs(tmp_path, req, data)
    engine = MockEngine(req["signals"])
    result = run(tmp_path, req, engine)
    assert "INPUT_UNAVAILABLE" in codes(result) and result.reached_time_s == 0.01
    assert len(result.value["series"]["samples"]) == 1
    assert not validate_time_stepped_result(result.value, request=req)


@pytest.mark.parametrize(
    "limits",
    [
        RunLimits(max_steps=2),
        RunLimits(max_signals=1),
        RunLimits(max_cells=3),
        RunLimits(max_file_bytes=10),
    ],
)
def test_work_is_bounded_before_engine_calls(tmp_path, limits):
    req = request()
    write_inputs(tmp_path, req)
    engine = MockEngine(req["signals"])
    result = run(tmp_path, req, engine, limits=limits)
    assert not result.ok and result.value is None and not engine.calls


def test_working_budget_and_sampling_mismatch(tmp_path):
    req = request()
    write_inputs(tmp_path, req)
    engine = MockEngine(req["signals"])
    result = run(tmp_path, req, engine, limits=RunLimits(max_working=1))
    assert "WORK_LIMIT" in codes(result) and result.reached_time_s == 0.01
    result = run(tmp_path, req, MockEngine(req["signals"]), sampling="instant")
    assert "SAMPLING" in codes(result)


@pytest.mark.parametrize(
    "kind",
    [
        "absolute",
        "traversal",
        "symlink",
        "alias",
        "wrong-request",
        "nonfinite",
        "bad-axis",
    ],
)
def test_confined_bounded_original_files(tmp_path, kind):
    req = request()
    write_inputs(tmp_path, req)
    if kind == "wrong-request":
        (tmp_path / "request.json").write_text("{}")
    elif kind == "nonfinite":
        (tmp_path / "model.json").write_text('{"gain":NaN}')
    elif kind == "bad-axis":
        data = series(req)
        data["time_axis"] = {
            "kind": "utc",
            "unit": "s",
            "origin": "2024-01-01T00:00:00Z",
        }
        (tmp_path / "data.json").write_text(json.dumps(data))
    else:
        if kind == "symlink":
            (tmp_path / "data.json").unlink()
            outside = tmp_path.parent / "outside.json"
            outside.write_text("{}")
            (tmp_path / "data.json").symlink_to(outside)
        if kind == "absolute":
            req["input_series_file"] = str(tmp_path / "data.json")
        if kind == "traversal":
            req["input_series_file"] = "../data.json"
        if kind == "alias":
            req["input_series_file"] = "model.json"
        (tmp_path / "request.json").write_text(json.dumps(req))
    engine = MockEngine(req["signals"])
    result = run(tmp_path, req, engine)
    assert not result.ok and not engine.calls
    assert all(d.element_ref and d.element_ref["field"] for d in result.diagnostics)


def test_utc_and_wrapper_provenance(tmp_path):
    req = request()
    req["time_axis"] = {"kind": "utc", "unit": "s", "origin": "2024-01-01T00:00:00Z"}
    data = series(request())
    data["time_axis"] = req["time_axis"]
    for row, a, b in zip(
        data["samples"],
        [".000000", ".010000", ".020000"],
        [".010000", ".020000", ".030000"],
        strict=True,
    ):
        row["time"] = "2024-01-01T00:00:00" + a + "Z"
        row["end_time"] = "2024-01-01T00:00:00" + b + "Z"
    write_inputs(tmp_path, req, data, wrapper=True)
    first = run(
        tmp_path, req, MockEngine(req["signals"]), request_pointer=("execution",)
    )
    assert first.ok, first.diagnostics
    assert (
        first.value["series"]["samples"][-1]["end_time"]
        == "2024-01-01T00:00:00.030000Z"
    )
    assert not validate_time_stepped_result(first.value, request=req)
    for file in first.value["input_files"]:
        assert (
            file["sha256"]
            == hashlib.sha256((tmp_path / file["path"]).read_bytes()).hexdigest()
        )
    wrapper = json.loads((tmp_path / "request.json").read_text())
    wrapper["metadata"] = "changed wrapper data"
    (tmp_path / "request.json").write_text(json.dumps(wrapper))
    second = run(
        tmp_path, req, MockEngine(req["signals"]), request_pointer=("execution",)
    )
    assert (
        second.value["provenance"]["input_hash_sha256"]
        != first.value["provenance"]["input_hash_sha256"]
    )


@pytest.mark.parametrize(
    "quantity",
    [Quantity(True, "W"), Quantity(float("inf"), "W"), Quantity(1, "nonsense")],
)
def test_bad_engine_output_never_becomes_a_valid_sample(tmp_path, quantity):
    req = request()
    write_inputs(tmp_path, req)
    engine = MockEngine(req["signals"])
    engine.get_outputs = lambda: {"y": quantity}
    result = run(tmp_path, req, engine)
    assert not result.ok and result.value["series"]["samples"] == []
    assert not validate_time_stepped_result(result.value, request=req)


def test_working_iterators_and_invalid_timestamp_are_diagnosed(tmp_path):
    req = request()
    write_inputs(tmp_path, req)
    engine = MockEngine(req["signals"])
    engine.step_to = lambda t: EngineStep(t, iter([]))
    result = run(tmp_path, req, engine)
    assert "ENGINE_WORKING" in codes(result)
    engine = MockEngine(req["signals"])
    result = run_fixed(
        req,
        engine,
        project_root=tmp_path,
        model_file="model.json",
        request_file="request.json",
        model_version="1",
        timestamp="not-a-time",
    )
    assert not result.ok and not engine.calls


def test_output_unit_and_integer_conversion_guard():
    req = request(scan=True)
    engine = MockEngine(req["signals"], scan=True)
    session = Session(engine, req["signals"])
    assert session.initialise(0).ok
    assert not session.set_inputs({"x": Quantity(1, "1")}).ok
    req = request()
    req["signals"][0].update(data_type="integer", unit="m")
    engine = MockEngine(req["signals"])
    session = Session(engine, req["signals"])
    assert session.initialise(0).ok
    assert session.set_inputs({"x": Quantity(1, "km")}).ok
    assert engine.image["x"].value == 1000
    assert not session.set_inputs({"x": Quantity(1, "cm")}).ok


def test_direct_session_rejects_malformed_and_coupled_ports():
    req = request()
    engine = MockEngine(req["signals"])
    session = Session(engine, [{}])
    assert not session.initialise(0).ok and not engine.calls
    ports = copy.deepcopy(req["signals"])
    ports[1]["model_id"] = "another-model"
    engine = MockEngine(ports)
    session = Session(engine, ports)
    assert "COUPLING_UNSUPPORTED" in codes(session.initialise(0))
    assert not engine.calls
