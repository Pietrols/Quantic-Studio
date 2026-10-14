"""Structured Text subset: parsing, types, diagnostics with positions, and the scan cycle (WP-2.8).

References: Bolton, Programmable Logic Controllers, 6th ed (Newnes, 2015): Table 6.3 p. 168
(operator precedence) and the worked example on pp. 168 to 169; ST is not case sensitive (p. 169);
mass I/O copying pp. 106 to 107. Expected values are worked by hand.
"""
from __future__ import annotations

import pytest
from qe_plc import InputEvent, PlcError, parse, run_program
from qe_plc.scan import ScanEngine


def single_scan(source):
    result = run_program(source, period_ms=10, duration_ms=10)
    assert result["status"] == "success", result["diagnostics"]
    return result["scans"][0]


def test_bolton_precedence_example():
    # Bolton pp. 168 to 169: InputA := 6; InputB := 4; InputC := 2;
    # OutputQ := InputA/3 + InputB/(3 - InputC) = 6/3 + 4/(3 - 2) = 2 + 4 = 6.
    scan = single_scan("""PROGRAM P
VAR InputA, InputB, InputC : INT; END_VAR
VAR_OUTPUT OutputQ : INT; END_VAR
InputA := 6;
InputB := 4;
InputC := 2;
OutputQ := InputA/3 + InputB/(3 - InputC);
END_PROGRAM""")
    assert scan["outputs"]["OutputQ"] == 6
    assert scan["steps"][-1] == {"line": 7, "kind": "assign", "target": "OutputQ",
                                 "expression": "InputA/3 + InputB/(3 - InputC)", "value": 6}


@pytest.mark.parametrize("expression,expected", [
    ("TRUE OR FALSE AND FALSE", True),        # AND binds tighter than OR
    ("TRUE XOR TRUE OR TRUE", True),          # XOR binds tighter than OR
    ("NOT FALSE AND FALSE", False),           # NOT binds tighter than AND
    ("2 + 3 * 4 = 14", True),                 # * before +, + before =
    ("1 < 2 = TRUE", True),                   # < before =
    ("-2 ** 2 = -4.0", True),                 # ** before unary minus: -(2 ** 2)
    ("7 MOD 3 = 1 AND -7 MOD 3 = -1", True),  # MOD keeps the sign of the dividend
    ("-7 / 2 = -3", True),                    # integer division truncates toward zero
    ("TRUE & FALSE", False),                  # & is AND
])
def test_precedence_table(expression, expected):
    scan = single_scan(f"PROGRAM P\nVAR_OUTPUT R : BOOL; END_VAR\nR := {expression};\nEND_PROGRAM")
    assert scan["outputs"]["R"] is expected


def test_case_insensitive_comments_and_time_literals():
    scan = single_scan("""program p (* block comment *)
var_output t1 : time; X : REAL; END_VAR
// line comment
T1 := t#1m30s + TIME#250ms;
x := 0.1;
END_PROGRAM""")
    assert scan["outputs"]["t1"] == 90_250
    # REAL is binary32: 0.1 is stored as 0.100000001490116...
    assert scan["outputs"]["X"] == pytest.approx(0.10000000149011612, rel=0, abs=1e-17)


def test_if_elsif_else_trace_records_conditions():
    scan = single_scan("""PROGRAM P
VAR_OUTPUT A : INT; END_VAR
VAR N : INT := 5; END_VAR
IF N > 10 THEN A := 1;
ELSIF N > 3 THEN A := 2;
ELSE A := 3;
END_IF;
END_PROGRAM""")
    assert scan["outputs"]["A"] == 2
    assert [(s["kind"], s["value"]) for s in scan["steps"]] == [("condition", False), ("condition", True),
                                                                 ("assign", 2)]


@pytest.mark.parametrize("source,code,line,column", [
    ("PROGRAM P\nVAR X : INT; END_VAR\nFOR X := 1 TO 3 DO END_FOR;\nEND_PROGRAM", "UNSUPPORTED_SYNTAX", 3, 1),
    ("PROGRAM P\nVAR X : INT; END_VAR\nX := Y;\nEND_PROGRAM", "UNKNOWN_NAME", 3, 6),
    ("PROGRAM P\nVAR X : INT; END_VAR\nX := TRUE;\nEND_PROGRAM", "TYPE_MISMATCH", 3, 1),
    ("PROGRAM P\nVAR_INPUT I : BOOL; END_VAR\nI := TRUE;\nEND_PROGRAM", "READ_ONLY", 3, 1),
    ("PROGRAM P\nVAR X : INT; END_VAR\nX := 1\nEND_PROGRAM", "SYNTAX", 4, 1),
    ("PROGRAM P\nVAR T : TON; END_VAR\nT(IN := 1);\nEND_PROGRAM", "TYPE_MISMATCH", 3, 9),
    ("PROGRAM P\nVAR X : DINT; END_VAR\nEND_PROGRAM", "UNSUPPORTED_SYNTAX", 2, 9),
    ("PROGRAM P\nVAR X : INT; X : BOOL; END_VAR\nEND_PROGRAM", "DUPLICATE_NAME", 2, 14),
    ("PROGRAM P\nVAR X : BOOL; END_VAR\nIF X THEN X := FALSE;\nEND_PROGRAM", "SYNTAX", 4, 1),
])
def test_static_errors_name_line_and_column(source, code, line, column):
    with pytest.raises(PlcError) as error:
        parse(source)
    assert (error.value.code, error.value.line, error.value.column) == (code, line, column)
    result = run_program(source, period_ms=10, duration_ms=10)
    assert result["status"] == "failed" and result["scans"] == []
    assert result["diagnostics"][0]["element_ref"]["field"] == f"source:{line}:{column}"


