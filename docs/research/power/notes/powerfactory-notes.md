# PowerFactory: working notes (paraphrased; source ids from powerfactory-sources.md)

## Product map [P1, P2]
Base package: load flow, short circuit, sensitivities and distribution factors, basic
MV/LV network analysis, equipment models, network representation, model management,
outage management, administration, diagrams and graphics, results and reporting, data
converters. Advanced functions (licensed add-ons): contingency analysis, quasi-dynamic
simulation, network reduction, protection, arc flash, cable analysis, power quality and
harmonics, connection request assessment, transmission tools, distribution tools,
economic analysis, probabilistic analysis, reliability and restoration, OPF, unit
commitment and dispatch, state estimation, RMS stability, EMT, motor starting, small
signal (eigenvalues), system parameter identification, scripting and automation, AI,
interfaces, extra converters, DPL/DSL/QDSL encryption.
Public documents: brochures, yearly highlights, product specification, edition and
licence documents, and about 25 technical papers. The user manual and technical
references need a registered account (not used).

## Load flow [P3]
- AC: one iterative non-decoupled Newton-Raphson for balanced and unbalanced networks,
  robust from arbitrary starts; linear DC load flow for P and angles. Coupled AC/DC incl.
  meshed DC grids.
- Controls: SVC, switched shunts, tap controllers; station controllers with Q(U),
  cos phi(P), Q(P), droop; local or remote control; user-defined controller models.
- Loads voltage dependent; detailed induction machines; temperature dependency of
  conductors.
- Active power: primary and secondary control, inertia-based distribution, distributed
  slack over loads and generators, interchange schedules.
- Limits: P and Q limits including voltage-dependent capability curves.
- Scaling of load and generation; automatic feeder load scaling (balanced or
  unbalanced) to measured feeder values.
- Results checked against continuous and short-term thermal ratings that may depend on
  ambient temperature, wind speed or irradiance; "power at risk".

## Short circuit [P4]
- Methods: IEC 60909, VDE 0102 and 0103, ANSI C37, IEEE 141, IEEE 551, G74 (incl. issue
  2), IEC 61363; DC per IEC 61660 and IEEE 946 incl. pole-to-pole.
- Complete method: superposition on an actual load flow operating point, without the
  standard's simplifications, incl. dynamic voltage support of converter-connected
  generation.
- Any single or multiple fault, incl. open conductor, single-phase interruption,
  inter-circuit faults; fault sweep along lines with custom sweep diagrams; short circuit
  inside contingency analysis (parallel).

## Equipment models [P5]
- Synchronous machine: classical, standard 2.2, 3.3 (rotor model orders), asynchronous
  starting, permanent magnet; GENQEC. Asynchronous machine: single and double cage,
  saturable single cage, doubly fed; parameter identification.
- Static generator (generic for wind, PV, fuel cell, micro-turbine, battery, storage)
  with wind power curve in load flow; PV system (output from irradiance; load flow and
  quasi-dynamic); PV panel with two DC terminals; MPPT controller.
- External grid; loads simple and complex with Q(V), Q(P); MV and LV loads driven by
  annual energy or profiles; moving train load (1-phase AC and DC).
- Lines: from electrical data or tower geometry with parameter calculation; shared
  rights of way and coupling; PI or distributed; constant, frequency-dependent modal or
  phase-domain. Cables: electrical data or single and multi-core geometry, couplings,
  same model options.
- Busbar systems: simplified or detailed; single, double, breaker-and-a-half, with or
  without tie breaker and bypass.
- Transformers: 2, 3, 4 winding, auto, booster. Step voltage regulator.
- HVDC: LCC, CCC, two-level VSC, half and full bridge MMC (CIGRE TB 604 types 3 to 7),
  pulse generator. Power electronics: PWM converter, rectifier/inverter, soft starter,
  DC-DC converter; user EMT topologies from diodes, IGBTs, thyristors, MMC valves.
- FACTS: SVC, TCSC, SSSC, STATCOM; filters single-tuned, double-tuned, high-pass.
- Series reactor and capacitor, common impedance, breaker with TRV curve and SF6 arc
  model, fault current limiter, duplex reactor; AC and DC sources, DC battery, DC
  machine, DC load, Fourier and harmonic sources, impulse current source; FFT.
- Protection: relay models built from about 30 core function blocks; relay, fuse and LV
  trip unit library. Controllers: station and secondary controllers, tap controller,
  virtual power plant, generator capability curves.
- Characteristics: time profiles and parameter characteristics (scales, vectors,
  matrices, files) for load profiles, wind and PV infeed, temperature.
- Composite models with template library; grouping by zones, areas, boundaries,
  circuits, routes, feeders, operators, owners.

