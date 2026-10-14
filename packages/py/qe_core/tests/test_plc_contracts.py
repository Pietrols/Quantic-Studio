"""CC-6 PLC contracts against an original, handwritten motor-starter scan table.

Every expected value below was worked by hand from docs/specs/plc-program-and-scan.md
(scan ordering after Bolton, Programmable Logic Controllers, 6th ed, 2015, pp. 106 to
107; the authored motor-starter transition table in section 5). No engine produced it.

Program body (period 100 ms, run 400 ms, so four scans):

    Coil := (Start OR Coil) AND NOT Stop AND Permissive AND OverloadOk;   (line 1)
    FbTimer(IN := Coil AND NOT Feedback, PT := T#200ms);                  (line 2)
    Fault := FbTimer.Q;                                                   (line 3)

Input events: Start rises at 50 ms and falls at 200 ms; the overload event starts at
250 ms. Permissive is TRUE throughout.

| scan | start | Start | Fdbk | OL ok | Coil | timer IN, ET, Q | before c/t | event | after c/t/run |
| 0    | 0     | F     | F    | T     | F    | F, 0, F         | F/F        | F     | F/F/F         |
| 1    | 100   | T     | F    | T     | T    | T, 0, F         | F/F        | F     | T/F/T         |
| 2    | 200   | F     | T    | T     | T    | F, 0, F         | T/F        | F     | T/F/T         |
| 3    | 300   | F     | T    | T     | T    | F, 0, F         | T/F        | T     | F/T/F         |

Scan 1 latches the coil; the contactor closes at the commit (100 to 200 ms) and scan 2
is the first to read the feedback (one-scan feedback). At scan 3 the overload event
trips the relay, whose contact opens the contactor although the PLC coil is still TRUE:
the PLC only reads OverloadOk = FALSE at scan 4, outside this run.
"""

import copy
import hashlib
import json
import shutil
from pathlib import Path

import pytest
from qe_core import load_project
from qe_core.plc_contracts import (
    RESERVED,
    plc_event_changes,
    validate_plc_events,
    validate_plc_model,
    validate_plc_request,
    validate_plc_result,
)

ROOT = Path(__file__).resolve().parents[4]
F, T = False, True
BODY = (
    "Coil := (Start OR Coil) AND NOT Stop AND Permissive AND OverloadOk;\n"
    "FbTimer(IN := Coil AND NOT Feedback, PT := T#200ms);\n"
    "Fault := FbTimer.Q;\n"
)
INPUT_SIGNALS = ["start", "stop", "permissive", "ol_event", "ol_reset"]
OUTPUT_SIGNALS = ["coil", "fault", "running"]


def codes(problems):
    return {p.code for p in problems}


def model():
    return {
        "schema_version": "0.1.0",
        "controller_id": "starter-plc",
        "name": "Authored motor starter",
        "language": "quantic-st-0.1",
        "program": {"program_id": "MotorStarter", "body": BODY},
        "variables": [
            {"name": n, "section": "input", "type": "BOOL"}
            for n in ["Start", "Stop", "Permissive", "Feedback", "OverloadOk"]
        ]
        + [
            {"name": "Coil", "section": "output", "type": "BOOL", "initial": False},
            {"name": "Fault", "section": "output", "type": "BOOL"},
        ],
        "instances": [{"name": "FbTimer", "block": "TON"}],
        "task": {"task_id": "main", "kind": "cyclic", "period_ms": 100},
        "devices": [
            {"device_id": "start-button", "label": "Start pushbutton", "io": ["Start"]},
            {"device_id": "k1", "label": "Contactor K1", "io": ["Coil", "Feedback"]},
        ],
        "process": {
            "process_id": "motor-1",
            "kind": "motor_starter",
            "wiring": {"coil": "Coil", "contactor_feedback": "Feedback", "overload_ok": "OverloadOk"},
            "initial": {"contactor_closed": False, "overload_tripped": False},
        },
    }


def signal(sid, causality):
    return {
        "schema_version": "0.1.0",
        "signal_id": sid,
        "model_id": "starter",
        "name": sid,
        "data_type": "boolean",
        "unit": "1",
        "causality": causality,
    }


