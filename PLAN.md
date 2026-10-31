# Quantic Studio: Master Plan v2 (build phase)

**Owner:** Peter Kabamba, Quantic Engineering Limited
**Plan version:** 2.0 (31 October 2026)
**Repository:** `Pietrols/Quantic-Studio`
**Previous plan:** `docs/plan/PLAN-v1.md` holds Phases 0 to 2 and the research phase (WP-0.0 to WP-2.30) with every status line and change record. It is history; this file is the live plan.

**Version history**

| Version | Date | Change |
| --- | --- | --- |
| 1.0 to 1.x | 2026-10-07 to 2026-10-30 | Phases 0 to 2 and the research phase, archived in `docs/plan/PLAN-v1.md` |
| 2.0 | 2026-10-31 | Peter ends the research phase and opens Phase 3, the power suite build. Learn-then-build method (section 2). Work split into batches A to D: A and C to Claude, B and D to ChatGPT. Groundwork WPs 3.1 to 3.3 first |

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
| Implementing model | Only the `Status:` and `Change record:` lines of its WP |
| Batch auditor | Records findings in new logs; does not edit WPs |
| Peter | Anything. Peter alone approves new WPs, contract changes and edits to sections 0 to 6 |

### 0.3 Reading order for a busy owner

Section 1, then the status lines in sections 7 to 11.

---

## 1. Summary

**What:** one engineering suite that combines what ETAP, PowerFactory and PowerWorld do for power systems, then PVsyst for solar, PLC software for automation, and MATLAB/Simulink and Proteus for circuits and control, so users can switch with little change. CAD (AutoCAD and SolidWorks style) comes later on the SolidCraft and CADCraft forks.

**Where we are:** Phase 0 to 2 delivered contracts, CI, a pandapower adapter (load flow, IEC 60909, motor start), a textbook Newton-Raphson solver, a PLC Structured Text engine and a first web workbench. The research phase (WP-2.10 to WP-2.30) produced the parity matrix, engine inventory, requirements and comparison cases in `docs/research/`. Peter's static survey of the reference engines is in the private reference library.

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
      loadflow/           NR, GS, FD, controls             (batch A)
      topology/           switching, islands               (batch A)
      contingency/        N-1, N-2, screening              (batch A)
      fault/              sequence networks, IEC, ANSI     (batch B)
      motor/              dynamic motor starting           (batch B)
      harmonic/           frequency scan, harmonic flow    (batch B)
      protection/         curves, coordination, arc flash  (batch B)
      unbalanced/         three-phase phase-domain flow    (batch C)
      dynamics/           transient stability              (batch C)
      opf/, stability/, planning/                          (batch C)
    io/                   MATPOWER and PSS/E import        (batch D)
  qe_pv/, qe_plc/, qe_report/, qe_cli/, qe_api/
packages/ts/, apps/web/   workbench                        (batch D)
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

### 4.1 Lanes and batches

| Lane | Holder | Phase 3 work |
| --- | --- | --- |
| P | Peter | Decisions, approvals, survey refreshes, back-test runs on licensed copies |
| A | Claude | Groundwork 3.1 to 3.3, batch A (load flow core), batch C (advanced studies) |
| B | ChatGPT | Batch B (faults and plant), batch D (workbench, import, libraries, reports) |

- A model works through its batch in order without waiting for Peter, one WP per PR, respecting dependencies.
- **Batch audit:** at the end of each batch the other model audits the whole batch (reruns acceptance on a clean checkout, reads diffs, rechecks sources and numbers). This replaces per-WP review, as Peter asked.
- **Credits:** ChatGPT takes large batches; Claude keeps reviews compact. Peter may reassign a batch at any time.

### 4.2 Work package lifecycle

1. Session review (AGENTS.md section 2), then the next Not started WP of your batch whose dependencies are Done.
2. Branch `wp-<id>-<short-name>`; change only owned paths, your Status and Change record, your learning note, and new files in `docs/log/` and `docs/sources/entries/`.
3. Tests first or alongside. Numerical code is tested against a reference with recorded provenance.
4. Final commit marks the WP Done with one `completed` log. PR titled `[WP-<id>] <title>` with acceptance output. Merge only with green CI.

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

