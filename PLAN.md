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
3. **A blocked WP stays In progress** with `blocked by <WP or reason>` appended to its status line.
4. WP-0.3 (plan checker and owned-path guard) is deferred until Peter reopens it. Manual status and ownership checks apply meanwhile; the absent checker does not block other WPs.

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

1. **Claim:** the model runs the session review (AGENTS.md section 2), picks a Not started WP whose dependencies are Done, sets it In progress, and creates branch `wp-<id>-<short-name>`.
2. **Build:** it changes only the WP's owned paths, plus its own Status and Change record, its named learning note, and new files in `docs/log/` and `docs/sources/entries/`.
3. **Pull request:** titled `[WP-<id>] <title>`, using the PR template, listing the acceptance commands and their output.
4. **Complete:** the implementer runs all tests and acceptance commands. Once CI is green, it marks its own WP Done and adds a completed log with evidence. CI must also pass on the final PR head containing the status/log update.
5. **Merge and continue:** the implementer merges with `gh`, pulls main, and proceeds to the next approved WP without waiting for Peter, respecting dependencies and explicit stop points.
6. **Milestone audit:** a different model reruns and reviews the milestone, first M0 in WP-0.10. Findings and their resolution are recorded before the milestone closes. WP-0.7 remains reserved for a model that has not read WP-0.6 implementation code.

### 4.3 Why there are no merge conflicts

| Shared resource | Conflict-free mechanism                                                                          |
| --------------- | ------------------------------------------------------------------------------------------------ |
| Source files    | Each WP owns disjoint paths; manual review checks ownership while WP-0.3 is deferred   |
| PLAN.md         | Each model edits only its WP's status lines; WP blocks are far apart, so git merges them cleanly |
| Change log      | One new file per event in `docs/log/`; nobody edits an existing log file                         |
| Source register | One YAML file per source in `docs/sources/entries/`                                              |
| Contracts       | Frozen after approval; changed only through a serial Contract Change WP (section 4.5)            |

### 4.4 Change log entries

File name: `docs/log/<YYYY-MM-DD>-<model>-WP-<id>-<event>.md`, for example `2026-10-12-claude-WP-0.6-start.md`.

```
wp: WP-0.6
model: Claude
event: start | progress | changed-design | ready-for-review | completed | audit | verified | dispute
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
| D7  | Reference library                                | Books and paid standards outside the repo at `~/QE-References/`; verification use only         | Agreed by Peter, 2026-10-07                 |
| D8  | Monorepo                                         | Monorepo with strict boundaries (section 2.3)                                                  | Recommended; recorded in ADR-0001 by WP-0.1 |
| D9  | Contract source of truth                         | JSON Schema, with generated Python and TypeScript types                                        | Recommended; recorded in ADR-0002 by WP-0.4 |

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

Status: [ ] Not started
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

Status: [ ] Not started
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

Status: [ ] Not started
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
Change record: none

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

Status: [ ] Not started
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
Change record: none

---

### WP-0.10 Integration and milestone M0

Status: [ ] Not started
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
Change record: none

---

### WP-0.11 Phase 1 planning

Status: [ ] Not started
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

## 8. Phase 1 onward

To be expanded by WP-0.11. Outline only:

- **Phase 1 (power network workbench):** pnpm workspace and React app; React Flow single-line editor that reads and writes the network contract; FastAPI study service; IEC 60909 short circuit via pandapower with textbook-verified fixtures; cable sizing and voltage drop; motor-start voltage dip; overcurrent time-current curves and coordination checks; PDF report; scenario comparison.
- **Phase 2 (PV):** pvlib sun position and transposition; irradiance import; module, string and inverter sizing; cabling and losses; yield; AC grid connection run through Phase 1 load flow and short circuit.
- **Phase 3 (circuits and control):** ngspice adapter; component canvas; oscilloscope view; python-control and SymPy transfer functions; step and Bode plots; controller tuning; evaluate Renode for microcontrollers.
- **Phase 4 (PLC and motors):** Structured Text subset interpreter or OpenPLC process bridge; MCC model; induction motor dq model; starter and drive comparison; fault injection with explained outcomes.
- **IT track (deferred, D6):** when reopened, starts with a topology contract and a containerlab generator (N1), then deploy and inspect labs (N2), a visual topology canvas sharing the Phase 1 canvas components (N3), and guided CCNA-style exercises (N4).

---

## 9. Seed source register

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

## 10. Appendix: prompt template for starting a WP

Paste this into whichever model is taking a WP:

> You are working in the `qe-platform` repository. First read `AGENTS.md` fully and follow its session-start review. Then implement **WP-<id>** from `PLAN.md` and nothing else. Change only that WP's owned paths, its own status line in `PLAN.md`, and one new file in `docs/log/`. If you need to depart from the WP as written, set the Changed design status with all three clauses before continuing. Finish by opening a pull request titled `[WP-<id>] <title>` using the template, with every acceptance command and its output.

Prompt template for verifying:

> You are verifying **WP-<id>** in the `qe-platform` repository. Read `AGENTS.md` and do the session-start review. Check out the PR branch, re-run every acceptance command yourself, read the full diff, and confirm that only owned paths changed. If everything holds, set the WP to Done with your name as verifier and add a `verified` log file. If not, add a `dispute` log file explaining exactly what failed, and leave the status unchanged.
