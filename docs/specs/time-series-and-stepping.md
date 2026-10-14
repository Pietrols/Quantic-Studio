# CC-4: time series and a limited stepping protocol, version 0.1.0

All five contracts are new namespaces. No existing schema is changed or needs an
archive in this CC. Future changes archive these original bytes before replacing
a version. Core semantic entry points live in `qe_core.time_series`; consumers
must call them in addition to schema validation. The existing `qe_core.validate`
checks schema shape and finite numbers; it intentionally does not dispatch these
new cross-row semantics from an unowned file.

## Signals and samples

A signal has a unique signal_id, model_id, optional asset_id, name, data_type,
explicit unit and input/output causality. Real, integer and boolean are distinct;
boolean is never the number 0 or 1. Boolean units are `1`; count signals also use
`1`. Unit compatibility is dimensional, not a promise that two ports represent
the same physical quantity. A caller must explicitly convert compatible units
and check port meanings. Temperature offset conversions cannot be replaced by a
scale factor. Pint checks unit labels without consulting a domain engine.

A series has a series_id, one time_axis, sampling, signal declarations, samples
and diagnostics. Every row contains exactly one cell per declared signal. Cells
have value/status/diagnostics. A valid cell has its declared scalar type. Missing
or invalid has null and a diagnostic; neither is silently changed to zero. A valid
cell cannot carry an error diagnostic. Finite numbers are required throughout.

Elapsed time is a nonnegative number of seconds. UTC is an ISO date-time ending
in Z with an explicit UTC origin, measured in seconds relative to that origin.
UTC samples before the origin are invalid; local wall times and mixed axes are
rejected. Consumers normalize timezone data before storing it. Instantaneous
samples have a time and no end_time. Interval means cover [time, end_time), with
strictly positive duration and no overlap. Starts must increase strictly. Gaps
may be stored for input data, but an incomplete output cannot claim complete
coverage. Sample means and instants must never share an integration rule implicitly.

## Requests, operations and result coverage

A time-stepped request identifies request/study/model, its time axis, start/stop,
step size, clock, signal definitions and a confined local input-series path.
Stop > start and (stop - start) / step must be an integer. `fixed_ms` additionally
requires every time to be an exact integer number of milliseconds; `fixed_s`
permits an exact decimal fixed grid. Decimal comparisons use the serialized
values; no numerical tolerance is invented to round a time onto a grid.
Unrepresentable arithmetic or malformed context is a diagnostic. File resolution,
symlink confinement and worker/resource bounds belong to later project/runtime WPs.

A time-step object is a completed operation record, not an executable call string.
It names the session, operation, before/after state, current/requested/reached
elapsed times, success/failed, named input/output cells and diagnostics.

| Operation | Successful state transition | Time and signal rule |
| --- | --- | --- |
| initialise | instantiated to initialized | reached = requested initial time; input/output snapshot allowed |
| set_inputs | initialized/running to same | no time advance; input cells only |
| step_to | initialized/running to running | target > current, reached = target; input/output exchange allowed |
| get_outputs | initialized/running to same | no time advance; output snapshot only |
| terminate | initialized/running to terminated | no time advance or signal exchange |
| reset | any declared state to instantiated | uninitialized elapsed time zero; new study run follows |

Failed attempts enter error, retain current as last successful time, and require
an error diagnostic. They can record an attempted illegal state operation without
pretending it succeeded. Sequence validation checks session, prior reached time
and prior after-state. Unsupported rollback, intermediate/event iteration and
algebraic coupling have no operation or schema field and are rejected. Runtime
execution and actual engine calls are WP-2.3, not this Contract Change.

A result has complete/partial/failed, requested end and reached time, series,
operation trace, calculation working, model_versions, input_files, provenance
and diagnostics. Its trace begins with initialization; a reset belongs to a new
result. Reached time equals the trace's last successful time. Failed requires an
error; incomplete requires diagnostics. Complete cannot contain errors, unavailable
output or omit its endpoint. Supplying the request to the result validator checks
exact model/request/study/time-axis binding, grid coverage, sample count and each
step increment. Instant output includes every boundary from start through reached;
interval-mean output includes every reached interval. Partial output stops on a
reached grid boundary; it is not padded. Failure before initialization may have
no samples, but still records the failed initialization and diagnostics.

`working` contains authored equation/source/locator, named substituted quantities
with units and the resulting quantity. Empty working is valid for a failed run
with no calculations; numerical suite results must populate it under their own
CCs and D11. The operation trace itself is always present. A schema cannot prove
an equation was evaluated correctly; each domain adapter must compute/check its
own working, as required by D11.

Input_files hashes cover each original model/request/data file, with unique,
confined relative paths. Provenance input_hash_sha256 covers the canonical full
model, complete request and referenced data hashes; model_versions and solver
version identify implementations/contracts. Canonicalization and hashing execution
are provided by the later runtime; this CC declares what must be covered.

## Source and compatibility

FMI 3.0.2, sections 2.3 (common API/state concepts), 2.4 (variables and units) and
4.2.2.1 (Co-Simulation step), informs the lifecycle shape. Exact fixed-grid/no-
rollback/single-run rules above are our declared subset. This is not the FMI C ABI,
an FMU loader or a standards certification. The specification is CC BY-SA 4.0;
its companion code is BSD-2. Only references and original designs are committed.

Python tests contain original dimensional examples and handwritten transition/
coverage tables, independent of any solver. TS types are generated into separate
files under contracts/src/time. Existing public power types and all pre-CC-4
schema bytes are checked against the approved base commit. Runtime schema constants
retain their URN references; a consumer registers referenced schemas before use.
