# Power workbench product specification

## Design direction

Use familiar engineering interactions documented in the existing ETAP, PowerFactory and PowerWorld dossiers: project tree, single-line diagrams, equipment properties, study modes, tabular data, plots and reports. Implement original components and symbols. Do not reproduce vendor assets, proprietary screen layouts pixel-for-pixel, or opaque formats.

White and neutral grey are the default work surfaces; reserve colour for selection and engineering meaning. Keep the current React/TypeScript and canvas foundation unless a measured limitation warrants replacement. Desktop engineering is the first target. Minimum viewport and density targets below are proposed QA targets, not existing performance claims.

## Workspace regions

| Region | Content | Behavior |
| --- | --- | --- |
| Top command area | Project, undo/redo, save, study mode, run/cancel | Compact, keyboard accessible, commands disabled with a reason |
| Left navigator | Project, networks, diagrams, scenarios, study cases, libraries, results | Search, collapse, context actions; selected object shared across views |
| Centre document tabs | Single-line, equipment table, plots, report | Multiple views of the same model; diagram deletion does not delete equipment |
| Right inspector | Structured property groups, units, type/instance source, validation | Explicit Apply/Cancel; optional advanced JSON; hidden fields preserved |
| Bottom dock | Diagnostics, result table, execution log | Resizable and collapsible; selecting a diagnostic focuses object and field |
| Status bar | Active scenario/revision, run status, stale state | Never a green success indicator for invalid, cancelled or unconverged studies |

Avoid a permanent large marketing rail. Other suites remain discoverable but do not occupy the primary power workspace. Familiar terminology is allowed; Quantic navigation and visual identity remain original.

## Component boundaries

Split App orchestration into project/session controller, selection store, engineering command history, study controller and view components. Keep API effects and stale-response guards outside presentation components. An engineering command changes a model revision; layout commands change display state. Use stable physical IDs across tree/canvas/table/inspector/report.

Implement forms from existing schemas with a separate presentation annotation layer for labels, units, grouping and ordering. UI annotations cannot change engineering defaults. Fields show missing required input, supplied value, type-derived value and explicit instance override distinctly. JSON remains an advanced editor with the same validation and transaction semantics.

Tables use stable row IDs after sorting/filtering. Multi-cell paste validates the entire transaction or presents a clear partial-acceptance policy before applying; default proposed policy is atomic rejection. Results are read-only. CSV export preserves units, element IDs, scenario and run revision, and escapes spreadsheet formula prefixes in user-controlled text.

## Required interactions and tests

| ID | User journey | Acceptance evidence |
| --- | --- | --- |
| UI-01 | Add/edit bus, branch, transformer, source and load through forms | No JSON required for supported fields; keyboard access; correct units; missing data diagnosed |
| UI-02 | Connect/disconnect and move symbols | Model topology changes only for electrical commands; movement leaves electrical input hash unchanged |
| UI-03 | Edit in sorted equipment table, undo/redo | Intended IDs change; undo restores model and stale-result state coherently |
| UI-04 | Switch project/model with unapplied changes | Save/discard/cancel choices; no late response from prior project overwrites current state |
| UI-05 | Create and compare operating cases | Base model preserved; resolved input provenance and conflict rules visible |
| UI-06 | Run a supported study | Running, cancelled, failed, converged and limit-exceeded states differ; no unsupported fallback |
| UI-07 | Edit while viewing prior results | Results visibly stale or cleared; exporting stale output requires explicit historical-run selection |
| UI-08 | Select overload/diagnostic | Focuses matching element; table, canvas and inspector agree on identity |
| UI-09 | Configure panels/theme/labels | User preferences do not change solver inputs; restore defaults recovers workspace |
| UI-10 | Save, close and reopen project elsewhere | Model and portable diagram layout retained; local preferences remain optional |
| UI-11 | API unavailable, timeout or save conflict | Clear recovery with unsaved edits preserved; no false save/run success |
| UI-12 | Compare and export runs | Solver/version, method, source edition, input hash, units, assumptions and diagnostics travel with output |

## Diagram and results

Single-line canvas needs snap/grid, pan/zoom, fit-to-selection, orthogonal routing, labels, terminal-aware connection, box selection, copy/paste with new identities, explicit electrical deletion and undo. Distinguish symbol from equipment deletion in UI language.

Results overlays should offer voltage, loading, fault current and status themes only where the selected run supplies them. Include units, legend, bounds and colour-independent warnings. Never compare magnitudes from different RMS/peak/sequence/time conventions on a shared scale without conversion. Clicking any result opens its governing equation, substituted values, assumptions and source, meeting D11.

TCC/harmonic/dynamic views arrive with their engines. Plots require axis labels/units, appropriate linear/log scales, legends, cursors, provenance and accessible data tables. Unavailable views show a capability reason, not mock production data.

## Validation and visual review

Capture actual browser screenshots on the tested commit at 1366x768 and 1920x1080, including a populated network, selected equipment, validation error, result overlay, failed solve and expanded table. Check 200% browser zoom, visible focus, keyboard navigation, modal focus return and non-colour diagnostics. These dimensions are initial test cases, not a restriction on window resizing.

Run Playwright against the real local API with original fixtures. Mocked UI tests cover component edge cases but do not establish the end-to-end journey. Keep test results and screenshots tied to the exact commit. Claude reviews task completion and visual coherence; the implementation-quality reviewer follows the journey without reading the implementer's success narrative first.

## Persisted display and user customization

Browser-local layout is an existing limitation for portable projects. A display schema and migration WP must define project diagram coordinates, symbols, labels and view metadata independently of electrical data. Malformed display files recover to a safe default without losing equipment. User theme/layout preferences can remain local. Arbitrary scripts and untrusted SVG execution are outside the first workbench scope.