## Model management [P6]
- Hierarchical object-oriented database, single or multi-user; libraries and projects.
- Time-varying network: variations made of time-stamped expansion stages (variation
  manager). Operation scenarios hold operating data (switch states, dispatch, loads)
  separately (operation scenario manager). Study cases combine grids, variations,
  scenarios and triggers (characteristic time points) with calculation settings.
- Project versions; master (base) and derived projects with merge; compare and merge
  tool; combine projects horizontally or vertically.
- Data manager with address line; network model manager (spreadsheet of equipment data
  and results); filters and groups; data model extension (custom classes and
  attributes); undo and rollback in the database; local database encryption.

## Network representation [P7]
- Radial and meshed AC and DC, 1 to 4 wires; 1-phase, 2-phase, bi-phase, 3-phase, with or
  without neutral.
- Hierarchy: sites, substations, bays, primary and secondary equipment. Substation
  layouts: single, double busbar (with or without tie), breaker-and-a-half, bypass,
  user-defined. Switching devices: breakers, fuses, disconnectors, load-break switches,
  earthing switches, neutral earthing; CT, VT, CVT, combined CT/VT. Running arrangements
  and switching rules for substation automation.

## Diagrams [P8]
- Single-line in simplified (schematic, design) or detailed (every switch, primary and
  secondary) form, convertible; overview diagrams of nodes or branches; geographic
  diagrams on GPS coordinates with map backgrounds (OpenStreetMap, Google, Esri);
  automatically drawn substation and site diagrams; grouped objects (sites, bays,
  feeders, paths, towers, controllers).
- Diagram Layout Tool draws all or part of a network automatically or guided, incl.
  feeders, CTs, VTs and relays, and expands diagrams on demand.
- Colouring modes and a background heatmap; custom and composite symbols; templates
  (substations, wind turbines, PV); layers with opacity and annotation layers; graphic
  and geographic search; navigation pane; zoom bookmarks.

## Results and reporting [P9]
- Results in diagrams with flexible labels; tables in the Network Model Manager;
  "Flexible Data" pages (user-chosen columns of input and result variables); built-in
  tabular reports per calculation; interactive plots (protection, harmonics, stability,
  transients, eigenvalues) with statistics and digital signal and fault recorder views;
  PDF output and a Report Designer for custom layouts; filterable output window; export
  to standard formats; results comparison mode.

## Sensitivities [P10]
- Voltage and branch-flow sensitivities; tap sensitivities (continuous and discrete);
  distribution factors PTDF, LODF, OTDF, PSDF, TCDF; single or multiple; with
  contingencies; modal analysis to find weak and strong network parts.

## Protection [P11]
- Manufacturer relay library usable in steady state, RMS and EMT; models synchronised with
  StationWare so settings move to and from real devices; fuses, LV breakers, reclosers;
  programmable logic; inter-relay signals for intertrip and interblock.
- Overcurrent: drag-editable TCC diagrams with auto legend; phase, negative and zero
  sequence inverse and definite time; thermal overload; cable and transformer damage and
  motor starting curves; directional with cross, self and memory polarisation and
  wattmetric; differential with harmonic blocking; over and under voltage; frequency and
  df/dt.
- Distance: mho and polygonal zones, starting units; R-X and P-Q diagrams with measured
  impedance trace; time-distance diagrams; out-of-step and power swing blocking (needs
  RMS or EMT).
- Checks: steady-state response with traceable steps, tripping times from transient or
  subtransient values, transient response, "short-circuit trace" stepping through fault
  clearance.
- Protection Graphic Assistant: short-circuit sweep diagrams showing settings and colour
  zone reach. Coordination assistant: automatic overcurrent and distance settings with
  user rules. Protection audit: automatic topology and fault-level detection, fault-type
  sweep, reports flagging coordination, tripping and clearing time problems.
- CT, VT, CVT models with saturation. Settings reports and exports.

## Arc flash [P12]
- AC: IEEE 1584-2002 and 2018, NFPA 70E-2021, DGUV 203-077, EPRI methods. DC: NFPA 70E,
  DGUV. Clearing times from protection settings; incident energy, boundary and PPE
  category on the diagram; reports; automatic labels.

## Cables [P13]
- Sizing per IEC 60364-5-52, IEC 60502-2, BS 7671, NF C15-100, NF C13-200, VDE 0298-4,
  VDE 0276-1000; recommends new line types against voltage, thermal and short-circuit
  limits; optimises cross-section or parallel count. Ampacity by IEC 60287 and
  Neher-McGrath with geometric model, laying method, surroundings, heat sources and
  neighbouring cables.

## Power quality and harmonics [P14]
- Harmonic load flow balanced and unbalanced, with contingencies; non-characteristic and
  interharmonics; sources: current and voltage, thyristor rectifiers, PWM converters,
  SVCs, non-linear loads, Norton equivalents; background distortion; frequency-dependent
  R and L.
