# The motor-starter process: one-scan feedback and interlocks

WP-2.9 connects the Structured Text engine to a simulated plant: a motor starter with a
contactor, an auxiliary feedback contact and an overload relay. This note explains how
the simulation is ordered, why the feedback lags by one scan, and what the 12-scan test
scenario teaches about interlocks.

## 1. Two machines taking turns

A PLC and its plant both change state, and the order of those changes decides the
answer. CC-6 fixes the order for every scan k (period h = 100 ms):

```
t_k            scan k executes                 t_(k+1)
 | read inputs  ->  statements  ->  write outputs |  plant moves
```

1. **Read**: external inputs (buttons) come from the latest event at or before t_k.
   Plant inputs (`Feedback`, `OverloadOk`) come from the plant state left after scan
   k - 1.
2. **Execute**: the statements run top to bottom. Timers use t_k.
3. **Commit**: the output image is written at t_(k+1).
4. **Plant**: the motor starter takes the committed coil and changes state.

Nothing in the plant can reach the program inside the same scan. That is the
mass-I/O-copying model Bolton describes (6th ed, pp. 106 to 107), applied to a plant.

## 2. The transition table

With overload event E, reset R, coil K, contactor closed C and relay tripped O:

```
O' = E OR (O AND NOT R)        overload wins over reset
C' = K AND NOT O'              relay contact is in series with the coil
running' = C'                  no motor dynamics
next scan: Feedback = C', OverloadOk = NOT O'
```

This table is authored. It is a tool for testing control logic, not a motor model: a
real contactor takes a finite time to close, and a real overload relay trips on
a time-current curve. Neither is modelled, and the reports say so.

## 3. Reading the test scenario

The program is a seal-in starter:

```
Run := (Start OR Run) AND NOT Stop AND Permissive AND OverloadOk;
Coil := Run;
FbTimer(IN := Coil AND NOT Feedback, PT := T#200ms);   (* supervision *)
Fault := FbTimer.Q;
Starts(CU := Coil, R := Reset, PV := 2);               (* start counter *)
```

| scan | what happens | lesson |
|---|---|---|
| 1 | Start pressed, no permissive: refused | permissives gate the seal-in |
| 3 | Start with permissive: Coil on, contactor closes at the commit | output appears at t_(k+1) |
| 3 | Timer IN is TRUE for one scan (no feedback yet) | supervision must tolerate one scan |
| 4 | Feedback arrives; timer resets at ET = 0 | one-scan feedback |
| 6 | Overload at 550 ms, first seen at 600 ms: relay trips, contactor opens, coil still on | the hardwired contact acts before software |
| 7 | Program reads OverloadOk = FALSE, drops Run; Start refused | software interlock follows one scan later |
| 8 | Reset clears the relay | E wins over R only while E is present |
| 9 | Restart; counter reaches PV = 2 and Q turns on | CTU counts rising edges, not scans |
| 10 | Stop drops the coil | NOT Stop in the seal-in has priority |
| 11 | Reset clears the counter | R wins over counting |

A pushbutton pulse shorter than one period can fall between two scans and be missed
entirely. The event list in every result shows which scan first saw each change.

## 4. Counters corrected

CC-6 fixed the counter rules to the sources. Bolton's Figure 10.1 (p. 246) says an
up-counter stops at PV and a down-counter stops at 0, and Beckhoff's CTUD counts down
only while CV > 0. The engine now does both. The WP-2.8 trace that let CTD reach -1 was
rewritten by hand to stop at 0.

## 5. Faults keep the evidence

A runtime error (divide by zero, INT or TIME overflow, a negative timer preset) stops the
run at that scan, as a PLC faults. The scans already completed stay in the result with
status `partial`, and the diagnostic gives the line and column in the program body. A
syntax error fails before any scan, also with its body position. Nothing is silently
skipped.
