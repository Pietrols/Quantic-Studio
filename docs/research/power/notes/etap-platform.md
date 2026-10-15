# ETAP platform and workflow: working notes (paraphrased)

## Data model [E34, E25]
- One project database is the single source of truth: one-line diagrams, configurations,
  study cases, libraries, elements. Data is stored once and every study reads it, so
  "what-if" work never needs project copies.
- Three independent dimensions, combinable freely [E34]:
  1. Presentations: unlimited graphical views of the same network, each with its own
     layout, symbols, sizes, colours and device visibility; each remembers its mode,
     configuration, zoom and position.
  2. Configurations (status configurations): saved operating states: switching device
     open or closed, loads and motors continuous, intermittent or spare, generator
     control mode (swing, voltage control, Mvar, PF), MOV states. Any configuration can
     attach to any presentation.
  3. Revision data: base data (revision 0) plus unlimited revisions of engineering
     properties (nameplates, settings); one active at a time; compare alternatives,
     model future additions out of service, merge into base. Connectivity changes and
     new elements only in base data.
- Elements carry electrical, logical, mechanical and physical attributes together, for
  example cable routing feeds ampacity derating.
- Study cases hold calculation options per study type, separate from the network data.
- Loading categories are project-level names (Project, Settings) used for per-element
  percent loading (for example design, normal, max) [E35].

## Main window [E34]
- One-line view canvas: zoom, grid, drag and drop, cut and paste, undo and redo, groups.
- Toolbars: project (file, edit, view, grid, continuity check, themes, templates,
  hyperlinks, power calculator, find, help); theme (colour schemes, connector styles,
  background, contouring); mode (edit or a study mode); element palettes (AC, DC,
  instrument); study case (choose and edit case, output report name, report manager);
  system (scenario, study and project wizards); presentation and configuration
  selectors.
- Project view: a tree of presentations, configurations, study cases, libraries and
  components, plus a "dumpster" holding deleted items for recovery.
- Message logger (activity, users, access level); help line describing the active
  field; active error viewer listing missing or invalid data before a run, where a
  double-click opens the editor at fault.

## Modes [E34]
Edit mode plus 27 study modes in version 16: load flow, short circuit, arc flash, motor
acceleration, harmonic, transient stability, Star coordination, DC load flow, DC short
circuit, DC arc flash, battery sizing and discharge, unbalanced load flow, time-domain
load flow, unbalanced short circuit, voltage stability, OPF, reliability, optimal
capacitor placement, switching optimisation, FMSR (fault management and service
restoration), switching sequence management, contingency, rail traction, Star systems,
underground raceway, ground grid, cable pulling. Each mode has its own toolbar with run,
display options, alert view, report manager and result analyzer.

## Editing [E34, E35]
- Place elements from palettes (double-click a button for repeated placement); connect by
  dragging between pins or through the editor's Info page; buses connect along their
  whole length; nodes added automatically; protective devices dropped onto a branch
  without breaking it; right-click for orientation, size, symbol standard (ANSI or IEC)
  and hiding unused pins.
- Composite networks and composite motors nest subsystems to any depth.
- Element editors open on double-click, organised in pages (tabs); minimal required
  entry; typical data substitution; range and interdependency checks; change tracking;
  white fields are user entry; Library button opens "Quick Pick" to fill from
  manufacturer data; navigation buttons step through all elements of that type.
- Examples [E35]: motor editor Info page (in or out of service, unique ID, bus,
  equipment info, connection type, quantity), Nameplate page (HP or kW, percent loading
  per loading category). Cable: Info (ID, buses, length, service status, library),
  Impedance page needed for load flow and short circuit. Transformer: Rating page
  (primary and secondary kV, rating kVA or MVA, maximum rating, impedance or typical).
  Lumped load: model type, rating MVA or MW, percent loading per category, a slider
  splitting static and motor load.
- Continuity check greys out de-energised elements.

## Results and reporting [E34, E37]
- Results drawn on the one-line with configurable display options; overrated devices
  coloured; alert view (marginal and critical).
- Plots: time slider for transients, frequency scan plots, motor start plots.
- Report Manager: 250+ Crystal Reports formats in six languages (complete, input, result,
  summary), export to PDF, Word, Access, Excel, search by element ID.
- Schedules: bus, branch, load and cable schedules filtered by base or revision,
  energised status or dumpster.
- Result Analyzers compare studies.

## Automation and exchange [E34, E22, E26]
- Scenario wizard: records presentation, revision, configuration, mode, study case and
  report as a named scenario. Study wizard groups scenarios into macros. Project wizard
  runs macros across projects. Output database comparison against a benchmark run.
- ODBC (Access, SQL Server, Oracle), OLE, XML, ASCII import, converters from other tools;
  drawings to DXF, EMF, WMF, images. etapPy Python API, now with REST.

## System managers [E37]
- Theme manager: colour one-lines by standard, voltage level, area, grounding type,
  earthing system or ground-switch state; per-diagram themes; alert colours; phase
  count distinction; faulted bus marking.
- Configuration manager: table of all configurations, compare source, load and switch
  states, flag changes, copy, merge, import, export, print.
- Report manager (above). Data manager: view and edit base and revision data field by
  field, absolute values or differences, merge per item.

## Verification practice [E36]
ETAP publishes V&V cases comparing each module with published references. These are the
benchmarks a recreation must reproduce (references only; we use the original public
sources, not ETAP's documents):
- Load flow: Anderson and Fouad, Power System Control and Stability; R.N. Dhar,
  Computer Aided Power System Operation and Analysis; IEEE 399-1997; IEEE 3002.2.
- Unbalanced load flow: IEEE 13-node test feeder.
- Short circuit ANSI: GE short-circuit application guide hand calculation; Anderson,
  Faulted Power System Analysis (1973) pp. 38 to 40; IEEE 399-1997 section 7.7 44-bus.
- Short circuit IEC: a published example; IEC TR 60909-4:2021.
- Harmonics: IEEE 519-1992 example 13.1 (RMS, ASUM, THD, TIF, TPF).
- Motor starting: hand calculation with torque control; comparison with transient
  stability.
- Transient stability: field start-up data; IEEJ benchmark; DFR records; Anderson and
  Fouad 9-bus; PSS/E comparison.
- Arc flash: IEEE 1584-2018 examples; IEEE C2-2023 (NESC); DGUV-I 203-077 examples 5.1
  and 5.8 (AC and DC).
- Scale of regression testing stated: over 1,600 motor-starting and 1,100 IEC
  short-circuit scenarios per release.
