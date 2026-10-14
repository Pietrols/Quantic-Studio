"""Scan engine: mass I/O copying driven by simulated time.

Each scan (Bolton, Programmable Logic Controllers, 6th ed, section 4.3, pp. 106 to 107):
1. copy every input into the input image; 2. execute the program statements in order,
writing outputs to the output image; 3. transfer the output image to the outputs;
4. repeat. Simulated time advances by the scan period between scans, so results do
not depend on the host computer's speed. Every scan returns a trace of its working
(decision D11): the input image, each statement with its evaluated value, function
block inputs and outputs, and the committed output image.
"""
from __future__ import annotations

import math
import struct
from dataclasses import dataclass

from .blocks import BLOCK_TYPES, INT_MAX, INT_MIN
from .errors import PlcError
from .lexer import TIME_MAX, TIME_MIN
from .parser import BLOCKS, Assign, If, Literal, Member, Name, Program, Unary, parse

MAX_SCANS = 100_000


@dataclass(frozen=True)
class InputEvent:
    """Set input `name` to `value` from simulated time `time_ms` onwards. It is seen by the
    first scan whose start time is at or after time_ms."""
    time_ms: int
    name: str
    value: object


def _real(value):
    """REAL is IEEE 754 binary32: results are rounded to single precision on assignment."""
    if not math.isfinite(value):
        raise ArithmeticError("REAL result is not finite")
    return struct.unpack("f", struct.pack("f", value))[0]


def _int(value, node):
    if not INT_MIN <= value <= INT_MAX:
        raise PlcError("INT_OVERFLOW", f"Result {value} is outside INT (-32768 to 32767)", node.line, node.column)
    return value


def _time(value, node):
    if not TIME_MIN <= value <= TIME_MAX:
        raise PlcError("TIME_OVERFLOW", f"Result {value} ms is outside TIME", node.line, node.column)
    return value


class ScanEngine:
    def __init__(self, program: Program | str, period_ms: int):
        self.program = parse(program) if isinstance(program, str) else program
        if not isinstance(period_ms, int) or period_ms <= 0:
            raise ValueError("Scan period must be a positive whole number of milliseconds")
        self.period_ms = period_ms
        self.values = {}
        self.blocks = {}
        for key, decl in self.program.decls.items():
            if decl.type in BLOCKS:
                self.blocks[key] = BLOCK_TYPES[decl.type]()
            else:
                self.values[key] = _real(decl.initial) if decl.type == "REAL" else decl.initial
        self.inputs = {k: d for k, d in self.program.decls.items() if d.section == "input"}
        self.outputs = {k: d for k, d in self.program.decls.items() if d.section == "output"}
        self.output_image = {d.name: self.values[k] for k, d in self.outputs.items()}
        self.time_ms = 0
        self.scan_count = 0

    # expression evaluation
    def value(self, node):
        if isinstance(node, Literal):
            return node.value
        if isinstance(node, Name):
            return self.values[node.key]
        if isinstance(node, Member):
            return getattr(self.blocks[node.instance], node.field)
        if isinstance(node, Unary):
            operand = self.value(node.operand)
            if node.op == "NOT":
                return not operand
            if node.type == "INT":
                return _int(-operand, node)
            return _time(-operand, node) if node.type == "TIME" else -operand
        left, right = self.value(node.left), self.value(node.right)
        op = node.op
        if op == "AND":
            return left and right
        if op == "OR":
            return left or right
        if op == "XOR":
            return left != right
        if op == "=":
            return left == right
        if op == "<>":
            return left != right
        if op == "<":
            return left < right
        if op == ">":
            return left > right
        if op == "<=":
            return left <= right
        if op == ">=":
            return left >= right
        if op in ("/", "MOD") and right == 0:
            raise PlcError("DIVIDE_BY_ZERO", "Division by zero", node.line, node.column)
        if node.type == "INT":
            if op == "+":
                return _int(left + right, node)
            if op == "-":
                return _int(left - right, node)
            if op == "*":
                return _int(left * right, node)
            # Integer division truncates toward zero; MOD takes the sign of the dividend.
            quotient = abs(left) // abs(right)
            quotient = quotient if (left >= 0) == (right > 0) else -quotient
            if op == "/":
                return _int(quotient, node)
            if op == "MOD":
                return _int(left - quotient * right, node)
        if node.type == "TIME":
            return _time(left + right if op == "+" else left - right, node)
        try:
            if op == "+":
                return float(left) + float(right)
            if op == "-":
                return float(left) - float(right)
            if op == "*":
                return float(left) * float(right)
            if op == "/":
                return float(left) / float(right)
            result = float(left) ** float(right)
            if isinstance(result, complex) or not math.isfinite(result):
                raise ValueError("no real result")
            return result
        except (OverflowError, ZeroDivisionError, ValueError) as exc:
            raise PlcError("REAL_RANGE", f"{op} has no finite REAL result ({exc})", node.line, node.column) from exc

    # statements
    def run_statements(self, statements, steps):
        for statement in statements:
            if isinstance(statement, Assign):
                decl = self.program.decls[statement.target]
                value = self.value(statement.expr)
                if decl.type == "REAL":
                    try:
                        value = _real(float(value))
                    except ArithmeticError as exc:
                        raise PlcError("REAL_RANGE", str(exc), statement.line, statement.column) from exc
                self.values[statement.target] = value
                steps.append({"line": statement.line, "kind": "assign", "target": decl.name,
                              "expression": statement.text, "value": value})
            elif isinstance(statement, If):
                for condition, text, branch in statement.branches:
                    result = self.value(condition)
                    steps.append({"line": condition.line, "kind": "condition", "expression": text, "value": result})
                    if result:
                        self.run_statements(branch, steps)
                        break
                else:
                    if statement.otherwise is not None:
                        self.run_statements(statement.otherwise, steps)
            else:
                decl = self.program.decls[statement.instance]
                arguments = {name: self.value(expr) for name, expr, _, _ in statement.params}
                block = self.blocks[statement.instance]
                if decl.type in ("TON", "TOF", "TP") and arguments.get("PT", 0) < 0:
                    raise PlcError("TIMER_PRESET", f"{decl.name} has a negative preset PT", statement.line,
                                   statement.column)
                block.call(self.time_ms, **arguments)
                steps.append({"line": statement.line, "kind": "call", "instance": decl.name, "block": decl.type,
                              "inputs": arguments, "outputs": block.state()})

    def scan(self, input_values: dict) -> dict:
        """One scan at the current simulated time with the given input image."""
        image = {}
        for key, decl in self.inputs.items():
            value = input_values.get(decl.name, self.values[key])
            self.values[key] = value
            image[decl.name] = value
        steps = []
        self.run_statements(self.program.body, steps)
        self.output_image = {d.name: self.values[k] for k, d in self.outputs.items()}
        trace = {"scan": self.scan_count, "time_ms": self.time_ms, "inputs": image, "steps": steps,
                 "outputs": dict(self.output_image),
                 "blocks": {self.program.decls[k].name: b.state() for k, b in self.blocks.items()}}
        self.scan_count += 1
        self.time_ms += self.period_ms
        return trace


