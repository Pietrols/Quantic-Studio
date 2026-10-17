# ETAP studies: working notes (paraphrased; source ids from etap-sources.md)

## Product map [E1]
ETAP sells a family organised as Design, Build, Operate, Automate, Digital transformation,
Data management. Power system analysis core: Load Flow and Voltage Drop, Panel schedules,
Short Circuit, Motor Acceleration, Harmonics, DC Load Flow, DC Short Circuit, PV array.
Related: Cable Ampacity, Cable Sizing, Cable Thermal, Transformer Sizing. Wider: Caneco
(LV design, BT, BIM), SEE Electrical (schematics, 3D panel, harness, PLM), protection and
coordination (Star), arc flash (ArcSafety, ArcFault), distribution network analysis,
dynamics and transients, grid code compliance, rail traction (eTraX), PMS, EMS, ADMS,
digital substation, eProtect (relay asset management), operator training simulator,
SCADA, load shedding (ILS), power plant controller, microgrid controller, digital twin,
intelligent single-line diagram, data exchange, NetPM (cloud project management),
mobile data collection app, sustainability analysis.

## Load flow [E2]
- Results: bus voltages, branch flows, currents, power factors, losses (P and Q), demand,
  voltage drop, generation versus loading, PF and efficiency at no-load and overload.
- Sources: swing, voltage-regulated, unregulated; multiple grids and generators;
  isolated single-phase sources.
- Controls: phase-shifting transformers; 2- and 3-winding LTC action; AVR action;
  automatic adjustment of online LTC and regulator settings; automatic temperature
  correction of conductors; combined 3-phase and 1-phase solution in one run.
- Loading: multiple loading and generation categories per element, multiple demand
  factors, global and per-bus diversity factors, several lumped-load models, unlimited
  configurations (switching states) and "what-if" studies in one database; option to
  update initial conditions from a solution.
- Solver: user convergence parameters; five levels of automatic data error checking;
  solution parameters saved per scenario; AutoRun on system change; online (real-time)
  interface. The page names no algorithm (algorithms are named on the harmonics page:
  embedded Newton-Raphson and Gauss-Seidel [E5]).
- Evaluation: automatic device evaluation, critical and marginal limit alerts, overload
  warnings for buses, transformers, cables, generators; alert summary reports.
- Output: Load Flow Result Analyzer (compare many reports and scenarios in one view);
  one-click result unit toolbar; results drawn on an interactive one-line; study case
  editor. Related: Optimal Power Flow (optimises controls within constraints), Unbalanced
  Load Flow (unsymmetrical components).
- Literature to read: load flow fact sheet and tutorial PDFs, OPF and unbalanced LF fact
  sheets, result analyzer and reporting sub-pages.

## Short circuit [E3]
- Faults: 3-phase, line-ground, line-line, line-line-ground; balanced and unbalanced.
- Standards: ANSI/IEEE C37 with UL 489, IEC 60909, IEC 61363 (transient, with device
  duty), GOST R 52735. Each has its own sub-page.
- Device duty: automatic evaluation for 3-phase, 1-phase and panel systems; worst-case
  duty; evaluation on total or maximum through-fault current; comparison with
  manufacturer ratings from device libraries; generator circuit breaker evaluation;
  global or per-device impedance tolerance for max and min currents.
- Modelling: load-terminal faults; automatic conductor resistance (temperature) and
  length adjustment; fault impedance on or off; branch shunt admittance on or off for
  unbalanced faults; phase-shifting transformers; grounding of generators, transformers,
  motors, loads; motor contribution by loading category or demand factor; faults at
  motor terminals without extra buses; wind turbine and converter models; prefault
  voltage from loading for transient studies; fault bus selection graphical or tabular.
- Output: overstressed device alarms on the one-line, critical and marginal alerts,
  alert view, reports, Short Circuit Analyzer comparing scenarios; one-line datablocks
  updated with worst case. Feeds protection coordination (Star) and arc flash.

## Motor starting [E4]
- Dynamic (motor acceleration with torque-speed models) and static (impact) methods.
- Sequence of events: start motors individually or move the whole system to another
  state; unlimited events; accelerate or stop several motors; load ramping.
- Starters: VFD (frequency control), soft starter, and others on a sub-page; capacitor
  start; compare starters.
- Network dynamics during start: regulators, substation LTCs, switched capacitors.
- Vary generator and grid parameters; transition loading of the whole system.
- Plots: speed and torque, terminal voltage and current, kW and kvar, versus time.
  Result Analyzer tabulates worst cases across starter combinations; Plot Analyzer
  compares plots with alerts; Python scripting for automated evaluation and Excel output.
- Sub-pages to read: libraries and modelling, motor starters, alerts and reporting.

## Harmonics [E5]
- Methods: harmonic load flow with embedded Newton-Raphson or Gauss-Seidel fundamental
  flow, harmonic current injection, frequency scan, parallel resonance identification.
- Models: impedance scaled to harmonic order; temperature-dependent R; skin effect for
  motors and transformers; phase shift of transformers; load cable modelling.
- Sources: expandable harmonic library (typical and user), voltage and current sources
  with magnitude and phase, by spectrum or device parameters, interharmonics, VFD, UPS
  input and output, PV inverter, wind type 4.
