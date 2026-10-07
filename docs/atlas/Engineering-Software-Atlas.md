# Engineering Software Atlas

**Electrical, electronics, mechanical, civil, information technology and their intersections**  
Research date: 7 October 2026 · Prepared for Peter Kabamba

## The central finding

An open engineering platform is feasible as a collection of interoperable workbenches. Replacing every established commercial suite feature-for-feature is a much larger undertaking. The strongest starting position is to combine existing open numerical engines with excellent modelling interfaces, trustworthy libraries, reproducible studies and clear reports.

The market is not empty. Open projects already address circuits, power networks, CFD, structural analysis, CAD, building energy, robotics and numerical computing. The opportunity is often the last mile: making a correct analysis understandable, repeatable, connected to the engineer's other tools and practical without a specialist maintaining the installation.

This atlas contains **48 subfields and ten shortlist entries per field: 480 field-tool entries**: 36 engineering subfields and 12 information technology subfields. Entries include products, modules and a few explicitly identified toolchains. These are not 480 independent companies or interchangeable applications. A suite can appear in multiple fields because it genuinely serves multiple workflows.

## How to interpret the research

“Top ten” means an **unranked research shortlist** selected for engineering relevance, breadth, established workflow presence, distinctive capability or value as an open implementation reference. There is no defensible global market-share ranking available here, and no numerical ranking is invented. Commercial incumbents dominate many lists; open alternatives are included deliberately because the purpose is to plan an open platform.

Product descriptions are based on public primary sources and engineering analysis. No commercial binaries were reverse-engineered, and no comparative performance benchmark was run. “Best-fit job” identifies intended use; “boundary” identifies a practical distinction to investigate, not a measured product defect. Scientific methods describe the field unless a specific implementation is documented. Do not read a field-level method as proof that every listed tool implements it.

The workbook separates three evidence levels: **product/family named in a retrieved source**, **vendor reference only**, and **candidate requiring direct verification**. A retrieved vendor page is not proof of every edition, feature, license term or current sales status. Product names and ownership change; recognizable families are retained and edition-sensitive claims are avoided. Links marked as candidates are research leads, not verified current offerings. This is a substantial landscape and architecture study, not a completed procurement qualification of 360 entries.

License labels: **P** proprietary commercial; **F** no-cost proprietary distribution/IDE; **O** open-source project; **M** mixed editions/access or component-dependent terms; **O/M** open core with commercial additions; **S** source available with restrictions. These are screening labels, not a license audit. An open project's models, plugins, datasets and linked libraries can have different terms.

The taxonomy covers the requested main disciplines, plus information technology, at a practical software-workflow level. It is not every academic specialization. Photonics, acoustics, semiconductor process TCAD, fire, offshore engineering, specialist rail systems and detailed construction cost/scheduling can each justify additional atlases. Chemical, petroleum and biomedical engineering are outside the main scope, although several underlying methods overlap.

## How the disciplines connect

