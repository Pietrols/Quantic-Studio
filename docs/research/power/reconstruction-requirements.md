# Power reconstruction requirements

WP-2.14, ChatGPT, 2026-10-17. Research specification, not implemented capability or
an authorization to resume builds. This document converts the four product dossiers
into requirements for an independent Quantic implementation. Public documentation
describes externally visible behavior; it does not reveal proprietary source code.

## Reading and priority

Each R-ID has a priority, evidence class, dossier reference, shared matrix IDs and
an acceptance check. **O** means the behavior is product-observed in the cited
documentation, not independently executed. **I** means our proposed inference or
design rule. Even O requirements are proposals for Quantic, not proof of parity.
An acceptance check below is a future obligation, not a test reported as passing.
Book references support methods, not today's standards limits or equipment defaults.

P0 prioritizes Zambian mining and industrial study needs. P1 adds industrial depth;
P2 covers wider planning and advanced analysis. These are research priorities, not
approved build order. No mine-specific voltage, torque, relay or safety limits are
assumed; site and manufacturer inputs must supply them with provenance.

| Priority workflow | Principal requirements | Required dependency chain |
| --- | --- | --- |
| P0: mill and conveyor starting | R-009, R-015, R-016, R-017, R-021 | Operating state, load flow, motor/load torque and inertia, starter, generator response, protection |
| P0: coordination and arc energy | R-023 to R-030 | Fault method, source contributions, device measurement, relay and breaker sequence, energy integration |
| P0: drive harmonics | R-014, R-034, R-048 | Fundamental operating point, source spectrum/phase, frequency-dependent network, resonance and reporting |
| P0: grounding and earth return | R-025, R-031 to R-035 | Winding/neutral connections, fault return, soil/grid model, current split, method-specific safety assessment |
| P0: islanded gensets and transfer | R-004, R-010, R-017 to R-022 | Island/reference detection, generation control, initialized dynamics, switching and load pickup |
| P1/P2: broader industrial and planning depth | R-011 to R-013, R-036, R-050, R-051 | Reusable model and provenance with separately specified solver families |

Evidence keys below link to the existing research. Source IDs such as W197 refer to
the numbered source ledger in that dossier, not fresh runtime measurements.