- Filters: single-tuned, high-pass, band-pass; sizing and tuning; performance check.
- Compliance: rule book for V and I distortion at global, local and individual points;
  TDD and TRD limits; percentile multipliers; automatic alerts.
- Standards: IEEE 519 (1992, 2014, 2022), IEEE 399, IEEE 141, IEC 61000-3-14,
  IEC 61000-3-6, IEEE 3002.8, IEEE 1547-2018, IEEE 2800-2022, IEEE 1531-2020.
- Indices: THD, IHD (V and I), TIF, I*T, RMS, arithmetic sum, IEEE 519 indices.
- Equipment: transformer K-factor; transformer and cable derating alerts; cable sizing
  linked to harmonic results; telephone interference.
- Output: one-line display, spectrum and waveform plots, order display, text reports with
  violation flags, Crystal Reports, export of one-lines to CAD, Plot Analyzer.

## Load flow, more detail [E6, E7]
- Methods named: Newton-Raphson, fast decoupled, accelerated Gauss-Seidel, with user
  convergence settings (maximum iterations, precision) [E7, E6]. Transient stability
  page adds "conventional and adaptive" Newton-Raphson for its initial flow [E16].
- Workflow [E6]: a Mode toolbar switches the one-line between study modes (edit, load
  flow, short circuit ...); a Study Case toolbar picks the case and the output report
  name (overwrite or prompt); Run; results on the one-line with Display Options; Alert
  View; Report Manager (several formats); edits such as enabling Auto LTC on a
  transformer winding with a regulated bus, then rerun; Result Analyzer to filter and
  compare. Load flow solves every sub-network (islands) in one run.
- Study case content [E6]: method, iterations, precision; loading and generation
  categories; diversity factors; per-element-type adjustments (transformers, reactors,
  overload heaters, cables, lines: tolerances and temperature); alert criteria.
- Element models [E7]: bus, branch and cable, 2- and 3-winding transformer, phase
  shifter, LTC and regulator, generator with governor (isochronous or droop) and exciter
  (AVR, or Mvar or PF control), loads incl. lumped and DC loads, swing / regulated /
  unregulated sources, panels, UPS, single-phase elements. Radial and loop networks.
  Simultaneous solution of 3-phase, 1-phase, panel and UPS systems. Load forecasting.
  Demand factors per continuous, intermittent and spare operation.
- Result Analyzer [E7]: compare reports, also across projects; baseline report with
  deviation flags; locate element on the one-line from the table; export to Excel.
- Graphical output [E7]: voltage drop, load terminal voltage, branch losses, LTC
  settings, device evaluation, marginal and critical buses; one-line export to CAD.
- Reports [E7]: Crystal Reports customisable, any language; input data, detailed and
  summary reports; export to word processors.

## Optimal power flow [E8]
- Objectives: minimise P and Q losses, fuel cost, energy cost, load shedding, heat rate;
  optimise exchange with grid or IPPs; maximise voltage and flow security indices;
  multi-objective.
- Controls: generator MW and Mvar setpoints, transformer taps, capacitor sizes, each
  within limits. Constraints: equipment and operating limits, interface flow limits, bus
  and branch constraints with weighting factors.
- Method: interior point with logarithmic barrier functions on a full AC flow; user
  controlled infeasibility handling. Output: optimal settings and the changes made.

## Unbalanced load flow [E9]
- Current-injection method; phase and sequence V and I; unbalance factors; losses.
- Automatic line constant calculation; mutual coupling within and between lines.
- Phase configurations: 1-phase, 2-phase (2 and 3 wire), 3-phase (3 and 4 wire).
- Loads constant P, constant Z, constant I, or generic function of V and f. Machine
  sequence impedances, grounding impedances, transformer winding connections.
- Alerts on voltage and current unbalance. Scale: 10,000+ buses, licence-limited.

## Short circuit by standard [E10, E11, E12]
- ANSI/IEEE [E10]: equivalent voltage source at the fault; three networks for three time
  frames: 1/2 cycle (subtransient, momentary), 1.5 to 4 cycle (transient, interrupting),
  30 cycle (steady state). Separate R and X networks for X/R at each fault; X/R gives
  the multiplying factor for DC offset; no-AC-decay (NACD) ratio. Duties: momentary for
  breakers and buses, interrupting (depends on contact parting time), closing and
  latching, symmetrical versus total rated breakers, LV breaker interrupting at maximum
  voltage, generator breakers for system-side and generator-side faults. Standards
  named: IEEE C37.04, C37.010, C37.13, C37.013, C37.20.1, IEEE 399, 141, 242, UL 489.
- IEC 60909 [E11]: edition 2.0 (2016); Ib, Ik, idc, with Ib for meshed networks from each
  machine's contribution; ip method A, B or C selectable; user c factor; max and min;
  near and far from generator; KT, KG, KSO corrections; impedance tolerance plus or
  minus; device duty incl. 1-pole and 2-pole for 1-phase panel and UPS; LV breaker
  service or ultimate capacity; IEC 62271-100, -200, -203, 60947-1, -2, 60282-2, 60781;
  wind (asynchronous, DFIG, full converter) and PV (full converter) contributions;
  contribution reports for unbalanced faults.
- IEC 61363 [E12] (ships and offshore): time-domain decay curves of idc, AC RMS and ip;
  prefault loading from a load flow; user c factor; relay-test-set compatible plots.

