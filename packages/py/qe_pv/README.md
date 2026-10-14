# qe_pv interface seed

Install with `uv sync --all-packages --locked`. This package is not a simulated
PV suite. `UnavailablePVEngine` raises `ENGINE_UNAVAILABLE`; no numerical result
is invented. pvlib 0.16.1 is pinned and licence-reviewed, but this seed does not
import it. Only code below `qe_pv/adapters/pvlib/` may import pvlib in WP-2.5.

The future PV adapter implements `qe_core.stepping.SteppingEngine`: explicit
named port definitions, output sampling, solver name/version, initialise,
set_inputs, step_to, get_outputs, terminate and reset. All times are Decimal
seconds; quantities carry value and unit; `EngineStep` confirms reached time
and carries CC-4 working entries. Failed calls raise `EngineError` with element
and field diagnostics. Interval-mean outputs describe the last completed
interval, not an endpoint value that the runner silently integrates.

CC-5 callers pass the common `request['execution']` to `run_fixed` and select
it in the full request file with `request_pointer=('execution',)`. This pointer
comes from trusted routing code. Full model/request JSON and referenced data
hash enter the provenance digest. The domain adapter additionally validates
CC-5 inputs/results, supplies its equations and independent working checks,
and owns any engine resources; the shared runner imports no domain package.

API/CLI/report/web entry points are WP-2.4. The real PV model is WP-2.5.
