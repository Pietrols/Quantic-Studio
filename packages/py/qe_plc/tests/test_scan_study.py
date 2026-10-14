"""CC-6 scan study against a handwritten table (WP-2.9).

Fixture: tests/fixtures/plc/motor_starter (original authored scenario). The table below
was worked by hand, scan by scan, from docs/specs/plc-program-and-scan.md sections 4 and
5 and the block rules in structured-text-subset.md section 6. Period 100 ms, 12 scans.

Body: Run := (Start OR Run) AND NOT Stop AND Permissive AND OverloadOk;  Coil := Run;
FbTimer(IN := Coil AND NOT Feedback, PT := T#200ms); Fault := FbTimer.Q;
Starts(CU := Coil, R := Reset, PV := 2); StartCount := Starts.CV;

Story: scan 1 Start is refused (no permissive); scan 3 starts; scan 4 first sees the
feedback (one scan late), so the 200 ms supervision timer never expires; the overload
event at 550 ms trips the relay at the scan 6 commit while the coil is still on; scan 7
reads OverloadOk = FALSE and refuses Start; the reset at 800 ms clears the relay; scan 9
restarts and the counter reaches PV 2; Stop at scan 10 drops it; Reset at scan 11 clears
the counter.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest
from qe_core.plc_contracts import validate_plc_result
from qe_plc import compose, run_scan_study

ROOT = Path(__file__).resolve().parents[4]
FIXTURE = ROOT / "tests/fixtures/plc/motor_starter"
F, T = False, True
STAMP = "2026-10-14T00:00:00Z"

# scan: Start Stop Perm Reset Fdbk OLok | Run Coil | timer IN | CV Q | event reset | after C O run
TABLE = [
    (F, F, F, F, F, T, F, F, F, 0, F, F, F, (F, F, F)),
    (T, F, F, F, F, T, F, F, F, 0, F, F, F, (F, F, F)),
    (F, F, F, F, F, T, F, F, F, 0, F, F, F, (F, F, F)),
    (T, F, T, F, F, T, T, T, T, 1, F, F, F, (T, F, T)),
    (F, F, T, F, T, T, T, T, F, 1, F, F, F, (T, F, T)),
    (F, F, T, F, T, T, T, T, F, 1, F, F, F, (T, F, T)),
    (F, F, T, F, T, T, T, T, F, 1, F, T, F, (F, T, F)),
    (T, F, T, F, F, F, F, F, F, 1, F, F, F, (F, T, F)),
    (F, F, T, F, F, F, F, F, F, 1, F, F, T, (F, F, F)),
    (T, F, T, F, F, T, T, T, T, 2, T, F, F, (T, F, T)),
    (F, T, T, F, T, T, F, F, F, 2, T, F, F, (F, F, F)),
    (F, F, T, T, F, T, F, F, F, 0, F, F, F, (F, F, F)),
]


def load():
    raw = {name: (FIXTURE / name).read_bytes() for name in ("model.json", "scan.json", "events.json")}
    files = [{"path": f"plc/{name}", "role": role, "sha256": hashlib.sha256(raw[name]).hexdigest()}
             for name, role in (("model.json", "model"), ("scan.json", "request"), ("events.json", "data"))]
    return (*(json.loads(raw[n]) for n in ("model.json", "scan.json", "events.json")), files)


def run(model=None, request=None, events=None):
    m, r, e, files = load()
    return run_scan_study(model or m, request or r, events or e, input_files=files, timestamp=STAMP)


def test_motor_starter_matches_the_handwritten_table():
    result, diagnostics = run()
    assert diagnostics == []
    assert result["execution"]["status"] == "complete"
    scans = result["scans"]
    assert len(scans) == 12
    for k, (start, stop, perm, reset, fb, ok, run_, coil, timer_in, cv, cq, ev, rst, after) in enumerate(TABLE):
        scan = scans[k]
        assert scan["start_ms"] == 100 * k and scan["commit_ms"] == 100 * (k + 1)
        assert scan["inputs"] == {"Start": start, "Stop": stop, "Permissive": perm, "Reset": reset,
                                  "Feedback": fb, "OverloadOk": ok}, k
        values = {s["target"]: s["value"] for s in scan["statements"] if s["kind"] == "assign"}
        assert values == {"Run": run_, "Coil": coil, "Fault": F, "StartCount": cv}, k
        timer = next(s for s in scan["statements"] if s.get("instance") == "FbTimer")
        assert timer["inputs"] == {"IN": timer_in, "PT": 200} and timer["outputs"] == {"Q": F, "ET": 0}, k
        assert scan["blocks"]["Starts"] == {"Q": cq, "CV": cv}, k
        assert scan["process"]["scenario"] == {"overload_event": ev, "overload_reset": rst}, k
        assert scan["process"]["after"] == dict(zip(("contactor_closed", "overload_tripped", "motor_running"),
                                                    after)), k


def test_interlocks_hold_at_every_scan():
    result, _ = run()
    for scan in result["scans"]:
        if scan["outputs"]["Coil"]:
            assert scan["inputs"]["Permissive"] and scan["inputs"]["OverloadOk"] and not scan["inputs"]["Stop"]
        if scan["process"]["after"]["contactor_closed"]:
            assert scan["process"]["coil"] and not scan["process"]["after"]["overload_tripped"]


def test_result_satisfies_the_cc6_contract_and_lines_refer_to_the_body():
    model, request, events, _ = load()
    result, _ = run()
    assert validate_plc_result(result, request=request, model=model, events=events) == []
    assert [s["line"] for s in result["scans"][0]["statements"]] == [2, 3, 4, 5, 6, 7]
    assert result["events"][-1] == {"signal_id": "reset", "time_ms": 1100, "value": T, "first_scan": 11}
    # 550 ms lies between scans: first seen by scan 6, which starts at 600 ms.
    assert {"signal_id": "ol_event", "time_ms": 550, "value": T, "first_scan": 6} in result["events"]


def test_replay_is_deterministic_and_inputs_untouched():
    before = {p.name: p.read_bytes() for p in FIXTURE.iterdir()}
    first, _ = run()
    second, _ = run()
    assert first == second
    assert {p.name: p.read_bytes() for p in FIXTURE.iterdir()} == before


def test_compose_puts_the_body_after_a_counted_header():
    model, *_ = load()
    text, header = compose(model)
    assert text.splitlines()[header:header + 2] == model["program"]["body"].splitlines()[:2]


def test_runtime_fault_keeps_completed_scans():
    model, request, events, _ = load()
    model["variables"].append({"name": "N", "section": "internal", "type": "INT", "initial": 0})
    # Scan 0: N = 1, 10 / (3 - 1); scan 1: N = 2, 10 / 1; scan 2: N = 3, 10 / 0 faults.
    model["program"]["body"] += "N := N + 1;\nStartCount := 10 / (3 - N);\n"
    result, diagnostics = run(model=model)
    assert result["execution"]["status"] == "partial"
    assert len(result["scans"]) == 2 and result["execution"]["reached_time_s"] == 0.2
    assert diagnostics[0]["code"] == "DIVIDE_BY_ZERO"
    assert diagnostics[0]["element_ref"]["field"] == "program.body:9:18"  # the / operator
    assert validate_plc_result(result, request=request, model=model, events=events) == []


def test_static_error_is_a_failed_result_with_body_position():
    model, request, events, _ = load()
    model["program"]["body"] = "Coil := Run\nFault := TRUE;\n"
    result, diagnostics = run(model=model)
    assert result["execution"]["status"] == "failed" and result["scans"] == []
    assert diagnostics[0]["code"] == "SYNTAX"
    assert diagnostics[0]["element_ref"]["field"].startswith("program.body:2:")
    assert validate_plc_result(result, request=request, model=model, events=events) == []


@pytest.mark.parametrize("body,code", [
    ("FOR i := 1 TO 3 DO END_FOR;\n", "UNSUPPORTED_SYNTAX"),
    ("Coil := Ghost;\n", "UNKNOWN_NAME"),
    ("Start := TRUE;\n", "READ_ONLY"),
    ("FbTimer(IN := TRUE, PT := T#0ms - T#1ms);\n", "TIMER_PRESET"),
])
def test_program_errors_name_the_body_position(body, code):
    model, *_ = load()
    model["program"]["body"] = body
    _, diagnostics = run(model=model)
    assert diagnostics[0]["code"] == code
    assert diagnostics[0]["element_ref"]["field"].startswith("program.body:1:")


def test_invalid_contract_inputs_do_not_run():
    model, request, events, _ = load()
    bad = copy.deepcopy(request)
    bad["bindings"].pop(0)
    result, diagnostics = run(request=bad)
    assert result is None and diagnostics[0]["code"] == "PLC_BINDING"
    bad = copy.deepcopy(events)
    bad["samples"][1]["time"] = 0.1005
    result, diagnostics = run(events=bad)
    assert result is None and diagnostics[0]["code"] == "PLC_EVENTS"


def test_initial_values_and_reals_survive_composition():
    model, *_ = load()
    model["variables"] += [
        {"name": "Gain", "section": "internal", "type": "REAL", "initial": 1e-05},
        {"name": "Big", "section": "internal", "type": "REAL", "initial": 2.5e20},
        {"name": "Delay", "section": "internal", "type": "TIME", "initial": -5},
        {"name": "Low", "section": "internal", "type": "INT", "initial": -32768},
    ]
    result, diagnostics = run(model=model)
    assert diagnostics == [] and result["execution"]["status"] == "complete"