- Indices THD, HD, HF, THF, TAD, TIF, RMS, loadings, losses; limit plots incl.
  IEC 61000-3-6 and BDEW 2008; impedance loci at the connection point; waveforms;
  transformer K-factor and loss factor (UL 1562, EN 50464-3, EN 50541-2, IEEE C57.110).
- Flicker: IEC 61400-21 (continuous and switching), flickermeter IEC 61000-4-15 on EMT or
  RMS signals and COMTRADE or CSV files.
- Frequency sweep: auto or fixed steps, balanced or unbalanced, self and mutual
  impedances in phase and sequence, automatic resonance detection, sub-synchronous risk
  via radiality factors.
- Filters: models, design parameters, sizing and verification reports; ripple control.

## Contingency analysis [P15]
- AC, DC and linearised AC methods; regional assessment; single and multiple time phases
  (controller time constants, short-term thermal ratings); fault cases generated
  automatically or manually with validity periods; dynamic contingencies created during
  the run; remedial action schemes with validity periods; switching rules; fast
  screening then AC recheck; spreadsheet reports with graphics of critical cases;
  tracing of single cases; comparison mode; multi-core.

## Quasi-dynamic simulation [P16]
- Series of load flows over a user window and step; time characteristics for loads and
  generation; time-dependent states (storage charge); planned outages, events,
  variations and expansion stages honoured over time; QDSL for user load flow and
  time-dependent equations; statistics; multi-core; optional neural-network surrogate.

## RMS stability [P17]
- Balanced and unbalanced, AC and DC; variable adaptive step (ms to minutes) with
  A-stable integration; per-model step settings; parallel regions; real-time mode;
  precise event handling; protection library active in simulation.
- Modelling: DSL (graphical block diagrams, macros, text, nonlinear continuous control,
  compiled to DLL); Modelica editor with FMU export (FMI 2 and 3); UDM framework with
  nestable composite frames and signal access; libraries of IEEE, IEC, WECC and ENTSO-E
  CIM models; imports via FMI, IEC 61400-27 DLL, IEEE/CIGRE TB 958; OPC and IEEE C37.118
  PMU streams.
- Co-simulation RMS balanced, unbalanced and EMT, implicit or explicit, with automatic
  network splitting.
- Scans: frequency, loss of synchronism, speed, voltage, fault ride-through, variable.
  FFT and Prony; Bode and Nyquist for models.

## EMT [P18]
- Multiphase AC and DC; FACTS; LCC and VSC HVDC incl. MMC; power electronics switches;
  lines and cables constant or frequency dependent; saturation and hysteresis; series
  capacitors with spark gaps; arresters; EMT wind, PV and storage models; RLC; user
  models in DSL or Modelica. Parallel partitioning; fixed or adaptive step.
- Studies: lightning, switching and temporary overvoltages, insulation coordination,
  inrush, ferroresonance, SSR, TRV, point-on-wave and stochastic switching, AC-DC faults;
  COMTRADE; FFT and Prony.

## Motor starting [P19]
- Static calculation or dynamic simulation; single or multiple starts; synchronous and
  asynchronous with controllers; starting methods reactor, autotransformer, variable
  rotor resistance, star-delta, thyristor soft starter, start at any speed; thermal
  checks of cables and transformers; automatic pass/fail check shown on the single
  line; indicators: voltage drop before, during and after, start time, loading.

## OPF [P20]
- AC OPF on full AC load flow with interior point (built in or IPOPT); DC OPF as linear
  programme (CBC, or CPLEX and Gurobi if licensed). Modules: reactive power
  optimisation (AC) and economic dispatch (cost-based, DC contingency constrained).
- Objectives: losses (total or partial), reactive reserve, generation cost, load
  shedding, post-fault remedial actions (booster taps), redispatch cost.
- Controls: generator P and Q, transformer, quad booster and shunt taps, SVS, STATCOM,
  HVDC; estimation of load scaling. Constraints: branch flows, voltages, generator
  limits, reserves, boundary flows, bay loading.

## Reliability [P21]
- Fast state enumeration for network reliability (balanced and unbalanced), IEEE 1366
  indices and per-component contributions; failure models for lines, transformers,
  busbars, breakers, stochastic multi-state generators, N-1, N-2, common mode, double
  earth faults, independent second failures, protection and breaker malfunction.
- Restoration: backbone paths between feeders; failure effect analysis with
  protection-based clearing, reconfiguration and load shedding within flow, voltage and
  earth-current limits; optimal manual switching schemes.
- Generation adequacy by Monte Carlo (LOLP, capacity credit) with outages, maintenance,
  load variation, wind. Optimal remote-controlled switch and recloser placement with
  economics. Animated restoration traces and action plans.