def request():
    def var(name):
        return {"kind": "variable", "variable": name}

    def port(name):
        return {"kind": "process_port", "port": name}

    targets = {
        "start": var("Start"), "stop": var("Stop"), "permissive": var("Permissive"),
        "ol_event": port("overload_event"), "ol_reset": port("overload_reset"),
        "coil": var("Coil"), "fault": var("Fault"), "running": port("motor_running"),
    }
    return {
        "schema_version": "0.1.0",
        "model_file": "starter.json",
        "execution": {
            "schema_version": "0.1.0",
            "request_id": "starter-run",
            "study_id": "starter-scan",
            "model_id": "starter",
            "time_axis": {"kind": "elapsed", "unit": "s"},
            "clock": "fixed_ms",
            "start_time_s": 0,
            "stop_time_s": 0.4,
            "step_size_s": 0.1,
            "signals": [signal(s, "input") for s in INPUT_SIGNALS]
            + [signal(s, "output") for s in OUTPUT_SIGNALS],
            "input_series_file": "starter-events.json",
        },
        "start": "cold",
        "events": {"sha256": "0" * 64, "classification": "authored",
                   "description": "Original authored start and overload scenario"},
        "bindings": [{"signal_id": s, "target": t} for s, t in targets.items()],
    }


def cell(value):
    return {"value": value, "status": "valid", "diagnostics": []}


def row(time, values, names):
    return {"time": time, "values": {n: cell(v) for n, v in zip(names, values)}}


def events():
    #            start stop perm  event reset
    rows = [(0, [F, F, T, F, F]), (0.05, [T, F, T, F, F]),
            (0.2, [F, F, T, F, F]), (0.25, [F, F, T, T, F])]
    return {
        "schema_version": "0.1.0",
        "series_id": "starter-events",
        "time_axis": {"kind": "elapsed", "unit": "s"},
        "sampling": "instant",
        "signals": [signal(s, "input") for s in INPUT_SIGNALS],
        "samples": [row(t, v, INPUT_SIGNALS) for t, v in rows],
        "diagnostics": [],
    }


# Handwritten table from the module docstring.
SCANS = [
    # inputs Start, Feedback, OverloadOk; Coil; timer IN; before; event; after
    (F, F, T, F, F, (F, F), F, (F, F, F)),
    (T, F, T, T, T, (F, F), F, (T, F, T)),
    (F, T, T, T, F, (T, F), F, (T, F, T)),
    (F, T, T, T, F, (T, F), T, (F, T, F)),
]


def scans():
    out = []
    for k, (start, fb, ok, coil, timer_in, before, event, after) in enumerate(SCANS):
        out.append({
            "scan": k, "start_ms": 100 * k, "commit_ms": 100 * (k + 1),
            "inputs": {"Start": start, "Stop": F, "Permissive": T, "Feedback": fb, "OverloadOk": ok},
            "statements": [
                {"line": 1, "kind": "assign", "target": "Coil",
                 "expression": "(Start OR Coil) AND NOT Stop AND Permissive AND OverloadOk", "value": coil},
                {"line": 2, "kind": "call", "instance": "FbTimer", "block": "TON",
                 "inputs": {"IN": timer_in, "PT": 200}, "outputs": {"Q": F, "ET": 0}},
                {"line": 3, "kind": "assign", "target": "Fault", "expression": "FbTimer.Q", "value": F},
            ],
            "outputs": {"Coil": coil, "Fault": F},
            "blocks": {"FbTimer": {"Q": F, "ET": 0}},
            "process": {
                "before": {"contactor_closed": before[0], "overload_tripped": before[1]},
                "scenario": {"overload_event": event, "overload_reset": F},
                "coil": coil,
                "after": {"contactor_closed": after[0], "overload_tripped": after[1], "motor_running": after[2]},
            },
        })
    return out


# Series samples at 0, 100, 200, 300, 400 ms: inputs read at that time, outputs committed.
SERIES = [
    #  start stop perm event reset | coil fault running
    ([F, F, T, F, F], [F, F, F]),
    ([T, F, T, F, F], [F, F, F]),
    ([F, F, T, F, F], [T, F, T]),
    ([F, F, T, T, F], [T, F, T]),
    ([F, F, T, T, F], [T, F, F]),
]


