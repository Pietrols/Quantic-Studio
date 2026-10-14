# One clock, isolated engines

Peter, the scheduler owns the clock and the engine owns its equations. Keeping
those responsibilities separate lets PV, a PLC trend and later scope traces use
the same time format without forcing their physics into one solver.

The shape follows FMI 3.0.2 sections 2.3 and 4.2.1: initialise, exchange named
values, advance to a requested boundary, read outputs, terminate and reset.
This is Quantic's limited Python interface, not the FMI C ABI, an FMU importer
or a conformance claim. It runs exactly one trusted engine and one model.
Coupled systems, rollback, event iteration and arbitrary import strings are out.

## The clock and state

The authored fixed-grid rule is `t_k = t_start + k*h`, for integer k. Every
successful engine step confirms `reached = requested`; an early return is a
failure. Decimal arithmetic uses the serialized inputs, avoiding accumulated
binary rounding. We compute each boundary from its index, not repeated floating
addition. UTC labels must also fit microsecond datetime precision; unsupported
precision is diagnosed before the engine starts.

For an original 10 ms device with three steps, boundaries are 0, 0.01, 0.02 and
0.03 s. Its rule is "increment the count when the input is true on a step".
Inputs true, false, true produce count snapshots 0, 1, 1, 2. This is our small
handwritten scheduler oracle, not a PLC timer standard or an electrical model.

A session starts instantiated. Initialisation makes it initialized; steps make
it running; termination makes it terminated. Failed operations enter error and
retain the last successfully reached time. Reset calls the engine reset and
returns to instantiated at zero, clearing cached values and working. A new study
gets a fresh session, so its result never includes a reset from a previous run.
The caller owns engine resources; an error never pretends termination succeeded.

## Values, units and sampling

Each port has an ID, model ID, direction, scalar type and explicit unit. A
Quantity carries a value and unit at every exchange. Engine and request ports
must agree on identities/types/directions and compatible dimensions. The runner
converts explicitly at that boundary; trace cells use request units. Integer
ports cannot acquire fractional values during conversion, and true is not 1.
An original unit test is 1 kW = 1000 W. Offset conversion is also essential:
25 degrees Celsius = 298.15 kelvin. Multiplication alone cannot convert absolute
temperatures. Unit definitions come from the existing Pint registry.

Instantaneous output is a snapshot at a boundary. Interval-mean output describes
the completed half-open interval `[t_k,t_(k+1))`. The engine declares which it
publishes; the runner cannot reinterpret an endpoint as a mean. Instant output
includes an initial snapshot; interval output has one row per completed step.
An input image is held through each step. The right-boundary instant snapshot
contains the image used for that step, before the next exchange.

For the original interval device `y = 2*x`, inputs 1, 2, 3 W produce means
2, 4, 6 W. If power is later integrated, `E = sum(P_mean * duration)`.
Multiplying an instant by a whole interval would introduce an assumption the
engine did not make. The numerical suites supply their own sourced equations
and independent D11 working checks; the scheduler only preserves their trace.

Input files may contain gaps or unavailable cells, but execution stops at the
first required unavailable image instead of inventing zero or interpolation.
The valid prefix and actual reached time remain visible. A successfully reached
boundary whose output read fails is recorded as reached, with no fabricated row.
Sparse domain events must be turned into explicitly defined images by that
domain's approved semantics; this generic runner never invents an event rule.

## Bounds and provenance

RunLimits is an explicit resource policy, not engineering constants. Defaults:
100000 steps, 256 ports, 4000000 bytes per input file, 1000000 cells and 100000
working entries. Callers may tighten them. Count/file/cell bounds are checked
before expensive validation or engine calls. They cannot stop a Python engine
that hangs inside one call; killable service-worker deadlines remain required.

The runner resolves model, request and data paths within the project, including
symlinks. Files are distinct, bounded UTF-8 JSON objects. Every original file has
its own byte SHA-256. The overall input digest uses canonical UTF-8 JSON
(sorted keys, compact separators, no nonfinite values) of the full model, the
full request and the referenced data path/hash. Wrapper fields matter: selecting
`execution` for CC-5 does not discard the rest of that request from provenance.
Solver name/version and explicit model version are captured before execution.

## A known CC-4 limit

CC-4 currently rejects a result reached before its request's nonzero start,
even when initialization failed. We must not say that an uninitialized engine
reached 1 s when it is still at zero. In that case RunOutcome carries the real
requested/reached time, failed operation trace and `RESULT_UNREPRESENTABLE`,
with no serialized study result. Claude confirmed this handling in the agent
channel and scheduled a Contract Change after WP-2.7. The Phase 2 PLC slice
starts at zero; PV uses elapsed zero on its own UTC origin. Ordinary zero-start
initialization failures have a contract-valid failed result with no samples.

## The PV seed

The installable qe_pv package is only an interface seed here. Its engine raises
ENGINE_UNAVAILABLE. Pinning and reviewing pvlib 0.16.1 prepares WP-2.5; installing
a dependency does not turn the seed into a simulated result or a completed suite.
Only qe_pv/adapters/pvlib may import pvlib. Domains depend internally only on
core and never import one another. Import and dependency-metadata guard tests
exercise both valid and forbidden examples.

The exact pvlib required dependency/license record is
`docs/sources/entries/pvlib-0.16.1-runtime.yaml`. No optional extras or GPL PLC
programs are imported. Existing NumPy/SciPy native-runtime notices still matter
when distributing compiled wheels; the record distinguishes those from the
BSD Python packages. No vendor login, paid standard, book content or weather
network request is needed by the runtime tests.
