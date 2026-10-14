"""Standard function blocks driven by simulated time in whole milliseconds.

Shapes from Bolton, Programmable Logic Controllers, 6th ed (Newnes, 2015):
timers section 9.1, p. 225 and Figure 9.3, p. 226; counters section 10.1, p. 245.
Where the book is silent (elapsed-time reset, retriggering, simultaneous edges,
saturation) the behaviour is a declared Quantic subset choice, listed in
docs/specs/structured-text-subset.md section 6 and marked "choice" below.
Each block is evaluated once per call, at the scan's time `now` (ms).
"""
from __future__ import annotations

INT_MIN, INT_MAX = -32768, 32767


class Timer:
    kind = ""

    def __init__(self):
        self.Q = False
        self.ET = 0
        self.prev_in = False
        self.running = False
        self.start = 0

    def state(self):
        return {"Q": self.Q, "ET": self.ET}


class TON(Timer):
    """On-delay (Fig. 9.3a): with IN true, ET rises from 0 and Q becomes 1 when ET reaches PT.
    IN false: Q 0 and ET 0 (choice: immediate reset)."""
    kind = "TON"

    def call(self, now, IN=False, PT=0):
        if not IN:
            self.Q, self.ET, self.running = False, 0, False
        else:
            if not self.running:
                self.running, self.start = True, now
            self.ET = min(now - self.start, PT)
            self.Q = self.ET >= PT
        self.prev_in = IN


class TOF(Timer):
    """Off-delay (Fig. 9.3b): Q follows IN to 1; after IN falls, Q stays 1 until ET reaches PT.
    IN true again resets ET to 0 (choice). Before IN has ever been true, Q is 0."""
    kind = "TOF"

    def call(self, now, IN=False, PT=0):
        if IN:
            self.Q, self.ET, self.running = True, 0, False
        else:
            if self.prev_in:
                self.running, self.start = True, now
            if self.running:
                self.ET = min(now - self.start, PT)
                if self.ET >= PT:
                    self.Q, self.running = False, False
        self.prev_in = IN


class TP(Timer):
    """Pulse (Fig. 9.3c): a rising IN starts a pulse; Q is 1 while ET < PT, whatever IN does.
    Not retriggerable during the pulse (choice). After the pulse ET holds PT while IN stays true
    and returns to 0 when IN is false (choice)."""
    kind = "TP"

    def call(self, now, IN=False, PT=0):
        if IN and not self.prev_in and not self.running:
            self.running, self.start = True, now
        if self.running:
            self.ET = min(now - self.start, PT)
            if self.ET >= PT:
                self.running = False
        self.Q = self.running
        if not self.running and not IN:
            self.ET = 0
        self.prev_in = IN


def _bounded(value):
    """INT saturation for counters (choice): CV stays within -32768..32767."""
    return max(INT_MIN, min(INT_MAX, value))


class CTU:
    """Up counter (section 10.1): each rising CU adds 1; R sets CV to 0 and wins (choice); Q = CV >= PV."""
    kind = "CTU"

    def __init__(self):
        self.Q, self.CV, self.prev = False, 0, False

    def call(self, now, CU=False, R=False, PV=0):
        if R:
            self.CV = 0
        elif CU and not self.prev:
            self.CV = _bounded(self.CV + 1)
        self.prev = CU
        self.Q = self.CV >= PV

    def state(self):
        return {"Q": self.Q, "CV": self.CV}


class CTD:
    """Down counter (section 10.1): LD loads PV and wins (choice); each rising CD subtracts 1; Q = CV <= 0."""
    kind = "CTD"

    def __init__(self):
        self.Q, self.CV, self.prev = False, 0, False

    def call(self, now, CD=False, LD=False, PV=0):
        if LD:
            self.CV = PV
        elif CD and not self.prev:
            self.CV = _bounded(self.CV - 1)
        self.prev = CD
        self.Q = self.CV <= 0

    def state(self):
        return {"Q": self.Q, "CV": self.CV}


class CTUD:
    """Up-down counter (section 10.1). Priority (choice): R, then LD, then edges; simultaneous
    rising CU and CD leave CV unchanged. QU = CV >= PV, QD = CV <= 0."""
    kind = "CTUD"

    def __init__(self):
        self.QU, self.QD, self.CV, self.prev_u, self.prev_d = False, False, 0, False, False

    def call(self, now, CU=False, CD=False, R=False, LD=False, PV=0):
        up, down = CU and not self.prev_u, CD and not self.prev_d
        if R:
            self.CV = 0
        elif LD:
            self.CV = PV
        elif up and not down:
            self.CV = _bounded(self.CV + 1)
        elif down and not up:
            self.CV = _bounded(self.CV - 1)
        self.prev_u, self.prev_d = CU, CD
        self.QU, self.QD = self.CV >= PV, self.CV <= 0

    def state(self):
        return {"QU": self.QU, "QD": self.QD, "CV": self.CV}


BLOCK_TYPES = {cls.kind: cls for cls in (TON, TOF, TP, CTU, CTD, CTUD)}
