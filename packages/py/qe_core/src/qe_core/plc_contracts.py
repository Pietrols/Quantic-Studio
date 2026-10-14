"""CC-6 engine-free PLC model, scan request, input-event and scan result validation.

The scan ordering follows Bolton, Programmable Logic Controllers, 6th ed (Newnes,
2015), pp. 106 to 107 (mass I/O copying). The motor-starter process is an authored
discrete transition table, not a model of real equipment. Both, with every declared
subset choice, are specified in docs/specs/plc-program-and-scan.md. This module
never parses or runs Structured Text: statement-level errors belong to qe_plc.
"""

from __future__ import annotations

import hashlib
import math
from decimal import Decimal

from .time_series import (
    _safe_semantics,
    validate_time_series,
    validate_time_stepped_request,
    validate_time_stepped_result,
)
from .validation import diagnostic, validate

LANGUAGE = "quantic-st-0.1"
MODEL_VERSIONS = ("0.1.0",)
MAX_SCANS = 100_000
INT_MIN, INT_MAX = -32768, 32767
TIME_MIN, TIME_MAX = -(2**31), 2**31 - 1  # milliseconds, declared subset range
REAL_MAX = 3.4028234663852886e38  # largest finite IEEE 754 binary32 value
DEFAULTS = {"BOOL": False, "INT": 0, "REAL": 0.0, "TIME": 0}
BLOCK_OUTPUTS = {
    "TON": {"Q", "ET"},
    "TOF": {"Q", "ET"},
    "TP": {"Q", "ET"},
    "CTU": {"Q", "CV"},
    "CTD": {"Q", "CV"},
    "CTUD": {"QU", "QD", "CV"},
}
SCENARIO_PORTS = ("overload_event", "overload_reset")
STATE_PORTS = ("contactor_closed", "overload_tripped", "motor_running")
# Words of the quantic-st-0.1 subset and the constructs it rejects by name. qe_plc's
# lexer holds the same two sets; a qe_plc test keeps them identical.
RESERVED = frozenset(
    {
        "PROGRAM", "END_PROGRAM", "VAR", "VAR_INPUT", "VAR_OUTPUT", "END_VAR", "IF", "THEN",
        "ELSIF", "ELSE", "END_IF", "AND", "OR", "XOR", "NOT", "MOD", "TRUE", "FALSE", "BOOL",
        "INT", "REAL", "TIME", "TON", "TOF", "TP", "CTU", "CTD", "CTUD", "FOR", "WHILE",
        "REPEAT", "CASE", "FUNCTION", "FUNCTION_BLOCK", "RETURN", "EXIT", "POINTER", "REF_TO",
        "ARRAY", "STRUCT", "VAR_IN_OUT", "VAR_GLOBAL", "VAR_TEMP", "AT", "CONSTANT", "RETAIN",
        "DINT", "LREAL", "WORD", "DWORD", "STRING", "JMP",
    }
)


def problem(code, field, message, identifier="plc"):
    return diagnostic(code, message, "plc", identifier, field)


def _local(path):
    return bool(path) and not (
        path.startswith("/") or "\\" in path or ":" in path or ".." in path.split("/")
    )


def typed(value, kind):
    """True when a JSON value is a valid value of the ST type, with no coercion."""
    if kind == "BOOL":
        return type(value) is bool
    if kind == "INT":
        return type(value) is int and INT_MIN <= value <= INT_MAX
    if kind == "TIME":
        return type(value) is int and TIME_MIN <= value <= TIME_MAX
    return type(value) in (int, float) and math.isfinite(value) and abs(value) <= REAL_MAX


def plc_elements(model):
    """Element identities an asset registry may reference (CC-3 representations)."""
    elements = {
        "controller": {model["controller_id"]},
        "devices": {d["device_id"] for d in model["devices"]},
        "variables": {v["name"] for v in model["variables"]},
        "function_blocks": {i["name"] for i in model["instances"]},
    }
    if model["process"] is not None:
        elements["process"] = {model["process"]["process_id"]}
    return elements


def _variables(model):
    return {v["name"]: v for v in model["variables"]}


def _initial(variable):
    return variable.get("initial", DEFAULTS[variable["type"]])


