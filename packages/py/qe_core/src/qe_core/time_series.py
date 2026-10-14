"""CC-4 semantic validation. No engines, stepping execution or inferred units.

Lifecycle concepts: FMI 3.0.2 sections 2.3, 2.4 and 4.2.2.1. Quantic's
fixed-grid, no-rollback restrictions are declared subset choices, not FMI rules.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal, DecimalException
from functools import wraps

import pint

from .validation import diagnostic, validate

_UNITS = pint.UnitRegistry()


def _problem(code, message, identifier, field):
    return diagnostic(code, message, "signal_or_time", identifier, field)


def _safe_semantics(fn):
    """Malformed context or unrepresentable time produces diagnostics, not crashes."""

    @wraps(fn)
    def wrapped(value, *args, **kwargs):
        try:
            return fn(value, *args, **kwargs)
        except (
            DecimalException,
            ValueError,
            TypeError,
            OverflowError,
            KeyError,
        ) as exc:
            identifier = (
                value.get("request_id", value.get("result_id", "request"))
                if isinstance(value, dict)
                else "request"
            )
            return [
                _problem("CONTRACT_SEMANTICS", str(exc), identifier, "time_or_context")
            ]

    return wrapped


def units_compatible(left: str, right: str) -> bool:
    """Compatibility only; conversion and semantic port matching are not implicit."""
    try:
        return _UNITS.Unit(left).dimensionality == _UNITS.Unit(right).dimensionality
    except (ValueError, TypeError, pint.errors.PintError):
        return False


def validate_signal(value):
    errors = validate(value, "common/signal")
    if errors:
        return errors
    try:
        _UNITS.Unit(value["unit"])
    except (ValueError, TypeError, pint.errors.PintError):
        errors.append(
            _problem("SIGNAL_UNIT", "Unknown explicit unit", value["signal_id"], "unit")
        )
    if value["data_type"] == "boolean" and value["unit"] != "1":
        errors.append(
            _problem(
                "SIGNAL_UNIT",
                "Boolean signals require unit 1",
                value["signal_id"],
                "unit",
            )
        )
    return errors


def _signals(items):
    errors, signals = [], {}
    for item in items:
        problems = validate_signal(item)
        errors.extend(problems)
        if problems:
            continue
        sid = item["signal_id"]
        if sid in signals:
            errors.append(
                _problem(
                    "DUPLICATE_SIGNAL", "Signal ID must be unique", sid, "signal_id"
                )
            )
        signals[sid] = item
    return signals, errors


def _cells(values, signals, field, *, exact=True, causality=None):
    errors = []
    expected = {
        sid
        for sid, s in signals.items()
        if causality is None or s["causality"] == causality
    }
    if (exact and set(values) != expected) or not set(values) <= expected:
        errors.append(
            _problem(
                "SIGNAL_ALIGNMENT",
                "Cells must name exactly their declared signals",
                "series",
                field,
            )
        )
    for sid, cell in values.items():
        if sid not in expected:
            continue
        v, state = cell["value"], cell["status"]
        if state != "valid":
            if v is not None or not cell["diagnostics"]:
                errors.append(
                    _problem(
                        "MISSING_VALUE",
                        "Unavailable values require null and diagnostics",
                        sid,
                        field,
                    )
                )
            continue
        kind = signals[sid]["data_type"]
        ok = (
            type(v) is bool
            if kind == "boolean"
            else type(v) is int
            if kind == "integer"
            else type(v) in (int, float)
        )
        if not ok:
            errors.append(
                _problem(
                    "SIGNAL_TYPE",
                    f"Expected {kind}, without implicit coercion",
                    sid,
                    field,
                )
            )
        if any(d["severity"] == "error" for d in cell["diagnostics"]):
            errors.append(
                _problem(
                    "VALUE_STATUS",
                    "A valid cell cannot contain an error diagnostic",
                    sid,
                    field,
                )
            )
    return errors


def _time(value, axis):
    if axis["kind"] == "elapsed":
        if type(value) not in (int, float):
            raise ValueError("Elapsed sample time must be numeric seconds")
        return Decimal(str(value))
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("UTC sample time must end in Z")
    dt = datetime.fromisoformat(value)
    origin = datetime.fromisoformat(axis["origin"])
    delta = dt - origin
    return (
        Decimal(delta.days * 86400 + delta.seconds)
        + Decimal(delta.microseconds) / 1000000
    )


@_safe_semantics
def validate_time_series(value):
    errors = validate(value, "common/time-series")
    if errors:
        return errors
    signals, errors = _signals(value["signals"])
    previous_start = previous_end = None
    for i, row in enumerate(value["samples"]):
        field = f"samples.{i}"
        errors.extend(_cells(row["values"], signals, field + ".values"))
        try:
            start = _time(row["time"], value["time_axis"])
            if start < 0 or (previous_start is not None and start <= previous_start):
                raise ValueError(
                    "Sample starts must increase strictly from the declared origin"
                )
            if value["sampling"] == "interval_mean":
                if "end_time" not in row:
                    raise ValueError("Interval means need an explicit end_time")
                end = _time(row["end_time"], value["time_axis"])
                if end <= start or (previous_end is not None and start < previous_end):
                    raise ValueError(
                        "Intervals must have positive duration and cannot overlap"
                    )
                previous_end = end
            elif "end_time" in row:
                raise ValueError("Instantaneous samples cannot have end_time")
            previous_start = start
        except (ValueError, TypeError, OverflowError) as exc:
            errors.append(
                _problem(
                    "TIME_ALIGNMENT", str(exc), value["series_id"], field + ".time"
                )
            )
    return errors


@_safe_semantics
def validate_time_stepped_request(value):
    errors = validate(value, "studies/time-stepped-request")
    if errors:
        return errors
    _, errors = _signals(value["signals"])
    a, b, h = (
        Decimal(str(value[k])) for k in ("start_time_s", "stop_time_s", "step_size_s")
    )
    if b <= a or (b - a) % h:
        errors.append(
            _problem(
                "TIME_GRID",
                "Stop must follow start on the exact fixed-step grid",
                value["request_id"],
                "stop_time_s",
            )
        )
    if value["clock"] == "fixed_ms" and any((x * 1000) % 1 for x in (a, b, h)):
        errors.append(
            _problem(
                "TIME_GRID",
                "PLC clock values must be exact integer milliseconds",
                value["request_id"],
                "step_size_s",
            )
        )
    path = value["input_series_file"]
    if path.startswith("/") or "\\" in path or ":" in path or ".." in path.split("/"):
        errors.append(
            _problem(
                "REQUEST_PATH",
                "Data path must be project-relative and confined",
                value["request_id"],
                "input_series_file",
            )
        )
    if any(s["model_id"] != value["model_id"] for s in value["signals"]):
        errors.append(
            _problem(
                "SIGNAL_MODEL",
                "Single-model study signals must bind to its model",
                value["request_id"],
                "signals",
            )
        )
    return errors


@_safe_semantics
def validate_time_step(value, *, previous=None, signals=None):
    errors = validate(value, "common/time-step")
    if errors:
        return errors
    op, before, after = value["operation"], value["state_before"], value["state_after"]
    current, target, reached = (
        Decimal(str(value[k]))
        for k in ("current_time_s", "requested_time_s", "reached_time_s")
    )
    transitions = {
        "initialise": ({"instantiated"}, "initialized"),
        "step_to": ({"initialized", "running"}, "running"),
        "set_inputs": ({"initialized", "running"}, before),
        "get_outputs": ({"initialized", "running"}, before),
        "terminate": ({"initialized", "running"}, "terminated"),
        "reset": (
            {"instantiated", "initialized", "running", "terminated", "error"},
            "instantiated",
        ),
    }
    states, destination = transitions[op]
    if (value["status"] == "success" and before not in states) or after != (
        "error" if value["status"] == "failed" else destination
    ):
        errors.append(
            _problem(
                "LIFECYCLE",
                "Unsupported lifecycle transition",
                value["session_id"],
                "state_after",
            )
        )
    if value["status"] == "failed":
        if (
            not any(d["severity"] == "error" for d in value["diagnostics"])
            or reached != current
        ):
            errors.append(
                _problem(
                    "STEP_FAILURE",
                    "Failure requires an error and retains the last successful time",
                    value["session_id"],
                    "reached_time_s",
                )
            )
    else:
        if any(d["severity"] == "error" for d in value["diagnostics"]):
            errors.append(
                _problem(
                    "STEP_FAILURE",
                    "Successful operation cannot contain errors",
                    value["session_id"],
                    "diagnostics",
                )
            )
        if op == "step_to" and (target <= current or reached != target):
            errors.append(
                _problem(
                    "TIME_ADVANCE",
                    "Successful steps must advance exactly to target",
                    value["session_id"],
                    "requested_time_s",
                )
            )
        if op in ("get_outputs", "set_inputs", "terminate") and not (
            current == target == reached
        ):
            errors.append(
                _problem(
                    "TIME_ADVANCE",
                    "This operation cannot advance time",
                    value["session_id"],
                    "requested_time_s",
                )
            )
        if op == "initialise" and reached != target:
            errors.append(
                _problem(
                    "TIME_ADVANCE",
                    "Initialization must reach its declared initial time",
                    value["session_id"],
                    "reached_time_s",
                )
            )
        if op == "reset" and (target != 0 or reached != 0):
            errors.append(
                _problem(
                    "TIME_ADVANCE",
                    "Reset returns to uninitialized elapsed time zero",
                    value["session_id"],
                    "reached_time_s",
                )
            )
    if op not in ("initialise", "set_inputs", "step_to") and value["inputs"]:
        errors.append(
            _problem(
                "SIGNAL_DIRECTION",
                "Operation cannot set inputs",
                value["session_id"],
                "inputs",
            )
        )
    if op not in ("initialise", "step_to", "get_outputs") and value["outputs"]:
        errors.append(
            _problem(
                "SIGNAL_DIRECTION",
                "Operation cannot return outputs",
                value["session_id"],
                "outputs",
            )
        )
    if previous is not None and (
        value["session_id"] != previous["session_id"]
        or before != previous["state_after"]
        or current != Decimal(str(previous["reached_time_s"]))
    ):
        errors.append(
            _problem(
                "STEP_SEQUENCE",
                "Session, state and current time must continue the previous operation",
                value["session_id"],
                "state_before",
            )
        )
    if signals is not None:
        definitions, problems = _signals(signals)
        errors.extend(problems)
        errors.extend(
            _cells(
                value["inputs"], definitions, "inputs", exact=False, causality="input"
            )
        )
        errors.extend(
            _cells(
                value["outputs"],
                definitions,
                "outputs",
                exact=False,
                causality="output",
            )
        )
    return errors


@_safe_semantics
def validate_time_stepped_result(value, *, request=None):
    errors = validate(value, "studies/time-stepped-result")
    if errors:
        return errors
    series_errors = validate_time_series(value["series"])
    if series_errors:
        return series_errors
    target, reached = (
        Decimal(str(value[k])) for k in ("requested_end_time_s", "reached_time_s")
    )
    status = value["status"]
    if (
        reached > target
        or (status == "complete" and reached != target)
        or (status == "partial" and reached >= target)
    ):
        errors.append(
            _problem(
                "RESULT_COVERAGE",
                "Status and reached time disagree with requested coverage",
                value["result_id"],
                "reached_time_s",
            )
        )
    if status == "failed" and not any(
        d["severity"] == "error" for d in value["diagnostics"]
    ):
        errors.append(
            _problem(
                "RESULT_COVERAGE",
                "Failed study requires an error diagnostic",
                value["result_id"],
                "diagnostics",
            )
        )
    if status != "complete" and not value["diagnostics"]:
        errors.append(
            _problem(
                "RESULT_COVERAGE",
                "Incomplete studies require diagnostics",
                value["result_id"],
                "diagnostics",
            )
        )
    if status == "complete" and any(
        d["severity"] == "error" for d in value["diagnostics"]
    ):
        errors.append(
            _problem(
                "RESULT_COVERAGE",
                "Complete studies cannot contain errors",
                value["result_id"],
                "diagnostics",
            )
        )
    if value["model_id"] not in value["model_versions"] or any(
        s["model_id"] != value["model_id"] for s in value["series"]["signals"]
    ):
        errors.append(
            _problem(
                "SIGNAL_MODEL",
                "Model version and output signals must identify the study model",
                value["result_id"],
                "model_id",
            )
        )
    if any(
        f["path"].startswith("/")
        or "\\" in f["path"]
        or ":" in f["path"]
        or ".." in f["path"].split("/")
        for f in value["input_files"]
    ):
        errors.append(
            _problem(
                "INPUT_PROVENANCE",
                "Input paths must be confined project-relative names",
                value["result_id"],
                "input_files",
            )
        )
    if len({f["path"] for f in value["input_files"]}) != len(
        value["input_files"]
    ) or not {"model", "request"} <= {f["role"] for f in value["input_files"]}:
        errors.append(
            _problem(
                "INPUT_PROVENANCE",
                "Unique paths must include model and request hashes",
                value["result_id"],
                "input_files",
            )
        )
    previous = None
    for packet in value["steps"]:
        errors.extend(
            validate_time_step(
                packet,
                previous=previous,
                signals=value["series"]["signals"]
                if request is None
                else request["signals"],
            )
        )
        previous = packet
    if (
        not value["steps"]
        or Decimal(str(value["steps"][-1]["reached_time_s"])) != reached
    ):
        errors.append(
            _problem(
                "RESULT_COVERAGE",
                "Result reached time must equal its operation trace",
                value["result_id"],
                "steps",
            )
        )
    for i, row in enumerate(value["series"]["samples"]):
        t = _time(row.get("end_time", row["time"]), value["series"]["time_axis"])
        if t > reached:
            errors.append(
                _problem(
                    "RESULT_COVERAGE",
                    "Sample extends past last successful time",
                    value["result_id"],
                    f"series.samples.{i}.time",
                )
            )
        if status == "complete" and any(
            c["status"] != "valid" for c in row["values"].values()
        ):
            errors.append(
                _problem(
                    "RESULT_COVERAGE",
                    "Complete study cannot contain unavailable output",
                    value["result_id"],
                    f"series.samples.{i}.values",
                )
            )
    if request is not None:
        request_errors = validate_time_stepped_request(request)
        if request_errors:
            return [*errors, *request_errors]
        if (
            any(value[k] != request[k] for k in ("request_id", "study_id", "model_id"))
            or target != Decimal(str(request["stop_time_s"]))
            or value["series"]["time_axis"] != request["time_axis"]
        ):
            errors.append(
                _problem(
                    "RESULT_BINDING",
                    "Result must bind to the exact request/model/time axis",
                    value["result_id"],
                    "request_id",
                )
            )
    if status == "complete" and (
        not value["series"]["samples"]
        or _time(
            value["series"]["samples"][-1].get(
                "end_time", value["series"]["samples"][-1]["time"]
            ),
            value["series"]["time_axis"],
        )
        != reached
    ):
        errors.append(
            _problem(
                "RESULT_COVERAGE",
                "Complete output must cover its declared end",
                value["result_id"],
                "series.samples",
            )
        )
    if value["steps"] and value["steps"][0]["operation"] != "initialise":
        errors.append(
            _problem(
                "STEP_SEQUENCE",
                "A study trace starts with initialization",
                value["result_id"],
                "steps",
            )
        )
    if any(p["operation"] == "reset" for p in value["steps"]):
        errors.append(
            _problem(
                "STEP_SEQUENCE",
                "A result describes one run; resets start a new result",
                value["result_id"],
                "steps",
            )
        )
    if request is not None:
        if value["series"]["signals"] != request["signals"]:
            errors.append(
                _problem(
                    "SIGNAL_ALIGNMENT",
                    "Result declarations must preserve request signal order, identities, units and types",
                    value["result_id"],
                    "series.signals",
                )
            )
        if (
            value["steps"]
            and value["steps"][0]["status"] == "success"
            and Decimal(str(value["steps"][0]["reached_time_s"]))
            != Decimal(str(request["start_time_s"]))
        ):
            errors.append(
                _problem(
                    "STEP_SEQUENCE",
                    "Initialization must reach the requested start, not skip steps",
                    value["result_id"],
                    "steps.0.reached_time_s",
                )
            )
        a, h = (
            Decimal(str(request["start_time_s"])),
            Decimal(str(request["step_size_s"])),
        )
        if reached < a or (reached - a) % h:
            errors.append(
                _problem(
                    "RESULT_COVERAGE",
                    "Reached time must lie on the request grid",
                    value["result_id"],
                    "reached_time_s",
                )
            )
        else:
            count = int((reached - a) / h)
            expected_count = (
                count + 1 if value["series"]["sampling"] == "instant" else count
            )
            rows = value["series"]["samples"]
            if status != "failed" and len(rows) != expected_count:
                errors.append(
                    _problem(
                        "RESULT_COVERAGE",
                        "Every reached grid sample/interval must be reported",
                        value["result_id"],
                        "series.samples",
                    )
                )
            for i, row in enumerate(rows):
                if _time(row["time"], value["series"]["time_axis"]) != a + i * h or (
                    "end_time" in row
                    and _time(row["end_time"], value["series"]["time_axis"])
                    != a + (i + 1) * h
                ):
                    errors.append(
                        _problem(
                            "RESULT_COVERAGE",
                            "Samples must align with the exact request grid",
                            value["result_id"],
                            f"series.samples.{i}",
                        )
                    )
        for packet in value["steps"]:
            if (
                packet["operation"] == "step_to"
                and packet["status"] == "success"
                and Decimal(str(packet["reached_time_s"]))
                - Decimal(str(packet["current_time_s"]))
                != h
            ):
                errors.append(
                    _problem(
                        "TIME_GRID",
                        "Trace advances one declared fixed step at a time",
                        value["result_id"],
                        "steps",
                    )
                )
    return errors