def result():
    req = request()
    names = INPUT_SIGNALS + OUTPUT_SIGNALS
    samples = [row(i / 10, a + b, names) for i, (a, b) in enumerate(SERIES)]
    steps = [{
        "schema_version": "0.1.0", "session_id": "run-1", "operation": "initialise",
        "state_before": "instantiated", "state_after": "initialized", "current_time_s": 0,
        "requested_time_s": 0, "reached_time_s": 0, "status": "success",
        "inputs": {}, "outputs": {}, "diagnostics": [],
    }]
    for k in range(4):
        steps.append({
            "schema_version": "0.1.0", "session_id": "run-1", "operation": "step_to",
            "state_before": "initialized" if k == 0 else "running", "state_after": "running",
            "current_time_s": k / 10, "requested_time_s": (k + 1) / 10, "reached_time_s": (k + 1) / 10,
            "status": "success",
            "inputs": {s: cell(v) for s, v in zip(INPUT_SIGNALS, SERIES[k][0])},
            "outputs": {s: cell(v) for s, v in zip(OUTPUT_SIGNALS, SERIES[k + 1][1])},
            "diagnostics": [],
        })
    execution = {
        "schema_version": "0.1.0", "result_id": "starter-result", "request_id": "starter-run",
        "study_id": "starter-scan", "model_id": "starter", "status": "complete",
        "requested_end_time_s": 0.4, "reached_time_s": 0.4,
        "series": {"schema_version": "0.1.0", "series_id": "starter-trace",
                   "time_axis": {"kind": "elapsed", "unit": "s"}, "sampling": "instant",
                   "signals": copy.deepcopy(req["execution"]["signals"]), "samples": samples,
                   "diagnostics": []},
        "steps": steps, "working": [], "model_versions": {"starter": "0.1.0"},
        "input_files": [{"path": "starter.json", "role": "model", "sha256": "1" * 64},
                        {"path": "starter-scan.json", "role": "request", "sha256": "2" * 64},
                        {"path": "starter-events.json", "role": "data", "sha256": "3" * 64}],
        "provenance": {"solver_name": "authored-reference", "solver_version": "1",
                       "input_hash_sha256": "4" * 64, "timestamp": "2026-10-14T00:00:00Z"},
        "diagnostics": [],
    }
    # Handwritten: all five inputs at 0 ms; Start at 50 and 200 ms; overload event at 250 ms.
    changes = [{"signal_id": s, "time_ms": 0, "value": v, "first_scan": 0}
               for s, v in zip(INPUT_SIGNALS, [F, F, T, F, F])]
    changes += [{"signal_id": "start", "time_ms": 50, "value": T, "first_scan": 1},
                {"signal_id": "start", "time_ms": 200, "value": F, "first_scan": 2},
                {"signal_id": "ol_event", "time_ms": 250, "value": T, "first_scan": 3}]
    return {
        "schema_version": "0.1.0", "execution": execution, "language": "quantic-st-0.1",
        "program": {"program_id": "MotorStarter", "body_sha256": hashlib.sha256(BODY.encode()).hexdigest()},
        "events": changes, "scans": scans(),
        "limitations": ["Authored discrete process; no motor dynamics, no safety rating, no IEC 61131-3 claim"],
    }


def check(res=None, ev=None):
    return validate_plc_result(result() if res is None else res, request=request(), model=model(),
                               events=events() if ev is None else ev)


def test_handwritten_motor_starter_is_valid():
    assert validate_plc_model(model()) == []
    assert validate_plc_request(request(), model=model()) == []
    assert validate_plc_events(events(), request=request()) == []
    assert check() == []


def test_event_changes_match_the_handwritten_list():
    assert plc_event_changes(events(), request()) == result()["events"]


