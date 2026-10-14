# PLC contracts and scan images

This note explains what WP-2.2 (CC-6) froze and why: how a PLC program, its I/O and a
simulated run are written down as data, so that the engine, the API, the reports and the
web view all agree on one meaning.

## 1. Why a contract for a PLC study

A short-circuit study is one calculation. A PLC study is a run: the same program executes
again and again, and what it does at one scan depends on what happened before. To check
a run you need three things fixed in advance:

1. **What the controller is**: its variables, function blocks, task period and program.
2. **What happens to it**: the input events and the plant it controls.
3. **What a correct answer looks like**: a trace of every scan that someone can check by
   hand.

CC-6 fixes all three. The engine (WP-2.9) has to produce results that pass these checks,
so a wrong engine fails loudly instead of producing plausible numbers.

## 2. Declarations as data, statements as text

In the model, variables and function-block instances are JSON, and `program.body` holds
only the statements. Two benefits:

- The core can check names, types, initial values and I/O wiring without parsing
  Structured Text. `qe_core` must not import `qe_plc`, because domains depend on the
  core and never the other way round.
- The web view can show I/O as a table and the logic as an editor.

## 3. The scan and its two images

A PLC does not read an input the moment the program mentions it. Bolton (6th ed, pp. 106
to 107) describes mass I/O copying: at the start of each scan every input is copied into
the input image, the program runs against that frozen copy, and the outputs are written
from the output image at the end.

```
time   0 ms        100 ms        200 ms        300 ms
       |  scan 0     |  scan 1     |  scan 2     |
       read inputs   read inputs   read inputs
                commit outputs commit outputs commit outputs
```

Consequences you can see in the tests:

- An input that changes at 50 ms is invisible to scan 0 and first seen by scan 1. So a
  pushbutton press shorter than one scan can be missed entirely.
- Outputs computed in scan k appear at 100(k + 1) ms. CC-6 treats the whole period as the
  scan's execution time. That is a modelling choice, and it is stated.

## 4. One-scan feedback

The motor starter is the plant. When scan 1 sets the coil, the contactor closes at the
commit (200 ms). Its auxiliary contact is wired to the `Feedback` input, so scan 2 is the
first scan that can see it:

```
scan        0    1    2    3
Start       0    1    0    0
Coil        0    1    1    1     (seal-in: Coil := (Start OR Coil) AND ...)
Feedback    0    0    1    1     (one scan behind Coil)
```

A supervision timer such as `FbTimer(IN := Coil AND NOT Feedback, PT := T#200ms)` must
therefore tolerate at least one scan of disagreement. With PT = 0 (T#0ms) the timer's Q is
TRUE in the very scan the coil turns on, so every start would raise a false fault. In a
real plant PT must also cover the contactor's own closing time, which this authored
process does not model.

## 5. The overload and the hardwired interlock

The table in the spec (section 5) puts the overload relay's contact in series with the
coil, as in a conventional starter. When the overload event occurs at 250 ms:

- Scan 3 (300 ms) still drives the coil, because the PLC has not yet read `OverloadOk`.
- The contactor opens at the commit anyway, because the relay contact breaks the coil
  circuit.
- Scan 4 would read `OverloadOk = FALSE` and drop the coil in software.

The hardwired path acts at least one scan earlier than the software path. That is why
protective interlocks are wired, not only programmed.

## 6. Counters stop, they do not wrap

While freezing CC-6 the counter rules were checked against the sources. Bolton's Figure
10.1 (p. 246) says an up-counter stops counting at PV and a down-counter stops at 0, and
Beckhoff's CTUD decrements only while CV > 0. The WP-2.8 draft let counts run past those
limits. CC-6 follows the sources, and WP-2.9 corrects the engine. Where the sources say
nothing (which of R and LD wins, or CU and CD rising together), the rule is labelled a
Quantic choice in the spec, never presented as a standard.

## 7. What a result must prove

A `plc.scan` result is accepted only if its scans line up with time (scan k at 100k ms),
its images name exactly the declared I/O, every timer has 0 <= ET <= PT and PT >= 0,
every counter output agrees with CV and PV, every input equals the latest event at or
before the scan start, process feedback lags by exactly one scan, and the time series
repeats the trace. The test file builds one such result entirely by hand, the four-scan
table in `packages/py/qe_core/tests/test_plc_contracts.py`, and then breaks each rule to
show that the validator catches it.
