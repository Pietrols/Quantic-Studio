# Quantic Studio: Master Plan v2 (build phase)

**Owner:** Peter Kabamba, Quantic Engineering Limited
**Plan version:** 3.0 proposed (4 November 2026), pending ChatGPT agreement and Peter's approval
**Repository:** `Pietrols/Quantic-Studio`
**Previous plan:** `docs/plan/PLAN-v1.md` holds Phases 0 to 2 and the research phase (WP-0.0 to WP-2.30) with every status line and change record. It is history; this file is the live plan.

**Version history**

| Version | Date | Change |
| --- | --- | --- |
| 1.0 to 1.x | 2026-10-07 to 2026-10-30 | Phases 0 to 2 and the research phase, archived in `docs/plan/PLAN-v1.md` |
| 2.0 | 2026-10-31 | Peter ends the research phase and opens Phase 3, the power suite build. Learn-then-build method (section 2). Work split into batches A to D: A and C to Claude, B and D to ChatGPT. Groundwork WPs 3.1 to 3.3 first |
| 3.0 | 2026-11-04 | Peter's new roles: Claude product owner, ChatGPT product manager, DeepSeek workers in OpenCode. Phase 3 restructured into milestones M3.0 to M3.5 with parallel tracks; network model v1 (type/element, terminals, derived bus types); PowerFactory-style workbench as milestone M3.U; textbook worked examples and recorded demos per milestone (sections 7 to 11, decisions D19 to D25) |

This is the single source of truth for what gets built, in what order, by whom, and in what state it is. Every AI model reads it at the start of every session, as `AGENTS.md` requires.

---

## 0. How to use this document

### 0.1 Status legend

Every work package (WP) has exactly one `Status:` line. Only four forms are allowed:

| Status | Exact line format |
| --- | --- |
| Not started | `Status: [ ] Not started` |
| In progress | `Status: [~] In progress \| <model> \| branch <branch-name> \| started <YYYY-MM-DD>` |
| Done | `Status: [x] Done \| implemented by <model> \| commit <short-sha> \| <YYYY-MM-DD>` |
| Changed design | `Status: [!] Changed design \| due to <reason>, while original was <original>, as it was better for <benefit> \| <model> \| <YYYY-MM-DD>` |

Rules:

1. **Done means the implementer has passed all tests and acceptance commands with green CI.** The implementer marks its own WP Done. A different model audits each batch at its end (section 4.1).
2. **Changed design is a record, not a hiding place.** Set it before continuing and copy the same sentence into the WP's `Change record:`. The record stays after the WP is Done.
3. **In progress is optional.** Use it only when a WP pauses across sessions or is blocked.
4. CI validates every status line and checks that a WP branch changes only its owned paths.

### 0.2 Who edits what in this file

| Who | May edit |
| --- | --- |
| Worker (DeepSeek) | Only the `Status:` and `Change record:` lines of its WP |
| Manager (ChatGPT) | Status lines when merging or returning work; findings in new logs |
| Product owner (Claude) | Drafts WPs, acceptance criteria and plan revisions for Peter's approval |
| Peter | Anything. Peter alone approves new WPs, contract changes and edits to sections 0 to 6 |

### 0.3 Reading order for a busy owner

Section 1, then the status lines in sections 7 to 11.

---

## 1. Summary

**What:** one engineering suite that combines what ETAP, PowerFactory and PowerWorld do for power systems, then PVsyst for solar, PLC software for automation, and MATLAB/Simulink and Proteus for circuits and control, so users can switch with little change. CAD (AutoCAD and SolidWorks style) comes later on the SolidCraft and CADCraft forks.

**Where we are (2026-11-04):** no Phase 3 WP has started yet. Phase 0 to 2 delivered contracts, CI, a pandapower adapter (load flow, IEC 60909, motor start), a textbook Newton-Raphson solver, a PLC Structured Text engine and a first web workbench. The research phase (WP-2.10 to WP-2.30) produced the parity matrix, engine inventory, requirements and comparison cases in `docs/research/`. Peter's static survey of the reference engines is in the private reference library.

**Research since plan v2:** the private reference library now holds a 39-chapter ETAP 16 atlas (load flow reproduced to about 0.0002 percentage points on shipped solved cases after a tap-convention repair, one held-out bus still open), a first PowerFactory 15.1 study (object model, load-flow options and inner/outer loop, UI workflow, interchange formats), and studies of Proteus, PVsyst, LogixPro and MATLAB for later phases. Plan v3 uses ETAP for engine behaviour and PowerFactory for data model and workflow.

**Phase 3 goal:** Quantic's own power engines, native Python on NumPy and SciPy, covering every study family in the parity matrix, each showing its working (D11), checked against analytical cases, public benchmarks and reference-product behaviour. pandapower stays as an independent cross-check, not the product engine.

**Release:** one product, close to finished at release. No separate student edition.

---

## 2. Method: learn, then build

Decided by Peter, 2026-10-31.

