"""Quantic Studio PLC engine core (WP-2.8).

Our own lexer, parser, type checker and interpreter for a bounded Structured Text
subset, the TON/TOF/TP/CTU/CTD/CTUD function blocks and a scan engine driven by
simulated time. The grammar and semantics are frozen in
docs/specs/structured-text-subset.md. No eval, exec or shell is ever used.
"""
from .errors import PlcError
from .parser import parse
from .scan import InputEvent, ScanEngine, run_program

__all__ = ["InputEvent", "PlcError", "ScanEngine", "parse", "run_program"]
