# Quantic Open Engineering Platform: Master Plan

**Owner:** Peter Kabamba, Quantic Engineering Limited
**Plan version:** 1.2 (7 October 2026)
**Repository:** `Pietrols/Quantic-Studio` (product name: Quantic Studio)
**Companion research:** `docs/atlas/Engineering-Software-Atlas.md` and `docs/atlas/Engineering-Software-Catalogue.xlsx`

**Version history**

| Version | Date       | Change                                                                                                                                                                                                                                                                            |
| ------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-10-07 | First issue                                                                                                                                                                                                                                                                       |
| 1.1     | 2026-10-07 | Peter's review: IT network lab moved out of Phase 0 and year-one parallel work, so electrical comes first; textbooks held in a local reference library for verification only; Peter's hand calculation replaced by published textbook cases; WPs renumbered (no work had started) |
| 1.2     | 2026-10-07 | Decisions D1 to D4 recorded; WP-0.0 closed; GitHub Copilot added as Lane A implementer for WP-0.1                                                                                                                                                                                 |

This is the single source of truth for what gets built, in what order, by whom, and in what state it is. Every AI model working on this repository must read it at the start of every session, as `AGENTS.md` requires.

---

## 0. How to use this document

### 0.1 Status legend

Every work package (WP) has exactly one `Status:` line. Only four forms are allowed:

| Status         | Exact line format                                                                                                                         |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Not started    | `Status: [ ] Not started`                                                                                                                 |
| In progress    | `Status: [~] In progress \| <model> \| branch <branch-name> \| started <YYYY-MM-DD>`                                                      |
| Done           | `Status: [x] Done \| implemented by <model> \| commit <short-sha> \| <YYYY-MM-DD>`                        |
| Changed design | `Status: [!] Changed design \| due to <reason>, while original was <original>, as it was better for <benefit> \| <model> \| <YYYY-MM-DD>` |

Rules:

1. **Done means the implementer has passed all tests and acceptance commands with green CI.** The implementing agent marks its own WP Done. There is no per-WP cross-verification. A different model cross-audits each milestone, first M0 in WP-0.10. Historical Done lines with a `verified by` field remain valid records.
2. **Changed design is a record, not a hiding place.** When a model departs from a WP as written, it sets the Changed design status _before_ continuing, and copies the same sentence into that WP's `Change record:` list. The Change record is permanent. When the WP is later completed, the status becomes Done, but the Change record stays.
3. **In progress is optional.** A WP normally goes from Not started to Done in a single pull request. Use In progress only when a WP must pause across sessions or is blocked; a blocked WP appends `blocked by <WP or reason>` to its status line.
4. WP-0.3 (plan checker and owned-path guard) is Done. CI validates every status line and checks that a WP branch changes only its owned paths.

### 0.2 Who edits what in this file

| Who                | May edit                                                                              |
| ------------------ | ------------------------------------------------------------------------------------- |
| Implementing model | Only the `Status:` and `Change record:` lines of its WP, including setting its own Done status              |
| Milestone auditor | Records milestone audit findings in new logs; does not perform per-WP sign-off |
| Peter              | Anything. Peter alone approves new WPs, contract changes and edits to sections 0 to 6 |

All other changes to this file go through a WP that names `PLAN.md` in its owned paths, and only Peter approves that WP.

### 0.3 Reading order for a busy owner

If you only have five minutes, read section 1 and the status lines in section 7. Everything else is reference.

---

## 1. Summary

**What:** an open, cross-platform engineering software suite, built as one platform with focused workbenches that share a project format, units, schemas, plotting, reports and solver adapters.

**Year-one purpose:** tools usable for real engineering work and real contracts, with the governing equations and assumptions visible so they also teach.

**Year-one order (agreed):**

1. Power network study workbench (load flow, short circuit, cable and motor-start checks, protection basics, reports)
2. PV plant design workbench
3. Circuit and control canvas (Proteus/Simulink-style)
4. PLC and motor control workbench

**Electrical comes first and alone.** The IT track (visual network lab) and the mechanical, civil and robotics branches start only after Peter decides the electrical work is far enough along. They reuse the same platform, so nothing built now is wasted.

**First milestone (M0, end of week 2):** one command runs a verified load flow on the IEEE 14-bus test network and produces a results file and a readable report. Two independent solvers agree with each other and with the published reference solution, and CI proves it on every commit.

---

## 2. Answers to the starting questions

### 2.1 Do the models need textbooks?

Not for standard theory. Newton-Raphson load flow, symmetrical components, transfer functions and machine equivalent circuits are well known, and any model can derive them. Textbooks help in three narrower ways:

1. **Worked examples become test cases.** A textbook example with a published answer is an independent check on our solvers.
2. **Standards hold numbers that models must not guess.** IEC 60909 correction factors, IEC 60255 curve constants and cable ampacity tables must be taken from the actual standard, not recalled.
3. **Textbook worked examples checked locally.** Peter's books stay in the local reference library (section 2.2) and are used to confirm that our formulas and results are right, so nothing in the platform rests on a guessed or invented value.

### 2.2 Can textbooks be attached to the repo?

**Not copyrighted ones.** Owning a copy for study does not give the right to redistribute it, and a public repository is redistribution. Formulas, physical laws and engineering methods are not protected by copyright, so we may use the information freely. What we may not publish is the book's own text, figures, tables or worked examples.

**The local reference library.** Peter keeps his books and paid standards in a folder **outside the repository**, for example `~/QE-References/`. Keeping it outside the repo means a book can never be committed by accident. Rules:

1. Models use the library to check formulas, constants and parameters, never to copy passages.
2. Every formula or constant in our code cites its source in a comment: book, edition, page or clause. Example: `# Theraja, Electrical Technology Vol. 3, page <n>: per-unit base conversion`.
3. A source entry in `docs/sources/entries/` records each book used (citation only, no content).
4. Only a model that can reach Peter's Mac, and that Peter has granted access to that folder, can read the library. A cloud model without that access asks Peter for the value, or hands the check to a session that has access.
5. CI rejects committed `.pdf`, `.epub` and `.djvu` files outside an explicit allowlist (WP-0.2), as a second safety net.

What _can_ be committed:

- Openly licensed material, under its license terms, such as OpenStax (CC BY 4.0) and _Lessons in Electric Circuits_ (Design Science License). MIT OpenCourseWare is CC BY-NC-SA, so its non-commercial condition needs care for a company project.
- Public-domain material.
- Our own derivations and test cases, including cases built from textbook problems where we write our own numbers and wording.
- Test data with permissive licenses, such as MATPOWER cases (BSD-3), which include published textbook networks, and the University of Washington Power Systems Test Case Archive.

Paid standards (IEC, IEEE) and client data never go in the public repo. They stay in the local reference library. The repo also git-ignores a `private/` folder for scratch work.

### 2.3 Repository strategy

**One monorepo with strict package boundaries.** Reasons:

- Early work changes schemas, adapters, tests and docs together. One repo keeps those changes atomic.
- One CI, one issue tracker and one plan for all models.
- Boundaries are enforced by owned paths, dependency rules and CI checks, so packages can split into separate repos later if needed.
- Large external engines (pandapower, ngspice, containerlab) stay external dependencies. They are never copied in.

**Host:** GitHub, under Peter's personal account or a free organisation (decision D2). **Visibility:** public from day one is recommended (decision D3). GitHub Free only enforces protected branches on public repositories, and protected branches are what stop unreviewed merges.

### 2.4 Languages per layer

| Layer                                                   | Language and tools                                               | Why                                                                                    |
| ------------------------------------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Contracts (shared data definitions)                     | JSON Schema 2020-12                                              | Language-neutral; generates Python and TypeScript types                                |
| Engines and adapters                                    | Python 3.12+, managed with `uv`                                  | The open engines we reuse are Python (pandapower, pvlib, python-control, SymPy, SciPy) |
| Performance kernels (only if profiling proves the need) | Rust via PyO3, or WebAssembly for browser use                    | Not before a measured bottleneck                                                       |
| API service                                             | Python with FastAPI                                              | Same process as the engines                                                            |
| User interface                                          | TypeScript + React, managed with `pnpm`; React Flow for diagrams | Peter's existing skill set; MIT-licensed canvas                                        |
| Desktop packaging (later phase)                         | Tauri (Rust shell) with a Python sidecar                         | One codebase for Windows, macOS and Linux                                              |
| Documentation                                           | Markdown                                                         | Diffable in git; readable by every model                                               |

### 2.5 Engines: reuse versus build

| Capability                              | Reuse                                                  | Our own code                                                  | Note                                                   |
| --------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------- | ------------------------------------------------------ |
| Balanced load flow                      | pandapower (BSD-3)                                     | Textbook Newton-Raphson solver for verification and teaching  | Two independent implementations cross-check each other |
| Unbalanced and time-series distribution | pandapower 3-phase; OpenDSS via DSS-Extensions (BSD-3) | Adapter only                                                  | Evaluate in Phase 1                                    |
| Short circuit                           | pandapower IEC 60909 module                            | Textbook-verified fixtures                                    | Standard values from the purchased standard only       |
| Protection coordination                 | Evaluate pandapower protection module                  | Time-current curves, coordination checks, plots               | Curve constants from IEC 60255-151                     |
| PV design                               | pvlib (BSD-3); irradiance from PVGIS or NASA POWER     | Sizing rules, cabling, losses, report                         | Check data-source terms in Phase 2                     |
| Circuit simulation                      | ngspice (BSD-style) via netlist files and subprocess   | Netlist generator, waveform viewer                            | Avoid PySpice: it is GPL-3 and would bind our code     |
| Control analysis                        | python-control, SymPy, SciPy (all BSD-3)               | Block-diagram model, reduction, plots                         |                                                        |
| Microcontroller simulation              | Evaluate Renode (MIT)                                  | Board and peripheral visuals                                  | Phase 3 decision                                       |
| PLC logic                               | Evaluate OpenPLC/MATIEC (GPL-3, process boundary only) | Likely our own IEC 61131-3 Structured Text subset interpreter | Phase 4 decision                                       |
| Motor and generator dynamics            | SciPy ODE solvers                                      | dq-axis machine models                                        | Validated against published examples                   |
| Units                                   | pint (BSD-3)                                           | Unit conventions                                              |                                                        |

**GPL rule:** GPL programs may be used as separate processes that exchange files or network messages. GPL Python libraries must not be imported into our packages. (This is the common reading of the license, not legal advice.)

---

## 3. Architecture

### 3.1 Repository layout

```
qe-platform/
  PLAN.md                 this file
  AGENTS.md               rules every AI model follows
  CLAUDE.md               one line: @AGENTS.md
  README.md
  LICENSE
  contracts/              JSON Schemas: the shared language (versioned)
    common/               units, identifiers, diagnostics, provenance
    project/              project manifest
    power/                power network model and study results
  packages/
    py/
      qe_core/            loads and validates contracts; units; project IO
      qe_power/           power studies: adapters/ and textbook/
      qe_report/          report generation
      qe_cli/             command line entry point (qe ...)
    ts/                   added in Phase 1 (web UI)
  examples/               ready-to-run projects
  tests/
    fixtures/             reference cases, each with a provenance file
    integration/          cross-package and cross-solver tests
  tools/
    check_plan/           status-line and owned-path checker
  docs/
    atlas/                research atlas and catalogue
    decisions/            architecture decision records (ADR-0001 ...)
    specs/                human-readable contract specifications
    learning/             explainers written for Peter, one per topic
    sources/entries/      one YAML file per source (conflict-free register)
    log/                  one file per status change (conflict-free change log)
  private/                git-ignored scratch space
  .github/                CI workflows, PR and WP templates, CODEOWNERS

~/QE-References/          OUTSIDE the repo, on Peter's Mac only: books and paid standards
```

### 3.2 Dependency rules (enforced in CI from WP-0.2)

1. `qe_core` depends on nothing internal.
2. Domain packages (`qe_power` now; later ones such as `qe_pv`, `qe_circuit`, `qe_plc`) depend only on `qe_core` and `contracts/`. **Domain packages never import each other.**
3. Only `qe_power/adapters/<engine>/` may import that engine. If pandapower is replaced, only one folder changes.
4. `qe_cli` and `qe_report` may depend on any domain package.
5. TypeScript code never imports Python. It talks to the API using types generated from `contracts/`.

### 3.3 Data flow of a study

```
project folder (JSON) -> qe_core validates against contracts/ -> domain adapter runs engine
-> results JSON (contract-shaped, with diagnostics and provenance) -> qe_report -> report.md / PDF
```

Every result records the solver name and version, input file hash, convergence data and diagnostics. A result without provenance is a bug.

---

## 4. Collaboration protocol (how several models work without conflict)

### 4.1 Lanes

| Lane | Default holder | Focus                                                              |
| ---- | -------------- | ------------------------------------------------------------------ |
| P    | Peter          | Accounts, decisions, approvals, local reference checks, merging    |
| A    | Claude         | Python core, power engines, contracts drafting                     |
| B    | ChatGPT        | Tooling, CI, plan checker, reference fixtures, independent solvers |

Lane holders can be swapped (decision D5). **A different model cross-audits each milestone, first M0 in WP-0.10. Individual WPs are completed by their implementers.** Existing Lane fields naming per-WP verifiers describe the previous process and do not impose a sign-off gate.

### 4.2 Work package lifecycle

1. **Pick up:** the model runs the session review (AGENTS.md section 2), takes the Not started WP Peter assigned whose dependencies are Done, and creates branch `wp-<id>-<short-name>`. No reservation commit or start log.
2. **Build:** it changes only the WP's owned paths, plus its own Status and Change record, its named learning note, and new files in `docs/log/` and `docs/sources/entries/`.
3. **Complete:** the implementer runs all tests and acceptance commands locally, then in one final commit marks its own WP Done and adds the single completed log with evidence.
4. **Pull request:** titled `[WP-<id>] <title>`, using the PR template, listing the acceptance commands and their output. CI must pass on the PR head; failures are fixed in the same PR. Done reaches `main` only through a merge with green CI.
5. **Merge and continue:** the implementer merges with `gh`, pulls main, and proceeds to the next approved WP without waiting for Peter, respecting dependencies and explicit stop points.
6. **Milestone audit:** a different model reruns and reviews the milestone, first M0 in WP-0.10. Findings and their resolution are recorded before the milestone closes. WP-0.7 remains reserved for a model that has not read WP-0.6 implementation code.

### 4.3 Why there are no merge conflicts

| Shared resource | Conflict-free mechanism                                                                          |
| --------------- | ------------------------------------------------------------------------------------------------ |
| Source files    | Each WP owns disjoint paths; the WP-0.3 checker enforces ownership in CI               |
| PLAN.md         | Each model edits only its WP's status lines; WP blocks are far apart, so git merges them cleanly |
| Change log      | One new file per event in `docs/log/`; nobody edits an existing log file                         |
| Source register | One YAML file per source in `docs/sources/entries/`                                              |
| Contracts       | Frozen after approval; changed only through a serial Contract Change WP (section 4.5)            |

