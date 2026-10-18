# MATLAB, Simulink and Simscape Electrical

WP-2.27, ChatGPT, 2026-10-18. S statements below come from public MathWorks
documentation unless labelled I/U. Documentation version R2026b is visible on
the inspected current help. No licensed application or example was executed.

## 1. Identity: versions, licences and platform boundaries

MATLAB is the surrounding programming/data environment; Simulink supplies the
block-model environment [SL1/SL2]. Simscape supplies physical-network technology;
Simscape Electrical adds electrical/electronic/electromechanical components
[SL3/SL4/SL5]. The published requirements list MATLAB, Simulink and Simscape
for Simscape Electrical, with Mac/Windows/Linux platform families [SL4]. Exact
OS, compiler and add-on compatibility still require the selected release.

These are proprietary products. Simulink Coder, control-design, real-time and
FMU-export products are separate capability/entitlement questions, not evidence
of an open reusable simulator core [SL11/SL16/SL18/SL20]. Acceleration uses code
generation technology but does not require Simulink Coder merely to accelerate
the simulation; its generated target is for acceleration [SL11]. Do not equate
that target with production embedded code or a redistribution grant (I).

Specialized Power Systems was removed in R2026a. Current migration guidance
offers a conversion assistant and an HTML report of fully/partly/unsupported
blocks; manual conversion remains necessary for unsupported content [SL6]. A
legacy powergui example is therefore not a current-native Simscape workflow (I).
No prices, licence agreement or runtime redistribution rights were accepted here.

## 2. Sources

All accessed 2026-10-18. Primary product help/requisites, not recovered source.
Pages were read for the indicated topic, not a claim to have audited every link.