1. **Learn from everything available.** Agents read the private reference library: textbooks and standards, and the ETAP static survey (`etap-survey/` in `Pietrols/QE-References`: journal, engine reports, pseudocode and the independent prototype). The goal is to understand how each engine is put together: data flow, equations, numerical method, controls, stopping rules, outputs.
2. **We do not copy.** Quantic code is written fresh in Python. No pseudocode, decompiled text or prototype code is pasted or transliterated into this repository.
3. **We do not reinvent the wheel.** Established principles, methods and constants are used as they are. Where the survey shows a tuned value (for example a Gauss-Seidel acceleration factor of 1.47, or fast-decoupled update caps of 0.4 rad and 0.3 pu) that value is the default. It changes only when a benchmark gives a reason.
4. **Reference behaviour is a benchmark.** Survey observations and, later, back-test runs on licensed copies (sister companies, via the products' official scripting interfaces) are test targets alongside published benchmarks.
5. **Private stays private.** This public repository cites the survey only as "private study notes" with an engine family name. Paths, addresses and excerpts from the survey stay in QE-References. The WP-to-survey map is `etap-survey/WP-MAP.md` in QE-References.
6. **Engineering numbers still need a source** (AGENTS.md rule 5): a textbook, standard, published benchmark or the private study notes. Record which in the code comment and in `docs/sources/entries/`.
7. **Every result shows its working** (D11): governing equation, substituted values, result, source.

---

## 3. Architecture

### 3.1 Repository layout (Phase 3 additions in bold)

```
PLAN.md, AGENTS.md, CLAUDE.md, README.md
contracts/                JSON Schemas (common, project, power, pv, automation, studies)
packages/py/
  qe_core/                contracts, units, validation, project IO
  qe_power/
    adapters/pandapower/  independent cross-check (load flow, IEC 60909, motor start)
    textbook/             teaching Newton-Raphson (kept as a second reference)
    native/               Quantic's own power engines (Phase 3)
      core/               network compile, per-unit, sparse Ybus, stamps, factorization
      loadflow/           NR, GS, FD, DC, controls         (M3.1)
      topology/           switching, islands               (M3.1)
      contingency/        N-1, N-2, screening              (M3.1)
      fault/              sequence networks, IEC, ANSI     (M3.2)
      motor/              dynamic motor starting           (M3.3)
      harmonic/           frequency scan, harmonic flow    (M3.3)
      protection/         curves, coordination, arc flash  (M3.3)
      unbalanced/         three-phase phase-domain flow    (M3.4)
      dynamics/           transient stability              (M3.4)
      opf/, stability/, planning/                          (M3.4)
    io/                   MATPOWER, PSS/E, DGS import      (M3.5)
  qe_pv/, qe_plc/, qe_report/, qe_cli/, qe_api/
packages/ts/, apps/web/   workbench (apps/web/src/power/)  (M3.U)
tests/benchmarks/         shared benchmark cases and harness (WP-3.2)
docs/plan/PLAN-v1.md      archived plan
docs/research/            research phase outputs (parity matrix, engines, requirements)
```

### 3.2 Dependency rules (enforced in CI)

1. `qe_core` depends on nothing internal.
2. Domain packages depend only on `qe_core` and `contracts/`. Domain packages never import each other.
3. Only `qe_power/adapters/<engine>/` may import that engine (pandapower). `native/` uses NumPy and SciPy only and never imports an adapter.
4. Inside `native/`, every family depends on `native/core/`; families may use `native/loadflow/` for prefault or initial states; no other cross-family imports without a WP saying so.
5. `qe_cli`, `qe_api` and `qe_report` may depend on any domain package.
6. TypeScript never imports Python; it uses the API with types generated from `contracts/`.

### 3.3 Data flow of a study

```
project (JSON) -> qe_core validates -> native engine (or adapter) -> result JSON with diagnostics,
provenance and calculation trace -> qe_report -> report (Markdown, PDF)
```

---

## 4. Collaboration protocol

### 4.1 Roles and lanes (plan v3)

| Lane | Holder | Phase 3 work |
| --- | --- | --- |
| P | Peter | Owner: decisions, approvals, research requests on his PC, back-test runs on licensed copies |
| PO | Claude | Product owner: writes and revises the plan and acceptance criteria, accepts each milestone, answers requirement questions |
| PM | ChatGPT (Codex) | Product manager: keeps the board and work queue, reviews and merges every worker PR, returns rework, audits each milestone |
| W | DeepSeek agents in OpenCode | Workers: build every WP in tracks E, U, D and V (section 7.1) |

- Workers take WPs from the queue in `docs/agents/BOARD.md` in dependency order and never wait for review: open the PR, move to the next WP, come back for rework.
- **Review:** every PR gets an automatic Codex review (P0 and P1 findings) and a manager review before merge. The milestone audit replaces nothing; it is an extra check on the whole milestone.
- **Credits:** Claude and Peter keep their credits for Lender; Claude acts only at milestone acceptance and plan refreshes. Workers use the OpenCode Go allowance as set out in `AGENTS.md`.
- The full workflow, including how PRs, reviews and rework move without Peter, is `AGENTS.md`.

### 4.2 Work package lifecycle

1. Session review (AGENTS.md section 2), then the next WP in the queue whose dependencies are merged (or open, within the stacking rule of AGENTS.md).
2. Branch `wp-<id>-<short-name>`; change only owned paths, your Status and Change record, your learning note, and new files in `docs/log/` and `docs/sources/entries/`.
3. Tests first or alongside. Numerical code is tested against a reference with recorded provenance.
4. Commit at each completed section of the WP; final commit marks the WP Done with one `completed` log. PR titled `[WP-<id>] <title>` with acceptance output. The manager merges only with green CI and a passed review.

### 4.3 Why there are no merge conflicts

| Shared resource | Mechanism |
| --- | --- |
| Source files | Disjoint owned paths per WP; CI enforces |
| PLAN.md | Each model edits only its own WP status lines |
| Logs and sources | One new file per event or source |
| Contracts | Changed only by a Contract Change WP (4.5) |
| Benchmarks | WP-3.2 owns the harness; each later WP adds cases only under `tests/benchmarks/<family>/` |

### 4.4 Change log entries

`docs/log/<YYYY-MM-DD>-<model>-WP-<id>-<event>.md`, events `completed`, `changed-design`, `audit`, `dispute`. Format as in AGENTS.md section 5.

### 4.5 Contract changes

`contracts/` changes only through a Contract Change WP (CC-n) that Peter approves, that runs alone on the affected schema, bumps the schema version and updates dependants in the same PR. Phase 3 CC WPs are listed inside the batch that needs them.

### 4.6 Definition of Done (every WP)

- All acceptance commands pass on a clean checkout; CI is green.
- New code has tests; numerical code has a reference with provenance; tolerances are never loosened to pass.
- Results carry diagnostics, provenance and a calculation trace (D11).
- The learning note exists in `docs/learning/` and explains the concept and equations for Peter.
- No em dashes anywhere.
- Status set to Done with one completed log.

---

## 5. Decisions register

| ID | Decision | Status |
| --- | --- | --- |
| D1 | Product and repository name: Quantic Studio, `Pietrols/Quantic-Studio` | Agreed 2026-10-07 |
| D2 | Personal GitHub account | Agreed 2026-10-07 |
| D3 | Public repository | Agreed 2026-10-07 |
| D4 | License deferred (recommendation Apache-2.0 code, CC BY 4.0 docs) | Deferred 2026-10-07 |
| D5 | Lane holders: A Claude, B ChatGPT | Agreed 2026-10-07, batches 2026-10-31 |
| D6 | Electrical first; IT deferred | Agreed 2026-10-07 |
| D7 | Books, standards and the survey live only in private `Pietrols/QE-References` | Agreed 2026-10-07 and 2026-10-14; survey added 2026-10-31 |
| D8 | Monorepo with strict boundaries | Recorded in ADR-0001 |
| D9 | JSON Schema contracts, generated Python and TypeScript types | Recorded in ADR-0002 |
| D10 | LV c_min 0.95 (Kasikci 1st ed. Table 1.1 p. 8); revisit when IEC 60909-0 is owned | Decided 2026-10-14 |
| D11 | Every study result shows its working | Required 2026-10-14 |
| D12 | Voltage levels: LV up to 1 kV, MV above 1 kV to 33 kV, HV above 33 kV | Decided 2026-10-14 |
| D13 | Node 26 for local work and CI | Decided 2026-10-14 |
| D14 | Native engines in Python on NumPy/SciPy; Rust only later via PyO3 for proven bottlenecks | Decided 2026-10-21 |
| D15 | Learn-then-build method (section 2), including use of established and survey-observed constants as defaults | Decided by Peter 2026-10-31 |
| D16 | One product release, no separate student edition | Decided by Peter 2026-10-31 |
| D17 | Suite order after power: PV (PVsyst), PLC (TIA Portal, CODESYS), circuits and control (MATLAB/Simulink, Proteus); CAD later on SolidCraft and CADCraft | Decided by Peter 2026-10-31 |
| D18 | Paid standards bought only at release (acquisition list WP-2.29); until then a value without an owned source is a recorded gap | Agreed 2026-10-19 |
| D19 | Network model v1: terminals and implicit cubicles, switches as objects, type/element split with explicit overrides, operating scenarios as overlays, no stored bus type (derived from control modes), following PowerFactory | Proposed 2026-11-04 |
| D20 | Diagrams are a separate contract from topology; one element may have many symbols | Proposed 2026-11-04 |
| D21 | Results never write into inputs; results carry an input hash and become stale on edit; copying results into the model is an explicit action | Proposed 2026-11-04 |
| D22 | Users see PowerFactory's mixed sign convention; engines use one internal convention converted at the result boundary | Proposed 2026-11-04 |
| D23 | Discrete controls move at most one step per outer iteration; repeated control states stop the run as a detected cycle | Proposed 2026-11-04 |
| D24 | Workbench follows PowerFactory's layout and workflow with ETAP touches, in white and grey with no blue; every dialog also has a JSON tab | Proposed 2026-11-04 |
| D25 | Textbook worked examples are private fixtures loaded through `QE_REFERENCES`; public CI uses public benchmarks; each milestone ends with recorded Playwright demos | Proposed 2026-11-04 |
| D26 | Roles: Claude product owner, ChatGPT product manager, DeepSeek workers in OpenCode (AGENTS.md) | Decided by Peter 2026-11-04 |

---

## 6. Roadmap

| Phase | Content | Milestone |
| --- | --- | --- |
| 3 Power suite | Milestones M3.0, M3.1 and M3.U (first worker batch), then M3.2 to M3.5 (sections 7 to 11) | One audit per milestone |
| 3 back-test | Same networks on licensed ETAP/PowerFactory via official scripting, compared with Quantic | after M3.2 |
| 4 Solar PV | PVsyst and HelioScope style design and yield, on research WP-2.23 to 2.26 | planned at end of Phase 3 |
| 5 Automation | PLC (TIA Portal, CODESYS style), on qe_plc and WP-2.28 | planned later |
| 6 Circuits and control | MATLAB/Simulink and Proteus style, on WP-2.27 | planned later |
| 7 CAD | On the SolidCraft and CADCraft forks | later |

Each later phase follows the same method: Peter supplies material, agents study it, then build.

---

## 7. Phase 3 delivery structure (plan v3.0)

Proposed by Claude (product owner) on 2026-11-04 for agreement with ChatGPT (product manager) and approval by Peter. Workers are DeepSeek agents running in OpenCode. How they work, review and merge is in `AGENTS.md`; this section says what they build.

### 7.1 Tracks and milestones

Work runs in four parallel tracks with disjoint owned paths, so several worker sessions can run at once without conflicts.

| Track | Content | Worker agent |
| --- | --- | --- |
| E | Native engines in `qe_power/native/` | `qs-engine` |
| U | Workbench in `apps/web/` and `packages/ts/` | `qs-ui` |
| D | Contracts, migration, API, import/export | `qs-engine` (contract WPs run alone) |
| V | Benchmarks, worked examples, recorded demos | `qs-verify` |

| Milestone | WPs | Exit condition |
| --- | --- | --- |
| M3.0 Foundation | 3.0, 3.4, 3.5, 3.6, 3.1, 3.2, 3.3, 3.7, 3.49 | Workflow proven; network v1 contract; native core builds Ybus that matches references |
| M3.1 Load flow | 3.10 to 3.15, 3.17, 3.18, 3.19, 3.16 | Every load-flow method solves public and textbook cases with shown working |
| M3.U Workbench | 3.50 to 3.58, 3.59 | A user builds, runs and reads a load flow entirely in the UI, PowerFactory style, recorded on video |
| M3.2 Short circuit | 3.20, 3.21, 3.27, 3.28, 3.29, 3.26 | IEC 60909 and ANSI duties on native engine, textbook-checked |
| M3.3 Plant studies | 3.22 to 3.25, 3.36 | Motor starting, harmonics, protection, arc flash |
| M3.4 Advanced | 3.30 to 3.35 | Unbalanced, transient stability, OPF, voltage stability, planning |
| M3.5 Interchange and reports | 3.41 to 3.45 | Import/export, libraries, reports |

**First batch for the workers: M3.0, M3.1 and M3.U, 30 WPs.** M3.2 onward are specified at scope level here and are expanded by Claude in WP-3.60 after the M3.1 audit, with a research refresh, as Peter's method requires (deep research every 5 to 7 steps).

### 7.2 Product target for the power suite

A PowerFactory or ETAP user should recognise the workflow without training:

1. **Model**: terminals (busbars) connected through cubicles to elements; switches and couplers are real objects; each element references a **type** from a library (PowerFactory type/element split), with explicit instance overrides.
2. **Bus type is derived, never typed in**: slack, PV and PQ come from element control modes (external grid as reference, generator voltage control, load), as PowerFactory does.
3. **Operating data are separate from equipment data**: an operating scenario overlays dispatch, setpoints, tap positions and switch states; a study case selects grids, scenario and study commands.
4. **Diagrams are separate from topology**: one element may appear in several diagrams; deleting a symbol does not delete the element unless asked.
5. **Study commands are objects with documented options** (load flow command with Basic, Advanced and Iteration Control pages).
6. **Results never write into inputs.** Results are stored per study run with an input hash; editing inputs marks results stale. Copying results into the model (for example tap positions) is an explicit "update model" action.
7. **Every result shows its working** (D11), and every run lists warnings and errors that link back to the element.

### 7.3 Look and feel (for track U)

PowerFactory first, with ETAP touches, in Peter's colours: plain white canvas, grey panels and tabs, no blue.

```
+------------------------------------------------------------------------------------------+
| Menu: File  Edit  Calculation  Data  Output  Tools  Window  Help                         |
| Main toolbar: new/open/save | study case selector | scenario selector | run LF, SC ... |
+---------------------+------------------------------------------------+-------------------+
| Project tree        | Single-line diagram (tabs per diagram)          | Drawing tools     |
| (Data Manager):     | white canvas, IEC symbols, result boxes per     | terminal, line,   |
|  Library            | element side, colour by loading/voltage         | transformer, load,|
|  Network model      |                                                 | generator, grid,  |
|   Grids, Diagrams   |                                                 | switch, shunt ... |
|  Operating scenarios|                                                 |                   |
|  Study cases        |                                                 |                   |
+---------------------+------------------------------------------------+-------------------+
| Output window: progress, info / warning / error, each message links to its element        |
+------------------------------------------------------------------------------------------+
| Status bar: active study case | scenario | selection | zoom | unit system | result state  |
+------------------------------------------------------------------------------------------+
```

- Double-click an element: tabbed dialog (Basic Data, Load Flow, Short Circuit, Dynamics later, Description), type field with library picker, and a JSON tab that edits the same object (Peter: customisability, both JSON and a proper interface).
- Data Manager: tree plus a flexible data grid per element class (sort, filter, bulk edit, paste from spreadsheets).
- Result boxes: per element side, configurable variables and decimals; legend for colour bands.
- Panels dock, resize and hide; toolbar contents and result-box templates are user settings.
- Result sign convention shown to users is PowerFactory's "mixed" convention (branches and loads positive out of the bus, generation positive into the network); engines use one internal convention and convert only at the result boundary.

### 7.4 Reference material and fixtures

- **Reading map**: `research/engineering-software/PHASE3-READING-MAP.md` in the private reference library lists, per WP, which atlas chapters, survey reports and textbook pages to read. Read it before each WP. It points to the newest research through `research/engineering-software/CURRENT.md` there.
- **Public benchmarks** (MATPOWER cases, IEEE test feeders, values computed by our own independent code) live in this repository under `tests/benchmarks/` with licence notes.
- **Textbook worked examples** stay private (AGENTS.md rule 6). Their input data and printed answers are stored in the private library under `fixtures/textbook/<book-id>/<example>.json`. Tests in this repository load them through `QE_REFERENCES` (the path to a local clone) and skip, with a visible message, when it is not set. Public CI therefore runs public benchmarks only; the worker runs textbook checks locally and pastes only pass/fail and error figures into PRs, never the book's numbers.
- **Independent expectations**: no expected value in a test may be produced by the code under test. References come from hand calculation, a textbook, a published solution or an independent implementation (pandapower through its adapter boundary), with provenance.
- **Mandatory load-flow checks** for every method: KCL and power balance, Jacobian against finite differences (NR), PV/PQ limit entry and release, transformer orientation (tap on either side), island references, divergence and singular cases reported as failures. Later families get their own list in WP-3.60.
- **Recorded demos**: Playwright video of each milestone demo. Demos on public cases are attached to the milestone's GitHub release; demos on textbook cases are stored in the private library under `demos/`.

### 7.5 Workbench user journeys (acceptance for M3.U)

Agreed with ChatGPT on 2026-11-04 from its workbench specification. Every journey runs as a Playwright test against the real local API, not mocks.

| ID | Journey | Must hold |
| --- | --- | --- |
| UI-01 | Add and edit terminal, line, transformer, source and load through dialogs | No JSON needed for supported fields; units shown; missing data diagnosed on the field |
| UI-02 | Connect, disconnect and move symbols | Only electrical commands change topology; moving a symbol leaves the input hash unchanged |
| UI-03 | Edit in a sorted Data Manager grid, then undo and redo | The intended ids change; undo restores the model and the stale-result state together |
| UI-04 | Switch project or model with unsaved changes | Save, discard or cancel offered; a late response from the previous project never overwrites the current one |
| UI-05 | Create and compare operating scenarios | Base data preserved; which scenario supplied each value is visible |
| UI-06 | Run a study | Running, cancelled, failed, converged and not-converged look different; no silent fallback to another engine |
| UI-07 | Edit while viewing results | Results go stale visibly; exporting a stale result needs an explicit choice of the historical run |
| UI-08 | Select a violation or diagnostic | The matching element is selected in diagram, grid and dialog alike |
| UI-09 | Configure panels, toolbars and result boxes | Preferences never change solver inputs; restore defaults works |
| UI-10 | Save, close and reopen the project on another machine | Model and diagram layout retained; local preferences optional |
| UI-11 | API unavailable, timeout or save conflict | Clear recovery, unsaved edits kept, no false success |
| UI-12 | Compare and export runs | Engine and version, method, input hash, units, assumptions and diagnostics travel with the export |

Screenshots of the populated network, a selected element, a validation error, a result overlay, a failed solve and an expanded grid are captured at 1366x768 and 1920x1080 on the tested commit, and checked at 200 percent browser zoom with keyboard-only navigation.

---

## 8. Milestone M3.0: Foundation

### WP-3.9 Plan v3 adoption

Status: [x] Done | implemented by Claude | commit 7fedda7 | 2026-11-04
Lane: P (Peter approves), drafted by Claude with ChatGPT's review
Depends on: none
Owned paths: `PLAN.md`, `AGENTS.md`, `opencode.json`, `.opencode/**`, `docs/agents/README.md`, `docs/agents/BOARD.md`, `docs/agents/messages/**`

Authorized by Peter on 2026-11-04: replace the plan with plan v3.0 (roles: Claude product owner, ChatGPT product manager, DeepSeek workers in OpenCode; Phase 3 as milestones M3.0 to M3.5), replace `AGENTS.md` with the v3 workflow, add the OpenCode agent definitions, and hand the board to the product manager. Delivered in PR #84 after review by ChatGPT.

Acceptance: every CI check passes on the PR head, including the ownership check; ChatGPT records agreement in the channel; Peter merges.

Learning note: none.
Change record: none

### WP-3.0 Agentic workflow dry run

Status: [~] In progress | DeepSeek (opencode-go/deepseek-v4.1-flash) | branch wp-3.0-workflow-dry-run | started 2026-11-05 | blocked by Codex connection and manager steps
Lane: W-V (DeepSeek worker), with ChatGPT and Peter
Depends on: none
Owned paths: `docs/agents/workflow/dry-run.md`

Prove the delivery loop of `AGENTS.md` section 3 on a trivial change before any engineering WP:

1. The worker creates branch `wp-3.0-workflow-dry-run`, writes `docs/agents/workflow/dry-run.md` (one paragraph describing the run), commits in two commits, opens a PR with the template, and posts `@codex review`.
2. Codex automatic review (or the mention) posts a review. Record whether it ran automatically.
3. ChatGPT, as manager, requests one deliberate change. Record how the worker received it: comment polled by the local session, `/oc` comment handled by the OpenCode GitHub action, or scheduled action.
4. The worker fixes it on the same branch; ChatGPT merges with green CI.
5. On Peter's PC, record `opencode --version`, `opencode models` and `opencode agent list`; confirm every agent in `.opencode/agents/` loads and resolves to the intended DeepSeek model, and correct the model ids in the agent files if the host lists them differently.
6. Record in the document: which triggers worked, latency of each step, and anything that needed Peter.

Acceptance: PR merged by the manager with green CI; `dry-run.md` records the outcome of every step, including steps that failed and the fallback used.

Learning note: none.
Change record: none

### WP-3.4 Contract Change CC-10: network model v1.0

Status: [ ] Not started
Lane: W-D (DeepSeek worker), runs alone on `contracts/power/`
Depends on: WP-3.0
Owned paths: `contracts/power/**`, `contracts/common/**`, `packages/py/qe_core/src/qe_core/power/**`, `packages/py/qe_core/tests/power/**`, `packages/ts/contracts/**`, `docs/contracts/network-v1.md`

Add a separately versioned network v1 contract alongside the existing v0.2 contract, with an equipment model that PowerFactory and ETAP users recognise. Preserve existing schema files, IDs, generated exports and consumers until explicit migration. Schema version 1.0.0, `$id` `urn:quantic-studio:contracts:1.0.0:power:network`.

1. **Identity**: every object has a stable `id` (string), `name`, optional `description`, `out_of_service` flag. IDs never encode position.
2. **Containers**: `grids[]` (each with nominal frequency 50 or 60 Hz), `areas[]` and `zones[]` optional.
3. **Terminals** (`terminals[]`): `id`, `grid_id`, `nominal_kv`, `phase_technology` (`ABC`, later others), `usage` (`busbar`, `junction`, `internal`), optional voltage limits `v_min_pu`, `v_max_pu`.
4. **Cubicles** are implicit: each element connection is `{ "terminal": <terminal id> }` held on the element, with a fixed side name (`hv`, `lv`, `tv`, `from`, `to`, `bus`). This keeps PowerFactory's terminal to cubicle to element chain without a separate list.
5. **Switches and couplers** (`switches[]`): two terminal connections, `kind` (`circuit_breaker`, `disconnector`, `load_break`, `fuse`, `coupler`), `closed` default state, optional rated current. Closed ideal switches merge terminals in study preparation.
6. **Types** (`types` object with `line`, `cable`, `transformer_2w`, `transformer_3w`, `synchronous_machine`, `asynchronous_machine`, `load`): rated and per-length parameters only. Units in field names (`r_ohm_per_km`, `uk_percent`, `pcu_kw`, `tap_step_percent`, `tap_min`, `tap_max`, `tap_neutral`, `tap_side`, `vector_group`).
7. **Elements** (`lines[]`, `transformers_2w[]`, `transformers_3w[]`, `loads[]`, `synchronous_machines[]`, `asynchronous_machines[]`, `static_generators[]`, `external_grids[]`, `shunts[]`, `series_reactors[]`): connections, `type_id` where applicable, instance data (`length_km`, `parallel`, `tap_position`), and explicit nullable override fields where an instance may differ from its type. Lines may also carry direct per-unit or ohmic data without a type (`model: "type" | "direct"`).
8. **Control modes** on sources and loads: external grid `control: "slack" | "pv" | "pq"`; synchronous machine `control: "voltage" | "pq" | "slack"` with `v_setpoint_pu`, `q_min_mvar`, `q_max_mvar`, optional `controlled_terminal` for remote control; load model `constant_power | constant_current | constant_impedance | zip | exponential` with coefficients. There is no `bus_type` field anywhere.
9. **Transformer tap controller** on the element: `enabled`, `controlled_terminal`, `v_setpoint_pu`, `deadband_pu` (or upper and lower setpoints), `mode: "stepped" | "continuous"`.
10. **Operating scenarios** (`scenarios[]`): each overrides a whitelisted set of operating fields (switch states, dispatch, setpoints, tap positions, out-of-service flags). Base data plus one active scenario gives the study data.
11. **Units and bases**: system base `base_mva` at network level (default 100). Per-unit conversion happens only in study preparation, never in stored data.
12. Generated Python and TypeScript types; validation errors name the object id and field.

Acceptance:

- Schemas validate the four example networks after migration (WP-3.6 supplies them; this WP includes two hand-written v1 examples: a 3-terminal radial feeder and a 2-grid ring with a coupler).
- Negative tests: missing type reference, connection to unknown terminal, duplicate id, scenario overriding a non-whitelisted field. Each gives a diagnostic naming id and field.
- `docs/contracts/network-v1.md` documents every object with a v0.2 to v1 field map.

Learning note: `docs/learning/network-model-type-element.md`, explaining terminals, cubicles, type versus element, derived bus types and why operating data are separate.
Change record: none

### WP-3.5 Contract Change CC-11: diagram, study case and command contracts

Status: [ ] Not started
Lane: W-D (DeepSeek worker), runs alone on the new schemas
Depends on: WP-3.4
Owned paths: `contracts/project/diagram.schema.json`, `contracts/studies/**`, `packages/py/qe_core/src/qe_core/studies/**`, `packages/py/qe_core/tests/studies/**`, `packages/ts/contracts/src/diagram/**`, `packages/ts/contracts/src/studies/**`, `packages/ts/contracts/scripts/**`, `packages/ts/contracts/src/index.ts`, `packages/ts/contracts/src/generated.ts`, `docs/contracts/diagram-and-study-case.md`

1. **Diagram** (`diagram.schema.json`): `diagrams[]`, each a list of symbols `{ element_id, symbol, x, y, rotation, mirror, side_anchors }` and connection polylines. Many symbols may reference one element. This replaces browser-local layout storage.
2. **Study case**: `id`, `name`, active `grid_ids`, active `scenario_id`, list of command ids, study time (optional), result-box template id.
3. **Load flow command**: `method` (`ac_newton_raphson`, `ac_newton_raphson_current`, `ac_gauss_seidel`, `ac_fast_decoupled_xb`, `ac_fast_decoupled_bx`, `dc`), `flat_start` or `from_previous`, `tolerance_mva` (default 0.001, the documented ETAP criterion of 0.001 MW/Mvar), `max_iterations_inner` (default 25), `max_iterations_outer` (default 20), `consider_q_limits`, `automatic_tap_adjustment` (`off`, `stepped`, `continuous`), `automatic_shunt_adjustment`, `load_voltage_dependency`, `distributed_slack` (`none`, `by_generation`, `by_load`), `gs_acceleration` (default 1.47), `fd_angle_cap_rad` (0.4), `fd_voltage_cap_pu` (0.3), `nr_max_voltage_step_pu` (null, meaning none). Every default names its source in the schema description.
4. **Run/result envelope**: `run_id`, project/model revision, `study_case_id`, `command_id`, `input_hash` (SHA-256 of immutable canonical effective inputs), engine name and version, lifecycle (`queued`, `running`, `completed`, `failed`, `cancelled`), separate convergence and limit-assessment states, diagnostics and trace reference. Specify allowed transitions, cancellation acknowledgement versus process termination, stale-response rejection and artifact/restart policy. Failed or cancelled runs cannot expose a valid engineering result.
5. Existing study request contracts remain valid; the new command objects map onto them in WP-3.49.

Generation ownership is serialized after WP-3.4: the current generator writes src/generated.ts and uses scripts/generate.mjs; add explicit new outputs without deleting legacy exports.

Acceptance: schema tests for every command option and default; round trip through generated Python and TypeScript types; a study case referencing a missing scenario gives a named diagnostic.

Learning note: none (covered by WP-3.4 note and WP-3.55 note).
Change record: none

### WP-3.6 Migration from network v0.2 and adapter projection

Status: [ ] Not started
Lane: W-D (DeepSeek worker)
Depends on: WP-3.4
Owned paths: `packages/py/qe_core/src/qe_core/migrate/**`, `packages/py/qe_core/tests/migrate/**`, `packages/py/qe_power/src/qe_power/adapters/pandapower/project_v1.py`, `packages/py/qe_power/tests/adapters/test_project_v1.py`, `packages/py/qe_power/src/qe_power/textbook/project_v1.py`, `packages/py/qe_power/tests/textbook/test_project_v1.py`, `examples/**`, `docs/contracts/migration-v0.2-to-v1.md`

1. `qe_core.migrate.network_v02_to_v1(doc) -> (doc_v1, diagnostics)`: buses become terminals; lines and transformers get direct data (`model: "direct"`); `bus_type` becomes the control mode of the connected source; anything that cannot be mapped is reported, not dropped silently.
2. Migrate every network under `examples/`; keep the v0.2 originals under `examples/legacy-v0.2/` for regression.
3. Projection functions so the pandapower adapter and the textbook solver accept v1 networks (study preparation flattens v1 into their existing inputs). Their existing tests keep passing on migrated examples with identical results (1e-9 pu).

Acceptance: every example migrates with zero error diagnostics; adapter and textbook results on migrated examples equal the v0.2 results; a v0.2 network with an unmappable field produces a named warning.

Learning note: none.
Change record: none

### WP-3.1 Native power core: study preparation and sparse admittance

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.4
Owned paths: `packages/py/qe_power/src/qe_power/native/__init__.py`, `packages/py/qe_power/src/qe_power/native/core/**`, `packages/py/qe_power/tests/native/core/**`, `packages/py/qe_power/pyproject.toml`

Shared base for every native engine. NumPy and SciPy only (D14 and the 2026-11-01 engine-language consensus).

```
prepare(network_v1, scenario_id, grid_ids) -> StudySnapshot | diagnostics
  1. apply scenario overlay to a copy of base data
  2. drop out-of-service elements; record them
  3. merge terminals joined by closed switches/couplers (union-find); map terminal -> electrical node
  4. resolve types and instance overrides; convert to per unit on base_mva and each node's nominal kV
  5. derive node type from control modes: one slack per island (external grid or slack machine),
     PV for voltage-controlling sources with a controlled terminal, PQ otherwise
  6. freeze arrays: node index, element -> (node indices, stamp parameters), id maps for results

build_ybus(snapshot) -> scipy.sparse.csr_matrix (complex)
  pi line:        y = 1/(r + jx); stamp [[y + jb/2, -y], [-y, y + jb/2]]
  2W transformer: off-nominal ratio t and phase shift phi on the tap side, a = t * e^(j phi)
                  [[y/|a|^2, -y/conj(a)], [-y/a, y]]   (tap on from side)
  3W transformer: star equivalent from the three pair impedances, internal star node
  shunts:         diagonal admittance
  assemble with COO triplets, sum duplicates, convert to CSR once

factor(matrix) -> Factor   # scipy.sparse.linalg.splu wrapper; reuse for many right-hand sides
                           # only while the matrix values are unchanged (Newton Jacobians need a
                           # fresh numeric factor each iteration); a factor used after its matrix
                           # changed raises a diagnostic
  singular or near-singular matrix -> diagnostic naming the node set, never an exception to the user

trace module: Trace object that records steps as (equation id, symbolic form, substituted values,
  result, units, source); shared by all engines for D11
```

Transformer per-unit conversion: impedance from `uk_percent` and `pcu_kw` on the rated power, referred to the system base, with the off-nominal ratio computed from the rated voltages against the node nominal voltages and the tap position. Specify tap side, sign and impedance base independently for Quantic nameplate inputs. Private study notes include projection-specific stored-result reconstructions: do not apply a vendor-export impedance normalization to nameplate data or claim predictive vendor equivalence. Input adapters must identify their representation; test canonical stamps independently from original analytical inputs.

Acceptance:

- Ybus for MATPOWER case9, case14, case30 and case118 equals an independent build (pandapower internal Ybus, called only in the test through the adapter boundary) to 1e-12.
- Hand-calculated two-terminal line, tapped transformer (tap on each side, positive and negative steps), phase shifter and three-winding transformer cases match to 1e-12.
- Switch merging: a two-busbar station with a coupler produces one node when closed and two when open.
- Invalid topology (connection to unknown terminal, element with all terminals isolated) gives a named diagnostic.
- `prepare` on case118 runs in under one second warm on CI (recorded, not a product promise).

Learning note: `docs/learning/native-network-and-ybus.md`, explaining per unit, stamps, taps, phase shift, star equivalents and why sparse.
Change record: none

### WP-3.2 Benchmark library and comparison harness

Status: [ ] Not started
Lane: W-V (DeepSeek worker)
Depends on: WP-3.6
Owned paths: `tests/benchmarks/README.md`, `tests/benchmarks/harness/**`, `tests/benchmarks/cases/**`, `tests/benchmarks/test_harness.py`, `tests/benchmarks/private_fixtures.py`, `docs/benchmarks/**`

1. Public case library, each with source, licence and a stored reference solution: two-bus and three-bus analytical cases (our own derivation, shown in the README), MATPOWER case9, case14, case30, case57 and case118 converted to network v1, IEEE 4-node feeder (balanced).
2. Reference solutions: pandapower Newton-Raphson at tolerance 1e-10 (independent implementation) stored as JSON with version provenance; where MATPOWER publishes solved values, also the published values with their printed precision.
3. Harness: runs every registered solver on every case it supports and records maximum voltage magnitude error (pu), angle error (degrees), branch P and Q error (MW, Mvar), iterations, run time (cold and warm) and status. Exits nonzero if a solver exceeds its declared tolerance.
Performance evidence additionally records raw repetitions/distributions; model compile, assembly, solve and result/trace costs; peak process memory including native allocations and workers; hardware, OS, exact versions and thread settings. Expand to licence-reviewed larger cases after the small correctness baseline; add contingency/time-series throughput when available. Record unknown product budgets and do not turn preliminary adapter timings into native capacity claims.

4. `private_fixtures.py`: loads `fixtures/textbook/**` from `QE_REFERENCES`; skips with an explicit message when absent; never prints fixture values in test output (only pass/fail and error magnitudes).
5. Register what exists today: textbook NR solver and pandapower adapter. Write `docs/benchmarks/baseline-2026-11.md`.

Acceptance: `uv run pytest tests/benchmarks` passes; the harness fails on a deliberately perturbed reference; baseline lists every case and solver with numbers.

Learning note: `docs/learning/benchmarking-power-solvers.md`, explaining reference solutions, tolerances and why several independent checks.
Change record: none

### WP-3.3 Engine family map and Phase 3 learning index

Status: [ ] Not started
Lane: W-V (DeepSeek worker)
Depends on: none
Owned paths: `docs/research/power/phase3-family-map.md`

One table, one row per engine family: parity rows covered, WP, textbook and standard sources (by book id and section, no excerpts), public benchmarks, whether private study notes exist, open gaps (standards not owned). Survey paths stay in the private reading map.

Acceptance: every Phase 3 WP appears; every power parity row maps to a WP or is marked deferred.

Learning note: none.
Change record: none

### WP-3.7 Result store and invalidation

Status: [ ] Not started
Lane: W-D (DeepSeek worker)
Depends on: WP-3.5
Owned paths: `packages/py/qe_core/src/qe_core/results/**`, `packages/py/qe_core/tests/results/**`

1. Canonical serialisation of study data (base plus active scenario plus study case) and SHA-256 input hash.
2. Result store per project: `results/<study_case_id>/<run_id>.json` plus trace file; index of runs.
3. Staleness: a result is `current` when its input hash equals the hash of the present study data, otherwise `stale`. Stale results stay readable, flagged.
4. `update_model_from_result(result, fields)`: explicit, whitelisted copy of solved operating values (tap positions, generator Q) into the active scenario, returning a diff for the user to confirm.

Acceptance: editing any input field flips results to stale; editing a diagram position does not; update-model writes only whitelisted fields and the diff is exact.

Learning note: none.
Change record: none

### WP-3.49 API v1 for projects, network v1, study cases and results

Status: [ ] Not started
Lane: W-D (DeepSeek worker)
Depends on: WP-3.5, WP-3.6, WP-3.7
Owned paths: `packages/py/qe_api/src/qe_api/v1/**`, `packages/py/qe_api/src/qe_api/app.py`, `packages/py/qe_api/src/qe_api/runner.py`, `packages/py/qe_api/src/qe_api/worker.py`, `packages/py/qe_api/tests/v1/**`, `tests/integration/test_api_v1.py`, `docs/api/v1.md`

REST endpoints under `/api/v1/`: list and open projects; get and save network (with etag); get and save diagrams; CRUD study cases and commands; run a command (returns `run_id`, then progress events over Server-Sent Events, then result); list runs with stale flags; get result and trace; update model from result. Engine selection by command `method`, routing to native engines as they become available and to the pandapower adapter before that. Existing API stays for the old workbench until WP-3.59.

Reuse and extend the existing bounded process Runner; inventory timeout, byte-limit and slot-release behavior first. Register routes in app.py. Own v1/ integration exclusively until merged; WP-3.18 touches its nested registration paths only afterwards. Native/adapter selection must be explicit in capabilities and provenance, never a silent fallback for an unsupported method.

Acceptance: integration tests for every endpoint including etag conflict, cancellation that terminates the worker, worker failure, resource cleanup, immutable concurrent snapshots, late-response rejection and stale-result flagging after a save.

Learning note: none.
Change record: none

---

## 9. Milestone M3.1: Load flow

Worked-example milestone: when M3.1 closes, the workers solve, on our engines and through the UI, Grainger and Stevenson Example 9.5 (four-bus Newton-Raphson, printed page 353, with the Gauss-Seidel iteration of Examples 9.2 and 9.3 from printed page 338), Glover, Overbye and Sarma 6th edition Examples 6.9 to 6.11 (five-bus system, printed pages 346 to 357), and MATPOWER case9 to case118. Fixtures for the textbook cases are prepared in WP-3.19.

### WP-3.10 Native Newton-Raphson load flow

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.1, WP-3.2
Owned paths: `packages/py/qe_power/src/qe_power/native/loadflow/__init__.py`, `packages/py/qe_power/src/qe_power/native/loadflow/newton.py`, `packages/py/qe_power/src/qe_power/native/loadflow/mismatch.py`, `packages/py/qe_power/src/qe_power/native/loadflow/flows.py`, `packages/py/qe_power/src/qe_power/native/loadflow/options.py`, `packages/py/qe_power/tests/native/loadflow/test_newton*.py`, `packages/py/qe_power/tests/native/loadflow/test_flows*.py`, `tests/benchmarks/cases/loadflow/**`

```
solve_nr(snapshot, cmd) -> LoadFlowResult
  V = flat start (|V| = setpoint at PV and slack, 1.0 elsewhere; angle 0) or previous solution
  S_spec(V) = generation - load(V)            # ZIP and exponential loads depend on |V|
  for k in 1..max_iterations_inner:
      S_calc = V * conj(Ybus @ V)             # vectorised, sparse
      dP = P_spec - P_calc  (PV and PQ nodes); dQ = Q_spec - Q_calc (PQ nodes)
      record mismatch norm, worst node, in trace
      if max(|dP|, |dQ|) * base_mva <= tolerance_mva: converged
      J = sparse polar Jacobian from dS/dVa and dS/dVm (vectorised, no per-pair Python loop),
          including the dS_spec/dVm term for voltage-dependent loads
      solve J dx = mismatch with a fresh splu factor (values change each iteration)
      optional cap on |dVm| (nr_max_voltage_step_pu)
      update Va, Vm
  if not converged: status not_converged, result holds last iterate flagged invalid, never as a solution
  Q limits (consider_q_limits): after inner convergence, any PV node whose Q leaves [Qmin, Qmax]
      is clamped and becomes PQ (largest violation first); a clamped node returns to PV when its
      voltage crosses back past the setpoint in the recovering direction; re-solve; cap at
      max_iterations_outer; record every switch in the trace
  slack P and Q, PV Q computed from the solution
```

`flows.py`: branch terminal currents and powers from each branch's own stamp (taps and shunts included), losses per branch, loading in percent of rated current or MVA, node voltage in kV and pu, total generation, load and losses, and a power-balance check (residual reported).

Trace (D11): Ybus summary, the first iteration in full (mismatch vector, Jacobian entries for a chosen node, increment, updated state), every later iteration as norms and worst node, final balance.

Acceptance:

- case9, case14, case30, case57, case118: |V| within 1e-8 pu and angle within 1e-6 degrees of the pandapower reference; branch flows within 1e-6 MW/Mvar; published MATPOWER values within their printed precision.
- The two-bus example of the reading map reproduces its first-iteration increment to four significant figures.
- Q-limit case (case14 with tightened limits): the expected generators switch and the solution matches the reference with the same limits.
- An original analytically infeasible case with documented assumptions, or a deliberately exhausted iteration budget, returns the appropriate failure status with the worst node named. A fixed load multiplier is not proof of infeasibility; distinguish iteration exhaustion from physical infeasibility.
- Agrees with the textbook solver on all its supported cases.
- The analytic Jacobian matches a finite-difference Jacobian to 1e-6 relative on case14 at a non-flat state; KCL and power balance close to 1e-9 pu at every node of every converged case.

Learning note: `docs/learning/native-newton-raphson.md`, with mismatch, the four Jacobian blocks, why quadratic convergence, and Q-limit switching.
Change record: none

### WP-3.11 Gauss-Seidel and fast-decoupled solvers

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.10
Owned paths: `packages/py/qe_power/src/qe_power/native/loadflow/gauss_seidel.py`, `packages/py/qe_power/src/qe_power/native/loadflow/fast_decoupled.py`, `packages/py/qe_power/tests/native/loadflow/test_gauss_seidel*.py`, `packages/py/qe_power/tests/native/loadflow/test_fast_decoupled*.py`

1. Gauss-Seidel: sequential complex voltage update per node from the nodal equation, acceleration factor `gs_acceleration` (default 1.47 from the private study notes; the ETAP help gives 1.2 to 1.7, typically 1.45, so test both), PV nodes compute Q from the current state, update, then reset |V| to setpoint. Stop on the actual power residual, not only voltage change. Iteration budget from the command (ETAP documents 2000 for GS).
2. Fast-decoupled, XB and BX variants: constant B' and B'' factored once each (here factor reuse applies), alternating half iterations, caps 0.4 rad and 0.3 pu per update (private study notes).
3. Both reuse `mismatch.py` and `flows.py` from WP-3.10 and produce the same result structure and trace format.

Acceptance: both solve case9 to case118 to the NR solution within 1e-6 pu (they need not match NR's iteration history); GS fails cleanly (not_converged) on a case with a series capacitor where it is known to struggle; iteration counts recorded in the benchmark baseline.

Learning note: `docs/learning/gauss-seidel-and-fast-decoupled.md`.
Change record: none

### WP-3.12 Control outer loop: taps, switched shunts, remote voltage, load models

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.10
Owned paths: `packages/py/qe_power/src/qe_power/native/loadflow/controls/**`, `packages/py/qe_power/tests/native/loadflow/controls/**`, `packages/py/qe_power/src/qe_power/native/loadflow/loads.py`, `packages/py/qe_power/tests/native/loadflow/test_loads*.py`

1. Stepped tap control: after inner convergence, each controlled transformer whose controlled-terminal voltage lies outside its band moves **one step** toward the band per outer iteration (PowerFactory documents one step per outer iteration to avoid hunting); respects tap limits; reports limit reached.
2. Continuous tap control: tap ratio as an extra unknown replacing the controlled voltage equation, then rounded to the nearest step with a final re-solve when the command asks for discrete results.
3. Switched shunts: step toward the band, one step per outer iteration.
4. Remote voltage control by a generator (controlled terminal other than its own).
5. Cycle detection: if a control state repeats, stop with `not_converged` and a diagnostic naming the controllers in the cycle.
6. Load models in `loads.py`: constant P, I, Z, ZIP and exponential `P = P0 (V/V0)^a`, `Q = Q0 (V/V0)^b`, with their derivatives for the Jacobian.
7. Distributed slack by generation participation (option), solved with the slack-sharing variable in the Jacobian.

Acceptance: tap case where one transformer must move three steps does so in three outer iterations and reaches the band; a two-transformer interaction case converges without hunting; a forced oscillation case is detected as a cycle; ZIP loads match the pandapower reference with equivalent load models to 1e-8 pu; distributed slack matches a hand-checked three-node case.

Learning note: `docs/learning/load-flow-controls.md`.
Change record: none

### WP-3.13 Topology processing and islands

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.1, WP-3.10
Owned paths: `packages/py/qe_power/src/qe_power/native/topology/**`, `packages/py/qe_power/tests/native/topology/**`

1. Island detection on the prepared node graph (union-find over in-service branches and closed switches).
2. Per island: exactly one reference source chosen by priority (external grid slack, then slack machine, then the largest voltage-controlling machine if the command allows automatic choice, with a warning); islands without a source are **unsupplied** and reported, with no voltages invented.
3. Engines solve each energised island independently and merge results.
4. Connectivity checks for the UI: list of elements per island, de-energised elements.

Acceptance: a network opened at a coupler solves as two islands matching two separate solves; an island with loads and no source is reported unsupplied and its elements have no voltage; the reference choice is recorded in the trace.

Learning note: `docs/learning/topology-and-islands.md`.
Change record: none

### WP-3.14 Contract Change CC-8: contingency study contracts

Status: [ ] Not started
Lane: W-D (DeepSeek worker), runs alone on the contingency schemas
Depends on: WP-3.5
Owned paths: `contracts/studies/contingency-*.schema.json`, `packages/py/qe_core/src/qe_core/studies/contingency.py`, `packages/py/qe_core/tests/studies/test_contingency*.py`, `packages/ts/contracts/src/studies/contingency/**`

Contingency command: list or rule set of outages (N-1 of branches, transformers, generators; user-defined N-2 groups), monitored elements, limits (thermal percent, voltage band), screening method (`full_ac`, `dc_screen_then_ac`). Result: per contingency status, worst violations, and comparison with base case.

Acceptance: schema tests and round trip; invalid outage reference gives a named diagnostic.

Learning note: none.
Change record: none

### WP-3.15 Contingency analysis

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.12, WP-3.13, WP-3.14, WP-3.17
Owned paths: `packages/py/qe_power/src/qe_power/native/contingency/**`, `packages/py/qe_power/tests/native/contingency/**`

1. Full AC N-1: for each outage, re-prepare topology (islands may form), warm-start from the base solution, solve with the command's method, record violations.
2. DC screening: linear outage distribution factors (LODF) from the DC model to rank contingencies; only the top ranked go to full AC.
3. Results ranked by severity with the base case alongside.

Acceptance: case30 N-1 full AC equals 41 independent full solves; DC screening records ranking differences and recall against full AC under declared assumptions; all reported critical candidates are AC-verified and unscreened cases are explicitly unevaluated, with no guarantee that DC reproduces AC ranking; an islanding outage reports the unsupplied load.

Learning note: `docs/learning/contingency-analysis.md`.
Change record: none

### WP-3.17 DC load flow

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.1
Owned paths: `packages/py/qe_power/src/qe_power/native/loadflow/dc.py`, `packages/py/qe_power/tests/native/loadflow/test_dc*.py`

B-theta formulation from branch reactances and phase shifts, one linear solve, flows from angle differences. Trace shows the B matrix and the solve.

Acceptance: equals the pandapower DC reference to 1e-10 on case9 to case118.

Learning note: covered in `docs/learning/contingency-analysis.md`.
Change record: none

### WP-3.18 Load flow verification report and engine registration

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.10, WP-3.11, WP-3.12, WP-3.13, WP-3.17, WP-3.49
Owned paths: `packages/py/qe_power/src/qe_power/native/loadflow/report.py`, `packages/py/qe_power/src/qe_power/native/loadflow/register.py`, `packages/py/qe_power/tests/native/loadflow/test_report*.py`, `packages/py/qe_api/src/qe_api/v1/engines/loadflow.py`, `packages/py/qe_api/tests/v1/engines/test_loadflow*.py`

1. Verification report like PowerFactory's: overloaded elements over a threshold, voltage violations against terminal limits, generators at Q limit, transformers at tap limit, unsupplied areas.
2. Result conversion to the user-facing mixed sign convention at the boundary, with the convention named in the result.
3. Register every native load-flow method with the API engine router; native NR becomes the default engine for `ac_newton_raphson`.

Acceptance: report on case14 with tightened limits lists exactly the expected violations; API runs every method end to end; sign convention test on a three-node case with generation, load and a line.

Learning note: none.
Change record: none

### WP-3.19 Load flow worked examples and fixture pack

Status: [ ] Not started
Lane: W-V (DeepSeek worker)
Depends on: WP-3.2, WP-3.11
Owned paths: `tests/benchmarks/textbook/**`, `docs/benchmarks/loadflow-worked-examples.md`

1. In the private library (separate PR there): fixture JSON for Grainger Examples 9.2, 9.3 and 9.5 and Glover Examples 6.9 to 6.11, each with book id, edition, example number, printed page, network data, and printed answers with their printed precision. Data transcribed from the book pages and checked against the PDF page, not from OCR alone.
2. In this repository: tests that run every load-flow method on each fixture through `private_fixtures.py`, asserting agreement within half the printed last digit, printing only pass/fail and error magnitudes.
3. `docs/benchmarks/loadflow-worked-examples.md`: which examples pass, method, iteration counts, maximum error, and any disagreement explained (with no textbook numbers).

Acceptance: every fixture passes with NR; GS reproduces the textbook's first-iteration values where the book prints them; the document lists all results.

Learning note: none.
Change record: none

### WP-3.16 Milestone M3.1 audit

Status: [ ] Not started
Lane: Manager (ChatGPT), with product owner acceptance by Claude
Depends on: WP-3.10 to WP-3.15, WP-3.17 to WP-3.19
Owned paths: `docs/log/**`

ChatGPT reruns every M3.1 acceptance command on a clean checkout, rereads the numerical tests and their references, and checks the trace of one case by hand. Claude then reviews the milestone against section 7.2 and accepts or returns it with numbered findings.

Acceptance: `audit` log by ChatGPT and an acceptance log by Claude; disputes resolved.

Learning note: none.
Change record: none

---

## 10. Milestone M3.U: Workbench

Starts as soon as WP-3.5 is merged (it builds on the contracts) and runs in parallel with M3.1. Supersedes WP-3.40. Owned paths below are inside `apps/web/src/power/` and `packages/ts/`; the old workbench files stay until WP-3.59 retires them.

### WP-3.50 Application shell and layout

Status: [ ] Not started
Lane: W-U (DeepSeek worker)
Depends on: WP-3.5
Owned paths: `apps/web/src/power/shell/**`, `apps/web/src/power/theme/**`, `apps/web/tests/power/shell/**`, `apps/web/e2e/power/shell.spec.ts`, `apps/web/power.html`, `apps/web/src/power/main.tsx`, `apps/web/src/power/App.tsx`, `apps/web/vite.config.ts`

Layout of section 7.3: menu bar, main toolbar with study case and scenario selectors, project tree left, diagram tabs centre, drawing tools right, output window bottom, status bar. Dockable, resizable, hideable panels with layout saved per user. Theme tokens: white canvas, greys for panels and tabs, no blue (accents in dark grey and a single warm accent for selection). Keyboard: standard shortcuts (Ctrl+S, Ctrl+Z, Delete, F2 rename, F10 run load flow following ETAP habit, documented in a shortcut sheet).

Mount the new shell through a separate power.html development/test entry before any UI e2e. Keep the old default entry until retirement. Add a minimal bootstrap App for shared composition; subsequent feature integration is coordinated through one owner. Initial shell e2e may use explicit contract fixtures; integrated journeys later use the real API.

Acceptance: e2e test opens the new entry and checks every region; panels resize and persist; no colour with a blue hue in theme tokens (test reads tokens).

Learning note: none.
Change record: none

### WP-3.51 Single-line diagram editor

Status: [ ] Not started
Lane: W-U (DeepSeek worker)
Depends on: WP-3.50, WP-3.49
Owned paths: `apps/web/src/power/diagram/**`, `packages/ts/canvas/**`, `apps/web/tests/power/diagram/**`, `apps/web/e2e/power/diagram.spec.ts`

1. IEC symbols for terminal (busbar drawn as a bar), line, cable, 2W and 3W transformer, synchronous machine, asynchronous motor, load, static generator, external grid, shunt, switch, breaker.
2. Drawing like PowerFactory: pick a tool, click a terminal to start, click another to finish; the element is created in the network with its connections; dialog opens for type selection.
3. Grid snap, orthogonal routing, move with connections following, multi-select, copy and paste (new ids), undo and redo.
4. Several diagrams per grid; delete symbol versus delete element distinguished.
5. Persist through the diagram contract (WP-3.5) via the API, replacing localStorage layout.

Acceptance: e2e draws the three-terminal radial feeder from empty, saves, reloads identically; undo and redo of ten operations; deleting a symbol keeps the element and its other symbols.

Learning note: none.
Change record: none

### WP-3.52 Element and type dialogs

Status: [ ] Not started
Lane: W-U (DeepSeek worker)
Depends on: WP-3.50, WP-3.49
Owned paths: `apps/web/src/power/dialogs/**`, `apps/web/tests/power/dialogs/**`, `apps/web/e2e/power/dialogs.spec.ts`

Tabbed dialogs for every element and type class of network v1: Basic Data, Load Flow, Short Circuit (fields present, used from M3.2), Description, JSON. Type field with library picker and "edit type". Instance overrides shown beside the type value. Units shown with every field and convertible in place. Validation inline, using the same diagnostics as the API. The JSON tab edits the same object with schema validation, and switching tabs keeps edits.

Acceptance: e2e edits a transformer through both the form and JSON tabs and the saved network is identical either way; an invalid value shows the API diagnostic on the field; every element class opens a dialog (generated test over the schema).

Learning note: none.
Change record: none

### WP-3.53 Data Manager and flexible data grid

Status: [ ] Not started
Lane: W-U (DeepSeek worker)
Depends on: WP-3.50, WP-3.49
Owned paths: `apps/web/src/power/datamanager/**`, `apps/web/tests/power/datamanager/**`, `apps/web/e2e/power/datamanager.spec.ts`

Project tree (Library, Network model with grids and diagrams, Operating scenarios, Study cases) and, for a selected class, a grid of all objects with chosen columns; sort, filter, bulk edit, paste a block from a spreadsheet, export CSV. Selecting a row highlights the symbol on the diagram and the reverse.

Acceptance: paste of 20 load rows from CSV text updates 20 loads; filter and sort; cross-selection between grid and diagram.

Learning note: none.
Change record: none

### WP-3.54 Equipment libraries in the UI

Status: [ ] Not started
Lane: W-U (DeepSeek worker)
Depends on: WP-3.52
Owned paths: `apps/web/src/power/library/**`, `apps/web/tests/power/library/**`

Global (read-only shipped) and project libraries of types; create, copy and edit project types; where-used list for a type; changing a type shows which elements are affected. Shipped types come only from sourced data (WP-3.42); until then the global library is empty with an explanation.

Acceptance: create a line type, assign to three lines, edit it, see three elements affected; where-used is exact.

Learning note: none.
Change record: none

### WP-3.55 Study cases, scenarios and the load flow command dialog

Status: [ ] Not started
Lane: W-U (DeepSeek worker)
Depends on: WP-3.50, WP-3.49
Owned paths: `apps/web/src/power/studycase/**`, `apps/web/tests/power/studycase/**`, `apps/web/e2e/power/studycase.spec.ts`

Create, copy and activate study cases and scenarios; scenario editor shows only the fields that differ from base. Load flow command dialog with pages Basic (method, Q limits, tap and shunt adjustment, load voltage dependency), Advanced (initialisation, distributed slack, step caps) and Iteration Control (tolerances, inner and outer limits, GS acceleration), every field with its default and a help line naming its source.

Acceptance: e2e creates a scenario that opens a breaker, activates it, and the run uses it; every command option round-trips.

Learning note: `docs/learning/study-cases-and-scenarios.md`, for users moving from PowerFactory and ETAP.
Change record: none

### WP-3.56 Output window, progress and cancellation

Status: [ ] Not started
Lane: W-U (DeepSeek worker)
Depends on: WP-3.50, WP-3.49
Owned paths: `apps/web/src/power/output/**`, `apps/web/tests/power/output/**`

Streams run progress (iteration, mismatch norm) from the API events; messages as info, warning and error with a severity icon and grey styling (not colour alone); double-click a message to select and open the element; cancel a running study; copy and export the log.

Acceptance: a nonconvergent run shows its worst-node error message and clicking it selects that terminal; cancel stops a long contingency run.

Learning note: none.
Change record: none

### WP-3.57 Results on the diagram, result grid and comparison

Status: [ ] Not started
Lane: W-U (DeepSeek worker)
Depends on: WP-3.51, WP-3.53, WP-3.18
Owned paths: `apps/web/src/power/results/**`, `apps/web/tests/power/results/**`, `apps/web/e2e/power/results.spec.ts`

Result boxes per element side with templates (default: terminal kV, pu and angle; branch P, Q, I and loading), colour bands for voltage and loading with legend; stale results greyed with a banner; result grid per class; "show working" opens the trace for a selected element; compare two runs side by side with differences; update model from result with a confirm diff.

Acceptance: case14 run shows result boxes equal to the API result; editing a load marks results stale; comparison of two scenarios shows the correct differences.

Learning note: none.
Change record: none

### WP-3.58 Recorded demos

Status: [ ] Not started
Lane: W-V (DeepSeek worker)
Depends on: WP-3.57, WP-3.19
Owned paths: `apps/web/e2e/demos/**`, `apps/web/playwright.demos.config.ts`, `docs/demos/README.md`

Playwright scripts, run headed-equivalent with `video: "on"` and slowed actions, that build a network from an empty project through the UI, run a load flow and assert the displayed values. Demos: MATPOWER case9 built by hand (public, attached to the M3.U release), and the Grainger four-bus and Glover five-bus examples (private, read from `QE_REFERENCES`, video saved to the private library `demos/`). Each video has a caption track naming the steps.

Acceptance: demos run in CI for the public case and produce a video artifact; private demos run locally; `docs/demos/README.md` explains how to rerun them.

Learning note: none.
Change record: none

### WP-3.59 Milestone M3.U audit and old workbench retirement

Status: [ ] Not started
Lane: Manager (ChatGPT), with product owner acceptance by Claude
Depends on: WP-3.50 to WP-3.58
Owned paths: `docs/log/**`, `apps/web/src/App.tsx`, `apps/web/src/GraphCanvas.tsx`, `apps/web/src/Symbol.tsx`, `apps/web/src/main.tsx`, `apps/web/tests/app.test.tsx`, `apps/web/tests/project-switch.test.tsx`, `apps/web/tests/power.test.ts`, `apps/web/e2e/workspace.spec.ts`

ChatGPT audits as for WP-3.16, then switches `main.tsx` to the new power workbench and removes the old power files once nothing references them (PV and PLC workspaces stay). Claude reviews the recorded demos against section 7.3 and accepts or returns findings; Peter tries it.

Acceptance: every journey of section 7.5 passes; audit and acceptance logs; old workbench tests removed or migrated; CI green.

Learning note: none.
Change record: none

---

## 11. Later milestones (scope level, expanded in WP-3.60)

### WP-3.60 Plan refresh for M3.2 onward

Status: [ ] Not started
Lane: Product owner (Claude), reviewed by ChatGPT
Depends on: WP-3.16
Owned paths: `PLAN.md` (section 11 only)

After the M3.1 audit, with a research refresh on ETAP and PowerFactory short-circuit, protection and arc-flash behaviour, expand the WPs below to the level of sections 8 to 10.

Acceptance: section 11 WPs carry full steps, owned paths and acceptance; ChatGPT agrees in the channel; Peter approves.

Learning note: none.
Change record: none

### WP-3.20 Native fault engine: sequence networks and fault types

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.1, WP-3.10
Owned paths: `packages/py/qe_power/src/qe_power/native/fault/**`, `packages/py/qe_power/tests/native/fault/**`, `tests/benchmarks/fault/**`

Positive, negative and zero sequence networks from network v1 (vector groups and earthing decide zero-sequence connectivity); balanced and unbalanced faults (3-phase, line-to-ground, line-to-line, double line-to-ground) by Thevenin impedances from factored sequence matrices; prefault from flat 1 pu or a load-flow solution; contributions per branch. Worked examples: Glover chapter 7 and 9, Grainger chapters 10 to 12.

Acceptance: to be detailed in WP-3.60.
Learning note: `docs/learning/sequence-networks-and-faults.md`.
Change record: none

### WP-3.21 IEC 60909 on the native fault engine

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.20
Owned paths: `packages/py/qe_power/src/qe_power/native/fault/iec60909/**`, `packages/py/qe_power/tests/native/fault/iec60909/**`

Initial symmetrical current, voltage factor c (D10 and D18 gaps recorded), correction factors for generators, power station units and network transformers, peak current methods, breaking current, thermal equivalent, near and far from generator. Worked examples: Kasikci and Das (2002), with the edition limits recorded in the catalogue.

Acceptance: to be detailed in WP-3.60.
Learning note: `docs/learning/iec-60909-native.md`.
Change record: none

### WP-3.27 ANSI/IEEE fault duties

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.20
Owned paths: `packages/py/qe_power/src/qe_power/native/fault/ansi/**`, `packages/py/qe_power/tests/native/fault/ansi/**`

First-cycle, interrupting and 30-cycle networks, multiplying factors, X/R methods, equipment duty checks. Sources: Das (2002) and the private study notes.

Acceptance: to be detailed in WP-3.60.
Learning note: `docs/learning/ansi-fault-duties.md`.
Change record: none

### WP-3.28 Short-circuit UI

Status: [ ] Not started
Lane: W-U (DeepSeek worker)
Depends on: WP-3.57, WP-3.21
Owned paths: `apps/web/src/power/shortcircuit/**`, `apps/web/tests/power/shortcircuit/**`

Short-circuit command dialog, fault location selection on the diagram, result boxes for fault currents and contributions, duty check grid.

Acceptance: to be detailed in WP-3.60.
Learning note: none.
Change record: none

### WP-3.29 Short-circuit worked examples

Status: [ ] Not started
Lane: W-V (DeepSeek worker)
Depends on: WP-3.21, WP-3.27
Owned paths: `tests/benchmarks/textbook/fault/**`, `docs/benchmarks/fault-worked-examples.md`

Acceptance: to be detailed in WP-3.60.
Learning note: none.
Change record: none

### WP-3.26 Milestone M3.2 audit

Status: [ ] Not started
Lane: Manager (ChatGPT), with product owner acceptance by Claude
Depends on: WP-3.20, WP-3.21, WP-3.27, WP-3.28, WP-3.29
Owned paths: `docs/log/**`

Acceptance: as WP-3.16.
Learning note: none.
Change record: none

### WP-3.22 Dynamic motor starting

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.10, WP-3.20
Owned paths: `packages/py/qe_power/src/qe_power/native/motor/**`, `packages/py/qe_power/tests/native/motor/**`

Static and dynamic motor starting with torque-slip models and load torque, starter types, voltage dip at terminals over time. Acceptance to be detailed in WP-3.60.

Learning note: `docs/learning/dynamic-motor-starting.md`.
Change record: none

### WP-3.23 Contract Change CC-9: harmonic, protection and arc-flash contracts

Status: [ ] Not started
Lane: W-D (DeepSeek worker), runs alone on the affected schemas
Depends on: WP-3.5
Owned paths: `contracts/studies/harmonic-*.schema.json`, `contracts/studies/protection-*.schema.json`, `contracts/studies/arcflash-*.schema.json`, `packages/py/qe_core/src/qe_core/studies/plant.py`, `packages/py/qe_core/tests/studies/test_plant*.py`

Acceptance to be detailed in WP-3.60.
Learning note: none.
Change record: none

### WP-3.24 Harmonic analysis

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.10, WP-3.23
Owned paths: `packages/py/qe_power/src/qe_power/native/harmonic/**`, `packages/py/qe_power/tests/native/harmonic/**`

Frequency scan (driving-point impedance), harmonic load flow with current-source injections, THD and IHD, resonance identification. Sources: Arrillaga and Watson; Das (2002). Acceptance to be detailed in WP-3.60.

Learning note: `docs/learning/harmonic-analysis.md`.
Change record: none

### WP-3.25 Protection curves, coordination and arc flash

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.21, WP-3.23
Owned paths: `packages/py/qe_power/src/qe_power/native/protection/**`, `packages/py/qe_power/tests/native/protection/**`

IEC and IEEE inverse-time curves, coordination margins, clearing time from fault currents, incident energy by IEEE 1584 (edition gap recorded per D18). Sources: Blackburn and Domin; Alstom NPAG; Das (2021). Acceptance to be detailed in WP-3.60.

Learning note: `docs/learning/protection-and-arc-flash.md`.
Change record: none

### WP-3.36 Milestone M3.3 audit

Status: [ ] Not started
Lane: Manager (ChatGPT), with product owner acceptance by Claude
Depends on: WP-3.22, WP-3.24, WP-3.25
Owned paths: `docs/log/**`

Acceptance: as WP-3.16.
Learning note: none.
Change record: none

### WP-3.30 Three-phase unbalanced load flow

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.12, WP-3.20
Owned paths: `packages/py/qe_power/src/qe_power/native/unbalanced/**`, `packages/py/qe_power/tests/native/unbalanced/**`

Phase-domain current-injection Newton (PowerFactory documents the current formulation as better for unbalanced networks), IEEE 4-node and 13-node feeders. Acceptance to be detailed in WP-3.60.

Learning note: `docs/learning/unbalanced-load-flow.md`.
Change record: none

### WP-3.31 Transient stability

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.10, WP-3.20
Owned paths: `packages/py/qe_power/src/qe_power/native/dynamics/**`, `packages/py/qe_power/tests/native/dynamics/**`

Classical and detailed machine models, exciters and governors from public standard block definitions, events, integration with network solution at each step. Sources: Kundur; Sauer and Pai. Acceptance to be detailed in WP-3.60.

Learning note: `docs/learning/transient-stability.md`.
Change record: none

### WP-3.32 AC optimal power flow

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.10
Owned paths: `packages/py/qe_power/src/qe_power/native/opf/**`, `packages/py/qe_power/tests/native/opf/**`

Acceptance to be detailed in WP-3.60.
Learning note: `docs/learning/optimal-power-flow.md`.
Change record: none

### WP-3.33 Voltage stability (continuation power flow)

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.10
Owned paths: `packages/py/qe_power/src/qe_power/native/stability/**`, `packages/py/qe_power/tests/native/stability/**`

Acceptance to be detailed in WP-3.60.
Learning note: `docs/learning/voltage-stability.md`.
Change record: none

### WP-3.34 Planning tools: capacitor placement and battery sizing

Status: [ ] Not started
Lane: W-E (DeepSeek worker)
Depends on: WP-3.12
Owned paths: `packages/py/qe_power/src/qe_power/native/planning/**`, `packages/py/qe_power/tests/native/planning/**`

Acceptance to be detailed in WP-3.60.
Learning note: `docs/learning/planning-tools.md`.
Change record: none

### WP-3.35 Milestone M3.4 audit

Status: [ ] Not started
Lane: Manager (ChatGPT), with product owner acceptance by Claude
Depends on: WP-3.30 to WP-3.34
Owned paths: `docs/log/**`

Acceptance: as WP-3.16.
Learning note: none.
Change record: none

### WP-3.41 Network import: MATPOWER and PSS/E RAW

Status: [ ] Not started
Lane: W-D (DeepSeek worker)
Depends on: WP-3.4
Owned paths: `packages/py/qe_power/src/qe_power/io/matpower/**`, `packages/py/qe_power/src/qe_power/io/psse/**`, `packages/py/qe_power/tests/io/**`

Import to network v1 with a loss report (what could not be represented). Acceptance to be detailed in WP-3.60.

Learning note: none.
Change record: none

### WP-3.42 Equipment libraries

Status: [ ] Not started
Lane: W-D (DeepSeek worker)
Depends on: WP-3.4
Owned paths: `packages/py/qe_core/src/qe_core/library/**`, `packages/py/qe_core/tests/library/**`, `libraries/**`

Shipped global type library built only from sourced data (textbook tables, manufacturer datasheets, each entry with its source). Acceptance to be detailed in WP-3.60.

Learning note: none.
Change record: none

### WP-3.43 Study reports for the native engines

Status: [ ] Not started
Lane: W-D (DeepSeek worker)
Depends on: WP-3.18
Owned paths: `packages/py/qe_report/src/qe_report/native/**`, `packages/py/qe_report/tests/native/**`

Markdown and PDF reports with input summary, results, violations and the calculation trace (D11). Acceptance to be detailed in WP-3.60.

Learning note: none.
Change record: none

### WP-3.45 PowerFactory and ETAP interchange

Status: [ ] Not started
Lane: W-D (DeepSeek worker)
Depends on: WP-3.41
Owned paths: `packages/py/qe_power/src/qe_power/io/dgs/**`, `packages/py/qe_power/tests/io/dgs/**`

Import of PowerFactory DGS exports for the core classes (terminals, lines, transformers, loads, machines, external grids, switches) into network v1, so PowerFactory users can bring models across. ETAP interchange is investigated in the research refresh. Acceptance to be detailed in WP-3.60.

Learning note: none.
Change record: none

### WP-3.44 Milestone M3.5 audit

Status: [ ] Not started
Lane: Manager (ChatGPT), with product owner acceptance by Claude
Depends on: WP-3.41 to WP-3.43, WP-3.45
Owned paths: `docs/log/**`

Acceptance: as WP-3.16.
Learning note: none.
Change record: none

### WP-3.61 Release qualification for the power suite

Status: [ ] Not started
Lane: Manager (ChatGPT), with product owner acceptance by Claude
Depends on: WP-3.44
Owned paths: `docs/release/**`

Proposed by ChatGPT (campaign B9). Clean-machine install, offline use, backup and restore, project migration and rollback, licence and source gates, operating documentation. Detailed in WP-3.60.

Acceptance: to be detailed in WP-3.60.
Learning note: none.
Change record: none

### WP-3.40 Workbench redesign

Status: [!] Changed design | due to Peter's request for a PowerFactory-style workbench built by worker agents, while original was one redesign WP in batch D, as it was better for building the UI as nine testable WPs in parallel with the engines (M3.U, WP-3.50 to WP-3.59) | Claude | 2026-11-04
Lane: superseded
Depends on: none
Owned paths: none

Superseded by milestone M3.U.

Learning note: none.
Change record: Status: [!] Changed design | due to Peter's request for a PowerFactory-style workbench built by worker agents, while original was one redesign WP in batch D, as it was better for building the UI as nine testable WPs in parallel with the engines (M3.U, WP-3.50 to WP-3.59) | Claude | 2026-11-04

---

## 12. Carried over from plan v1

Kept so their branches stay valid. Parked until Peter reopens them.

### WP-2.5 Solar PV first end-to-end yield slice

Status: [ ] Not started
Lane: B, parked (branch `wp-2.5-pv-yield`); full text in `docs/plan/PLAN-v1.md`
Depends on: WP-2.4 (Done, see archive)
Owned paths: `packages/py/qe_pv/**`, `packages/py/qe_api/src/qe_api/pv/**`, `packages/py/qe_cli/src/qe_cli/pv/**`, `packages/py/qe_report/src/qe_report/pv/**`, `packages/py/qe_report/tests/pv/**`, `apps/web/src/workspaces/pv/**`, `apps/web/tests/pv/**`, `apps/web/e2e/pv/**`, `tests/fixtures/pv/**`, `tests/integration/pv/**`, `examples/pv/**`

Learning note: `docs/learning/pv-first-yield-study.md`, explaining solar geometry, POA, temperature, loss order, clipping and energy coverage.
Change record: none

### WP-2.6 Industrial automation first end-to-end scan slice

Status: [ ] Not started
Lane: A, parked; full text in `docs/plan/PLAN-v1.md`
Depends on: WP-2.4, WP-2.9 (Done, see archive)
Owned paths: `packages/py/qe_plc/**`, `packages/py/qe_api/src/qe_api/plc/**`, `packages/py/qe_cli/src/qe_cli/plc/**`, `packages/py/qe_report/src/qe_report/plc/**`, `packages/py/qe_report/tests/plc/**`, `apps/web/src/workspaces/plc/**`, `apps/web/tests/plc/**`, `apps/web/e2e/plc/**`, `tests/fixtures/plc/**`, `tests/integration/plc/**`, `examples/plc/**`

Learning note: `docs/learning/plc-first-scan-and-process-study.md`, explaining ST evaluation, scan images, timer/counter state and discrete interlocks.
Change record: none

### WP-2.30 Power research refresh against the original products

Status: [ ] Not started
Lane: B (ChatGPT), optional; draft prepared, full text in `docs/plan/PLAN-v1.md`
Depends on: WP-2.12 (Done, see archive)
Owned paths: `docs/research/power/refresh-2026-10.md`

Learning note: none.
Change record: none