# Model: declarations, I/O types, devices, wiring and duplicate instances.
@pytest.mark.parametrize("mutate,code", [
    (lambda m: m["instances"].append({"name": "fbtimer", "block": "TOF"}), "DUPLICATE_NAME"),
    (lambda m: m["instances"].append({"name": "FbTimer", "block": "TON"}), "DUPLICATE_NAME"),
    (lambda m: m["variables"].append({"name": "Elsif", "section": "internal", "type": "INT"}), "RESERVED_NAME"),
    (lambda m: m["variables"].append({"name": "Speed", "section": "input", "type": "INT"}), "PLC_IO_TYPE"),
    (lambda m: m["variables"][0].update(initial=True), "PLC_INITIAL"),
    (lambda m: m["variables"].append({"name": "N", "section": "internal", "type": "INT", "initial": 32768}),
     "PLC_INITIAL"),
    (lambda m: m["variables"].append({"name": "N", "section": "internal", "type": "INT", "initial": 1.0}),
     "PLC_INITIAL"),
    (lambda m: m["variables"].append({"name": "X", "section": "internal", "type": "REAL", "initial": 1e39}),
     "PLC_INITIAL"),
    (lambda m: m["variables"].append({"name": "D", "section": "internal", "type": "TIME", "initial": 2**31}),
     "PLC_INITIAL"),
    (lambda m: m["devices"][0]["io"].append("Coil"), "PLC_DEVICE"),
    (lambda m: m["devices"].append({"device_id": "k1", "label": "Copy", "io": ["Stop"]}), "DUPLICATE_ID"),
    (lambda m: m["devices"][0].update(io=["Ghost"]), "PLC_DEVICE"),
    (lambda m: m["process"]["wiring"].update(coil="Start"), "PLC_WIRING"),
    (lambda m: m["process"]["wiring"].update(overload_ok="Feedback"), "PLC_WIRING"),
    (lambda m: m["process"]["initial"].update(contactor_closed=True), "PLC_PROCESS_STATE"),
])
def test_model_errors_name_their_element(mutate, code):
    m = model()
    mutate(m)
    problems = validate_plc_model(m)
    assert code in codes(problems)
    assert all(p.element_ref and p.element_ref["field"] for p in problems)


def test_model_schema_rejects_unsupported_shapes():
    for mutate in [
        lambda m: m["instances"].append({"name": "Loop", "block": "FOR"}),
        lambda m: m["variables"].append({"name": "S", "section": "internal", "type": "STRING"}),
        lambda m: m["variables"].append({"name": "2bad", "section": "internal", "type": "INT"}),
        lambda m: m["task"].update(kind="event"),
        lambda m: m["task"].update(period_ms=0),
        lambda m: m.update(language="iec-61131-3"),
    ]:
        m = model()
        mutate(m)
        assert validate_plc_model(m)


# Request: invalid I/O bindings, signal types and scan grid.
@pytest.mark.parametrize("mutate,code", [
    (lambda r: r["bindings"].pop(0), "PLC_BINDING"),  # Start has no source
    (lambda r: r["bindings"][0]["target"].update(variable="Coil"), "PLC_BINDING"),  # input to output
    (lambda r: r["bindings"][5]["target"].update(variable="Start"), "PLC_BINDING"),  # output to input
    (lambda r: r["bindings"][0]["target"].update(variable="Feedback"), "PLC_BINDING"),  # process-wired
    (lambda r: r["bindings"][1]["target"].update(variable="Start"), "PLC_BINDING"),  # bound twice
    (lambda r: r["bindings"][3].update(target={"kind": "process_port", "port": "motor_running"}), "PLC_BINDING"),
    (lambda r: r["execution"]["signals"][0].update(data_type="real"), "PLC_SIGNAL"),
    (lambda r: r["execution"].update(step_size_s=0.05, stop_time_s=0.4), "PLC_TIME"),
    (lambda r: r["execution"].update(clock="fixed_s"), "PLC_TIME"),
    (lambda r: r["execution"].update(start_time_s=0.1), "PLC_TIME"),
    (lambda r: r["execution"].update(stop_time_s=10_000.1), "RUN_LIMIT"),
    (lambda r: r.update(model_file="../starter.json"), "PROJECT_PATH"),
])
def test_request_errors(mutate, code):
    r = request()
    mutate(r)
    assert code in codes(validate_plc_request(r, model=model()))


def test_request_without_process_rejects_process_ports():
    m = model()
    m["process"] = None
    assert "PLC_BINDING" in codes(validate_plc_request(request(), model=m))


# Events: scan/event alignment.
@pytest.mark.parametrize("mutate,code", [
    (lambda e: e["samples"][1].update(time=0.0505), "PLC_EVENTS"),  # not a whole ms
    (lambda e: e["samples"].pop(0), "PLC_EVENTS"),  # nothing at 0 ms
    (lambda e: e["samples"].append(row(0.4, [F, F, T, T, F], INPUT_SIGNALS)), "PLC_EVENTS"),  # at stop
    (lambda e: e.update(sampling="interval_mean"), "TIME_ALIGNMENT"),  # CC-4 rejects it first
    (lambda e: e["signals"].reverse(), "PLC_EVENTS"),
])
def test_event_alignment(mutate, code):
    e = events()
    mutate(e)
    assert code in codes(validate_plc_events(e, request=request()))