## Distribution tools [P22]
- Hosting capacity against thermal, voltage, protection and power quality limits; tie
  open point optimisation (losses, reliability, switching); phase balancing by
  reconnection; voltage profile optimisation (tap settings for generation and demand
  cases, MV and LV); optimal equipment placement (storage, regulators) with costs;
  optimal capacitor placement (location, type, phases, size); backbone calculation; LV
  probabilistic load flow with coincidence curves.

## Transmission tools [P23]
- PV curves (critical point, limiting contingencies), QV curves (reactive margin,
  compensation sizing), transfer capacity between regions with scaling and thermal,
  voltage and contingency limits, PTDFs, flow decomposition into loop, transit and
  import/export incl. HVDC and phase shifter induced flows.

## Scripting [P24]
- DPL (C-like, object access, C extension, encryption); Python with full data model and
  virtual environments; external C++ API for full automation; Task Automation Tool for
  parallel runs of commands and scripts; add-on module framework with custom input
  attributes and result variables.

## Converters [P25]
- Import in base package: PSS/E v27 to 35 (RAW, RAWX, SEQ, DYR), PSS/U, PSS/ADEPT, Siemens
  Sincal, UCTE-DEF, NEPLAN 5, Integral (FGH), Reticmaster, ANAREDE and ANAFAS. Export:
  UCTE on request. DGS: DIgSILENT's own two-way exchange format over ASCII, XML, CSV and
  ODBC, used for GIS and SCADA interfaces. CIM/CGMES described in a separate paper.

## State estimation [P26]
- P, Q, I, V measurements; optimisation solver (built in or IPOPT); balanced and
  unbalanced; observability and redundancy checks with options for unobservable areas;
  plausibility checks and automatic bad data removal; estimates load P and Q or
  scaling, generator P and Q, compensator Q, tap positions.

## Small signal [P27]
- All or selected eigenvalues; balanced or unbalanced incl. AC/DC and converter-based
  generation; interactive eigenvalue, mode bar and mode phasor plots; eigenvectors on
  diagrams; damping ratios and frequencies; participation factors; controllability and
  observability; impedance-based Nyquist stability for inverter connections.

## Basic MV/LV, connection requests, outages [P28 to P30]
- MV/LV: voltage profile plots along one or many feeders; feeder load scaling for radial
  and meshed feeders; automatic schematic of feeder topology; tools to change voltage
  level and phase configuration of radial feeders.
- Connection request assessment against D-A-CH-CZ, BDEW 2008, VDE-AR-N 4105, 4100, 4110:
  voltage change, flicker, unbalance, loading, short circuit, harmonics, interharmonics,
  ripple control, commutation notches, resonances; a pass or fail report.
- Outage planning: scheduled and recurring outages applied and undone quickly, linked
  corrective switching and load shedding, action recorder, Gantt charts, maps of
  affected areas.

## 2026 release, editions [P31, P32]
- 2026: impedance-based stability for inverter connections; parallel EMT with network
  partitioning; Modelica improvements; validity periods for fault cases and RAS; DC
  faults between two DC terminals (bipolar HVDC, two-terminal batteries); better
  time-distance and sweep plots; CGMES CSA profile; line coupling with cables and metal
  pipes; per-section loading of multi-section lines.
- Editions: single-user (local SQLite), multi-user (licence server, local DBs, 30-day
  floating), team (central Oracle, SQL Server or PostgreSQL with master projects,
  versions, derived projects, compare and merge, offline mode). Licences by node count
  (100, 250, 500, unlimited) and type (commercial, research, education 50 nodes, student
  50 nodes, thesis, 28-day demo without API or exports); engine licences without GUI.

## Results and reporting workflow [P34]
- Output window: progress with selectable detail, warnings and errors, load flow
  convergence, RAS triggers, simulation events; filter, search, copy.
- Diagram colouring by default flags overloads and voltage violations; thresholds
  configurable; heatmap; in contingency mode colours show the worst violation over all
  cases.
- Result boxes: configurable content and format, user-made boxes for detail or summary.
- Network Model Manager: per element class table of attributes and results, sort and
  filter, Flexible Data page with user-chosen columns, copy to Excel.
- Plots: time series (variables chosen before a run, plots arranged after), R-X,
  eigenvalue, vector, protection plots (time-distance, time-overcurrent, sweep, relay
  limits, differential, curve input).
- Tabular reports for large outputs (contingencies) with filters by case and time phase
  and colouring; protection audit and coordination reports can write computed settings
  back to devices.
- PDF reports from report commands with built-in viewer, export to Word, logos and
  headers; Report Designer; user scripts (Python, DPL) reading the results file.