@pytest.mark.parametrize("statement,code", [
    ("X := 32767 + 1;", "INT_OVERFLOW"),
    ("X := 10 / Z;", "DIVIDE_BY_ZERO"),
    ("X := 10 MOD Z;", "DIVIDE_BY_ZERO"),
    ("R := (0.0 - 8.0) ** 0.5;", "REAL_RANGE"),
])
def test_runtime_errors_stop_the_run_with_position(statement, code):
    source = f"PROGRAM P\nVAR X, Z : INT; R : REAL; END_VAR\n{statement}\nEND_PROGRAM"
    result = run_program(source, period_ms=10, duration_ms=30)
    assert result["status"] == "failed"
    assert result["diagnostics"][0]["code"] == code
    assert result["diagnostics"][0]["element_ref"]["field"].startswith("source:3:")


MOTOR_STARTER = """PROGRAM MotorStarter
VAR_INPUT Start, Stop, Overload : BOOL; END_VAR
VAR_OUTPUT Contactor : BOOL; END_VAR
(* Seal-in: Start latches the contactor; Stop or Overload drops it. *)
Contactor := (Start OR Contactor) AND NOT Stop AND NOT Overload;
END_PROGRAM"""


def test_motor_starter_handwritten_trace():
    # Scan:      0  1  2  3  4  5  6  7  8  9
    # Start:     0  1  0  0  0  0  1  0  1  0
    # Stop:      0  0  0  0  0  0  0  0  0  1
    # Overload:  0  0  0  0  1  1  1  0  0  0
    # Contactor: 0  1  1  1  0  0  0  0  1  0
    # Scan 1 latches; scans 2 and 3 hold with Start released; overload at scan 4 drops it; Start at scan 6
    # is refused while the overload persists; scan 8 restarts after it clears; Stop at scan 9 drops it.
    rows = {"Start": [0, 1, 0, 0, 0, 0, 1, 0, 1, 0], "Stop": [0] * 9 + [1],
            "Overload": [0, 0, 0, 0, 1, 1, 1, 0, 0, 0]}
    events = [InputEvent(i * 100, name, bool(v)) for name, values in rows.items() for i, v in enumerate(values)]
    result = run_program(MOTOR_STARTER, period_ms=100, duration_ms=1000, events=events)
    assert [s["outputs"]["Contactor"] for s in result["scans"]] == [bool(v) for v in
                                                                    [0, 1, 1, 1, 0, 0, 0, 0, 1, 0]]


def test_input_events_take_effect_at_the_next_scan_boundary():
    # An event at 150 ms with a 100 ms scan is first seen by the scan starting at 200 ms (mass I/O copying).
    result = run_program(MOTOR_STARTER, period_ms=100, duration_ms=400, events=[InputEvent(150, "Start", True)])
    assert [s["inputs"]["Start"] for s in result["scans"]] == [False, False, True, True]
    assert [s["time_ms"] for s in result["scans"]] == [0, 100, 200, 300]


def test_runs_are_deterministic_and_bounded():
    events = [InputEvent(100, "Start", True)]
    first = run_program(MOTOR_STARTER, period_ms=100, duration_ms=500, events=events)
    second = run_program(MOTOR_STARTER, period_ms=100, duration_ms=500, events=events)
    assert first == second
    assert run_program(MOTOR_STARTER, period_ms=1, duration_ms=10**9)["diagnostics"][0]["code"] == "RUN_LIMIT"
    assert run_program(MOTOR_STARTER, period_ms=0, duration_ms=10)["diagnostics"][0]["code"] == "SCAN_PERIOD"
    bad = run_program(MOTOR_STARTER, period_ms=10, duration_ms=10, events=[InputEvent(0, "Start", 1)])
    assert bad["diagnostics"][0]["code"] == "INPUT_EVENT"


def test_no_python_evaluation_of_program_text():
    # Program text is only tokenised and interpreted; Python syntax is rejected, never executed.
    with pytest.raises(PlcError):
        parse("PROGRAM P\nVAR X : INT; END_VAR\nX := __import__('os');\nEND_PROGRAM")


def test_engine_rejects_invalid_period():
    with pytest.raises(ValueError):
        ScanEngine(MOTOR_STARTER, 2.5)