| Intersection | What joins together | Software consequences |
|---|---|---|
| Electrical + mechanical | Motors, generators, actuators, thermal limits | Couple field calculations, motion, circuits and cooling |
| Electronics + mechanical + control | Mechatronics, robotics, embedded products | Exchange dynamics, sensor, timing and control models |
| Electrical + civil | Substations, distribution assets, earthing and building services | Connect network models to spatial, structural and installation data |
| Mechanical + civil | Structures, HVAC, pipelines and hydraulics | Reuse continuum mechanics and flow methods, with different design rules |
| All four | System optimization, reliability and digital representations of assets | Shared units, identifiers, revisions, uncertainty and provenance |
| Any discipline + IT | Networks, data, security and operations behind every engineering system | See the [information technology branch](#information-technology-branch) |

“Electromechanical” usually emphasizes conversion between electrical and mechanical energy. “Mechatronics” adds electronics, sensing, software and control to the mechanical system. Structural engineering sits within civil engineering but shares much of its mechanics and numerical machinery with mechanical FEA. Control engineering is a cross-cutting discipline, not merely PLC programming.

## What makes engineering software work

A useful decomposition has eight layers:

1. **Project and domain model.** An electrical bus, material, beam, valve or robot joint must have an identity, units, relationships and a revision history.
2. **Model construction.** A schematic, CAD model, mesh, network diagram, block diagram or worksheet captures assumptions in a form the engineer can inspect.
3. **Physical and mathematical formulation.** Convert the model into equations, constraints, graph operations or events. Choose the approximations explicitly.
4. **Numerical execution.** Solve linear/nonlinear equations, integrate dynamics, optimize, process geometry or advance events.
5. **Domain libraries.** Materials, devices, curves, equipment, weather, terrain, rules and standards provide much of the useful engineering content.
6. **Results and diagnostics.** Show quantities, residuals, convergence, violated assumptions, uncertainty and engineering meaning, not just colored pictures.
7. **Interoperability and reporting.** Exchange models, preserve identifiers, and produce a calculation record another engineer can reproduce.
8. **Product operation.** Installation, offline use, plugins, updates, collaboration, performance and support make the system practical.

These layers explain why implementing a formula does not recreate ETAP, MATLAB or Abaqus. Conversely, they explain why a small team can build a valuable specialized product without inventing an entirely new solver.

## The recurring mathematical engines

| Engine family | Core idea | Where it recurs | Useful open foundations |
|---|---|---|---|
| Dense/sparse linear algebra | Solve Ax=b; eigenvalues; factorizations | Almost every numerical field | BLAS/LAPACK, Eigen, SuiteSparse, PETSc |
| Nonlinear equations | Iterate until a residual is sufficiently small | Load flow, semiconductor circuits, nonlinear FEA | PETSc SNES, SciPy, SUNDIALS components |
| ODE/DAE integration | Advance differential and algebraic states through time | Controls, circuits, multibody, thermal systems | SUNDIALS, SciML, OpenModelica |
| PDE discretization | Approximate fields on a mesh/grid/basis | Fluids, stress, electromagnetics, heat | OpenFOAM, FEniCSx, deal.II, MOOSE, Elmer |
| Computational geometry | Robust intersections, topology and constraints | CAD, CAM, PCB, BIM, survey | Open CASCADE, CGAL, Gmsh, GDAL/PROJ |
| Graph algorithms | Connectivity, routing, dependencies and traversal | Circuits, networks, wiring, scheduling | Domain-specific graph models and general graph libraries |
| Optimization | Choose variables subject to objectives/constraints | Dispatch, design, control, transport | HiGHS, IPOPT, JuMP, Pyomo, CasADi |
| Discrete events | Jump between state-changing events | PLC simulation, logistics, reliability | SimPy, JaamSim, event schedulers |
| Signal algorithms | Transform, filter, estimate and detect | Communications, controls, vibration | SciPy, FFTW, GNU Radio |
| Rules and semantics | Evaluate structured requirements | Code design, DRC, BIM checks, protection | A versioned rules engine plus licensed source data |

These are candidate building blocks, not a license-compatible bundle. PETSc documents separate linear, nonlinear and time-integration facilities; FMI documents model exchange and co-simulation interfaces. The integration architecture must respect these boundaries. [PETSc documentation](https://petsc.org/release/manual/) · [FMI specification](https://fmi-standard.org/docs/3.0.2/)

### Load flow: how the electrical diagram becomes a solver

Represent buses, branches, transformers, generators and loads as structured data. Choose bases and convert parameters consistently to per-unit quantities. Assemble the complex bus-admittance matrix. Specify the unknowns and constraints for reference, PV and PQ buses.

For each bus, the complex-power relation is:

`S_i = V_i × conjugate(Σ_j Y_ij V_j)`

Given specified active/reactive injections, evaluate the mismatch at the current voltage estimate. Newton–Raphson constructs a Jacobian, solves for an update and repeats. A production implementation needs limit handling, island detection, transformer phase shifts, sparse matrix ordering, diagnostics and a policy for difficult convergence. Three-phase unbalanced models require more detailed phase and connection representations.

The product then maps voltages and branch flows back onto the diagram and explains overloads and assumptions. Optimal power flow adds controllable decisions and constraints. Short-circuit and EMT studies are separate formulations; they are not simply new colors on the same load-flow result. [ETAP load-flow scope](https://etap.com/product/load-flow-software) · [pandapower](https://www.pandapower.org/)

### Structural FEA: how a part becomes a stiffness system

Define geometry, materials, supports, loads and the intended idealization. A thin beam, shell and 3D solid are different models. Mesh the domain, choose shape functions, integrate element contributions and assemble a global system. For small-deformation linear statics, the familiar result is `K u = f`.

Applying boundary conditions incorrectly can create an artificial constraint or a singular system. After solving displacements, calculate strains and stresses, then evaluate appropriate engineering criteria. Nonlinear geometry, contact and plasticity require incremental loading and iteration; transient dynamics adds mass, damping and time integration.

A meaningful result includes mesh sensitivity, equilibrium checks and modelling assumptions. Peak stress at an ideal sharp corner may be singular; reporting ever-larger mesh-refined peaks as an increasingly precise failure prediction is a mistake. CSI's analysis manual usefully distinguishes the shared analysis engine from the product-specific modelling and design workflows. [CSI analysis reference](https://docs.csiamerica.com/manuals/etabs/Analysis%20Reference.pdf)

### CFD: conservation plus approximations

Discretize mass, momentum and energy conservation over a geometry. In a finite-volume approach, fluxes across cell faces provide a conservative accounting framework. Pressure and velocity must be coupled consistently. Turbulence, multiphase interfaces, combustion or compressibility introduce additional models and numerical choices.

Two runs with identical geometry can disagree because they use different meshes, near-wall treatments, boundary conditions or closure models. Small residuals only show progress toward the chosen discretized equations. Check global conservation and engineering outputs, then refine the mesh and time step. OpenFOAM exposes a C++ implementation and finite-volume framework, making it an unusually useful learning and integration reference. [OpenFOAM resources](https://openfoam.org/resources/) · [Source documentation](https://cpp.openfoam.org/)

### CAD and PLCs show why not everything is a numerical solver

CAD must maintain topology and geometric tolerances through editing, intersections and Boolean operations. The hard cases often involve nearly coincident geometry, tiny edges and changes that invalidate feature references. Open CASCADE provides an open C++ kernel, while FreeCAD supplies a much larger application around it. [Open CASCADE introduction](https://dev.opencascade.org/sites/default/files/pdf/Preliminaries.pdf) · [FreeCAD source documentation](https://www.freecad.org/api/)

A PLC engineering environment instead parses programs, checks types, compiles or interprets logic, configures I/O and supports runtime debugging. Its control logic may use Structured Text or Ladder Diagram; that says nothing definitive about the IDE's own implementation language. SCADA then adds supervisory state, communication quality, alarms and historical data. It is not interchangeable with the deterministic controller underneath it. [CODESYS development system](https://store.codesys.com/en/codesys.html) · [Ignition architectures](https://inductiveautomation.com/ignition/architectures)

## What is MATLAB actually written in?

There are several different questions hiding inside that sentence.

| Layer or period | What the public evidence establishes |
|---|---|
| Original academic MATLAB | Cleve Moler's matrix program was written in **Fortran**. |
| Early commercial MATLAB | Jack Little and Steve Bangert rewrote and extended it in **C**. |
| User programs | Engineers write the **MATLAB language**; this is not the implementation language of the whole application. |
| Modern execution | MathWorks documents a JIT execution engine; MATLAB code is executed through that runtime rather than simply being C source. |
| Numerical libraries/extensions | MATLAB documents BLAS/LAPACK use and C/C++/Fortran MEX interfaces. Interface support alone does not prove the language of every internal component. |
| Desktop interface | MathWorks says the R2025a desktop/graphics rebuild uses **JavaScript and HTML instead of Java**, separating the front end from execution. |
| Complete current codebase | A definitive, component-by-component source-language inventory was not established from public sources. Native C/C++ internals are a reasonable architectural hypothesis, not a complete verified inventory. |

Sources: [Moler's history](https://www.mathworks.com/company/technical-articles/a-brief-history-of-matlab.html), [origins](https://www.mathworks.com/company/technical-articles/the-origins-of-matlab.html), [execution engine](https://blogs.mathworks.com/loren/2016/02/12/run-code-faster-with-the-new-matlab-execution-engine/), [LAPACK](https://www.mathworks.com/help/matlab/math/lapack-in-matlab.html), [MEX/BLAS interface](https://www.mathworks.com/help/matlab/matlab_external/calling-lapack-and-blas-functions-from-mex-files.html), [desktop rebuild](https://blogs.mathworks.com/matlab/2025/05/16/whats-with-all-the-big-changes-in-r2025a/).

Suppose the user writes `x = A\b`. Conceptually, the application parses the expression, resolves types and dimensions, selects an appropriate algorithm and dispatches numerical work to compiled routines. It normally solves the system; it should not be understood as explicitly computing `inverse(A) × b`. A different operation may run language-level code, use a specialized library, or combine several paths.

To create a MATLAB-like platform from scratch, you would need language semantics, a parser, runtime, arrays, type handling, memory management, numerical libraries, graphics, a debugger, packages, files, documentation and compatibility behavior. A JIT is another major subsystem. Reusing Python, Julia or Octave dramatically reduces that burden. GNU Octave already targets MATLAB-like numerical workflows, but does not promise full compatibility with all MATLAB products or toolboxes. [GNU Octave](https://octave.org/about)

## How to investigate a closed program without pretending to know its source

Keep four evidence classes separate:

| Class | Valid evidence | What it permits |
|---|---|---|
| Documented implementation | Official architecture statement, published source or original author account | State the identified component/language with its version or historical scope |
| Documented interface | Plugin SDK, UDF, scripting or generated-code documentation | State how users extend it; do not promote this into a core-language claim |
| Architectural hypothesis | Workload, historical lineage, deployment and ecosystem clues | Suggest a plausible implementation, explicitly labelled as uncertain |
| Unknown | No credible public evidence located | Say unknown; do not fill the gap with a confident language name |

Examples: Ignition documents a Java platform and Jython scripting. PSCAD documents compiling Fortran and C simulation code, which does not identify the language of its entire GUI. Fluent documents C/C++ user-defined functions, which is interface evidence. FreeCAD exposes C++ and Python source, which is direct implementation evidence. These distinctions are more useful than a table that confidently says every engineering product is “C++.”

## Architecture proposed for an open platform

Start with independently useful modules sharing a project format and conventions. Do not force all physics into a single solver or one enormous database schema.

| Layer | Initial design choice | Reason and boundary |
|---|---|---|
| Workbench UI | TypeScript with a web UI; optional desktop packaging | Accessible workflows, diagrams and reports; keep large numerical work outside the UI thread |
| Scientific orchestration | Python first; Julia where a particular modelling stack warrants it | Broad engineering packages; language selection follows the engine, not fashion |
| Numerical kernels | Existing C/C++/Fortran engines; new native code only for demonstrated gaps | Reuse verified methods and avoid costly rewrites |
| Project storage | Versioned JSON metadata plus structured tables and binary result arrays | Open, inspectable data; distinguish source inputs from derived outputs |
| Local persistence | SQLite for single-user projects; PostgreSQL if collaboration warrants it | Offline use first, multi-user complexity later |
| Solver adapters | A small versioned contract over files or a local process API | Isolate crashes and dependencies; record engine version and settings |
| Geometry and meshes | Existing kernel/mesher and neutral interchange where practical | CAD robustness is a large independent engineering undertaking |
| Visualization | Diagram tools and standard charting; VTK/ParaView-compatible result paths for fields | A browser mesh renderer is not an engineering geometry kernel |
| Coupling | FMI where both engines meaningfully support it; explicit domain mappings elsewhere | FMI does not magically standardize CAD, units, solver accuracy or all project semantics |

The project record should preserve entity IDs, unit systems, coordinate frames, sign conventions, material/model sources, boundary conditions, mesh settings, solver version, tolerances, scenarios and diagnostics. Never silently reinterpret a field when a schema evolves. A useful run is reproducible from its input manifest.

Examples of an adapter contract: `validate(model)`, `prepare(model, settings)`, `run(job)`, `cancel(job)`, `read_results(job)` and `explain_diagnostics(job)`. Keep the solver's native input/output files available. That makes debugging, independent review and migration possible.

### Five errors the platform must expose

**Model error:** the equations/idealizations omit relevant physics. **Parameter uncertainty:** loads, material properties or boundary conditions are not known accurately. **Discretization error:** mesh and time-step choices approximate a continuous problem. **Algebraic error:** the numerical iteration has not adequately converged. **Implementation/data error:** code, unit conversions, imports or metadata are wrong. These are different failures and require different remedies.

Verification asks whether the implementation solves the stated equations correctly. Validation asks whether those equations and parameters describe the real system well enough for the intended use. Agreement with a commercial package is useful evidence, but both tools can share a wrong assumption.

## What to build first

This prioritization is an engineering judgment, not a measured market forecast.

| Priority | Initial product | Reuse | Why it is a sensible starting point | Main remaining difficulty |
|---|---|---|---|---|
| 1 | Power-study workbench | pandapower or OpenDSS, selected by study type | Clear engineering workflow; strong open engines; natural path to diagrams and reports | Correct equipment data, model boundaries and user trust |
| 2 | Circuit experimentation and model review | ngspice/Xyce with existing schematic tooling | Mature solver foundation; bounded examples are easy to verify | Device models, convergence and library rights |
| 3 | Pump/pipe or drainage study workbench | EPANET/SWMM, depending on the problem | Practical civil/mechanical overlap and transparent conservation checks | GIS, calibration and keeping model classes distinct |
| 4 | Control and system-identification lab | python-control, SciPy, CasADi/OpenModelica where appropriate | Strong educational and practical value with modest graphics complexity | Matching model assumptions to real plants |
| 5 | Engineering calculation/report workspace | Python/Julia/Octave plus units and provenance | Shared foundation across disciplines | Avoiding an unfocused general notebook clone |
| Later | General CAD, broad nonlinear multiphysics or full industrial PLC platform | Existing mature projects | Potentially valuable, but much wider compatibility and validation obligations | Geometry robustness, hardware ecosystems, model libraries and support |

My recommended first slice is a single-line power-network workbench: model a small network, run a clearly specified steady-state study, display voltages/loading, compare scenarios and export a reproducible engineering report. For unbalanced distribution, consider OpenDSS; for Python-driven studies and automation, evaluate pandapower. Benchmark both against the exact intended network class before committing.

Do not begin by claiming a full ETAP replacement. Begin with a well-defined result that a user can inspect and verify, then expand according to actual missing workflows. The same strategy applies to the other fields.

### Proposed first twelve weeks (not a full-suite estimate)

| Period | Concrete output | Exit condition |
|---|---|---|
| Weeks 1–2 | User workflow, supported study scope, engine/license choice, reference cases | A written boundary and reproducible baseline cases |
| Weeks 3–4 | Project schema, units, entity validation and engine adapter | Headless studies reproduce the baseline |
| Weeks 5–7 | Diagram/model editor and results view | An engineer can create and inspect the chosen study end-to-end |
| Weeks 8–9 | Scenarios, diagnostics and report generation | Reports include inputs, assumptions, versions and reproducibility data |
| Weeks 10–12 | Independent review, documentation, installation and small pilot | Known errors are visible; pilot users can reproduce results |

This is a planning hypothesis for a tightly bounded prototype with existing engines and engineering review. It is not a staffing, cost or production-readiness guarantee. A broad commercial-suite substitute is an ongoing product and maintenance program, not a twelve-week project.

## Reuse and licensing findings

Open-source software can support a commercial service or product; the actual obligations depend on each component and how it is distributed or combined. Track the software, models, data, symbols, documentation and standards separately. A vendor's free simulator does not grant rights to redistribute its device models or engine.

The published OpenSees copyright permits specified noncommercial distribution and internal uses, while directing commercial product incorporation to separate permission. It therefore should not casually be treated as an unrestricted dependency for this platform. OpenFOAM's GPL terms and OpenModelica's compiler/runtime licensing also warrant component-specific planning. KiCad separately documents its software and library licensing. These examples demonstrate why a name containing “Open” is not enough. [OpenSees terms](https://github.com/OpenSees/OpenSees/blob/master/COPYRIGHT) · [OpenFOAM licence](https://openfoam.org/licence/) · [OpenModelica licence index](https://openmodelica.org/useresresources/license/) · [KiCad software](https://www.kicad.org/about/licenses/) · [KiCad libraries](https://www.kicad.org/libraries/license/)

Implement from published science and appropriately licensed specifications, datasets and code. Compatibility with a proprietary file format, API or model library should be treated as a separate research and rights question. Do not assume that process separation by itself resolves every license issue. Record exact release licenses before embedding or redistribution.

## Reading the field atlas

Each field below gives its scope, science, numerical methods, failure modes, open foundations, a proposed first product and verification targets. The ten tools are unranked and deliberately include distinct roles. Product links point to the official product/vendor or project; the workbook carries the source-coverage status separately.


## Field index

| ID | Branch | Field |
|---|---|---|
| E01 | Electrical | [Power systems and load flow](#e01-power-systems-and-load-flow) |
| E02 | Electrical | [Protection, faults and coordination](#e02-protection-faults-and-coordination) |
| E03 | Electrical | [Power electronics and electromagnetic transients](#e03-power-electronics-and-electromagnetic-transients) |
| E04 | Electrical | [Control engineering and system identification](#e04-control-engineering-and-system-identification) |
| E05 | Electrical | [PLC and industrial automation](#e05-plc-and-industrial-automation) |
| E06 | Electrical | [SCADA, HMI and industrial data](#e06-scada-hmi-and-industrial-data) |
| E07 | Electrical | [Electrical CAD, wiring and building electrical design](#e07-electrical-cad-wiring-and-building-electrical-design) |
| E08 | Electrical | [Renewables, storage and energy planning](#e08-renewables-storage-and-energy-planning) |
| N01 | Electronics | [Analog and mixed-signal circuits](#n01-analog-and-mixed-signal-circuits) |
| N02 | Electronics | [PCB design and electronic packaging](#n02-pcb-design-and-electronic-packaging) |
| N03 | Electronics | [RF, antennas and electromagnetic compatibility](#n03-rf-antennas-and-electromagnetic-compatibility) |
| N04 | Electronics | [Signals, communications and DSP](#n04-signals-communications-and-dsp) |
| N05 | Electronics | [Embedded software and instrumentation](#n05-embedded-software-and-instrumentation) |
| N06 | Electronics | [FPGA and digital hardware verification](#n06-fpga-and-digital-hardware-verification) |
| N07 | Electronics | [IC design, physical implementation and signoff](#n07-ic-design-physical-implementation-and-signoff) |
| N08 | Electronics | [Electrical machines, magnetics and drives](#n08-electrical-machines-magnetics-and-drives) |
| M01 | Mechanical | [Mechanical CAD and product geometry](#m01-mechanical-cad-and-product-geometry) |
| M02 | Mechanical | [Stress, deformation and structural FEA](#m02-stress-deformation-and-structural-fea) |
| M03 | Mechanical | [Computational fluid dynamics](#m03-computational-fluid-dynamics) |
| M04 | Mechanical | [Heat transfer, HVAC and building energy](#m04-heat-transfer-hvac-and-building-energy) |
| M05 | Mechanical | [Multibody dynamics, vibration and mechanisms](#m05-multibody-dynamics-vibration-and-mechanisms) |
| M06 | Mechanical | [Manufacturing, CAM and process simulation](#m06-manufacturing-cam-and-process-simulation) |
| M07 | Mechanical | [Fluid networks, piping and hydraulic systems](#m07-fluid-networks-piping-and-hydraulic-systems) |
| M08 | Mechanical | [Fatigue, fracture and material durability](#m08-fatigue-fracture-and-material-durability) |
| C01 | Civil | [Buildings and structural engineering](#c01-buildings-and-structural-engineering) |
| C02 | Civil | [Bridge engineering and staged construction](#c02-bridge-engineering-and-staged-construction) |
| C03 | Civil | [Geotechnical engineering and foundations](#c03-geotechnical-engineering-and-foundations) |
| C04 | Civil | [Water resources, hydrology and drainage](#c04-water-resources-hydrology-and-drainage) |
| C05 | Civil | [Road, railway and earthworks design](#c05-road-railway-and-earthworks-design) |
| C06 | Civil | [Transportation, traffic and pedestrian simulation](#c06-transportation-traffic-and-pedestrian-simulation) |
| C07 | Civil | [BIM, coordination and construction information](#c07-bim-coordination-and-construction-information) |
| C08 | Civil | [Surveying, GIS and reality capture](#c08-surveying-gis-and-reality-capture) |
| X01 | Cross-disciplinary | [Robotics and mechatronics](#x01-robotics-and-mechatronics) |
| X02 | Cross-disciplinary | [Multiphysics and systems modelling](#x02-multiphysics-and-systems-modelling) |
| X03 | Cross-disciplinary | [Numerical computing and optimization](#x03-numerical-computing-and-optimization) |
| X04 | Cross-disciplinary | [Industrial systems, logistics and reliability](#x04-industrial-systems-logistics-and-reliability) |
| I01 | Information technology | [Network design, simulation and emulation](#i01-network-design-simulation-and-emulation) |
| I02 | Information technology | [Network and infrastructure monitoring](#i02-network-and-infrastructure-monitoring) |
| I03 | Information technology | [Network automation and source of truth](#i03-network-automation-and-source-of-truth) |
| I04 | Information technology | [Wireless, RF and link planning](#i04-wireless-rf-and-link-planning) |
| I05 | Information technology | [Security monitoring, SIEM and detection](#i05-security-monitoring-siem-and-detection) |
| I06 | Information technology | [Packet analysis, vulnerability assessment and penetration testing](#i06-packet-analysis-vulnerability-assessment-and-penetration-testing) |
| I07 | Information technology | [Industrial networks and OT security](#i07-industrial-networks-and-ot-security) |
| I08 | Information technology | [Endpoint, systems and configuration management](#i08-endpoint-systems-and-configuration-management) |
| I09 | Information technology | [Virtualization and private cloud](#i09-virtualization-and-private-cloud) |
| I10 | Information technology | [DevOps, containers and infrastructure as code](#i10-devops-containers-and-infrastructure-as-code) |
| I11 | Information technology | [Databases, time series and industrial historians](#i11-databases-time-series-and-industrial-historians) |
| I12 | Information technology | [IT service management, assets and documentation](#i12-it-service-management-assets-and-documentation) |

## E01 Power systems and load flow

**Branch:** Electrical. **Scope:** Transmission, distribution and industrial networks; voltage, loading, losses, contingencies and dispatch.

**Fundamental science:** Kirchhoff laws, complex power, per-unit quantities and network admittance. Bus injections obey S_i = V_i conjugate(sum_j Y_ij V_j).

**Computational methods:** Newton–Raphson and sparse linear algebra; backward/forward sweep for suitable radial models; constrained nonlinear optimization for AC optimal power flow.

**Where results go wrong:** A converged solution can still use wrong load models, transformer connections or operating limits. Unbalanced feeders need phase-aware models; ordinary load flow does not resolve switching transients.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [ETAP](https://etap.com/solutions/power-system-analysis) | P | Industrial network studies | Capabilities depend on modules |
| [DIgSILENT PowerFactory](https://www.digsilent.de/en/functions.html) | P | Transmission and distribution studies | Detailed models require specialist setup |
| [PSS E](https://www.siemens.com/) | P | Transmission planning and dynamics | Not a complete industrial electrical design package |
| [PowerWorld Simulator](https://www.powerworld.com/) | P | Network visualization and transmission analysis | Check distribution and dynamics requirements |
| [CYME](https://www.cyme.com/) | P | Distribution network analysis | Licensed modules determine coverage |
| [Synergi Electric](https://www.dnv.com/) | P | Distribution planning | Utility data preparation remains substantial |
| [SKM PowerTools](https://www.skm.com/) | P | Industrial power system studies | Study types and device libraries need checking |
| [NEPLAN](https://www.neplan.ch/) | P | Electrical network analysis | Verify edition and solver options |
| [OpenDSS](https://sourceforge.net/projects/electricdss/) | O | Unbalanced distribution simulation | Engineering interface work remains |
| [pandapower](https://www.pandapower.org/) | O | Automated Python-based network studies | Library rather than turnkey desktop suite |

**Open foundations to investigate:** pandapower; OpenDSS; MATPOWER; GridCal; PyPSA for planning and optimization.

**Plausible first open product:** A local-first single-line editor with load flow, voltage-drop plots, scenario comparison and a reproducible calculation report.

**Verification and validation targets:** Hand-solved two-bus case, public IEEE feeder cases, transformer phase shifts, disconnected islands and an independent solver comparison.

## E02 Protection, faults and coordination

**Branch:** Electrical. **Scope:** Short-circuit duties, relay selectivity, breaker coordination, arc-flash studies and protection settings.

**Fundamental science:** Symmetrical components, sequence networks, equipment withstand, inverse-time curves and empirical arc-energy models.

**Computational methods:** Fault-network solves; curve intersections; time-current plotting; rule and standards evaluation.

**Where results go wrong:** Settings, CT saturation, grounding and upstream timing errors change conclusions. Arc-flash results are sensitive to fault current and clearing time. Standards and device curves are separately versioned data.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [ETAP protection modules](https://etap.com/) | P | Relay coordination and arc-flash workflows | Module and standards edition matter |
| [SKM PowerTools CAPTOR and A_Fault](https://www.skm.com/) | P | Time-current and arc-flash studies | Device data and settings require review |
| [EasyPower](https://www.easypower.com/) | P | Facility electrical safety studies | Check supported calculation standards |
| [DIgSILENT PowerFactory protection](https://www.digsilent.de/en/functions.html) | P | Protection within a network model | Specialized relay models need validation |
| [ASPEN OneLiner](https://www.aspeninc.com/) | P | Fault and relay studies | Not a general CAD or EMT environment |
| [CAPE](https://www.siemens.com/) | P | Utility protection engineering | Utility-scale setup and licensing |
| [CYME protection modules](https://www.cyme.com/) | P | Distribution coordination | Module availability varies |
| [NEPLAN protection](https://www.neplan.ch/) | P | Network fault and protection analysis | Verify relay library coverage |
| [ERACS](https://www.eracs.co.uk/) | P | Industrial fault and protection studies | Check current modules and standards |
| [DIgSILENT StationWare](https://www.digsilent.de/) | P | Protection settings management | Companion database, not a fault solver |

**Open foundations to investigate:** pandapower short-circuit functions; OpenDSS fault and protection models; independently licensed curve databases.

**Plausible first open product:** A coordination-curve workbench with explicit assumptions and versioned device data; add standards-specific calculations only after verification.

**Verification and validation targets:** Published reference fault cases, relay manufacturer curve points, pickup boundaries and independent review of units and clearing-time selection.

## E03 Power electronics and electromagnetic transients

**Branch:** Electrical. **Scope:** Converters, inverters, switching, insulation transients, grid-forming controls and hardware-in-the-loop.

**Fundamental science:** Kirchhoff equations coupled to semiconductor, inductor and capacitor models: v=L di/dt and i=C dv/dt; nonlinear differential-algebraic equations.

**Computational methods:** Modified nodal analysis, implicit integration, switch-event handling, averaged converter models and fixed-step real-time execution.

**Where results go wrong:** Averaged models omit switching ripple; fine switching models can be expensive and stiff. Real-time execution adds deadline constraints, not automatic physical fidelity.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [PSCAD/EMTDC](https://www.pscad.com/) | P | Grid electromagnetic transients | Generated simulation needs a compiler |
| [EMTP](https://www.emtp.com/) | P | Power-network transient studies | Detailed equipment models required |
| [PLECS](https://www.plexim.com/) | P | Converter and control simulation | Thermal and real-time features vary |
| [PSIM](https://altair.com/psim) | P | Power electronics and motor drives | Check model fidelity for parasitics |
| [Simulink with Simscape Electrical](https://www.mathworks.com/products/simscape-electrical.html) | P | Controls and physical electrical models | Multiple product licenses may be needed |
| [SIMetrix/SIMPLIS](https://www.simetrix.co.uk/) | P | Switching power-supply analysis | Simulator model assumptions differ |
| [LTspice](https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html) | F | SPICE circuit simulation | Freeware, not open source |
| [QSPICE](https://www.qorvo.com/design-hub/design-tools/interactive/qspice) | F | Mixed circuit simulation | Freeware, not an open engine |
| [Typhoon HIL toolchain](https://www.typhoon-hil.com/) | P | Real-time converter testing | Hardware-coupled workflow |
| [RT-LAB](https://www.opal-rt.com/) | P | Real-time simulation integration | Timing and hardware setup dominate |

**Open foundations to investigate:** ngspice; Xyce; OpenModelica; Julia/SciML for custom models.

**Plausible first open product:** An offline converter workbench with loss-aware averaged and switching models and clear comparisons between them.

**Verification and validation targets:** Buck-converter analytical limits, RLC step response, timestep refinement, energy balance and measured switching traces.

## E04 Control engineering and system identification

**Branch:** Electrical. **Scope:** Feedback design, tuning, estimation, model fitting, stability, optimal control and model-based implementation.

**Fundamental science:** State-space models x_dot=Ax+Bu, y=Cx+Du; transfer functions; feedback stability; probability and constrained optimization.

**Computational methods:** Eigenvalue analysis, frequency response, numerical integration, least squares, Kalman filtering, LQR and model predictive control.

**Where results go wrong:** Linearization is local. Delays, saturation, sample time, noise and actuator limits can defeat a design that looks excellent in a nominal simulation.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [MATLAB Control System Toolbox](https://www.mathworks.com/products/control.html) | P | Control analysis and design | Requires MATLAB and relevant add-ons |
| [Simulink](https://www.mathworks.com/products/simulink.html) | P | Block-diagram dynamic simulation | Solver and sample-time choices matter |
| [LabVIEW](https://www.ni.com/en/shop/labview.html) | P | Control experiments and instrumentation | Real-time deployment needs matching platform |
| [Simcenter Amesim](https://www.siemens.com/en-us/products/simcenter/) | P | Control with physical system models | Library and license scope varies |
| [MapleSim](https://www.maplesoft.com/products/maplesim/) | P | Symbolic and physical modelling | Not interchangeable with every toolbox |
| [Wolfram System Modeler](https://www.wolfram.com/system-modeler/) | P | Modelica-based system dynamics | Ecosystem differs from Simulink |
| [Scilab/Xcos](https://www.scilab.org/) | O | Open numerical and block-diagram analysis | Toolbox compatibility is incomplete |
| [python-control](https://python-control.readthedocs.io/) | O | Programmable feedback-system analysis | Code-first experience |
| [OpenModelica](https://openmodelica.org/) | O | Equation-based physical control models | Model translation can be difficult |
| [GNU Octave control package](https://octave.org/) | O | MATLAB-like control workflows | Not complete MATLAB toolbox parity |

**Open foundations to investigate:** python-control; SciPy; SLICOT; CasADi; do-mpc; Scilab/Xcos; OpenModelica.

**Plausible first open product:** An interactive plant-identification and PID/state-space design tool with reusable experiments and exportable models.

**Verification and validation targets:** Analytical first/second-order systems, delayed plants, saturation and anti-windup cases, parameter uncertainty and held-out identification data.

## E05 PLC and industrial automation

**Branch:** Electrical. **Scope:** Machine sequences, interlocks, motion, I/O configuration, commissioning and deterministic execution.

**Fundamental science:** Finite-state machines, Boolean logic, cyclic and event tasks, discrete control and real-time scheduling.

**Computational methods:** IEC 61131 programming, compilation, scan-cycle execution, online monitoring and device/protocol mapping.

**Where results go wrong:** A simulator does not reproduce every device, fieldbus or timing behavior. Safety runtimes, online changes and hardware support are separate engineering problems.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [TIA Portal STEP 7](https://www.siemens.com/en-gb/products/tia-portal/step7/) | P | Siemens controller engineering | Device-family coupling |
| [Studio 5000 Logix Designer](https://www.rockwellautomation.com/) | P | Allen-Bradley Logix engineering | Controller ecosystem dependence |
| [TwinCAT 3](https://www.beckhoff.com/en-en/products/automation/twincat/) | P | PC-based PLC and motion | Runtime licenses and real-time setup |
| [CODESYS Development System](https://www.codesys.com/) | F | IEC 61131 engineering across vendors | Free IDE does not mean free/open runtime |
| [EcoStruxure Control Expert](https://www.se.com/) | P | Schneider process PLCs | Controller-specific deployment |
| [Sysmac Studio](https://automation.omron.com/) | P | Omron automation and motion | Hardware-family dependence |
| [GX Works3](https://www.mitsubishielectric.com/fa/) | P | Mitsubishi PLC engineering | Hardware-family dependence |
| [Automation Studio](https://www.br-automation.com/) | P | B&R control and motion | Different from Famicom product of same name |
| [OpenPLC](https://openplcproject.com/) | O | Open PLC development and runtime | Verify current runtime and hardware support |
| [Beremiz](https://beremiz.org/) | O | Open IEC 61131 programming | Smaller device and support ecosystem |

**Open foundations to investigate:** OpenPLC; Beremiz; Eclipse 4diac for IEC 61499; open protocol stacks where licenses fit.

**Plausible first open product:** An offline PLC learning and testing environment with simulated I/O, test traces and vendor-neutral project exports.

**Verification and validation targets:** Scan-order tests, timer semantics, restart states, dropped communications and deterministic timing on the intended runtime.

## E06 SCADA, HMI and industrial data

**Branch:** Electrical. **Scope:** Supervisory screens, tags, alarms, historians, gateways, trends and plant-data integration.

**Fundamental science:** Distributed state, timestamped events, sampled signals, quality flags, alarm state machines and time-series storage.

**Computational methods:** Polling and subscriptions, protocol drivers, event processing, database queries and rendering; not primarily a PDE solver.

**Where results go wrong:** Clock errors, stale values, alarm flooding and missing quality metadata can mislead operators. A dashboard without device semantics is not a full SCADA platform.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Ignition](https://inductiveautomation.com/ignition/) | P | Modular industrial HMI and data platform | Module and deployment design matter |
| [SIMATIC WinCC](https://www.siemens.com/) | P | Siemens HMI and SCADA | Distinguish Unified and other product lines |
| [AVEVA System Platform](https://www.aveva.com/) | P | Plant-wide supervisory applications | Substantial application engineering |
| [AVEVA InTouch HMI](https://www.aveva.com/) | P | Operator visualization | Not the full System Platform stack |
| [FactoryTalk View](https://www.rockwellautomation.com/) | P | Rockwell visualization | Distinguish SE and ME editions |
| [VTScada](https://www.vtscada.com/) | P | Integrated SCADA applications | Protocol and redundancy requirements vary |
| [zenon](https://www.copadata.com/) | P | Industrial visualization and automation | Product modules and drivers vary |
| [Movicon.NExT](https://www.movicon.info/) | P | HMI and SCADA engineering | Verify required connectors |
| [Rapid SCADA](https://rapidscada.org/) | O/M | Open core SCADA | Some modules are commercial |
| [FUXA](https://github.com/frangoteam/FUXA) | O | Browser-based industrial visualization | Validate maturity for the intended workload |

**Open foundations to investigate:** Node-RED plus a historian and HMI components; Eclipse Milo/open62541; FUXA; Rapid SCADA, with component-level license review.

**Plausible first open product:** A read-only Modbus/OPC UA monitoring workbench with tag mapping, timestamps, signal quality and exportable trends.

**Verification and validation targets:** Communication outages, stale-data display, restart/replay behavior, alarm ordering and timestamp consistency.

## E07 Electrical CAD, wiring and building electrical design

**Branch:** Electrical. **Scope:** Schematics, panel layouts, cable schedules, wire numbering, bills of materials and installation calculations.

**Fundamental science:** Graph connectivity, symbol semantics, geometric constraints, wiring rules and equipment metadata.

**Computational methods:** Connectivity checking, automatic cross-references, graph traversal, cable rules and document generation.

**Where results go wrong:** Drawing lines is easier than preserving electrical connectivity. Vendor symbol libraries and correct revision propagation are a large part of product value.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [EPLAN Electric P8](https://www.eplan-software.com/) | P | Data-driven electrical schematics | Library and platform integration effort |
| [AutoCAD Electrical](https://www.autodesk.com/) | P | Electrical drafting and automation | Different from ordinary AutoCAD drawings |
| [Zuken E3.series](https://www.zuken.com/) | P | Electrical wiring and harness design | Modules serve different workflows |
| [SEE Electrical](https://www.ige-xao.com/) | P | Electrical schematic documentation | Edition capabilities vary |
| [WSCAD ELECTRIX](https://www.wscad.com/) | P | Electrical and building-services design | Library and edition checks needed |
| [SOLIDWORKS Electrical](https://www.solidworks.com/) | P | Electrical-mechanical design linkage | Requires a compatible CAD workflow |
| [Engineering Base](https://www.aucotec.com/) | P | Plant engineering data and diagrams | Enterprise data-model complexity |
| [Capital](https://www.siemens.com/) | P | Harness and electrical systems engineering | Large-system workflow, not a small CAD clone |
| [Caneco BT](https://www.caneco.com/) | P | Low-voltage installation design | Country rules and editions matter |
| [QElectroTech](https://qelectrotech.org/) | O | Open electrical diagram creation | Not a complete calculation suite |

**Open foundations to investigate:** QElectroTech; FreeCAD; KiCad for electronic schematics; a separately designed electrical data schema.

**Plausible first open product:** A wiring and panel documentation tool with reusable symbols, automatic wire lists and consistent revisions.

**Verification and validation targets:** Round-trip exports, changed terminal numbers, duplicate references, disconnected wires and bill-of-material reconciliation.

## E08 Renewables, storage and energy planning

**Branch:** Electrical. **Scope:** PV yield, wind resources, microgrids, batteries, dispatch and techno-economic scenarios.

**Fundamental science:** Solar geometry, irradiance, electrical conversion, turbine curves, storage energy balance and discounted cash flow.

**Computational methods:** Time-series simulation, weather interpolation, loss chains, dispatch optimization and stochastic scenarios.

**Where results go wrong:** Weather quality and tariff assumptions can dominate accuracy. Annual energy alone hides curtailment, intermittency and battery degradation.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [PVsyst](https://www.pvsyst.com/en/products/pvsyst/) | P | Detailed photovoltaic yield studies | Input weather and shading remain critical |
| [HOMER Pro](https://www.homerenergy.com/) | P | Microgrid techno-economic studies | Dispatch assumptions need review |
| [PV*SOL](https://valentin-software.com/) | P | PV system design and yield | Check supported regional components |
| [HelioScope](https://helioscope.com/) | P | PV layout and production modelling | Cloud workflow and project limits |
| [SAM](https://sam.nrel.gov/) | O | Renewable energy performance and finance | Not every technology has equal model depth |
| [windPRO](https://www.emd-international.com/) | P | Wind-project modelling workflow | Specialist modules and data required |
| [WindFarmer](https://www.dnv.com/) | P | Wind farm energy assessment | Wake and resource assumptions dominate |
| [WAsP](https://www.wasp.dk/) | P | Wind resource modelling | Terrain/model applicability matters |
| [RETScreen Expert](https://natural-resources.canada.ca/) | M | Energy project feasibility and management | Access tiers differ; not an open engine |
| [PyPSA](https://pypsa.org/) | O | Energy-system optimization | Planning library, not PV layout CAD |

**Open foundations to investigate:** SAM; pvlib; PyPSA; OpenDSS; REopt API/source components after license checks.

**Plausible first open product:** A PV-and-battery feasibility tool with transparent hourly dispatch, editable loss assumptions and uncertainty ranges.

**Verification and validation targets:** Energy conservation, known PV reference cases, measured monthly yield and dispatch under zero/negative prices and battery limits.

## N01 Analog and mixed-signal circuits

**Branch:** Electronics. **Scope:** Amplifiers, filters, sensor circuits, power supplies, semiconductor devices and mixed analog/digital behavior.

**Fundamental science:** KCL/KVL plus nonlinear device equations; modified nodal equations G(x)x+C(x)x_dot=b.

**Computational methods:** Newton iterations, DC operating point, AC linearization, transient integration and Monte Carlo variation.

**Where results go wrong:** Convergence does not validate device models. Parasitics, operating temperature, manufacturing variation and encrypted vendor models limit portability.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Cadence PSpice](https://www.cadence.com/en_US/home/tools/pcb-design-and-analysis/analog-mixed-signal-simulation/pspice.html) | P | Board-level analog/mixed-signal simulation | Device model compatibility matters |
| [Cadence Spectre](https://www.cadence.com/en_US/home/tools/custom-ic-analog-rf-design/circuit-simulation.html) | P | IC analog and RF simulation | Foundry models and licenses needed |
| [HSPICE](https://www.synopsys.com/) | P | Transistor-level circuit simulation | Large circuits can be expensive |
| [Siemens Eldo](https://www.siemens.com/) | P | Analog and mixed-signal verification | Check supported model formats |
| [SIMetrix/SIMPLIS](https://www.simetrix.co.uk/) | P | Analog and switching circuits | Different engines use different model assumptions |
| [NI Multisim](https://www.ni.com/) | P | Interactive circuit design and education | Check current edition and deployment support |
| [LTspice](https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html) | F | Free SPICE circuit exploration | Closed-source freeware |
| [QSPICE](https://www.qorvo.com/design-hub/design-tools/interactive/qspice) | F | Free mixed circuit simulation | Closed-source freeware |
| [ngspice](https://ngspice.sourceforge.io/) | O | Embeddable open SPICE engine | GUI and model curation are separate |
| [Xyce](https://xyce.sandia.gov/) | O | Parallel circuit simulation | Not a full PCB design interface |

**Open foundations to investigate:** ngspice; Xyce; Qucs-S; KiCad schematic integration.

**Plausible first open product:** A schematic-to-ngspice workbench with model provenance, tolerance sweeps and explainable convergence failures.

**Verification and validation targets:** RC/RLC analytical circuits, diode operating points, oscillator startup, timestep convergence and measured board behavior.

## N02 PCB design and electronic packaging

**Branch:** Electronics. **Scope:** Schematic capture, component placement, routing, footprints, clearances and fabrication outputs.

**Fundamental science:** Graph connectivity, computational geometry, impedance constraints, manufacturing tolerances and stack-up models.

**Computational methods:** Constraint checking, interactive routing, geometric collision tests and format conversion; field solvers handle detailed SI/PI.

**Where results go wrong:** A correct netlist does not imply signal integrity or manufacturability. Libraries, stackups and fabrication rules must be trustworthy.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Altium Designer](https://www.altium.com/) | P | Integrated professional PCB workflow | Subscription and library ecosystem |
| [Cadence Allegro X](https://www.cadence.com/en_US/home/tools.html) | P | Complex PCB and package design | Advanced setup and constraint management |
| [Cadence OrCAD X](https://www.cadence.com/en_US/home/tools/pcb-design-and-analysis/orcad.html) | P | PCB design and simulation integration | Different scope from full Allegro enterprise flow |
| [Siemens Xpedition](https://www.siemens.com/en-gb/products/pcb/xpedition/) | P | Scalable enterprise PCB design | Choose the correct product tier |
| [Zuken CR-8000](https://www.zuken.com/) | P | System-centric PCB engineering | Enterprise workflow complexity |
| [Zuken CADSTAR](https://www.zuken.com/) | P | PCB design workflow | Verify current support and migration path |
| [Autodesk Fusion Electronics](https://www.autodesk.com/products/fusion-360/overview) | P | Linked mechanical and electronics design | Cloud and subscription dependencies |
| [Proteus Design Suite](https://www.labcenter.com/) | P | PCB plus embedded circuit simulation | Simulation requires supported device models |
| [KiCad](https://www.kicad.org/) | O | Open schematic and PCB design | Enterprise library governance is separate |
| [LibrePCB](https://librepcb.org/) | O | Open PCB design with structured libraries | Smaller advanced-feature ecosystem |

**Open foundations to investigate:** KiCad; LibrePCB; open fabrication formats and independently maintained footprint libraries.

**Plausible first open product:** Contribute workflow improvements to KiCad or build a focused review/DFM companion rather than another full PCB editor.

**Verification and validation targets:** Gerber/drill round trips, netlist consistency, clearance boundaries, footprint pin mapping and manufacturer fabrication checks.

## N03 RF, antennas and electromagnetic compatibility

**Branch:** Electronics. **Scope:** Antennas, microwave components, waveguides, scattering, electromagnetic coupling and high-frequency packaging.

**Fundamental science:** Maxwell equations, wave propagation, boundary conditions, S-parameters and material dispersion.

**Computational methods:** Finite elements, finite-difference time domain, method of moments, integral equations and hybrid ray methods.

**Where results go wrong:** Mesh dispersion, port definitions, absorbing boundaries and material data can dominate error. No single EM formulation is best at every electrical size.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Ansys HFSS](https://www.ansys.com/products/electronics/ansys-hfss) | P | 3D high-frequency electromagnetics | Mesh and port setup are demanding |
| [CST Studio Suite](https://www.3ds.com/products/simulia/cst-studio-suite) | P | Multiple EM solution methods | Solver selection matters |
| [Altair Feko](https://altair.com/feko) | P | Antennas and electromagnetic scattering | Validate formulation for scale |
| [Keysight ADS](https://www.keysight.com/us/en/products/software/pathwave-design-software/pathwave-advanced-design-system.html) | P | RF circuits and EM co-design | Not every task is a 3D field solve |
| [Keysight EMPro](https://www.keysight.com/) | P | 3D electromagnetic component design | Licensing and solver configuration |
| [Cadence AWR Microwave Office](https://www.cadence.com/) | P | Microwave circuit design | EM analysis may use companion tools |
| [COMSOL RF Module](https://www.comsol.com/products) | P | RF within multiphysics models | General modelling requires expertise |
| [Sonnet](https://www.sonnetsoftware.com/) | P | Planar high-frequency EM analysis | Planar specialization is intentional |
| [Remcom XFdtd](https://www.remcom.com/) | P | FDTD electromagnetic simulation | Spatial and time discretization costs |
| [openEMS](https://www.openems.de/) | O | Open FDTD EM solver | Model creation and UI need work |

**Open foundations to investigate:** openEMS; Meep; GetDP/Gmsh; scuff-em.

**Plausible first open product:** An antenna workbench for a bounded geometry family with meshing presets, convergence checks and S-parameter reports.

**Verification and validation targets:** Dipole and waveguide analytical limits, scattering reference cases, mesh refinement and measured S-parameters.

## N04 Signals, communications and DSP

**Branch:** Electronics. **Scope:** Sampling, filters, modulation, coding, channel models, SDR and signal processing chains.

**Fundamental science:** Fourier/z transforms, convolution, sampling theory, probability, estimation and information theory.

**Computational methods:** FFT, FIR/IIR filtering, multirate processing, Monte Carlo BER estimation and streaming dataflow.

**Where results go wrong:** Ideal simulations omit quantization, clipping, synchronization, oscillator drift and real RF impairments. Reproducible random seeds and units matter.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [MATLAB Signal Processing Toolbox](https://www.mathworks.com/products/signal.html) | P | Signal analysis and filter design | MATLAB required |
| [MATLAB Communications Toolbox](https://www.mathworks.com/products/communications.html) | P | Communication-system modelling | Standards add-ons may be separate |
| [Simulink DSP System Toolbox](https://www.mathworks.com/products/dsp-system.html) | P | Streaming DSP and implementation | Deployment features require more products |
| [Keysight SystemVue](https://www.keysight.com/) | P | RF communication system design | Specialized libraries and modules |
| [LabVIEW](https://www.ni.com/en/shop/labview.html) | P | Measurement and streaming signal workflows | Hardware drivers and editions matter |
| [GNU Radio](https://www.gnuradio.org/) | O | SDR and streaming signal processing | Hardware and block compatibility |
| [Scilab](https://www.scilab.org/) | O | Numerical signal-processing studies | Smaller specialist toolbox ecosystem |
| [GNU Octave signal package](https://octave.org/) | O | MATLAB-like signal analysis | Compatibility is partial |
| [SciPy signal](https://docs.scipy.org/doc/scipy/reference/signal.html) | O | Python signal algorithms | Library, not a turnkey instrument UI |
| [JuliaDSP](https://github.com/JuliaDSP/DSP.jl) | O | Julia signal processing | Smaller commercial integration ecosystem |

**Open foundations to investigate:** GNU Radio; SciPy; liquid-dsp; FFTW; JuliaDSP.

**Plausible first open product:** A visual DSP lab with inspectable blocks, recorded datasets and a reproducible code export.

**Verification and validation targets:** FFT normalization, filter response, analytical AWGN BER, aliasing cases and sample-rate/latency tests.

## N05 Embedded software and instrumentation

**Branch:** Electronics. **Scope:** Microcontrollers, firmware, debugging, RTOS integration, hardware interfaces and automated test.

**Fundamental science:** Computer architecture, interrupts, concurrency, finite-state machines, sampling and real-time constraints.

**Computational methods:** Compilers, linkers, debuggers, static analysis, instruction simulation and hardware tracing.

**Where results go wrong:** Compiler success does not establish timing, stack safety or hardware correctness. Proprietary probe interfaces and peripheral models complicate replacement.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Arm Keil MDK](https://www.keil.com/) | P | Arm microcontroller development | Device and compiler licensing |
| [IAR Embedded Workbench](https://www.iar.com/) | P | Embedded compilation and debugging | Target-specific packages |
| [TASKING toolsets](https://www.tasking.com/) | P | Automotive and embedded toolchains | Architecture-specific scope |
| [SEGGER Embedded Studio](https://www.segger.com/) | M | Embedded C/C++ development | Commercial and free-use terms differ |
| [STM32CubeIDE](https://www.st.com/) | F | STM32 firmware development | Bundled components have different licenses |
| [MPLAB X IDE](https://www.microchip.com/) | F | Microchip development | Compiler features/licensing are separate |
| [Code Composer Studio](https://www.ti.com/) | F | Texas Instruments targets | Target ecosystem dependence |
| [MCUXpresso IDE](https://www.nxp.com/) | F | NXP microcontrollers | Edition and component license differences |
| [PlatformIO Core](https://platformio.org/) | O | Multi-board reproducible development | Core openness does not cover all vendor SDKs |
| [Renode](https://renode.io/) | O | Embedded-system simulation | Only supported models reproduce peripherals |

**Open foundations to investigate:** GCC/LLVM; GDB; OpenOCD; Zephyr; PlatformIO Core; Renode; QEMU where devices are supported.

**Plausible first open product:** A reproducible firmware workspace with board definitions, build manifests, simulation tests and trace capture.

**Verification and validation targets:** Peripheral register behavior, interrupt ordering, memory boundaries, timing tests and real-board regression cases.

## N06 FPGA and digital hardware verification

**Branch:** Electronics. **Scope:** RTL design, logic synthesis, timing closure, simulation, formal checks and FPGA place-and-route.

**Fundamental science:** Boolean algebra, sequential logic, synchronous timing, graph optimization and satisfiability.

**Computational methods:** HDL parsing/elaboration, event simulation, synthesis, placement, routing, static timing and SAT/SMT checking.

**Where results go wrong:** Passing simulation does not prove all states. Clock-domain crossings, device-specific primitives and bitstream formats limit portability.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [AMD Vivado](https://www.amd.com/) | M | AMD FPGA design implementation | Free and paid tiers differ |
| [Altera Quartus Prime](https://www.altera.com/) | M | Altera FPGA design implementation | Device support varies by edition |
| [Microchip Libero SoC](https://www.microchip.com/) | M | Microchip FPGA and SoC flow | Device and IP licensing |
| [Lattice Radiant](https://www.latticesemi.com/) | M | Lattice FPGA implementation | Family and license coverage |
| [Siemens Questa](https://www.siemens.com/) | P | Digital simulation and verification | Different verification products and tiers |
| [Cadence Xcelium](https://www.cadence.com/) | P | RTL and mixed-signal verification | Not a complete FPGA place-and-route flow |
| [Synopsys VCS](https://www.synopsys.com/) | P | SystemVerilog simulation | Licensing and verification setup |
| [Yosys with nextpnr](https://yosyshq.net/) | O | Open synthesis and supported FPGA implementation | Device coverage is limited |
| [Verilator](https://verilator.org/) | O | Compiled Verilog/SystemVerilog simulation | Semantics/features differ from event simulators |
| [GHDL](https://ghdl.github.io/ghdl/) | O | VHDL simulation | Not a universal FPGA implementation suite |

**Open foundations to investigate:** Yosys; nextpnr; Verilator; GHDL; SymbiYosys; supported open FPGA flows.

**Plausible first open product:** A teaching and verification workbench for supported FPGA families, with testbenches and transparent timing reports.

**Verification and validation targets:** RTL-to-netlist equivalence, arithmetic edge cases, reset sequencing, timing constraints and programming real supported hardware.

## N07 IC design, physical implementation and signoff

**Branch:** Electronics. **Scope:** Analog layout, digital ASIC synthesis, physical design, timing, parasitic extraction and verification.

**Fundamental science:** Semiconductor circuit models, RC networks, Boolean optimization, graph placement and geometric design rules.

**Computational methods:** Synthesis, floorplanning, placement/routing, extraction, DRC/LVS and statistical/timing analysis.

**Where results go wrong:** A runnable design is not a manufacturable chip. Foundry PDKs, qualified rule decks, device IP and signoff acceptance create major barriers.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Cadence Virtuoso Studio](https://www.cadence.com/) | P | Custom analog IC design | Foundry PDK access required |
| [Synopsys Custom Compiler](https://www.synopsys.com/) | P | Custom IC layout and design | PDK and ecosystem dependency |
| [Cadence Innovus](https://www.cadence.com/) | P | Digital physical implementation | Not standalone foundry signoff |
| [Synopsys Fusion Compiler](https://www.synopsys.com/) | P | Digital synthesis and physical design | Complex licensed flow |
| [Synopsys PrimeTime](https://www.synopsys.com/) | P | Timing signoff | Companion stage, not full design suite |
| [Siemens Calibre](https://www.siemens.com/) | P | Physical verification and extraction | Qualified rule decks are essential |
| [Cadence Pegasus](https://www.cadence.com/) | P | Physical verification | Requires appropriate foundry decks |
| [OpenROAD](https://theopenroadproject.org/) | O | Open digital physical implementation | Supported PDK and signoff limitations |
| [KLayout](https://www.klayout.de/) | O | Layout editing and verification scripting | Not the complete ASIC flow |
| [Magic](http://opencircuitdesign.com/magic/) | O | Open IC layout and extraction | Process coverage and workflow limitations |

**Open foundations to investigate:** OpenROAD; Yosys; KLayout; Magic; Xschem; ngspice; an appropriately licensed open PDK.

**Plausible first open product:** A reproducible educational ASIC flow on one supported open PDK; keep production signoff claims out of scope.

**Verification and validation targets:** DRC/LVS regressions, extraction comparisons, timing checks, reproducible builds and eventual measured test-chip results.

## N08 Electrical machines, magnetics and drives

**Branch:** Electronics. **Scope:** Motors, generators, transformers, actuators, inductors and coupled electromagnetic/thermal performance.

**Fundamental science:** Maxwell equations in quasi-static regimes; magnetic constitutive laws B(H); force/torque and thermal energy balances.

**Computational methods:** Magnetic equivalent circuits, finite elements, rotating meshes, hysteresis/loss models and circuit coupling.

**Where results go wrong:** Lamination losses, saturation, end effects, temperature and manufacturing variation are easily under-modelled. A 2D model cannot resolve every 3D effect.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Ansys Maxwell](https://www.ansys.com/) | P | Low-frequency electromagnetic FEA | Geometry and material fidelity matter |
| [Ansys Motor-CAD](https://www.ansys.com/) | P | Motor multiphysics design | Template families bound design freedom |
| [JMAG-Designer](https://www.jmag-international.com/) | P | Electrical machine and magnetics FEA | Specialist setup and material data |
| [Altair Flux](https://altair.com/flux) | P | Low-frequency electromagnetic simulation | Solver/module choices |
| [SIMULIA Opera](https://www.3ds.com/) | P | Electromagnetic machine modelling | Check application-specific modules |
| [Simcenter MAGNET](https://www.siemens.com/) | P | Electromagnetic device simulation | Detailed loss modelling needs validation |
| [COMSOL AC/DC Module](https://www.comsol.com/products) | P | Magnetics coupled to other physics | General-purpose model setup |
| [Simcenter SPEED](https://www.siemens.com/) | P | Motor design calculations | Analytical/template assumptions |
| [FEMM](https://www.femm.info/) | O | 2D/axisymmetric magnetics and related fields | Not a general 3D solver |
| [Pyleecan](https://www.pyleecan.org/) | O | Open electrical machine analysis framework | Depends on available solver integrations |

**Open foundations to investigate:** FEMM; Elmer; GetDP; Pyleecan with supported solver adapters.

**Plausible first open product:** A parameterized motor/transformer design assistant with reproducible geometry and documented material data.

**Verification and validation targets:** Magnetic circuit limits, mesh convergence, torque consistency, measured back-EMF and loss/temperature tests.

## M01 Mechanical CAD and product geometry

**Branch:** Mechanical. **Scope:** Parts, assemblies, mechanisms, drawings, dimensions and manufacturing geometry.

**Fundamental science:** Analytic geometry, boundary representation, NURBS surfaces, topology and geometric constraints.

**Computational methods:** Sketch constraint solving, Boolean operations, surface intersections, feature history and assembly constraints.

**Where results go wrong:** Robust geometry is difficult near coincident faces and tiny features. Importing a solid does not recover its original design intent or parametric history.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [SOLIDWORKS](https://www.solidworks.com/) | P | Mechanical parts and assemblies | Add-ons and data-management scope vary |
| [CATIA](https://www.3ds.com/products/catia) | P | Complex product and surface design | Large ecosystem and learning burden |
| [Siemens NX](https://www.siemens.com/) | P | Integrated advanced CAD/CAM/CAE | Module and workflow complexity |
| [PTC Creo](https://www.ptc.com/en/products/creo) | P | Parametric product development | Extensions and interoperability need review |
| [Autodesk Inventor](https://www.autodesk.com/) | P | Mechanical design and drawings | Product data workflow is separate |
| [Autodesk Fusion](https://www.autodesk.com/products/fusion-360/overview) | M | Integrated CAD/CAM workflow | Free-use restrictions and cloud dependence |
| [Solid Edge](https://www.siemens.com/) | P | Mechanical modelling and drafting | Edition-dependent capabilities |
| [Onshape](https://www.ptc.com/en/products/onshape) | M | Cloud-native collaborative CAD | Free plan is not open-source software |
| [FreeCAD](https://www.freecad.org/) | O | Open parametric mechanical CAD | Workflow robustness varies by workbench |
| [Rhino](https://www.rhino3d.com/) | P | Freeform and NURBS modelling | Assembly/engineering features need additions |

**Open foundations to investigate:** FreeCAD and Open CASCADE; SolveSpace; CadQuery; build on an existing geometry kernel.

**Plausible first open product:** A focused part configurator or engineering workbench on FreeCAD with open project storage.

**Verification and validation targets:** Watertight solids, Boolean stress cases, STEP round trips, parameter changes and dimensional drawing consistency.

## M02 Stress, deformation and structural FEA

**Branch:** Mechanical. **Scope:** Mechanical components under static, dynamic, thermal, contact and nonlinear loads.

**Fundamental science:** Continuum mechanics, constitutive laws and weak forms; linear static discretization produces K u=f.

**Computational methods:** Finite elements, sparse factorization/Krylov solves, Newton iterations, modal analysis and implicit/explicit dynamics.

**Where results go wrong:** Stress singularities can increase under mesh refinement. Contact, plasticity, constraints and material calibration matter more than a polished contour plot.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Ansys Mechanical](https://www.ansys.com/) | P | General structural finite elements | Nonlinear setup and licenses vary |
| [SIMULIA Abaqus](https://www.3ds.com/products/simulia/abaqus) | P | Nonlinear mechanics and contact | Material and convergence expertise required |
| [Simcenter Nastran](https://www.siemens.com/en-gb/products/simcenter/mechanical-simulation/nastran/) | P | Structural and dynamic analysis | Capabilities depend on solver package |
| [MSC Nastran](https://nexus.hexagon.com/home/product/category/software/) | P | Structural dynamics and aerospace workflows | Not identical to other Nastran variants |
| [Altair OptiStruct](https://altair.com/optistruct) | P | Structural analysis and optimization | Optimization assumptions need validation |
| [LS-DYNA](https://www.ansys.com/) | P | Explicit nonlinear dynamics and crash | Very small time steps can be costly |
| [COMSOL Structural Mechanics Module](https://www.comsol.com/products) | P | Structures with multiphysics coupling | General modelling effort |
| [SOLIDWORKS Simulation](https://www.solidworks.com/) | P | CAD-integrated structural studies | Edition and model scope matter |
| [CalculiX](https://www.calculix.de/) | O | Open finite-element analysis | Pre/post-processing and robustness work |
| [Code_Aster](https://www.code-aster.org/) | O | Broad open structural mechanics | Substantial learning and setup burden |

**Open foundations to investigate:** CalculiX; Code_Aster; Elmer; Kratos; FEniCSx/deal.II for custom formulations.

**Plausible first open product:** A bounded linear-static workbench with material provenance, clear boundary conditions, mesh studies and auditable reports.

**Verification and validation targets:** Patch test, cantilever deflection, thick/thin beam limits, analytical pressure vessel and mesh-energy convergence.

## M03 Computational fluid dynamics

**Branch:** Mechanical. **Scope:** Internal/external flow, aerodynamics, mixing, turbulence, multiphase flow and fluid-structure coupling.

**Fundamental science:** Mass, momentum and energy conservation; Navier–Stokes equations with constitutive and turbulence closure models.

**Computational methods:** Finite volume/FEM; pressure-velocity coupling; RANS/LES; shock capture; interface tracking and parallel sparse solves.

**Where results go wrong:** Residual convergence alone is insufficient. Mesh, near-wall treatment, inlet turbulence and closure assumptions determine reliability; model error remains after discretization error falls.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Ansys Fluent](https://www.ansys.com/) | P | Broad industrial CFD | Turbulence and multiphase models need judgment |
| [Simcenter STAR-CCM+](https://www.siemens.com/en-us/products/simcenter/) | P | Integrated CFD workflow and automation | Compute and model complexity |
| [Ansys CFX](https://www.ansys.com/) | P | Rotating machinery and fluid simulation | Specialist workflow focus |
| [Cadence Fidelity](https://www.cadence.com/) | P | CFD portfolio and meshing | Choose the specific product/solver |
| [COMSOL CFD Module](https://www.comsol.com/products) | P | Flow coupled to other fields | Not identical to specialist CFD packages |
| [Altair AcuSolve](https://help.altair.com/hwsolvers/altair_help/index.htm) | P | Finite-element-based CFD | Solver-specific modelling choices |
| [SimScale](https://www.simscale.com/) | M | Browser-based engineering simulation | Hosted access does not imply open platform |
| [OpenFOAM](https://openfoam.org/) | O | Open finite-volume CFD platform | Distribution choice and setup matter |
| [SU2](https://su2code.github.io/) | O | Aerodynamics and design optimization | Application scope differs from general CFD |
| [Code_Saturne](https://www.code-saturne.org/) | O | General-purpose open CFD | UI and workflows need specialist knowledge |

**Open foundations to investigate:** OpenFOAM; SU2; Code_Saturne; OpenLB; NekRS for specialist workflows.

**Plausible first open product:** A guided incompressible internal-flow application with geometry cleanup, mesh presets and pressure-drop verification.

**Verification and validation targets:** Poiseuille flow, cavity flow, drag references, mass conservation, mesh/time-step studies and measured pressure drop.

## M04 Heat transfer, HVAC and building energy

**Branch:** Mechanical. **Scope:** Conduction, convection, radiation, cooling loads, building operation, comfort and energy use.

**Fundamental science:** Energy conservation, heat diffusion, radiation exchange, psychrometrics and thermal resistance/capacitance networks.

**Computational methods:** Transient heat balances, FEA/CFD, zone models, HVAC equipment maps and annual weather-driven simulation.

**Where results go wrong:** A building energy model and a resolved electronics-cooling model answer different questions. Schedules, infiltration, moisture and control assumptions can dominate predictions.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [IES Virtual Environment](https://www.iesve.com/) | P | Building energy and performance analysis | Calibration and occupancy assumptions |
| [DesignBuilder](https://designbuilder.co.uk/) | P | Building simulation front end | Commercial interface can use open engines |
| [Trane TRACE 3D Plus](https://www.trane.com/) | P | HVAC loads and energy modelling | Equipment and regional method scope |
| [Carrier HAP](https://www.carrier.com/us/en/commercial/software/hvac-system-design/hourly-analysis-program/) | P | HVAC sizing and energy studies | Load assumptions require careful input |
| [EnergyPlus](https://github.com/NREL/EnergyPlus) | O | Whole-building energy simulation engine | Not a complete graphical design system |
| [OpenStudio](https://www.openstudio.net/) | O | Building-energy modelling workflow | Engine and SDK version compatibility |
| [TRNSYS](https://www.trnsys.com/) | P | Transient thermal and energy systems | Source access is not an unrestricted license |
| [Ansys Icepak](https://www.ansys.com/) | P | Electronics thermal management | Different scale from HVAC building loads |
| [Simcenter Flotherm](https://www.siemens.com/) | P | Electronics cooling | Package and board representation assumptions |
| [COMSOL Heat Transfer Module](https://www.comsol.com/products) | P | General coupled heat-transfer analysis | Build domain-specific workflow yourself |

**Open foundations to investigate:** EnergyPlus; OpenStudio; Modelica Buildings; CoolProp; OpenFOAM/Elmer for resolved fields.

**Plausible first open product:** A building-load and energy-study interface with explicit weather, schedules, envelope data and uncertainty.

**Verification and validation targets:** Analytical wall conduction, thermal RC response, energy closure and published building-energy benchmark cases.

## M05 Multibody dynamics, vibration and mechanisms

**Branch:** Mechanical. **Scope:** Linkages, suspension, machinery motion, joints, flexible bodies, contacts and vibration.

**Fundamental science:** Newton–Euler/Lagrange equations with constraints; M(q)q_ddot+C+g=Q+J^T lambda.

**Computational methods:** Constraint stabilization, differential-algebraic integration, contact detection, modal reduction and eigenanalysis.

**Where results go wrong:** Stiff contacts, redundant constraints and poorly known friction/damping create numerical and physical uncertainty. Animation quality is not dynamic accuracy.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [MSC Adams](https://nexus.hexagon.com/home/product/adams/) | P | Mechanical multibody systems | Contact and flexible body setup |
| [SIMULIA Simpack](https://www.3ds.com/) | P | Rail, vehicle and machinery dynamics | Specialized component models |
| [Simcenter 3D Motion](https://www.siemens.com/) | P | Motion in CAE workflows | Product and solver licensing |
| [Altair MotionSolve](https://altair.com/) | P | Multibody and coupled simulation | Model and contact calibration |
| [RecurDyn](https://www.functionbay.com/) | P | Flexible multibody dynamics | Specialist modules vary |
| [Simscape Multibody](https://www.mathworks.com/products/simscape-multibody.html) | P | Mechanisms integrated with controls | Requires related MathWorks products |
| [SOLIDWORKS Motion](https://www.solidworks.com/) | P | CAD-integrated mechanism simulation | Not full parity with specialist MBD |
| [MapleSim](https://www.maplesoft.com/products/maplesim/) | P | Equation-based system dynamics | Specialized libraries vary |
| [Project Chrono](https://projectchrono.org/) | O | Open dynamics and contact engine | Application interface must be assembled |
| [MBDyn](https://www.mbdyn.org/) | O | Open multibody dynamics | Input workflow is technical |

**Open foundations to investigate:** Project Chrono; MBDyn; OpenModelica MultiBody; Simbody.

**Plausible first open product:** A mechanism explorer with joints, motor torques, flexible-body imports and explicit energy checks.

**Verification and validation targets:** Pendulum and four-bar cases, constraint drift, momentum/energy balance and measured modal frequencies.

## M06 Manufacturing, CAM and process simulation

**Branch:** Mechanical. **Scope:** Machining toolpaths, machine kinematics, forming, molding, casting and production process models.

**Fundamental science:** Computational geometry, rigid-body kinematics, material removal, plasticity, heat flow and fluid rheology.

**Computational methods:** Toolpath generation, collision detection, stock removal, finite-element forming and process-specific simulation.

**Where results go wrong:** A CAM postprocessor is machine-specific. Geometrically valid code may still exceed machine limits; forming and molding need calibrated material/process data.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Mastercam](https://www.mastercam.com/) | P | CNC programming | Postprocessor and machine setup matter |
| [Siemens NX CAM](https://www.siemens.com/) | P | Advanced integrated manufacturing | Modules and machine libraries |
| [Autodesk Fusion Manufacturing](https://www.autodesk.com/) | P | CAD-to-CAM workflow | Advanced capabilities may be extensions |
| [Autodesk PowerMill](https://www.autodesk.com/) | P | Complex CNC toolpaths | Specialist machining focus |
| [hyperMILL](https://www.openmind-tech.com/) | P | Advanced multi-axis CAM | Machine-specific postprocessing |
| [VERICUT](https://www.cgtech.com/) | P | NC verification and machine simulation | Verification companion, not full CAM authoring |
| [Autodesk Moldflow](https://www.autodesk.com/) | P | Injection molding simulation | Material database and process calibration |
| [DEFORM](https://www.deform.com/) | P | Metal forming process simulation | Specialist process scope |
| [Simufact](https://nexus.hexagon.com/home/product/category/software/) | P | Manufacturing process simulation | Products cover different processes |
| [FreeCAD CAM](https://www.freecad.org/) | O | Open CAM within parametric CAD | Advanced machines need extensive validation |

**Open foundations to investigate:** FreeCAD CAM; LinuxCNC for control; CAMotics for selected verification; OpenCAMLib; specialist solvers where suitable.

**Plausible first open product:** A 2.5D machining workflow for one machine family, with stock simulation and reviewed postprocessor.

**Verification and validation targets:** G-code backplot, machine travel/acceleration limits, collision fixtures and test cuts on sacrificial stock.

## M07 Fluid networks, piping and hydraulic systems

**Branch:** Mechanical. **Scope:** Pumps, pipes, valves, compressed gas, water hammer, hydraulic machinery and lumped fluid systems.

**Fundamental science:** Mass continuity, Bernoulli/energy equations, Darcy–Weisbach losses, compressibility and thermodynamic properties.

**Computational methods:** Nonlinear network solves, friction correlations, method of characteristics for transients and lumped ODE/DAE models.

**Where results go wrong:** A steady incompressible network solver cannot predict all water-hammer, cavitation or two-phase effects. Valve closure laws and fluid properties are essential.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Fathom (AFT/Datacor)](https://docs.aft.com/) | P | Steady incompressible flow networks | Not the transient surge product |
| [Arrow (AFT/Datacor)](https://docs.aft.com/) | P | Compressible flow networks | Check gas and heat-transfer assumptions |
| [Impulse (AFT/Datacor)](https://docs.aft.com/) | P | Liquid surge and water hammer | Valve and pump transient data matter |
| [Pipe Flow Expert](https://www.pipeflow.com/) | P | Pipe network calculations | Check supported fluid and transient scope |
| [PIPE-FLO](https://www.pipe-flo.com/) | P | Fluid system modelling | Edition and scenario capabilities |
| [PIPENET](https://www.sunrise-sys.com/) | P | Fluid networks and firewater analysis | Modules answer different study types |
| [Simcenter Flomaster](https://www.siemens.com/) | P | Thermofluid system simulation | Component calibration required |
| [Simcenter Amesim](https://www.siemens.com/en-us/products/simcenter/) | P | Hydraulic and coupled system dynamics | Component libraries and licenses |
| [GT-SUITE](https://www.gtisoft.com/gt-suite/) | P | Integrated 1D thermofluid systems | Model fidelity is configurable |
| [EPANET](https://www.epa.gov/water-research/epanet) | O | Water distribution hydraulics | Not general compressible/multiphase piping |

**Open foundations to investigate:** EPANET; Modelica.Fluid; pandapipes; CoolProp; bespoke transient solvers after verification.

**Plausible first open product:** A pump-and-pipe sizing workbench with system curves, duty-point comparisons and transparent pressure-loss calculations.

**Verification and validation targets:** Single-pipe Darcy losses, parallel branches, pump-curve intersections, reverse flow and benchmark surge cases.

## M08 Fatigue, fracture and material durability

**Branch:** Mechanical. **Scope:** Repeated loads, cracks, welds, composite failure and lifetime estimation.

**Fundamental science:** Stress-life/strain-life relations, rainflow cycle counting, cumulative damage, fracture mechanics and probabilistic scatter.

**Computational methods:** Fatigue postprocessing, critical-plane analysis, crack propagation laws and constitutive/material fitting.

**Where results go wrong:** Life predictions are highly sensitive to local stress, surface finish, load history and material data. A deterministic life figure conceals substantial scatter.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Ansys nCode DesignLife](https://www.ansys.com/) | P | FE-based fatigue assessment | Material and load-history quality |
| [SIMULIA fe-safe](https://www.3ds.com/) | P | Multiaxial fatigue postprocessing | Requires reliable stress/strain inputs |
| [Altair HyperLife](https://altair.com/) | P | Durability workflows | Modules and material coverage |
| [MSC Fatigue](https://nexus.hexagon.com/home/product/category/software/) | P | Fatigue assessment | Check current product support and licensing |
| [FEMFAT](https://femfat.magna.com/) | P | Industrial fatigue evaluation | Method and material calibration |
| [FRANC3D](https://www.fracanalysis.com/) | P | 3D crack-growth modelling | Companion FE workflow |
| [NASGRO](https://www.swri.org/) | P | Fracture and fatigue crack growth | Access and material database terms |
| [Ansys Mechanical fatigue tools](https://www.ansys.com/) | P | Integrated baseline fatigue studies | Not equivalent to full DesignLife |
| [Code_Aster](https://www.code-aster.org/) | O | Open structural and damage modelling | Complex workflow and material calibration |
| [pyLife](https://github.com/boschresearch/pylife) | O | Python reliability and fatigue analysis | Framework rather than complete FE suite |

**Open foundations to investigate:** Code_Aster; pyLife; fatigue libraries; FEniCSx for research formulations.

**Plausible first open product:** A fatigue calculation notebook/workbench with traceable load histories, material curves and sensitivity plots.

**Verification and validation targets:** Known rainflow sequences, constant-amplitude life, notch cases, published coupon data and independent damage calculations.

## C01 Buildings and structural engineering

**Branch:** Civil. **Scope:** Frames, slabs, foundations, seismic response and structural code checks.

**Fundamental science:** Equilibrium, compatibility, stiffness, stability, concrete/steel behavior and structural dynamics.

**Computational methods:** Beam/shell FEM, modal and response-spectrum analysis, nonlinear time history and rule-based design checks.

**Where results go wrong:** Code checks and analysis are distinct layers. Wrong supports, diaphragm assumptions, cracked stiffness or load combinations can invalidate results.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [ETABS](https://www.csiamerica.com/) | P | Multi-storey building analysis | Building idealizations require judgment |
| [SAP2000](https://www.csiamerica.com/) | P | General structural analysis | Design codes and modules vary |
| [STAAD.Pro](https://www.bentley.com/products/) | P | Structural analysis and design | Code/edition coverage matters |
| [Autodesk Robot Structural Analysis](https://www.autodesk.com/collections) | P | Building structure analysis | Interoperability needs checking |
| [Tekla Structural Designer](https://www.tekla.com/) | P | Building analysis and design | Regional design codes vary |
| [RFEM](https://www.dlubal.com/) | P | General member and surface FEA | Add-on requirements |
| [SCIA Engineer](https://www.scia.net/) | P | Structural analysis and design | Country code modules |
| [MIDAS Gen](https://www.midasuser.com/) | P | General/building structural engineering | Product and code edition checks |
| [RISA-3D](https://risa.com/) | P | Building and general frame analysis | Regional workflow focus |
| [OpenSees](https://github.com/OpenSees/OpenSees/blob/master/COPYRIGHT) | S | Nonlinear structural/earthquake research | Published redistribution terms restrict commercial use |

**Open foundations to investigate:** Code_Aster; CalculiX; Frame3DD; IFC tooling; OpenSees as a license-sensitive reference.

**Plausible first open product:** A 2D frame/slab analysis tool with transparent load combinations and calculation sheets for one clearly specified design basis.

**Verification and validation targets:** Hand frame solutions, patch tests, rigid-body checks, modal benchmarks and independent design-check verification.

## C02 Bridge engineering and staged construction

**Branch:** Civil. **Scope:** Bridge decks, girders, moving loads, construction sequences, creep, prestress and seismic response.

**Fundamental science:** Structural mechanics plus time-dependent materials, influence lines, prestress losses and staged boundary conditions.

**Computational methods:** Beam/shell/solid FEM, moving-load envelopes, time stepping and staged activation.

**Where results go wrong:** Final geometry alone omits construction history. Creep, shrinkage, prestress, bearing behavior and load-code implementation need careful review.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [CSiBridge](https://www.csiamerica.com/) | P | Bridge analysis design and rating | Code and staged-model setup |
| [MIDAS Civil](https://www.midasuser.com/) | P | Bridge and civil structural analysis | Creep and sequence assumptions |
| [RM Bridge](https://www.bentley.com/products/) | P | Complex bridge engineering | Specialist modelling workflow |
| [LUSAS Bridge](https://www.lusas.com/) | P | Bridge finite-element analysis | Product options and expertise |
| [SOFiSTiK](https://www.sofistik.com/) | P | Bridge analysis and design automation | Module and workflow complexity |
| [OpenBridge Designer](https://www.bentley.com/products/) | P | Bridge modelling and analysis integration | Suite components have distinct roles |
| [LEAP Bridge Concrete](https://www.bentley.com/products/) | P | Concrete bridge workflows | Template and regional code scope |
| [LEAP Bridge Steel](https://www.bentley.com/products/) | P | Steel bridge workflows | Template and regional code scope |
| [SAP2000](https://www.csiamerica.com/) | P | General bridge structural modelling | Specialized bridge workflow may need additions |
| [Ansys Mechanical](https://www.ansys.com/) | P | Detailed bridge components and nonlinear FEA | Not a turnkey bridge code-design suite |

**Open foundations to investigate:** Code_Aster; CalculiX; custom moving-load and staged-construction layers.

**Plausible first open product:** A beam-bridge load-envelope tool with visible influence lines and one documented vehicle/load-code implementation.

**Verification and validation targets:** Analytical influence lines, moving point loads, stage-by-stage equilibrium and independently checked prestress losses.

## C03 Geotechnical engineering and foundations

**Branch:** Civil. **Scope:** Soil/rock stability, settlement, excavations, tunnelling, foundations and groundwater coupling.

**Fundamental science:** Effective stress, constitutive soil/rock behavior, consolidation, Darcy flow and shear strength.

**Computational methods:** Limit equilibrium, FEM/FDM, shear-strength reduction, consolidation and staged excavation.

**Where results go wrong:** Ground parameter uncertainty often dominates numerical precision. A visually detailed model cannot compensate for poor site investigation or unsuitable constitutive laws.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [PLAXIS 2D/3D](https://www.bentley.com/products/) | P | Geotechnical finite elements | Soil constitutive calibration |
| [GeoStudio](https://www.bentley.com/en/products/geostudio-3d/) | P | Slope seepage and geotechnical studies | Modules use different formulations |
| [Rocscience RS2](https://www.rocscience.com/software/rs2) | P | 2D geotechnical FEA | Plane-strain assumptions |
| [Rocscience RS3](https://www.rocscience.com/software/rs3) | P | 3D geotechnical FEA | Parameter and mesh uncertainty |
| [Rocscience Slide2](https://www.rocscience.com/software/slope-stability) | P | 2D limit-equilibrium slopes | Failure-surface assumptions |
| [Rocscience Slide3](https://www.rocscience.com/software/slope-stability) | P | 3D limit-equilibrium slopes | Geometry and search settings matter |
| [FLAC3D](https://www.itascacg.com/) | P | Geomechanical continuum modelling | Specialist constitutive and boundary setup |
| [GEO5](https://www.finesoftware.eu/) | P | Practical geotechnical design programs | Individual modules cover different tasks |
| [MIDAS GTS NX](https://www.midasuser.com/) | P | Geotechnical finite elements | Verify current product/version naming |
| [Rocscience Settle3](https://www.rocscience.com/software/settle3) | P | Settlement and consolidation | Companion specialty, not all geotechnics |

**Open foundations to investigate:** Kratos/GeoMechanics; Code_Aster; Elmer; research geotechnical packages with verified licenses.

**Plausible first open product:** A transparent slope-stability or shallow-foundation calculator with sensitivity ranges and documented methods.

**Verification and validation targets:** Published slope examples, Terzaghi consolidation, bearing-capacity limits and sensitivity to water table/material parameters.

## C04 Water resources, hydrology and drainage

**Branch:** Civil. **Scope:** Rainfall-runoff, rivers, floods, drainage, stormwater, water distribution and water quality.

**Fundamental science:** Catchment mass balance, infiltration, open-channel/shallow-water equations, pipe hydraulics and pollutant transport.

**Computational methods:** Hydrograph routing, finite-volume/difference flow solvers, pipe-network iteration and advection/dispersion.

**Where results go wrong:** Terrain resolution, rainfall statistics, roughness and boundary conditions can outweigh solver differences. Water distribution and catchment flooding are different model classes.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [MIKE+](https://www.dhigroup.com/technologies/mikepoweredbydhi/products) | P | Integrated urban water modelling | Modules and model coupling |
| [MIKE 21](https://www.dhigroup.com/technologies/mikepoweredbydhi/products) | P | 2D coastal and free-surface flow | Different from pipe-network analysis |
| [OpenFlows Water](https://www.bentley.com/products/) | P | Water distribution studies | Package/legacy WaterGEMS naming varies |
| [OpenFlows Sewer](https://www.bentley.com/products/) | P | Wastewater and storm networks | Edition and engine options |
| [Autodesk InfoWorks ICM](https://www.autodesk.com/) | P | Integrated catchment modelling | Large models need careful calibration |
| [Autodesk InfoDrainage](https://www.autodesk.com/products/infodrainage/overview) | P | Drainage design | Local rainfall/design criteria matter |
| [PCSWMM](https://www.pcswmm.com/) | P | SWMM-based modelling environment | Commercial interface around model workflows |
| [HEC-RAS](https://www.hec.usace.army.mil/software/hec-ras/) | F | River hydraulics and flood modelling | Free access is not full open-source equivalence |
| [EPA SWMM](https://github.com/USEPA/Stormwater-Management-Model) | O | Stormwater and sewer modelling engine | GIS/design interface may be separate |
| [EPANET](https://github.com/USEPA/epanet-engine) | O | Water distribution and quality simulation | Different problem from surface flooding |

**Open foundations to investigate:** EPA SWMM; EPANET; TELEMAC; Delft3D components; GIS integration.

**Plausible first open product:** A drainage-study workbench with terrain/rainfall provenance, SWMM scenarios, maps and mass-balance diagnostics.

**Verification and validation targets:** Rational/unit-hydrograph checks within applicability, channel-flow references, wetting/drying cases and recorded storm events.

## C05 Road, railway and earthworks design

**Branch:** Civil. **Scope:** Alignments, profiles, corridors, cross-sections, earthwork quantities and road/rail geometry.

**Fundamental science:** Coordinate geometry, terrain interpolation, curve design, geometric constraints and volume integration.

**Computational methods:** TIN surfaces, spline/clothoid curves, corridor templates, cut/fill integration and design-rule checking.

**Where results go wrong:** Survey datums, breaklines and surface quality strongly affect quantities. Design criteria and corridor interoperability are separate from raw geometry.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Autodesk Civil 3D](https://www.autodesk.com/collections) | P | Civil surfaces and corridor design | Templates and data shortcuts require governance |
| [OpenRoads Designer](https://www.bentley.com/products/) | P | Roadway design and documentation | Regional workspace setup |
| [OpenRail Designer](https://www.bentley.com/products/) | P | Rail geometry and corridor design | Specialized rail constraints |
| [12d Model](https://www.12d.com/) | P | Survey civil and drainage design | Workflow and module configuration |
| [Trimble Novapoint](https://novapoint.com/) | P | Infrastructure design | Regional module availability |
| [Trimble Quantm](https://construction.trimble.com/) | P | Alignment planning and optimization | Early-stage planning, not full detailed CAD |
| [Carlson Civil](https://www.carlsonsw.com/) | P | Civil engineering CAD workflow | Host CAD and module dependencies |
| [Civil Site Design](https://www.civilsitedesign.com/) | P | Road and site modelling | Host CAD requirements |
| [CGS Labs Civil Solutions](https://cgs-labs.com/) | P | Road rail and river design tools | Choose the relevant product module |
| [InfraWorks](https://www.autodesk.com/) | P | Conceptual infrastructure modelling | Not detailed corridor analysis parity |

**Open foundations to investigate:** QGIS/GRASS; FreeCAD; GDAL/PROJ; open alignment and IFC infrastructure tooling.

**Plausible first open product:** A terrain-to-alignment and cross-section tool with transparent cut/fill calculations and open data exports.

**Verification and validation targets:** Known volume solids, survey-coordinate transforms, cross-section integration and alignment continuity checks.

## C06 Transportation, traffic and pedestrian simulation

**Branch:** Civil. **Scope:** Demand models, network assignment, intersections, signals, vehicle interactions and pedestrian movement.

**Fundamental science:** Traffic-flow theory, queueing, stochastic behavior, network equilibrium and discrete agent interactions.

**Computational methods:** Car-following/lane-changing models, mesoscopic simulation, route assignment and signal optimization.

**Where results go wrong:** Animated traffic is not evidence of predictive accuracy. Demand, route choice and behavioral calibration must be tested against independent counts and travel times.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [PTV Vissim](https://www.ptvgroup.com/en/products/ptv-vissim) | P | Microscopic multimodal traffic | Behavioral calibration required |
| [PTV Visum](https://www.ptvgroup.com/) | P | Transport demand and network planning | Different scale from microscopic simulation |
| [Aimsun Next](https://www.aimsun.com/) | P | Traffic modelling across scales | Scenario and calibration expertise |
| [TransModeler](https://www.caliper.com/) | P | Traffic simulation | Network and demand preparation |
| [TransCAD](https://www.caliper.com/) | P | Transport planning with GIS | Not the same task as junction microsimulation |
| [SIDRA INTERSECTION](https://www.sidrasolutions.com/) | P | Intersection capacity and performance | Method applicability must be checked |
| [Synchro Studio](https://www.cubic.com/) | P | Signal timing and traffic analysis | Check current supplier/package naming |
| [PTV Vistro](https://www.ptvgroup.com/) | P | Traffic impact and signal analysis | Regional methods and scope |
| [SUMO](https://eclipse.dev/sumo/) | O | Open microscopic traffic simulation | Data preparation and calibration are substantial |
| [MATSim](https://www.matsim.org/) | O | Large-scale agent-based transport demand | Research-oriented configuration |

**Open foundations to investigate:** SUMO; MATSim; AequilibraE; network/GIS libraries.

**Plausible first open product:** A corridor and intersection analysis workbench around SUMO with repeatable calibration and scenario comparison.

**Verification and validation targets:** Flow conservation, queue formation, signal timing, multiple random seeds and held-out counts/travel-time data.

## C07 BIM, coordination and construction information

**Branch:** Civil. **Scope:** Building/infrastructure objects, quantities, drawings, coordination, revisions and construction sequencing.

**Fundamental science:** Semantic object models, geometry, relationships, spatial indexing, classification and information exchange.

**Computational methods:** Parametric authoring, clash detection, model validation, quantities and schedule/model linking.

**Where results go wrong:** BIM geometry is not automatically an analysis-ready model. Units, object meaning, identifiers and revision ownership are frequent integration failures.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Autodesk Revit](https://www.autodesk.com/collections) | P | Building information authoring | Analytical model still needs review |
| [Tekla Structures](https://www.tekla.com/) | P | Detailed structural modelling | Not equivalent to structural analysis software |
| [Archicad](https://graphisoft.com/) | P | Architectural BIM authoring | Engineering analyses use companion tools |
| [OpenBuildings Designer](https://www.bentley.com/products/) | P | Multidiscipline building modelling | Workspace and interoperability setup |
| [Navisworks Manage](https://www.autodesk.com/) | P | Coordination and clash review | Review tool, not primary authoring CAD |
| [Solibri](https://www.solibri.com/) | P | Model checking and coordination | Rules must match project requirements |
| [SYNCHRO 4D](https://www.bentley.com/products/) | P | Construction sequencing linked to models | Needs reliable schedule and model data |
| [Trimble Connect](https://geospatial.trimble.com/en/products/software/trimble-connect) | M | Model collaboration and sharing | Access tiers and data governance |
| [Bonsai](https://bonsaibim.org/) | O | Native openBIM authoring workflow | Blender-based workflow learning |
| [FreeCAD BIM](https://www.freecad.org/) | O | Open building information modelling | Interoperability and feature scope vary |

**Open foundations to investigate:** IfcOpenShell; Bonsai; FreeCAD BIM; Speckle components subject to exact licenses.

**Plausible first open product:** An IFC review and quantity-audit tool with change tracking, model checks and transparent take-off rules.

**Verification and validation targets:** IFC import/export round trips, stable IDs, unit consistency, geometry/quantity comparisons and deliberate clash cases.

## C08 Surveying, GIS and reality capture

**Branch:** Civil. **Scope:** Coordinates, GNSS/total-station adjustment, terrain, point clouds, photogrammetry and spatial analysis.

**Fundamental science:** Geodesy, coordinate transforms, least-squares estimation, bundle adjustment, image geometry and spatial statistics.

**Computational methods:** Network adjustment, triangulation, structure from motion, point-cloud registration and raster/vector processing.

**Where results go wrong:** A low image reprojection error can coexist with a wrong datum or scale. Ground control, geoid models and positional uncertainty must remain explicit.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Trimble Business Center](https://help.fieldsystems.trimble.com/tbc/home.htm) | P | Survey-to-office processing | Device and module support |
| [Leica Infinity](https://leica-geosystems.com/) | P | Survey data processing | Instrument ecosystem integration |
| [Autodesk Civil 3D](https://www.autodesk.com/collections) | P | Survey surfaces and civil data | Not a full photogrammetry engine |
| [ArcGIS Pro](https://www.esri.com/) | P | GIS analysis and mapping | Extensions and organizational licensing |
| [Global Mapper](https://www.bluemarblegeo.com/) | P | GIS and terrain processing | Advanced point-cloud functions vary |
| [Pix4Dmatic](https://www.pix4d.com/) | P | Photogrammetric reconstruction | Acquisition and control quality |
| [Agisoft Metashape](https://www.agisoft.com/) | P | Image-based 3D reconstruction | Scale and georeferencing still need control |
| [QGIS](https://qgis.org/) | O | Open GIS platform | Specialist survey tools may be plugins |
| [CloudCompare](https://www.cloudcompare.org/) | O | Point-cloud processing and inspection | Not complete survey project management |
| [OpenDroneMap](https://www.opendronemap.org/) | O | Open aerial photogrammetry | Compute requirements and acquisition quality |

**Open foundations to investigate:** QGIS; GDAL/PROJ; PDAL; CloudCompare; OpenDroneMap; MicMac.

**Plausible first open product:** A survey-quality and terrain workbench with explicit coordinate reference systems and uncertainty reports.

**Verification and validation targets:** Known coordinate transforms, survey closures, independent checkpoints, point-cloud registration and volume comparisons.

## X01 Robotics and mechatronics

**Branch:** Cross-disciplinary. **Scope:** Mechanisms plus actuators, sensors, embedded control, perception, robot programming and motion planning.

**Fundamental science:** Rigid transformations, Jacobians, inverse kinematics, constrained dynamics, estimation and motion optimization.

**Computational methods:** Collision detection, sampling/trajectory planning, contact simulation, sensor models and controller integration.

**Where results go wrong:** Simulation-to-reality gaps arise from friction, latency, flexible hardware and perception error. Industrial offline programs still need accurate calibration and controller-specific output.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [ABB RobotStudio](https://new.abb.com/products/robotics/robotstudio) | P | ABB offline programming | Robot/controller ecosystem dependence |
| [RoboDK](https://robodk.com/) | P | Multibrand robot simulation and programming | API accessibility does not make engine open |
| [Siemens Process Simulate](https://www.siemens.com/) | P | Manufacturing robot/cell simulation | Enterprise setup and licensing |
| [DELMIA Robotics](https://www.3ds.com/) | P | Robot manufacturing workflows | Platform and controller configuration |
| [Visual Components](https://www.visualcomponents.com/) | P | Production and robot-cell simulation | Product tier and postprocessor limits |
| [Gazebo](https://gazebosim.org/) | O | Open robotics simulation | Select compatible physics and ROS versions |
| [Webots](https://cyberbotics.com/) | O | Robot simulation environment | Model fidelity and device coverage |
| [CoppeliaSim](https://www.coppeliarobotics.com/) | M | Flexible robot simulation | Editions and component licenses differ |
| [MuJoCo](https://mujoco.org/) | O | Fast articulated/contact dynamics | Not complete industrial offline programming |
| [Drake](https://drake.mit.edu/) | O | Robotics dynamics planning and optimization | Code-first research/engineering framework |

**Open foundations to investigate:** ROS 2; MoveIt; Gazebo; MuJoCo; Drake; Pinocchio; Project Chrono.

**Plausible first open product:** A robot-cell simulation and calibration workbench focused on one manipulator and a bounded task.

**Verification and validation targets:** Forward/inverse kinematic consistency, trajectory limits, collision margins and measured pose/latency errors.

## X02 Multiphysics and systems modelling

**Branch:** Cross-disciplinary. **Scope:** Coupled electrical, mechanical, thermal and fluid behavior; system architecture and model exchange.

**Fundamental science:** Conservation laws across domains, constitutive coupling, algebraic constraints and differential-algebraic systems.

**Computational methods:** Monolithic and partitioned solves, symbolic equation processing, co-simulation and model-order reduction.

**Where results go wrong:** Two accurate standalone solvers can become unstable when coupled with poor timing or interfaces. Units, causality and energy transfer across ports must be controlled.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [COMSOL Multiphysics](https://www.comsol.com/products) | P | Coupled field simulation | Modules and model setup determine scope |
| [Ansys Workbench/System Coupling](https://www.ansys.com/) | P | Coupled CAE workflow | Orchestration is not itself a universal solver |
| [Simcenter Amesim](https://www.siemens.com/en-us/products/simcenter/) | P | Lumped multidomain physical systems | Library licensing and parameter quality |
| [Dymola](https://www.3ds.com/) | P | Modelica physical-system modelling | Commercial libraries have separate terms |
| [Simulink with Simscape](https://www.mathworks.com/products/simscape.html) | P | Controls plus physical networks | Multiple licenses and modelling conventions |
| [MapleSim](https://www.maplesoft.com/products/maplesim/) | P | Symbolic multidomain modelling | Specialist library scope |
| [Wolfram System Modeler](https://www.wolfram.com/system-modeler/) | P | Equation-based system simulation | Library and integration differences |
| [Ansys Twin Builder](https://www.ansys.com/) | P | System-level modelling and reduced models | Twin validity depends on calibration |
| [GT-SUITE](https://www.gtisoft.com/gt-suite/) | P | Multiphysics system/component models | Configurable fidelity increases setup burden |
| [OpenModelica](https://openmodelica.org/) | O | Open equation-based system modelling | Model compatibility and solver choice matter |

**Open foundations to investigate:** OpenModelica; FEniCSx; Elmer; Kratos; MOOSE; FMI-compatible adapters.

**Plausible first open product:** A common project shell connecting two verified domain solvers through typed, unit-aware interfaces.

**Verification and validation targets:** Coupled analytical RC/thermal example, energy consistency, step-size sensitivity and comparison to a monolithic reference.

## X03 Numerical computing and optimization

**Branch:** Cross-disciplinary. **Scope:** Engineering calculations, linear algebra, data analysis, parameter estimation, optimization and reproducible notebooks.

**Fundamental science:** Numerical analysis, conditioning, floating-point arithmetic, calculus, probability and constrained optimization.

**Computational methods:** BLAS/LAPACK kernels, sparse solves, FFTs, numerical integration, symbolic manipulation and linear/nonlinear/mixed-integer optimization.

**Where results go wrong:** A fast language cannot fix ill-conditioning or an inappropriate method. Toolbox coverage, reproducibility and trustworthy units matter as much as syntax.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [MATLAB](https://www.mathworks.com/products/matlab.html) | P | Integrated numerical engineering environment | Toolboxes and deployment are separate products |
| [Wolfram Mathematica](https://www.wolfram.com/mathematica/) | P | Symbolic and numerical computing | Language and engine ecosystem differ |
| [Maple](https://www.maplesoft.com/) | P | Symbolic mathematics and engineering analysis | Not MATLAB toolbox compatibility |
| [PTC Mathcad Prime](https://www.ptc.com/en/store) | P | Readable engineering worksheets | Different programming model from MATLAB |
| [GAMS](https://www.gams.com/) | P | Algebraic optimization modelling | Solver licenses may be separate |
| [Gurobi](https://www.gurobi.com/) | P | Mathematical optimization solver | Not a complete engineering desktop environment |
| [IBM ILOG CPLEX Optimization Studio](https://www.ibm.com/) | P | Optimization modelling and solving | Scope and licensing need checking |
| [Python scientific stack](https://scipy.org/) | O | Programmable scientific computing | Assemble and support the environment |
| [Julia with SciML/JuMP](https://julialang.org/) | O | Numerical modelling and optimization | Package/compiler reproducibility matters |
| [GNU Octave](https://octave.org/) | O | MATLAB-like numerical computing | Incomplete toolbox and language parity |

**Open foundations to investigate:** Python/NumPy/SciPy/SymPy/Jupyter; Julia/SciML/JuMP; GNU Octave; Scilab; HiGHS/IPOPT.

**Plausible first open product:** An engineering calculation workspace with units, plots, versioned inputs and solver-backed worksheets; reuse an existing language.

**Verification and validation targets:** Conditioned/ill-conditioned linear systems, optimizer reference problems, unit checks, numerical tolerances and deterministic replay.

## X04 Industrial systems, logistics and reliability

**Branch:** Cross-disciplinary. **Scope:** Factories, queues, resource scheduling, throughput, maintenance, failure and repair processes.

**Fundamental science:** Queueing theory, probability, discrete events, Markov processes, reliability block diagrams and optimization.

**Computational methods:** Discrete-event simulation, Monte Carlo, scheduling optimization, fault trees and statistical fitting.

**Where results go wrong:** Good animation can conceal poor input distributions. Rare failures require appropriate sampling; throughput and physical process simulation are different layers.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [AnyLogic](https://www.anylogic.com/) | P | Discrete-event agent and system-dynamics modelling | Edition and deployment terms |
| [Simio](https://www.simio.com/) | P | Production/logistics simulation and scheduling | Data preparation and calibration |
| [Siemens Plant Simulation](https://www.siemens.com/) | P | Factory and material-flow simulation | Not detailed mechanical physics |
| [FlexSim](https://www.flexsim.com/) | P | 3D discrete-event operations simulation | Model logic matters more than animation |
| [Arena](https://www.rockwellautomation.com/) | P | Discrete-event process simulation | Statistical experimental design required |
| [SIMUL8](https://www.simul8.com/) | P | Operations and process simulation | Application-specific modelling work |
| [ExtendSim](https://extendsim.com/) | P | Discrete-event and continuous simulation | Libraries and deployment terms |
| [ReliaSoft suite](https://www.hbkworld.com/) | P | Reliability and maintainability analysis | Companion specialty, not factory flow simulation |
| [SimPy](https://simpy.readthedocs.io/) | O | Python discrete-event simulation | No complete graphical modeller included |
| [JaamSim](https://jaamsim.com/) | O | Open graphical discrete-event simulation | Specialized models and support need evaluation |

**Open foundations to investigate:** SimPy; salabim; JaamSim; OR-Tools; reliability libraries with checked licenses.

**Plausible first open product:** An open production-flow modeller with transparent distributions, repeatable experiments and confidence intervals.

**Verification and validation targets:** Analytical M/M/1 queues within assumptions, resource accounting, seeded repeatability and held-out production/repair data.

## Information technology branch

**Added 7 October 2026.** Twelve IT subfields with ten entries each: 120 field-tool entries. Field IDs use the prefix **I**.

### Why IT belongs in an engineering atlas

Modern engineering systems run on IT. A SCADA system is a networked database with screens. A substation relay talks IEC 61850 over Ethernet. A mine's process historian, wireless links, PLC networks and remote access paths are IT systems with physical consequences. A solar plant's monitoring, an XRF analyser's web interface and a BIM coordination server all depend on networks, databases, security and backups.

| Intersection | What joins together | Software consequences |
|---|---|---|
| Electrical + IT | SCADA, substation automation, PLC networks, energy metering | Industrial protocols, OT security, historians and time synchronisation |
| Electronics + IT | Embedded devices, IoT sensors, firmware updates | MQTT and OPC UA ingestion, device management, secure update pipelines |
| Mechanical + IT | Condition monitoring, vibration data, maintenance systems | Time-series storage, asset registers, analytics pipelines |
| Civil + IT | GIS, survey data, BIM coordination, smart water networks | Spatial databases, large file collaboration, field data collection |
| All five | Digital representations of physical assets | Shared identifiers, data ownership, access control, backups and audit trails |

The industry term for this overlap is **IT/OT convergence**. IT (information technology) prioritises confidentiality and fast change. OT (operational technology: PLCs, SCADA, drives, analysers) prioritises availability and safety, and changes slowly. The Purdue reference model and IEC 62443 zones and conduits describe how to separate and connect the two.

### The key finding for IT

IT is different from the engineering branches. In simulation and design (power studies, FEA, CFD, CAD), closed commercial suites dominate and open alternatives lag in usability. In IT infrastructure, **open source already dominates the foundations**: Linux, Kubernetes, PostgreSQL, Prometheus, Wireshark, Ansible, Zeek and Suricata are industry standards in their own right. Commercial IT products often package, host or manage these open cores.

That changes the opportunity. For IT, reimplementing software from scratch rarely makes sense. The value is in:

1. **Integration and packaging:** pre-built, tested bundles that a small organisation can deploy without a specialist.
2. **Domain adaptation:** monitoring templates for industrial devices, OT-aware security rules, mine-site link planning.
3. **Services:** design, deployment, managed monitoring and security reporting built on open tools.
4. **Gaps where open tools are weak:** industrial historians, OT asset visibility, RF and link planning with good interfaces, and field-service record systems for engineering contractors.

### License shifts are a planning risk

Between 2023 and 2025 several widely used IT projects changed their terms. Terraform and Vault moved to the Business Source License (OpenTofu and OpenBao forked). Redis moved to source-available terms in 2024, then added AGPLv3 with Redis 8 in 2025 (Valkey forked in between). Perforce moved Puppet development into private repositories, and the community responded with the OpenVox fork. Broadcom ended free ESXi in 2024 and then brought back a free entry edition in 2025. Elastic added an AGPL option in 2024 alongside its source-available licenses.

The lesson for Quantic: prefer projects governed by neutral foundations (Linux Foundation, Apache, CNCF, OpenSSF), record the exact license of every release you depend on, and keep an exit plan for every dependency. The same rule protects the engineering suites.

### How the IT branch connects to the Quantic suite

Two IT fields are infrastructure for the whole project rather than products:

- **I10 DevOps** provides the build backbone: self-hosted Git, CI, container registry and reproducible releases for every Quantic department.
- **I11 Databases** provides the shared storage layer, and its proposed open historian connects directly to SCADA (E06), renewables monitoring (E08) and condition monitoring.

Three IT fields map closely to work already done on mine sites: **I07 OT security**, **I04 wireless link planning** and **I12 field-service and asset records**.

## I01 Network design, simulation and emulation

**Branch:** Information technology. **Scope:** Topology design, protocol behaviour, capacity planning, training labs and pre-change testing.

**Fundamental science:** Graph theory, queueing, protocol state machines (OSPF, BGP, spanning tree), TCP congestion control and traffic engineering.

**Computational methods:** Discrete-event packet simulation; virtualised emulation of real network operating systems; Linux namespaces and containers; topology defined as code.

**Where results go wrong:** Simulators approximate vendor behaviour. Emulation needs licensed images and memory. Lab results do not reproduce production scale, timing or hardware forwarding behaviour.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Cisco Packet Tracer](https://www.netacad.com/cisco-packet-tracer) | F | Network learning and CCNA-level simulation | Simulated device behaviour; free but closed, via Cisco Networking Academy |
| [Cisco Modeling Labs](https://developer.cisco.com/modeling-labs/) | M | Real Cisco OS images in virtual topologies | Free tier is node-limited; larger labs need paid tiers |
| [GNS3](https://www.gns3.com/) | O | Multivendor network emulation with real images | Vendor router images carry their own licenses |
| [EVE-NG](https://www.eve-ng.net/) | M | Multivendor lab emulation | Community edition is free but closed; Pro is paid |
| [Riverbed Modeler](https://www.riverbed.com/) | P | Discrete-event network performance modelling (OPNET lineage) | Check current product availability and support |
| [NetSim](https://www.tetcos.com/) | P | Network simulation and emulation for research and teaching | Protocol libraries depend on edition |
| [containerlab](https://containerlab.dev/) | O | Container-based network labs defined as code | Needs container-packaged network operating systems |
| [Mininet](https://mininet.org/) | O | SDN and OpenFlow emulation on one Linux host | Namespaces and virtual switches, not a multivendor router emulator |
| [ns-3](https://www.nsnam.org/) | O | Packet-level discrete-event network research | Result validity depends on the chosen models |
| [OMNeT++](https://omnetpp.org/) | S | Modular discrete-event network simulation | Academic Public License; commercial use through OMNEST |

**Open foundations to investigate:** containerlab; GNS3; ns-3; Mininet; FRRouting; Open vSwitch.

**Plausible first open product:** A topology-as-code lab manager on containerlab with FRRouting and Open vSwitch nodes, saved scenarios and automatic reachability checks.

**Verification and validation targets:** Routing convergence on reference topologies, reachability matrices, link-failure injection and comparison with a physical lab.

**Source material to study:** RFC 2328 (OSPFv2), RFC 4271 (BGP-4), IEEE 802.1Q; Kurose and Ross, *Computer Networking: A Top-Down Approach*; Odom, *CCNA Official Cert Guide*; the ns-3 and containerlab manuals.

## I02 Network and infrastructure monitoring

**Branch:** Information technology. **Scope:** Availability, performance, capacity and alerting for networks, servers and services.

**Fundamental science:** Sampling theory, time-series statistics, the SNMP information model, counter-to-rate conversion and alert state machines.

**Computational methods:** SNMP and ICMP polling; streaming telemetry (gNMI); flow analysis (NetFlow, IPFIX, sFlow); time-series storage and query; thresholds and anomaly detection.

**Where results go wrong:** Polling intervals hide microbursts. Counter wraps and gaps distort rates. Alert floods hide real faults. Monitoring that shares a failure domain with the network goes blind during outages.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [SolarWinds Network Performance Monitor](https://www.solarwinds.com/network-performance-monitor) | P | Enterprise network performance monitoring | Licensing scope and supply-chain security review |
| [PRTG Network Monitor](https://www.paessler.com/prtg) | P | Sensor-based all-in-one monitoring | Licensed by sensor count |
| [Datadog Network Monitoring](https://www.datadoghq.com/) | P | Cloud SaaS observability | Per-host and data-volume pricing; data leaves site |
| [LogicMonitor](https://www.logicmonitor.com/) | P | SaaS infrastructure monitoring | Collector placement and data residency |
| [Zabbix](https://www.zabbix.com/) | O | Agent and SNMP infrastructure monitoring | AGPL licensing since version 7; template quality varies |
| [Nagios Core](https://www.nagios.org/) | O/M | Check-based availability monitoring | Nagios XI is commercial; core interface is dated |
| [LibreNMS](https://www.librenms.org/) | O | Auto-discovering SNMP network monitoring | Large estates need distributed pollers |
| [Prometheus with Grafana](https://prometheus.io/) | O | Metrics time series, alerting and dashboards | Grafana is AGPL; long-term storage is a separate choice |
| [Checkmk](https://checkmk.com/) | O/M | Rule-based infrastructure monitoring | Raw edition is open; higher editions are commercial |
| [Observium](https://www.observium.org/) | M | SNMP network monitoring | Community edition carries restricted terms |

**Open foundations to investigate:** Prometheus; Grafana; Zabbix; LibreNMS; Telegraf; VictoriaMetrics; pmacct for flows.

**Plausible first open product:** A site-ready monitoring appliance image with templates for common enterprise and industrial devices and an automatic outage report.

**Verification and validation targets:** Simulated device outages, counter-wrap tests, known iperf3 traffic loads and alert timing and escalation tests.

**Source material to study:** RFC 3411 to 3418 (SNMPv3), RFC 7011 (IPFIX), OpenConfig gNMI specification; Google's *Site Reliability Engineering* (free online); Prometheus and Zabbix documentation.

## I03 Network automation and source of truth

**Branch:** Information technology. **Scope:** Configuration generation, deployment, compliance and an authoritative record of intended network state.

**Fundamental science:** Declarative desired state, idempotence, graph models of topology and formal reasoning about forwarding and reachability.

**Computational methods:** Templating; API and CLI drivers; diff and dry run; YANG data models; parsing vendor configuration into neutral models; control-plane simulation for verification.

**Where results go wrong:** Automation repeats mistakes at scale. A stale source of truth generates wrong configuration. CLI parsing is brittle. Partial pushes leave inconsistent states.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Cisco Catalyst Center](https://developer.cisco.com/docs/catalyst-center/) | P | Intent-based management of Cisco campus networks | Formerly DNA Center; Cisco-centric |
| [Juniper Apstra](https://www.juniper.net/us/en/products/network-automation/apstra.html) | P | Intent-based data-centre fabric automation | Data-centre fabric scope; Juniper is now part of HPE |
| [Itential](https://www.itential.com/) | P | Network automation orchestration platform | Platform tiers and integration effort |
| [Forward Enterprise](https://www.forwardnetworks.com/) | P | Network digital twin and path verification | Fidelity depends on configuration and state collection |
| [NetBrain](https://www.netbraintech.com/) | P | Network mapping and runbook automation | Map accuracy depends on discovery coverage |
| [Ansible](https://docs.ansible.com/) | O/M | Agentless configuration automation | Automation Platform is commercial; idempotence varies by module |
| [NetBox](https://netboxlabs.com/) | O/M | IPAM, DCIM and network source of truth | Cloud and enterprise editions are commercial; data quality is the product |
| [Nautobot](https://networktocode.com/nautobot/) | O | Source of truth with automation apps | App ecosystem maturity varies |
| [Batfish](https://www.batfish.org/) | O | Pre-deployment configuration analysis and verification | Vendor configuration parser coverage |
| [NAPALM and Netmiko](https://napalm.readthedocs.io/) | O | Python libraries for multivendor device access | Libraries, not a platform |

**Open foundations to investigate:** NetBox; Nautobot; Ansible; Nornir; NAPALM; Netmiko; Batfish; OpenConfig models.

**Plausible first open product:** A source-of-truth-to-configuration pipeline: NetBox data, templates, Batfish pre-checks, staged deployment and an automatic rollback report.

**Verification and validation targets:** Golden configuration diffs, Batfish reachability assertions, dry-run versus applied state and rollback drills.

**Source material to study:** RFC 6241 (NETCONF), RFC 7950 (YANG 1.1), RFC 8040 (RESTCONF); Edelman, Lowe and Oswalt, *Network Programmability and Automation*; the Batfish NSDI 2015 paper.

## I04 Wireless, RF and link planning

**Branch:** Information technology. **Scope:** Wi-Fi design, cellular and DAS coverage, point-to-point microwave links and wireless ISP networks.

**Fundamental science:** Electromagnetic propagation, free-space path loss, Fresnel zones, terrain diffraction, fading, link budgets, SINR and Shannon capacity.

**Computational methods:** Empirical and deterministic propagation models (Longley-Rice/ITM, Okumura-Hata, ray tracing); terrain elevation processing; coverage rasters; channel planning.

**Where results go wrong:** Models need local calibration. Terrain and clutter resolution limit accuracy. Predicted coverage without a survey misleads. Permitted power and bands differ by country.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Ekahau AI Pro](https://www.ekahau.com/) | P | Enterprise Wi-Fi survey and design | Survey hardware needed to validate designs |
| [Hamina Network Planner](https://www.hamina.com/) | P | Cloud-based Wi-Fi planning | Cloud subscription |
| [iBwave Design](https://www.ibwave.com/) | P | In-building cellular, DAS and Wi-Fi design | Capabilities depend on modules |
| [Forsk Atoll](https://www.forsk.com/) | P | Operator radio network planning | Operator-scale data and calibration |
| [Infovista Planet](https://www.infovista.com/) | P | RF planning and optimization | Propagation models need calibration |
| [Cambium LINKPlanner](https://www.cambiumnetworks.com/products/software/linkplanner/) | F | Point-to-point and point-to-multipoint link planning | Focused on Cambium hardware |
| [UISP Design Center](https://design.uisp.com/) | F | Wireless ISP link and site design | Ubiquiti-centric |
| [Radio Mobile](https://www.ve2dbe.com/english1.html) | F | Terrain-based VHF, UHF and microwave coverage | Windows freeware with a dated interface |
| [SPLAT!](https://www.qsl.net/kd2bd/splat.html) | O | Terrain path and Longley-Rice coverage analysis | Command-line; terrain data preparation required |
| [Signal-Server](https://github.com/Cloud-RF/Signal-Server) | O | Multithreaded RF coverage engine | Engine without a design interface |

**Open foundations to investigate:** SPLAT!; Signal-Server; NTIA ITM reference code; QGIS and GDAL; SRTM and Copernicus elevation data.

**Plausible first open product:** A link-and-coverage planner for mine and rural sites: terrain profiles, Fresnel clearance, link budgets and GIS-ready coverage maps.

**Verification and validation targets:** Free-space analytical cases, published ITM test cases, survey measurements and measured link RSSI against prediction.

**Source material to study:** ITU-R P.525, P.526 and P.530; NTIA Irregular Terrain Model documentation; Rappaport, *Wireless Communications: Principles and Practice*; CWNA study guide; ZICTA spectrum and type-approval rules for Zambia.

## I05 Security monitoring, SIEM and detection

**Branch:** Information technology. **Scope:** Collecting logs and network telemetry, detecting threats, triage and incident response.

**Fundamental science:** Event correlation, statistical anomaly detection, attacker behaviour models (MITRE ATT&CK) and protocol analysis.

**Computational methods:** Log parsing and normalisation; indexing and search; correlation rules; signature-based intrusion detection; behavioural analytics; case management.

**Where results go wrong:** Missing log sources create blind spots. Untuned rules flood analysts. Clock drift breaks correlation. Ingestion pricing pushes teams to drop valuable data.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Splunk Enterprise Security](https://www.splunk.com/) | P | SIEM and security analytics | Ingest-based pricing; Splunk is now part of Cisco |
| [Microsoft Sentinel](https://learn.microsoft.com/azure/sentinel/) | P | Cloud-native SIEM on Azure | Azure data ingestion and retention costs |
| [CrowdStrike Falcon](https://www.crowdstrike.com/) | P | Endpoint detection and response | Agent-based subscription |
| [Cortex XSIAM](https://www.paloaltonetworks.com/cortex/cortex-xsiam) | P | SOC platform from Palo Alto Networks | Platform scope; absorbed QRadar SaaS customers |
| [Elastic Security](https://www.elastic.co/security) | O/M | SIEM built on Elasticsearch | AGPL, SSPL or Elastic License options; some features in paid tiers |
| [Wazuh](https://wazuh.com/) | O | Open XDR and SIEM with host intrusion detection lineage | Rule tuning and scale-out effort |
| [Security Onion](https://securityonion.net/) | M | Integrated network security monitoring distribution | Check the license of each release and bundled component |
| [Graylog](https://graylog.org/) | S | Log management and SIEM | Graylog Open uses SSPL, which is not OSI open source |
| [Suricata](https://suricata.io/) | O | Network IDS, IPS and security monitoring | Rule tuning and throughput sizing |
| [Zeek](https://zeek.org/) | O | Network traffic analysis and protocol logging | Analysis and logging, not an inline blocker |

**Open foundations to investigate:** Wazuh; Suricata; Zeek; OpenSearch; Sigma rules; MISP; Security Onion components after license checks.

**Plausible first open product:** A small-organisation security monitoring kit: Wazuh with Suricata and Zeek, curated Sigma rules, local playbooks and a monthly report.

**Verification and validation targets:** Atomic Red Team executions, replayed PCAPs with known attacks, ATT&CK coverage mapping and false-positive rate on normal traffic.

**Source material to study:** MITRE ATT&CK; NIST SP 800-61 (incident handling) and SP 800-92 (log management); the Sigma rule specification; Zambia's Data Protection Act 2021 and current cyber security legislation.

## I06 Packet analysis, vulnerability assessment and penetration testing

**Branch:** Information technology. **Scope:** Protocol troubleshooting, asset discovery, vulnerability assessment and authorised penetration testing.

**Fundamental science:** Protocol specifications, TCP/IP stack behaviour, fingerprinting, vulnerability scoring (CVSS) and attack graphs.

**Computational methods:** Packet capture and dissection; active probing and service fingerprinting; version-to-CVE matching; authenticated configuration checks; exploit validation.

**Where results go wrong:** Scans can disrupt fragile devices, especially in OT. Version matching produces false positives. Testing without written authorisation is illegal. Results go stale quickly.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Wireshark](https://www.wireshark.org/) | O | Packet capture and protocol dissection | Analysis tool, not a monitoring platform |
| [tcpdump and libpcap](https://www.tcpdump.org/) | O | Command-line capture and capture library | Text output and capture filters only |
| [Nmap](https://nmap.org/) | S | Network discovery and port scanning | Nmap Public Source License restricts proprietary redistribution |
| [Tenable Nessus](https://www.tenable.com/products/nessus) | P | Vulnerability scanning | Plugin feed is a subscription; Essentials tier is limited |
| [Qualys VMDR](https://www.qualys.com/) | P | Cloud vulnerability management | Agent and scanner licensing |
| [Rapid7 InsightVM](https://www.rapid7.com/products/insightvm/) | P | Vulnerability risk management | Subscription licensing |
| [Burp Suite Professional](https://portswigger.net/burp) | P | Web application security testing | Community edition is limited |
| [Metasploit Framework](https://www.metasploit.com/) | O/M | Exploit development and validation | Authorized testing only; Metasploit Pro is commercial |
| [Greenbone OpenVAS](https://www.greenbone.net/) | O/M | Open vulnerability scanning | Community feed differs from the enterprise feed |
| [ZAP](https://www.zaproxy.org/) | O | Open web application security scanner | Dynamic testing has coverage limits |

**Open foundations to investigate:** Wireshark; Nmap (license check); OpenVAS; ZAP; Nuclei; NVD and CISA KEV data feeds.

**Plausible first open product:** A vulnerability reporting workbench that imports Nmap and OpenVAS results, enriches them with NVD and CISA KEV data, prioritises and produces client reports.

**Verification and validation targets:** Deliberately vulnerable lab targets, known CVE detection rates, false-positive review and report reproducibility.

**Source material to study:** RFC 791 (IPv4) and RFC 9293 (TCP); Stevens, *TCP/IP Illustrated, Volume 1*; OWASP Web Security Testing Guide; NIST SP 800-115; the CVSS v4.0 specification.

## I07 Industrial networks and OT security

**Branch:** Information technology. **Scope:** Plant networks, PLC and SCADA communication, OT asset inventory, segmentation and industrial threat detection.

**Fundamental science:** Industrial protocols (Modbus, DNP3, EtherNet/IP, PROFINET, IEC 61850), Purdue and zone-and-conduit models and the interaction of safety and security.

**Computational methods:** Passive traffic analysis; industrial protocol deep packet inspection; behavioural baselining; asset fingerprinting; segmentation verification.

**Where results go wrong:** Active scanning can trip controllers. Proprietary or encrypted protocols resist inspection. Flat networks spread incidents. IT patch cycles do not fit OT outage windows.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Claroty xDome](https://claroty.com/) | P | OT and IoT asset visibility and threat detection | Passive sensor placement and coverage |
| [Nozomi Networks Guardian](https://www.nozominetworks.com/) | P | OT network monitoring and anomaly detection | Sensor deployment and tuning |
| [Dragos Platform](https://www.dragos.com/) | P | ICS threat detection and response | Industrial-focused licensing |
| [Tenable OT Security](https://www.tenable.com/products/tenable-ot) | P | OT asset inventory and vulnerability management | Review the safety of any active queries |
| [Microsoft Defender for IoT](https://learn.microsoft.com/azure/defender-for-iot/) | P | OT monitoring within Microsoft security tooling | Microsoft and Azure ecosystem |
| [Siemens SINEC NMS](https://www.siemens.com/) | P | Industrial network management for Siemens networks | Siemens-centric device support |
| [Moxa MXview One](https://www.moxa.com/) | P | Industrial network topology and monitoring | Strongest with Moxa devices |
| [Belden Industrial HiVision](https://www.belden.com/) | P | Industrial Ethernet network management | Strongest with Hirschmann and Belden devices |
| [Malcolm](https://github.com/cisagov/Malcolm) | O | Open traffic analysis suite for ICS networks (CISA) | Resource-heavy integration of many components |
| [Zeek ICSNPP parsers](https://github.com/cisagov/ICSNPP) | O | Industrial protocol parsers for Zeek | Coverage differs by protocol |

**Open foundations to investigate:** Malcolm; Zeek with ICSNPP; Suricata; Wireshark industrial dissectors; GRASSMARLIN as historical reference only.

**Plausible first open product:** A passive OT visibility kit for mine sites: span-port capture, asset inventory, protocol map and an IEC 62443 zone-and-conduit report.

**Verification and validation targets:** Recorded PCAPs from lab PLCs, known asset lists, injected anomalies such as unexpected writes and proof of no impact on live networks.

**Source material to study:** IEC 62443 series; NIST SP 800-82 Rev. 3; Modbus Application Protocol specification (modbus.org); Knapp and Langill, *Industrial Network Security*; CISA ICS advisories.

## I08 Endpoint, systems and configuration management

**Branch:** Information technology. **Scope:** Device inventory, patching, software deployment, configuration baselines and remote support.

**Fundamental science:** Desired-state convergence, idempotent operations, inventory data models and scheduling.

**Computational methods:** Agent-based and agentless execution; pull-based convergence; package management; policy evaluation; remote command execution.

**Where results go wrong:** Manual changes cause drift. A bad policy reaches every device. A compromised agent compromises the fleet. Vendor license changes can strand users.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Microsoft Intune](https://learn.microsoft.com/mem/intune/) | P | Cloud device management (MDM and MAM) | Microsoft 365 licensing |
| [Microsoft Configuration Manager](https://learn.microsoft.com/mem/configmgr/) | P | On-premises Windows estate management | Windows-centric and infrastructure-heavy |
| [Jamf Pro](https://www.jamf.com/products/jamf-pro/) | P | Apple device management | Apple devices only |
| [ManageEngine Endpoint Central](https://www.manageengine.com/products/desktop-central/) | P | Unified endpoint management | Edition and module tiers |
| [NinjaOne](https://www.ninjaone.com/) | P | Remote monitoring and management for IT teams and MSPs | Per-device subscription |
| [OpenVox](https://voxpupuli.org/) | O | Declarative configuration management (community Puppet fork) | Forked after Perforce moved Puppet development to private repositories |
| [Salt](https://saltproject.io/) | O | Event-driven configuration and remote execution | Owned by Broadcom; check roadmap |
| [Chef Infra](https://www.chef.io/) | O/M | Code-driven configuration management | Source is Apache-licensed; official distributions have commercial terms |
| [osquery with Fleet](https://osquery.io/) | O/M | SQL-queried endpoint telemetry and fleet management | Fleet premium features are commercial |
| [MeshCentral](https://meshcentral.com/) | O | Self-hosted remote management and remote desktop | Security hardening is the operator's responsibility |

**Open foundations to investigate:** OpenVox; Salt; Ansible; osquery; Fleet; MeshCentral; RustDesk.

**Plausible first open product:** A small-business IT management bundle: osquery inventory, Ansible patching and baselines, MeshCentral remote support and one dashboard.

**Verification and validation targets:** Baseline compliance on test machines, canary patch rollouts, rollback and loss-of-agent scenarios.

**Source material to study:** CIS Benchmarks and CIS Controls; Limoncelli, Hogan and Chalup, *The Practice of System and Network Administration*; Ansible and OpenVox documentation.

## I09 Virtualization and private cloud

**Branch:** Information technology. **Scope:** Server consolidation, virtual machines, software-defined storage and private cloud.

**Fundamental science:** Hardware-assisted virtualization, CPU and memory scheduling, storage replication and distributed consensus.

**Computational methods:** Hypervisors; live migration; software-defined storage (Ceph, ZFS); clustering, high availability and quorum.

**Where results go wrong:** Overcommitment causes contention. Clusters without quorum risk split-brain. Storage latency dominates performance. Vendor licensing shifts can force migrations.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [VMware vSphere](https://www.vmware.com/) | P | Enterprise server virtualization | Broadcom subscriptions; free ESXi entry edition returned in 2025 without support |
| [Microsoft Hyper-V](https://learn.microsoft.com/windows-server/virtualization/hyper-v/) | P | Windows Server virtualization | Windows Server licensing |
| [Nutanix AHV](https://www.nutanix.com/) | P | Hyperconverged infrastructure | Community Edition has limits |
| [XenServer](https://www.xenserver.com/) | P | Xen-based enterprise virtualization | Check current ownership, naming and licensing |
| [Proxmox VE](https://www.proxmox.com/) | O | KVM and container virtualization platform | AGPL; enterprise repository needs a subscription |
| [XCP-ng](https://xcp-ng.org/) | O | Open Xen hypervisor platform | Xen Orchestra source builds differ from the supported appliance |
| [KVM, QEMU and libvirt](https://www.qemu.org/) | O | Linux virtualization building blocks | Components, not a management platform |
| [OpenStack](https://www.openstack.org/) | O | Private infrastructure-as-a-service cloud | High operational complexity |
| [Apache CloudStack](https://cloudstack.apache.org/) | O | Turnkey IaaS cloud orchestration | Smaller ecosystem than OpenStack |
| [Harvester](https://harvesterhci.io/) | O | Kubernetes-based hyperconverged infrastructure | Requires Kubernetes operating skills |

**Open foundations to investigate:** Proxmox VE; KVM, QEMU and libvirt; Ceph; ZFS; XCP-ng; OpenStack.

**Plausible first open product:** A tested Proxmox reference design and VMware-to-Proxmox migration kit with documentation for small and mid-sized organisations.

**Verification and validation targets:** Live migration under load, node-failure HA tests, fio storage benchmarks and backup restore drills.

**Source material to study:** Popek and Goldberg (1974) on virtualization requirements; Smith and Nair, *Virtual Machines*; the Proxmox VE administration guide; Ceph documentation.

## I10 DevOps, containers and infrastructure as code

**Branch:** Information technology. **Scope:** Version control, build and deployment pipelines, infrastructure as code, containers, orchestration and secrets.

**Fundamental science:** Declarative desired state, reconciliation loops, dependency graphs and distributed consensus (Raft).

**Computational methods:** Plan-and-apply diffs; layered container images; scheduling; GitOps reconciliation; pipeline execution.

**Where results go wrong:** State drift or corruption, secrets leaking through pipelines, unpinned dependencies and vendor license changes.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Terraform](https://www.terraform.io/) | S | Infrastructure as code | Business Source License since 2023; HashiCorp is now part of IBM |
| [OpenTofu](https://opentofu.org/) | O | Open-source fork of Terraform | Provider compatibility varies by version |
| [Kubernetes](https://kubernetes.io/) | O | Container orchestration | Operational complexity for small teams |
| [Red Hat OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) | P | Enterprise Kubernetes platform | Subscription; OKD is the community distribution |
| [Docker Engine (Moby)](https://docs.docker.com/engine/) | O | Container build and runtime | Docker Desktop has separate commercial terms |
| [GitLab](https://about.gitlab.com/) | O/M | Git hosting, CI/CD and DevSecOps | Community edition is open; enterprise features are proprietary |
| [GitHub Actions](https://docs.github.com/actions) | P | Hosted CI/CD on GitHub | Hosted minutes and runner policies |
| [Jenkins](https://www.jenkins.io/) | O | Self-hosted CI automation server | Plugin sprawl and maintenance burden |
| [Argo CD](https://argo-cd.readthedocs.io/) | O | GitOps continuous delivery for Kubernetes | Kubernetes-only |
| [HashiCorp Vault](https://www.vaultproject.io/) | S | Secrets management | Business Source License; OpenBao is the open fork |

**Open foundations to investigate:** OpenTofu; Kubernetes; k3s; Podman; Forgejo; Woodpecker CI; Argo CD; OpenBao.

**Plausible first open product:** A self-hosted engineering platform template (Forgejo, CI, container registry, OpenTofu) that also becomes the build backbone for the Quantic suite.

**Verification and validation targets:** Reproducible builds, plan/apply idempotence, Git and registry disaster recovery and secret scanning.

**Source material to study:** The Twelve-Factor App; Kim, Humble, Debois and Willis, *The DevOps Handbook*; Ongaro and Ousterhout (2014) on Raft; Kubernetes and OpenTofu documentation.

## I11 Databases, time series and industrial historians

**Branch:** Information technology. **Scope:** Transactional data, analytics, caching, time-series sensor data and industrial process history.

**Fundamental science:** Relational algebra, ACID transactions, B-tree and LSM indexing, consistency models and time-series compression.

**Computational methods:** Query planning; write-ahead logging; replication; columnar storage; downsampling and retention.

**Where results go wrong:** Weak schema design, missing backups, untested restores, runaway time-series cardinality and historian licensing that locks plant data in.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [Oracle Database](https://www.oracle.com/database/) | P | Enterprise relational database | Licensing complexity |
| [Microsoft SQL Server](https://www.microsoft.com/sql-server) | P | Enterprise relational database | Core-based licensing; Express edition limits |
| [AVEVA PI System](https://www.aveva.com/en/products/aveva-pi-system/) | P | Industrial process historian | Tag-based licensing; data held in vendor formats |
| [PostgreSQL](https://www.postgresql.org/) | O | General-purpose relational database | Tuning and high availability are separate design work |
| [MySQL](https://www.mysql.com/) | O/M | Relational database for web workloads | GPL community edition versus Oracle commercial editions; MariaDB is the fork |
| [MongoDB](https://www.mongodb.com/) | S | Document database | SSPL is not an OSI-approved open-source license |
| [Redis](https://redis.io/) | O | In-memory data store and cache | Redis 8 added AGPLv3; Valkey is the BSD-licensed fork |
| [TimescaleDB](https://github.com/timescale/timescaledb) | O/M | Time-series extension for PostgreSQL | Some features use the Timescale License rather than Apache |
| [InfluxDB](https://www.influxdata.com/) | O/M | Time-series metrics database | Version 3 Core is open; Enterprise is commercial |
| [SQLite](https://www.sqlite.org/) | O | Embedded single-file database | Single-writer concurrency |

**Open foundations to investigate:** PostgreSQL; TimescaleDB (license check); SQLite; Valkey; DuckDB; ClickHouse.

**Plausible first open product:** An open industrial historian: OPC UA and MQTT ingestion into PostgreSQL with tag metadata, trends and export for plants priced out of commercial historians.

**Verification and validation targets:** Ingestion rate tests, restore drills, timestamp ordering, compression ratio and query results against raw data.

**Source material to study:** Kleppmann, *Designing Data-Intensive Applications*; Date, *An Introduction to Database Systems*; PostgreSQL documentation; OPC UA (IEC 62541) and MQTT 5.0 specifications.

## I12 IT service management, assets and documentation

**Branch:** Information technology. **Scope:** Incident, request, change and problem management; asset registers; documentation and knowledge.

**Fundamental science:** Queueing and service levels, workflow state machines and configuration-item relationship graphs.

**Computational methods:** Ticket workflows; SLA timers; CMDB relationships; discovery; knowledge search.

**Where results go wrong:** A CMDB decays without discovery. Heavy process burdens small teams. SaaS platforms can lock in service history.

| Tool or toolchain | Access | Best-fit job | Boundary to check |
|---|---|---|---|
| [ServiceNow ITSM](https://www.servicenow.com/) | P | Enterprise ITSM and workflow platform | High implementation cost |
| [Jira Service Management](https://www.atlassian.com/software/jira/service-management) | P | Service desk on the Atlassian platform | Atlassian is moving self-hosted customers to cloud |
| [Freshservice](https://www.freshworks.com/freshservice/) | P | Cloud ITSM for mid-sized organisations | Plan tiers |
| [ManageEngine ServiceDesk Plus](https://www.manageengine.com/products/service-desk/) | P | ITIL service desk with asset management | Edition tiers |
| [IT Glue](https://www.itglue.com/) | P | IT documentation for MSPs | Subscription within the Kaseya ecosystem |
| [GLPI](https://glpi-project.org/) | O | ITSM and asset management | Plugin quality varies |
| [Zammad](https://zammad.org/) | O | Helpdesk and ticketing | Not a full ITIL suite |
| [Snipe-IT](https://snipeitapp.com/) | O | IT asset management | Asset-focused only |
| [iTop](https://www.combodo.com/itop) | O | ITSM with a configuration management database | Data model takes time to learn |
| [Request Tracker](https://bestpractical.com/request-tracker) | O | Ticket tracking | Perl stack to maintain |

**Open foundations to investigate:** GLPI; Zammad; Snipe-IT; iTop; BookStack; NetBox for network assets.

**Plausible first open product:** A lightweight field-service and asset system for engineering contractors: site assets, visit logs, calibration records and client reports.

**Verification and validation targets:** Workflow transitions, SLA timer accuracy, asset import round trips and audit-trail completeness.

**Source material to study:** ITIL 4 concepts (a licensed publication: learn the ideas, do not copy the text); ISO/IEC 20000-1; GLPI and iTop documentation.

## Implementation evidence register

This table deliberately separates implementation, extension languages, generated code and hypotheses. The workbook applies these categories to every catalogue row; an unreviewed open project is labelled as unreviewed rather than assigned a guessed language.

| Product/component | Implementation evidence | User/extension language | Confidence and boundary | Source |
|---|---|---|---|---|
| MATLAB | Historic Fortran; commercial rewrite C; R2025a UI HTML/JavaScript | MATLAB; C/C++/Fortran MEX | Documented history, UI and interfaces. Complete modern internal language mix not established | [Primary reference](https://www.mathworks.com/company/technical-articles/a-brief-history-of-matlab.html) |
| MATLAB desktop | Java historically; HTML/JavaScript in R2025a rebuild | MATLAB | Documented implementation component. Does not identify the numerical engine language | [Primary reference](https://blogs.mathworks.com/matlab/2025/05/16/whats-with-all-the-big-changes-in-r2025a/) |
| Ignition | Java platform | Python via Jython; SQL | Documented platform and scripting. Do not infer every module or browser component is Java | [Primary reference](https://www.docs.inductiveautomation.com/docs/8.3/platform) |
| PSCAD/EMTDC | Fortran/C simulation compilation path | Graphical models; Fortran/C components | Documented generated-code/runtime path. Does not establish PSCAD GUI implementation | [Primary reference](https://www.pscad.com/knowledge-base/article/584) |
| Ansys Fluent | Closed core; C/C++ is a plausible native-core hypothesis | C/C++ UDFs | Documented interface; core hypothesis. UDF language is not a complete core-language inventory | [Primary reference](https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/flu_udf/flu_udf_WhatIsAUDF.html) |
| SIMULIA Abaqus | Closed core; C/C++/Fortran are plausible solver languages | Python scripting; C/C++/Fortran user subroutines | Documented interfaces; core hypothesis. Subsystem-by-subsystem implementation remains unverified | [Primary reference](https://docs.software.vt.edu/abaqusv2025/English/SIMACAESUBRefMap/simasub-c-subroutineover.htm) |
| FreeCAD | C++ and Python | Python | Direct public source documentation. Plugins and bundled libraries have their own implementations | [Primary reference](https://www.freecad.org/api/) |
| KiCad | C++ components; Python integration | Python interfaces; schematic/PCB formats | Direct public source documentation. Library data licensing differs from application licensing | [Primary reference](https://docs.kicad.org/doxygen/python__manager_8cpp_source.html) |
| OpenFOAM | C++ | C++ extensions; case dictionaries | Direct public source documentation. Choose a particular distribution and release | [Primary reference](https://openfoam.org/resources/) |
| OpenDSS | Delphi/Object Pascal; Free Pascal in OpenDSSCmd | DSS commands; external automation interfaces | Official project distribution documentation. EPRI engine and alternative wrappers are different components | [Primary reference](https://sourceforge.net/projects/electricdss/files/OpenDSS/) |
| pandapower | Python, using numerical dependencies | Python | Project documentation and repository. Python front end can call compiled numerical libraries | [Primary reference](https://www.pandapower.org/) |
| PyPSA | Python with external numerical/optimization dependencies | Python | Project documentation. Optimization solver is a separately selected dependency | [Primary reference](https://pypsa.org/) |
| OpenModelica | MetaModelica compiler architecture; generated C/C++ runtime paths | Modelica; scripting/interfaces | Official compiler documentation. Compiler, runtime and model-library licenses differ | [Primary reference](https://openmodelica.org/doc/OpenModelicaUsersGuide/1.26/compiler.html) |
| EPANET | C engine | Network input files; C toolkit and wrappers | Official source repository. Engine implementation does not identify every GUI or fork | [Primary reference](https://github.com/USEPA/epanet-engine) |
| EPA SWMM | C engine | SWMM model files; APIs/wrappers | Official source repository. Separate GUI and community forks need separate checks | [Primary reference](https://github.com/USEPA/Stormwater-Management-Model) |
| Project Chrono | C++ | C++; Python bindings | Official implementation statement. Bindings and optional modules introduce dependencies | [Primary reference](https://www.projectchrono.org/) |
| GHDL | Ada and C | VHDL | Official repository and build documentation. HDL being simulated is distinct from simulator language | [Primary reference](https://github.com/ghdl/ghdl) |
| SimPy | Python | Python | Official documentation. Process/event model, not a continuous physics solver | [Primary reference](https://simpy.readthedocs.io/) |
| GNU Octave | Public compiled implementation; detailed mix not audited here | Octave language; native extensions | Official source and extension documentation. C/C++/Fortran extension support alone is not a source inventory | [Primary reference](https://octave.org/about) |
| ngspice | Public SPICE implementation; full language mix not audited here | SPICE netlists and control language; C shared-library interface | Official developer/interface documentation. Source availability is stronger evidence than a guessed commercial lineage | [Primary reference](https://ngspice.sourceforge.io/faq.html) |
| EnergyPlus | Public source; native simulation engine | Input models; C/Python APIs | Official project repository. API language alone does not prove complete source mix | [Primary reference](https://github.com/NatLabRockies/EnergyPlus) |
| RoboDK | Closed engine; implementation unknown in this study | Python and other API clients; robot-specific output | Documented API only. Python API does not establish a Python implementation | [Primary reference](https://robodk.com/doc/en/RoboDK-API.html) |
| TIA Portal / Studio 5000 / PLC IDE family | Unknown; native compiler/runtime with desktop or web UI is plausible | IEC 61131 languages; vendor-specific features | Architecture hypothesis only. Do not treat ladder/ST as the IDE implementation language | [Primary reference](https://www.siemens.com/en-gb/products/tia-portal/step7/) |
| Commercial CAD family | Hypothesis: native C++ geometry; UI stack varies | Product-specific scripting and APIs | Architecture hypothesis only. Kernel lineage and API languages need product-specific verification | [Primary reference](https://www.ptc.com/en/products/creo) |
| Commercial FEA/CFD family | Hypothesis: C/C++ and/or Fortran numerical kernels; mixed UI | Product-specific scripting, UDFs and input decks | Architecture hypothesis only. No product-by-product source access was obtained | [Primary reference](https://www.ansys.com/products) |
| Commercial EDA family | Hypothesis: C/C++ performance-sensitive engines; mixed scripting/UI | HDLs, SPICE, Tcl or vendor DSLs depending on tool | Architecture hypothesis only. Different stages in a suite are separate programs | [Primary reference](https://www.cadence.com/en_US/home/tools.html) |
| Wireshark | C | Lua dissectors; C plugins | Public repository language; recheck at chosen release. Capture library (libpcap/Npcap) is a separate component | [Primary reference](https://gitlab.com/wireshark/wireshark) |
| Zabbix | C server; PHP frontend; Go agent 2 | Templates; JavaScript preprocessing | Public repository language; recheck at chosen release. Components use different languages; AGPL since version 7 | [Primary reference](https://github.com/zabbix/zabbix) |
| Prometheus | Go | PromQL; exporters in any language | Public repository language; recheck at chosen release. Grafana is a separate AGPL project | [Primary reference](https://github.com/prometheus/prometheus) |
| NetBox | Python (Django) | Python scripts; REST and GraphQL | Public repository language; recheck at chosen release. Hosted editions add commercial components | [Primary reference](https://github.com/netbox-community/netbox) |
| Ansible | Python | YAML playbooks; Jinja2; Python modules | Public repository language; recheck at chosen release. Collections are separately maintained and licensed | [Primary reference](https://github.com/ansible/ansible) |
| Batfish | Java | Python client | Public repository language; recheck at chosen release. Parser coverage differs by vendor | [Primary reference](https://github.com/batfish/batfish) |
| Suricata | C and Rust | Suricata rules; Lua | Public repository language; recheck at chosen release. Rule sets have their own licenses | [Primary reference](https://github.com/OISF/suricata) |
| Zeek | C++ | Zeek scripting language; Spicy | Public repository language; recheck at chosen release. Script packages are separate projects | [Primary reference](https://github.com/zeek/zeek) |
| Nmap | C and C++ | Lua (NSE) | Public repository language; recheck at chosen release. Nmap Public Source License restricts proprietary redistribution | [Primary reference](https://github.com/nmap/nmap) |
| Metasploit Framework | Ruby | Ruby modules | Public repository language; recheck at chosen release. Metasploit Pro is a separate commercial product | [Primary reference](https://github.com/rapid7/metasploit-framework) |
| OpenVox | Ruby; Clojure server | Puppet language | Public repository language; recheck at chosen release. Community fork; Perforce Puppet is now a separate closed fork | [Primary reference](https://github.com/OpenVoxProject/openvox) |
| Proxmox VE | Perl and Rust; JavaScript web UI | REST API; CLI | Public repository language; recheck at chosen release. Bundles KVM, QEMU, LXC and Ceph with their own licenses | [Primary reference](https://git.proxmox.com/) |
| Kubernetes | Go | YAML manifests; Go operators | Public repository language; recheck at chosen release. Distributions add their own components | [Primary reference](https://github.com/kubernetes/kubernetes) |
| OpenTofu | Go | HCL | Public repository language; recheck at chosen release. Providers are separate plugins with separate licenses | [Primary reference](https://github.com/opentofu/opentofu) |
| PostgreSQL | C | SQL; PL/pgSQL; C extensions | Public repository language; recheck at chosen release. Extensions such as TimescaleDB carry their own licenses | [Primary reference](https://github.com/postgres/postgres) |
| InfluxDB 3 | Rust | SQL; InfluxQL | Public repository language; recheck at chosen release. Earlier major versions used Go | [Primary reference](https://github.com/influxdata/influxdb) |
| GLPI | PHP | PHP plugins; REST API | Public repository language; recheck at chosen release. Plugins are separately maintained | [Primary reference](https://github.com/glpi-project/glpi) |
| Commercial IT platform family | Unknown; closed products | Vendor query languages (SPL, KQL, XQL) and REST APIs | Architecture hypothesis only. A query language describes the interface, not the implementation | [Primary reference](https://www.splunk.com/) |

## Research coverage and next decisions

The catalogue contains 48 fields and 480 entries. Source coverage is: 292 product/family reference; 46 vendor-level reference; 30 candidate: direct verification pending; 112 known product: source check pending. The last label is new and applies only to the IT branch: well-established products named from analyst knowledge whose official pages were linked but not retrieved in this pass. These are coverage labels, not a quality score, and refer to product families rather than every edition or feature. Product-level evaluation requires a narrower next pass.

For each shortlisted first build, settle five questions: Who will use it? What exact engineering decision will it support? Which model assumptions are acceptable? Which independent cases establish accuracy? Which workflow improvements justify adoption over the existing open tool?

Before committing to a dependency, inspect its exact release and license, exercise its API, run the proposed reference cases and record missing functionality. Before claiming equivalence to a commercial product, define a feature matrix and test both on the same documented inputs. That comparison has not been performed in this research.

The broad plan is one shared engineering workspace with independent domain modules. The first commitment should be one module whose calculations, assumptions and limits can be defended.
