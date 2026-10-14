"""CC-6 `plc.scan` study: run a validated automation.plc model against its input events.

Ordering per scan k with period h (docs/specs/plc-program-and-scan.md section 4, after
Bolton, 6th ed, pp. 106 to 107): capture the input image at t_k (external inputs from
the latest event at or before t_k, process-wired inputs from the process state left by
scan k - 1), execute the statements, commit the output image at t_(k+1), then advance
the process. The result is a CC-6 result whose `scans` are the working (decision D11).
"""
from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from decimal import Decimal
from importlib.metadata import version

from qe_core import Diagnostic
from qe_core.plc_contracts import (
    DEFAULTS,
    LANGUAGE,
    plc_event_changes,
    validate_plc_events,
    validate_plc_model,
    validate_plc_request,
)

from .errors import PlcError
from .parser import parse
from .process import MotorStarter
from .scan import ScanEngine

LIMITATIONS = [
    "Structured Text subset quantic-st-0.1 only; no IEC 61131-3 conformance or edition claim.",
    "Simulated time: one cyclic task, scan execution modelled as the whole period, no jitter.",
    "Digital (BOOL) I/O only; no analog I/O, fieldbus, retain memory or multitasking.",
    "The motor starter is an authored discrete transition table: no motor dynamics, contactor "
    "timing or safety rating.",
    "Timer and counter corner cases follow declared subset choices where Bolton and Beckhoff "
    "are silent (structured-text-subset.md section 6).",
]


def _literal(value, kind):
    if kind == "BOOL":
        return "TRUE" if value else "FALSE"
    if kind == "TIME":
        return f"T#{value}ms"
    if kind == "INT":
        return str(value)
    text = repr(float(value))
    # The lexer reads reals as digits.digits[e[+-]digits]; repr may give 1e-05 or 1e+20.
    return text if "." in text and "e" not in text else format(float(value), ".17e")


def compose(model) -> tuple[str, int]:
    """Program text from the model's declarations and statement body, and the header length.

    Body line n is text line header + n, so diagnostics map back to the body exactly.
    """
    lines = [f"PROGRAM {model['program']['program_id']}"]
    for section, keyword in (("input", "VAR_INPUT"), ("output", "VAR_OUTPUT"), ("internal", "VAR")):
        decls = [
            f"{v['name']} : {v['type']}"
            + (f" := {_literal(v['initial'], v['type'])}" if "initial" in v else "")
            + ";"
            for v in model["variables"]
            if v["section"] == section
        ]
        if section == "internal":
            decls += [f"{i['name']} : {i['block']};" for i in model["instances"]]
        if decls:
            lines.append(f"{keyword} {' '.join(decls)} END_VAR")
    return "\n".join(lines) + "\n" + model["program"]["body"] + "\nEND_PROGRAM\n", len(lines)


def _body_diagnostic(error: PlcError, header: int, program_id: str) -> dict:
    line = error.line - header
    field = f"program.body:{line}:{error.column}" if line >= 1 else "variables"
    where = f"line {line}, column {error.column}" if line >= 1 else "declarations"
    return Diagnostic(error.code, f"{where}: {error.message}",
                      {"element_type": "program", "element_id": program_id, "field": field}).to_dict()


def _cell(value):
    return {"value": value, "status": "valid", "diagnostics": []}


def _seconds(ms):
    return ms / 1000  # integer ms over 1000 is correctly rounded, so str() gives the exact grid value


