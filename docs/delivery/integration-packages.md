# Proposed integration work packages for product-owner review

The numerical WPs already specify algorithms. These missing seams must be approved in PLAN with exact owned paths before workers implement them. This document is the proposed scope, not a silent expansion of existing WPs.

## I1 Model capability and contract audit

Dependency: B0 begins with this audit before unsupported core device work. Inventory every native-core assumption against network schemas and generated types: transformers, shunts, switches, controls, neutral/sequence data, source bounds and phase identity. Output a field-by-field supported/missing/migration table and divide missing schemas into CCs. Existing clients keep their current version; no breaking overwrite.

Acceptance: each native-core supported device has a complete validated representation; each unsupported device is rejected by capability validation; compatibility tests preserve existing examples. This audit must resolve the current three-winding/switch contract gap before claiming those capabilities.

Proposed ownership: new audit document and capability tests. Schema mutations belong to the CCs below, not this audit.

## I2 Display and authoring CC

Version diagram display independently from engineering data. Define diagram ID, physical element reference, geometry, labels and view settings. Define migration from browser-local layout as an explicit optional import, not invisible data transfer. Preserve unknown compatible extensions and reject invalid identity references diagnostically.

Acceptance: one physical element in two diagrams; layout changes do not alter electrical inputs; round-trip and older-project migration tests; malformed display data does not destroy the model. Generated types, schema examples, qe_core IO and API consumers update together.

## I3 Run identity and capabilities CC

Define capability descriptor and run lifecycle before asynchronous execution: queued, running, completed, failed, cancelled; explicit result validity and limit status. Bind run to project/model IDs, revision/hash, study/options, solver version and source editions. Define cancellation acknowledgement separately from termination, artifact expiry and restart behavior. A result arriving after selection changes cannot attach to a different active model.

Acceptance: schema state examples; duplicate submission policy; invalid transition rejection; immutable snapshot binding; no unknown study fallback; API compatibility with existing synchronous clients until migrated.

## I4 Early authoring workbench

Depends on I1/I2. Split App responsibilities; structured forms for currently supported equipment; validated equipment tables; command history; project tree; portable display; keyboard/accessibility basics. The first iteration may use existing synchronous study API, explicitly preserving busy-state editing restrictions.

Acceptance: UI-01 through UI-04 and UI-09 through UI-11 from workbench.md; actual browser evidence and real API tests. No native-engine dependency is needed to improve editing of existing supported networks. Own only frontend files and specifically approved API/display integrations. Existing 3.40 later completes advanced study views.

## I5 Native routing and bounded execution

Depends on B1 native load flow and I3. Route explicit native solver requests; keep adapter reference route separate. Compile a snapshot once, run in a managed process, enforce resource/concurrency limits, deliver progress and cancel correctly. No unbounded background thread per HTTP request. Include cleanup and process-failure recovery. Decide restart persistence explicitly rather than implying a durable queue from an in-memory dictionary.

Acceptance: successful native study with provenance, unsupported request, worker crash, timeout, cancellation, duplicate request, concurrent isolated studies, shutdown cleanup and old-client compatibility. Measure total memory, including workers. The UI can remain synchronous until this slice is accepted.

## I6 First vertical native study

Depends on I4/I5 and B1 numerical acceptance. An original feeder is authored, saved, solved, inspected, edited, solved again, exported and reopened. Bind all UI results to immutable run identity; add calculation-trace drilldown and branch results. Test a late response while switching models and invalidating inputs. Exported reports preserve original inputs and never recompute from the currently edited model.

Acceptance: the B1 demonstration plus UI-05 to UI-08/UI-12 as supported by approved scenario contracts. If scenario CC is deferred, present only the base case and record that limitation; do not fabricate scenario persistence. Claude product acceptance is based on actual journey evidence.

## I7 Scenario/type model CC and integration

Define base equipment, type/instance overrides, operating state and study definition as separate layers. Specify overlay precedence, removals, conflicting edits, effective-value provenance and result invalidation. Shareable types cannot overwrite documented instance overrides silently. Migration is explicit and reversible through a saved prior project version.

Acceptance: two operating states share one base model; update a type with two instances, retain one override; reproduce earlier run after switching state; invalid references and overlay conflicts identify object and field. Stage this before B2 controls and B8 libraries that require it.

## I8 Local release qualification

Decide packaging through a short measured spike: supported Windows and macOS target versions, local API lifecycle, Python scientific wheels, offline dependencies, browser or desktop wrapper, install footprint/startup and updates. Preserve current browser/local API architecture until that decision. Do not add Electron, Tauri, cloud auth or billing incidentally.

Acceptance: clean-machine installation, offline study, uninstall without deleting projects, backup/restore, migration rollback and unsigned/signed distribution status recorded. Licence decision D4 and unread safety-critical source gates must be resolved for release. Produce reproducible build manifest and release notes; Peter authorizes distribution.