def test_missing_event_cell_is_rejected():
    e = events()
    e["samples"][2]["values"]["start"] = {"value": None, "status": "missing", "diagnostics": [{
        "code": "AUTHORED", "message": "gap", "severity": "warning",
        "element_ref": {"element_type": "signal", "element_id": "start", "field": "value"}}]}
    assert "PLC_EVENTS" in codes(validate_plc_events(e, request=request()))


def test_event_between_scans_is_seen_by_the_next_scan_only():
    # Start at 50 ms is first seen by scan 1 (100 ms), never by scan 0 (Bolton pp. 106 to 107).
    res = result()
    res["scans"][0]["inputs"]["Start"] = T
    assert "PLC_EVENTS" in codes(check(res))
    res = result()
    res["events"][5]["first_scan"] = 0
    assert "PLC_EVENTS" in codes(check(res))


# Result: trace coverage, timer presets, counters, feedback timing and series agreement.
@pytest.mark.parametrize("mutate,code", [
    (lambda r: r["scans"].pop(), "PLC_TRACE"),
    (lambda r: r["scans"][1].update(start_ms=150), "PLC_TRACE"),
    (lambda r: r["scans"][1]["inputs"].pop("Stop"), "PLC_TRACE"),
    (lambda r: r["scans"][1]["blocks"].pop("FbTimer"), "PLC_TRACE"),
    (lambda r: r["scans"][1]["statements"][0].update(target="Start"), "PLC_TRACE"),
    (lambda r: r["scans"][1]["statements"][1]["inputs"].update(PT=-1), "PLC_TIMER"),
    (lambda r: r["scans"][1]["statements"][1]["outputs"].update(ET=300), "PLC_TIMER"),
    (lambda r: r["scans"][1]["statements"][1].update(instance="Ghost"), "PLC_TRACE"),
    (lambda r: r["scans"][2]["inputs"].update(Feedback=F), "PLC_PROCESS"),  # feedback not one scan late
    (lambda r: r["scans"][1]["inputs"].update(Feedback=T), "PLC_PROCESS"),  # feedback in the same scan
    (lambda r: r["scans"][3]["process"]["after"].update(contactor_closed=T, overload_tripped=T), "PLC_PROCESS"),
    (lambda r: r["scans"][1].update(process=None), "PLC_PROCESS"),
    (lambda r: r["execution"]["series"]["samples"][2]["values"]["coil"].update(value=F), "PLC_SERIES"),
    (lambda r: r["program"].update(body_sha256="0" * 64), "PLC_PROGRAM"),
])
def test_result_errors(mutate, code):
    res = result()
    mutate(res)
    assert code in codes(check(res))


def test_counter_trace_invariants():
    m = model()
    m["instances"].append({"name": "Trips", "block": "CTUD"})
    res = result()
    for scan in res["scans"]:
        scan["blocks"]["Trips"] = {"QU": F, "QD": T, "CV": 0}
    call = {"line": 4, "kind": "call", "instance": "Trips", "block": "CTUD",
            "inputs": {"CU": F, "CD": T, "PV": 2}, "outputs": {"QU": F, "QD": T, "CV": 0}}
    res["scans"][0]["statements"].append(call)
    assert validate_plc_result(res, request=request(), model=m, events=events()) == []
    call["outputs"].update(CV=-1)  # down counting stops at 0 (Bolton p. 246)
    assert "PLC_COUNTER" in codes(validate_plc_result(res, request=request(), model=m, events=events()))
    call["outputs"].update(CV=2, QU=F, QD=F)  # QU must be TRUE when CV >= PV
    assert "PLC_COUNTER" in codes(validate_plc_result(res, request=request(), model=m, events=events()))


