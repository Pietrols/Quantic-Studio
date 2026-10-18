# Mining network model validation

WP-2.19, ChatGPT, 2026-10-18. Research requirements for independently validating
Quantic's future mine power studies. No mine model, commercial solver, site test or
client dataset was executed here. No source project, figure or worked inputs are
reproduced. This document adds validation obligations, not build approval or field
settings, to the [reconstruction requirements](reconstruction-requirements.md).

## Evidence and scope

S identifies a statement read in a primary source, I an authored inference or
proposed requirement, and U an unresolved fact. Each V-ID distinguishes the
documentary evidence from the proposed Quantic behavior and future acceptance.
None of the acceptance checks below is reported as passed. Runtime validation of
ETAP, PowerFactory, PowerWorld and Quantic against mine measurements remains U.

The sources support a workflow, not universal engineering limits. They span a
historical mining application, contemporary vendor service descriptions, academic
method studies and a recent published mining simulation. A paper's claim that its
model is validated is S as an author statement; independent access to its measured
records, exact model and acceptance decision is a separate question, here U.

| ID | Primary source, date and exact inspected scope | What it establishes and what it does not |
| --- | --- | --- |
| MV1 | David Browne, DIgSILENT Pacific, [Modelling of a Large Mining Network](https://digsilent.com.au/en/publications.html?cid=13854&file=files/publications/2013/slides/Browne.D_Modelling+a+large+mining+network.pdf), 2013 publication path; 18-slide PDF, text read, especially PDF pp. 7-8, 13-16, 18 | Historical mine data collection, separate controls/loads, measured drive profiles and site-test comparison; no reusable public project or current default established |
| MV2 | DIgSILENT Pacific, [Power Plant and Power System Measurements](https://digsilent.com.au/en/consulting-power-plant-and-power-system-measurements.html), accessed 2026-10-18, service description | Measurement programs depend on objectives and operating constraints; generator/control validation service, not an independently audited accuracy result |
| MV3 | Cicilio and Cotilla-Sanchez, [Evaluating Measurement-Based Dynamic Load Modeling Techniques and Metrics](https://arxiv.org/abs/1907.07239), 2019; full online text, sections I-II and experimental conclusions | Demonstrates that response-fit metrics need validation before being used as accuracy proxies; not a mine-specific acceptance standard |
| MV4 | Jacob Eisenbarth, [A Testbed and Methods for Improved Power Plant Model Validation via PMU Terminal Measurements](https://digitalcommons.mtech.edu/grad_rsch/250/), 2020 Montana Tech MS thesis, repository abstract only | Describes measured voltage/frequency playback and comparison of simulated/measured P/Q; proposes parameter uncertainty treatment. Full thesis methods and results not read here |
| MV5 | EPRI, [Harmonics Load Modeling](https://opendss.epri.com/HarmonicsLoadModeling.html), technical note, accessed 2026-10-18, load/transformer damping discussion | Harmonic load representation and resistance assumptions alter resonance/damping; published defaults are not measured mining equipment data |
| MV6 | [Comprehensive Assessment of Large-Scale Photovoltaic Integration in an Isolated Mining Microgrid](https://www.scirp.net/journal/paperinformation?paperid=153670), 2026 publication, online sections 3.2-3.6 and 4 | Authors describe operating-data collection, ETAP base-case checks and renewable scenarios. Raw event replay evidence and an independent validation verdict not established by this reading |
| MV7 | Tjerk den Boer, [Validation of Dynamic Power System Models using Synchrophasor Measurements](https://repository.tudelft.nl/record/uuid:b871e4b7-451c-493e-9d2d-3d0b0d76a15e), 2020 TU Delft thesis, repository abstract only | Contrasts system-wide and hybrid validation and highlights operating-point/disturbance representation errors. Full thesis and mine applicability not verified |

All sources were accessed on 2026-10-18. The [source ledger](../../sources/entries/power-mining-validation-2026-10-18.yaml)
records retrieval limits. PDF page references are one-based file pages. The generic
measurement papers complement the mining examples; they are not evidence that a
particular mine followed every proposed practice below.

## What practitioners validate

MV1's data collection spans equipment schedules, drawings, nameplates, manufacturer
controls and operational philosophy. Its drive treatment distinguishes direct-on-line
machines from aggregate variable-speed loads. The described P/Q starting trajectory
and voltage/frequency disconnection behavior are application-specific inputs, not
a universal VSD model. Its validation discussion calls for comparison with site
tests, including machine control and process-load behavior (S, MV1 pp. 7-8, 13-16).

MV6 reports a diesel-only operating-point check before adding renewable scenarios
(S, sections 3.2/3.4). That establishes the authors' sequence, not proof that dynamic
parameters are identifiable from the reported operating points. MV4 and MV7 describe
using event measurements to test dynamics; MV3 warns that a small response error
alone need not identify the correct underlying model (S, inspected scopes above).

For Quantic this implies a validation ladder (I): verify equipment/connectivity and
operating state first; validate individual responses and measurement definitions;
then test coupled disturbances and protection; finally assess predictions across
the intended operating envelope. A pass at one rung does not certify another.

| Study question | Minimum model distinction | Minimum independent observation | Main open gate |
| --- | --- | --- | --- |
| Mill/conveyor start | Shaft/load torque and inertia, motor electrical states, starter topology | Terminal V/I/P/Q, speed if available, contactor/starter events | Torque/inertia and electrical transients cannot be inferred uniquely from a static dip |
| Islanded load pickup | Machine and turbine bases, governor/AVR, station secondary controls, limits | Raw frequency/reference, source P/Q, voltage, control/event states | Separate generator dynamics from station-level sharing and meter filtering |
| Weak-grid drive behavior | Supply impedance and controls, converter demand/current limits, disconnection | Simultaneous upstream/downstream phasors and event records | An ideal slack or unlimited constant-power element can hide the limiting mechanism |
| Protection sequence | As-found CT/VT/relay settings, latch/reset, breaker delay/failure | Relay event records and breaker indications | Fault current agreement alone cannot prove clearing or selectivity |
| Resonance and distortion | Source phases/spectra, passive loads, frequency-dependent R/L/C | Spectrum/phasors and switched capacitor/topology states | Arbitrary damping can produce a convincing but wrong resonance peak |
| PV/storage on a mine island | Actual grid-forming source, dispatch/headroom, current/control limits | Power balance, voltage/frequency and saturation/curtailment states | Added MW capacity does not prove available regulating reserve |

## Numbered validation requirements

### V-001: Define the prediction being validated

Evidence class: S (MV2, measurement objectives); Quantic proposal: I.
R-IDs: R-042, R-045, R-049. Matrix: G10, G11, T1, M2.
State the question, outputs, network boundary, model revision and operating envelope
before selecting data or fitting parameters.
Acceptance: a proposed mill-start study lists required outputs, observable states
and excluded phenomena; a reviewer can distinguish voltage-dip validation from
speed/torque and equipment-safety validation. Missing evidence is U, not a pass.

### V-002: Preserve parameter origin and effective value

Evidence class: S (MV1 p. 7); Quantic proposal: I.
R-IDs: R-002, R-016, R-041. Matrix: D2, D11, D12, M4.
Keep nameplate, manufacturer calculation, typical assumption, fitted value and
site measurement distinct, with units, base, date and applicable equipment revision.
Acceptance: replace one assumed motor parameter with a measured value and trace
the affected runs. The ledger shows both values and their uncertainty; a library
match must not silently promote an assumption into verified site data.

### V-003: Verify physical topology and operating state independently

Evidence class: S (MV1 p. 7; MV6 sections 3.2/3.4); Quantic proposal: I.
R-IDs: R-001, R-003, R-004, R-006. Matrix: D1, D4, D5, G2, G7.
Reconcile drawings, terminal connectivity, switch indications and actual dispatch
at the measurement time; retain uncertainty in undocumented connections.
Acceptance: an original fixture contains a deliberately incorrect open tie and
transformer connection. The review detects both before numerical calibration;
adjusting impedance to compensate for wrong topology is rejected with named evidence.

### V-004: Validate the pre-event operating point

Evidence class: S (MV6 sections 3.2/3.4; MV7 abstract); Quantic proposal: I.
R-IDs: R-007, R-017, R-018, R-045. Matrix: S1, S6, S9, T6.
Match supply, loading, taps, controller modes and relevant losses before applying
the disturbance; record algebraic and derivative residuals separately.
Acceptance: reproduce a synthetic no-event record without material drift under
the declared numerical gate, then deliberately perturb one initial control state.
Diagnose that mismatch separately from a fitted dynamic time constant.

### V-005: Define the measurement chain and alignment

Evidence class: S (MV3 section II; MV4 abstract); Quantic proposal: I.
R-IDs: R-020, R-044, R-049. Matrix: G5, G12, T1, T4.
Record sensor location, CT/VT ratio, phase reference, sign, RMS/phasor definition,
time basis, sample interval, missing-data flags and known delay/filtering.
Acceptance: compare original signals with a declared ratio inversion and known
time offset. Recover only the allowed calibrated transformation and retain the raw
record. Unrestricted time warping must not erase a physically incorrect trip time.

### V-006: Use load models matched to the question

Evidence class: S (MV1 pp. 8/13; MV3 section I); Quantic proposal: I.
R-IDs: R-009, R-015, R-021, R-049. Matrix: S7, M1, M2, T1.
Distinguish static ZIP or prescribed P/Q trajectories from motors with electrical
and mechanical states and from controlled converters. State aggregation boundaries.
Acceptance: apply the same authored voltage disturbance to a fixed-admittance load,
a constant-power variant and a dynamic motor. Differences in recovery are labelled
model differences; agreement in one operating point cannot make them interchangeable.

### V-007: Identify mechanical and starter behavior explicitly

Evidence class: S (MV1 pp. 8/16; [model mapping](comparison-mapping.md), section A); Quantic proposal: I.
R-IDs: R-009, R-015, R-016, R-019. Matrix: M1, M2, M3, M4.
Record combined versus separate inertia, torque-speed load, starter connections,
bypass logic and initial shaft state. Keep fitted acceleration time distinct from
computed acceleration.
Acceptance: C-01/C-02 comparisons preserve mechanical curves and shaft continuity;
altering inertia and altering starting voltage must be distinguishable using the
declared observables. If no speed/torque evidence separates them, report the ambiguity.

### V-008: Validate VSD demand and disconnection separately

Evidence class: S (MV1 pp. 13-14); Quantic proposal: I.
R-IDs: R-009, R-019, R-021, R-044. Matrix: S7, M3, T1, P4.
Separate process demand, input converter control/current limit, speed control and
voltage/frequency trips. A measured P/Q trajectory is a prescribed replay, not a
predictive drive model outside the conditions in which it was measured.
Acceptance: replay an original demand trace, then change source impedance and
exercise a declared synthetic current limit and trip/reset rule. The replay and
closed-loop predictions are distinct variants, with all limiting events recorded.

### V-009: Separate machine, governor, AVR and station control

Evidence class: S (MV1 pp. 7-8/16; MV2); Quantic proposal: I.
R-IDs: R-010, R-017, R-018, R-022. Matrix: S6, T1, T2, T6.
Identify each controller's inputs, references, power base, limits, time scales and
initial states. Do not count a station-level regulation effect twice in a governor.
Acceptance: C-07 remains a classical-source/first-order-governor test. Adding AVR
or secondary sharing creates a named extension with independent excitation and
load events; fitting one loop must not conceal an incorrect reference in another.

### V-010: Declare grid strength and regulating reserve

Evidence class: I (derived from MV1 islanded context, MV6 sections 3.5/4 and R-010).
Quantic proposal: I. R-IDs: R-004, R-010, R-017, R-022. Matrix: S6, S9, T1.
Define the actual reference/forming source, online units, source impedance,
dispatch/headroom and control/current limits for each connected or islanded state.
Acceptance: an original loss-of-source event exposes a generation deficit and
active limits; no implicit physical slack supplies it. Sweep declared source
impedance and operating reserve without treating a single stiffness scalar as a
complete substitute for converter/control dynamics.

### V-011: Reproduce the disturbance, not only its nominal label

Evidence class: S (MV7 abstract; MV1 p. 16); Quantic proposal: I.
R-IDs: R-019, R-020, R-027, R-049. Matrix: T1, P4, M2, T6.
Capture event inception, fault/transition type, clearing topology, command versus
physical operation and initial/final states; distinguish uncertain events from
uncertain model parameters.
Acceptance: replay an original two-stage switching record; a one-stage surrogate
is diagnosed even if its final voltage agrees. Unknown event timing is carried
as an uncertainty interval rather than silently tuned as a motor constant.

### V-012: Keep calibration and independent evaluation separate

Evidence class: I (MV3 metric-validity concern; MV4 calibration discussion).
Quantic proposal: I. R-IDs: R-016, R-047, R-048, R-049. Matrix: M4, X-4, T1.
Declare which complete events, operating points and outputs are used to fit a
model and which are withheld for evaluation. Random samples from the same event
must not masquerade as independent operating evidence.
Acceptance: a model fitted to one original pickup event is evaluated unchanged
on a second declared loading state and a source-loss event. Record failures and
revisions; a refit makes a new model revision and invalidates the prior holdout label.

### V-013: Test whether the metrics discriminate model errors

Evidence class: S (MV3 sections II and conclusions); Quantic proposal: I.
R-IDs: R-044, R-048, R-049. Matrix: G12, M2, T1, P4.
Select metrics for the physical prediction, including transient windows and event
times. Do not make one correlation or whole-record fit score a universal verdict.
Acceptance: use original signals with a wrong gain, delayed trip and incorrect
oscillation frequency. The chosen metric set identifies each material error;
an excellent long steady-state fit cannot hide a failed acceleration or delayed clearing.

### V-014: Report uncertainty and non-identifiability

Evidence class: S (MV4 abstract, uncertainty proposal; MV3 parameter dependency discussion).
Quantic proposal: I. R-IDs: R-016, R-045, R-048, R-050. Matrix: M4, S22, X-4.
Record measurement and parameter uncertainty, bounds, sensitivity and competing
parameter sets that fit the available evidence. A single optimiser output is
not proof of uniquely identified machine parameters.
Acceptance: a declared synthetic underdetermined fit reports more than one feasible
parameter set and their predictive spread on a second event. Any confidence interval
states its noise model and method; missing evidence does not produce invented precision.

### V-015: Validate protection against as-found measurements and settings

Evidence class: S (MV1 pp. 7/15; R-053/R-054); Quantic proposal: I.
R-IDs: R-023, R-026, R-027, R-053, R-054. Matrix: P1, P4, P6, P7, P8, P9.
Keep CT/VT wiring, firmware/model revision, actual settings and breaker behavior
separate from proposed coordination settings. Use recorded operation evidence
without assuming that a simulated fault magnitude proves selectivity.
Acceptance: C-03 and original distance/differential fixtures expose pickup, reset,
trip and breaker-open states independently. A changed CT polarity or failed breaker
must alter the predicted sequence visibly, with source and setting revisions retained.

### V-016: Validate harmonic sources and passive damping independently

Evidence class: S (MV5 load/transformer harmonic discussion); Quantic proposal: I.
R-IDs: R-014, R-031, R-034, R-044. Matrix: H1, H2, S11.
Separate harmonic injections/phases from background admittance, transformer/line
frequency dependence and switched compensation. Arbitrary damping is not a
substitute for the correct network or measured load mix.
Acceptance: C-05's source cancellation and capacitor-open cases distinguish
injection error from network resonance error. Report frequency-grid refinement
and sensitivity to uncertain R(f); native defaults remain assumptions until sourced.

### V-017: Prove numerical convergence and model equivalence separately

Evidence class: I (R-048/R-049 and comparison-case gates); Quantic proposal: I.
R-IDs: R-020, R-047, R-048, R-049. Matrix: M2, T1, T4, H1, C6.
Use independent original oracles and timestep/mesh/frequency refinement before
assigning discrepancies to physical parameters. Matching model names is insufficient.
Acceptance: refine C-01/C-07 numerical trajectories while retaining equations;
classify a native flux-state or limiter mismatch as model mismatch even after
both solvers converge. Record effective auto-corrections and measurement filters.

### V-018: Issue a scoped validation decision and invalidate it on change

Evidence class: I (MV1 p. 18 ongoing validation; R-042/R-052).
Quantic proposal: I. R-IDs: R-003, R-041, R-042, R-045, R-052. Matrix: D12, G10, G11.
Publish evidence origin, tested conditions, known failures, unsupported predictions,
revision/hash and next evidence required. Distinguish numerical verification,
calibration, measured validation and compliance review.
Acceptance: a source-setting or equipment-model revision invalidates dependent
validation records. A report can state steady-state validated/dynamics U without
showing a blanket green status or inventing standards compliance.

## Validation record and unresolved evidence

For each future study retain: purpose and V/R/matrix IDs; topology/parameter and
measurement manifests; effective model version; raw and processed channels; event
list; training/evaluation split; uncertainty assumptions; metrics and gates fixed
before fitting; numerical refinement; deviations and a scoped engineering decision.
This is a proposed record format (I), not an existing client/test record.

| Gap (U) | Evidence needed before the associated claim |
| --- | --- |
| Copperbelt mill, conveyor and diesel/renewable measured responses | Authorised site records with sensor metadata, settings and operating state; no Zambia dataset is supplied here |
| Exact native commercial equation mappings | Close the model/base/initialisation/limit fields in comparison-mapping.md and perform legitimate versioned runs |
| Published mine simulation reproducibility | Obtain permitted model and raw measurement evidence; a paper's normal-state comparisons alone do not certify dynamic predictions |
| Safe site test procedures and engineering thresholds | Site owner/test engineer approval and the applicable readable manufacturer/rule documents; this research does not prescribe a live disturbance test |
| Standards and local compliance | WP-2.21 source/edition/clause mapping; no numeric safety or trip setting is inferred from these papers |
| Full thesis methods | MV4/MV7 abstracts are methodological leads only until their full texts are inspected |

The immediate research priority is a validation manifest for the original cases,
followed by data-supported mine-specific model envelopes. No particular commercial
engine, fitted parameter set or field result is certified by this document.
