# The PLC scan cycle and Structured Text

A PLC does not react to an input the instant it changes. It runs in a loop, the scan,
and everything it does happens at scan boundaries. Understanding that loop explains
most of the behaviour that surprises people new to PLCs, and it is exactly what the
`qe_plc` engine simulates.

## 1. The scan: mass I/O copying

Bolton (Programmable Logic Controllers, 6th ed, pp. 106 to 107) describes the cycle:

1. Read every input and copy it into memory (the input image).
2. Execute the whole program, top to bottom, using only the copied inputs and writing
   results into memory (the output image).
3. Copy the output image to the physical outputs.
4. Repeat.

Consequences you can see in the engine's traces:

- **An input change waits for the next scan.** With a 100 ms scan, a button pressed at
  150 ms is first seen by the scan that starts at 200 ms.
- **Inputs are frozen during a scan.** Every statement sees the same input values, even if
  the real signal changes mid-scan.
- **Outputs change once per scan.** If a statement sets an output TRUE and a later one sets
  it FALSE, the plant only ever sees FALSE.
- **A pulse shorter than the scan can be missed** entirely, because no scan samples it.

Typical real scan times are 10 to 50 ms. The engine uses simulated time: it advances a
clock by the scan period instead of waiting, so a one-hour process runs in a fraction of
a second and every run is exactly repeatable.

## 2. Structured Text in one page

Structured Text (ST) reads like Pascal. A program declares its variables, then lists
statements that run once per scan:

```
PROGRAM MotorStarter
VAR_INPUT Start, Stop, Overload : BOOL; END_VAR
VAR_OUTPUT Contactor : BOOL; END_VAR
Contactor := (Start OR Contactor) AND NOT Stop AND NOT Overload;
END_PROGRAM
```

That one line is the classic seal-in (latch) circuit. Because `Contactor` appears on both
sides, once Start has made it TRUE it stays TRUE on later scans after Start is released.
Stop or Overload breaks it. Trace it by hand, one scan at a time, and you have the same
table as the test `test_motor_starter_handwritten_trace`.

Operators bind in a fixed order (Bolton Table 6.3, p. 168). From weakest to strongest:
OR, XOR, AND, comparisons (= <>), ordering (< > <= >=), + and -, * / MOD, unary minus and
NOT, then **. So `A OR B AND C` means `A OR (B AND C)`. Bolton's own worked example:

```
OutputQ := InputA/3 + InputB/(3 - InputC);   with InputA = 6, InputB = 4, InputC = 2
         = 6/3 + 4/(3 - 2) = 2 + 4 = 6
```

INT is a 16-bit integer, -32768 to 32767. Going outside that range is an error, not a
silent wrap. Integer division drops the fraction toward zero: -7 / 2 = -3.

## 3. Timers

Bolton Figure 9.3 (p. 226) draws all three as timing diagrams. In text, with a 100 ms
scan and PT = 300 ms:

**TON, on-delay.** The output comes on PT after the input comes on, and drops as soon as
the input drops.

```
time (ms)   0   100  200  300  400  500  600
IN          0    1    1    1    1    1    0
ET (ms)     0    0  100  200  300  300    0
Q           0    0    0    0    1    1    0
```

Use: start a conveyor only after its warning horn has sounded for 3 s.

**TOF, off-delay.** The output comes on with the input and stays on for PT after the
input goes off. Use: keep a cooling fan running for a while after a motor stops.

**TP, pulse.** A rising input gives an output pulse of exactly PT, however long or short
the input is. Use: a fixed-length pulse to a solenoid from a push button.

ET is the elapsed time output. It lets a program show how long a timer has been running.

## 4. Counters

Counters count rising edges, changes from FALSE to TRUE, not scans where the input is
TRUE. A sensor held TRUE for ten scans counts once (Bolton section 10.1, p. 245).

- **CTU** counts up; Q comes on when CV reaches PV; R resets to 0.
- **CTD** counts down from PV (loaded by LD); Q comes on at 0 or below.
- **CTUD** does both, with QU at PV and QD at 0.

Use: count bottles on a conveyor and stop the line after 24 for each crate.

## 5. Where the books stop and our choices begin

The owned books give the shape of each block but not every corner case: what ET shows
after a pulse, whether a pulse can be retriggered, which wins when reset and load arrive
together. The spec (`docs/specs/structured-text-subset.md`, section 6) states each choice
explicitly. Real PLC brands differ on some of these, which is why a program moved between
brands must be retested. Our tests are handwritten tables of exactly these cases, so any
change to a choice shows up immediately.

## 6. Showing the working

Every scan returns a trace: the input image, each statement with its source line, the
expression and its value, each block call with inputs and outputs, and the output image.
That is decision D11 applied to PLC logic: a reviewer can replay any scan on paper.
