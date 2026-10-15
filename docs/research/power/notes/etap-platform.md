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

## Data exchange and scripting [E45, E46]
- Exchange: Excel and Access worksheet mapping; ArcFM CIM XML import with GIS diagram
  generation; ESRI ArcGIS conversion; SKM PowerTools (Dapper, Captor) conversion; legacy
  converters; Revit import; AVEVA Electrical; SmartPlant Electrical two-way sync; eXCAD;
  universal mapping between databases.
- etapPy: Python inside ETAP (bundled IDLE or external IDE); batch studies across
  revisions, configurations and study cases; read project data (bus and element names,
  configurations, revisions, one-line XML); load flow, unbalanced load flow, harmonics,
  transient stability, motor starting, voltage stability, short circuit and any
  scenario-wizard study; local or remote ETAP instances; distribution of runs across
  machines; Excel templates for some studies.

## What users say [E47]
- 2009 Arc Flash Forum thread: ETAP judged friendlier and more flexible than SKM, with an
  inspectable Access-compatible database; complaints about bugs in a major release
  (arc flash, aluminium cable ampacity, reports), late releases, uneven support, and a
  missing option to enter bus duct impedance as Z% rather than X/R. Common advice:
  understand the IEEE calculations so software results can be judged. (Old thread;
  more recent user feedback still to collect.)

## Review themes [E48, E49, E50]
- Praised: approachable drag-and-drop modelling with sensible defaults; breadth of
  studies in one tool; responsive support, webinars and training.
- Criticised: incomplete libraries (regional cables, relays, breakers) and slow additions
  via support tickets; expensive add-on modules and maintenance; dongle and licence
  manager trouble; files not opening in older versions and model transfer problems;
  unclear error messages; learning curve needing training; slow runs on a few hundred
  buses without progress indication; report presentation, diagram printing and
  difference reports; missing devices and languages in some versions. G2 rates cost in
  its most expensive band. (ZipDo list is generic and weighted low.)

## Training scope (what ETAP teaches first) [E67 to E69]
- Order of the standard 4-day course: modelling (menus and toolbars, components,
  manual or automatic one-line building, display options and colour themes, revisions,
  the 3-D database, libraries, import and export, project management, scenario wizards);
  load flow (data needs, methods, load and generation models, diversity and demand
  factors, settings, reports, result analysis); cable sizing (libraries, loading,
  installation types, ampacity, standards, constraints); ANSI short circuit (1/2, 4 and
  30 cycle, device duty, 3-phase and unbalanced faults); static and dynamic motor
  starting (models, starting devices, parameter estimation, plots); coordination and
  selectivity (library, arrangements, TCCs); automated evaluation and sequence of
  operation (rules, zones, error handling); AC arc flash (NFPA 70E and IEEE 1584, PPE,
  labels); harmonics and filter sizing; underground cable thermal (conduit and duct bank,
  heat sources, steady and transient temperature); ground grid (regular and irregular,
  IEEE 80 and FEM, 3D plots).
- The arc flash course adds IEC short circuit (IEC 60909 in meshed and non-meshed
  networks, IEC 61363 transient currents).
- Reading: the core workflow every ETAP user learns is model, load flow, cable sizing,
  short circuit and duty, motor starting, coordination, arc flash. This is the industrial
  study chain a recreation must cover first, in this order.

## Comparisons [E82, E83]
- A 2024 thesis comparing ETAP and PowerFactory finds no universally better tool.
  PowerFactory splits a generator into a reusable type and a diagram element (flexible
  for complex systems); ETAP keeps one object with pages (Info, Rating, Imp/Model,
  Protection), which is practical. ETAP's "Typical Data" fills impedances when
  equipment data is incomplete in early project phases; generation categories give
  several operating profiles per machine; strong decrement curves. PowerFactory derives
  the generator damage curve from machine parameters and has a dedicated IEC 60909 page.
- ETAP versus SKM: ETAP's single integrated one-line model feeds all studies, has broad
  specialty modules and live plant links (utilities, EPC, heavy industry); SKM's
  coordination and TCC workflow is fast and its core package cheaper (consultants doing
  coordination and arc flash); neither imports the other's native files, so switching
  means rebuilding the model.
- Design lesson for us: offer both styles (one element with typical data for early
  phases, plus reusable types for detailed work), and import competitors' files so
  switching does not mean rebuilding.