def run_scan_study(model, request, events, *, input_files, timestamp=None):
    """Return (result, diagnostics). Invalid contracts give (None, diagnostics): no run happens.

    `input_files` are the CC-4 provenance entries ({path, role, sha256}) supplied by the caller,
    which read the files. `timestamp` (ISO 8601 UTC) makes replays byte-identical.
    """
    problems = validate_plc_model(model)
    if not problems:
        problems = validate_plc_request(request, model=model)
    if not problems:
        problems = validate_plc_events(events, request=request)
    if problems:
        return None, [p.to_dict() for p in problems]

    run = request["execution"]
    program_id = model["program"]["program_id"]
    period = model["task"]["period_ms"]
    total = int(Decimal(str(run["stop_time_s"])) * 1000) // period
    variables = {v["name"]: v for v in model["variables"]}
    process_model = model["process"]
    wiring = process_model["wiring"] if process_model else {}
    targets = {b["signal_id"]: b["target"] for b in request["bindings"]}
    inputs = [s["signal_id"] for s in run["signals"] if s["causality"] == "input"]
    outputs = [s["signal_id"] for s in run["signals"] if s["causality"] == "output"]
    changes = plc_event_changes(events, request)

    def held(sid, time_ms):
        value = None
        for change in changes:
            if change["signal_id"] == sid and change["time_ms"] <= time_ms:
                value = change["value"]
        return value

    def input_cells(time_ms):
        return {sid: _cell(held(sid, time_ms)) for sid in inputs}

    initial_state = None
    if process_model:
        initial_state = {**process_model["initial"], "motor_running": process_model["initial"]["contactor_closed"]}

    def output_cells(scan):
        cells = {}
        for sid in outputs:
            target = targets[sid]
            if target["kind"] == "variable":
                name = target["variable"]
                value = (variables[name].get("initial", DEFAULTS[variables[name]["type"]])
                         if scan is None else scan["outputs"][name])
            else:
                value = initial_state[target["port"]] if scan is None else scan["process"]["after"][target["port"]]
            cells[sid] = _cell(value)
        return cells

    source, header = compose(model)
    steps, scans, diagnostics = [], [], []
    init = {"schema_version": "0.1.0", "session_id": run["request_id"], "operation": "initialise",
            "state_before": "instantiated", "current_time_s": 0, "requested_time_s": 0,
            "reached_time_s": 0, "inputs": {}, "outputs": {}}
    try:
        engine = ScanEngine(parse(source), period)
    except PlcError as error:
        diagnostics.append(_body_diagnostic(error, header, program_id))
        steps.append({**init, "state_after": "error", "status": "failed", "diagnostics": diagnostics})
        engine = None
    else:
        steps.append({**init, "state_after": "initialized", "status": "success", "diagnostics": []})
    process = MotorStarter(**process_model["initial"]) if process_model else None

    for k in range(total if engine else 0):
        start, commit = k * period, (k + 1) * period
        image = {}
        for sid in inputs:
            if targets[sid]["kind"] == "variable":
                image[targets[sid]["variable"]] = held(sid, start)
        if process:
            image[wiring["contactor_feedback"]] = process.contactor_closed
            image[wiring["overload_ok"]] = not process.overload_tripped
        packet = {"schema_version": "0.1.0", "session_id": run["request_id"], "operation": "step_to",
                  "state_before": "initialized" if k == 0 else "running",
                  "current_time_s": _seconds(start), "requested_time_s": _seconds(commit),
                  "inputs": input_cells(start)}
        try:
            trace = engine.scan(image)
        except PlcError as error:
            diagnostics.append(_body_diagnostic(error, header, program_id))
            steps.append({**packet, "state_after": "error", "reached_time_s": _seconds(start),
                          "status": "failed", "outputs": {}, "diagnostics": list(diagnostics)})
            break
        statements = [{**step, "line": step["line"] - header} for step in trace["steps"]]
        scan = {"scan": k, "start_ms": start, "commit_ms": commit, "inputs": trace["inputs"],
                "statements": statements, "outputs": trace["outputs"], "blocks": trace["blocks"],
                "process": None}
        if process:
            scan["process"] = process.advance(
                trace["outputs"][wiring["coil"]],
                held(_port_signal(targets, "overload_event"), start),
                held(_port_signal(targets, "overload_reset"), start),
            )
        scans.append(scan)
        steps.append({**packet, "state_after": "running", "reached_time_s": _seconds(commit),
                      "status": "success", "outputs": output_cells(scan), "diagnostics": []})

    completed = len(scans)
    reached_ms = completed * period
    samples = []
    if engine is not None:
        for i in range(completed + 1):
            samples.append({"time": _seconds(i * period),
                            "values": {**input_cells(i * period),
                                       **output_cells(scans[i - 1] if i else None)}})
    status = "complete" if completed == total else ("partial" if completed else "failed")
    hashes = "".join(sorted(f["sha256"] for f in input_files))
    execution = {
        "schema_version": "0.1.0", "result_id": run["request_id"] + "-result",
        "request_id": run["request_id"], "study_id": run["study_id"], "model_id": run["model_id"],
        "status": status, "requested_end_time_s": run["stop_time_s"], "reached_time_s": _seconds(reached_ms),
        "series": {"schema_version": "0.1.0", "series_id": run["request_id"] + "-trace",
                   "time_axis": run["time_axis"], "sampling": "instant", "signals": run["signals"],
                   "samples": samples, "diagnostics": []},
        "steps": steps, "working": [], "model_versions": {run["model_id"]: model["schema_version"]},
        "input_files": input_files,
        "provenance": {"solver_name": "qe_plc", "solver_version": version("qe-plc"),
                       "input_hash_sha256": hashlib.sha256(hashes.encode()).hexdigest(),
                       "timestamp": timestamp or datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")},
        "diagnostics": diagnostics,
    }
    result = {
        "schema_version": "0.1.0", "execution": execution, "language": LANGUAGE,
        "program": {"program_id": program_id,
                    "body_sha256": hashlib.sha256(model["program"]["body"].encode("utf-8")).hexdigest()},
        "events": changes, "scans": scans, "limitations": LIMITATIONS,
    }
    return result, diagnostics


def _port_signal(targets, port):
    return next(sid for sid, t in targets.items() if t["kind"] == "process_port" and t["port"] == port)