| ID | Topic / primary source |
| --- | --- |
| SL1 | [Simulink Editor](https://www.mathworks.com/help/simulink/slref/simulinkeditor.html), R2026b, editing/hierarchy/properties/diagnostics |
| SL2 | [Simulink tools](https://www.mathworks.com/help/simulink/slref/simulink-concepts-tools.html), library/data/logging tools |
| SL3 | [Simscape Electrical docs](https://www.mathworks.com/help/simscape-electrical/index.html), R2026b, component/application scope |
| SL4 | [Simscape Electrical prerequisites](https://www.mathworks.com/support/requirements/simscape-electrical.html), required products/platforms |
| SL5 | [Physical-network principles](https://www.mathworks.com/help/simscape/ug/basic-principles-of-modeling-physical-networks.html), ports/units |
| SL6 | [Upgrade SPS models](https://www.mathworks.com/help/simscape-electrical/ug/upgrade-sps-models-to-use-simscape-blocks.html), R2026b, removal and conversion report |
| SL7 | [How Simscape simulation works](https://www.mathworks.com/help/simscape/ug/how-simscape-simulation-works.html), validation/network equations/initial targets |
| SL8 | [Solver Configuration](https://www.mathworks.com/help/simscape/ref/solverconfiguration.html), DAE reduction/local solvers/settings |
| SL9 | [Choose a solver](https://www.mathworks.com/help/simulink/ug/choose-a-solver.html), fixed/variable and continuous/discrete choices |
| SL10 | [Zero-crossing detection](https://www.mathworks.com/help/simulink/ug/zero-crossing-detection.html), event location/chattering limits |
| SL11 | [How acceleration works](https://www.mathworks.com/help/simulink/ug/how-the-acceleration-modes-work.html), simulation-target versus Coder boundary |
| SL12 | [Algebraic-loop concepts](https://www.mathworks.com/help/simulink/ug/algebraic-loops.html), direct feedthrough and loop resolution |
| SL13 | [Sample time](https://www.mathworks.com/help/simulink/ug/what-is-sample-time.html), timing semantics |
| SL14 | [Transfer Fcn](https://www.mathworks.com/help/simulink/slref/transferfcn.html), polynomial/state interpretation |
| SL15 | [Continuous system modeling](https://www.mathworks.com/help/simulink/ug/modeling-a-continuous-system.html), integrator/feedback/transfer realization |
| SL16 | [Simulink Control Design](https://www.mathworks.com/products/simcontrol.html), operating points/linearization/tuning product scope |
| SL17 | [FMU importing](https://www.mathworks.com/help/simulink/ug/work-with-fmi-in-simulink.html), version and ME/CS distinction |
| SL18 | [FMU export](https://www.mathworks.com/help/fmuexport/ug/export-simulink-models-to-functional-mock-up-units.html), export-specific product route, FMI 2/3 |
| SL19 | [SimulationInput](https://www.mathworks.com/help/simulink/slref/simulink.simulationinput.html), per-run model/variable changes |
| SL20 | [parsim](https://www.mathworks.com/help/simulink/slref/parsim.html), parallel/serial simulation and supporting requirements |
| SL21 | [Physical-signal unit propagation](https://www.mathworks.com/help/simscape/ug/physical-signal-unit-propagation.html), dimensional operations |
| SL22 | [Choosing electrical blocks](https://www.mathworks.com/help/simscape-electrical/ug/choose-blocks-to-model-electrical-systems.html), fidelity and component selection |
| SL23 | [Simscape Electrical product](https://www.mathworks.com/products/simscape-electrical.html), power electronics, machines and SPICE conversion scope |
| SL24 | [Electrical release notes](https://www.mathworks.com/help/simscape-electrical/release-notes.html), migration/version context; no downloaded binary |

## 3. Architecture and data model

Simulink diagrams contain blocks, directed signals and hierarchical subsystems;
parameters and data are inspectable in dedicated tools [SL1/SL2]. Sample times
govern evaluation instants and discrete updates [SL13]. A feedback line can
contain dynamic state or form an algebraic loop through direct-feedthrough
blocks; drawing a loop does not supply a delay [SL12/SL15].

Simscape's physical connections are not directed signal wires. Conserving ports
share Across quantities and balance Through quantities; physical-signal ports
and Simulink converters carry directed information with units [SL5/SL21]. The
solver constructs algebraic/differential equations and removes unneeded variables.
Initial targets have priorities and need not all be achieved; a consistent solved
initial state is distinct from the requested target [SL7].

Each topologically separate physical network requires one Solver Configuration
block [SL7/SL8]. A local solver applies to its connected network and exposes its
state to the global environment as sample-based/discrete behavior [SL8]. This is
not a claim that continuous physics has disappeared (I): integration and exchange
semantics have changed. Preserve solver configuration as a study input.

Original Quantic inference (I): store a signal graph separately from physical
connectivity, geometric layout and numerical state. Typed ports, identity,
parameters, units, clocks, initial conditions and external resources belong in
the executable model; graphical coordinates alone do not specify equations.
Compilation/reduction and exported-code internals remain proprietary/U beyond
the processes documented above.

## 4. Element catalogue and fidelity

| Element family | Public semantics / units | Modeling boundary |
| --- | --- | --- |
| Sum, gain, integration, transfer representation | Signal computation and continuous state [SL14/SL15]; transfer coefficients depend on declared variable/time convention | Transfer Fcn uses a particular zero-state realization; an arbitrary physical initial state needs explicit state treatment |
| Sampled/discrete blocks | Sample time and update instants [SL13] | Sampling, holding and delay are not interchangeable; exact scheduling needs release-specific tests |
| Physical passive elements and sources | Electrical voltage V/current A and constitutive behavior selected by block fidelity [SL5/SL22] | Reference/ground, orientation and parasitics are physical model choices |
| Semiconductors / converters | Ideal/switched-linear/nonlinear model families, electrical and thermal choices [SL6/SL22/SL23] | An averaged converter does not resolve every switching edge or junction waveform |
| Machines / drives | Electromechanical model and drive application scope [SL3/SL23] | Exact winding, saturation, torque/inertia and control parameters need the selected block documentation |
| Transformers / conductors / three-phase systems | Electrical component families and composite representation [SL6/SL22] | Frequency range, connection, zero-sequence/neutral and distributed versus lumped fidelity need separate qualification |
| Solver/initialisation objects | Equation formulation, consistency tolerance, index reduction and local step [SL8] | Values are numerical study settings, not universal engineering defaults |
| Measurement and bridges | Sensors and physical-signal/Simulink units [SL5/SL21] | Unit conversion and observation point must match the quantity reported |

No numeric device value or solver tolerance is adopted. A manufacturer model,
its library licence and its usable operating region require separate evidence.

## 5. Studies, solvers and outputs

| Study question | Public method / inputs / result | Evidence and limit |
| --- | --- | --- |
| Continuous/discrete system response | Fixed or variable step selected for states, events and sample times | SL9/SL13; numerical step is not output display interval |
| Nonlinear physical transient | DAE assembly, consistent initial solve, integration and transient consistency | SL7/SL8; singular/overconstrained networks need diagnostics |
| Switching and hybrid events | Locate discontinuities with zero crossings; adaptive/nonadaptive choices and excessive-crossing behavior | SL10; chattering can stop or slow a simulation, no universal cure inferred |
| Local physical solver | Backward Euler, trapezoidal or partitioning options, with fixed-cost settings available | SL8; stability, damping and cost differ. No step/default copied |
| Transfer/feedback study | Integrator and rational transfer realizations | SL14/SL15; actual initial states and direct feedthrough matter |
| Linearisation/control design | Operating points, linearisation, response estimation and tuning in the separate Control Design product | SL16; not a claim every block/toolbox supports every operation |
| Simulation acceleration | Normal versus generated acceleration targets | SL11; production deployment and target hardware remain separate |
| Programmed run families | SimulationInput varies model data/settings, parsim runs multiple cases | SL19/SL20; supporting licences/workers/version must be recorded |
| Model exchange/co-simulation | FMI version, ME versus CS and supported modes explicit | SL17/SL18; import/export or equal signal names do not establish timing/ABI parity |
| Electrical power/motor model | Component fidelity chosen for the electrical/control question | SL3/SL22/SL23; a system-level switching model is not automatically device/EMI or grid-protection validation |

Original analysis implications (I): obtain the operating point before small-signal
linearisation; compare state and event timing as well as plotted outputs; retain
solver tolerances, resets and rejected steps where available; distinguish an
algebraic constraint from physical energy storage. A diagram with feedback is
not enough to justify a particular ODE or DAE solution strategy.

For rectifiers, converters and motor drives, the independent model must identify
whether it resolves switching, uses an averaged law or uses another abstraction
(I). A chosen 50/60 Hz fundamental does not determine the required time step
for a high-frequency converter. No MHz capability/accuracy is asserted from a
product family name; device parasitics, solver and observation bandwidth require
evidence and measurement validation.

## 6. Workflow and interface

Documented, not an observed application session: use the Editor to place/connect
blocks, navigate hierarchy and edit parameters. Property Inspector, block dialogs
and Model Data Editor expose different views of model data [SL1]. Library Browser
finds blocks; Model Explorer handles hierarchy/workspace data; Simulation Data
Inspector logs/compares runs [SL2]. Errors can highlight implicated blocks [SL1].

Configure states/solver/sample times before a run [SL8/SL9/SL13]. For physical
models, check network configuration and units, inspect consistent initial targets
and then simulate [SL7/SL21]. Controls and physical sensors exchange values through
declared converters. Trace units and signal timing before interpreting a Scope.

SimulationInput provides per-run changes without making an edited picture the
sole run record [SL19]. parsim has serial/parallel operation; accelerated modes
trade execution behavior and constraints [SL11/SL20]. Use FMI import and export
as separately qualified workflows [SL17/SL18]. Legacy SPS conversion reports
explicitly identify unsupported content [SL6].

Original Quantic workflow proposal (I): select model family/fidelity; build and
validate typed connectivity; set source/initial and numerical assumptions; run
with progress/diagnostics; inspect states/events/energy and compare references;
save immutable run inputs/results. UI artwork, menus and proprietary file layout
are not copied. The independent interface should make these relationships clear
without requiring users to infer simulation state from a moving picture.

## 7. User value and complaints

No representative user survey was read. Our evaluation (I): explicit solver and
physical-model documentation helps trace assumptions; integrated hierarchy/data
inspection and run comparison reduce context switching [SL1/SL2/SL7/SL8]. These
are inferred workflow benefits, not measured productivity claims.

Concrete source-documented constraints are the SPS migration/unsupported-block
report [SL6], initial-target feasibility [SL7], algebraic loops [SL12], excessive
zero-crossing behavior [SL10] and separate generation/exchange capabilities
[SL11/SL18]. They indicate questions a user must resolve, not a defect prevalence
or performance ranking. Support quality, licence pain, customer satisfaction and
real model execution cost remain U in this dossier.

## 8. Engines implied and independent routes

Original engine split (I): typed model compiler; causal scheduling and clock
handling; physical-network equation construction/reduction; ODE/DAE/nonlinear
solvers; consistent initialisation; event detection and state reset; device/model
library; analysis/linearisation; waveform/measurement and provenance; code/FMI
adapters with explicit capabilities. The evidence basis is SL5-SL21.

The [peer dossier section 8](other-products.md#8-engines-open-licences-and-owned-references)
records actual dated licences and candidate boundaries: ngspice for netlist
circuits, python-control for control algebra/analysis, SciPy for numerical methods,
SymPy for symbolic work, and external Xcos/OpenModelica workflows. None supplies
a complete validated Simulink/Simscape replacement merely by being installed.

Owned-reference leads from the existing power library map: Pillage 1995, Najm
2010 and Vlach 1983 for circuit numerical methods; Astrom/Murray 2008 for feedback;
Mohan 1995, Rashid 2014 and Bose 2002 for converters/drives. These are search/ownership
leads, not read-page assertions or authority for present vendor defaults. No
private text was accessed/copied in this WP.

Original proposed fixtures (I, unrun): RC/RLC analytic responses with nonzero
initial state; equivalent transfer and state-space realizations with state
mapping; an algebraic loop with known solution and an inconsistent loop;
sampled feedback with distinct hold/delay; switch event between output samples;
converter energy balance at two fidelity levels; machine torque/energy balance;
FMU time/units/capability mismatch. Declare references and justified tolerances
before executing comparisons. Shared-backend agreement is not independence.

## 9. Gaps and closure routes

| Gap | Evidence or action needed |
| --- | --- |
| SG1 | Lawful exact release/licence/compiler environment, selected add-ons and any deployment rights; no application access in this WP |
| SG2 | Exhaustive block/parameter/default coverage and proprietary compiled representation remain unavailable; qualify a bounded subset using public block docs |
| SG3 | Exact device/machine/parasitic/thermal parameter evidence and model-library rights before simulation claims |
| SG4 | Independent DAE/event/initialisation references and original numerical tests; no solver parity established |
| SG5 | Exact SPS project conversion losses and source/target versions; removal is documented, conversion losslessness is not |
| SG6 | FMI version/mode/platform/clock and binary rights, code-generation eligibility and target tests; no import/export execution |
| SG7 | Actual user evidence, runtime performance, HIL deadlines, measurement bandwidth and site validation; public features are not measured results |
| SG8 | Owned-book page verification and modern methods/standards gaps; no copied examples or assumed engineering thresholds |

Building remains parked. The dossier specifies evidence and independent design
needs; it does not adopt a proprietary architecture, default or interface.