## Diagram workflow [P35]
- An element may appear in several diagrams; diagrams open as tabs or tiled.
- Toolbox of symbols per class; drag, drop, configure; groupings (feeders, areas, owners)
  drawn graphically.
- Data-first workflow: create objects in the data manager (manual, script, import) and
  then draw them with the Diagram Layout Tool: k-neighbourhood expansion from a selected
  element, feeder schematics, detailed substation or terminal views, area interchange
  diagrams with arrows scaled by exchange.
- Three substation detail levels: composite node (overview), design view (bays,
  busbars, breakers, graphical busbar changeover), detailed graphic (all switches,
  relays, CTs).
- Several symbols per type plus a symbol editor. Geographic diagrams from coordinates
  over OSM, Esri, Google, Bing, IGN, WMS/WMTS or local map files.
- Colouring by voltage level, owner, grid, or results (loading, voltage) with heatmap and
  filter-based rules; switch markers for normally open points; load and generation
  circles; distance measurement; flow arrows; line width by loading.
- Block diagrams for dynamic models: composite model frames (slots and signals), DSL
  (with a macro library e.g. PID, dead band), Modelica.

## Team workflow [P36]
- Central database; master (base) model published in versions by an administrator;
  users derive their own models from a base version, storing only differences; merge
  approved derived changes into the base; pull new base versions into derived models
  with notifications; two-way and three-way compare by ID (foreign key, CIM rdf:ID) or
  hierarchy; conflict dialog; groups with rights; Active Directory login; read-only,
  read-write or full sharing; offline subscriptions synchronised at start and end;
  interface profiles per group (buttons, menus, functions, models) and script
  distribution.

## Contingency workflow [P37]
- Fault cases generated from a selection (all lines, all busbars) and stored; each holds
  short-circuit events; topology tracing finds and opens the right breakers; extra
  switching and dispatch events can be added.
- AC (balanced or unbalanced), DC or AC-linearised; parallel cores.
- Dynamic contingencies chosen from base results (for example all circuits above x %).
- Single time phase (simultaneous) or multiple phases (sequenced taps, automatic
  switching, dispatch) with graphical trace playback.
- Remedial action schemes: triggers, variable changes, nesting. Effectiveness of chosen
  generators and phase shifters on overloads.
- Time sweep over periods (e.g. each hour) using study case time to pick up profiles,
  topology changes, expansion stages and planned outages.
- Reports: loadings, voltage violations, lost load and generation, islanding; results
  file readable by scripts.

## FAQ details [P38 to P41]
- The public FAQ is organised by category (dynamic simulation, load flow, equipment
  models, quasi-dynamic, scripting) and by about 70 tags (from API and Battery to Wind
  Power). Most answers are short and point to the Technical References (registered).
- Objects are typed classes: element versus type objects (for example a load element
  references a load type "TypLod"); commands are objects too (load flow command
  "ComLdf"). Voltage dependence of loads is set in the load type as a polynomial with
  coefficients and exponents for P and Q separately; the load's P and Q are values at
  nominal voltage; the load flow command has an option to consider voltage dependency.
- Result and input variables are addressed by names (for example "b:ipat" for the
  isolated area index of a bus) and can be added as columns to Flexible Data pages.
- Losses: line total = Pi + Pj; line no-load = Ui^2 B1/2 + Uj^2 B1/2; load losses = total
  minus no-load. Transformer total = sum of terminal P; no-load = voltage times
  magnetising current; load = total minus no-load. Other elements: no-load zero. Grid and
  zone totals are sums.
- Isolated areas: groups of connected nodes with no link to the rest; each needs and gets
  its own slack; indexed per bus. Unsupplied areas: edge elements (loads, branches) with
  no source; diagrams can be coloured by isolated area.

## Further functions [P42 to P50]
- Network reduction: boundary definition tool; AC or DC load flow and short-circuit
  equivalents; load, Ward, extended Ward or REI-DIMO equivalents; region by region;
  dynamic equivalents for RMS; aggregation of nonlinear elements; switch original and
  reduced grid via variations.
- Probabilistic load flow (and OPF): unlimited random inputs with distributions
  (discrete and continuous), correlations, fitted from history; Monte Carlo and
  quasi-Monte Carlo; statistics with confidence intervals, extremes, moments; analyzer
  for worst or typical cases.
- Unit commitment and dispatch: AC, DC or both; hydro, storage, phase shifters, HVDC;
  costs incl. emissions and start-up; curtailment and shedding; ramping, minimum up and
  down times, spinning reserve; contingency-constrained with preventive and curative
  redispatch; generates optimal scenarios and time series; CPLEX or Gurobi optional.
- Economics: techno-economic NPV of expansion strategies (investment, losses,
  interruption costs, timing; best investment year); power park energy analysis by
  Weibull, time series, or probabilistic methods.
