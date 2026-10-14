# Time series and stepping: agreeing on what a sample means

Peter, the reusable part is time and named quantities. A PV study may advance an
hour at a time, while a PLC scan advances milliseconds. Both need to say where
time starts, what was requested, what was reached and what each signal measures.
A motor seen in several suites keeps its asset ID, but each model owns its signals.

A sample of power is not automatically energy. For interval-mean power:

`E = sum(P_i * (t_end_i - t_start_i))`.

For an original example, 20 W maintained for 0.02 s gives `20 * 0.02 = 0.4 J`.
This is dimensional accounting (W = J/s), not an engineering constant. The same
integration cannot be applied silently to instantaneous samples: a numerical
interpolation/integration assumption would be required and must be reported.
Missing power is unknown, not zero. An omitted sunny interval cannot be padded
with zero and still called a complete annual energy result.

For a fixed clock, `t_k = t_start + k * h`. An original 10 ms scan starting at
zero has boundaries 0, 0.01, 0.02 seconds. A 0.025-second stop is off that grid.
Rather than move it onto a grid with an arbitrary tolerance, CC-4 diagnoses it.
Exact decimal arithmetic checks the written times. An integer-millisecond clock
also rejects a 0.5 ms step. These are explicit subset rules, not physical limits.

FMI 3.0.2 is the free design reference for initialization, typed variables with
units and Co-Simulation advancement. Its sections 2.3, 2.4 and 4.2.2.1 explain
these interfaces. Our protocol has similar concepts but is deliberately smaller:
initialize, supply inputs, advance to the next time, inspect outputs, terminate,
or reset for a new run. We do not claim FMU/FMI compatibility. The scheduler is a
later WP; this one only freezes the messages and tests their meaning.

Every completed operation says its before/after state, current/requested/reached
time and diagnostics. A failed step retains the last successful time instead of
claiming the target. An original partial run requested through 0.02 s may stop at
0.01 s and show why. Replaying a failed or reset operation cannot be disguised as
one complete monotone run. UTC series explicitly declare an origin; local times
are normalized first so timezone and daylight-saving mistakes are visible.

Signals are not just numbers. A boolean is boolean, an integer counter is integer,
and a real measurement carries an explicit unit. W and kW have compatible
dimensions, while W and J do not. Compatibility does not perform a conversion or
prove that two quantities have the same meaning. Absolute-temperature offsets
also need the proper conversion. The later routing layer checks model and asset
bindings before exchanging values.

D11 requires results to show their working. CC-4 declares an operation trace and
calculation working with equation, source/locator, substitutions with units and
result. The domain engine must compute and verify this trace itself; the report
presents it, not a separately guessed calculation. Hashes identify model, request
and data, while versions identify the model contracts and solver implementation.
No engine or engineering default is introduced by these shared contracts.