## User feedback from forums (E96, E97; read 2026-10-15; old threads, treat as indicative)

- **2019 Eng-Tips [E96]:**
  - EasyPower is praised for ease of use and fast support, including adding library
    devices.
  - Licences come in bus-count tiers and module bundles you may not need.
  - SKM is mandated by many specifications in some regions.
  - A plant buyer's real concern: the model changes often (half the flows reshuffled,
    yearly major reconfiguration), so **ease of editing and model maintenance matter
    more than features**.
  - Another member warns that firms train one person, keep paying maintenance, and lose
    the know-how when that person leaves.
- **2009 Arc Flash Forum [E97]:**
  - users found EasyPower and SKM friendlier, with better printed output, than ETAP;
  - SKM is valued for its pre-modelled equipment library (including European types);
  - ETAP is more common in utilities.
- **Quantic implications:**
  1. Model maintenance (diff, merge, bulk edit; our git and JSON approach) is a buying
     reason.
  2. Bus-count and module tiers frustrate buyers. A simple, transparent pricing story
     helps.
  3. Report quality is a visible differentiator.
  4. Built-in learning material and the worked trace reduce the "one trained person"
     risk. This matches the learning notes Quantic already writes.

## Technology stack (E105, ETAP 26.0.1 requirements; read 2026-10-15)

- **OS:** 64-bit Windows only (Windows 10 and 11, Server 2019 to 2025). Windows on ARM
  and Parallels on Apple M3 are "tested, not fully supported".
- **Runtimes:** both .NET Framework 4.8 and .NET 8 (desktop and ASP.NET Core), which
  points to a legacy WinForms/WPF core plus newer web services.
- **Data:** SQL Server 2022 Express LocalDB (installed), SQLite, the Access engine and
  MongoDB, with ODBC and OLE DB drivers. Several storage generations coexist.
- **Calculation engines:** the Intel Fortran runtime is required, which suggests at least
  some solvers are Fortran.
- **Other components:**
  - reporting: SAP Crystal Reports runtime;
  - licensing: Thales Sentinel RTE, network or USB key;
  - graphics: Direct2D;
  - Python 3.13 and Node.js 24 present (scripting, etapPy, web tooling).
- **Hardware:** sized by bus count (8 GB at 100 to 500 buses, 32 GB at 10,000+);
  recommended **dual 4K monitors**; NVMe for 20,000+ buses.
- **Quantic implications:**
  1. ETAP is Windows-bound with heavy installs (30 to 100 GB). A browser-based
     workbench with a Python engine runs on any OS, including Peter's Mac and site
     laptops. That is a real distribution advantage.
  2. Their mixed storage shows the cost of decades of growth. Our single JSON contract
     plus git is simpler, and we must keep it that way (one source of truth).
  3. Dual-4K recommendations show how dense the ETAP UI is. Peter's "plain, less
     cluttered" direction is a deliberate contrast.

## Enterprise protection management: eProtect (E104)

A central relay settings database across sites:

- as-found against as-designed comparison;
- change notifications and a tracking dashboard;
- settings download and upload over FTP, SFTP and IEC 61850;
- vendor software integration and automatic setting-file generation;
- asset lifecycle and maintenance planning;
- NERC compliance reporting;
- a mobile web interface;
- multi-user access control.

It is the ETAP counterpart of PowerFactory's StationWare (P71). Both vendors sell
settings management as a separate enterprise product. For mines with hundreds of relays
it is a natural later Quantic product built on the protection device library.

## Arc flash scope (E106)

- **Standards:** IEEE 1584-2018 and 2002, NFPA 70E (including DC annexes), German BGI/GUV
  5188E (the predecessor of DGUV-I 203-077), Australian ENA NENS 09-2014.
- **Workflow:** auto-evaluation at many locations; mitigation comparisons; multilingual
  labels; work permits; PPE approval.
- **DC methods:** maximum power, Stokes and Oppenlander, Paukert.
- **HV:** 1 to 800 kV, approach distances (OSHA 1910.269, NESC), arc-in-a-box from 15 to
  36 kV.
- **Integration:** flags device mis-operation due to arc flash; integrates with Star TCC.
- Confirms that the IEC-world method (DGUV and its predecessor) is a mainstream option,
  supporting `engine-arc-flash.md` sec. 6a.