- Interfaces: API; OPC DA/UA to SCADA; IEEE C37.118 PMU stream simulation; FMI 2.0
  co-simulation with third-party RMS or EMT tools.
- General: 64-bit Windows; persistent database; multilingual UI with UTF-8; tabbed
  flexible window layout; customisable toolbars, dialogs and context menus per profile;
  categorised output window; integrated script editor and report designer; user manual
  over 1,500 pages plus technical references per model; interactive tutorial; examples
  with videos.
- Parameter identification: estimate multiple parameters from measured or simulated
  signals for load flow, quasi-dynamic, RMS and EMT models; gradient, swarm, pattern
  search and global optimisers; bounds; tune for example PSS to a target response.
- AI: neural networks trained (GPU) on generated data to approximate load flow during
  quasi-dynamic simulation.
- Academic tutorials [P42] build the Anderson and Fouad 9-bus system step by step,
  study cases for transients, modal analysis, versions and derived projects, wind
  turbine DSL models, file-driven inputs (ElmFile), MATLAB coupling.

## 2025 release [P54]
- Flexible window layout with panels in any arrangement; collapsible panels (output
  window, drawing toolbox, project overview); dark mode; per-project directory and pfdx
  archives bundling external files; filter layers in diagrams; short circuit inside
  contingency analysis; contingency restoration analysis; reliability for partially
  meshed networks; reactive power in unit commitment; Modelica hybrid models; new R-X
  plots with tolerances.
- The full function list with base versus licensed split is in the public brochure
  [P53]; our fetch tool could not download it (see gaps).

## Training syllabi (scope as the vendor teaches it) [P55, P57]
- Introductory course sequence: interface and data structure (menus, drawing tools,
  output window, data manager, users and projects); network data versus diagrams versus
  library; type versus element data; Network Model Manager; build an HV network; simple
  busbars versus detailed substations and sites with bays; load flow methods, settings,
  results, colouring, NMM analysis and PDF reports for overloads and violations; load
  flow control with **inner and outer loops**, limits, voltage and Q control, station
  controllers, automatic taps, generator Q limits; extending an MV network as a
  separate grid with templates; short circuit per IEC 60909 for thermal and mechanical
  stress of cables and busbars and breaker dimensioning; complete method, multiple
  faults, dynamic voltage support; star-point earthing concepts and single-phase faults
  in MV; grouping and connecting grids; variations and expansion stages; operation
  scenarios; study cases combining them.
- All courses: Python scripting (objects, commands, navigation, reports, result files,
  diagrams, add-on variables); grid connection of wind (full converter, DFIG) and PV in
  load flow, short circuit, harmonics and dynamics with Q capability curves; advanced
  handling (diagram customisation, load flow troubleshooting, merge and compare, DGS,
  data extensions, task automation); connection assessment and hosting capacity
  (German); harmonics (frequency-dependent models, sweeps, filters, IEC 61000, flicker);
  protection (overcurrent with fuses, breakers, directional relays, earth fault,
  distance zones with infeed and parallel lines, transformer differential, audits,
  communication schemes); time-domain basics (initial conditions, variables, events,
  scans, RMS and EMT, FFT, composite models); stability (transient, oscillatory,
  voltage, frequency); DSL; Modelica and FMI for inverter controls; EMT (temporary,
  slow-front and fast-front overvoltages, saturation and energisation, capacitor
  switching, TRV, frequency-dependent line and cable geometry, lightning); HVDC (LCC,
  MMC); arc flash; cable analysis (multi-circuit trenches, wind farm cables); contingency
  (time phases, post-fault actions, sweeps, short-term ratings, RAS); database
  administration; distribution tools; motor starting (DOL, star-delta, rotor
  resistance, autotransformer, series reactor, VSD by dynamic simulation); network
  reduction (Ward, REI, coherent generator dynamic reduction); OPF (interior point,
  LP, contingency constrained, marginal and shadow prices); PSS tuning (Bode, root
  locus); probabilistic analysis; quasi-dynamic and QDSL (P(U), custom taps, EV
  charging states); reliability (failure models, indices, vulnerability, costs);
  techno-economics (NPV, IRR, payback); transmission tools; unit commitment.

## Customisation, LV methods, planning, CIM [P58 to P61]
- User settings: light or dark mode; hide unused dialog pages and parameters; background
  colours; split the main window vertically or horizontally into tab groups holding
  diagrams, data managers and reports, across several screens; pin or collapse panels
  (output window collapsed by default); built-in and user hot keys; a personal Quick
  Access menu.
- Administrator: user groups (default "Everybody") control project sharing, licence
  modules and visible profiles; profiles configure toolbars, menus, dialog pages and
  parameters (built-in "Standard" and "Base Package"); a User-defined Tools toolbox
  exposes scripts with custom icons; new toolboxes; editable context menus; trimmed
  dialogs. Project level: WMS/WMTS maps, symbol editor, user colouring filters.