## Arc flash [E13, E14]
- Standards: IEEE 1584-2018 (and a 2002 calculator), NFPA 70E, OSHA 1910.269 and NESC
  (HV), DGUV-I 203-077, ENA NENS 09-2014; DC methods maximum power, Stokes and
  Oppenlander, Paukert.
- AC: 1-phase, 3-phase, UPS; enclosed and open air; enclosure editor with box
  templates; typical or user working distance; shock approach boundaries.
- Clearing time: automatic, time-varying with current decay; source protective device
  found automatically or user set; relay functions 49, 50, 51, 67, 79, 87 modelled;
  current-limiting fuses. Generator AC decrement and motor decay included; individual
  arcing current contributions; radial and multi-source systems.
- Mitigation modelled: differential relays, maintenance mode switch, arc light and
  pressure sensors, ZSI, current-limiting fuses, HRG, high-speed grounding switch, arc
  quenching, line-side isolation.
- Outputs: incident energy at buses and load terminals; boundaries (arc flash, limited,
  restricted); constant incident energy curves on TCCs; PPE editor and alerts on
  insufficient arc rating; labels (many languages, QR codes, two-energy labels); work
  permits and data sheets; Result Analyzer; calculator without a one-line; capacitor
  hazard evaluation (NFPA 70E art. 360). HV ArcFault module 1 kV to 800 kV incl. arc in
  a box 15 to 36 kV. DC arc flash incl. transient for battery storage.

## Protection and coordination, Star [E15]
- Auto-Evaluation of protection and coordination; StarZ distance relay coordination for
  T and D; energy and current-limiting curves (MCCB, fuse, cable); ZSI evaluation;
  sequence of operation; zone and path detection; short-circuit and incident energy
  curves on TCC; time-overcurrent selectivity; settings reports with filter and export;
  device libraries from manufacturer data (video cites about 100,000 models); design
  assessment for missing data and disabled functions; user-defined device fields.
- Sub-pages listed for later reading (Star auto-evaluation, StarZ, sequence of operation,
  libraries, settings report, design assessment).

## Dynamics and transients [E16, E17]
- Transient stability: critical clearing and separation times, rotor angle stability,
  motor acceleration and reacceleration, load shedding (optimised or relay based), fast
  bus transfer, relay setting checks, microgrid grid-connected, islanded and transition,
  loss of excitation, generator start and frequency response, synchronisation checks,
  LVRT and HVRT, MOV starting, frequency relays with voltage blocking.
- Models: synchronous and induction machines (frequency dependent), exciters,
  governors, PSS, SVC, HVDC, VSC and inverters, renewables and storage, V, I, f, P and
  sync-check relays.
- Events: faults on bus, branch or branch segment with impedance, device open and close,
  generator setpoint, mode, field faults, start; grid sags, swells, frequency changes;
  motor events; wind gusts and ramps; load steps and ramps; VFD frequency; inverter
  charge and discharge. Settings: total time, time step.
- Output: live plots on the one-line, plot view, plot analyzer.
- Package modules: transient stability, user-defined dynamic models (block diagrams),
  eMT (electromagnetic transients program), eMTCoSim (phasor and EMT co-simulation),
  transformer inrush, dynamic parameter estimation and tuning, motor parameter
  estimation, generator start-up (black start); related ILS and wind turbine generator.

## Cables, transformers, DC [E18 to E21]
- Cable sizing criteria: load current, voltage drop, minimum voltage at motor start,
  short-circuit withstand, protective device, harmonics, minimum conductors per phase,
  let-through energy; requirements typed in or taken from load flow, short-circuit and
  protection results. Standards: IEEE 399, NEC, ICEA P-54-440 (tray), IEC 60502,
  IEC 60364-5-52 and -4-41, IEC 60092 (ships), BS 7671, NF C15-100, NF C13-200,
  AS/NZS 3008 (and 3000 shock protection). Grid view with sort, filter, batch update and
  batch selection from library; optimal and alternative sizes; reports.
- Related: electric shock protection (earthing systems, touch voltage), PE conductor
  sizing, underground cable thermal analysis (Neher-McGrath and IEC 60287 per [E22]),
  cable pulling (3D tension and sidewall pressure [E22]).
- Transformer sizing: ANSI/IEEE C57.12, C57.92, C57.96, IEC 60076, IEC 60726; sized from
  connected or operating load with growth and load factors, ambient and altitude,
  cooling stages, dry or liquid; impedance and BIL checks against standard minimums.
  Tap optimisation (optimal turns ratio for reactive output) per [E22].
- DC load flow: Newton-Raphson; batteries (take load on low voltage), chargers and UPS
  (mode switching, current limit), DC converters, DC motors (voltage-dependent model);
  integrated AC and DC; IEEE 946; checks against bus limits, ampacity, source capacity.
  Battery sizing and discharge with duty cycles and DC short circuit are separate modules
  [E22] (pages not yet read).

## Whole catalogue [E22]
Core analysis groups and modules, as ETAP structures them:
- System modelling and visualisation: intelligent one-line, geospatial view, feeder and
  substation diagrams, multi-dimensional digital twin, etapPy Python scripting.
- Power flow: load flow, DC load flow, unbalanced load flow, quasi-dynamic unified load
  flow (AC and DC together with time-varying loads).