### 4.4 Change log entries

File name: `docs/log/<YYYY-MM-DD>-<model>-WP-<id>-<event>.md`, for example `2026-10-12-claude-WP-0.6-completed.md`. One `completed` log per WP; extra logs only for `changed-design`, `audit` and `dispute`. Older `start`, `progress`, `ready-for-review` and `verified` logs remain valid history.

```
wp: WP-0.6
model: Claude
event: completed | changed-design | audit | dispute
commit: <short-sha or none>
date: 2026-10-12
summary: one or two sentences
evidence: commands run and their result, or link to CI run
```

### 4.5 Contract changes

`contracts/` is frozen once its WP is Done. Any change needs a Contract Change WP, numbered CC-1, CC-2 and so on, which:

1. Is approved by Peter before work starts.
2. Runs alone: no other WP touching the affected contract may be In progress.
3. Bumps the schema version (major for breaking changes, minor for additions).
4. Updates every dependent package in the same PR, or opens follow-up WPs for them.

### 4.6 Definition of Done (every WP)

- All acceptance commands pass on a clean checkout.
- CI is green.
- New code has tests. Numerical code is tested against a reference with recorded provenance.
- The learning note named in the WP exists in `docs/learning/` and explains the concept, not just the code.
- No em dashes in any file (Peter's house style; CI checks this from WP-0.2).
- The implementer has updated the status and completed log with acceptance and CI evidence. Cross-audit happens at the milestone, not per WP.

---

The learning note named in a WP is an authorized path even when omitted from its Owned paths list. This standing rule resolves the plan gap and does not require a Changed design entry. Until older templates and WP wording are revised, this section takes precedence over their per-WP verifier checkboxes. Milestone M0 still requires its independent numerical checks and Peter's recorded run.

## 5. Decisions register

| ID  | Decision                                         | Recommendation                                                                                 | Status                                      |
| --- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------- | ------------------------------------------- |
| D1  | Product and repository name                      | Quantic Studio; repository `Pietrols/Quantic-Studio`                                           | Agreed by Peter, 2026-10-07                 |
| D2  | Personal account or free GitHub organisation     | Personal account (can transfer to an organisation later)                                       | Agreed by Peter, 2026-10-07                 |
| D3  | Public or private from day one                   | Public                                                                                         | Agreed by Peter, 2026-10-07                 |
| D4  | License                                          | Deferred; no LICENSE file yet (recommendation remains Apache-2.0 for code, CC BY 4.0 for docs) | Deferred by Peter, 2026-10-07               |
| D5  | Lane holders                                     | Lane A Claude, Lane B ChatGPT; GitHub Copilot implements WP-0.1 for Lane A                     | Agreed by Peter, 2026-10-07                 |
| D6  | Electrical first; IT and other branches deferred | Electrical only until Peter reopens other branches                                             | Agreed by Peter, 2026-10-07                 |
| D7  | Reference library                                | Books and paid standards in the private repo `Pietrols/QE-References` (local `~/QE-References/`), never in this repo; verification use only, readable by cloud agents | Agreed by Peter, 2026-10-07; private repo agreed 2026-10-14 |
| D8  | Monorepo                                         | Monorepo with strict boundaries (section 2.3)                                                  | Recommended; recorded in ADR-0001 by WP-0.1 |
| D9  | Contract source of truth                         | JSON Schema, with generated Python and TypeScript types                                        | Recommended; recorded in ADR-0002 by WP-0.4 |
| D10 | LV minimum voltage factor c_min                  | 0.95 for low-voltage networks of both tolerance classes (+6% and +10%), per Kasikci 1st ed (2002) Table 1.1 p. 8. IEC 60909-0:2016 Table 1 (as reported by DIgSILENT) gives 0.90 for the +10% class; 0.95 gives a minimum current about 5.6% higher there. Revisit when the 2016 or 2026 text is owned | Decided by Peter, 2026-10-14 |
| D12 | Voltage levels for fault studies                 | LV up to and including 1 kV, MV above 1 kV up to 33 kV, HV above 33 kV. Voltage factors follow Kasikci Table 1.1 p. 8 (MV and HV both 1.10 / 1.00) with D10 for LV; the adapter supplies them to the engine | Decided by Peter, 2026-10-14 |
| D13 | Node version                                     | Node 26 for local work and CI | Decided by Peter, 2026-10-14 |
| D11 | Every study result shows its working             | Reports state each governing equation, the substituted input values and the result, with the book source, so a reviewer can redo the calculation by hand | Required by Peter, 2026-10-14 |

---

## 6. Year-one roadmap

Week numbers are targets, not promises. Phases after Phase 0 are expanded into detailed WPs by a planning WP at the end of the previous phase, because detailed tickets written months ahead would be fiction.

| Phase                        | Target weeks           | Milestone  | What exists at the end                                                                                                                                               |
| ---------------------------- | ---------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0 Foundation                 | 1 to 2                 | M0         | Repo, CI, contracts v0, verified load flow from the command line                                                                                                     |
| 1 Power network workbench    | 3 to 14                | M1 to M5   | Web single-line editor; load flow; IEC 60909 short circuit; cable sizing and voltage drop; motor-start voltage dip; overcurrent coordination plots; PDF study report |
| 2 PV plant design            | 15 to 26               | M6 to M8   | Sun position and irradiance; module, string and inverter sizing; DC and AC cabling; loss chain; energy yield; grid connection studied with Phase 1 tools             |
| 3 Circuit and control canvas | 27 to 38               | M9 to M11  | Component canvas, ngspice simulation, oscilloscope view, transfer functions, step and Bode plots, controller tuning                                                  |
| 4 PLC and motor control      | 39 to 50               | M12 to M14 | Structured Text logic, MCC with several motors, interlocks, induction motor dynamics, starter and drive comparison, fault injection                                  |
| IT track (deferred, D6)      | After Peter reopens it | N1 to N4   | Topology generator (N1), deploy and inspect labs (N2), visual topology canvas (N3), guided CCNA-style exercises (N4)                                                 |
| Packaging                    | from Phase 1           | Releases   | Web build first; Tauri desktop builds for Windows, macOS and Linux                                                                                                   |

---

## 7. Phase 0 work packages (weeks 1 and 2)

**Dependency map:**

```
WP-0.0 (P) -> WP-0.1 (A) -> WP-0.2 (B), WP-0.3 (B), WP-0.4 (A)
WP-0.4 -> WP-0.5 (A), WP-0.8 (B)
WP-0.5 -> WP-0.6 (A), WP-0.7 (B)
WP-0.6 + WP-0.8 -> WP-0.9 (A)
WP-0.6 + WP-0.7 + WP-0.8 + WP-0.9 -> WP-0.10 (P + A, verified by B) -> M0
WP-0.10 -> WP-0.11 (Phase 1 planning)
```

**Week 1:** WP-0.0 to WP-0.4. **Week 2:** WP-0.5 to WP-0.11.

---

### WP-0.0 Manual setup by Peter

Status: [x] Done | implemented by Peter | verified by Claude | commit bootstrap | 2026-10-07
Lane: P
Depends on: none
Owned paths: none (outside the repository)

Peter creates the repository himself, so that he (or Quantic) owns it. The AI models are then given access to it; they do not own it.

Steps:

1. Make decisions D1 to D4 in section 5.
2. If D2 is "organisation": on github.com, create a free organisation. Then create an **empty** repository with the agreed name and visibility. Do not tick "Add a README"; WP-0.1 creates all files.
3. Tell Claude the repository's `owner/name`, so Claude can attach it to its session and do WP-0.1. Give ChatGPT access through its own GitHub connection when Lane B starts (WP-0.2).
4. Create the reference library folder on the Mac, outside any repository: `~/QE-References/`. Put the Theraja volumes and any standards there. Never place it inside the repo folder.
5. Before milestone M0, install the tools needed to run the code on the Mac yourself (the cloud models already have their own): Homebrew, git, GitHub CLI (`gh`), `uv`, and VS Code. Node.js with `pnpm` is needed only from Phase 1.
6. After WP-0.1 merges, turn on branch protection for `main`: require a pull request, require CI to pass, block force pushes.

Acceptance: Claude can read and push branches to the repo; decisions D1 to D4 are recorded in section 5; `~/QE-References/` exists outside the repo.
Learning note: none.
Change record:

- Changed design due to GitHub Copilot implementing WP-0.1 instead of Claude, while original was "Claude can read and push branches to the repo", as it was better for saving tokens in the planning session. Claude remains the verifier. (Peter, 2026-10-07)
- Changed design due to a repository with no commits blocking every branch, while original was "WP-0.1 creates all files", as it was better for giving all models a `main` branch to start from: Peter's bootstrap commit adds PLAN.md, AGENTS.md and a minimal .gitignore, which WP-0.1 then extends. (Peter, 2026-10-07)
- Branch protection (step 6) still happens after WP-0.1 merges.

---

### WP-0.1 Repository skeleton and rules

Status: [x] Done | implemented by Copilot | verified by Codex | commit cc4d834 | 2026-10-08
Lane: A (implement), B (verify)
Depends on: WP-0.0
Owned paths: `/*` (root files), `.github/ISSUE_TEMPLATE/**`, `.github/pull_request_template.md`, `.github/CODEOWNERS`, `docs/decisions/ADR-0001-monorepo.md`, `docs/README.md`, `docs/atlas/**`, all empty directories in section 3.1 (with `.gitkeep`)

This WP runs alone. No other WP starts until it is Done.

Steps:

1. Create the layout in section 3.1, with `.gitkeep` in empty folders.
2. Add `PLAN.md` and `AGENTS.md` exactly as supplied by Peter, and `CLAUDE.md` containing the single line `@AGENTS.md`.
3. Add `README.md` (purpose, status, how to run tests), `LICENSE` per D4, and `.gitignore` (Python, Node, OS files, `private/`, `QE-References/`, and `*.pdf`, `*.epub`, `*.djvu` with an explicit allowlist folder `docs/assets/` for our own PDFs).
4. Add the root `pyproject.toml` declaring a `uv` workspace with members `packages/py/*`.
5. Add `.github/ISSUE_TEMPLATE/work-package.md` mirroring the WP fields, and `.github/pull_request_template.md` with: WP id, owned paths touched, acceptance commands with output, learning note link, and a checklist from section 4.6.
6. Add `CODEOWNERS` assigning everything to Peter.
7. Copy the atlas and catalogue into `docs/atlas/`.
8. Write ADR-0001 recording the monorepo decision and its reasons (section 2.3).

Acceptance (verifier runs):

- `uv sync` succeeds at the repo root.
- Every folder in section 3.1 exists.
- The em dash check finds nothing: `LC_ALL=C.UTF-8 grep -rnP '\x{2014}' --exclude-dir=.git --exclude-dir=.venv --exclude-dir=node_modules .` returns no lines. (On macOS, use `ggrep` with the same arguments.)

Learning note: `docs/learning/monorepo-and-workspaces.md`: what a monorepo is, how `uv` workspaces work, why boundaries matter.
Change record:

- Changed design due to uv sync rejecting the package directories before WP-0.5 adds member manifests, while original was enabling the packages/py/* workspace members in WP-0.1, as it was better for keeping uv sync usable without inventing placeholder packages. (Copilot, 2026-10-07)
- Acceptance em dash command now excludes .venv and node_modules, due to installed dependencies containing em dashes. (Peter, 2026-10-07)

---

### WP-0.2 Continuous integration

Status: [x] Done | implemented by Codex | commit 55bd82e | 2026-10-08
Lane: B (implement), A (verify)
Depends on: WP-0.1
Owned paths: `.github/workflows/**`, `tools/ci/**`

Steps:

1. Add a GitHub Actions workflow running on every PR and on pushes to `main`: set up `uv`, run `uv sync`, run `ruff check`, run `pytest` across the workspace.
2. Add an em dash check script in `tools/ci/` that fails if any tracked text file contains U+2014.
3. Add an import-boundary check enforcing section 3.2 (for example with `import-linter`, configured in `tools/ci/`).
4. Add a reference-file guard that fails if any tracked `.pdf`, `.epub` or `.djvu` file exists outside `docs/assets/`.
5. Call `tools/check_plan` if it exists, so CI picks it up when WP-0.3 merges.

Acceptance:

- A test PR containing an em dash fails CI; removing it passes.
- A test PR where `qe_core` imports `qe_power` fails the boundary check.
- A test PR adding `book.pdf` at the repo root fails the reference-file guard.

Learning note: `docs/learning/continuous-integration.md`.
Change record: none

---

### WP-0.3 Plan checker and owned-path guard

Status: [x] Done | implemented by ChatGPT | commit 8923e6d | 2026-10-10
Lane: B (implement), A (verify)
Depends on: WP-0.1
Owned paths: `tools/check_plan/**`

Steps:

1. Write a Python command `tools/check_plan` that parses `PLAN.md` and checks:
   - every WP has exactly one `Status:` line in one of the four formats in section 0.1;
   - Done lines name a verifier different from the implementer;
   - Changed design lines contain all three clauses: `due to`, `while original was`, `as it was better for`;
   - every WP has `Lane`, `Depends on`, `Owned paths`, `Learning note` and `Change record` fields.
2. Add an owned-path guard: given a branch named `wp-<id>-...`, compare `git diff --name-only origin/main...HEAD` against that WP's owned paths, allowing only `PLAN.md` (its own status line), new files in `docs/log/`, and new files in `docs/sources/entries/`.
3. Add a summary mode that prints a table of all WPs and their statuses, so Peter can see progress at a glance.
4. Test both checks with good and bad sample plans.

Acceptance:

- `uv run python -m check_plan PLAN.md` passes on the real plan.
- Each malformed sample fails with a clear message naming the WP and the rule.
- `uv run python -m check_plan --summary PLAN.md` prints the status table.

Learning note: `docs/learning/parsing-and-validation.md`.
Change record: none

---

### WP-0.4 Contracts v0

Status: [x] Done | implemented by Copilot | commit a14e2b5 | 2026-10-08
Lane: A (implement), B (verify), Peter approves
Depends on: WP-0.1
Owned paths: `contracts/common/**`, `contracts/project/**`, `contracts/power/**`, `docs/specs/**`, `docs/decisions/ADR-0002-contracts.md`

Steps:

1. `contracts/common/`: diagnostic (code, severity, message, element reference), provenance (solver name and version, input hash, timestamp), and unit conventions. Field names carry their unit as a suffix: `vn_kv`, `p_mw`, `q_mvar`, `length_km`, `r_ohm_per_km`.
2. `contracts/project/`: project manifest (schema version, name, network file, list of studies).
3. `contracts/power/network`: buses, lines, two-winding transformers, loads, generators, external grid, shunts. Keep it engine-neutral: no pandapower-only fields.
4. `contracts/power/loadflow-request` and `loadflow-result`: per-bus voltage magnitude (pu) and angle (degrees); per-branch power flows, losses and loading; convergence (converged, iterations, largest mismatch); diagnostics; provenance.
5. `docs/specs/`: a readable page per schema with one example.
6. ADR-0002: why JSON Schema is the source of truth.

Acceptance:

- Every example in `docs/specs/` validates against its schema (verifier runs a short validation script).
- Peter has read the specs and approved in the PR.

Learning note: `docs/learning/data-contracts-and-per-unit.md`, covering both JSON Schema and the per-unit system.
Change record: none

---

### WP-0.5 Core package

Status: [x] Done | implemented by Codex | commit 6e69c0e | 2026-10-08
Lane: A (implement), B (verify)
Depends on: WP-0.4
Owned paths: `packages/py/qe_core/**`

Steps:

1. Generate Python models from the schemas, or validate with `jsonschema` at load time. Record which approach in the package README.
2. Add a project loader: read the manifest, load the network, validate, and return typed objects plus a list of diagnostics. Invalid input never raises an unexplained exception.
3. Add a units helper using `pint` and the conventions from WP-0.4.
4. Add a provenance helper that hashes input files.

Acceptance:

- `uv run pytest packages/py/qe_core` passes.
- Loading a deliberately broken project returns diagnostics naming the bad element and field.

Learning note: `docs/learning/validating-engineering-input.md`.
Change record: none

---

### WP-0.6 Pandapower load-flow adapter

Status: [x] Done | implemented by Codex and Claude | commit 81008fe | 2026-10-08
Lane: A (implement), B (verify)
Depends on: WP-0.5
Owned paths: `packages/py/qe_power/src/qe_power/adapters/pandapower/**`, `packages/py/qe_power/tests/adapters/**`, `packages/py/qe_power/pyproject.toml`

Steps:

1. Convert a contract network into a pandapower network. Report unsupported fields as diagnostics, never silently drop them.
2. Run Newton-Raphson load flow and convert results to the `loadflow-result` contract, including convergence data and provenance.
3. Translate non-convergence into a diagnostic that explains likely causes.

Acceptance:

- `uv run pytest packages/py/qe_power/tests/adapters` passes.
- A network built so it cannot converge returns a result with `converged: false` and a diagnostic, not a crash.

Learning note: `docs/learning/load-flow-with-pandapower.md`.
Change record: none

---

### WP-0.7 Textbook Newton-Raphson solver (independent implementation)

Status: [!] Changed design | due to Peter authorizing Codex to correct current-based loading, while original was reserving WP-0.7 for a model independent of WP-0.6, as it was better for resolving the loading defect with a formula-derived regression test and a documented limited exception | Codex | 2026-10-08
Lane: B (implement), A (verify)
Depends on: WP-0.5
Owned paths: `packages/py/qe_power/src/qe_power/textbook/**`, `packages/py/qe_power/tests/textbook/**`

This must be written **without reading the WP-0.6 code**. Its value is that it is independent.

Steps:

1. Build the bus admittance matrix (Y-bus) from the contract network, including line charging and off-nominal transformer taps.
2. Implement polar-form Newton-Raphson with an explicit Jacobian, using NumPy only (no pandapower).
3. Return results in the `loadflow-result` contract, with per-iteration mismatch history in the diagnostics.
4. Write the code to be read: comments link each step to the equation it implements.

Acceptance:

- `uv run pytest packages/py/qe_power/tests/textbook` passes.
- The Grainger and Stevenson 4-bus case from WP-0.8 matches the published solution within its rounding.
- Peter (or a local session with access to `~/QE-References/`) checks one worked load-flow example from his reference books against the solver and records the result, with book and page, in a `verified` log file. No book content is committed.

Learning note: `docs/learning/newton-raphson-load-flow.md`: Y-bus, the power equations, the Jacobian and convergence, derived step by step.
Change record:
- [!] Changed design | due to Peter authorizing Codex to correct current-based loading, while original was reserving WP-0.7 for a model independent of WP-0.6, as it was better for resolving the loading defect with a formula-derived regression test and a documented limited exception | Codex | 2026-10-08

- Changed design due to WP-0.8 replacing the case4gs fixture and no published case4gs solution being available, while original was validating Newton-Raphson against the Grainger and Stevenson case4gs results, as it was better for a fully owned analytic two-bus reference and a three-bus iteration-history test. (Copilot, 2026-10-08)

---

### WP-0.8 Reference fixtures

Status: [x] Done | implemented by Copilot | commit 62b8597 | 2026-10-08
Lane: B (implement), A (verify)
Depends on: WP-0.4
Owned paths: `tests/fixtures/power/**`, `examples/ieee14/**`

Steps:

1. Obtain the IEEE 14-bus case from the University of Washington Power Systems Test Case Archive (IEEE Common Data Format, which includes the solved voltages and angles). Record the URL, retrieval date and license in a source entry (`docs/sources/entries/uw-pstca-ieee14.yaml`).
2. Convert it to the contract network format with a small, committed script, so the conversion is reproducible.
3. Store the published solved voltages and angles as the reference solution, noting their rounding.
4. Package it as a runnable example project in `examples/ieee14/`.
5. Add MATPOWER's `case4gs` (the 4-bus example from Grainger and Stevenson, _Power System Analysis_) as a second, small fixture, with its published solution. Confirm the MATPOWER data license and record it in a source entry.

Acceptance:

- Both fixtures validate against the contracts.
- Each fixture folder has a `PROVENANCE.md` stating source, license, conversion steps and known modelling differences.

Learning note: `docs/learning/ieee-test-cases.md`.
Change record:

- Changed design due to source terms not permitting commercial CI use and case4gs having no published solution, while original was IEEE 14-bus and case4gs fixtures, as it was better for fully owned, redistributable fixtures with independent references. (Copilot, 2026-10-08)

---

### WP-0.9 Command line and report

Status: [x] Done | implemented by Claude | commit f160585 | 2026-10-08
Lane: A (implement), B (verify)
Depends on: WP-0.6, WP-0.8
Owned paths: `packages/py/qe_cli/**`, `packages/py/qe_report/**`

Steps:

1. Add the command `qe study run <project-folder> --study loadflow [--solver pandapower|textbook]`.
2. Write `results.json` (contract-shaped) and `report.md` into `<project-folder>/out/`.
3. The report contains: study summary, assumptions, bus voltage table, branch flow table, losses, convergence, diagnostics, provenance. Voltages outside 0.95 to 1.05 pu are flagged (limits configurable in the project).

Acceptance:

- `uv run qe study run examples/ieee14 --study loadflow` produces both files.
- The report opens and reads correctly in a Markdown viewer.

Learning note: `docs/learning/reading-a-load-flow-report.md`.
Change record:
- Changed design due to the project manifest contract having no field for voltage limits, while original was "limits configurable in the project", as it was better for avoiding a contract change in Phase 0: limits are set with --vmin and --vmax (default 0.95 and 1.05 pu) and stated in the report. A future Contract Change WP can add them to the manifest. (Claude, 2026-10-08)
- Changed design due to WP-0.8 replacing IEEE 14-bus with original fixtures and the example using project.json, which qe_core does not load, while original was "uv run qe study run examples/ieee14", as it was better for a runnable example: examples/fourteen_bus now has manifest.json, loadflow-request.json and an exact copy of the fixture network, guarded by a byte-equality test. The WP-0.8 fixture test now reads manifest.json. (Claude, 2026-10-08)
- Changed design due to the solvers not enforcing generator reactive limits, while original was a report without source outputs, as it was better for catching impossible operating points: the report back-calculates each source's P and Q from power balance and warns when Q limits are breached. (Claude, 2026-10-08)
- qe_power is now a proper workspace package (packages/py/qe_power/pyproject.toml) so qe_cli can depend on it. WP-0.6 adds pandapower to its dependencies. (Claude, 2026-10-08)

---

### WP-0.10 Integration and milestone M0

Status: [x] Done | implemented by Claude and Codex | commit a5a412f | 2026-10-08
Lane: P and A (implement), B (verify)
Depends on: WP-0.6, WP-0.7, WP-0.8, WP-0.9
Owned paths: `tests/integration/**`, `docs/milestones/M0.md`

Steps:

1. Add a cross-check test: pandapower and the textbook solver agree on IEEE 14-bus within 1e-6 pu and 1e-4 degrees.
2. Add a reference test: both agree with the published solution within its rounding (about 1e-3 pu and 0.05 degrees). Document any modelling differences rather than loosening tolerances to hide them.
3. Peter runs the CLI himself on a clean checkout and records the output in `docs/milestones/M0.md`.

Acceptance:

- CI runs both tests and passes.
- `docs/milestones/M0.md` contains Peter's run, the versions used and a short "what we learned".

Learning note: the milestone file itself.
Change record:
- Changed design due to WP-0.8 replacing IEEE 14-bus with original fixtures that have no published solution, while original was a pandapower and textbook cross-check on IEEE 14-bus plus agreement with its published solution (about 1e-3 pu and 0.05 degrees), as it was better for a fully owned reference: the cross-check (1e-6 pu, 1e-4 degrees) runs on every fixture in tests/fixtures/power, and the reference test uses the closed-form two_bus_analytic/reference.json. (Claude, 2026-10-08)

---

### WP-0.11 Phase 1 planning

Status: [x] Done | implemented by ChatGPT | commit 5c10723 | 2026-10-12
Lane: A (draft), B (review), Peter approves
Depends on: WP-0.10
Owned paths: `PLAN.md` (section 8 only)

Steps:

1. Expand Phase 1 into WPs in the same format as section 7: web UI workspace, single-line editor, API service, short circuit, cable sizing, motor start, protection plots, PDF report.
2. Assign lanes so parallel WPs own disjoint paths.
3. List the standards each study needs and which ones Peter must obtain.

Acceptance: `tools/check_plan` passes, and Peter approves.
Learning note: none.
Change record: none

---

## 8. Phase 1: power network workbench

Peter approved this scope and order on 2026-10-08. Execute WP-0.11, WP-1.1,
WP-1.2 and WP-1.3 serially, one PR each, merging only after green final-head CI.
Peter reopened the next motor-start prerequisite on 2026-10-10 by replying
"Proceed" after WP-1.3 completion. ChatGPT owns WP-1.8 (CC-2); WP-1.4
follows only after that Contract Change is complete. WP-1.5 through WP-1.7
remain planned and require the four-suite project-contract prerequisite.
Peter's 2026-10-11 Continue instruction reopens WP-0.11 to record ADR-0003's
architecture prerequisites and authorizes WP-1.9 (CC-3) next, serially after
WP-1.4. The updated WP-1.6 below records the generic canvas direction; its
implementation, WP-1.5 and WP-1.7 are still separate future work packages.
Shared paths below are protected by serial dependencies.

Every numerical WP has an independent, hand-derived reference with authored
inputs, equations and provenance. Do not use another solver's output as the
reference. Standard-derived values must come from a readable source, with a
pandapower documentation page cited in tests and a source-register entry.
Peter has not supplied IEC 60909-0; use the documented pandapower implementation
and state its assumptions and limitations, without claiming independent standards
certification. Missing documented constants or equipment data are diagnostics,
not opportunities to insert plausible values.

### WP-1.1 Generator reactive-limit enforcement

Status: [x] Done | implemented by ChatGPT | commit 936553e | 2026-10-08
Lane: B (ChatGPT implements)
Depends on: WP-0.11, WP-0.6, WP-0.10
Owned paths: `packages/py/qe_power/src/qe_power/adapters/pandapower/**`, `packages/py/qe_power/tests/adapters/**`

Steps:

1. Enforce generator `q_min_mvar` and `q_max_mvar` through pandapower PV to PQ switching. Emit an element-specific diagnostic for every generator at a reactive limit, stating the limit, actual Q and loss of voltage control.
2. Validate inconsistent limits and preserve existing convergence and provenance behavior. Omitted limits remain unbounded.
3. Restore 1.010 and 1.005 pu only in a temporary copy of the fourteen-bus case. Verify convergence, both Q caps, voltage relaxation and one diagnostic per affected generator. Leave committed fixtures unchanged.
4. Add an independent hand-derived two-bus reference for upper and lower limits, plus an unconstrained case. Cite the pandapower load-flow documentation for enforcement behavior.

Acceptance:

- `uv run pytest packages/py/qe_power/tests/adapters -v` passes, including the temporary fourteen-bus regression and independent upper/lower-limit reference.
- `uv run pytest` and all existing CI guards pass without relaxing tolerances.

Learning note: `docs/learning/generator-reactive-limits.md`, for an electrical engineer: PV/PQ equations, capability limits and why converged voltage may differ from the setpoint.
Change record: due to reactive-limit enforcement making legacy unconstrained comparisons solve different operating conditions, while original was adapter-only ownership with unchanged cross-solver tests, as it was better for preserving independent comparisons using temporary unbounded inputs without changing fixtures or tolerances | ChatGPT | 2026-10-08

---

### WP-1.2 Contract Change CC-1: short-circuit contracts

Status: [x] Done | implemented by ChatGPT | commit 8f0b89a | 2026-10-08
Lane: B (ChatGPT implements); Peter approved CC-1 in this session
Depends on: WP-1.1
Owned paths: `contracts/**`, `docs/specs/**`, `docs/decisions/ADR-0003-short-circuit-contracts.md`, `packages/py/qe_core/**`, `packages/py/qe_power/src/qe_power/adapters/pandapower/**`, `packages/py/qe_power/tests/adapters/**`, `examples/shortcircuit/**`

Steps:

1. Run this Contract Change alone. Add engine-neutral three-phase short-circuit request/result schemas, maximum/minimum cases, fault duration, per-bus Ik'', ip and Ith in kA, diagnostics and provenance. Define unsuccessful and partial-result semantics explicitly.
2. Add optional study inputs to the network: external-grid maximum/minimum short-circuit MVA and R/X, generator subtransient reactance and other documented nameplate/correction inputs, and line temperature where needed for minimum faults. Assess transformer vector group: three-phase faults use the positive-sequence network, so add it only if needed. Do not invent missing equipment values.
3. Bump affected schema versions for additive changes. Keep v0.1 load-flow projects readable, update core schema dispatch and project loading, and test both versions and invalid inputs. Load flow must explicitly account for study-only fields rather than issuing misleading unsupported-field errors.
4. Update specs, examples, schema validation and an ADR documenting units, impedance bases, compatibility and fault-study assumptions. WP-1.3 implements the new contracts in the solver, CLI and report; motor-start contracts require a separate approved Contract Change before WP-1.4.

Acceptance:

- `uv run python docs/specs/validate_examples.py` validates all documented examples.
- `uv run pytest packages/py/qe_core packages/py/qe_power/tests/adapters -v` passes, covering new schema constraints, version compatibility and a short-circuit project load.
- `uv run pytest` and existing CI guards pass. Review schema/spec/example consistency and Peter's explicit CC-1 authorization recorded in the start log.

Learning note: `docs/learning/short-circuit-inputs-and-contracts.md`, for an electrical engineer: fault level to Thevenin impedance, R/X, machine subtransient bases and the distinction between load-flow and fault inputs.
Change record: none

---

### WP-1.3 Three-phase short circuit via pandapower

Status: [x] Done | implemented by ChatGPT | commit 4d4847e | 2026-10-10
Lane: B (ChatGPT implements)
Depends on: WP-1.2
Owned paths: `packages/py/qe_power/src/qe_power/adapters/pandapower/**`, `packages/py/qe_power/tests/adapters/**`, `packages/py/qe_cli/**`, `packages/py/qe_report/**`, `tests/integration/test_shortcircuit.py`, `examples/shortcircuit/**`

Steps:

1. Implement balanced three-phase IEC 60909 calculations using pandapower. Return Ik'', ip and Ith at every bus for maximum and minimum cases, with explicit duration, voltage factor assumptions, diagnostics and solver/input provenance. Pandapower documents ip/Ith only for faults far from synchronous generators; unsupported near-generator duties must be unavailable with a diagnostic, never presented as verified values. Diagnose missing fault data, disconnected buses and unsupported modelling instead of silently choosing equipment data.
2. Verify against an independent hand-derived case: an infinite source through one transformer, Ik'' = c Un / (sqrt(3) |Z|). Derive c from a cited pandapower documentation page and state it in the test. Include the documented transformer correction in Z, derive ip and Ith from documented equations, and demonstrate a finite-source approximation converges to the infinite-source result without loosening tolerances.
3. Add `qe study run <project-folder> --study shortcircuit` and a runnable authored example. Validate results against CC-1 and include both maximum and minimum bus results.
4. Add a report section explaining Ik'', ip, Ith, units, duration, inputs and correction assumptions, maximum/minimum results, diagnostics and provenance. Preserve load-flow behavior.

Acceptance:

- `uv run pytest packages/py/qe_power/tests/adapters packages/py/qe_cli packages/py/qe_report tests/integration/test_shortcircuit.py -v` passes, including the hand-derived reference and invalid-input diagnostics.
- `uv run qe study run examples/shortcircuit --study shortcircuit` produces schema-valid `out/results.json` and readable `out/report.md` with maximum/minimum results at every bus.
- `uv run qe study run examples/fourteen_bus --study loadflow` still passes; `uv run pytest` and all CI guards pass.

Learning note: `docs/learning/three-phase-short-circuit.md`, for an electrical engineer: positive-sequence Thevenin circuit, voltage and transformer corrections, initial symmetrical/peak/thermal currents, and maximum versus minimum duties.
Change record: none

---

### WP-1.8 Contract Change CC-2: motor-start contracts

Status: [x] Done | implemented by ChatGPT | commit d043748 | 2026-10-10
Lane: B (ChatGPT implements); Peter authorized the next prerequisite on 2026-10-10
Depends on: WP-1.3
Owned paths: `PLAN.md`, `contracts/**`, `docs/specs/**`, `docs/decisions/ADR-0004-motorstart-contracts.md`, `packages/py/qe_core/**`, `examples/motorstart/**`

Steps:

1. Add engine-neutral motor-start request/result contracts with explicit shaft rating, efficiency, rated voltage and power factor, locked-rotor current ratio and power factor. The study adds one initially disconnected motor; it must not duplicate an existing network load.
2. Version the manifest additively and retain exact previous schemas. Motor inputs are study-local, leaving existing network contracts unchanged. Preserve v0.1 load flow and v0.2 short circuit.
3. Define bus voltage bases, signed relative dip, user limit, numerical status versus limit compliance, unavailable diagnostics and provenance. Validate cross-field invariants and motor bus references in core.
4. Update specs, an authored example and ADR. WP-1.4 is the explicit follow-up for adapter, CLI and reports; no claim of runnable motor-start solving in this Contract Change. Preserve ADR-0003's separate multi-domain manifest prerequisite before API/editor work.

Acceptance:

- `uv run python docs/specs/validate_examples.py` passes.
- `uv run pytest packages/py/qe_core -v` covers version dispatch, nameplate bounds, bus references, results and compatibility.
- Full workspace tests, Ruff and all existing CI guards pass on a clean checkout and final-head CI is green.

Learning note: `docs/learning/motorstart-contracts.md`, explaining nameplate bases, study-local equipment and unavailable results.
Change record: none

---

### WP-1.4 Motor-start voltage dip

Status: [x] Done | implemented by ChatGPT | commit 8e49106 | 2026-10-11
Lane: B (ChatGPT implements following CC-2)
Depends on: WP-1.3, WP-1.8
Owned paths: `packages/py/qe_power/motorstart/**`, `packages/py/qe_power/src/qe_power/motorstart/**`, `packages/py/qe_power/src/qe_power/adapters/pandapower/**`, `packages/py/qe_power/tests/motorstart/**`, `packages/py/qe_cli/**`, `packages/py/qe_report/**`, `examples/motorstart/**`

Steps:

1. Before implementation, obtain approval and completion of a separate Contract Change WP for motor inputs, requests/results and core dispatch. WP-1.4 itself does not own contracts.
2. Model the locked-rotor motor as impedance derived from shaft-rated kW, efficiency, rated power factor, locked-rotor current ratio and locked-rotor power factor. State voltage basis and distinguish rated and starting power factors; all nameplate values are user inputs.
3. Compare pre-start and locked-rotor voltages at every bus against a user-set dip limit. Report both voltages, dip definition, pass/fail, diagnostics and provenance. This is a steady locked-rotor check, not a dynamic acceleration study.
4. Derive an original two-bus source/line/motor case by complex voltage division; use its independent result as the reference test. Add CLI and report integration.

Acceptance:

- `uv run pytest packages/py/qe_power/tests/motorstart -v` passes with the hand-derived two-bus impedance reference and invalid nameplate-input tests.
- `uv run qe study run examples/motorstart --study motorstart` reports every bus and the selected dip limit.
- Full workspace tests and CI pass after the prerequisite Contract Change is complete.

Learning note: `docs/learning/motor-start-voltage-dip.md`, deriving rated current, locked-rotor impedance and complex voltage division.
Change record: none

---

### WP-1.9 Contract Change CC-3: multi-domain projects and asset identity

Status: [x] Done | implemented by ChatGPT | commit 5693c0e | 2026-10-11
Lane: B (ChatGPT implements); Peter authorized the documented next architecture prerequisite on 2026-10-11
Depends on: WP-1.4, WP-0.11
Owned paths: `contracts/**`, `docs/specs/**`, `docs/decisions/ADR-0005-multi-domain-projects.md`, `packages/py/qe_core/**`, `packages/py/qe_cli/**`, `packages/py/qe_report/**`, `examples/multi_domain/**`

Steps:

1. Run CC-3 alone. Introduce a versioned project manifest with stable model IDs, domain/model kinds, confined model files and study-to-model references. Replace the top-level single network binding with explicit per-study model selection, using a major manifest version for the incompatible shape. Archive v0.3 byte-for-byte and preserve v0.1/v0.2/v0.3 project loading and requests.
2. Add a project asset registry linking one stable physical asset ID to representations in multiple models. Keep identity outside domain engine imports. Validate duplicate IDs, model references and known power element references. Explicitly diagnose deferred validation of representations or payloads whose domain contracts do not exist yet; storage is not numerical validation or execution support.
3. Core loads project models without importing engines; executable power studies must bind to a power network and their request must name exactly that model file. CLI selects the study's model, never the first power model. Unknown/deferred model or study types must be preserved for storage and diagnosed/rejected for execution without blocking an unrelated supported power study. Preserve the single-network compatibility accessor only where unambiguous.
4. Update all current dependent packages in this PR. Add an authored mixed-domain project with at least two distinct power networks and a deferred non-power model; run all three power study types and preserve foreign content without lossy rewriting. Define model/study/asset identifier namespaces and input provenance boundaries in specs and ADR.
5. Verify schema/spec/example consistency, legacy projects, exact model routing, duplicate and dangling identifiers, unsupported execution, path traversal/absolute paths/symlinks and mismatched request/model files. No foreign engine or GUI is implemented in this Contract Change. Time-series and FMI-style co-simulation remain explicit later contracts.

Acceptance:

- `uv run python docs/specs/validate_examples.py` passes.
- `uv run pytest packages/py/qe_core packages/py/qe_cli -v` covers old/new versions, two-network routing, asset references, deferred models and path safety.
- Each supported study in `examples/multi_domain` runs through the CLI, returns its selected network ID and contract-valid results; a deferred study is rejected explicitly.
- Full workspace tests, Ruff, repository guards, plan/owned-path checker and final-head CI pass on a clean checkout.

Learning note: `docs/learning/multi-domain-projects-and-assets.md`, explaining model versus physical asset identity, version migration, study binding and storage versus execution.
Change record: none

---

### WP-1.5 Project study API

Status: [x] Done | implemented by ChatGPT | commit 76b801d | 2026-10-12
Lane: A (implement, after Peter reopens work)
Depends on: WP-1.4, WP-1.9
Owned paths: `packages/py/qe_api/**`, `pyproject.toml`, `uv.lock`, `tests/integration/test_api.py`, `tools/ci/check_repository.py`, `tools/ci/tests/test_guards.py`

Steps:

1. Add a FastAPI package exposing load flow, short circuit and motor start for a multi-domain project under a configured project root. Select the model through the study binding from CC-3; never assume one network per project. Reuse contract validation and solver entry points.
2. Validate paths, bound execution, return structured diagnostics and provenance, and preserve project data. Bind locally by default and document the trust boundary before remote use.
3. Document requests/responses and test all three studies, unknown studies, traversal, missing inputs and solver failures. Extend the existing import guard narrowly to let qe_api depend on domain/report packages as an orchestration layer, while preserving core/domain/engine isolation. Add a guard regression for this allowed layer and forbidden engine imports.

Acceptance:

- `uv run pytest packages/py/qe_api tests/integration/test_api.py -v` passes.
- An API request for each authored project returns contract-valid results and useful errors for invalid inputs; full workspace tests and CI pass.

Learning note: `docs/learning/study-api.md`, explaining the project-to-study boundary and traceable results.
Change record: due to the approved editor requiring validated model reads and saves, while original was a study-execution-only API, as it was better for providing one path-confined project boundary with stale-edit protection before the editor is built | ChatGPT | 2026-10-12

---

### WP-1.6 Generic diagram canvas and power workspace

Status: [x] Done | implemented by ChatGPT | commit e5c4d6c | 2026-10-12
Lane: B (implement, after Peter reopens work)
Depends on: WP-1.5, WP-1.9
Owned paths: `packages/ts/**`, `apps/web/**`, `package.json`, `pnpm-workspace.yaml`, `pnpm-lock.yaml`, `.github/workflows/web.yml`

Steps:

1. Establish a pnpm workspace with React, TypeScript and React Flow. Generate contract types and build a domain-neutral node/port/edge canvas with a power-specific symbol and connection-rule layer. Single-line diagrams are the first workspace; circuit, block-diagram and SCADA graphs must be possible without embedding their engines in the canvas. Ladder logic remains a separate grid component.
2. Read/write the selected model in a CC-3 multi-domain project without losing unedited electrical or foreign model/asset data. Keep presentation layout separate from engineering payloads and bind visual elements to model IDs and asset references. If persisted layout needs a new shared contract, complete a separate Contract Change before implementation; WP-1.6 does not own contracts. Validate edits and show element-specific diagnostics.
3. Call the FastAPI studies, show per-bus results and limits, and expose report download. Provide keyboard access, readable symbols/units and clear save/run state.
4. Test model/project round trips, edits, typed ports/connections, validation and API error/results flows. Test that the generic canvas does not hard-code electrical solver fields, and power rules remain in the power workspace.

Acceptance:

- `pnpm install --frozen-lockfile`, `pnpm --filter qe-web test` and `pnpm --filter qe-web build` pass in CI.
- A user can open an authored multi-domain project, select a power model, edit and save it, run its studies and inspect diagnostics/results without losing other models or asset bindings.

Learning note: `docs/learning/single-line-editor.md`, connecting diagram topology to electrical contracts and solver results.
Change record: none

---

### WP-1.7 PDF study reports

Status: [x] Done | implemented by ChatGPT | commit 71c98df | 2026-10-12
Lane: A (implement, after Peter reopens work)
Depends on: WP-1.6
Owned paths: `packages/py/qe_report/**`, `packages/py/qe_cli/**`, `packages/py/qe_api/**`, `pyproject.toml`, `uv.lock`, `tests/integration/test_pdf.py`

Steps:

1. Export load-flow, short-circuit and motor-start reports as PDF using a permissively licensed dependency. Preserve equations, units, assumptions, warnings and provenance.
2. Add CLI/API export, page breaks and readable multipage tables. Keep generated PDFs out of tracked source files and expose errors as diagnostics.
3. Test extracted report text, pagination on larger networks and failed/partial-study warnings; visually inspect all three reports.

Acceptance:

- `uv run pytest packages/py/qe_report tests/integration/test_pdf.py -v` passes.
- PDF export for each authored example produces readable pages with the same numerical results and diagnostics as Markdown; workspace tests and CI pass.

Learning note: `docs/learning/engineering-pdf-reports.md`, explaining reproducibility and what an engineer must include in a study deliverable.
Change record: none

### Deferred scope and source gaps

- Cable sizing is deferred: ampacity and installation/derating tables require a paid standard Peter does not yet have. Peter must identify and obtain the applicable standard and edition before a cable-sizing WP can be approved. Do not type remembered table values into tests or code.
- Protection coordination, scenario comparison and unbalanced studies need later approved WPs. IEC 60255-151 curve constants require readable sources before implementation.
- ADR-0003 controls the future suite sequence: after the first Power slice and shared infrastructure, Solar PV and Industrial Automation can proceed in separate engine lanes, then Electronics/Control/Multiphysics workspace by workspace. Detailed WPs are still required before any suite starts; no foreign engine implementation is authorized here. The IT track remains deferred under D6.

---

### WP-1.10 Phase 2 planning: solar PV and industrial automation

Status: [x] Done | implemented by ChatGPT and Claude | commit bf13a15 | 2026-10-14
Lane: B (ChatGPT drafts), Peter approves
Depends on: WP-1.7
Owned paths: `PLAN.md` (section 9 only)

Peter authorized this WP on 2026-10-13 ("continue with the pv and plc as suggested"), following ADR-0003 section 5 step 2.

Steps:

1. Expand section 9 into WPs in the same format as sections 7 and 8, for Suite 4 (Solar PV) and Suite 2 (Industrial Automation) as defined in `docs/decisions/ADR-0003-four-suites.md`.
2. Put shared prerequisites first: a Contract Change for time series and time-stepped studies (ADR-0003 section 3, items 3 and 4), then one Contract Change per suite for its model kind in the multi-domain project. Contract Changes run serially and alone.
3. After the Contract Changes, PV and PLC engine WPs must own disjoint paths so they can run in parallel, for example `packages/py/qe_pv/**` and `packages/py/qe_plc/**`, each with its own workspace in `apps/web` behind the generic canvas.
4. Each numerical or semantic WP names an independent reference with recorded provenance and a readable, free or owned source. List sources per WP, and list separately anything that needs a paid standard (for example IEC 61131-3, IEC 61724-1), stating how the WP proceeds without it.
5. Check every dependency licence. GPL code (for example OpenPLC runtime, MatIEC) may only run as a separate process, never be imported.
6. Keep the first slice of each suite small and end to end: input, engine, contract-valid result, report section, CLI and API run, a web view.

Acceptance: `tools/check_plan` passes, and Peter approves the section 9 plan in chat.
Learning note: none.
Change record: due to ChatGPT's planning branch being unreachable from GitHub (its environment had no authenticated gh), while original was Lane B ChatGPT drafting and merging alone, as it was better for landing ChatGPT's draft unchanged in substance with Claude's review revisions (WP-2.3 split, owned books cited, decision D11, cross-audit) in one reviewed PR | Claude | 2026-10-14

### WP-1.11 Contract Change CC-7: auditable calculation traces in results and reports

Status: [x] Done | implemented by Claude | commit 1be443e | 2026-10-14
Lane: A (Claude)
Depends on: WP-1.7
Owned paths: `contracts/power/shortcircuit-result.schema.json`, `contracts/power/motorstart-result.schema.json`, `contracts/v0.2/power/shortcircuit-result.schema.json`, `contracts/v0.3/power/motorstart-result.schema.json`, `docs/specs/shortcircuit-result.md`, `docs/specs/motorstart-result.md`, `docs/decisions/ADR-0006-calculation-traces.md`, `packages/py/qe_core/**`, `packages/py/qe_power/src/qe_power/adapters/pandapower/shortcircuit.py`, `packages/py/qe_power/src/qe_power/adapters/pandapower/motorstart.py`, `packages/py/qe_power/tests/**`, `packages/py/qe_report/**`, `packages/ts/contracts/**`, `apps/web/**`, `tests/integration/**`, `examples/shortcircuit/**`, `examples/motorstart/**`

Peter required on 2026-10-14 (decision D11) that results carry their working, after the Phase 1 audit dispute 2026-10-14-claude-WP-1.7-dispute.md.

Steps:

1. Additive Contract Change. Short-circuit result 0.2.0 to 0.3.0 adds an optional per-bus `trace`: nominal voltage, voltage factor, source voltage, the element impedances (formula, inputs and ohms referred to the fault bus) for single-source radial components, the Thevenin impedance R + jX at the fault bus, R/X, kappa and its method, m, n and the frequency used. Motor-start result 0.3.0 to 0.4.0 adds an optional `motor_trace`: rated current, locked-rotor current, impedance magnitude and angle, R and X, and the equivalent shunt. Archive the previous schemas byte for byte and keep validating them.
2. The adapters fill the traces from their own independent arithmetic: element impedances from the inputs (external grid Z_Q = c U_n^2 / S''_kQ, transformer Z_T = (u_k/100) U_rT^2 / S_rT with K_T, line (r' + j x') l with temperature correction, generator K_G (R_G + j X''_d)), summed along the radial path and referred by rated transformer ratios. That sum must agree with the engine's Thevenin impedance to a relative 1e-9, and Ik'' = c U_n / (sqrt(3) |Z_k|) must reproduce the engine current; otherwise the value is unavailable with a TRACE_MISMATCH diagnostic.
3. Reports (Markdown and PDF) gain a Method section with every governing equation and its book source, and a per-bus worked calculation showing each equation with the substituted numbers and the result. The load-flow report gains its method (bus power-balance equations, Newton-Raphson update, convergence test, branch flow, losses, loading and reactive-limit rule).
4. Use ASCII notation in reports (sqrt, kappa, ^) so PDF fonts render it.

Reference: Kasikci, Short Circuits in Power Systems, 1st ed 2002: eq. 9.3 p. 76 (K_G), eq. 9.14 p. 79 (K_T), eqs. 11.22 and 11.23 p. 98 (ip, kappa), eqs. 13.1 and 13.2 p. 117 (n, m), p. 12 (temperature factor); Fitzgerald, Electric Machinery, 6th ed 2003, section 6.6.2 pp. 333 to 334 (locked rotor); Glover, Power System Analysis and Design, 6th ed 2017, sections 6.4 to 6.6 (Newton-Raphson, PV buses).

Acceptance:

- `uv run pytest` passes, including tests that recompute each worked line of the example reports by hand from the inputs.
- `uv run qe study run examples/shortcircuit --study shortcircuit --report-format pdf` and the same for `examples/motorstart` produce reports whose worked calculations match the tables; old 0.2.0 and 0.3.0 results still validate; `pnpm generate:check` and CI pass.

Learning note: `docs/learning/auditable-calculation-traces.md`, explaining why a study must show its working and how to check a trace by hand.
Change record: none

### WP-1.12 Short-circuit cases unlocked from owned references

Status: [x] Done | implemented by Claude | commit 425b81d | 2026-10-14
Lane: A (Claude)
Depends on: WP-1.11
Owned paths: `packages/py/qe_power/src/qe_power/adapters/pandapower/shortcircuit.py`, `packages/py/qe_power/tests/**`, `packages/py/qe_report/**`, `tests/integration/test_shortcircuit.py`, `tests/integration/test_pdf.py`, `examples/shortcircuit/**`, `docs/learning/three-phase-short-circuit.md`

Steps:

1. Voltage factor (D10): c_min = 0.95 at LV for both tolerance classes; c_max stays 1.05 (+6%) and 1.10 (+10%). Exactly 1 kV stays unavailable, with the corrected reason: both owned books put 1000 V in the LV band but the engine applies MV factors at 1.0 kV.
2. K_T in the minimum case = 1: Kasikci ch. 9 p. 75 states the impedance corrections are needed above all for the greatest current and does not list them for the smallest; pandapower 3.5.6 cites IEC 60909-0:2016 clause 6.3.3 for the same rule; K_T = 1 gives the larger impedance, the conservative direction for minimum duty.
3. Thermal current from the book equation (Kasikci eq. 13.2 p. 117) in the adapter, with the request frequency (50 or 60 Hz) and the limit m = 2 at kappa = 2, replacing the engine's m = 0 shortcut and 50-Hz hardcode.
4. Line end temperature other than 20 C: R = R_20 (1 + 0.004 (theta_e - 20)), Kasikci p. 12.
5. Generator correction with unequal network and machine rated voltage (p_G = 0): K_G = (U_n/U_rG) c_max / (1 + x''_d sin phi_rG), Kasikci eq. 9.3 p. 76 and Das eq. 8.11. Nonzero p_G stays unavailable.
6. Meshed single-frequency components: peak current by method C (Kasikci p. 99: reactances at 20 Hz for 50 Hz, 24 Hz for 60 Hz), only where a hand-derived meshed reference agrees with the engine.
7. Each unlock has a hand-derived test with inputs, equations and the book page in the test docstring.

Acceptance:

- `uv run pytest packages/py/qe_power tests/integration/test_shortcircuit.py -v` passes with the new hand references.
- The example report shows the newly available values with their worked calculations; CI passes.

Learning note: `docs/learning/three-phase-short-circuit.md` (updated), explaining each decision and its source.
Change record: due to the method-C worked line living in qe_report and two tests using 60 Hz to force a partial result that this WP makes available, while original was owning only the adapter, its tests, the short-circuit integration test, the example and the learning note, as it was better for keeping each report line and test consistent with the new results (owned paths widened on main before implementation) | Claude | 2026-10-14

### WP-1.13 Pin the Node version for local web work

Status: [x] Done | implemented by Claude | commit d867c35 | 2026-10-14
Lane: A (Claude)
Depends on: WP-1.6
Owned paths: `apps/web/**`, `.nvmrc`, `package.json`, `.github/workflows/web.yml`

Steps:

1. Add `.nvmrc` with the CI Node major and an `engines` range in the root `package.json`; make CI read `.nvmrc`.
2. Make the web tests independent of the host's global `localStorage` (Node 25 and later define one that shadows jsdom's) by binding jsdom's storage in a test setup file.

Acceptance:

- `pnpm --filter qe-web test` passes under Node 24 and under Node 26; CI passes.

Learning note: none.
Change record: none

### WP-1.14 Short-circuit: 1 kV as LV and meshed networks with transformers

Status: [x] Done | implemented by Claude | commit 3d92db9 | 2026-10-14
Lane: A (Claude)
Depends on: WP-1.12
Owned paths: `packages/py/qe_power/src/qe_power/adapters/pandapower/shortcircuit.py`, `packages/py/qe_power/tests/**`, `packages/py/qe_report/**`, `tests/integration/test_shortcircuit.py`, `examples/shortcircuit/**`, `docs/learning/three-phase-short-circuit.md`

Peter ruled on 2026-10-14 (D12): 1 kV is low voltage, and meshed networks must work.

Steps:

1. The adapter supplies the voltage factors to the engine from its own table (D10, D12), so 1 kV takes LV factors and K_T and K_G use the same c_max. Check the applied factors per bus as before.
2. Extend the independent nodal solve to transformers, modelled by their rated ratio as an ideal transformer with the series impedance on the LV side, and to several external grids. Meshed and multi-source far-from-generator components then get ip and Ith by method C wherever our solve agrees with the engine at f and at fc.
3. Hand-derived tests for a 1 kV bus, a two-transformer mesh and a two-grid network.

Acceptance:

- `uv run pytest packages/py/qe_power tests/integration/test_shortcircuit.py -v` passes with the new hand references; CI passes.

Learning note: `docs/learning/three-phase-short-circuit.md` (updated).
Change record: none

### WP-1.15 Node 26

Status: [x] Done | implemented by Claude | commit 288c1d1 | 2026-10-14
Lane: A (Claude)
Depends on: WP-1.13
Owned paths: `.nvmrc`, `package.json`, `apps/web/README.md`, `apps/web/package.json`, `pnpm-lock.yaml`

Steps:

1. Set `.nvmrc` to 26 and `engines.node` to `>=26` (D13). CI already reads `.nvmrc`.
2. Upgrade `@playwright/test` to 1.63.0: browser installs before 1.60.0 hang on Node 26 (microsoft/playwright issues 40724 and 40998, Node bug nodejs/node#63487).

Acceptance:

- Web unit tests, build and e2e pass in CI on Node 26.

Learning note: none.
Change record: none

### WP-1.16 Workbench: no stale model request after switching project

Status: [x] Done | implemented by Claude | commit ff2fbc6 | 2026-10-14
Lane: A (Claude)
Depends on: WP-1.15
Owned paths: `apps/web/src/App.tsx`, `apps/web/tests/**`

Found on 2026-10-14 while running the workbench: after switching project, the page briefly requests the previous project's model ID from the new project (HTTP 404) before the new model list arrives.

Steps:

1. Clear the selected model when the project changes, and request a model only if it belongs to the loaded project.
2. Add a regression test that switches between two projects and asserts that no model is requested from the wrong project.

Acceptance:

- `pnpm --filter qe-web test` passes with the new test; CI passes.

Learning note: none.
Change record: none

---

## 9. Phase 2: solar PV and industrial automation

Drafted by ChatGPT (WP-1.10, 2026-10-13) and revised by Claude after review on 2026-10-14: WP-2.3 split into two packages, the owned PV and PLC books added as references, decision D11 (show the working) added to common acceptance, and the milestone audit made a cross-audit.

**Approved by Peter on 2026-10-14** ("write a prompt for ChatGPT to build something in phase 2 while you also build your own section"). Lanes, so both models work at once:

- Lane B (ChatGPT): WP-2.0, WP-2.1, then WP-2.3, WP-2.4 and WP-2.5 (shared infrastructure and the PV suite).
- Lane A (Claude): WP-2.8 now (PLC engine core, no contracts), WP-2.2 once WP-2.1 is Done, then WP-2.6 once WP-2.4 is Done.
- Contract Changes still run one at a time in the order 2.0, 2.1, 2.2. Root `pyproject.toml` and `uv.lock` are touched by WP-2.8 and WP-2.3 only; whoever merges second rebases and re-locks.

**Revised order, 2026-10-14, at Peter's direction (Claude main agent, ChatGPT co-agent, talking in `docs/agents/`):** WP-2.3 consumes CC-4, not CC-6, and its owned paths are disjoint from WP-2.2's, so it now depends on WP-2.1 and runs beside WP-2.2. WP-2.4 waits for both. New WP-2.9 (PLC process engine on CC-6, `qe_plc` only) lets Lane A work while Lane B does WP-2.4. Pairs that run together:

1. Claude WP-2.2 with ChatGPT WP-2.3.
2. Claude WP-2.9 with ChatGPT WP-2.4.
3. Claude WP-2.6 with ChatGPT WP-2.5.
4. WP-2.7: Claude audits PV, ChatGPT audits PLC.

**Research first, 2026-10-15, Peter's ruling:** building pauses while both models research the reference products in depth (WP-2.10, WP-2.11, then WP-2.12), for as long as it takes. In-progress engine WPs park on their branches.

**Approval gate (original wording):** This section is a proposed implementation plan. Merging the
WP-1.10 planning PR does not authorize its implementation. STOP after WP-1.10 and
ask Peter to approve section 9 in chat. No section 9 WP starts before that approval.
The requested sequence is to merge the checked planning draft, then obtain this
approval. Do not record approval as received until Peter actually gives it.

**First deliverables:** one fixed-tilt PV energy-yield study and one simulated
Structured Text motor-starter study. Each includes a validated CC-3 project,
engine, result, CLI/API run, Markdown/PDF report and web workspace. They reuse
shared infrastructure; `qe_pv` and `qe_plc` never import each other or `qe_power`.
There is no live PLC hardware control, full SCADA, ladder editor, detailed shading,
PV electrical installation design or coupled PV/power/PLC study in this slice.

**Order and lanes:**

| Order | WP | Deliverable | Execution |
| --- | --- | --- | --- |
| 1 | WP-2.0, CC-4 | Shared time-series and stepping contracts | Serial and alone |
| 2 | WP-2.1, CC-5 | PV site/system and yield-study contracts | Serial and alone |
| 3 | WP-2.2, CC-6 | PLC program/I/O and scan-study contracts | Serial and alone |
| 4 | WP-2.3 | Shared time runner and suite package seeding | Serial |
| 5 | WP-2.4 | Service routing, report registry and workspace scaffolding | Serial; shared files settled before suite lanes |
| 6a | WP-2.5 | PV engine and complete first web/CLI/API/report slice | Lane B (ChatGPT), disjoint suite paths |
| 5b | WP-2.9 | PLC process engine and CC-6 binding (`qe_plc` only) | Lane A (Claude), beside WP-2.4 |
| 6b | WP-2.6 | PLC interpreter, scan/process engine and complete first slice | Lane A (Claude), disjoint suite paths |
| 7 | WP-2.7 | Phase 2 milestone cross-audit | Each suite audited by the model that did not build it |

If only one implementer is available, execute 2.0 to 2.6 in order. With two
agents, 2.5 and 2.6 may run together after 2.4 merges. Each agent
still works on one WP at a time. Contract Changes never overlap one another or
another active contract consumer. Phase 1 auditing may continue on disjoint paths;
a Phase 1 fix and Phase 2 WP sharing a file must be serialized. No lane edits the
other lane's Status or files, root locks, shared registration files or contracts.

**References and provenance:** Every WP below names its reference. Record URL,
edition/version, access date, section/page, fixture origin, units, expected values,
tolerance rationale and input SHA-256 in its permitted new source entries and
fixture provenance. Published outputs and independently hand-derived equations
or state traces are references; a second call to the same tested implementation
is not. Read the source before taking a constant from it. Missing source values
produce an element/field diagnostic or a TODO naming the source, not a plausible
default. Test scenarios may use explicitly authored hypothetical inputs; never
present them as measured weather, manufacturer ratings or standards values.

**Source and dependency policy:**

| Source or dependency | Access/licence and intended use |
| --- | --- |
| [FMI 3.0.2 specification](https://fmi-standard.org/docs/3.0.2/) | Free specification, CC BY-SA 4.0; accompanying code is BSD-2. Cite lifecycle/variable/unit concepts and author our own protocol. No copied specification or FMU compatibility claim. |
| [Reda and Andreas, NREL/TP-560-34302, revised January 2008](https://docs.nlr.gov/docs/fy08osti/34302.pdf) | Free report; Appendix A.5 and Table A5.1, printed pp. A-15/A-16, provide the independent solar-position case. Citation and necessary test facts only. Do not redistribute the report or NREL C implementation. |
| [Dobos, PVWatts Version 5 Manual, NREL/TP-6A20-62641](https://docs.nlr.gov/docs/fy14osti/62641.pdf) | Free report and equations for the simple module/inverter reference. Record the applicable equation/page when implementing. Our study is a declared subset, not the whole PVWatts calculator. |
| [pvlib documentation](https://pvlib-python.readthedocs.io/en/stable/) and cited papers | pvlib is BSD-3-Clause and may be imported, confined to `qe_pv/adapters/pvlib/`. Pin the installed version and its documentation; use Python SPA, not the separately restricted NREL C source. Record each selected model's citation. A paywalled cited paper is not a readable source just because its citation is free. |
| Owned PV books in `Pietrols/QE-References` | Mertens, Photovoltaics: Fundamentals, Technology and Practice, 2nd ed (Wiley, 2019); Masters, Renewable and Efficient Electric Power Systems (Wiley, 2004); Gilman, SAM Photovoltaic Model Technical Reference (NREL/TP-6A20-64102, 2015); Stein, PV Performance Modeling Methods and Practices (IEA-PVPS T13-06:2017). Cite edition and page for solar geometry, transposition, temperature and loss equations. Duffie and Beckman is not in the library (catalogue gap); do not cite it until it is. |
| Owned PLC books in `Pietrols/QE-References` | Bolton, Programmable Logic Controllers, 6th ed (Newnes, 2015), written around IEC 61131-3 (Structured Text, timers, counters, scan); Petruzella, Programmable Logic Controllers, 3rd ed (McGraw-Hill, 2005). Cite chapter and page for language and timing semantics alongside the vendor pages. John and Tiegelkamp is a catalogue gap. |
| [Beckhoff TON](https://infosys.beckhoff.com/content/1033/tcplclib_tc2_standard/74406539.html), [TOF](https://infosys.beckhoff.com/content/1033/tcplclib_tc2_standard/74405003.html), [TP](https://infosys.beckhoff.com/content/1033/tcplclib_tc2_standard/74408075.html), [CTU](https://infosys.beckhoff.com/content/1033/tcplclib_tc2_standard/74400523.html), [CTUD](https://infosys.beckhoff.com/content/1033/tcplclib_tc2_standard/74402059.html) | Free vendor documentation, copyrighted. Read and cite behaviour; write original code and traces. Do not copy vendor source, figures or manuals. |
| [CODESYS Bus Cycle Task](https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_buscycle_task.html) and [ST expressions](https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_st_expressions.html), [IF](https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_st_instruction_if.html) and [assignment](https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_st_operator_assignment.html) help | Free vendor documentation for input capture, task execution, output transfer and supported language syntax. Cite semantics, not a redistribution licence for vendor software. |
| New Python dependencies | pvlib, NumPy, pandas and SciPy are BSD-3-Clause, checked against their package metadata. PLC uses our parser/interpreter and the Python standard library, with no new parser/runtime dependency. Review the exact locked distributions and transitive licences in WP-2.3. |
| Existing infrastructure | Reuse installed FastAPI/Pydantic, JSON Schema, units, React/React Flow and ReportLab dependencies. No new browser/chart dependency is required for this slice. Record exact licences for any newly resolved distribution before adding it. |
| OpenPLC runtime and MatIEC | GPL projects are optional later external comparisons only, executed as separate processes with documented version/licence. Never import, vendor or link their GPL code into our packages. Neither is required to pass Phase 2 acceptance. |
| Committed weather fixtures | First use small original synthetic scenarios, with an explicit CC0-1.0 data dedication and authorship recorded in `docs/sources/entries/` and the fixture provenance. This data-only policy does not decide the repository's deferred overall licence. Imported observations require readable redistribution terms before committing; a library's licence does not license its example/weather datasets. |

**Paid sources and how work proceeds without them:**

| Unavailable source | Affected WPs | Permitted first slice and excluded claim |
| --- | --- | --- |
| IEC 61724-1, PV performance monitoring | 2.1, 2.5, 2.7 | State weather provenance, sample coverage, model assumptions and energy units. Use declared energy accounting and the free numerical references. No IEC monitoring class, sensor requirement, standard performance-ratio compliance or certification claim. |
| IEC 61131-3, programmable-controller languages | 2.2, 2.6, 2.7 | Implement an explicitly specified ST subset and vendor-documented timers/counters/scan behaviour with original test traces. No full language, edition-specific conformance, vendor binary compatibility or certified PLC/safety claim. |
| Paid papers/textbooks cited by a model | Any WP using that model | Read an owned lawful copy if available, or use a freely readable model/equation. Record the gap and defer any unavailable constant. Peter is asked only for a scope/source decision, never to run acceptance commands. |

**Show the working (decision D11):** every Phase 2 result carries a trace of
its calculation, and every report states each governing equation with its
source, the substituted values and the result, as WP-1.11 does for Phase 1.
For PV this covers sun position, POA components, cell temperature, DC power,
inverter output, each loss stage and the energy integration for at least one
representative interval per report; for PLC, each scan's input image,
evaluated statements, timer and counter state and output image.

**Common acceptance:** Each implementer runs its named commands plus locked Python
sync, workspace tests, Ruff, text/reference/import-boundary guards and committed
plan/ownership checks. Any TS/web change also passes frozen pnpm install,
`pnpm generate:check`, web tests/build and applicable real API browser flows.
CI and Web must pass on the final PR head. No expected value or tolerance is
changed to hide a disagreement. All tests run offline, with no weather download,
remote solver, vendor login, hardware, paid tooling or secrets required.

### WP-2.0 Contract Change CC-4: shared time series and stepping

Status: [x] Done | implemented by ChatGPT | commit 84db0c8 | 2026-10-14
Lane: B, serial Contract Change
Depends on: WP-1.10
Owned paths: `contracts/common/time-series.schema.json`, `contracts/common/signal.schema.json`, `contracts/common/time-step.schema.json`, `contracts/studies/time-stepped-request.schema.json`, `contracts/studies/time-stepped-result.schema.json`, `packages/py/qe_core/src/qe_core/time_series.py`, `packages/py/qe_core/tests/test_time_series_contracts.py`, `packages/ts/contracts/**`, `docs/specs/time-series-and-stepping.md`

Steps:

1. Add independently versioned JSON Schema contracts for named typed signals with units, time-series samples, time-stepped requests/results and lifecycle messages. Map `initialise(t0)`, set/exchange named inputs, `step_to(t)`, read named outputs and termination to FMI initialization/Co-Simulation concepts. This is a Quantic protocol, not an FMI ABI/FMUs implementation.
2. Specify absolute UTC timestamps versus elapsed simulation time, explicit time origin/units, monotone advancement, requested and reached time, initialization/reset/error states and supported fixed-step boundaries. Define interval start/end versus instantaneous samples and unit-compatible connections. For first PLC runs, time must map exactly to declared integer-millisecond scan boundaries. Reject unsupported rollback, asynchronous event iteration and algebraic coupling; do not invent a full co-simulation master.
3. Define unique signal IDs, stable model/asset references, boolean/integer/real typing, dimensionless signals, missing-value status/diagnostics, finite-number rules, sample alignment and complete/partial/failed coverage. Missing is never zero. Provenance covers canonical requests/models and referenced data, with solver/model versions.
4. Write engine-free validators and original positive/negative fixtures. Preserve every existing schema byte-for-byte; any change to an existing contract requires a separately approved CC with archive/version/migration steps. Extend TS generation for the new schema types without changing existing public power types.

Reference: FMI 3.0.2 initialization, Co-Simulation `doStep`, variable causality/types and UnitDefinitions; independently authored state-transition and dimensional-consistency tables, linked in fixture provenance. No numerical engine is required.

Acceptance:

- `uv run pytest packages/py/qe_core/tests/test_time_series_contracts.py -v` passes for units, alignment, repeated/backward time, invalid signal types, missing samples, initialization and partial results.
- `pnpm generate:check` passes. Existing project/power contracts, fixtures and generated public types retain compatibility; all common acceptance checks pass.

Learning note: `docs/learning/time-series-and-stepping.md`, explaining time origins, sample meaning, units and the limited FMI-shaped lifecycle.
Change record: none

### WP-2.1 Contract Change CC-5: PV site, system and yield study

Status: [x] Done | implemented by ChatGPT | commit cbd328e | 2026-10-14
Lane: B, serial Contract Change
Depends on: WP-2.0
Owned paths: `contracts/pv/**`, `packages/py/qe_core/src/qe_core/multidomain.py`, `packages/py/qe_core/src/qe_core/pv_contracts.py`, `packages/py/qe_core/tests/test_pv_contracts.py`, `packages/ts/contracts/**`, `docs/specs/pv-site-and-yield.md`

Steps:

1. Specify a `pv.site` model and `pv.yield` request/result inside the existing CC-3 manifest, with model IDs and asset representations for site, fixed-tilt array, modules and inverter. Use the manifest's current open model/study kinds; do not fork or replace its schema.
2. Require coordinates/elevation, orientation convention, explicit module rating/temperature coefficient, temperature-model input, inverter ratings/efficiency parameters, albedo and named loss fractions. Distinguish module reference DC rating from inverter DC input limit. Missing required engineering inputs receive field diagnostics, never fabricated equipment defaults.
3. Bind local weather files through safe project paths and CC-4 series, including irradiance components, air/cell temperature as required by the selected model, interval semantics, timezone/calendar and data provenance. Record source hash, synthetic/observed classification, validity and coverage. Define per-step sun position/POA/DC/AC/loss outputs and covered-period/monthly/annual energy; incomplete years cannot claim an annual total.
4. Add pure domain registration/validation, reference checks and mixed-domain round-trip fixtures. Other model files, assets and all existing contracts remain unchanged. Contract fixtures use explicitly authored hypothetical inputs and validation tables, not unverified datasheet constants.

Reference: CC-3 binding rules and CC-4 unit/time tables; free pvlib solar-position, isotropic irradiance, Ross cell-temperature and PVWatts DC/inverter documentation; Dobos's manual. Independent dimensional, rating-distinction and calendar-coverage cases have recorded provenance. IEC 61724-1 claims remain excluded.

Acceptance:

- `uv run pytest packages/py/qe_core/tests/test_pv_contracts.py packages/py/qe_core/tests/test_multidomain.py -v` passes, including broken assets/files, incompatible units, missing inputs and incomplete-year coverage.
- New JSON payloads and TS types round-trip without modifying power/PLC/foreign data; `pnpm generate:check` and all common acceptance checks pass.

Learning note: `docs/learning/pv-contracts-and-energy-accounting.md`, explaining site inputs, sample coverage and power versus energy.
Change record: none

### WP-2.2 Contract Change CC-6: PLC program, I/O and scan study

Status: [x] Done | implemented by Claude | commit 8102e01 | 2026-10-14
Lane: A or B, serial Contract Change
Depends on: WP-2.1
Owned paths: `contracts/automation/**`, `packages/py/qe_core/src/qe_core/multidomain.py`, `packages/py/qe_core/src/qe_core/plc_contracts.py`, `packages/py/qe_core/tests/test_plc_contracts.py`, `packages/ts/contracts/**`, `docs/specs/plc-program-and-scan.md`, `docs/specs/structured-text-subset.md`

Steps:

1. Specify `automation.plc` models and `plc.scan` requests/results within CC-3, retaining its manifest and stable asset IDs. Define program source, typed variables and initial values, function-block instances, digital I/O names/directions, one cyclic task, scan period, run duration and scheduled input events.
2. Freeze a deliberately bounded ST grammar: BOOL/INT/REAL/TIME declarations, literals, assignment, declared expression operators/precedence, IF/ELSIF/ELSE and named timer/counter calls. Define integer range/overflow, TIME precision, initialization/reset, persistent state between scans and invalid-program diagnostics with line/column. Unsupported loops, functions, pointers, multitasking and vendor extensions are diagnosed, never silently executed.
3. Define TON/TOF/TP and CTU/CTUD state inputs/outputs, reset/load/edge rules, timer elapsed time, invocation order and sampling convention. Resolve ambiguous simultaneous events and mid-pulse parameter changes as explicit Quantic subset choices, with vendor citations and declared limitations, not alleged IEC requirements.
4. Define the motor-starter process as an authored discrete transition table: start/stop command, permissive, overload/trip, contactor feedback and running state. State exact boundary ordering: capture input image, execute statements/blocks in order, commit output image, advance the process to the next scan. No electrical motor dynamics or safety certification is implied.
5. Add CC-4 trace/result bindings, per-scan status, diagnostics, event source and provenance, pure domain/asset validation and original mixed-project fixtures. Preserve existing contracts and power behaviour.

Reference: Beckhoff TON/TOF/TP/CTU/CTUD documentation and CODESYS Bus Cycle Task/ST syntax help; independent handwritten timing/edge/scan/process tables. Every unspecified vendor corner case is identified before freezing the subset. IEC 61131-3 is unavailable; no full conformance claim.

Acceptance:

- `uv run pytest packages/py/qe_core/tests/test_plc_contracts.py packages/py/qe_core/tests/test_multidomain.py -v` passes for invalid I/O binding/types, scan/event alignment, timer presets, duplicate instances and trace coverage.
- The grammar and independent reference traces are documented, new TS types regenerate, mixed-project preservation and all common acceptance checks pass.

Learning note: `docs/learning/plc-contracts-and-scan-images.md`, explaining typed programs, scan snapshots, state and declared subset limits.
Change record: none

### WP-2.3 Shared time runner and suite package seeding

Status: [x] Done | implemented by ChatGPT | commit af42263 | 2026-10-14
Lane: B, shared infrastructure; runs beside WP-2.2 (disjoint paths, consumes CC-4 only)
Depends on: WP-2.1
Owned paths: `packages/py/qe_core/src/qe_core/stepping.py`, `packages/py/qe_core/tests/test_stepping.py`, `packages/py/qe_pv/**`, `pyproject.toml`, `uv.lock`, `tools/ci/check_repository.py`, `tools/ci/tests/test_guards.py`, `tools/ci/README.md`

Steps:

1. Implement CC-4 lifecycle and deterministic fixed-step execution in the core, using original mock engines. Exchange only typed named signals; reject invalid ordering/units and unsupported coupled systems. Preserve requested/reached time, failure diagnostics and bounded work. No domain imports into core.
2. Seed the installable `qe_pv` package with a documented engine interface and explicit ENGINE_UNAVAILABLE diagnostics (WP-2.8 has already created `qe_plc`). Add `qe_pv` and the reviewed pvlib dependency to the locked workspace configuration. Stub behaviour is not a simulated result or a completed suite.
3. Extend boundary checks narrowly: domains may depend only on core, never one another; pvlib imports occur only inside `qe_pv/adapters/pvlib/`. Exercise negative guard fixtures. Do not edit `qe_power` or existing contracts.
4. Record exact dependency and transitive licence checks and version pinning.

Reference: CC-4 state tables and independently derived mock scan/interval traces, plus FMI lifecycle concepts.

Acceptance:

- `uv run pytest packages/py/qe_core/tests/test_stepping.py tools/ci/tests -v` passes, including incompatible units, unavailable engines, forbidden imports and bounded work.
- Frozen install and the full Python suite pass; all common acceptance checks pass.

Learning note: `docs/learning/phase2-time-runtime.md`, explaining the stepping lifecycle and isolated engines.
Change record: none

### WP-2.4 Service routing, report registry and workspace scaffolding

Status: [x] Done | implemented by ChatGPT | commit e3a56b6 | 2026-10-15
Lane: B, serial shared infrastructure; runs beside WP-2.9
Depends on: WP-2.2, WP-2.3
Owned paths: `packages/py/qe_api/**`, `packages/py/qe_cli/**`, `packages/py/qe_report/src/qe_report/__init__.py`, `packages/py/qe_report/src/qe_report/registry.py`, `packages/py/qe_report/src/qe_report/pv/**`, `packages/py/qe_report/src/qe_report/plc/**`, `packages/py/qe_report/tests/test_report_registry.py`, `packages/ts/contracts/**`, `apps/web/**`, `pnpm-lock.yaml`, `.github/workflows/web.yml`, `tests/integration/test_phase2_routing.py`, `tools/ci/check_repository.py`, `tools/ci/tests/test_guards.py`, `tools/ci/README.md`, `uv.lock`

Steps:

1. Establish explicit allowlisted model/study handlers and atomic save validation in CLI/API, pure report dispatch and workspace selection in the existing web shell. Keep loopback/origin/path/body/etag restrictions and killable worker limits. Time-series file access is confined and bounded; no arbitrary import string or filesystem execution comes from project data. Preserve the existing power routes and Markdown/PDF flows.
2. Seed suite-local API/CLI/report/web entry points for PV and PLC that report ENGINE_UNAVAILABLE until the engines land. Extend the import guard narrowly so API orchestration may call the two new domain packages.
3. Seed `apps/web/src/workspaces/pv/` and `plc/` components and suite test/e2e directories. Generic canvas handles graphs/ports; ST is a text editor plus process/I/O graph, never a ladder grid disguised as a graph. Route suite-local browser tests through shared CI without requiring unavailable engines.
4. Place future suite implementations entirely under the disjoint paths granted to 2.5/2.6. No contract edits and no further root/lock/shared-shell edits in the parallel engine WPs.

Reference: CC-5/CC-6 routing/validation fixtures. Reuse the existing API/browser tests as preservation evidence, not as the new engine's reference.

Acceptance:

- `uv run pytest packages/py/qe_report/tests/test_report_registry.py tests/integration/test_phase2_routing.py -v` passes, including kill/release limits, unavailable handlers, schema routing and foreign-file preservation.
- Generated types, full Python/web tests, build and existing real power browser flows pass. Stub workspaces report unavailable engines correctly. Owned-path sets for 2.5/2.6 have zero intersection; all common acceptance checks pass.

Learning note: `docs/learning/phase2-routing.md`, explaining common execution infrastructure and how a suite plugs in.
Change record: due to step 2 requiring the API import-guard extension and the new API/CLI domain dependencies, while original Owned paths omitted `tools/ci/check_repository.py`, `tools/ci/tests/test_guards.py`, `tools/ci/README.md` and `uv.lock`, as it was better for keeping the guard and lock in the same WP as the code they cover (granted by Claude as main agent at Peter's direction, no scope change) | Claude | 2026-10-15; due to PR #51 being merged before the required import guard and dependency metadata were completed, while original was one fully completed PR per WP, as it was better for completing approved routing infrastructure in a follow-up on the existing branch before either engine lane starts | ChatGPT | 2026-10-15

### WP-2.5 Solar PV first end-to-end yield slice

Status: [ ] Not started
Lane: B, PV engine/workspace; may overlap only WP-2.6
Depends on: WP-2.4
Owned paths: `packages/py/qe_pv/**`, `packages/py/qe_api/src/qe_api/pv/**`, `packages/py/qe_cli/src/qe_cli/pv/**`, `packages/py/qe_report/src/qe_report/pv/**`, `packages/py/qe_report/tests/pv/**`, `apps/web/src/workspaces/pv/**`, `apps/web/tests/pv/**`, `apps/web/e2e/pv/**`, `tests/fixtures/pv/**`, `tests/integration/pv/**`, `examples/pv/**`

Steps:

1. Implement a pvlib adapter for the fixed-tilt `pv.yield` study: Python SPA sun position, direct beam plus isotropic sky and ground-reflected POA, an explicit Ross or supplied cell-temperature input, simple PVWatts DC/module and inverter models, clipping and a basic named loss chain. Declare simplifications and each stage's units/order. Module, inverter, temperature, albedo and loss inputs are required or explicitly sourced, never unexplained library defaults.
2. Read only local validated weather. Commit a small authored day fixture and a compact complete-year hourly fixture with the declared data licence, authorship, file hash and interval/calendar provenance. Test data are synthetic and labelled as such. Real user files are supported locally but never committed without recorded redistribution rights. Tests/download-free acceptance never call pvlib online iotools or remote weather services.
3. Write independent references before or alongside the adapter: the published SPA Appendix A.5/Table A5.1 case with its actual inputs/outputs, hand-derived POA cases, Ross temperature/DC/inverter equation cases and loss/integration arithmetic. Store derivations and fixed tolerance rationale without calling pvlib to produce expected values. Required published constants come from the readable NREL report/documented model. If an inaccessible source is required, diagnose/defer that model.
4. Integrate covered-period and monthly energy from actual interval durations; report annual yield only for complete validated calendar coverage. Test leap years, timezone/UTC conversion, interval means versus instants, dark hours, clipping, missing/nonfinite samples and mixed-project asset preservation. Do not annualize a short series or fill missing irradiance with zero. A synthetic year's result is a scenario yield, not a weather prediction for Kitwe or any real site.
5. Implement the pre-registered suite handlers and pure report modules: CLI study selection/exit codes, bounded API request/result, equations/units/inputs/loss stages/assumptions/coverage/diagnostics/provenance in Markdown and existing PDF export. Hash weather content as well as model/request. Source gaps and partial results remain visible.
6. Provide a generic-canvas PV workspace showing site/array/inverter graph, model/weather selection, validated property edits, loss/energy summary and unit-labelled time-series view. Run and download the same study through the existing API; test edits/save/assets, invalid input and study errors. No geometric roof CAD, shading mesh, electrical cable sizing, bankability or IEC compliance feature is inferred.

Reference: Reda/Andreas revised-2008 SPA Table A5.1 (pp. A-15/A-16); Dobos PVWatts Version 5 equations; owned Mertens 2nd ed 2019 and Gilman 2015 for transposition, temperature and loss equations, cited by page; pvlib [isotropic](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.irradiance.isotropic.html), [Ross](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.temperature.ross.html), [DC](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.pvsystem.pvwatts_dc.html) and [inverter](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.inverter.pvwatts.html) equations and their cited papers. Ross's fixed-wind/slowly-changing-irradiance assumptions are explicitly reported. Independently derive limiting cases and energy/loss accounting. IEC 61724-1 remains a stated gap.

Acceptance:

- `uv run pytest packages/py/qe_pv packages/py/qe_report/tests/pv tests/integration/pv -v` passes offline against the independent references and all invalid/partial cases.
- CLI and API execute the committed PV example; full-year energy matches independently summed interval energy within the recorded tolerance. `pnpm --filter qe-web test -- tests/pv` and `pnpm --filter qe-web exec playwright test e2e/pv` pass with a real API worker.
- Inspect the web view and rendered report/PDF, including warnings/units/coverage/provenance. Other model/asset files are unchanged; all common acceptance checks pass. No root locks, shared handlers, power paths or contracts changed.

Learning note: `docs/learning/pv-first-yield-study.md`, explaining solar geometry, POA, temperature, loss order, clipping and energy coverage.
Change record: none

### WP-2.6 Industrial automation first end-to-end scan slice

Status: [ ] Not started
Lane: A, PLC engine/workspace; may overlap only WP-2.5
Depends on: WP-2.4, WP-2.9
Owned paths: `packages/py/qe_plc/**`, `packages/py/qe_api/src/qe_api/plc/**`, `packages/py/qe_cli/src/qe_cli/plc/**`, `packages/py/qe_report/src/qe_report/plc/**`, `packages/py/qe_report/tests/plc/**`, `apps/web/src/workspaces/plc/**`, `apps/web/tests/plc/**`, `apps/web/e2e/plc/**`, `tests/fixtures/plc/**`, `tests/integration/plc/**`, `examples/plc/**`

Steps:

1. Write our own bounded ST lexer/parser/typed interpreter for exactly the CC-6 subset. Never use Python `eval`/`exec`, transpile arbitrary input or launch a shell from program text. Diagnose unsupported syntax, unknown names, type mismatches, divide-by-zero, overflow and execution/resource limits with source location and element/field references.
2. Implement deterministic input-image capture, ordered program/block calls and output-image commit on each scan, with persistent variables/block state and declared reset behaviour. Simulated time, not wall-clock speed, drives TON/TOF/TP and CTU/CTUD. Honour CC-6's timing, edge, saturation/overflow and precedence choices, documenting their limits.
3. Author independent expected scan tables from the free vendor timing/scan documentation before or alongside the interpreter. Cover preset boundaries, zero preset, held/pulsed inputs, timer cancellation and off delay, TP input changes, counter held edges/reset/load/simultaneous events, invocation order and scan-boundary input events. Distinguish vendor-documented behaviour from our declared subset choices; never claim these tests certify IEC 61131-3.
4. Implement one authored discrete motor-starter process with permissive/interlock, stop and overload/trip events plus contactor/running feedback, using CC-6's explicit transition table and scan ordering. Assert interlocks at every step, one-scan feedback timing and deterministic replay. Parameters are explicit fictional scenario inputs, not guessed machine constants or a model of safety-rated hardware.
5. Implement suite-local CLI/API/report handlers: validated contract trace, scan counts and reached time, states/I/O/timer/counter tables, unsupported features, process assumptions, diagnostics, source and program/model/input hashes. Existing Markdown/PDF export preserves semantic failures and partial traces; bounded worker execution never controls real equipment or writes unselected files.
6. Provide an ST text editor and generic-canvas I/O/controller/motor process view with typed ports, input-event controls and a unit-labelled scan timeline. Editing validates/saves the selected model, running shows the same trace as CLI/API, and downloads expose report/provenance. Ladder logic, multitask/fieldbus runtime, full HMI/SCADA, analog process dynamics and hardware deployment remain deferred.

Reference: Beckhoff TON/TOF/TP/CTU/CTUD pages, CODESYS Bus Cycle Task/ST help and Bolton 6th ed 2015 (cited by chapter and page), translated into original independently handwritten scan traces; the authored motor-starter transition table is the process reference. Record source versions/access dates and corner-case conventions. No GPL runtime dependency and no paid IEC 61131-3 conformance claim.

Acceptance:

- `uv run pytest packages/py/qe_plc packages/py/qe_report/tests/plc tests/integration/plc -v` passes offline with exact integer-time/boolean/counter reference traces and justified real-number tolerances where needed.
- CLI/API reproduce the motor-starter example and intentional syntax/interlock/timer failures with bounded work. `pnpm --filter qe-web test -- tests/plc` and `pnpm --filter qe-web exec playwright test e2e/plc` pass with a real API worker.
- Inspect the process view and report/PDF; unsupported semantics and source gaps are visible. Input/program/foreign model files remain unchanged after runs; all common acceptance checks pass. No shared/root/power/contract files changed.

Learning note: `docs/learning/plc-first-scan-and-process-study.md`, explaining ST evaluation, scan images, timer/counter state and discrete interlocks.
Change record: none

### WP-2.7 Phase 2 milestone cross-audit

Status: [ ] Not started
Lane: Cross-audit: the PV slice is audited by the model that did not build it, and the PLC slice likewise
Depends on: WP-2.5, WP-2.6
Owned paths: `tests/integration/phase2_audit/**`

Steps:

1. Follow AGENTS.md section 4 on a clean checkout. Independently rerun both suites' acceptance, schema/asset/unit/time validation, mixed-project save preservation, bounded API/browser flows and report/PDF comparisons. Recheck SPA/equation references and handwritten PLC traces from their primary sources, not just pasted CI output.
2. Check weather licences/hashes, offline test operation, module/inverter/loss assumptions, calendar coverage, timer/counter/scan boundaries, source gaps, dependency licences, domain/import boundaries and that every report shows its working (D11). Verify the two engine WP path sets are disjoint and no Phase 1 or frozen contract changes slipped in.
3. Record the milestone audit in an `audit` log and `dispute` logs for failures. Do not repair unowned files; a fix needs an approved WP with explicit paths.

Reference: Reproduce the published SPA case, hand-derived PV equations/energy totals and vendor-derived PLC/process trace tables independently. No second invocation of the suite under audit substitutes for its reference.

Acceptance:

- `uv run pytest tests/integration/phase2_audit -v`, both suite acceptance sets, full offline workspace/web checks and CI pass on the audit head; all disputes are closed with rerun evidence.
- STOP at this milestone. Do not begin coupled engines, detailed PV/PLC features, Suite 3 or deeper Phase 1 work without a newly approved planning or fix WP.

Learning note: none.
Change record: none

### WP-2.8 PLC Structured Text engine core

Status: [x] Done | implemented by Claude | commit 951a2d8 | 2026-10-14
Lane: A (Claude), runs now in parallel with Lane B's WP-2.0 and WP-2.1
Depends on: WP-1.10
Owned paths: `packages/py/qe_plc/**`, `pyproject.toml`, `uv.lock`, `docs/specs/structured-text-subset.md`

Steps:

1. Create the `qe_plc` workspace package: our own lexer, parser and typed interpreter for a bounded Structured Text subset (BOOL, INT, REAL, TIME; literals; assignment; arithmetic, comparison and boolean operators with stated precedence; IF/ELSIF/ELSE). Never `eval`, `exec` or a shell. Unsupported syntax, unknown names, type mismatches, divide-by-zero and INT overflow are diagnostics with line and column.
2. Function blocks TON, TOF, TP, CTU, CTD and CTUD with persistent instance state, driven by simulated time.
3. A scan engine: capture the input image, execute the program, commit the output image, advance simulated time by the scan period. Each scan returns a trace (D11): input image, each assignment with its evaluated value, timer and counter state, output image.
4. Write `docs/specs/structured-text-subset.md` freezing the grammar and the timer and counter semantics, with sources. WP-2.2 (CC-6) builds its contract on it; until then the engine has no JSON contract.

Reference: Bolton, Programmable Logic Controllers, 6th ed (Newnes, 2015) and Petruzella, 3rd ed (2005) for ST and timer and counter behaviour, cited by chapter and page; Beckhoff TC2_Standard TON/TOF/TP/CTU/CTUD pages. Independent handwritten scan traces for every block.

Acceptance:

- `uv run pytest packages/py/qe_plc -v` passes against the handwritten traces; the full suite, ruff and guards pass; CI passes.

Learning note: `docs/learning/plc-scan-cycle-and-structured-text.md`, explaining the scan cycle, the input and output images, and each timer and counter with timing diagrams in text.
Change record: none

### WP-2.9 PLC process engine and CC-6 binding

Status: [x] Done | implemented by Claude | commit 2dd3b56 | 2026-10-14
Lane: A (Claude), runs beside Lane B's WP-2.4
Depends on: WP-2.2
Owned paths: `packages/py/qe_plc/**`, `tests/fixtures/plc/**`

Steps:

1. Bind the WP-2.8 engine to CC-6: load an `automation.plc` model and a `plc.scan` request, validate them, run, and return a contract-valid `plc.scan` result with the per-scan trace, provenance (engine version, program/model/request hashes) and diagnostics with element/field references.
2. Implement the CC-6 authored motor-starter transition table as a discrete process model advanced after each output-image commit, with permissive/interlock, stop, overload/trip and contactor/running feedback arriving one scan later.
3. Commit the motor-starter fixture project and handwritten expected scan tables, including interlock refusal, overload trip, stop priority and deterministic replay.

Reference: the CC-6 transition table and scan ordering in `docs/specs/plc-program-and-scan.md`; Bolton 6th ed 2015 pp. 106 to 107 (mass I/O copying); independent handwritten scan tables.

Acceptance:

- `uv run pytest packages/py/qe_plc -v` passes against the handwritten tables; results validate against the CC-6 schemas; full suite, ruff and guards pass; CI passes. No API, CLI, report, web, contract or root lock changes.

Learning note: `docs/learning/plc-motor-starter-process.md`, explaining the process model, one-scan feedback and interlocks.
Change record: none

### WP-2.10 Power reference-product research: ETAP and PowerFactory

Status: [x] Done | implemented by Claude | commit d03d811 | 2026-10-17
Lane: A (Claude); research only, no code
Depends on: WP-1.10
Owned paths: `docs/research/power/etap.md`, `docs/research/power/powerfactory.md`, `docs/research/power/notes/**`

Steps:

1. Read every public ETAP and DIgSILENT PowerFactory source that can be found: product and module pages, brochures, published user manuals and help, release notes, technical references, webinars, papers and user articles.
2. Write one dossier per product following `docs/research/power/README.md`, citing every claim, paraphrasing only.

Reference: the sources listed in each dossier.

Acceptance:

- Both dossiers cover every template section, every claim cites a numbered source, the gaps list is explicit, text and reference guards pass.

Learning note: none.
Change record: none

### WP-2.11 Power reference-product research: PowerWorld Simulator

Status: [x] Done | implemented by ChatGPT | commit 7c0b9e0 | 2026-10-15
Lane: B (ChatGPT); research only, no code
Depends on: WP-1.10
Owned paths: `docs/research/power/powerworld.md`

Steps:

1. Read every public PowerWorld Simulator source: product and add-on pages, the online help, release notes, training material, papers and user articles.
2. Write the dossier following `docs/research/power/README.md`, citing every claim, paraphrasing only.

Reference: the sources listed in the dossier.

Acceptance:

- The dossier covers every template section, every claim cites a numbered source, the gaps list is explicit, text and reference guards pass.

Learning note: none.
Change record: none

### WP-2.12 Power parity matrix and engine inventory

Status: [ ] Not started
Lane: A (Claude), with ChatGPT review
Depends on: WP-2.10, WP-2.11
Owned paths: `docs/research/power/parity-matrix.md`, `docs/research/power/engines.md`

Steps:

1. Merge the dossiers (ETAP, PowerFactory, PowerWorld and, since 2026-10-16, the WP-2.13 competitors) into one capability matrix with our current status and the owned book that will verify each row.
2. List every calculation engine the products imply, which we have, which we lack, and the owned books that cover each.
3. Tag every product cell and engine claim with one evidence class (Peter, 2026-10-17): **S** seen (stated in a cited primary source or observed in the product), **I** inferred (our reasoning from cited evidence), **U** unknown (not established; unknown is not absent).
4. Cite the WP-2.14 R-IDs that each row depends on.

Reference: the dossiers, `reconstruction-requirements.md` and the owned library catalogue.

Acceptance:

- Every dossier capability appears in the matrix; every product cell carries S, I or U; every engine row names its sources; ChatGPT has reviewed it in the channel.

Learning note: none.
Change record: none

### WP-2.13 Power reference-product research: industrial and transmission competitors

Status: [x] Done | implemented by ChatGPT | commit a8c3efee75b303ba7bb2c41d569a826585a0c79a | 2026-10-16
Lane: B (ChatGPT); research only, no code
Depends on: WP-1.10
Owned paths: `docs/research/power/other-products.md`

Added 2026-10-16 on Peter's chat instruction to continue the research phase. It covers
the products a Copperbelt mine or consultancy compares with ETAP: EasyPower, SKM
PowerTools, NEPLAN and Siemens PSS/E.

Steps:

1. For each product, read the public sources: product and module pages, help or user
   manuals, release notes, licence and pricing pages, training material, validation
   papers and dated user reports.
2. Write one dossier following `docs/research/power/README.md`, with one section per
   product, citing every claim and paraphrasing only. Use the shared matrix row IDs
   (D, G, S, F, P, A, M, T, H, C), and add product-specific rows only where needed.
3. Keep the WP-2.11 evidence discipline: unknown is not absent, vendor claims stay
   vendor claims, and dated prices are observations, not quotes.

Reference: the sources listed in the dossier.

Acceptance:

- The dossier covers every template section for each product, every claim cites a
  numbered source, the gaps list is explicit, and the text and reference guards pass.

Learning note: none.
Change record: none

### WP-2.14 Power reconstruction requirements

Status: [x] Done | implemented by ChatGPT | commit 86fb11c | 2026-10-17
Lane: B (ChatGPT); research only, no code
Depends on: WP-2.11, WP-2.13
Owned paths: `docs/research/power/reconstruction-requirements.md`

Added 2026-10-17 at ChatGPT's request (channel 2026-10-16T1249Z), under Peter's
research-first ruling. The cross-product mechanism findings now sit inside the
PowerWorld dossier (sections 8.3 to 8.9). This WP turns them into product-neutral
requirements that the engine inventory and the later builds can cite.

Steps:

1. Write numbered requirements (R-IDs), grouped by: data and topology, solver and
   control loops, model initialization and events, protection and arc energy, line,
   neutral and grounding reductions, file import and loss, report provenance and
   show-your-working traces (decision D11), and independent verification.
2. Each requirement cites the dossier evidence (any product) and the shared matrix row
   IDs, states its acceptance check, and marks whether it is product-observed or our
   inference.
3. Rank by relevance to Zambian mining and industrial work first: motor starting, protection
   coordination, arc flash, harmonics from drives, grounding and islanded generation.
4. Reference the PowerWorld sections instead of duplicating them; do not rewrite other
   dossiers.

Reference: the four power dossiers and the source entries they cite.

Acceptance:

- Every requirement has an R-ID, a cited source or a marked inference, matrix row IDs
  and an acceptance check; the text and reference guards pass.

Learning note: none.
Change record: none

### WP-2.15 Observed-behaviour comparison cases

Status: [x] Done | implemented by ChatGPT | commit 2146242 | 2026-10-17
Lane: B (ChatGPT); research only, no code
Depends on: WP-2.14
Owned paths: `docs/research/power/comparison-cases.md`; in `docs/research/power/reconstruction-requirements.md` only the evidence-class amendment in step 4; in `docs/research/power/other-products.md` only the NEPLAN NP2 wording correction (channel 2026-10-17T0840Z)

Added 2026-10-17 on Peter's instruction. Method taken from the public REA project
(feature at a time; seen, inferred, unknown; rebuild and test against observed
behaviour), applied clean-room: we compare a product's outputs on our own inputs and
never inspect, decompile or trace its code. REA's decompilers and binary tools are
not used on any reference product and are not added to this repository.

Steps:

1. Author original test networks (no vendor or textbook case data), led by the P0
   mining workflows in WP-2.14: mill and conveyor motor start, 11 kV and 33 kV faults
   with coordination, an arc-flash bus, a VSD harmonic case, a grounding case and an
   islanded genset pickup. Each case is fully specified so any product can be fed the
   same inputs.
2. For each case, list the outputs to record from each product (values, units,
   conventions, method and version, options) and the tolerance rule, citing R-IDs.
3. Record which legitimate access route exists per product: free educational, demo or
   student editions and their limits, licensed contacts, and the platform needed
   (Windows). Dated observations, no guessed entitlements.
4. Amend `reconstruction-requirements.md` so each R-ID carries S, I or U as in WP-2.12
   step 3, adding U where the product behaviour is not established.
5. Apply the NEPLAN NP2 wording correction.

Reference: the four power dossiers, `reconstruction-requirements.md`, the owned library.

Acceptance:

- Every case is original, fully specified and linked to R-IDs; every product row names
  an access route or states unknown; every R-ID has S, I or U; text and reference
  guards pass.

Learning note: none.
Change record: none

**Implementer stop point:** A model stops after its assigned engine WP merges and
hands its suite to the other model for WP-2.7. It does not audit its own suite. Peter is asked only for assignment/scope
choices; all builds, acceptance, CI checks and merges are performed by the agents.

## 10. Seed source register

WP-0.8 and later WPs create one YAML entry per source in `docs/sources/entries/`. Starting list for Phases 0 and 1:

| Source                                                                               | Type                  | Use                                                           | Can it be in the repo?                                        |
| ------------------------------------------------------------------------------------ | --------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- |
| UW Power Systems Test Case Archive (IEEE 14, 30, 57, 118 bus)                        | Test data             | Load-flow reference solutions                                 | Data and citation, per archive terms                          |
| MATPOWER test cases, including `case4gs` (Grainger and Stevenson 4-bus) and `case9`  | Test data (BSD-3)     | Additional networks with published solutions                  | Yes, with license                                             |
| pandapower documentation and example networks                                        | Docs and data (BSD-3) | Adapter behaviour                                             | Yes, with license                                             |
| Grainger and Stevenson, _Power System Analysis_                                      | Textbook              | Load flow, faults, symmetrical components                     | Citation only                                                 |
| Glover, Overbye and Sarma, _Power System Analysis and Design_                        | Textbook              | Same, with worked examples                                    | Citation only                                                 |
| Saadat, _Power System Analysis_                                                      | Textbook              | Worked examples with software-style solutions                 | Citation only                                                 |
| Kundur, _Power System Stability and Control_                                         | Textbook              | Machine and stability models (later phases)                   | Citation only                                                 |
| IEC 60909-0                                                                          | Paid standard         | Short-circuit calculation                                     | Never; local reference library only                           |
| IEC 60255-151                                                                        | Paid standard         | Overcurrent curve formulas                                    | Never; local reference library only                           |
| IEEE 3002 series (successor to the IEEE Brown Book)                                  | Paid standards        | Industrial power system study practice                        | Never; local reference library only                           |
| B. L. Theraja and A. K. Theraja, _A Textbook of Electrical Technology_ (all volumes) | Textbook              | Broad verification of electrical formulas and worked examples | Never; local reference library only, cited by volume and page |

---

## 11. Appendix: prompt template for starting a WP

Paste this into whichever model is taking a WP:

> You are working in the Quantic Studio repository. First read `AGENTS.md` fully and follow its session-start review. Then implement **WP-<id>** from `PLAN.md` and nothing else. Change only that WP's owned paths, its own Status and Change record lines in `PLAN.md`, its learning note and new files in `docs/log/` and `docs/sources/entries/`. If you need to depart from the WP as written, set the Changed design status with all three clauses before continuing. Follow AGENTS.md section 3: one branch, one PR titled `[WP-<id>] <title>` with every acceptance command and its output, one completed log, merge after green CI.

Prompt template for a milestone audit:

> You are auditing milestone **<M>** in the Quantic Studio repository. You did not implement it. Read `AGENTS.md` and follow section 4: rerun the acceptance commands on a clean checkout, read the diffs, check owned paths, sources and numerical references, and record findings in an `audit` log, with a `dispute` log for each failure.
