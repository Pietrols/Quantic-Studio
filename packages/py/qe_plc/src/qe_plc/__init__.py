"""Quantic Studio PLC engine (WP-2.8 core, WP-2.9 CC-6 study and motor-starter process).

Our own lexer, parser, type checker and interpreter for a bounded Structured Text
subset, the TON/TOF/TP/CTU/CTD/CTUD function blocks and a scan engine driven by
simulated time. The grammar and semantics are frozen in
docs/specs/structured-text-subset.md. No eval, exec or shell is ever used.
"""
from .errors import PlcError
from .parser import parse
from .process import MotorStarter
from .scan import InputEvent, ScanEngine, run_program
from .study import compose, run_scan_study

__all__ = ["InputEvent", "MotorStarter", "PlcError", "ScanEngine", "compose", "parse", "run_program",
           "run_scan_study"]