- Short circuit: ANSI/IEEE, distribution short circuit (unbalanced, over time), fault
  management and service restoration, IEC 60909, IEC 61363, GOST R 52735 and R 28249, DC.
- Protection (Star): TOC coordination and selectivity, sequence of operation, automated
  coordination with zone detection and miscoordination checks, library and settings
  report. StarZ: distance, differential and other relay characteristics, unified
  protection and dynamic stability incl. out-of-step, line loadability, settings import
  incl. IEC 61850, as-found versus as-designed change tracking. eProtect asset database.
- Arc flash: AC, DC, auto-evaluation, result analyzer, HV (OSHA, NESC), calculators,
  ArcFault.
- Renewables: wind turbine generator, PV array, microgrid controller (software in the
  loop), battery sizing and discharge, energy storage (charging, arbitrage).
- Network analysis: load allocation (technical and non-technical losses), motor
  acceleration, voltage stability (P-V and Q-V), grid code compliance (impedance locus,
  ride-through), harmonics, reliability (customer and energy indices), contingency
  analysis (N-1, N-2 ranking and screening).
- Dynamics: transient stability, eMT (switching, surges, insulation coordination),
  eMTCoSim, generator start-up, parameter estimation (NERC MOD-026, MOD-027), machine
  parameter estimation, UDM, built-in and DLL models.
- Optimisation: OPF, volt/var optimisation (conservation voltage reduction), switching
  optimisation (feeder balancing, loss reduction), optimal capacitor placement.
- Grounding: ground grid (step and touch), finite element for irregular grids, soil
  resistivity calculator, conductor and rod optimisation (IEEE 80, IEEE 665).
- Lines and HVDC: overhead line impedance and coupling, sag and tension, line ampacity
  (IEEE 738), HVDC incl. VSC.
- Cables: thermal, shock protection, PE sizing, ampacity and sizing, pulling.
- Transformers and control: inrush incl. sympathetic, sizing, tap optimisation, control
  schematics (AC and DC control circuit simulation).
- Data exchange: Revit, Excel, universal mapping, MultiSpeak, CIM; legacy import incl.
  AVEVA and SmartPlant; etapPy batch automation.
- Rail: eTraX (AC and DC traction, train performance, track modelling, scheduling).
- Operations: real-time, eSCADA (IEC 61850, IEC 60870-5, Modbus, DNP3, OPC UA),
  predictive simulation, event playback, operator training simulator, GMS (AGC, unit
  commitment, economic dispatch), ADMS (state estimation, FLISR, VVO, OMS), load
  shedding (iLS, iDLS), microgrid controller, power plant controller, substation
  automation, field hardware (iCE).
- Data management: etapAPP field collection (geo-tags, photos, sync), NetPM multi-user
  change control and approvals.
- Commercial sector extras: panel board schedules, UPS design, redundancy adequacy,
  FMEA, rule-based design, Revit and BIM interface.

## Motor models and starters [E23, E24]
- Induction rotor models: single cage, single cage with deep bar, double cage with
  dependent circuit, double cage with independent circuit; a characteristic model from
  performance curves. Synchronous motor dynamic models. Torque-slip curves.
- Load torque models: polynomial and characteristic (curve) types; libraries for
  nameplate data, equivalent circuits, torque-speed data, curve and equation loads.
- LTC time delays global or per device; transformer phase shift.
- Conventional starters: autotransformer, stator resistor, stator reactor, bus-side
  capacitor, terminal-side capacitor, rotor resistor, rotor reactor, star-delta, partial
  winding.
- Soft starter control modes: current limit, current control, voltage control, torque
  control.
- VFD: between motor and bus or through transformers and cables (long subsea feeds);
  multiple input transformers for 12, 18, 24 pulse; ten steady-state frequency settings
  with user V/Hz; input PF rated, load PF or user value; starting by frequency control
  (frequency and V/Hz versus time, constant torque or constant power) or torque control
  with a current limit; low-frequency voltage boost; dynamic rectifier, DC link and
  inverter model with V and f control.

## Modelling platform [E25, E26]
- One multi-dimensional project database holding graphical views (presentations),
  status configurations (switching states), base and revision data with merging,
  operating parameters; project wizards; rule-based data entry; client-server with user
  permissions; Python scripting.
- One-line editor: 1-, 2- and 3-phase AC and DC; unlimited buses; instrumentation and
  grounding components; templates; automatic connection; nesting (composite networks);
  synchronised GIS and one-line views; logical feeder layouts generated from GIS;
  bus-breaker substation detail; unlimited switching topologies.
- SCADA and web views, etapAPP and NetPM (see catalogue).
- 2026 additions: 3D network view of data and results; Network Manager (matrix view for
  bulk editing and troubleshooting); editing inside revisions and revision comparison;
  AI copilot with natural language queries and edits; AI auto-complete of one-line
  connections; feeder hosting capacity with protection, harmonic and short-circuit
  limits; VVO with CO2 tracking; interconnection studies with network reduction and
  aggregation; transmission thermal limits (IEEE 738, IEEE 605, IEEE C57.91, FERC 881);
  time-series load flow; flicker; transformer loading capability; unbalanced transient
  stability; inverter-based resource EMT-like behaviour; frequency response estimation;
  MotorPro (motor parameters from manufacturer data); fault isolation verification in
  meshed networks; TCC original and shifted curves with breaker delays, fuse preloading
  and shift factors; multi-stage short circuit and coordination; StarZ stepped events;
  NFPA 70B maintenance tracking and risk-based maintenance; DataX for GIS, BIM, CAD;
  etapPy REST API that can create one-lines; imports from SKM V11, Revit, AutoCAD, CIM17,
  ESRI, CanecoBT, ERACS; Excel exchange with universal mapping; FLISR; switching
  sequence generation.
