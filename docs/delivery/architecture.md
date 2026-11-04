# Baseline audit and power architecture

## Repository evidence

| Area | Existing evidence | Delivery consequence |
| --- | --- | --- |
| Numerical path | `qe_power/adapters/pandapower`, `qe_power/textbook/solver.py` | Retain both as references; do not mistake them for new native engines |
| Workbench | `apps/web/src/App.tsx`, `GraphCanvas.tsx`, `style.css` | Reuse canvas and project plumbing; replace JSON-first authoring, split orchestration from view components |
| Persistence | `qe_core`, project manifest and API etags | Preserve conflict detection and multi-model files; version new state explicitly |
| Types | `contracts/`, generated TS/Python | Contract changes first with migration and consumer tests |
| Validation | CI, Web workflows and `tools/check_plan` | Existing checks remain required; ownership uses merge-base PLAN, not a branch's self-grant |
| Research | `docs/research/power/{parity-matrix,reconstruction-requirements,comparison-mapping}.md` | Capability coverage must map to requirements and tests, not counts of documents |
| UI intent | `docs/research/power/notes/ui-customisation-lessons.md` | White/grey workbench, forms plus JSON, configurable panels and tables |

Code-level audit observations, not browser-tested defects: App currently presents element/new-element JSON textareas, stores layout in localStorage, uses a dark blue suite rail, exposes a synchronous run interaction and renders basic bus tables. It already invalidates displayed results on edits and preserves separate layout, which the redesign must retain. An asynchronous run response needs an explicit run/model/revision guard before future concurrent editing is enabled. Unknown study kinds must never fall through into a short-circuit renderer.

## Language decision

Python owns model compilation, orchestration, native study logic, diagnostics, trace and report assembly. NumPy/SciPy own array and sparse numerical operations. TypeScript/React owns the workbench and typed API client. Keep Node 26, pnpm lockfile and Python/uv lockfile discipline.

The dense teaching solver's all-pairs Jacobian loops are not the production design. Separate typed array/sparse kernel interfaces from model objects and JSON. Numeric LU reuse is valid only when matrix values are unchanged; a changed Newton Jacobian requires new numeric factors. Distinguish sparsity-pattern reuse from numerical-factor reuse.

Profile complete workloads before acceleration. First improve algorithms, sparse assembly, copies and scheduling. Rust/PyO3 is a candidate for custom compiled kernels; existing suitable compiled libraries remain candidates subject to licence rules. Numba is optional with explicit dependency approval, cold-start and packaging measurements. No Go or Julia runtime is added. Future EMT and real-time PLC have separate decisions.

## Five distinct state layers

1. Project model: durable equipment, terminals and type identities, parameters with units and source attribution.
2. Operating state: versioned loading, switching and dispatch overlays with documented precedence and conflict detection.
3. Study definition: method, options, source editions, tolerances, limits and requested outputs.
4. Compiled snapshot: immutable effective inputs, physical-to-solver map, canonical hash and dependency versions.
5. Run/result: unique run ID, snapshot hash, solver/version, status, diagnostics, trace, artifacts. Layout and display preferences are independent.

A study compiler validates and resolves the first three layers before assembly. Unsupported devices/options fail explicitly or require a declared approximation accepted in the study definition. No silent omission. Keep canonical hashing deterministic and test unit/base-equivalent inputs separately from byte-identical hashing.

Result status distinguishes input failure, unsupplied island, numerical failure, cancellation, valid completion and completion with limits. Limit assessment is not synonymous with numerical convergence. Partial or failed results are diagnostic, never silently accepted for reporting.

## Integration seams requiring contract work

Existing network fields do not automatically cover switches, three-winding transformers, phase models, controller settings, device libraries and scenario overlays. Each affected implementation must first list missing fields and propose an owned CC WP. Do not store undocumented semantics in arbitrary dictionaries to evade a schema change. Generated types and migrations belong to that CC PR.

A capability registry exposes supported study/device/method/version combinations to API and UI. The frontend must display unavailable functionality with a reason rather than fabricated results. An execution service eventually isolates CPU work in cancellable worker processes, snapshots inputs once, bounds concurrency, and returns run IDs. Introduce job/status/cancel/result contracts before making the current API asynchronous. Cancellation must terminate work, not merely hide progress.

## Research-to-code gate

For every mechanism record: public requirement ID; source/version; evidence class; explicit assumptions; independent derivation; authored fixture; expected result; tolerance chosen before execution; implementation entry point; test; open gap.

Evidence classes: documented behavior, artifact observation, static inference, independent analytical test, stored-result reconstruction, executed vendor comparison. Never upgrade one into another. The recent private ETAP review warns about result-derived inputs, retrospective tolerances, mixed transformer bases, tap double counting, duplicate contribution rows and unresolved method/grounding enums. The PowerFactory review likewise does not establish vendor solver execution or opaque-container interoperability.

Consequences for Quantic: use original predictive fixtures from inputs alone; keep diagnostic reconstructions separate; test terminal orientation, tap side and impedance base explicitly; keep physical switch identity through bus reduction; derive control equations from declared device modes; report source contributions without summing duplicate nested rows. Unresolved arc-flash editions/equations and protection delays cannot become safety outputs.

## Performance evidence

B0 retains small correctness cases. Then add reviewed large-case datasets and measure cold start, repeated warm distributions, compile/assembly/solve/result/trace phases, total wall time and peak resident memory including native allocations and worker processes. Record CPU, RAM, OS, versions, thread counts, raw samples, options and case hashes. Later measure contingency throughput and time-series workloads. No network-size capacity claim until workloads and budgets are agreed and measured.

Track D11 trace volume separately: preserve enough derivation to reproduce the result without materializing every sparse matrix entry for every iteration. Detailed traces may be on-demand artifacts with bounded retention; final reports must not lose equation/source/input linkage.
