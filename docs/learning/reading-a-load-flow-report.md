# Reading a load-flow report

This note explains what each section of the report written by `qe study run` means, how to check it, and what to be suspicious of. The worked example is the original fourteen-bus network in `examples/fourteen_bus`.

## Running a study

```
uv run qe study run examples/fourteen_bus --study loadflow --solver textbook
```

The command loads `manifest.json`, validates the network and the request against the contracts, runs the chosen solver, checks that the result itself is contract-valid, and writes two files into `out/`:

- `results.json`: the machine-readable result. Every number in the report comes from here or from the network file.
- `report.md`: the human-readable study.

Exit codes tell a script what happened: 0 converged, 1 ran but did not converge, 2 invalid project or arguments (nothing written), 3 solver not installed.

## 1. Summary: read this first, then distrust it

The summary gives the status, total load, total series losses, the voltage range and two counts: buses outside the voltage band and sources outside their reactive limits.

A load flow can converge and still be wrong as engineering. Convergence only means the equations were satisfied to the tolerance. It says nothing about whether the operating point is achievable. That is why the summary also counts limit breaches.

Sanity checks to do in your head:

- **Losses as a percentage of load.** A healthy distribution network typically sits in the low single digits. A much higher figure means heavy loading or, as in the example below, power circulating between sources.
- **Voltage range.** If every bus is within a fraction of a percent of 1.0 pu, currents are small. Small currents and high losses together contradict each other, so look at section 4.

## 2. Assumptions

The report states the model (balanced, positive sequence), the MVA base, the convergence tolerance, the initialisation and the voltage band. If any of these is not what you intended, the rest of the report answers a different question from yours.

## 3. Bus voltages

Voltage magnitude in per unit and in kV, the angle in degrees, and a check against the band you set with `--vmin` and `--vmax` (default 0.95 to 1.05 pu).

Per unit: `V_pu = V_actual / V_nominal`. A bus at 0.97 pu on an 11 kV system is at 10.67 kV.

Angles are measured relative to the slack (grid) bus, which is fixed at 0 degrees. Real power flows from leading angle to lagging angle, so angles fall as you move away from the sources towards the loads.

## 4. Sources: what each source actually had to supply

The solver reports branch flows, not generator outputs. The report recovers each source's output from power balance at its bus (Kirchhoff's current law written in power):

```
S_source,k = sum of S entering every branch at bus k + S_load,k + S_shunt,k x |V_k|^2
```

Shunts are specified at nominal voltage and behave as constant impedance, so their power scales with the square of the voltage.

Two checks prove this section is consistent:

1. A generator's P must equal its specified `p_mw`, because a PV bus fixes P.
2. Grid P plus generator P must equal total load plus total losses.

### Why reactive limits matter

A PV bus holds its voltage setpoint by producing whatever reactive power that takes. The solvers in Phase 0 do **not** enforce `q_min_mvar` and `q_max_mvar`. The report checks them instead and raises a warning when a source would have to exceed them.

### The fourteen-bus example

The fourteen-bus run converges in two iterations and every voltage is between 0.9996 and 1.010 pu. Yet losses are 7 % of load, and the summary reports two sources outside their reactive limits. Section 4 shows why:

| Source | P (MW) | Q (Mvar) | Q limits (Mvar) |
|---|---|---|---|
| grid-01 | 1.56 | -21.7 | none |
| generator-02 | 0.60 | 19.7 | -1.0 to 1.0 |
| generator-08 | 0.30 | 3.19 | -0.5 to 0.5 |

Generator-02 is asked to hold 1.010 pu while the grid holds 1.000 pu, two kilometres away on a 33 kV line. The line impedance in per unit is tiny (about 0.0046 + j0.0070 pu on a 10 MVA base), and the reactive flow across a short line is roughly `Q ~ V dV / X`, which here is about `1.0 x 0.01 / 0.007 = 1.4 pu = 14 Mvar`. So about 20 Mvar circulates between the generator and the grid. That current produces the losses, while the load itself barely moves the voltages.

The mathematics is right; the operating point is impossible. A real 1 Mvar generator would hit its limit, stop regulating voltage and behave as a PQ source. Enforcing that switch inside the solver (PV to PQ conversion) is planned work. Until then, the report's warning is the safety net.

## 5. Branch flows

For each line and transformer: P and Q entering at each end, and the series losses. The sign convention is "into the branch": positive `P from` means power flows from the From bus into the branch. For a transformer, From is the HV side.

Check for any branch: `P loss = P from + P to`. If power enters at one end (positive) and leaves at the other (negative), the difference is the loss.

`Loading (%)` is shown only where the network gives a rating: `max_current_ka` for lines, `sn_mva` for transformers.

## 6. Losses

The total of the series losses. Shunt consumption is not a loss in this report; it is shown as part of the source balance.

## 7. Convergence

Iterations and the largest remaining power mismatch. Newton-Raphson converges quadratically: near the solution, each iteration roughly squares the error (1e-2, then 1e-4, then 1e-8). The full mismatch history is in `results.json`, under the `ITERATION_MISMATCH_HISTORY` diagnostic. If the error stalls or grows instead, suspect the data: a near-zero impedance, an islanded bus or an impossible setpoint.

## 8. Diagnostics

Messages from the solver and the loader, each with a severity. An `error` diagnostic means the result should not be used.

## 9. Provenance

Solver name and version, the SHA-256 hash of the exact network file bytes, and the run time. Re-running the same file with the same solver version must give the same numbers; the hash proves which input produced a given report.