- Library scale stated: 23,000+ models, 17,500+ new protective devices, 5,000+ PV array
  models, 900+ new cable types and sizes.

## Libraries [E27]
- Equipment: cables (with fire coating, stopping and wrapping options), overhead lines
  and ground wires, wind turbines, PV arrays, distribution transformers, motors
  (nameplate, circuit, characteristic and load models), VSDs (harmonic behaviour),
  system data (sector profiles, interruption costs, reliability data, rolling stock),
  batteries (lead-acid, lithium-ion), control devices (contacts, relays, solenoids).
- Protective devices: fuses; relays (overcurrent incl. overload, directional,
  voltage-controlled and voltage-restrained, differential with extra CT inputs,
  distance); reclosers (hydraulic, electronic); MV and HV breakers incl. generator
  breakers; LV breakers with slash ratings, per-pole ratings, ZSI flag, energy and
  current-limiting curves; trip units (solid state, thermal-magnetic,
  electromagnetic); motor circuit protectors and overload heaters; GFI and RCD.
- Equipment warehouse: a project-linked filtered subset of the master libraries.
- Management: add, copy, delete, smart merge, separate project library file, change
  tracking. Each release verified against manufacturer data.

## Protection automation [E28, E29, E30]
- Auto-Evaluation: rule book (default from standards and practice, customisable) for
  equipment protection and selectivity; finds zones and paths, fault locations and
  through-fault currents automatically; user picks fault type; checks cable protection
  by comparing cable energy withstand with breaker let-through, cable overload and
  voltage drop, ZSI; colour-coded violations with an interactive viewer to edit and
  re-evaluate; reports with snapshots.
- Sequence of operation: drag a fault onto the one-line; 3-phase, LL, SLG, DLG; max or
  min steady-state current per ANSI or IEC; each device time from its settings, curve and
  interlocks; functions 27, 49, 50, 51, 51V, 59, 67, 79, 87; simulate a device failing
  to see backup clearing; option to ignore maintenance switch; event table linked
  both ways to the one-line, with autorun and slider playback; devices animate on the
  one-line; normalised (shifted) TCC that scales each curve by its through current and
  voltage so selectivity can be compared directly.
- StarZ: realistic distance relay models (polarisation, dynamic mho expansion),
  distance, overcurrent, directional, differential, load encroachment; R-X plots in
  primary or secondary units with transformer scaling; time-distance plots; inter-relay
  communication and interlocks, local and remote backup, breaker failure; CT, VT,
  breaker and switch modelled graphically with faults placed between them to find blind
  spots; analog and digital I/O simulation; settings export to XML and Excel.

## Reliability [E31]
- Indices: customer (SAIFI, SAIDI, CAIDI, ASAI, ASUI, ASIFI, ASIDI, MAIFI, MAIDI, CTAIDI,
  ALII, ACCI, CEMI, CELID, TIEPE, NIEPE), energy and cost (EENS, ECOST, IEAR), system
  (average failure rate, outage duration, annual unavailability U), per load point, bus,
  feeder or system.
- Method: radial and looped; single and double contingencies; fault isolation and
  restoration through switching devices; maximum load transfer and critical elements;
  optional load flow constraints (capacity, voltage drop, minimum voltage), incl.
  unbalanced. Data: IEEE 493-2007 and IEEE 3006.8 based library; customer damage
  function interruption costs; EENS and ECOST sensitivity and ranking of contributors.

## Ground grid [E32]
- IEEE 80 and 81 uniform-grid method; IEEE 665; FEM for irregular grids with 3D rod and
  conductor placement; two-layer soil fitted from Wenner measurements plus a surface
  layer; tolerable step and touch per IEEE 80 (body weight and temperature options) and
  EN 50522 (body, glove, footwear impedance); surface potential tables; layout
  optimisation for safety and cost; conductor current check against fault current;
  3D and contour plots of surface, step and touch voltage; reports.

## Contingency analysis [E33]
- User-defined outage lists; N-1 and N-2; fast screening and ranking with performance
  indices on bus voltage, branch overload and changes in P and Q flow; detailed AC runs
  for the ranked cases; outputs: comparisons against base case, lost generation, lost
  load, customers interrupted, cost of lost power.

## eMT and UDM [E38, E39]
- eMT runs on the PSCAD EMTDC engine (as the page states); wideband line and cable
  models; machines, shunt compensation, STATCOM, power electronics, HVDC, FACTS.
  Studies: deterministic and statistical switching, single-pole switching and fast
  reclosing, capacitor switching, fault clearing, TRV, insulation coordination, lightning
  (backflash, induced, incoming surges, arresters), ferroresonance, inrush, shaft
  torsional stress and SSR, current chopping, delayed current zero. Parallel runs on
  8 to 64 cores; editions limited by node count (200 or unlimited).
- UDM: graphical block-diagram editor with transfer-function blocks and ports; compiler
  with initialisation; built-in load acceptance, rejection and fault tests; library of
  AVR, PSS, exciter, turbine, governor, shunt device, dynamic load, wind, PV, storage,
  fuel cell models; Norton or Thevenin interface for inverters; vendor DLL black boxes.

