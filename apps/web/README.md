# Quantic Studio power workspace

```sh
uv sync --all-packages --locked
uv run qe-api --project-root examples
# In another terminal:
pnpm install --frozen-lockfile
pnpm --filter qe-web dev
```

Open http://127.0.0.1:5173. Vite proxies API requests to the loopback service.
This is a runnable local workbench; this WP does not publish a hosted site.

Choose a project, then a model. Power networks are editable; future-domain data
are visible but not executable. Select a bus, equipment symbol or branch to edit
its JSON properties. Apply validates a copy; Save sends only the selected model
with its etag. Optional electrical fields and foreign models/assets are preserved.
Use Model JSON for coordinated topology changes such as renaming referenced bus
IDs. Add element provides all seven supported collections with explicit null
placeholders for required equipment numbers; supply your own data, not guessed
manufacturer/standard values. Connect bus ports to equipment to reassign it, or
connect buses to supply an explicit line/transformer definition.

Select nodes and controls with the keyboard; property fields, project/model/study
selectors and save/run buttons are native accessible controls. Unsaved engineering
changes block study runs and ask before switching models/projects. A failed save
retains edits. A new edit or study selection clears stale results.

Dragging stores positions in localStorage per project/model. It does not alter
network data, dirty a model or change solver provenance. Layout is browser-local,
not a shared contract or portable project attachment. A later persisted layout
contract needs its own approved Contract Change. Reset layout restores the initial
arrangement. Generated graph IDs bind visual elements to model-local elements;
asset links are displayed for bound representations.

Run a study by explicit ID. Results show per-bus voltage/current, availability and
motor dip compliance; reports retain limits, assumptions and provenance. HTTP
success and numerical convergence do not establish feasibility. Download Markdown
or result JSON. PDF appears automatically when WP-1.7 advertises that API format.

## Packages and checks

- @quantic/contracts generates types/runtime network schemas from frozen repo contracts.
- @quantic/canvas defines domain-neutral nodes, typed ports and positions.
- @quantic/power maps network payloads and enforces power editing rules.
- qe-web composes the workspace and local API. Its GraphCanvas receives symbols
  as presentation, without reading MW, kV or electrical fields.

```sh
pnpm generate:check
pnpm --filter qe-web test
pnpm --filter qe-web build
pnpm --filter qe-web exec playwright install chromium
pnpm --filter qe-web e2e
```

Web CI runs these checks and real API/browser smoke tests. Browser tests copy
projects under an ignored .e2e-projects folder and do not edit authored examples.
Ladder logic is not implemented by this free graph canvas and remains a later
separate grid component. Foreign engines and co-simulation are outside this WP.

## Node version

Use Node 26, the version in `.nvmrc` that CI also uses (decision D13), for example with `nvm use`. `tests/setup.ts` binds jsdom's Web Storage over the global `localStorage` that Node 25 and later define, so the unit tests behave like a browser.