| Key | Dossier evidence to consult | Important boundary |
| --- | --- | --- |
| PW-D | [PowerWorld sections 3 and 5.11](powerworld.md#3-architecture-and-data-model) | Database/diagram separation and topology processing |
| PW-S | [PowerWorld section 8.3](powerworld.md#83-mechanism-level-reconstruction-notes) | Controls, topology, initialization and interchange, W165 to W176 |
| PW-M | [PowerWorld section 8.4](powerworld.md#84-independent-mathematical-references-and-complementary-engines) | Independent methods, W177 to W195; no common-backend claim |
| PW-V | [PowerWorld sections 8.5 and 8.6](powerworld.md#85-proposed-verification-ledger-for-our-own-implementation) | Proposed checks versus performed normalized arithmetic |
| PW-X | [PowerWorld section 8.7](powerworld.md#87-cross-product-checks-that-affect-a-faithful-comparison) | ETAP/PF dynamics and meter comparisons, W196 to W205 |
| PW-L | [PowerWorld section 8.8](powerworld.md#88-lines-neutrals-and-grounding-need-study-specific-reductions) | Line representation, neutral boundaries, GIC, W206 to W217 |
| PW-I | [PowerWorld section 8.9](powerworld.md#89-dynamic-model-semantics-beyond-the-model-name) | Model validation, limits, load composition and events, W218 to W227 |
| ET-D | [ETAP sections 3 and 6](etap.md#3-architecture-and-data-model) | Configurations, libraries, study cases and workflow |
| ET-S | [ETAP section 5](etap.md#5-studies-and-modules) | E4/E23/E24 motors; E5 harmonics; E11 faults; E13/E14 arc; E15 protection; E16 dynamics; E32 grounding |
| PF-D | [PowerFactory sections 3 and 6](powerfactory.md#3-architecture-and-data-model) | Types, scenarios, variations and study cases |
| PF-S | [PowerFactory section 5](powerfactory.md#5-studies-and-modules) | P3 load flow; P4 faults; P11 protection; P12 arc; P14 harmonics; P17 RMS; P19 motors |
| OTHER | [Other products](other-products.md) | EasyPower, SKM, NEPLAN and PSS/E, with product/version boundaries |
| BOOK | [Book verification entry](../../sources/entries/power-reconstruction-book-methods-2026-10-17.yaml) | Glover pp. 352, 356-357; Kundur pp. 285-287, 299-301; Das PDF pages and sections below |

Matrix references use the IDs in the
[shared draft matrix](notes/matrix-draft-etap-powerfactory.md), not its provisional
vendor-support cells. **PLAN decision D11** means show-your-working; **matrix D11**
means manufacturer libraries. G13 is the matrix row for show-your-working.
ETAP and PowerFactory source IDs resolve through their
[ETAP source index](notes/etap-sources.md) and
[PowerFactory source index](notes/powerfactory-sources.md). E87 is a historical
motor-fitting tutorial indexed there and discussed as a research gap in ETAP
section 10; it is not evidence of independently verified modern fitting behavior.

## 1. Data and topology

### R-001: One physical model, multiple presentations

Priority: P0. Class: O. Evidence: PW-D; ET-D; PF-D. Matrix: D1, D3, G1, G2.
Keep persistent equipment and terminal identities independent of diagram objects.
Acceptance: show one feeder in two views; edit its impedance in one view and obtain
one shared model revision. Moving or deleting its symbol must leave connectivity
unchanged unless an explicit electrical edit is requested. Reports resolve every
result to the same physical element ID.

### R-002: Types, instances and sourced parameters

Priority: P0. Class: O. Evidence: ET-D; PF-D; OTHER sections 3/4. Matrix: D2, D10, D11, D12.
Separate shared equipment types from installed instances, with explicit overrides
and provenance for manufacturer curves and ratings.
Acceptance: update a type used by two motors, retain one documented instance
override, show both effective parameter sets and invalidate affected results.
Missing required curve data must identify the element and field, with no invented default.

### R-003: Reproducible operating state and study options

Priority: P0. Class: O. Evidence: ET-D; PF-D; PW-D. Matrix: D4, D5, D6, D7, D8, G10.
Resolve base network, engineering variation, switching/dispatch/loading state,
time profile and calculation options into a reproducible run input.
Acceptance: run two loading states and a maintenance state without changing the
base; resolve conflicts visibly, retain the effective values and reproduce each
result after another scenario has run. Record profile interpolation and time basis.

### R-004: Topology reduction with island and identity maps

Priority: P0. Class: I. Evidence: PW-S subsection A, W171/W172; PF-S P15. Matrix: G2, G7, S9.
Separate physical node/breaker topology from each study's reduced electrical graph.
Acceptance: close, split and rejoin an ideal-switch group; retain a reversible
physical-to-solver map, detect islands and references, invalidate stale solutions,
and diagnose an unsupplied island explicitly. Preserve breaker identity for protection.

### R-005: Transactional studies and batch isolation

Priority: P0. Class: I. Evidence: PW-S subsection A; PW-V contingency checks; ET-D; PF-D.
Matrix: D9, D13, D14, D15, S15.
Study actions must produce traceable derived states and support restoration.
Acceptance: run an outage study that fails midway, then rerun the base case; its
effective input hash and solution must match the uncontaminated base. Batch order
and parallel execution must not leak switch, setting or controller state between runs.

### R-006: Quantities and validation before solving

Priority: P0. Class: I. Evidence: PW-D section 3.3; PW-M subsection A; BOOK Glover section 6.6.
Matrix: D12, S1, F1, M1.
Declare bases, units, sign/direction, phase/sequence and RMS/peak conventions.
Acceptance: equivalent unit/base representations give equivalent physical results;
inconsistent voltage bases, absent endpoints and invalid model parameters produce
element/field diagnostics before numerical assembly. Do not silently reinterpret bad data.

## 2. Solvers and control loops

### R-007: AC network equations and convergence evidence

Priority: P0. Class: I. Evidence: PW-M subsection A, W177/W178; PW-V; BOOK Glover pp. 356-357.
Matrix: S1, S2, S7, S8, G13.
Specify branch stamps, transformer tap side and phase, shunts, load dependence,
temperature assumptions, mismatch scaling and stopping criteria.
Acceptance: independent terminal-current and power-balance checks, derivative
checks and equivalent reduced/retained PV formulations agree on an original small
network. Iteration exhaustion, singularity and convergence have distinct diagnostics.

### R-008: Voltage controls and reactive limits

Priority: P0. Class: O. Evidence: PW-S subsections B/C, W166-W170; PF-S P3; BOOK Glover pp. 352, 356-357.
Matrix: S3, S4, S5, S6.
Represent regulated measurements, participating devices, capability limits and
control priority, including local/remote voltage, tap and shunt control.
Acceptance: drive a generator into and out of a Q limit and remove a remote-control
participant; verify individual bounds, active equations, release policy and control
trace. A feasible aggregate Q must not conceal an individual violation or control conflict.

### R-009: Static starting dip is a separate calculation

Priority: P0. Class: O. Evidence: ET-S E4/E23/E24; PF-S P19; BOOK Das section 12.11, PDF 438-439.
Matrix: M1, M3, S7.
Specify standstill motor representation, starting method and network/source model
for initial voltage dip; report the approximation separately from acceleration.
Acceptance: compare an original locked-rotor circuit and solved network with an
independent circuit solution. Changing starter impedance changes terminal voltage
and current consistently. A snapshot result must not claim starting time or successful run-up.

### R-010: Island slack and generation sharing

Priority: P0. Class: I. Evidence: PW-S subsections B/C; PF-S P3; ET-S E16. Matrix: S6, S9, T5.
Distinguish a steady-state reference/slack policy from physical governor/exciter
and droop dynamics. Declare generation bounds and load-shedding policy.
Acceptance: separate two islands, trip a participating genset and apply a load step;
balance each energized island or report unmet load/insufficient control. A static
slack solution alone cannot validate frequency recovery or black start.

### R-011: Contingencies and sensitivities with declared assumptions

Priority: P1. Class: I. Evidence: PW-V; PW-M; PF-S P10/P15. Matrix: S15, S16.
Record outage sets, balancing policy, controls, ratings and AC/DC approximation.
Acceptance: compare sensitivity predictions to independent small perturbations
under matching assumptions and verify full AC post-contingency feasibility. Detect
islanding and invalid linearization rather than returning a plausible sensitivity.

### R-012: Separate loadability, optimization and chronology

Priority: P2. Class: I. Evidence: PW-M subsections B/C/I, W179-W182/W190/W191; PF-S P20/P45.
Matrix: S13, S14, S17, S26.
Define continuation direction/limits, OPF objective/constraints and chronological
dispatch or commitment states as distinct problems.
Acceptance: identify a continuation limit with a refinement bracket, check final
nonlinear OPF feasibility independently, and exercise an authored ramp/minimum-up
constraint across periods. Snapshot dispatch must not stand in for unit commitment.

### R-013: Phase-domain and physical DC studies

Priority: P1. Class: I. Evidence: PW-M subsection F; PW-L subsection D; ET-S E9/E21; PF-S P3/P4.
Matrix: S10, S12, F2, F5.
Select balanced, explicit-phase/neutral or physical DC network equations by study.
Acceptance: solve an asymmetric original feeder against a primitive phase circuit;
its balanced special case matches a compatible sequence calculation. A resistive
physical DC fixture must use actual conductors and return paths, with no substitution
of the transmission DC-angle approximation.

### R-014: Drive harmonics and frequency scans

Priority: P0. Class: O. Evidence: ET-S E5; PF-S P14; PW-M subsection H, W189; BOOK Das sections 18.5.1, 19.1.2/19.1.4, PDF 624-625, 636-637.
Matrix: H1, H2.
Specify source spectrum, phase reference, operating point, frequency-dependent
equipment and damping; separate harmonic flow from unit-injection impedance scans.
Acceptance: compare an original RLC network to an independent complex-circuit
solution; refine frequency spacing around resonance and test source phase
cancellation. Report THD/TDD denominators and assess limits only against a sourced edition.

## 3. Model initialization and events

### R-015: Motor acceleration with mechanical load

Priority: P0. Class: O. Evidence: ET-S E4/E23/E24; PF-S P19; BOOK Kundur pp. 285-287, 299-301; Das section 12.11.2, PDF 439.
Matrix: M2, M3, T1.
Model motor electrical behavior, shaft/load inertia, torque-speed curve, starter
transitions and coupled bus voltage. Mill and conveyor load curves require actual
manufacturer/site data, not a generic fan-load assumption.
Acceptance: use original torque curves with positive and negative acceleration
regions; verify torque/work/energy balance and time-step refinement. Report stall,
failure to accelerate or protective trip distinctly from successful run-up.

### R-016: Parameter fitting exposes uncertainty

Priority: P1. Class: I. Evidence: ETAP section 10 and source index E87; PF-S P49; PW-I subsection D. Matrix: M4, D11, D12.
Keep supplied nameplate/test curves, fitted circuit parameters and model assumptions
separate; report fit range, residuals and non-identifiability.
Acceptance: fit an original synthetic curve from known parameters, then remove data
and demonstrate ambiguity or failure rather than asserting a unique motor model.
Hold out operating points and compare predicted current and torque there.

### R-017: Consistent static-to-dynamic initialization

Priority: P0. Class: I. Evidence: PW-S subsection D; PW-X W199; PW-I subsections A/C/D.
Matrix: T1, T2, M2, D12.
Declare model roles, terminal attachments, known/unknown signals and dependencies;
initialize differential/algebraic states from the effective operating point.
Acceptance: check residuals and no-event drift; expose missing setpoints and dependency
cycles. Count generator/load injections once. An inactive or unsupported dynamic
model must not disappear without a diagnostic or silently become a validated replacement.

### R-018: Validation changes and effective model ledger

Priority: P0. Class: I. Evidence: PW-I subsection A, W218/W219/W223/W224; PW-X. Matrix: D12, T1, T2.
Distinguish invalid input, persisted parameter repair, run-only limit adjustment
and model substitution. Retain requested and effective values and the reason.
Acceptance: initialize deliberately incompatible limits and an unsupported model;
exercise reject/explicit-repair policies, verify base data persistence, and reproduce
the effective run. Conflicting vendor prose must remain an unresolved source gap.

### R-019: Dynamic limits and load composition

Priority: P0. Class: I. Evidence: PW-I subsections B/C, W220-W222/W225/W226. Matrix: S7, T1, T2, M2.
Specify limiter state behavior, anti-windup/release, load fraction bases and internal
shunt reconciliation, rather than inferring equations from model names.
Acceptance: an original limit/reversal case distinguishes clipped output from
bounded state; independent P/Q component totals and voltage perturbations reveal
double counting or shunt treatment. Diagnose degenerate fraction/base cases explicitly.

### R-020: Events, integration steps and output samples

Priority: P0. Class: I. Evidence: PW-X W196-W198; PW-I subsection E, W227. Matrix: T1, T2, T5, G12.
Separate scheduled actions, state-triggered events, internal solver steps, stored
samples and display cadence. Specify simultaneous-event ordering and algebraic reinitialization.
Acceptance: change output cadence without changing the solved trajectory; locate
an authored pair of guard crossings even when endpoint signs agree, or issue an
explicit detection limitation. Refine steps independently and trace pre/post-event states.

### R-021: Protection, starters and transfer are coupled events

Priority: P0. Class: I. Evidence: ET-S E15/E16/E23; PF-S P11/P19; OTHER SKM section 6.1.
Matrix: M2, M3, P4, T5.
Sequence starter transitions, contactor logic, relay operation and breaker/transfer
actions using sourced settings and a shared event timeline.
Acceptance: on an authored motor/genset network, test run-up, stalled start and
failed transfer with different protective states. Re-solve affected topology after
opening; report the initiating condition, operating delay and resulting energized islands.

### R-022: Numerical method and coupling capabilities

Priority: P1. Class: I. Evidence: PW-X W197-W203; PW-M subsections D/E. Matrix: T1, T2, T3, T4.
Declare RMS versus EMT equations, integrator, tolerances, numerical damping,
reference frame, external-model interface and rollback/event capabilities.
Acceptance: lossless/damped original systems separate physical decay from numerical
decay; compare phase/amplitude under refinement. A partitioned comparison records
exchange residuals. Do not infer PowerFactory's theta mapping from UI endpoints,
ETAP's integrator from plot steps, or full-system modes from fitted signal modes.

## 4. Protection and arc energy

### R-023: Fault methods retain their assumptions

Priority: P0. Class: O. Evidence: ET-S E10-E12; PF-S P4; PW-M subsection F. Matrix: F1, F2, F3, F4, F6.
Separate standardized equivalent-source methods, loaded-prefault superposition and
time-domain decay. Record method edition, voltage/correction factors, machine/converter
contributions and maximum/minimum case assumptions.
Acceptance: independent original sequence/phase calculations verify supported fault
types; deliberately missing method-specific inputs cause diagnostics. A result from
one method must not be relabeled as another standard or edition.

### R-024: Fault locations, contribution paths and duty

Priority: P0. Class: I. Evidence: PF-S P4; ET-S E10/E11; OTHER EasyPower section 6.1, EP20-EP22.
Matrix: F7, F8, P4, A1.
Resolve fault location to terminal/compartment side, calculate source-path and
device currents, and distinguish current quantities used for equipment duty.
Acceptance: a two-source fixture gives different bus total and device currents;
moving the fault across an incomer changes the exposed compartment/path correctly.
Verify contribution sums and match each duty comparison to its rated quantity and time basis.

### R-025: Ground fault and instrument connections

Priority: P0. Class: I. Evidence: PW-M subsection F; PW-L subsection C; PF-S P11; ET-S E9/E15.
Matrix: F2, P1, P8, S10, S11.
Preserve winding/vector group, neutral grounding, CT/VT ratio, polarity, location
and residual/sequence measurement definitions.
Acceptance: change a grounding connection and reverse a CT polarity in an original
fixture; verify zero-sequence paths and measured relay quantities independently.
Unsupported saturation/transient instrument models must be marked outside scope.

### R-026: TCCs, motor envelopes and coordination checks

Priority: P0. Class: O. Evidence: ET-S E15/E28/E29; PF-S P11; OTHER sections 5. Matrix: P1, P2, P3, P5, D11.
Store curve family/edition, device revision, units, settings, tolerances and
applicable current/time range; compare start and damage envelopes explicitly.
Acceptance: independent evaluations agree at sourced curve points, boundaries and
pickup transitions. Test primary/backup overlap and a motor-start envelope crossing.
A diagram of curves alone is not a validated selectivity or motor thermal conclusion.

### R-027: Relay memory, decrement and breaker opening

Priority: P0. Class: I. Evidence: OTHER SKM section 6.1, SK21-SK23; EasyPower section 6.1, EP20-EP22.
Matrix: P4, A1, T5.
Specify relay accumulation/reset, pickup/dropout, contribution changes, failed trips
and breaker opening delay separately from an instantaneous curve lookup.
Acceptance: apply a piecewise current that falls below pickup before completion,
then recovers; verify the declared reset/memory rule and independent event sequence.
Do not adopt the SKM decrement example as a universal relay-memory law.

### R-028: Arc method domain and scenario inputs

Priority: P0. Class: I. Evidence: ET-S E13/E14; PF-S P12; OTHER EasyPower section 6.1, EP22.
Matrix: A1, A2, A3, A4.
Retain method/edition, electrode/enclosure configuration, gap, working distance,
equipment class and applicable domain, with separate AC/DC/HV routes.
Acceptance: omit a mandatory input and exercise domain edges; diagnose unsupported
cases instead of extrapolating a low-voltage empirical method. Method constants,
boundaries and labels require the readable governing source before implementation.

### R-029: Arc energy follows protection and changing current

Priority: P0. Class: I. Evidence: OTHER EasyPower section 6.1, EP20-EP22; SKM section 6.1, SK23; ET-S E13/E14.
Matrix: A1, P4, F7.
Evaluate required normal/reduced arcing-current cases and retain time-ordered source,
device, trip, current and energy intervals. Recalculate after each clearing action.
Acceptance: an authored case has lower current but longer clearing and higher energy;
another loses one source first. Verify interval accumulation independently, with
method-prescribed applicability. Never obtain clearing time from total bus current alone.

### R-030: Maintenance, backup and unresolved duration

Priority: P0. Class: I. Evidence: OTHER SKM section 6.1, SK21/SK22; EasyPower section 6.1, EP20-EP22.
Matrix: D4, P4, A1, A2.
Treat maintenance settings, main failure, upstream search, manual duration and time
caps as distinct scenarios or policies, exposing their effect on clearing and energy.
Acceptance: compare normal, maintenance and failed-main states; report selected
backup and any unresolved clearing. A capped calculation must identify the cap and
uncleared source; a label must retain scenario and assumptions rather than imply certainty.

## 5. Lines, neutrals and grounding

### R-031: Physical line and cable representation

Priority: P0. Class: I. Evidence: PW-L subsection A, W206-W211; ET-S E9/E18/E19; PF-S P13.
Matrix: S11, C1, C2, C8.
Preserve conductor/bundle geometry, units, sequence/phase representation, frequency,
temperature, earth-return assumptions and requested/effective model choices.
Acceptance: equivalent unit systems and explicitly transposed geometry agree;
changing temperature or frequency uses the declared physical model. Missing soil,
material or installation data cannot be replaced by unsourced engineering numbers.

### R-032: Long-line equivalents and terminal invariants

Priority: P1. Class: I. Evidence: PW-L subsection B; PW-V; BOOK Glover chapter 5 index in PW section 8.1.
Matrix: S11, S24.
Distinguish distributed-line equivalents from multiplying per-length lumped values.
Acceptance: compare an original distributed line and its equivalent at both terminals;
verify reciprocal two-port and short-length limit identities and refine segmentation.
Record the study/frequency range over which the reduction is claimed valid.

### R-033: Neutral elimination declares boundary conditions

Priority: P0. Class: I. Evidence: PW-L subsection C, W212/W213. Matrix: S10, S11, S24.
Record retained/eliminated conductors, grounding boundary conditions and the
reconstruction map for neutral voltages/currents.
Acceptance: compare a compatible reduced network to the full primitive network;
then alter the neutral grounding so the old reduction is invalid and require
reduction recomputation or an explicit diagnostic. Deleting a neutral is not a general Kron reduction.

### R-034: Frequency-specific return paths and reductions

Priority: P0. Class: I. Evidence: PW-L subsections C/E; PW-M subsection H; BOOK Das section 19.1, PDF 636-637.
Matrix: S11, S24, H1.
Qualify reduction validity by study and frequency, including zero-sequence and
harmonic return paths. Do not reuse a balanced power-flow equivalent without qualification.
Acceptance: compare full/reduced original phase circuits across the requested band
and switching states; report terminal errors and reconstructed return current.
A failure at a new frequency invalidates the claim there rather than changing the tolerance.

### R-035: Ground-grid model and fault-current split

Priority: P0. Class: I. Evidence: ET-S E32; OTHER EasyPower section 6.2, EP23; PW-L. Matrix: C6, F2, S11.
Separate grid/soil potential analysis from network grounding impedances and GIC.
Track soil measurements/model fit, conductor/grid geometry, fault-current split,
duration and sourced step/touch method inputs.
Acceptance: verify an original simple field/circuit case against an independent
method and a mesh/refinement study, then audit the fault-current split and return
paths. Product availability or a partner integration is not evidence of a validated grid solver.

### R-036: Geomagnetic and geographic calculations are separate studies

Priority: P2. Class: I. Evidence: PW-L subsections D/E, W214-W217. Matrix: S11, S12, D17.
Treat GIC as a physical resistive earth-return network with geographic field inputs,
not DC-angle power flow. Declare field sampling and transformer winding/earth models.
Acceptance: an original uniform-field route matches an independent line integral;
check parallel phase resistance versus shared grounding resistance and KCL. Do not
divide a common earth resistance by three or claim saturation/harmonics from a DC result alone.

## 6. File import and information loss

### R-037: Revision-specific import contract

Priority: P0. Class: I. Evidence: PW-S subsection F, W11/W172; PF-D; OTHER PSS/E section 6.1.
Matrix: D16, D12.
Declare supported format/revision, units, object/terminal identity mapping and study
coverage before translating data.
Acceptance: import original files with reordered records and repeated local names;
retain stable identities or report ambiguity. Unsupported revision/record variants
must be diagnosed rather than interpreted as the nearest known format silently.

### R-038: Loss, default and unsupported-model ledger

Priority: P0. Class: I. Evidence: PW-S subsection F; PW-I subsection A; OTHER PSS/E section 6.1.
Matrix: D16, D12, T2.
Report omitted, approximated, defaulted and inactive objects/fields, with original
values, target values, reason and affected studies.
Acceptance: import an original unknown dynamic model and an unsupported control;
block claims of full dynamic parity, retain unresolved source records and show
exactly which static studies remain meaningful. A successful parse is not a lossless translation.

### R-039: Physical round-trip verification

Priority: P1. Class: I. Evidence: PW-V interchange checks; PW-S subsection F. Matrix: D16, G10.
Define which semantics survive each import/export route, independently of text order.
Acceptance: round-trip an original transformer/phase/neutral/control network;
compare effective connectivity, bases, parameters and solved quantities under a
declared compatible study. Detect loss of vector group, control attachment or status
even when bus/branch counts and file syntax still match.

### R-040: Dynamic model and ABI version boundaries

Priority: P1. Class: O. Evidence: OTHER PSS/E section 6.1; PW-X W203; PW-I. Matrix: D16, T2, T4.
Record external-model format, interface version, compiler/runtime requirements and
supported state/rollback capabilities separately from model names.
Acceptance: incompatible model binaries/interfaces fail with actionable diagnostics;
an adapter advertises only supported capabilities. Reading a dynamic data record
must not claim execution of its proprietary binary or conformance to the full FMI standard.

### R-041: Source and dataset rights remain separate

Priority: P0. Class: I. Evidence: PW-M subsection J, W192-W195; PW section 8.1 W106; BOOK.
Matrix: D11, D16, D15.
Record permissions for engine code, bindings, models, curves, benchmarks and files
individually. Reference-only book methods may guide original checks without copying cases.
Acceptance: a proposed public fixture has a traceable per-dataset rights decision;
reject the inference that MATPOWER's code licence covers its case files. Keep GPL
programs in a separately invoked process under repository policy, with no package import.

## 7. Report provenance and show-your-working

### R-042: Reconstructible run provenance

Priority: P0. Class: I. Evidence: PW-V; PW-X W202; ET-D; PF-D; AGENTS engineering conduct.
Matrix: G11, G13, D6.
Retain input/effective-state hashes, solver/model/version, method edition, options,
source provenance, time basis and diagnostic summary for every result.
Acceptance: reconstruct a run from its manifest and match effective inputs; change
one controller, library revision or option and obtain a distinguishable provenance
record. Cached results with incompatible hashes must be invalidated.

### R-043: Trace equations, substitutions and control decisions

Priority: P0. Class: I. Evidence: PW-V; PW-I; BOOK Glover pp. 356-357; PLAN decision D11.
Matrix: G13, D12, S1, F1, M1, A1.
Expose governing method, parameter sources, conversions, effective values and
intermediate decisions at the level needed to audit the answer.
Acceptance: follow one fault result through corrections/contributions, one motor
result through circuit/torque assumptions, and one arc result through clearing
intervals. Each reported intermediate maps to the numerical run, not decorative reconstructed arithmetic.

### R-044: Measurement and plotting semantics

Priority: P0. Class: I. Evidence: PW-X W196/W201/W202; PW-I W227. Matrix: G5, G12, T1, T4, H1.
Label instantaneous, phasor, RMS, sequence and derived-meter quantities with
reference, window, filtering, latency and sampling/resampling policy.
Acceptance: retain raw and processed original signals; demonstrate the known
processing effect without changing physics. Compare vendor traces only after
matching quantity and meter definition, with plots identifying event and sample times.

### R-045: Violations, unsupported scope and engineering limits

Priority: P0. Class: I. Evidence: ET-D; PF-D; PW-D section 3.3; OTHER arc qualifications.
Matrix: G6, G9, G11, D12.
Distinguish converged, partially evaluated, nonconverged, out-of-domain and
unsupported results; attach each violation to its sourced limit and element.
Acceptance: force each outcome and inspect diagram/table/export consistency.
No-result must not become zero or a green status. A vendor capability claim or
historical textbook value must not become a present-day site compliance limit.

### R-046: Comparative reports preserve state and scope

Priority: P1. Class: I. Evidence: PW-X; ET-D; PF-D; OTHER arc scenarios. Matrix: G10, G11, A2, D4.
Compare scenarios using explicit common quantities and show changed inputs,
assumptions, unresolved losses and applicable study scope.
Acceptance: compare normal/maintenance states and two motor-start alternatives;
trace each delta to a scenario and method. Reports and arc labels carry revision,
location and assumptions and must not mix results from incompatible effective networks.

## 8. Independent verification and wider coverage

### R-047: Original fixtures and independent oracles

Priority: P0. Class: I. Evidence: PW-V; PW section 8.1 W106; BOOK. Matrix: S1, F1, F2, M1, M2, G13.
Use original small networks and independently evaluated equations before commercial
cross-checks; record source method, input origin and what has actually been verified.
Acceptance: a reviewer can reproduce an oracle without calling the solver under
test. Book-derived methods are page/section-cited, with original inputs; inspected
text or selected rendered pages are not promoted into complete verified case datasets.

### R-048: Acceptance is layered and discriminating

Priority: P0. Class: I. Evidence: PW-V; PW-L subsection F; PW-I subsection F; BOOK.
Matrix: S1, S11, M2, P4, A1, H1, C6.
Separate exact algebraic identities, numerical error, model adequacy and engineering
acceptability. Choose tolerances from method conditioning/refinement and source precision.
Acceptance: include conservation, limit transitions and counterexamples for the P0
workflows, not only expected outputs. A normalized arithmetic pass cannot certify
equipment settings, safety limits, an empirical arc model or a soil model.

### R-049: Vendor comparison is model- and version-specific

Priority: P0. Class: I. Evidence: PW-X W196-W202; PW section 9.2; OTHER version qualifications.
Matrix: G10, T1, T4, M2, A1.
Match equations, settings, initial states, events, numerical controls and meter
definitions before judging parity. Preserve source ambiguities and missing inputs.
Acceptance: a comparison manifest identifies exact vendor build and model revision;
deliberately introduce a known semantic difference and show that the process detects
it. Agreement between two executions of one engine is not an independent oracle.

### R-050: Observability, uncertainty and stochastic studies

Priority: P2. Class: I. Evidence: PW-M subsections G/I; PW-X W204; PF-S P26/P44. Matrix: S18, S19, S22, S23.
Specify measurement covariance/rank and bad data, uncertainty distributions and
correlations, hosting constraints/policy, failure rates and restoration chronology.
Acceptance: an unobservable original estimator fails despite ample measurement
count; seeded stochastic runs reproduce and satisfy independent simple probability
checks. Hosting and reliability outputs name their assumptions rather than imply universal capacities.

### R-051: Adjacent industrial engines keep distinct physics

Priority: P1. Class: I. Evidence: ET-S E18-E21/E31/E32/E70; PF-S P13/P21; OTHER SKM section 6.2.
Matrix: C1, C2, C3, C4, C5, C6, C7, C8, H3.
Keep cable ampacity/sizing, pulling, transformer sizing, battery duty, panels,
line mechanics, grounding and flicker as separately sourced calculations with
explicit input/output links to network studies.
Acceptance: each proposed engine has its governing method, edition, original
verification case and missing-source register before build approval. A cable
electrical pass cannot imply acceptable pulling tension or a battery-duty pass.

### R-052: Coverage and unresolved work remain auditable

Priority: P0. Class: I. Evidence: all four dossiers' gaps; PW-V; shared draft matrix.
Matrix: D12, G11, G13.
Maintain R-ID to source/matrix/test/implementation mappings, recording uninspected
clauses, conflicting documentation and unsupported capabilities explicitly.
Acceptance: audit every R-ID for class, evidence, matrix IDs and acceptance;
distinguish proposed, implemented and independently verified states. Update the
mapping when the final parity matrix arrives. Research coverage is not a claim to
have exhausted every source or reverse-engineered a proprietary implementation.

## Verification order and open gates

Start future numerical work with R-001 to R-008 and R-037/R-038/R-042/R-043,
then the six P0 workflows in the first table. Requirements within a workflow share
fixtures, but each check must expose the mechanism it verifies. Code changes and
contract changes still require their own approved WPs.

The present document verifies requirement structure and source traceability only.
It supplies no new arc equations, curve constants, soil safety limits, manufacturer
settings or copied textbook networks. Current standard clauses and equipment data
must be readable before those values can enter an implementation. The final
WP-2.12 matrix, Claude's pending ETAP/PowerFactory deepening and any identified
source conflicts remain inputs to later revisions, not reasons to invent missing behavior.