## Panels, batteries, DC short circuit [E40 to E43]
- Panel schedules: graphical panels and boards with unlimited branch circuits and
  sub-panels; upstream totals update; NEC demand factors and user factors with editable
  load-code tables; continuous and non-continuous loads; 3-phase 4-wire, 3-wire, 1-phase
  2-wire and 3-wire; Revit load code mapping; panel schedule reports.
- Battery sizing: IEEE 308, 485, 946; duty cycle from individual loads in 1-minute
  steps, random and non-random loads, diversity; duty cycle summation or load flow
  method with losses and drops; temperature, aging, initial capacity and design margin
  factors; selectable curve interpolation; result: strings, cells per string, cell size,
  checked by discharge simulation; IEEE 485 format report.
- Battery discharge: DC load flow or summation method; random load added at the lowest
  terminal voltage; Class 1E DC models; control system driven by battery voltage;
  capacity, voltage, current and power plots.
- DC short circuit: IEEE 946 basis; total and per-source contributions, rise time and
  decay; bus and branch contributions; device rating checks.

## Intelligent one-line [E44]
- Themes (unlimited) colouring by phase, voltage, area, feeder, grounding, earthing system
  (TT, TN, IT); display layers; nested composite views.
- Rule-based auto-build of diagrams with automatic spacing and alignment.
- Orthogonal or diagonal connectors; continuity shading of de-energised parts; topology
  processing updates the drawing after switching; tracing source to load and point to
  point; split buses; remote connections.
- Symbol sets, custom symbols and shared templates.
- Datablocks: templates applied by device type, showing input data and results of several
  studies; contouring of voltage or flow; embedded live plots overlaid on earlier
  results; result precision and visibility adapt to zoom level.

## Second pass: reports, alerts and packages [E51 to E62]
- Load flow reports: input data, detailed and summary; voltage drop, losses, flows, PF,
  branch losses and loading; alert view filterable by area, zone or region; multi-report
  analyzer with a reference report, side-by-side results, cross-project comparison,
  jump to element, Excel export.
- Short-circuit reports: load terminal fault currents; per-source contributions
  (symmetrical, asymmetrical, zero sequence); totals and summary; phase and sequence
  voltage and current profiles; phase and sequence impedance reports; alert view.
- Motor starting alerts: motor fails to start; low voltage at starting motors and MOVs;
  low bus voltage with thresholds by bus type and voltage level; generator and prime
  mover overload; user marginal and critical limits; sort by area, zone, region. Plots
  for motors, MOVs, static loads, capacitors, generators and buses (voltage, torque,
  power, slip, current), combinable, with line, bar, 3D, scatter.
- ArcFault: 15 kV and above (applicable 1 to 800 kV); custom equations; internal short
  circuit and device times; working and minimum approach distance; altitude and
  transient overvoltage adjustment; arc-in-a-box; current-limiting fuses; time-varying
  clearing and decay; OSHA 1910.269 App. E, NESC C2 2012 to 2023, extended IEEE
  1584-2002.
- DC arc flash: maximum power, Stokes and Oppenlander, Paukert, DGUV-I 203-077 worst case
  and iterative, transient DCAF per IEC 61660; BESS with SOC-based short-circuit model;
  PV with IV curves and irradiance; UPS, DC motors, converters, chargers with user
  short-circuit curves; mis-operation detection; NFPA 70E 2024 labels.
- Distribution package: unbalanced load flow, time-series unified power flow (AC and DC),
  load allocation from metering (technical and non-technical losses), unbalanced short
  circuit incl. simultaneous faults, FLISR, arc flash, motor acceleration, reliability,
  quasi-dynamic add-on. Optimisation package: OPF, switching optimisation (tie points),
  optimal capacitor placement (installation and operating cost), VVO coordinating taps,
  regulators, capacitors and inverters.
- Grid code: rulebooks (built in and user); ride-through, P and Q control, dynamic
  support, P-Q capability, harmonics and resonance at the point of measurement and per
  inverter; submission-ready Excel tables.
- Base package: digital twin platform (presentations, configurations, revisions,
  wizards); network editor (1-phase, 3-phase, DC, grounding, templates, tracing, GIS
  sync); element library; smart data entry and multi-level error checks; auto-build,
  data blocks, calculators, rulebooks, switching interlock checks; data, theme, plot and
  report managers; cable ampacity, sizing and impedance; cable manager; schedules;
  Python; Gantt project tracking; DXF export; DataHub packaging; 140,000+ library models
  and sizes; multilingual editions.
- PV array: any number of panels in series and parallel; 17,000+ panel models from the
  California Energy Commission list; I-V and P-V from datasheet values fitted with one-
  or two-diode models; sun-position irradiance from date, time and location; time-series
  output; temperature coefficients; built-in inverter with MPPT and user dynamic
  logic; solar farm design incl. collectors, combiners and grounding; hosting capacity.

## Tutorials: motor starting and short circuit [E63 to E65]
- Motor starting study case, Event page: total simulation time (example 10 s); any number
  of events, each with actions of three kinds: action by load (start or stop one load),
  action by starting category (start or stop a group of motors), load transitioning
  (move loads from one loading category to another, also used for fast bus transfer).
  Unlimited actions per event and events per run; start, stop and restart in one run.