@_safe_semantics
def validate_plc_model(value):
    errors = validate(value, "automation/plc-model")
    if errors:
        return errors
    seen = {}
    for kind, items in (("variables", value["variables"]), ("instances", value["instances"])):
        for item in items:
            name = item["name"]
            key = name.upper()  # ST names are not case sensitive (Bolton p. 169)
            if key in RESERVED:
                errors.append(problem("RESERVED_NAME", f"{kind}.{name}", "Name is a reserved word", name))
            if key in seen:
                errors.append(problem("DUPLICATE_NAME", f"{kind}.{name}",
                                      f"Name clashes with {seen[key]} (names are not case sensitive)", name))
            seen.setdefault(key, name)
    for var in value["variables"]:
        name, section, kind = var["name"], var["section"], var["type"]
        if section in ("input", "output") and kind != "BOOL":
            errors.append(problem("PLC_IO_TYPE", f"variables.{name}.type",
                                  "CC-6 first slice I/O is digital (BOOL) only", name))
        if "initial" in var:
            if section == "input":
                errors.append(problem("PLC_INITIAL", f"variables.{name}.initial",
                                      "Inputs take their value from the input image", name))
            elif not typed(var["initial"], kind):
                errors.append(problem("PLC_INITIAL", f"variables.{name}.initial",
                                      f"Initial value is not a valid {kind}", name))
    variables = _variables(value)
    devices, owners = set(), {}
    for device in value["devices"]:
        did = device["device_id"]
        if did in devices:
            errors.append(problem("DUPLICATE_ID", "devices.device_id", "Device ID must be unique", did))
        devices.add(did)
        for name in device["io"]:
            var = variables.get(name)
            if var is None or var["section"] == "internal":
                errors.append(problem("PLC_DEVICE", f"devices.{did}.io",
                                      f"{name} is not a declared input or output", did))
            elif name in owners:
                errors.append(problem("PLC_DEVICE", f"devices.{did}.io",
                                      f"{name} already belongs to device {owners[name]}", did))
            owners.setdefault(name, did)
    process = value["process"]
    if process is not None:
        pid, wiring = process["process_id"], process["wiring"]
        for port, section in (("coil", "output"), ("contactor_feedback", "input"), ("overload_ok", "input")):
            var = variables.get(wiring[port])
            if var is None or var["section"] != section or var["type"] != "BOOL":
                errors.append(problem("PLC_WIRING", f"process.wiring.{port}",
                                      f"Must name a declared BOOL {section} variable", pid))
        if wiring["contactor_feedback"] == wiring["overload_ok"]:
            errors.append(problem("PLC_WIRING", "process.wiring.overload_ok",
                                  "Feedback and overload contacts need separate inputs", pid))
        coil = variables.get(wiring["coil"])
        state = process["initial"]
        if coil is not None and state["contactor_closed"] != (
            _initial(coil) is True and not state["overload_tripped"]
        ):
            errors.append(problem("PLC_PROCESS_STATE", "process.initial.contactor_closed",
                                  "Initial contactor state must follow the initial coil and overload state", pid))
    return errors


def _scan_count(execution):
    start, stop, step = (Decimal(str(execution[k])) for k in ("start_time_s", "stop_time_s", "step_size_s"))
    return int((stop - start) / step)


def _period_ms(execution):
    return int(Decimal(str(execution["step_size_s"])) * 1000)


def _targets(request):
    signals = {s["signal_id"]: s for s in request["execution"]["signals"]}
    return {b["signal_id"]: (b["target"], signals.get(b["signal_id"])) for b in request["bindings"]}