def run_program(source: str, *, period_ms: int, duration_ms: int, events=(), program_id="program") -> dict:
    """Run `source` from t = 0 for `duration_ms` and return the per-scan traces and diagnostics.

    A program error stops the run at that scan, as a PLC faults, and is reported with its line and
    column; scans completed before it are kept. Nothing here touches files, the network or hardware.
    """
    result = {"status": "success", "period_ms": period_ms, "scans": [], "diagnostics": [], "reached_time_ms": 0}
    try:
        engine = ScanEngine(source, period_ms)
    except PlcError as error:
        result.update(status="failed", diagnostics=[error.diagnostic(program_id).to_dict()])
        return result
    except ValueError as error:
        result.update(status="failed", diagnostics=[{"code": "SCAN_PERIOD", "message": str(error), "severity": "error",
                      "element_ref": {"element_type": "program", "element_id": program_id, "field": "period_ms"}}])
        return result
    names = {d.name.upper(): d for d in engine.inputs.values()}
    ordered = sorted(events, key=lambda e: e.time_ms)
    for event in ordered:
        decl = names.get(event.name.upper())
        ok_type = decl is not None and (isinstance(event.value, bool) if decl.type == "BOOL" else
                                        isinstance(event.value, int) and not isinstance(event.value, bool)
                                        if decl.type in ("INT", "TIME") else
                                        isinstance(event.value, (int, float)) and not isinstance(event.value, bool))
        if not ok_type:
            result.update(status="failed", diagnostics=[{"code": "INPUT_EVENT", "severity": "error",
                "message": f"Event for {event.name} at {event.time_ms} ms does not match a declared input and its type",
                "element_ref": {"element_type": "input_event", "element_id": event.name, "field": "value"}}])
            return result
    scans = -(-duration_ms // period_ms)
    if scans > MAX_SCANS:
        result.update(status="failed", diagnostics=[{"code": "RUN_LIMIT", "severity": "error",
            "message": f"{scans} scans exceed the limit of {MAX_SCANS}",
            "element_ref": {"element_type": "program", "element_id": program_id, "field": "duration_ms"}}])
        return result
    current, position = {}, 0
    for _ in range(scans):
        while position < len(ordered) and ordered[position].time_ms <= engine.time_ms:
            event = ordered[position]
            current[names[event.name.upper()].name] = event.value
            position += 1
        try:
            result["scans"].append(engine.scan(current))
        except PlcError as error:
            result.update(status="failed", diagnostics=[error.diagnostic(program_id).to_dict()])
            break
        result["reached_time_ms"] = engine.time_ms
    return result