- Static start needs per motor only the no-load and full-load acceleration times (Load
  Model page) [E63]; dynamic start needs a dynamic model category (with Typical Data
  from nameplate), a load model from the library, and inertia H (WR2 updates
  automatically). Separate run buttons for static and dynamic starting; a plot
  selection window afterwards.
- Plot types [E65]: slip and speed, terminal and bus voltage, torque, electrical and
  mechanical power, terminal and line current, generator or grid current, power and PF,
  frequency, V/Hz; for motors, MOVs, static loads, capacitors, generators, buses; time
  slider.
- Pre-start conditions from different loading categories; group starts globally or bus
  by bus; soft starters and VFDs for starting and running; MOV five stages; Study Wizard
  runs presets in one click.
- Short-circuit study case [E64]: Info page puts buses in "Fault" or "Don't Fault" groups
  (also by right-click on the one-line; faulted bus drawn dark red); Standard page sets
  ANSI (default) or IEC; Alert page with a marginal checkbox and limit (example 70 %) and
  auto display of the alert view. Five ANSI studies and three IEC studies available as
  separate run buttons (for example "3-phase device duty"). Overstressed breakers drawn
  in magenta. Alerts: critical at 100 % of rating or more (always), marginal above the
  user limit and below 100 %.

## Tutorial: arc flash [E66]
- Quick calculator per bus: bus Rating page sets equipment type (enclosed such as MCC or
  switchgear, or open air); Typical Data loads typical gap, X factor and NFPA 70E
  approach boundaries; Arc Flash page holds working distance (filled from voltage and
  equipment type; the tutorial cites about 18 inches for LV), grounding (default
  ungrounded as conservative, or automatic), bolted fault current and a user fault
  clearing time; results: incident energy, flash boundary, hazard category; label
  templates printed through Crystal Reports.
- Global calculation: study case AF Data page defines gaps, working distance and other
  parameters globally (project settings hold the global table) so each bus needs only an
  equipment type; fault buses chosen as in short circuit; method NFPA 70E or IEEE 1584
  (default); clearing time found automatically from the TCCs of protective devices
  (typically only the main feeder device is given a TCC, as the slowest and most
  conservative), else the bus user FCT; option to write results back to each bus;
  reports, labels per device location and bus; AF Result Analyzer with worst case,
  labels, permits and data sheets.

## Third pass [E70 to E73]
- Cable thermal: Neher-McGrath and IEC 60287 steady state; transient by dynamic thermal
  circuit model for emergency loading; multiple duct banks and direct-buried conduits
  over several cross-sections; mixed sizes per raceway, phases in separate conduits,
  asymmetric layouts; cables dragged in from the one-line; user cable construction
  (insulation, screens, armour, sheath, jacket); derated ampacity and sizing with
  uniform-ampacity or uniform-temperature methods; fixed size or loading options;
  raceway rule book auto-layout; heat from neighbours and external sources; dielectric
  losses, loss factors, unbalanced load factors; outputs: dimensioned layouts, critical
  and marginal temperature flags, thermal resistances, EMF intensity, transient plots.
- Time-domain unified load flow: unlimited load and generation profiles, hourly or
  minute steps, CSV import, 8,760-hour years, seasons and holidays, blended customer
  classes, irradiance patterns, per-customer or meter profiles; single and multi-year
  growth; devices in or out of service over the period; smart inverters, STATCOMs,
  SVCs, VFDs; progress bar with elapsed and remaining time; time-series plots of current,
  drop, losses, demand, yield; Python custom reports.
- Voltage stability: four static methods: P-V curves, Q-V curves, Q-V sensitivity, Q-V
  modal (eigenvalue) analysis; loadability limit point.
- Intelligent load shedding white paper: conventional frequency relays act after about
  2 s and shed uncontrolled amounts, needing extra spinning reserve; ILS computes the
  exact load combination from the live system model and sheds within 80 ms, reprioritises
  continuously, verifies signals, and warns operators; cited example protects large SAG
  mills (mining) that take about a day to restart. (Vendor claims, not verified.)

## Fourth pass [E74 to E77]
- Underground raceway: Neher-McGrath and IEC 287; steady temperature, ampacity
  optimisation, automatic sizing, transient temperature from load profiles; tension and
  pulling analysis linked; grounded or ungrounded shields; armoured cables; thermal
  resistance and dielectric loss terms (Yc, Ys); unlimited cross-sections.
- Quasi-dynamic analysis: time-domain unbalanced load flow with a control system model:
  POI active power control, peak shaving, Q, V and PF control, storage management,
  renewable smoothing, islanded microgrid energy management, smart inverter Q-V and
  P-V droop with P-Q limits, user control logic, controller communication with delays,
  digital twins of plant and microgrid controllers, DNP3 for hardware in the loop.
- PMS (operations): real-time monitoring on one-lines and operator screens with alarm
  management; electrical and non-electrical tags; pseudo measurements; OPC; data
  reconciliation and bad data correction; predictive "what if" simulation on live data;
  event playback; energy accounting with tariffs; load forecasting; advisory corrective
  actions.
- Generator start-up: cold starts normal and emergency, frequency-dependent machine and
  network models, special turbine behaviour, saturation correction, field flashing,
  governor detail, relays (V, f, V/Hz, df/dt), motor acceleration under low V and f,
  load pick-up sequencing for black start.