@_safe_semantics
def validate_plc_request(value, *, model=None):
    errors = validate(value, "automation/plc-scan-request")
    if errors:
        return errors
    run = value["execution"]
    errors.extend(validate_time_stepped_request(run))
    if errors:
        return errors
    if not _local(value["model_file"]):
        errors.append(problem("PROJECT_PATH", "model_file", "Use a confined project-relative path"))
    if run["clock"] != "fixed_ms" or run["time_axis"]["kind"] != "elapsed" or run["start_time_s"] != 0:
        errors.append(problem("PLC_TIME", "execution",
                              "A PLC scan uses the fixed_ms clock on elapsed time from a cold start at 0"))
    for signal in run["signals"]:
        if signal["data_type"] != "boolean":
            errors.append(problem("PLC_SIGNAL", "execution.signals",
                                  "CC-6 first slice signals are boolean", signal["signal_id"]))
    signal_ids = [s["signal_id"] for s in run["signals"]]
    bound = [b["signal_id"] for b in value["bindings"]]
    if len(bound) != len(set(bound)) or set(bound) != set(signal_ids):
        errors.append(problem("PLC_BINDING", "bindings", "Every signal needs exactly one binding"))
    if _scan_count(run) > MAX_SCANS:
        errors.append(problem("RUN_LIMIT", "execution.stop_time_s", f"More than {MAX_SCANS} scans"))
    if model is None or errors:
        return errors
    if _period_ms(run) != model["task"]["period_ms"]:
        errors.append(problem("PLC_TIME", "execution.step_size_s",
                              "Step size must equal the cyclic task period"))
    variables = _variables(model)
    process = model["process"]
    wired = set() if process is None else {process["wiring"]["contactor_feedback"], process["wiring"]["overload_ok"]}
    uses = {}
    for sid, (target, signal) in _targets(value).items():
        direction = signal["causality"]
        if target["kind"] == "variable":
            name = target["variable"]
            var = variables.get(name)
            wanted = "input" if direction == "input" else "output"
            if var is None or var["section"] != wanted or name in wired:
                errors.append(problem("PLC_BINDING", f"bindings.{sid}",
                    f"An {direction} signal binds to an unwired {wanted} variable", sid))
                continue
            key = ("variable", name)
        else:
            port = target["port"]
            ok = process is not None and (port in SCENARIO_PORTS) == (direction == "input")
            if not ok:
                errors.append(problem("PLC_BINDING", f"bindings.{sid}",
                    "Process ports need a process; scenario ports take inputs, state ports give outputs", sid))
                continue
            key = ("port", port)
        if key in uses:
            errors.append(problem("PLC_BINDING", f"bindings.{sid}",
                                  f"{key[1]} is already bound to {uses[key]}", sid))
        uses.setdefault(key, sid)
    for var in model["variables"]:
        if var["section"] == "input" and var["name"] not in wired and ("variable", var["name"]) not in uses:
            errors.append(problem("PLC_BINDING", "bindings",
                                  f"Input {var['name']} has no input signal", var["name"]))
        if var["section"] == "output" and ("variable", var["name"]) not in uses:
            errors.append(problem("PLC_BINDING", "bindings",
                                  f"Output {var['name']} has no output signal", var["name"]))
    if process is not None:
        for port in SCENARIO_PORTS:
            if ("port", port) not in uses:
                errors.append(problem("PLC_BINDING", "bindings",
                                      f"Process scenario input {port} has no input signal", port))
    return errors


def _ms(seconds):
    return Decimal(str(seconds)) * 1000