- LV analysis methods compared: worst case (all loads at maximum; very conservative;
  base package); time series (most accurate; needs profiles, long runs; quasi-dynamic);
  coincidence curves (count consumers of each type downstream of each branch, apply the
  coincidence factor for that count to their maximum power; uses sensitivities so it
  works meshed; close to time-series peaks with little data; distribution tools);
  probabilistic (distributions, histograms, overload probability); load scaling
  (distribute the measured feeder maximum by annual energy or connection capacity;
  underestimates drops at feeder ends; ignores generation).
- Planning: variations hold timed stages adding, changing or removing elements, several
  alternatives can coexist; the study case date shows the network at that moment; a
  Gantt-style variation manager; one project spans many years; operation scenarios hold
  forecasts, generation and switching; compare alternatives as separate variations with
  graphical difference of results; techno-economic comparison; planned outages per
  year checked for security.
- CIM/CGMES: IEC 61970 CIM, ENTSO-E CGMES 2.4.15 and 3.0.0; profiles EQ (equipment and
  connectivity), TP (topology), SSH (operating hypothesis: taps, injections, controls),
  SV (load flow results), SC (short circuit), DY (dynamics), DL (diagram layout), GL
  (geography); import as validate then convert, keeping original data for fixes;
  node-breaker internally, bus-branch export by automatic reduction; individual grid
  models per authority with boundaries; full and difference models; network reduction
  to anonymise; scripted engine use for day-ahead and intraday processes; extension data
  kept and processable by scripts.

## GIS, hosting capacity service, smart meters [P62 to P64]
- GIS conversion to DGS (open format, file or database, partitioned) loaded by the
  standard importer; Python import GUI picking model parts by list or map; post-import
  scripts (for example assign profiles by load type); custom validation rules;
  topology from coordinates plus object references; automatic geographic, station and
  feeder diagrams; cleaning rules for isolated customers; fill missing impedances from
  library types; trace from each transformer to open points to assign model parts.
- Indicative hosting capacity service: headless engines on servers run per node maximum
  additional P and Q (at an assumed PF) under user constraints (loading, voltage,
  protection, harmonics), globally or per element or region, balanced or unbalanced,
  standard or stochastic LV load flow, many scenarios (switching, seasons), in parallel;
  reports limiting element and violated constraint; a Windows "Connector Service"
  schedules runs (periodic or on model change) and shows results in a browser; inputs
  from CGMES, DGS or other tools; versioned models for reruns.
- Smart meters: any parameter can carry a characteristic; time characteristics by study
  time; profile characteristics by day type and season; built from tables, result
  files, CSV or text files, or databases (Oracle, PostgreSQL, SQL Server, ODBC); P and Q
  series assigned to loads; quasi-dynamic runs give time curves and min and max
  statistics; future cases by growth factors or added elements with profiles.

## Calculation conventions from the FAQ [P65 to P69]
- Loading is always current based. Transformer: per winding |I| / I_rated with
  I_rated = S_rated / (sqrt(3) Un); Un is the connected busbar nominal voltage if a
  thermal rating object is assigned, else the transformer rated voltage; overall
  loading is the maximum over windings. Line: I_rat = I_nom times a derating factor,
  I_nom from the line type (air or earth value for cables), tower conductor type or
  cable system; with a thermal rating object the MVA rating is converted per end with
  the busbar Un; reported loading is the larger of the two ends.
- Voltage regulators in load flow can be modelled as an autotransformer with discrete
  taps (integer positions, lossy), a simplified lossless autotransformer with continuous
  ratio, a two-terminal AC voltage source with voltage control, or a common impedance
  with fixed ratio (no control).
- Tap side: adding turns on the HV side lowers secondary voltage; on the LV side raises
  it (Vs = Vp Ns / Np).
- Transformer star-point grounding on the element's basic data page: internal earth
  impedance (R, X), connection to the substation neutral grounded through an
  impedance, or an external single-phase neutral terminal grounded by another element.
- The protection FAQ (27 entries) covers power swing blocking, CTs in transformer
  neutrals, interlocking schemes, fuses from manufacturer curves, UFLS schemes, LV
  breaker releases (ACB, MCCB, MCB), transfer tripping for distance protection,
  anti-islanding for converters, adding all relays to a graphic, relay result boxes.

## Product family and support policy (P70, P71; read 2026-10-15)

- 2026 SP1 (2026-03-11): the interface is localised into English, German, Spanish,
  Turkish and Chinese; the manual is in English and German. Other changes are only in
  the release notes, which are not public.