def test_partial_run_keeps_completed_scans():
    # A runtime fault in scan 2 keeps scans 0 and 1, reaches 200 ms and names the fault.
    res = result()
    ex = res["execution"]
    fault = {"code": "DIVIDE_BY_ZERO", "message": "Division by zero", "severity": "error",
             "element_ref": {"element_type": "program", "element_id": "MotorStarter", "field": "program.body:1:9"}}
    ex.update(status="partial", reached_time_s=0.2, diagnostics=[fault])
    ex["series"]["samples"] = ex["series"]["samples"][:3]
    failed = copy.deepcopy(ex["steps"][3])
    failed.update(status="failed", state_after="error", reached_time_s=0.2, outputs={}, diagnostics=[fault])
    ex["steps"] = ex["steps"][:3] + [failed]
    res["scans"] = res["scans"][:2]
    assert check(res) == []
    ex["diagnostics"] = []
    assert check(res)


def test_reserved_words_cover_the_subset_spec():
    spec = (ROOT / "docs/specs/structured-text-subset.md").read_text()
    for word in ["FOR", "WHILE", "CASE", "FUNCTION_BLOCK", "POINTER", "ARRAY", "STRUCT", "DINT", "LREAL", "STRING"]:
        assert word in spec and word in RESERVED


@pytest.fixture
def mixed(tmp_path):
    shutil.copytree(ROOT / "examples/multi_domain", tmp_path, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("out"))
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    raw = json.dumps(events()).encode()
    req = request()
    req["events"]["sha256"] = hashlib.sha256(raw).hexdigest()
    (tmp_path / "starter-events.json").write_bytes(raw)
    (tmp_path / "starter.json").write_text(json.dumps(model()))
    (tmp_path / "starter-scan.json").write_text(json.dumps(req))
    manifest["models"].append({"model_id": "starter", "model_type": "automation.plc", "file": "starter.json"})
    manifest["studies"].append({"study_id": "starter-scan", "study_type": "plc.scan",
                                "model_id": "starter", "request_file": "starter-scan.json"})
    manifest["asset_registry"]["assets"].append({"asset_id": "motor-1-contactor", "name": "K1",
        "representations": [{"model_id": "starter", "element_type": "devices", "element_id": "k1"}]})
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    return tmp_path


def test_mixed_project_preserves_foreign_placeholder_and_power(mixed):
    before = {p.name: p.read_bytes() for p in mixed.glob("*.json")}
    loaded = load_project(mixed)
    assert loaded.ok, loaded.diagnostics
    assert loaded.value.model("starter").data == model()
    # The CC-3 placeholder declares no CC-6 version: stored, not validated, not executable.
    assert loaded.value.model("control").data == json.loads(before["control.json"])
    assert "DEFERRED_MODEL_VALIDATION" in {d.code for d in loaded.diagnostics}
    assert mixed / "starter-events.json" in loaded.value.files
    assert all(p.read_bytes() == before[p.name] for p in mixed.glob("*.json"))


@pytest.mark.parametrize("case", ["asset", "hash", "alias", "model-type", "study", "parent", "bad-model"])
def test_mixed_invalid_binding(mixed, case):
    mp, rp = mixed / "manifest.json", mixed / "starter-scan.json"
    manifest, req = json.loads(mp.read_text()), json.loads(rp.read_text())
    if case == "asset":
        manifest["asset_registry"]["assets"][-1]["representations"][0]["element_id"] = "ghost"
    elif case == "hash":
        req["events"]["sha256"] = "f" * 64
    elif case == "alias":
        req["execution"]["input_series_file"] = "scan.json"
    elif case == "model-type":
        manifest["studies"][-1]["model_id"] = "control"
        req["execution"]["model_id"] = "control"
    elif case == "study":
        req["execution"]["study_id"] = "other"
    elif case == "parent":
        req["execution"]["input_series_file"] = "../outside.json"
    else:
        bad = model()
        bad["variables"][0]["initial"] = True
        (mixed / "starter.json").write_text(json.dumps(bad))
    mp.write_text(json.dumps(manifest))
    rp.write_text(json.dumps(req))
    loaded = load_project(mixed)
    assert not loaded.ok
    assert all(d.element_ref and d.element_ref["field"] for d in loaded.diagnostics if d.severity == "error")


def test_plc_version_gate_keeps_legacy_loading_light():
    import subprocess
    import sys

    subprocess.run(
        [sys.executable, "-c",
         "import sys; from qe_core import load_project; "
         "assert load_project('examples/multi_domain').ok; "
         "assert 'qe_core.plc_contracts' not in sys.modules"],
        cwd=ROOT, check=True,
    )
