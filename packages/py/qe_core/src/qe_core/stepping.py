"""CC-4 single-engine fixed-grid runtime, no domain imports or FMI ABI.

Lifecycle reference: FMI 3.0.2 sections 2.3 and 4.2.1; exact stepping,
zero-order-held inputs and interval-mean publication are Quantic policies.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from decimal import Decimal, DecimalException
from pathlib import Path
from typing import Literal, Mapping, Protocol, Sequence

from jsonschema import Draft202012Validator

from .project import safe_path
from .time_series import (
    _time,
    units_compatible,
    validate_signal,
    validate_time_series,
    validate_time_stepped_request,
)
from .validation import Diagnostic, Outcome, contract_root, diagnostic, validate

Scalar = float | int | bool


@dataclass(frozen=True)
class Quantity:
    value: Scalar
    unit: str


@dataclass(frozen=True)
class EngineStep:
    reached_time_s: Decimal
    working: Sequence[dict] = ()


class SteppingEngine(Protocol):
    signals: Sequence[dict]
    output_sampling: Literal["instant", "interval_mean"]
    solver_name: str
    solver_version: str

    def initialise(self, time_s: Decimal) -> None: ...
    def set_inputs(self, values: Mapping[str, Quantity]) -> None: ...
    def step_to(self, time_s: Decimal) -> EngineStep: ...
    def get_outputs(self) -> Mapping[str, Quantity]: ...
    def terminate(self) -> None: ...
    def reset(self) -> None: ...


class EngineError(Exception):
    def __init__(self, diagnostics: Sequence[Diagnostic]):
        self.diagnostics = list(diagnostics)
        super().__init__("; ".join(d.message for d in diagnostics))


def _error(code, message, field, identifier="runtime"):
    return diagnostic(code, message, "time_runtime", identifier, field)


def _scalar(value, kind):
    valid = (
        type(value) is bool
        if kind == "boolean"
        else type(value) is int
        if kind == "integer"
        else type(value) in (int, float)
    )
    return valid and (not isinstance(value, float) or math.isfinite(value))


def _number(time):
    value = int(time) if time == time.to_integral_value() else float(time)
    if not time.is_finite() or time < 0 or Decimal(str(value)) != time:
        raise ValueError(
            "Time must be finite, nonnegative and losslessly JSON-representable"
        )
    return value


def _decimal(value):
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError("Explicit numeric seconds are required")
    time = Decimal(str(value))
    _number(time)
    return time


@dataclass(frozen=True)
class RunLimits:
    """Resource policy, not physical/engineering constants; callers may tighten it."""

    max_steps: int = 100_000
    max_signals: int = 256
    max_file_bytes: int = 4_000_000
    max_cells: int = 1_000_000
    max_working: int = 100_000

    def check(self):
        if any(type(v) is not int or v < 1 for v in vars(self).values()):
            raise ValueError("Every runtime budget must be a positive integer")


class Session:
    """Own lifecycle, typed unit exchange and trace. Caller owns engine resources.

    Quantities supplied by the caller and returned by the engine always carry
    units. Compatible conversions are explicit at this boundary, including
    temperature offsets. Trace cells use the request's declared units.
    """

    def __init__(
        self,
        engine: SteppingEngine,
        signals: Sequence[dict],
        *,
        session_id="session",
        limits: RunLimits | None = None,
    ):
        self.engine = engine
        self.limits = limits or RunLimits()
        self.limits.check()
        self.session_id = session_id
        self.state = "instantiated"
        self.current = Decimal(0)
        self.steps: list[dict] = []
        self.working: list[dict] = []
        self.inputs: dict = {}
        self.outputs: dict = {}
        self.signals = copy.deepcopy(list(signals))
        self.definitions = {
            s.get("signal_id"): s for s in self.signals if isinstance(s, dict)
        }
        self.problems: list[Diagnostic] = []
        self._units = None
        if not isinstance(session_id, str) or not session_id:
            self.problems.append(
                _error("SESSION_ID", "Nonempty session ID required", "session_id")
            )
        if len(self.signals) > self.limits.max_signals:
            self.problems.append(
                _error("WORK_LIMIT", "Signal budget exceeded", "signals")
            )
        for s in self.signals[: self.limits.max_signals]:
            self.problems.extend(validate_signal(s))
        if len({s.get("model_id") for s in self.signals if isinstance(s, dict)}) > 1:
            self.problems.append(
                _error(
                    "COUPLING_UNSUPPORTED",
                    "Session supports one model only",
                    "model_id",
                )
            )
        if len(self.definitions) != len(self.signals):
            self.problems.append(
                _error("DUPLICATE_SIGNAL", "Signal IDs must be unique", "signals")
            )
        try:
            if (
                not isinstance(engine.signals, Sequence)
                or len(engine.signals) > self.limits.max_signals
            ):
                raise ValueError("Engine ports must be a bounded sequence")
            self.engine_ports = {s["signal_id"]: s for s in engine.signals}
            if len(engine.signals) != len(self.engine_ports):
                raise ValueError(
                    "Engine port IDs must be unique and within the signal budget"
                )
            for s in engine.signals:
                self.problems.extend(validate_signal(s))
            if set(self.engine_ports) != set(self.definitions):
                raise ValueError("Engine and request must declare the same named ports")
            for sid, s in self.definitions.items():
                port = self.engine_ports[sid]
                if any(
                    s[k] != port[k] for k in ("data_type", "causality", "model_id")
                ) or not units_compatible(s["unit"], port["unit"]):
                    self.problems.append(
                        _error(
                            "ENGINE_PORT",
                            "Engine port type, model, direction or units disagree",
                            "unit",
                            sid,
                        )
                    )
            if engine.output_sampling not in ("instant", "interval_mean"):
                raise ValueError("Engine must explicitly declare output sampling")
            if not all(
                isinstance(v, str) and v
                for v in (engine.solver_name, engine.solver_version)
            ):
                raise ValueError("Engine must identify its name and version")
            for method in (
                "initialise",
                "set_inputs",
                "step_to",
                "get_outputs",
                "terminate",
                "reset",
            ):
                if not callable(getattr(engine, method, None)):
                    raise ValueError("Engine is missing method " + method)
        except Exception as exc:
            self.engine_ports = {}
            self.problems.append(_error("ENGINE_INTERFACE", str(exc), "engine"))
        schema = json.loads(
            (contract_root() / "studies/time-stepped-result.schema.json").read_text()
        )
        self._working_validator = Draft202012Validator(schema["properties"]["working"])

    def _convert(self, quantity, source, destination):
        if (
            not isinstance(quantity, Quantity)
            or not isinstance(quantity.unit, str)
            or not quantity.unit
            or not _scalar(quantity.value, source["data_type"])
        ):
            raise ValueError("Typed Quantity required without boolean/integer coercion")
        if not units_compatible(quantity.unit, source["unit"]):
            raise ValueError("Quantity unit is incompatible with its declared signal")
        value = quantity.value
        if quantity.unit != destination["unit"]:
            if source["data_type"] == "boolean":
                raise ValueError("Boolean units must be exactly 1")
            if self._units is None:
                import pint

                self._units = pint.UnitRegistry()
            value = (
                self._units.Quantity(value, quantity.unit)
                .to(destination["unit"])
                .magnitude
            )
            if (
                source["data_type"] == "integer"
                and type(value) is float
                and value.is_integer()
            ):
                value = int(value)
        if not _scalar(value, destination["data_type"]):
            raise ValueError(
                "Converted quantity must retain its declared scalar type and finiteness"
            )
        return Quantity(value, destination["unit"])

    def _exchange(self, values, direction, *, from_engine=False, exact=False):
        expected = {
            sid for sid, s in self.definitions.items() if s["causality"] == direction
        }
        if (
            not isinstance(values, Mapping)
            or len(values) > self.limits.max_signals
            or not set(values) <= expected
            or (exact and set(values) != expected)
        ):
            raise EngineError(
                [
                    _error(
                        "SIGNAL_ALIGNMENT",
                        "Exchange must match declared named ports and direction",
                        direction,
                    )
                ]
            )
        engine_values, cells = {}, {}
        for sid, q in values.items():
            source = self.engine_ports[sid] if from_engine else self.definitions[sid]
            try:
                canonical = self._convert(q, source, self.definitions[sid])
                engine_values[sid] = self._convert(
                    canonical, self.definitions[sid], self.engine_ports[sid]
                )
            except (ValueError, TypeError, ArithmeticError) as exc:
                raise EngineError(
                    [_error("SIGNAL_VALUE", str(exc), "value_or_unit", sid)]
                ) from exc
            cells[sid] = {
                "value": canonical.value,
                "status": "valid",
                "diagnostics": [],
            }
        return engine_values, cells

    def _operation(self, op, target=None, values=None):
        current, before = self.current, self.state
        target = current if target is None else target
        inputs, outputs, errors = {}, {}, []
        try:
            target = _decimal(target)
            if self.problems:
                raise EngineError(self.problems)
            allowed = {
                "initialise": {"instantiated"},
                "set_inputs": {"initialized", "running"},
                "step_to": {"initialized", "running"},
                "get_outputs": {"initialized", "running"},
                "terminate": {"initialized", "running"},
                "reset": {
                    "instantiated",
                    "initialized",
                    "running",
                    "terminated",
                    "error",
                },
            }
            if before not in allowed[op]:
                raise EngineError(
                    [
                        _error(
                            "LIFECYCLE", "Operation not allowed in state " + before, op
                        )
                    ]
                )
            if len(self.steps) >= 4 * self.limits.max_steps + 4:
                raise EngineError(
                    [_error("WORK_LIMIT", "Operation budget exceeded", op)]
                )
            if op == "initialise":
                self.engine.initialise(target)
                self.state, self.current = "initialized", target
            elif op == "set_inputs":
                engine_values, inputs = self._exchange(values, "input")
                self.engine.set_inputs(engine_values)
                self.inputs.update(inputs)
            elif op == "get_outputs":
                _, outputs = self._exchange(
                    self.engine.get_outputs(), "output", from_engine=True, exact=True
                )
                self.outputs = outputs
            elif op == "step_to":
                if target <= current:
                    raise EngineError(
                        [
                            _error(
                                "TIME_ADVANCE",
                                "Step must advance beyond current time",
                                op,
                            )
                        ]
                    )
                reply = self.engine.step_to(target)
                if (
                    not isinstance(reply, EngineStep)
                    or _decimal(reply.reached_time_s) != target
                ):
                    raise EngineError(
                        [
                            _error(
                                "STEP_REACHED",
                                "Engine must reach exactly the requested fixed boundary",
                                "reached_time_s",
                            )
                        ]
                    )
                if not isinstance(reply.working, (list, tuple)):
                    raise EngineError(
                        [
                            _error(
                                "ENGINE_WORKING",
                                "Working must be a bounded sequence",
                                "working",
                            )
                        ]
                    )
                if len(self.working) + len(reply.working) > self.limits.max_working:
                    raise EngineError(
                        [
                            _error(
                                "WORK_LIMIT", "Working-trace budget exceeded", "working"
                            )
                        ]
                    )
                working = copy.deepcopy(list(reply.working))
                json.dumps(working, allow_nan=False)
                if list(self._working_validator.iter_errors(working)):
                    raise EngineError(
                        [
                            _error(
                                "ENGINE_WORKING",
                                "Working must use the CC-4 equation/source/substitution shape",
                                "working",
                            )
                        ]
                    )
                self.working.extend(working)
                self.state, self.current = "running", target
            elif op == "terminate":
                self.engine.terminate()
                self.state = "terminated"
            else:
                self.engine.reset()
                self.state, self.current = "instantiated", Decimal(0)
                self.inputs, self.outputs, self.working = {}, {}, []
        except EngineError as exc:
            errors = exc.diagnostics
        except Exception as exc:
            errors = [_error("ENGINE_FAILURE", str(exc), op)]
        if errors:
            if not any(d.severity == "error" for d in errors):
                errors.append(
                    _error(
                        "ENGINE_FAILURE",
                        "Failed operation requires an error diagnostic",
                        op,
                    )
                )
            self.state, self.current = "error", current
        # Invalid caller time is diagnosed without emitting a nonfinite JSON field.
        try:
            requested = _number(_decimal(target))
        except (ValueError, DecimalException, OverflowError):
            requested = _number(current)
        packet = {
            "schema_version": "0.1.0",
            "session_id": self.session_id,
            "operation": op,
            "state_before": before,
            "state_after": self.state,
            "current_time_s": _number(current),
            "requested_time_s": requested,
            "reached_time_s": _number(self.current),
            "status": "failed" if errors else "success",
            "inputs": inputs,
            "outputs": outputs,
            "diagnostics": [d.to_dict() for d in errors],
        }
        if len(self.steps) < 4 * self.limits.max_steps + 4:
            self.steps.append(packet)
        return Outcome(packet, errors)

    def initialise(self, time_s):
        return self._operation("initialise", time_s)

    def set_inputs(self, values):
        return self._operation("set_inputs", values=values)

    def step_to(self, time_s):
        return self._operation("step_to", time_s)

    def get_outputs(self):
        return self._operation("get_outputs")

    def terminate(self):
        return self._operation("terminate")

    def reset(self):
        return self._operation("reset", 0)


@dataclass
class RunOutcome(Outcome[dict]):
    requested_time_s: int | float | None = None
    reached_time_s: int | float = 0
    steps: list[dict] = field(default_factory=list)


def _label(time, axis):
    if axis["kind"] == "elapsed":
        return _number(time)
    microseconds = time * 1000000
    if microseconds != microseconds.to_integral_value():
        raise ValueError("UTC runtime grid must be representable in microseconds")
    return (
        (
            datetime.fromisoformat(axis["origin"])
            + timedelta(microseconds=int(microseconds))
        )
        .isoformat()
        .replace("+00:00", "Z")
    )


def _read(root, name, limits):
    if (
        not isinstance(name, str)
        or not name
        or any(part == ".." for part in name.split("/"))
    ):
        raise ValueError("Input path must be a confined project-relative file")
    path = safe_path(root, name)
    with path.open("rb") as stream:
        raw = stream.read(limits.max_file_bytes + 1)
    if len(raw) > limits.max_file_bytes:
        raise ValueError("Input file byte budget exceeded: " + name)
    value = json.loads(raw.decode("utf-8"))
    json.dumps(value, allow_nan=False)
    if not isinstance(value, dict):
        raise ValueError("Input file must contain an object: " + name)
    return path, value, hashlib.sha256(raw).hexdigest()


def run_fixed(
    request,
    engine: SteppingEngine,
    *,
    project_root: Path,
    model_file: str,
    request_file: str,
    model_version: str,
    sampling="interval_mean",
    request_pointer: tuple[str, ...] = (),
    limits: RunLimits | None = None,
    timestamp: str | None = None,
) -> RunOutcome:
    """Run one trusted engine. File names and data never name Python imports.

    request_pointer selects the common request inside a wrapper, e.g. ('execution',)
    for CC-5. The allowlisted domain caller supplies it, never project routing data.
    Preflight returns diagnostics only. Runtime failure retains its exact trace.
    Cooperative call/count bounds cannot interrupt a hung engine; service workers
    supply the process timeout. No interpolation, gap filling or early return.
    """
    limits = limits or RunLimits()
    try:
        limits.check()
        if (
            isinstance(request, dict)
            and isinstance(request.get("signals"), list)
            and len(request["signals"]) > limits.max_signals
        ):
            return RunOutcome(
                diagnostics=[
                    _error(
                        "WORK_LIMIT",
                        "Signal budget exceeded before validation",
                        "signals",
                    )
                ]
            )
        errors = validate_time_stepped_request(request)
        if errors:
            return RunOutcome(diagnostics=errors)
        start, stop, h = (
            Decimal(str(request[k]))
            for k in ("start_time_s", "stop_time_s", "step_size_s")
        )
        count = int((stop - start) / h)
        if (
            count > limits.max_steps
            or len(request["signals"]) > limits.max_signals
            or (count + 1) * len(request["signals"]) > limits.max_cells
        ):
            return RunOutcome(
                diagnostics=[
                    _error(
                        "WORK_LIMIT",
                        "Requested work exceeds runtime budget",
                        "step_size_s",
                    )
                ],
                requested_time_s=_number(stop),
            )
        if (
            sampling not in ("instant", "interval_mean")
            or engine.output_sampling != sampling
        ):
            return RunOutcome(
                diagnostics=[
                    _error(
                        "SAMPLING",
                        "Runner must match the engine output semantics",
                        "sampling",
                    )
                ],
                requested_time_s=_number(stop),
            )
        for i in range(count + 1):
            _number(start + i * h)
        _label(start, request["time_axis"])
        _label(stop, request["time_axis"])
        if request["time_axis"]["kind"] == "utc":
            _label(h, request["time_axis"])
        if not isinstance(model_version, str) or not model_version:
            raise ValueError("Explicit model version required")
        root = Path(project_root).resolve()
        entries = [
            _read(root, name, limits)
            for name in (model_file, request_file, request["input_series_file"])
        ]
        if len({e[0] for e in entries}) != 3:
            raise ValueError("Model, request and data must be distinct confined files")
        model, full_request, data = [e[1] for e in entries]
        stored = full_request
        for key in request_pointer:
            stored = stored[key]
        if stored != request:
            raise ValueError(
                "Common request must match the selected stored request document"
            )
        if (
            isinstance(data.get("samples"), list)
            and isinstance(data.get("signals"), list)
            and (
                len(data["samples"]) * len(data["signals"]) > limits.max_cells
                or len(data["signals"]) > limits.max_signals
            )
        ):
            return RunOutcome(
                diagnostics=[
                    _error(
                        "WORK_LIMIT",
                        "Input series exceeds budget before validation",
                        "samples",
                    )
                ],
                requested_time_s=_number(stop),
            )
        errors = validate_time_series(data)
        if errors:
            return RunOutcome(diagnostics=errors, requested_time_s=_number(stop))
        if data["time_axis"] != request["time_axis"]:
            raise ValueError("Input time axis must equal the requested axis")
        input_ports = {
            s["signal_id"]: s for s in request["signals"] if s["causality"] == "input"
        }
        source_ports = {s["signal_id"]: s for s in data["signals"]}
        if input_ports and set(input_ports) != set(source_ports):
            raise ValueError(
                "Input series must declare exactly the requested input ports"
            )
        for sid, port in input_ports.items():
            source = source_ports[sid]
            if any(
                port[k] != source[k] for k in ("data_type", "causality", "model_id")
            ) or not units_compatible(port["unit"], source["unit"]):
                raise ValueError(
                    "Input series port type, direction, model or unit mismatch: " + sid
                )
        rows = {}
        for row in data["samples"]:
            t = _time(row["time"], data["time_axis"])
            if (
                t < start
                or t > stop
                or (t - start) % h
                or (
                    "end_time" in row
                    and _time(row["end_time"], data["time_axis"]) != t + h
                )
            ):
                raise ValueError("Input samples must align with the fixed request grid")
            if data["sampling"] == "interval_mean" and t + h > stop:
                raise ValueError("Input interval extends past requested stop")
            rows[t] = row
        session = Session(
            engine, request["signals"], session_id=request["request_id"], limits=limits
        )
        if session.problems:
            return RunOutcome(
                diagnostics=session.problems, requested_time_s=_number(stop)
            )
        files = [
            {"path": name, "role": role, "sha256": entry[2]}
            for name, role, entry in zip(
                (model_file, request_file, request["input_series_file"]),
                ("model", "request", "data"),
                entries,
                strict=True,
            )
        ]
        canonical = {"model": model, "request": full_request, "data_files": [files[2]]}
        digest = hashlib.sha256(
            json.dumps(
                canonical,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            ).encode()
        ).hexdigest()
        provenance = {
            "solver_name": engine.solver_name,
            "solver_version": engine.solver_version,
            "input_hash_sha256": digest,
            "timestamp": timestamp
            if timestamp is not None
            else datetime.now(timezone.utc).isoformat(),
        }
        stamp = provenance["timestamp"]
        if not isinstance(stamp, str) or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})", stamp
        ):
            return RunOutcome(
                diagnostics=[
                    _error(
                        "PROVENANCE_TIMESTAMP",
                        "Explicit RFC3339 timestamp required",
                        "timestamp",
                    )
                ],
                requested_time_s=_number(stop),
            )
        datetime.fromisoformat(stamp)
        problems = validate(provenance, "common/provenance")
        if problems:
            return RunOutcome(diagnostics=problems, requested_time_s=_number(stop))
    except Exception as exc:
        return RunOutcome(
            diagnostics=[_error("RUN_INPUT", str(exc), "request_or_files")]
        )
    samples, errors = [], []
    outcome = session.initialise(start)
    errors.extend(outcome.diagnostics)

    def inputs_at(t):
        if not input_ports:
            return {}
        row = rows.get(t)
        if row is None or any(
            row["values"][sid]["status"] != "valid" for sid in input_ports
        ):
            raise EngineError(
                [
                    _error(
                        "INPUT_UNAVAILABLE",
                        "Required input interval/sample is missing or invalid",
                        "samples",
                    )
                ]
            )
        return {
            sid: Quantity(row["values"][sid]["value"], source_ports[sid]["unit"])
            for sid in input_ports
        }

    def set_inputs(t):
        try:
            values = inputs_at(t)
            result = session.set_inputs(values)
        except EngineError as exc:
            # No fabricated input cell. Record a failed exchange, retaining time.
            before = session.state
            session.state = "error"
            packet = {
                "schema_version": "0.1.0",
                "session_id": session.session_id,
                "operation": "set_inputs",
                "state_before": before,
                "state_after": "error",
                "current_time_s": _number(session.current),
                "requested_time_s": _number(session.current),
                "reached_time_s": _number(session.current),
                "status": "failed",
                "inputs": {},
                "outputs": {},
                "diagnostics": [d.to_dict() for d in exc.diagnostics],
            }
            session.steps.append(packet)
            return exc.diagnostics
        return result.diagnostics

    def sample(a, b=None):
        row = {
            "time": _label(a, request["time_axis"]),
            "values": copy.deepcopy({**session.inputs, **session.outputs}),
        }
        if b is not None:
            row["end_time"] = _label(b, request["time_axis"])
        samples.append(row)

    if not errors:
        errors.extend(set_inputs(start))
    if not errors and sampling == "instant":
        errors.extend(session.get_outputs().diagnostics)
        if not errors:
            sample(start)
    for i in range(count):
        if errors:
            break
        a, b = start + i * h, start + (i + 1) * h
        if i:
            errors.extend(set_inputs(a))
        if not errors:
            errors.extend(session.step_to(b).diagnostics)
        if not errors:
            errors.extend(session.get_outputs().diagnostics)
        if not errors:
            sample(a, b) if sampling == "interval_mean" else sample(b)
    if not errors:
        errors.extend(session.terminate().diagnostics)
    result = {
        "schema_version": "0.1.0",
        "result_id": request["request_id"] + ".result",
        **{k: request[k] for k in ("request_id", "study_id", "model_id")},
        "status": "complete"
        if not errors
        else "partial"
        if samples and session.current < stop
        else "failed",
        "requested_end_time_s": _number(stop),
        "reached_time_s": _number(session.current),
        "series": {
            "schema_version": "0.1.0",
            "series_id": request["request_id"] + ".series",
            "time_axis": copy.deepcopy(request["time_axis"]),
            "sampling": sampling,
            "signals": copy.deepcopy(request["signals"]),
            "samples": samples,
            "diagnostics": [],
        },
        "steps": session.steps,
        "working": session.working,
        "model_versions": {request["model_id"]: model_version},
        "input_files": files,
        "provenance": provenance,
        "diagnostics": [d.to_dict() for d in errors],
    }
    # CC-4 currently rejects reached < start even for failed initialization.
    # Expose the truthful runtime trace, never serialize a false reached time.
    if errors and session.current < start:
        errors.append(
            _error(
                "RESULT_UNREPRESENTABLE",
                "CC-4 result semantics cannot represent failure before a nonzero start",
                "reached_time_s",
            )
        )
        result = None
    return RunOutcome(
        value=result,
        diagnostics=errors,
        requested_time_s=_number(stop),
        reached_time_s=_number(session.current),
        steps=session.steps,
    )