---

## 6. Roadmap

| Phase | Content | Milestone |
| --- | --- | --- |
| 3 Power suite | Groundwork, batches A to D below | M3A to M3D (batch audits) |
| 3 back-test | Same networks on licensed ETAP/PowerWorld via official scripting, compared with Quantic | after M3B |
| 4 Solar PV | PVsyst and HelioScope style design and yield, on research WP-2.23 to 2.26 | planned at end of Phase 3 |
| 5 Automation | PLC (TIA Portal, CODESYS style), on qe_plc and WP-2.28 | planned later |
| 6 Circuits and control | MATLAB/Simulink and Proteus style, on WP-2.27 | planned later |
| 7 CAD | On the SolidCraft and CADCraft forks | later |

Each later phase follows the same method: Peter supplies material, agents study it, then build.

---

## 7. Phase 3 groundwork (Lane A, Claude, start now)

ChatGPT is busy with the survey, so Claude lays the groundwork that every batch needs and measures what exists today.

### WP-3.1 Native power core: network compile and sparse admittance

Status: [ ] Not started
Lane: A (Claude)
Depends on: none
Owned paths: `packages/py/qe_power/src/qe_power/native/__init__.py`, `packages/py/qe_power/src/qe_power/native/core/**`, `packages/py/qe_power/tests/native/core/**`, `packages/py/qe_power/pyproject.toml`

Build the shared base every native engine uses:

1. Compile a validated `network` contract into an immutable study snapshot: bus index map, in-service elements, per-unit conversion on one documented base, element IDs kept for results.
2. Sparse bus admittance matrix (SciPy CSR) from four-block terminal stamps: pi lines, two-winding transformers with off-nominal and complex taps, shunts. Three-winding transformers as star equivalents.
3. A factorization wrapper (SciPy `splu`) that reuses one factor for many right-hand sides and reports singular systems as diagnostics.
4. Add SciPy to the package dependencies if not already present.

Acceptance:

