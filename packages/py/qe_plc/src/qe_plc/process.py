"""Authored discrete motor-starter process (CC-6, docs/specs/plc-program-and-scan.md section 5).

This is a scenario device for testing control logic, not a model of real equipment: no
electrical dynamics, contactor timing or safety rating. It advances once per scan, after
the output image is committed, so the program sees its effect one scan later.
"""
from __future__ import annotations


class MotorStarter:
    def __init__(self, contactor_closed: bool, overload_tripped: bool):
        self.contactor_closed = contactor_closed
        self.overload_tripped = overload_tripped

    def state(self) -> dict:
        return {"contactor_closed": self.contactor_closed, "overload_tripped": self.overload_tripped}

    def advance(self, coil: bool, overload_event: bool, overload_reset: bool) -> dict:
        """One transition. Returns the process working for the scan trace (decision D11)."""
        before = self.state()
        # Step 1: the overload condition wins over a reset in the same scan.
        tripped = overload_event or (self.overload_tripped and not overload_reset)
        # Step 2: the relay's contact is in series with the contactor coil (hardwired interlock).
        closed = coil and not tripped
        self.contactor_closed, self.overload_tripped = closed, tripped
        return {
            "before": before,
            "scenario": {"overload_event": overload_event, "overload_reset": overload_reset},
            "coil": coil,
            # Step 3: no acceleration model, so the motor runs exactly while the contactor is closed.
            "after": {"contactor_closed": closed, "overload_tripped": tripped, "motor_running": closed},
        }