## Fifth pass [E78 to E81]
- Optimal capacitor placement: objectives voltage support, PF correction, minimum
  installation and operating cost, maximum loss savings over a planning period; genetic
  algorithm with heuristic initialisation and integrated load flow; capacitor control
  analysed with load duration; speed versus precision setting; energy cost global or per
  source; candidate locations, types and bank sizes chosen by the user; maximum size from
  peak load, switched size from minimum load; min, max and average loading categories;
  planning period and interest rate; radial or meshed balanced networks; outputs:
  locations, bank sizes, branch capacity release, savings, operation cost.
- Switching optimisation: objectives losses, voltage violations, overloads, feeder load
  balancing through tie points, phase balancing, reliability risk on critical feeders;
  output a recommended switching list, before and after summaries, saved optimal
  configuration; switched capacitor modelling.
- Dynamics brochure model list: synchronous machines (IEEE equivalent, transient,
  subtransient; round and salient rotor); induction single and double cage;
  frequency-dependent machines and network; torsion; mechanical loads; UPS parallel
  operation; PV panels; VFD dynamics. Controls: IEEE exciters and AVRs, manufacturer
  exciters and governors, IEEE turbine-governors, PSS, user-defined. Events: 3-phase and
  L-G faults applied, cleared or on line segments, breakers, generator and load
  rejection, impact and ramp loading, grid voltage changes, governor mode switching,
  reference machine switching, motor acceleration and reacceleration; initial load flow
  NR or accelerated GS. Outputs: rotor angle, speed, V, I, Pm, Pe, exciter V and I,
  slip, torque, V/Hz, terminal impedance (for relays), branch flows, bus frequency, V/Hz
  vector difference, superimposed plots, one-line playback with event list.
- Wind turbine generators: types 1 to 4; individual or grouped; aerodynamics with power
  coefficients; DFIG with pitch and converter controls; ramp, gust and noise wind.
- UDM: library, block builder, Simulink import (brochure), compile and link, self tests.
- Parameter estimation: motor equivalent circuit at starting from locked-rotor current,
  PF and torque, full-load PF, efficiency and slip, and maximum torque, by curve fitting;
  single cage with deep bar result; torque-, current- and PF-slip curves; editor updated
  automatically.

## Star workflow and ARTTS (E101, E102; read 2026-10-15)

- **Workflow taught in the tutorial [E101]:**
  1. In Edit mode, drop a relay on the one-line.
  2. In the relay editor's OCR page, pick a library device through "Library Quick Pick"
     (example: GE Multilin 735/737). Settings levels have "link TOC + IOC" options.
  3. Enter CT ratios on the Input page (needed for calculations, not for viewing the
     TCC).
  4. Switch to Star mode and use "Create Star View" for a TCC.
  5. Add more devices with "Append to Star view", or Shift-drag from the one-line.
  6. Fuses are picked by manufacturer, model, speed and size.
- **Star capabilities [E102]:**
  - an intelligent alert view explains why a curve is missing data;
  - normalised (shifted) TCCs;
  - curve families: transformer damage and inrush, motor starting and stator damage,
    generator decrement, and arc flash energy curves;
  - device types: fuses, OC/OL/differential relays, reclosers, electronic controllers,
    HV and LV breakers, solid-state trips, thermal-magnetic, MCPs, overload heaters;
  - export of settings and short-circuit data to relay test sets.
- **ARTTS:** compares the relay's steady-state and transient responses against the
  manufacturer curves and reports the deviation, with COMTRADE export of fault
  waveforms.
- **Quantic implications:**
  - library pick-lists with manufacturer/model/size cascades are the core UX;
  - "why is this curve missing" alerts suit our diagnostics-with-field approach;
  - COMTRADE export (IEEE C37.111) of simulated faults is a cheap, valued feature that
    links protection to EMT (`engine-emt.md`).

## Getting Started guide: harmonics and stability (E110; relayed 2026-10-16)

Evidence classes: S seen in the cited source, I our inference, U unknown.

ChatGPT recovered the combined Getting Started guide (130 PDF pages), which closes the
failed tutorial fetches in dossier gap 3. Its printed pages 71 to 78 cover:

- **S** Harmonics: frequency scan and harmonic load flow are separate runs; results are
  plotted for selected buses and shown on the one-line.
- **S** Transient stability: events hold actions (for example a fault applied then
  cleared), machine models are selected per machine, and a time slider steps through
  results on the one-line.
- **U** The integration method, step defaults and harmonic solution method are not
  stated. The screens are historical workflow evidence, not 2026 defaults.
- **I** For Quantic: event payload, solver step, stored sample and plot selection stay
  separate objects; changing what is plotted must never change what is solved.

## Hosting capacity (E111, E112; relayed 2026-10-16)

- **S (relayed)** The product page offers nodal, stochastic and impact analysis with
  voltage and thermal constraints and smart-inverter functions [E111]. Not re-read by
  Claude: the fetch was not permitted on 2026-10-17.
- **S** ETAP announced US patent 12244141 for hosting-capacity analysis [E112].
  **U** its claims and scope. Before Quantic implements any hosting-capacity method, the
  patent's claims need reading and Peter's decision; general power-flow-constrained
  methods from the literature are a separate route.