def plc_event_changes(series, request):
    """Input changes from a validated event series, in time then signal order.

    The row at 0 ms sets every input; later rows list every input and only values that
    differ from the previous row are changes. A change at t_e is first seen by the first
    scan that starts at or after t_e (Bolton pp. 106 to 107), or by none inside the run.
    """
    run = request["execution"]
    period, scans = _period_ms(run), _scan_count(run)
    changes, previous = [], {}
    for row in series["samples"]:
        time_ms = int(_ms(row["time"]))
        first = -(-time_ms // period)
        for signal in series["signals"]:
            sid = signal["signal_id"]
            value = row["values"][sid]["value"]
            if previous.get(sid) != value:
                changes.append({"signal_id": sid, "time_ms": time_ms, "value": value,
                                "first_scan": first if first < scans else None})
            previous[sid] = value
    return changes


@_safe_semantics
def validate_plc_events(value, *, request, raw_bytes=None):
    errors = validate_time_series(value)
    if errors:
        return errors
    run = request["execution"]
    if value["time_axis"] != run["time_axis"] or value["sampling"] != "instant":
        errors.append(problem("PLC_EVENTS", "time_axis",
                              "Input events are instant samples on the request's elapsed axis"))
    inputs = [s for s in run["signals"] if s["causality"] == "input"]
    if value["signals"] != inputs:
        errors.append(problem("PLC_EVENTS", "signals",
                              "Event signals must equal the request input signals, in order"))
        return errors
    stop = _ms(run["stop_time_s"])
    for i, row in enumerate(value["samples"]):
        time = _ms(row["time"])
        if time % 1 or time >= stop or (i == 0 and time != 0):
            errors.append(problem("PLC_EVENTS", f"samples.{i}.time",
                                  "Event times are whole ms from 0 and before the stop time"))
        if any(cell["status"] != "valid" for cell in row["values"].values()):
            errors.append(problem("PLC_EVENTS", f"samples.{i}.values",
                                  "A PLC input is never missing; every event cell must be valid"))
    if not value["samples"]:
        errors.append(problem("PLC_EVENTS", "samples", "The first event row at 0 ms sets every input"))
    if raw_bytes is not None and hashlib.sha256(raw_bytes).hexdigest() != request["events"]["sha256"]:
        errors.append(problem("PLC_EVENTS_HASH", "events.sha256", "Event file does not match its hash"))
    return errors


def _held(changes, signal_id, time_ms):
    value = None
    for change in changes:
        if change["signal_id"] == signal_id and change["time_ms"] <= time_ms:
            value = change["value"]
    return value


def _call_problems(step, scan_field):
    """Invariants that hold for every timer and counter call (spec section 6)."""
    block, inputs, outputs = step["block"], step["inputs"], step["outputs"]
    field = f"{scan_field}.statements.{step['instance']}"
    if set(outputs) != BLOCK_OUTPUTS[block]:
        return [problem("PLC_TRACE", field, f"{block} reports exactly {sorted(BLOCK_OUTPUTS[block])}")]
    if block in ("TON", "TOF", "TP"):
        preset = inputs.get("PT", 0)
        if not typed(preset, "TIME") or preset < 0:
            return [problem("PLC_TIMER", field, "Timer preset PT must be a non-negative TIME")]
        if not 0 <= outputs["ET"] <= preset:
            return [problem("PLC_TIMER", field, "Elapsed time ET must lie between 0 and PT")]
        return []
    pv, cv = inputs.get("PV", 0), outputs["CV"]
    if not (typed(pv, "INT") and typed(cv, "INT")):
        return [problem("PLC_COUNTER", field, "PV and CV are INT")]
    expected = {"CTU": {"Q": cv >= pv}, "CTD": {"Q": cv <= 0}, "CTUD": {"QU": cv >= pv, "QD": cv <= 0}}[block]
    if block in ("CTD", "CTUD") and cv < 0:
        return [problem("PLC_COUNTER", field, "Down counting stops at 0")]
    if any(outputs[k] != v for k, v in expected.items()):
        return [problem("PLC_COUNTER", field, "Counter outputs disagree with CV and PV")]
    return []


def _process_after(before, scenario, coil):
    """Authored motor-starter transition table (docs/specs/plc-program-and-scan.md section 5)."""
    tripped = scenario["overload_event"] or (before["overload_tripped"] and not scenario["overload_reset"])
    closed = coil and not tripped
    return {"contactor_closed": closed, "overload_tripped": tripped, "motor_running": closed}


@_safe_semantics
def validate_plc_result(value, *, request, model, events=None):
    errors = validate(value, "automation/plc-scan-result")
    if errors:
        return errors
    run = request["execution"]
    errors.extend(validate_time_stepped_result(value["execution"], request=run))
    if errors:
        return errors
    body = model["program"]["body"].encode("utf-8")
    if (value["program"]["program_id"] != model["program"]["program_id"]
            or value["program"]["body_sha256"] != hashlib.sha256(body).hexdigest()):
        errors.append(problem("PLC_PROGRAM", "program", "Result must identify the model's program and body hash"))
    period, total = _period_ms(run), _scan_count(run)
    steps = value["execution"]["steps"]
    completed = sum(1 for s in steps if s["operation"] == "step_to" and s["status"] == "success")
    scans = value["scans"]
    if len(scans) != completed:
        errors.append(problem("PLC_TRACE", "scans", "One scan trace per completed step"))
        return errors
    variables = _variables(model)
    names = {section: {n for n, v in variables.items() if v["section"] == section}
             for section in ("input", "output")}
    blocks = {i["name"]: i["block"] for i in model["instances"]}
    process = model["process"]
    state = None if process is None else dict(process["initial"])
    for k, scan in enumerate(scans):
        field = f"scans.{k}"
        if scan["scan"] != k or scan["start_ms"] != k * period or scan["commit_ms"] != (k + 1) * period:
            errors.append(problem("PLC_TRACE", field, "Scan k starts at k * period and commits one period later"))
        if set(scan["inputs"]) != names["input"] or set(scan["outputs"]) != names["output"]:
            errors.append(problem("PLC_TRACE", field, "Scan images name exactly the declared inputs and outputs"))
            continue
        if any(not typed(v, variables[n]["type"]) for n, v in (*scan["inputs"].items(), *scan["outputs"].items())):
            errors.append(problem("PLC_TRACE", field, "Image values must match their declared types"))
        if set(scan["blocks"]) != set(blocks) or any(
            set(s) != BLOCK_OUTPUTS[blocks[n]] for n, s in scan["blocks"].items()
        ):
            errors.append(problem("PLC_TRACE", f"{field}.blocks", "Every instance reports its block outputs"))
        for step in scan["statements"]:
            if step["kind"] == "call":
                if blocks.get(step["instance"]) != step["block"]:
                    errors.append(problem("PLC_TRACE", f"{field}.statements", "Call names a declared instance"))
                else:
                    errors.extend(_call_problems(step, field))
            elif step["kind"] == "assign":
                var = variables.get(step["target"])
                if var is None or var["section"] == "input" or not typed(step["value"], var["type"]):
                    errors.append(problem("PLC_TRACE", f"{field}.statements",
                                          f"Assignment to {step['target']} is not a typed output or internal"))
        if (scan["process"] is None) != (process is None):
            errors.append(problem("PLC_PROCESS", f"{field}.process", "Process trace exists only with a process"))
            continue
        if process is None:
            continue
        wiring, trace = process["wiring"], scan["process"]
        # One-scan feedback: scan k reads the process state committed after scan k-1.
        if (trace["before"] != state
                or scan["inputs"][wiring["contactor_feedback"]] != state["contactor_closed"]
                or scan["inputs"][wiring["overload_ok"]] != (not state["overload_tripped"])):
            errors.append(problem("PLC_PROCESS", f"{field}.process.before",
                                  "Scan inputs must read the process state left by the previous scan"))
        if trace["coil"] != scan["outputs"][wiring["coil"]] or trace["after"] != _process_after(
            trace["before"], trace["scenario"], trace["coil"]
        ):
            errors.append(problem("PLC_PROCESS", f"{field}.process.after",
                                  "Process state must follow the transition table"))
        state = {k2: trace["after"][k2] for k2 in ("contactor_closed", "overload_tripped")}
    if errors:
        return errors  # Later checks index the scan images, so they need a well-formed trace.
    # Series cells must repeat the scan images (sample i holds what scan i read and scan i-1 committed).
    initial_state = None if process is None else {
        **process["initial"], "motor_running": process["initial"]["contactor_closed"]}
    targets = _targets(request)
    for i, row in enumerate(value["execution"]["series"]["samples"]):
        for sid, (target, _) in targets.items():
            cell = row["values"][sid]["value"]
            if target["kind"] == "variable" and target["variable"] in names["output"]:
                want = _initial(variables[target["variable"]]) if i == 0 else scans[i - 1]["outputs"][target["variable"]]
            elif target["kind"] == "process_port" and target["port"] in STATE_PORTS:
                want = initial_state[target["port"]] if i == 0 else scans[i - 1]["process"]["after"][target["port"]]
            elif i < len(scans) and target["kind"] == "variable":
                want = scans[i]["inputs"][target["variable"]]
            elif i < len(scans):
                want = scans[i]["process"]["scenario"][target["port"]]
            else:
                continue
            if cell != want:
                errors.append(problem("PLC_SERIES", f"execution.series.samples.{i}.values.{sid}",
                                      "Series value disagrees with the scan trace", sid))
    for n, change in enumerate(value["events"]):
        first = -(-change["time_ms"] // period)
        if change["first_scan"] != (first if first < total else None):
            errors.append(problem("PLC_EVENTS", f"events.{n}.first_scan",
                                  "An event is first seen by the first scan starting at or after it"))
    if events is not None and value["events"] != plc_event_changes(events, request):
        errors.append(problem("PLC_EVENTS", "events", "Event list must repeat the request's event file"))
    for k, scan in enumerate(scans):
        for sid, (target, signal) in targets.items():
            if signal["causality"] != "input":
                continue
            held = _held(value["events"], sid, scan["start_ms"])
            seen = (scan["inputs"][target["variable"]] if target["kind"] == "variable"
                    else scan["process"]["scenario"][target["port"]])
            if held != seen:
                errors.append(problem("PLC_EVENTS", f"scans.{k}.inputs",
                                      f"Scan input from {sid} must be the latest event at or before its start", sid))
    return errors
