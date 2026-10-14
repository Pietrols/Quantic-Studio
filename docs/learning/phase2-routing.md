# How a suite plugs into Quantic Studio

Peter, a project chooses data, not executable code. The service selects a trusted
handler from a small table keyed by model type, study type and schema version.
For example, `pv.site` plus `pv.yield` at version `0.1.0` selects the PV handler.
The older PLC placeholder remains stored but cannot run. Unknown suites cannot
turn a file name, program string or solver name into a Python import or shell command.

A study crosses three boundaries:

1. The project boundary confines paths to the selected local folder, bounds files,
   validates the manifest, model, request and weather or events, and checks bindings.
2. The execution boundary starts a trusted worker with a deadline and a concurrent
   slot. The worker receives the validated input snapshot, not instructions to read
   arbitrary files. Its input/output transport has configured byte limits.
3. The presentation boundary validates the result, checks its file hashes against
   the snapshot, and dispatches to a pure report renderer. Reports do not run engines.

The original resource policies are 2 MB per model/request, 4 MB per series, at most
500 input files, 10 MB per worker input, 64 MB per worker output and 1 MB stderr.
These are capacity policies, not engineering constants. `create_app` and `Runner`
accept explicit overrides. The existing 30 s worker deadline and two-slot default
remain. Transport uses temporary files outside the project, with output size checked
while the child runs and before its JSON is read. A producer can overshoot between
checks; oversized output is never accepted or loaded into an unbounded pipe buffer.
Timeout, invalid JSON, oversized output and process failure all release the slot.

## Saving is a separate operation

Running never writes a model. Saving requires the hash returned when the selected
model was opened, validates the proposed model against its associated studies and
asset references, and replaces only that model file through a temporary file and
atomic rename. The contract version cannot change during a property edit.

The concurrency rule is `etag_opened = SHA256(current_model_bytes)`. If the equality
fails, the API returns an edit conflict instead of overwriting newer input. JSON
serialization is finite and bounded before the replacement. Other models, weather,
program requests, the asset registry and opaque future files remain byte for byte.
Atomic replacement prevents half-written files; it does not make two unrelated
external editors participate in one transaction. The service lock serializes its
own saves, and its local project directory remains a trusted filesystem boundary.

## Provenance identifies the input snapshot

For each selected model, request and data file, the boundary records
`h_file = SHA256(raw UTF-8 bytes)`, with its project-relative path and role. Weather
and events must match the content hash pinned by the request. Freshly read model
and request objects must still equal those used to select the study. The result's
file records must equal the actual snapshot records before an API report is accepted.
An engine owns the aggregate input hash and the calculation trace required by CC-4.
The report must state the governing equations, their book/page references, substituted
values and results under decision D11. Routing cannot invent those calculations.

The two input boundaries in CLI and API are deliberately kept within their owned
packages, with a parity test. Neither imports the other. Moving that common file
boundary into core would require a future core-owned WP.

## Different workspaces, one canvas

PV has an array/inverter graph with DC and AC ports. PLC has an ST text editor and
a controller/device graph with typed I/O ports. Internal PLC variables are not device
ports. A graph does not claim to be a ladder editor or live hardware controller.
Dragging a node changes browser-local layout, never engineering inputs.

The existing shell selects a workspace by model type and version. Suite components
receive project/model identity, study selection and report format. They own their
model edits and study response views. This keeps the later PV and PLC work in
separate paths. The seeded handlers and reports return `ENGINE_UNAVAILABLE`; no
calculation, report or result is fabricated while the engines are not connected.

The first PV/PLC implementations replace their suite-local `execute(payload)`
functions in CLI and API. The payload contains `model`, `request`, `series`,
`input_files`, `study_type`, `model_type`, `model_id`, `project_name` and
`report_format`. API handlers may call `qe_api.responses.study_response(payload,
result)` for semantic result checks, snapshot checks and Markdown/PDF transport.
The CLI handler may call `qe_cli.responses.study_response(payload, result)`
for the same semantic, snapshot and report checks. It returns the same response envelope; its existing suite exporter
writes only `out/results.json`, `out/report.md` and the optional PDF. It returns 0
for CC-4 `complete`, 1 for partial/failed calculations and 2 for invalid input or
unavailable execution. Suite report modules expose `render_report(project_name,
model, request, result)` and compute/check their working independently of the engine.

## The independent references here

WP-2.4 contains no new physical solver. Its reference is the CC-5/CC-6 contract
fixtures: typed bindings, asset identities, unavailable handlers, file hash identity,
byte preservation and worker state transitions. The committed small synthetic
weather and authored event fixtures are dedicated to CC0-1.0 and recorded in the
source register. No test fetches weather or controls equipment. Existing real power
API, PDF and browser flows remain preservation checks. All generated TypeScript
consumers compile in CI, and an authored PV payload round-trips through Node 26.