- Support window: three versions at a time (2026, 2025 and 2024 supported; 2023 ended).
  Service packs continue for each supported version.
- Products besides PowerFactory:
  - **StationWare:** central protection settings database.
  - **PFM monitoring devices:** recording, power quality, fault recording.
  - **PFM300-GCC:** continuous grid code compliance monitoring.
  - A certification test laboratory (a service).
- Quantic implication: a **protection settings database** (StationWare-like) is a
  separate product line that utilities and mines pay for. It ties naturally to our
  device library and TCC engine (`engine-protection-tcc.md`). Record it as a later
  product idea, not a WP.

## More FAQ findings (P72 to P76; read 2026-10-15)

- **Fuse curves [P72]:**
  - Users digitise the manufacturer's melting-curve image, either inside PowerFactory
    (a virtual instrument with the image as background) or with a third-party tool, and
    paste the points into the fuse type.
  - The FAQ says nothing about interpolation, tolerance bands or I²t.
  - Quantic implication: a built-in **curve digitiser** (load an image, set the log
    axes, click points, store with a source citation) is a small, valued feature. It
    also solves our manufacturer-data gap in `engine-protection-tcc.md`.
- **LV breaker releases [P73]:**
  - Modelled as a relay with a 1:1 CT and the breaker rating as the nominal current; one
    relay type is reused for many breakers.
  - Long-time, short-time and instantaneous details are only in a paid tutorial.
  - Quantic: a native LV trip-unit element (LTPU, LTD, STPU, STD, I²t, INST, GF) is
    simpler for users.
- **UFLS [P74]:** an example on the IEEE 39-bus (New England) system, with stages in an
  attached project. It confirms UFLS as a standard RMS use case (T5).
- **PV and diesel co-generation, quasi-dynamic [P75]:**
  - The diesel as slack motors at high PV, which is undesired.
  - The fix is secondary (frequency) control sharing between both units, with the diesel
    held at a 10% minimum and the PV maximum following the PV profile. This curtails PV
    automatically.
  - Run over one day and one week.
  - **This is exactly a mine-site hybrid microgrid.** Quantic's PV suite (WP-2.5) plus a
    time-series load flow with a minimum-loading constraint on gensets reproduces it.
    A strong candidate demo case for mining clients.
- **Tag cloud [P76]:** about 70 tags, including Modelica and FMI (model exchange),
  Grid-forming, Microgrid, NEC/NER (neutral earthing resistors), Cable Sizing and Cable
  Ampacity, State Estimation, Flicker, Frequency Sweep, Phase Technology and Tower. This
  confirms PowerFactory's breadth matches the matrix rows already drafted. **FMI and
  Modelica are matrix row T2 evidence.**

## Cables and motor starting in PowerFactory (P77 to P80; read 2026-10-15)

**Cables [P77, P78]:** two tools.

- **Cable Sizing:** simplified derating from the line type's electrical data, for
  planning. Two methods:
  - "International Standards": recommend or verify by the selected standard, with no
    load flow needed;
  - "Cable Reinforcement": verify or recommend from the project's own library against
    user constraints.
- **Cable Ampacity:** a detailed geometric thermal model of the cable system type
  (IEC 60287 style) giving exact ampacity.
- The FAQ does not name the standards supported.
- This matches the split in `engine-cables.md` (tabulated sizing against an IEC 60287
  calculation).

**Motor starting [P79, P80]:** an example project with:

- star-delta switching (a parameter flag);
- added rotor resistance (stepped or continuous);
- an autotransformer via the transformer tap;
- a soft starter as an external device;
- a VSD.

It runs in **RMS and EMT** dynamic simulation, selected per study case. Separate
examples cover a VSD template and a synchronous motor with asynchronous starting.
Quantic: confirms the M3 starter list in `engine-motors.md` sec. 5. Synchronous motor
asynchronous starting (relevant to large mine mills) should be added there.

## Scripting pain points (P81; read 2026-10-15)

`powfacpy` (MIT, maintained mainly by Fraunhofer IEE) exists to wrap PowerFactory's
native Python API "with improved syntax and functionality". Its stated aims:

- readability and productivity;
- avoiding known problems, errors and obscurities of the native API;
- standardising how organisations work (for example, result export formats);
- tutorials for newcomers.

When a major research institute maintains a wrapper, the native API is evidently hard to
use. Quantic implication: a clean, documented, versioned API from day one (we have JSON
contracts and REST) is an advantage worth stating, and needs keeping.

## Platform (P86; read 2026-10-15)

PowerFactory is "fully compatible with MS Windows 64-bit". No Linux or macOS support is
stated. Detailed requirements are in the Product Specification Document, which still
would not open (dossier gap 1). Like ETAP, it is Windows-bound, so a browser-based
Quantic workbench differs from both on platform reach.
