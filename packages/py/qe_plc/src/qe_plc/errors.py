"""Diagnostics with source positions. Every user error names its line and column."""
from __future__ import annotations

from qe_core import Diagnostic


class PlcError(Exception):
    """A program error at a source position; converted to a diagnostic, never a crash."""

    def __init__(self, code: str, message: str, line: int, column: int):
        self.code, self.message, self.line, self.column = code, message, line, column
        super().__init__(f"{code} at {line}:{column}: {message}")

    def diagnostic(self, program_id: str = "program") -> Diagnostic:
        return Diagnostic(self.code, f"line {self.line}, column {self.column}: {self.message}",
                          {"element_type": "program", "element_id": program_id,
                           "field": f"source:{self.line}:{self.column}"})