- Ybus for MATPOWER case9 and case14 matches an independent build (pandapower's internal Ybus, run in the test only through the adapter boundary, or hand-built entries) to 1e-12.
- A two-bus and a tapped-transformer case match hand calculation.
- Invalid topology (dangling branch, unknown bus) gives a diagnostic naming the element and field.

Learning note: `docs/learning/native-network-and-ybus.md`, explaining per-unit, branch stamps, taps and why sparse.
Change record: none

### WP-3.2 Benchmark library and comparison harness

Status: [ ] Not started
Lane: A (Claude)
Depends on: none
Owned paths: `tests/benchmarks/README.md`, `tests/benchmarks/harness/**`, `tests/benchmarks/cases/**`, `tests/benchmarks/test_harness.py`, `docs/benchmarks/**`

1. Case library with provenance and licence notes: two-bus and three-bus analytical cases, MATPOWER case9, case14 and case30 with saved solutions, IEEE 4-node feeder cases (balanced and unbalanced).
2. A harness that runs every registered solver on every case it supports and records maximum voltage magnitude and angle error, branch flow error, iterations, run time and status.
3. Register what exists today: the textbook NR solver and the pandapower adapter.
4. Write the baseline: `docs/benchmarks/baseline-2026-10.md`, what we have today, where it is accurate and where it fails or has no coverage. Include the prototype results from the private study notes as a third column where recorded.

Acceptance:

- `uv run pytest tests/benchmarks` passes; the harness exits nonzero if a registered solver exceeds its declared tolerance.
- Baseline document lists every case and solver with numbers.

Learning note: `docs/learning/benchmarking-power-solvers.md`, explaining reference solutions, tolerances and why several independent checks.
Change record: none

### WP-3.3 Engine family map and Phase 3 learning index

Status: [ ] Not started
Lane: A (Claude)
Depends on: none
Owned paths: `docs/research/power/phase3-family-map.md`

One table, one row per engine family in Phase 3: parity matrix rows covered, Quantic WP, textbook and standard sources in the reference library, public benchmarks, whether private study notes exist, open gaps (for example standards not owned). The survey paths themselves go in `etap-survey/WP-MAP.md` in QE-References, not here.

Acceptance: every Phase 3 WP appears; every parity row of the power matrix maps to a WP or is marked deferred.

Learning note: none.
Change record: none

---

## 8. Batch A: load flow core (Lane A, Claude)

### WP-3.10 Native Newton-Raphson load flow

Status: [ ] Not started
Lane: A (Claude)
Depends on: WP-3.1, WP-3.2
Owned paths: `packages/py/qe_power/src/qe_power/native/loadflow/**`, `packages/py/qe_power/tests/native/loadflow/**`, `tests/benchmarks/loadflow/**`

Polar Newton-Raphson on the sparse core: power mismatch with scaled reactive residuals, sparse Jacobian, bounded voltage correction, convergence and iteration limits as explicit options. ZIP (constant power, current, impedance) loads. Generator reactive limits with PV to PQ switching and back. Branch flows, losses and power balance. Full calculation trace. Registered in the harness.

Acceptance: case9, case14 and case30 within 1e-6 pu of saved MATPOWER solutions; agrees with the textbook solver and pandapower; reactive-limit case switches correctly; nonconvergence is a failed status, never a result.

Learning note: `docs/learning/native-newton-raphson.md`.
Change record: none

### WP-3.11 Gauss-Seidel and fast-decoupled solvers

Status: [ ] Not started
Lane: A (Claude)
Depends on: WP-3.10
Owned paths: `packages/py/qe_power/src/qe_power/native/loadflow/gauss_seidel.py`, `packages/py/qe_power/src/qe_power/native/loadflow/fast_decoupled.py`, `packages/py/qe_power/tests/native/loadflow/test_gs_fd.py`

Same network, same result contract, selectable method. Gauss-Seidel with sequential updates and acceleration (default 1.47, user option). Fast-decoupled XB and BX variants with separate angle and magnitude factors and update caps (defaults 0.4 rad and 0.3 pu). Each reports iterations and the method's own stopping quantity.

Acceptance: all three methods agree on case9, case14 and case30 within tolerance; iteration counts recorded in the benchmark table.

Learning note: `docs/learning/gs-and-fast-decoupled.md`.
Change record: none

### WP-3.12 Control outer loop: taps, shunts, voltage control

Status: [ ] Not started
Lane: A (Claude)
Depends on: WP-3.10
Owned paths: `packages/py/qe_power/src/qe_power/native/loadflow/controls/**`, `packages/py/qe_power/tests/native/loadflow/controls/**`

Bounded outer loop around the inner solve: on-load tap changers with discrete steps and bandwidth, switched shunts, remote bus voltage control, generator reactive sharing. Each control action is listed in the trace. Distinct statuses: converged, converged with controls at limits, control oscillation, failed.

Acceptance: tap and shunt hand cases; a control at its limit is reported, not hidden; oscillation detection case.

Learning note: `docs/learning/load-flow-controls.md`.
Change record: none

### WP-3.13 Topology processing and islands

Status: [ ] Not started
Lane: A (Claude)
Depends on: WP-3.1
Owned paths: `packages/py/qe_power/src/qe_power/native/topology/**`, `packages/py/qe_power/tests/native/topology/**`

Switches and breakers, bus merging through closed switches, island detection, one slack per energised island, de-energised islands reported. Results mapped back to original element IDs.

Acceptance: two-island case solves both islands; an island with no source is reported de-energised; switch states change topology as expected.

Learning note: `docs/learning/topology-and-islands.md`.
Change record: none

### WP-3.14 Contract Change CC-8: contingency study contracts

Status: [ ] Not started
Lane: A (Claude)
Depends on: WP-3.10
Owned paths: `contracts/power/contingency-request.schema.json`, `contracts/power/contingency-result.schema.json`, `docs/specs/power/contingency.md`, generated types for these schemas

Request: outage lists (N-1, N-2, user sets), limits, method. Result: per contingency status, violations (voltage, thermal), ranking, island effects, trace.

Acceptance: schemas validate examples; generated types build.

Learning note: none.
Change record: none

### WP-3.15 Contingency analysis

Status: [ ] Not started
Lane: A (Claude)
Depends on: WP-3.13, WP-3.14
Owned paths: `packages/py/qe_power/src/qe_power/native/contingency/**`, `packages/py/qe_power/tests/native/contingency/**`, `tests/benchmarks/contingency/**`

AC contingency by re-solving each modified topology from the base state; fast DC screening with distribution factors (PTDF, LODF) to rank; violations reported separately from nonconverged and islanding cases.

Acceptance: case14 N-1 against an independent full re-solve; LODF screening agrees with AC ranking on the top violations; islanding outage reported.

Learning note: `docs/learning/contingency-analysis.md`.
Change record: none

### WP-3.16 Batch A audit (M3A)

Status: [ ] Not started
Lane: B (ChatGPT audits Claude's batch)
Depends on: WP-3.10, WP-3.11, WP-3.12, WP-3.13, WP-3.15
Owned paths: `docs/milestones/M3A.md`

Rerun every batch A acceptance on a clean checkout, read the diffs, recheck sources and numbers. Findings in an audit log; failures as disputes.

Learning note: none.
Change record: none

---

## 9. Batch B: faults and plant (Lane B, ChatGPT)

Starts when WP-3.1 is Done (WP-3.22 also needs WP-3.10).

### WP-3.20 Native fault engine: sequence networks and fault types

Status: [ ] Not started
Lane: B (ChatGPT)
Depends on: WP-3.1
Owned paths: `packages/py/qe_power/src/qe_power/native/fault/**`, `packages/py/qe_power/tests/native/fault/**`, `tests/benchmarks/fault/**`

Positive, negative and zero sequence networks with transformer winding and grounding connections; driving-point impedances from unit injections on one factorization; three-phase, line-to-ground, line-to-line and double line-to-ground faults with fault impedance; bus voltages and branch contributions in phase and sequence quantities; subtransient, transient and steady-state source sets.

Acceptance: textbook worked examples from the reference library; agrees with the pandapower adapter on its supported cases; solid and impedance limits; singular paths reported.

Learning note: `docs/learning/native-sequence-faults.md`.
Change record: none

### WP-3.21 IEC 60909 on the native fault engine

Status: [ ] Not started
Lane: B (ChatGPT)
Depends on: WP-3.20
Owned paths: `packages/py/qe_power/src/qe_power/native/fault/iec60909/**`, `packages/py/qe_power/tests/native/fault/iec60909/**`

Voltage factor c (D10, D12), impedance correction factors for transformers, generators and power station units, initial current, peak current (kappa methods), breaking current (mu, q), steady-state current, thermal equivalent current. Every factor cites its source; values not available from owned sources are recorded gaps (D18).

Acceptance: matches the existing adapter's cases; Kasikci worked examples; every factor traced in the report.

Learning note: `docs/learning/iec60909-native.md`.
Change record: none

### WP-3.22 Dynamic motor starting

Status: [ ] Not started
Lane: B (ChatGPT)
Depends on: WP-3.10, WP-3.20
Owned paths: `packages/py/qe_power/src/qe_power/native/motor/**`, `packages/py/qe_power/tests/native/motor/**`, `tests/benchmarks/motor/**`

Induction motor equivalent circuit with slip dynamics (speed from torque balance and inertia), load torque models (constant, quadratic, cubic, user curve), starters (direct on line, star-delta, autotransformer, soft starter, VFD current limit), network solved at each step with the native load flow, event schedule (start times, switching), voltage dip, acceleration time, stall detection. Mining loads first: mills, conveyors, pumps on weak supplies.

Acceptance: analytical constant-torque case; textbook motor examples; agrees with the existing quasi-steady adapter at the start instant; stall case reported.

Learning note: `docs/learning/dynamic-motor-starting.md`.
Change record: none

### WP-3.23 Contract Change CC-9: harmonic, protection and arc-flash contracts

Status: [ ] Not started
Lane: B (ChatGPT)
Depends on: WP-3.20
Owned paths: `contracts/power/harmonic-request.schema.json`, `contracts/power/harmonic-result.schema.json`, `contracts/power/protection-request.schema.json`, `contracts/power/protection-result.schema.json`, `contracts/power/arcflash-request.schema.json`, `contracts/power/arcflash-result.schema.json`, `docs/specs/power/harmonic.md`, `docs/specs/power/protection.md`, generated types for these schemas

Acceptance: schemas validate examples; generated types build.

Learning note: none.
Change record: none

### WP-3.24 Harmonic analysis

Status: [ ] Not started
Lane: B (ChatGPT)
Depends on: WP-3.10, WP-3.23
Owned paths: `packages/py/qe_power/src/qe_power/native/harmonic/**`, `packages/py/qe_power/tests/native/harmonic/**`, `tests/benchmarks/harmonic/**`

Frequency-dependent element models (including the h and 0.8+0.2h^2 resistance scaling options), frequency scan with one factorization per frequency and driving-point and transfer impedance, harmonic load flow with current-source spectra (VFDs, rectifiers), THD, TDD and individual distortion, resonance detection, limits against DZS 387 where the clause is owned.

Acceptance: analytical R-L-C resonance; superposition of sources; a six-pulse drive case against a textbook example.

Learning note: `docs/learning/harmonic-analysis.md`.
Change record: none

### WP-3.25 Protection curves, coordination and arc flash

Status: [ ] Not started
Lane: B (ChatGPT)
Depends on: WP-3.21, WP-3.23
Owned paths: `packages/py/qe_power/src/qe_power/native/protection/**`, `packages/py/qe_power/tests/native/protection/**`

Inverse-time (IEC and IEEE curve families with cited constants) and definite-time stages, fuse and breaker curves from user data, primary and backup coordination margins across the fault-current range from WP-3.21, TCC plot data. Arc flash: IEEE 1584 through `arcflash-calc` (MIT) and the DGUV-I 203-077 method, with clearing times from the coordination study.

Acceptance: curve constants match the cited standard text where owned; coordination margin case; arc flash matches `arcflash-calc` examples.

Learning note: `docs/learning/protection-and-arc-flash.md`.
Change record: none

### WP-3.26 Batch B audit (M3B)

Status: [ ] Not started
Lane: A (Claude audits ChatGPT's batch)
Depends on: WP-3.20, WP-3.21, WP-3.22, WP-3.24, WP-3.25
Owned paths: `docs/milestones/M3B.md`

Same procedure as WP-3.16.

Learning note: none.
Change record: none

---

## 10. Batch C: advanced studies (Lane A, Claude)

Starts when batch A is Done. Detailed steps are written into each WP when the batch opens, from the private study notes and the reference library.

### WP-3.30 Three-phase unbalanced load flow

Status: [ ] Not started
Lane: A (Claude)
Depends on: WP-3.10, WP-3.20
Owned paths: `packages/py/qe_power/src/qe_power/native/unbalanced/**`, `packages/py/qe_power/tests/native/unbalanced/**`, `tests/benchmarks/unbalanced/**`

Phase-domain current-injection Newton method, line coupling matrices, transformer winding connections (Yy, Yd, Dy, Dd with grounding), single-phase and unbalanced loads, neutral and ground paths. Acceptance: IEEE 4-node cases (all four connections, step up and down) and IEEE 13-node feeder.

Learning note: `docs/learning/unbalanced-load-flow.md`.
Change record: none

### WP-3.31 Transient stability

Status: [ ] Not started
Lane: A (Claude)
Depends on: WP-3.10, WP-3.20
Owned paths: `packages/py/qe_power/src/qe_power/native/dynamics/**`, `packages/py/qe_power/tests/native/dynamics/**`

Machine models (classical to subtransient), exciters, governors, dynamic loads, events (faults, clearing, switching), algebraic network solve each step, explicit integrator with event-aligned steps. Acceptance: single-machine infinite-bus analytical checks; published multi-machine benchmark (WSCC 9-bus).

Learning note: `docs/learning/transient-stability.md`.
Change record: none

### WP-3.32 AC optimal power flow

Status: [ ] Not started
Lane: A (Claude)
Depends on: WP-3.10
Owned paths: `packages/py/qe_power/src/qe_power/native/opf/**`, `packages/py/qe_power/tests/native/opf/**`

Primal-dual interior point with bound slacks, cost objectives, voltage and flow limits; discrete taps and shunts rounded in a separate stage. Acceptance: MATPOWER OPF saved solutions for case9 and case30.

Learning note: `docs/learning/optimal-power-flow.md`.
Change record: none

### WP-3.33 Voltage stability (continuation power flow)

Status: [ ] Not started
Lane: A (Claude)
Depends on: WP-3.10
Owned paths: `packages/py/qe_power/src/qe_power/native/stability/**`, `packages/py/qe_power/tests/native/stability/**`

Predictor-corrector continuation with adaptive step, PV and QV curves, nose point and margin, limits during continuation. Acceptance: two-bus analytical nose; case14 loading margin against a published value.

Learning note: `docs/learning/voltage-stability.md`.
Change record: none

### WP-3.34 Planning tools: capacitor placement and battery sizing

Status: [ ] Not started
Lane: A (Claude)
Depends on: WP-3.12
Owned paths: `packages/py/qe_power/src/qe_power/native/planning/**`, `packages/py/qe_power/tests/native/planning/**`

Optimal capacitor placement (loss and voltage objectives, discrete sizes, population search with explicit objective units) and DC battery duty-cycle sizing with cited method. Acceptance: small cases with exhaustive-search optimum; a textbook battery sizing example.

Learning note: `docs/learning/planning-tools.md`.
Change record: none

### WP-3.35 Batch C audit (M3C)

Status: [ ] Not started
Lane: B (ChatGPT audits Claude's batch)
Depends on: WP-3.30, WP-3.31, WP-3.32, WP-3.33, WP-3.34
Owned paths: `docs/milestones/M3C.md`

Same procedure as WP-3.16.

Learning note: none.
Change record: none

---

## 11. Batch D: workbench, import, libraries, reports (Lane B, ChatGPT)

Starts when batch B is Done. Steps are detailed when the batch opens.

### WP-3.40 Workbench redesign

Status: [ ] Not started
Lane: B (ChatGPT)
Depends on: WP-3.26
Owned paths: `apps/web/src/**`, `apps/web/tests/**`, `apps/web/e2e/**`, `packages/ts/**`

White background, grey panels and tabs, nothing blue; compact symbols; a PowerFactory and ETAP blend: single-line editor with IEC and ANSI symbols, element palette, every parameter editable both in a form and as JSON, result boxes on the diagram, colouring by result, alert view, spreadsheet view of elements and results. Uses the native engines through the API.

Learning note: `docs/learning/workbench-design.md`.
Change record: none

### WP-3.41 Network import: MATPOWER and PSS/E RAW

Status: [ ] Not started
Lane: B (ChatGPT)
Depends on: WP-3.1
Owned paths: `packages/py/qe_power/src/qe_power/io/**`, `packages/py/qe_power/tests/io/**`

From the public specifications in `docs/research/power/import-formats.md`. Acceptance: case9, case14, case30 round trip; a RAW file imports with diagnostics for unsupported records.

Learning note: none.
Change record: none

### WP-3.42 Equipment libraries

Status: [ ] Not started
Lane: B (ChatGPT)
Depends on: WP-3.1
Owned paths: `packages/py/qe_power/src/qe_power/library/**`, `packages/py/qe_power/tests/library/**`, `docs/specs/power/library.md`

Cables, transformers, motors, generators and protective devices from public manufacturer data with per-entry source. Mining first: trailing cables, mine transformers, mill and conveyor motors.

Learning note: none.
Change record: none

### WP-3.43 Study reports for the native engines

Status: [ ] Not started
Lane: B (ChatGPT)
Depends on: WP-3.26
Owned paths: `packages/py/qe_report/src/qe_report/native/**`, `packages/py/qe_report/tests/native/**`

One report per study family with the D11 working, tables, plots (TCC, PV curves, spectra, time series) and PDF and Word export.

Learning note: none.
Change record: none

### WP-3.44 Batch D audit (M3D)

Status: [ ] Not started
Lane: A (Claude audits ChatGPT's batch)
Depends on: WP-3.40, WP-3.41, WP-3.42, WP-3.43
Owned paths: `docs/milestones/M3D.md`

Same procedure as WP-3.16, plus Peter's review of the workbench.

Learning note: none.
Change record: none

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
