"""Tokens of the Structured Text subset. ST is not case sensitive (Bolton 6th ed, p. 169)."""
from __future__ import annotations

import re
from dataclasses import dataclass

from .errors import PlcError

KEYWORDS = {
    "PROGRAM", "END_PROGRAM", "VAR", "VAR_INPUT", "VAR_OUTPUT", "END_VAR", "IF", "THEN", "ELSIF",
    "ELSE", "END_IF", "AND", "OR", "XOR", "NOT", "MOD", "TRUE", "FALSE",
    "BOOL", "INT", "REAL", "TIME", "TON", "TOF", "TP", "CTU", "CTD", "CTUD",
}
# Constructs outside the subset: recognised so the diagnostic is precise, never executed.
UNSUPPORTED = {"FOR", "WHILE", "REPEAT", "CASE", "FUNCTION", "FUNCTION_BLOCK", "RETURN", "EXIT",
               "POINTER", "REF_TO", "ARRAY", "STRUCT", "VAR_IN_OUT", "VAR_GLOBAL", "VAR_TEMP",
               "AT", "CONSTANT", "RETAIN", "DINT", "LREAL", "WORD", "DWORD", "STRING", "JMP"}


# Declared TIME range in milliseconds (docs/specs/structured-text-subset.md section 4).
TIME_MIN, TIME_MAX = -(2**31), 2**31 - 1


@dataclass(frozen=True)
class Token:
    kind: str      # NAME, KEYWORD, INT, REAL, TIME, OP, EOF
    text: str
    value: object
    line: int
    column: int


_TIME = re.compile(r"(?:T|TIME)#(-?)((?:\d+(?:\.\d+)?(?:ms|d|h|m|s)_?)+)", re.IGNORECASE)
_TIME_PART = re.compile(r"(\d+(?:\.\d+)?)(ms|d|h|m|s)", re.IGNORECASE)
_UNIT_MS = {"d": 86_400_000, "h": 3_600_000, "m": 60_000, "s": 1000, "ms": 1}
_OPS = [":=", "<=", ">=", "<>", "**", "=", "<", ">", "+", "-", "*", "/", "(", ")", ";", ":", ",", ".", "&"]


def time_literal_ms(body: str, sign: str, line: int, column: int) -> int:
    total = 0.0
    for amount, unit in _TIME_PART.findall(body):
        total += float(amount) * _UNIT_MS[unit.lower()]
    if total != int(total):
        raise PlcError("TIME_PRECISION", "TIME literals resolve to whole milliseconds", line, column)
    value = -int(total) if sign else int(total)
    if not TIME_MIN <= value <= TIME_MAX:
        raise PlcError("TIME_OVERFLOW", f"{value} ms is outside TIME ({TIME_MIN} to {TIME_MAX} ms)", line, column)
    return value


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    i, line, column = 0, 1, 1

    def advance(text):
        nonlocal i, line, column
        for ch in text:
            if ch == "\n":
                line, column = line + 1, 1
            else:
                column += 1
        i += len(text)

    while i < len(source):
        ch = source[i]
        if ch in " \t\r\n":
            advance(ch)
            continue
        if source.startswith("(*", i):
            end = source.find("*)", i + 2)
            if end < 0:
                raise PlcError("SYNTAX", "Comment opened with (* is never closed", line, column)
            advance(source[i:end + 2])
            continue
        if source.startswith("//", i):
            end = source.find("\n", i)
            advance(source[i:] if end < 0 else source[i:end])
            continue
        start_line, start_column = line, column
        match = _TIME.match(source, i)
        if match:
            value = time_literal_ms(match[2], match[1], line, column)
            tokens.append(Token("TIME", match[0], value, start_line, start_column))
            advance(match[0])
            continue
        match = re.compile(r"\d+\.\d+(?:[eE][+-]?\d+)?|\d+").match(source, i)
        if match:
            text = match[0]
            kind = "REAL" if "." in text else "INT"
            tokens.append(Token(kind, text, float(text) if kind == "REAL" else int(text), start_line, start_column))
            advance(text)
            continue
        match = re.compile(r"[A-Za-z_][A-Za-z0-9_]*").match(source, i)
        if match:
            text = match[0]
            upper = text.upper()
            if upper in UNSUPPORTED:
                raise PlcError("UNSUPPORTED_SYNTAX", f"{upper} is outside the supported subset", line, column)
            kind = "KEYWORD" if upper in KEYWORDS else "NAME"
            tokens.append(Token(kind, upper if kind == "KEYWORD" else text, upper, start_line, start_column))
            advance(text)
            continue
        op = next((o for o in _OPS if source.startswith(o, i)), None)
        if op is None:
            raise PlcError("SYNTAX", f"Unexpected character {ch!r}", line, column)
        tokens.append(Token("OP", op, op, start_line, start_column))
        advance(op)
    tokens.append(Token("EOF", "", None, line, column))
    return tokens
