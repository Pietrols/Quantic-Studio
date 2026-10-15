# DIgSILENT PowerFactory

Dossier for WP-2.10. Paraphrased from public sources only. References such as [P3] point
to `notes/powerfactory-sources.md`; the fuller working notes are
`notes/powerfactory-notes.md`.

## 1. Identity

- **Vendor:** DIgSILENT GmbH, Germany.
- **Current release:** PowerFactory 2026 [P31].
- **Platform:** 64-bit Windows, with a multilingual user interface in UTF-8 [P48].

**Editions** [P32]:
- Single-user, with a local SQLite database.
- Multi-user, with a licence server and local databases.
- Team, with a central Oracle, SQL Server or PostgreSQL database. Team adds master
  projects, versions, derived projects, compare and merge, and offline mode.

**Licences** [P32]:
- Commercial licences are sold by node count: 100, 250, 500 or unlimited.
- Other licence types: research, education (50 nodes), student (50 nodes), thesis, and
  a 28-day demo without the API or exports.
- Engine licences run without a GUI.
- Licences come as perpetual, subscription or time-limited.

**Packaging** [P1]: a base package plus licensed advanced functions.

**Documentation** [P48, P2]:
- A user manual of over 1,500 pages, plus technical references for every model.
- Both require a registered account. They were not used.

## 2. Sources

Fifty numbered sources are listed in `notes/powerfactory-sources.md`, all accessed
2026-10-15:
- vendor function pages;
- the 2026 release note;
- licensing documentation;
- vendor white papers;
- the vendor's public FAQ;
- an academic tutorial site.

The public download area also offers brochures, highlights, the product specification
and about 25 technical papers [P2]. Their downloads did not open with our fetch tool and
are listed under gaps.

## 3. Architecture and data model

**Database.** PowerFactory uses one hierarchical, object-oriented database [P6]:
- **Libraries** hold types and templates.
- **Projects** hold grids, diagrams and study cases.
- The database supports undo and rollback.
- Local databases can be encrypted.

**Element and type objects** [P39, P5]:
- An element, such as a line or a load, references a type that holds shared
  data, such as a line type or a load type ("TypLod").
- Commands are objects too, such as the load flow command "ComLdf".
- Variables are addressed by name, such as "b:ipat" for the island index of a bus.
- Any variable can become a column in Flexible Data pages and the Network Model
  Manager [P34, P41].

**Time-varying network** [P6]:
- **Variations** are made of time-stamped expansion stages, managed in a variation
  manager.
- **Operation scenarios** hold operating data separately from the network: switch
  states, dispatch and loads. They have their own manager.
- **Study cases** bring together active grids, variations, operation scenario, triggers
  (time points that drive characteristics) and calculation commands.

**Versions and teams** [P6, P36]:
- Project versions record history.
- Master and derived projects store only differences from the base.
- Updates move from the base down to derived projects, and merges move from derived
  projects back up.
- Compare and merge works two-way or three-way, matching by ID (foreign key or CIM
  rdf:ID) or by position in the hierarchy.
- Users belong to groups with rights.
- Offline subscriptions sync back to the central database.
- Interface profiles are set per group.

**Data model extension** [P6]:
- Users can add their own classes and attributes.
- Add-on modules can add input attributes and result variables [P24].

**Characteristics** [P5, P16]:
- Time profiles and parameter characteristics drive values over time or by scenario:
  scales, vectors, matrices and files.
- Examples include load profiles, wind and PV infeed, and temperature.

**Grouping** [P5]: zones, areas, boundaries, circuits, routes, feeders, operators and
owners.

## 4. Element catalogue

From [P5, P7]:

| Group | Elements and noted variants |
|---|---|
| Topology | Sites, substations, bays; terminals and busbars; busbar systems (single, double with or without tie, breaker-and-a-half, bypass, user-defined); breakers, fuses, disconnectors, load-break and earthing switches, neutral earthing; running arrangements and switching rules |
| Instrument transformers | CT, VT, CVT, combined CT/VT, with saturation [P11] |
| Machines | Synchronous: classical, standard 2.2, 3.3, asynchronous starting, permanent magnet, GENQEC. Asynchronous: single and double cage, saturable, doubly fed |
| Static generation | Generic static generator (wind, PV, fuel cell, micro-turbine, battery, storage) with wind power curve; PV system from irradiance; PV panel with two DC terminals; MPPT controller |
| Sources and loads | External grid; general and complex loads with Q(V) and Q(P); MV and LV loads from annual energy or profiles; moving train load; voltage-dependent load types; AC and DC voltage and current sources; Fourier, harmonic and impulse sources |
| Branches | Overhead lines from electrical data or tower geometry (PI or distributed; constant or frequency-dependent modal or phase domain; couplings incl. with cables and pipes); cables from data or core geometry; series reactor and capacitor; common impedance; fault current limiter; duplex reactor; busbar trunking |
| Transformers | 2-, 3- and 4-winding, autotransformer, booster; step voltage regulator; tap controllers and line drop compensation [P38] |
| HVDC and power electronics | LCC, CCC, two-level VSC, half- and full-bridge MMC (CIGRE TB 604 types 3 to 7); PWM converter, rectifier and inverter, soft starter, DC-DC converter; user EMT topologies from diodes, IGBTs, thyristors, MMC valves |
| FACTS and filters | SVC, TCSC, SSSC, STATCOM; single-tuned, double-tuned and high-pass filters |
| DC | DC battery, DC machine, DC load, DC lines and cables |
| Protection | Relay models built from about 30 core function blocks; manufacturer relay, fuse, LV trip unit and recloser library; programmable logic; inter-relay signals [P11] |
| Control | Station and secondary controllers, virtual power plant, generator capability curves, user load flow controllers, DSL, Modelica and UDM dynamic models |
| Composite | Composite branch and node models with templates (substations, wind turbines, PV) [P8] |

## 5. Studies and modules

| Study | Method and options | Outputs | Standards | Sources |
|---|---|---|---|---|
| Load flow AC | One non-decoupled Newton-Raphson for balanced and unbalanced networks, robust from any start. Station controllers with Q(U), cos phi(P), Q(P) and droop, local or remote. Taps, shunts, SVC. Voltage-dependent loads. Detailed induction machines. Temperature dependency. P limits and voltage-dependent Q capability. Primary and secondary control, inertia-based or distributed slack, interchange schedules. Feeder load scaling | Flows, voltages, losses (load and no-load). Loading against continuous and short-term ratings depending on ambient, wind or irradiance. Power at risk | - | P3, P40 |
| Load flow DC | Linear DC for P and angles. Coupled AC/DC incl. meshed DC grids | - | - | P3 |
| Short circuit | IEC 60909, VDE 0102/0103, ANSI C37, IEEE 141, IEEE 551, G74 (issue 2), IEC 61363. "Complete method" superposition on an actual load flow incl. converter voltage support. DC per IEC 61660 and IEEE 946. Any single or multiple fault, incl. open conductors and inter-circuit faults. Fault sweep along lines. Short circuit within contingencies | Currents per standard, sweep diagrams | as listed | P4, P31 |
| Sensitivities | Voltage and flow sensitivities. Tap sensitivities. PTDF, LODF, OTDF, PSDF, TCDF. Modal analysis | - | - | P10 |
| Contingency | AC (balanced or unbalanced), DC, AC-linearised. Single or multiple time phases. Generated or manual fault cases with validity periods. Dynamic contingencies. Remedial action schemes. Effectiveness of controls. Time sweep. Parallel | Loading and voltage reports, lost load and generation, islanding, trace playback | - | P15, P37 |
| Quasi-dynamic | Load flow series over a time window with characteristics, storage states, planned outages and expansion stages. QDSL user equations. Neural-network surrogate (AI) | Time series, statistics | - | P16, P50 |
| Protection | Overcurrent TCC (drag-edit), sequence components, thermal, damage and motor curves. Directional polarisations. Differential with harmonic blocking. Voltage and frequency. Distance: mho, polygon, R-X, P-Q, time-distance, out-of-step. Short-circuit trace. Graphic assistant sweeps. Coordination assistant for automatic settings. Protection audit | Settings reports, audit reports, write-back of settings | - | P11 |
| Arc flash | IEEE 1584-2002 and 2018, NFPA 70E-2021, DGUV 203-077, EPRI. DC per NFPA 70E and DGUV. Clearing times from protection | Incident energy, boundary, PPE category on the diagram, labels | as listed | P12 |
| Cables | Sizing per IEC 60364-5-52, IEC 60502-2, BS 7671, NF C15-100, NF C13-200, VDE 0298-4, VDE 0276-1000. Ampacity by IEC 60287 and Neher-McGrath with geometry and neighbours | Recommended types, optimised size or parallel count | as listed | P13 |
| Harmonics and PQ | Balanced and unbalanced harmonic load flow incl. interharmonics. Frequency sweep with resonance detection. Flicker IEC 61400-21 and flickermeter IEC 61000-4-15. Filters. Ripple control. Transformer K-factor | THD, HD, TIF, limits plots (IEC 61000-3-6, BDEW), impedance loci, waveforms | IEC 61000-3-6, 61000-4-15, 61400-21, UL 1562, IEEE C57.110 | P14 |
| Connection assessment | Voltage change, flicker, unbalance, loading, short circuit, harmonics, interharmonics, ripple, notches, resonances | Pass or fail report | D-A-CH-CZ, BDEW, VDE-AR-N 4105, 4100, 4110 | P29 |
| Transmission tools | P-V and Q-V curves. Transfer capacity with constraints. PTDF. Flow decomposition | Curves, limits | - | P23 |
| Distribution tools | Hosting capacity. Tie open point optimisation. Phase balancing. Voltage profile optimisation. Optimal equipment and capacitor placement. Backbone calculation. Probabilistic LV load flow with coincidence curves. Feeder voltage profiles | Capacity maps, reports | - | P22, P28 |
| Reliability and restoration | Fast state enumeration with IEEE 1366 indices. Failure effect analysis with protection, reconfiguration and shedding. Optimal manual restoration. Monte Carlo generation adequacy. Optimal RCS and recloser placement | Indices, contributions, restoration animations | IEEE 1366 | P21 |
| OPF and dispatch | AC OPF by interior point (or IPOPT). DC OPF by LP. Objectives: losses, reactive reserve, cost, shedding, remedial actions, redispatch cost. Unit commitment with ramps, min up and down, reserves, storage, preventive and curative redispatch | Optimal setpoints, schedules | - | P20, P45 |
| State estimation | P, Q, I and V measurements. Optimisation solver. Observability and redundancy. Bad data detection | Estimated loads, generation, taps | - | P26 |
| Probabilistic | Monte Carlo and quasi-Monte Carlo load flow and OPF with correlated distributions | Statistics, distributions | - | P44 |
| Economics | Techno-economic NPV with best investment year. Power park energy (Weibull, time series, probabilistic) | Reports | - | P46 |
| Network reduction | Ward, extended Ward, REI-DIMO, load equivalents. Dynamic equivalents | Reduced grid as variation | - | P43 |
| RMS stability | Balanced and unbalanced. A-stable variable step (ms to minutes). DSL, Modelica (FMU export) and UDM. IEEE, IEC, WECC and ENTSO-E libraries. FMI, IEC 61400-27, TB 958 imports. Co-simulation RMS and EMT. Scans for frequency, synchronism, voltage, FRT | Plots, FFT, Prony, Bode, Nyquist | - | P17 |
| EMT | Detailed power electronics, frequency-dependent lines and cables, saturation, arresters. Fixed or adaptive step. Parallel partitioning | Overvoltage, inrush, TRV, ferroresonance, SSR results, COMTRADE | - | P18 |
| Small signal | All or selected eigenvalues, participation factors, controllability and observability. Impedance-based IBR stability | Eigenvalue plots, mode reports | - | P27 |
| Motor starting | Static or dynamic. Reactor, autotransformer, rotor resistance, star-delta, soft starter, start at any speed. Thermal checks of cables and transformers | Automatic start check on the diagram, voltage drop before, during and after, start time | - | P19 |
| Parameter identification | Fit model parameters to measurements (gradient, swarm, pattern search, global) | Fitted parameters | - | P49 |
| Outage planning | Scheduled and recurring outages with linked switching and shedding | Gantt charts, maps | - | P30 |

## 6. Workflow and interface

**Window and profiles** [P48, P36, P54]:
- Tabbed, flexible window layout. Since 2025, panels can be arranged freely and
  collapsed (output window, drawing toolbox, project overview). Dark mode is available.
- Interface profiles add or hide buttons, menus, functions and models per user group.
- Integrated script editor and report designer.
- Categorised output window.

**Data views** [P6, P34]:
- **Data Manager:** tree of the database, with an address line for fast navigation.
- **Network Model Manager:** spreadsheet per element class, holding input and results,
  sortable and filterable.
- **Flexible Data pages:** columns of variables the user chooses.
- Copy and paste to Excel.

**Diagrams** [P8, P35]:
- One element can appear in many diagrams.
- Single-line diagrams come in simplified or detailed form, with three substation
  detail levels: composite node, design view and detailed graphic.
- Geographic diagrams sit on map services or WMS.
- Overview and area-interchange diagrams.
- **Diagram Layout Tool:** draws from data, with k-neighbourhood expansion, feeders,
  detailed substations and area interchange.
- Symbol editor; templates; layers with opacity.
- Colouring by voltage, owner, grid or results, with a heatmap background.
- Flow arrows and loading-width lines.
- Load and generation circles; switch markers.

**Results** [P34]:
- Configurable result boxes on diagrams.
- Default colouring flags limit violations. In contingency mode it shows the worst case
  across all contingencies.
- Output window with warnings and convergence information.
- Plots: time series, protection, R-X, eigenvalue, vector.
- Tabular reports for large studies.
- PDF reports with a built-in viewer, Word export and branding.
- Report Designer.
- Script-based reports from the results file.

**Automation** [P24, P47]:
- DPL, a C-like scripting language.
- Python with the full data model.
- External C++ API.
- Task Automation Tool for parallel runs.
- OPC DA and UA, IEEE C37.118 PMU streams, FMI co-simulation.

**Exchange** [P25]:
- PSS/E v27 to v35 (RAW, RAWX, SEQ, DYR).
- PSS/U, PSS/ADEPT, Sincal, UCTE-DEF, NEPLAN 5, Integral, Reticmaster, ANAREDE and
  ANAFAS.
- DGS, its own two-way format over ASCII, XML, CSV and ODBC, used for GIS and SCADA.
- CIM/CGMES, covered in a white paper [P33].

**Training order** [P55, P57]:
1. Interface and data structure.
2. Type versus element data.
3. Build an HV network.
4. Simple busbars versus detailed substations.
5. Load flow settings and results.
6. Load flow control. Discrete taps, shunts and generator Q limits are handled in an
   outer loop around the Newton-Raphson inner loop. Station controllers and taps.
7. An MV extension as a separate grid, with templates.
8. IEC 60909 short circuit for cable, busbar and breaker dimensioning.
9. Complete method and multiple faults.
10. Earthing concepts and single-phase faults.
11. Grids, variations, expansion stages, operation scenarios and study cases.

Advanced courses cover scripting, renewables, harmonics, protection, stability, DSL,
Modelica, EMT, HVDC and every planning tool.

## 7. What users value and dislike

Public user reviews are scarce: G2 lists no reviews [P51].

The only comparison found was a generic listicle [P52], which mentions:
- several solvers with convergence control;
- unbalanced capability;
- a heavy data-governance load on large models;
- complex setup for contingency studies and mixed transmission and distribution work.

That listicle is weighted low, and the gap is recorded below.

**Lessons drawn from the design itself:**
- The element and type split and the operation-scenario and variation split keep large
  multi-year models manageable.
- The same object model serves the GUI, scripts and team merging.
- The price is a steep conceptual learning curve. We should keep the concepts but
  explain them in the interface.

## 8. Engines implied

| Area | Engines |
|---|---|
| Steady state | Unified balanced and unbalanced non-decoupled NR with station control, Q(U), droop and distributed slack. Linear DC flow. AC/DC with meshed DC grids. Quasi-dynamic time series. Probabilistic MC and QMC flow. Interior-point AC OPF. LP DC OPF and unit commitment. Weighted state estimation with bad-data detection. Sensitivities and distribution factors. Continuation P-V and Q-V. Transfer capacity. Network reduction (Ward, REI) |
| Faults | IEC 60909, VDE, ANSI, G74 and IEC 61363 standard methods. Complete superposition method. Multiple and open-conductor faults in phase frame. DC faults (IEC 61660, IEEE 946). Fault sweeps |
| Protection | Function-block relay engine shared by steady state, RMS and EMT. Overcurrent, distance, differential, directional. Automatic coordination and audit |
| Dynamics | A-stable variable-step RMS solver (balanced and unbalanced). DSL compiler. Modelica and FMI. EMT with frequency-dependent lines and switching. Co-simulation. Eigenvalue analysis. Impedance-based stability. Parameter identification |
| Planning | Reliability state enumeration with restoration. Monte Carlo adequacy. Hosting capacity. Tie open point and phase balancing optimisation. Techno-economic NPV |
| Design | Cable sizing to European and IEC standards. IEC 60287 and Neher-McGrath ampacity. Harmonic indices and filters. Flicker. Connection-request rules |

## 9. Gaps

1. **Product specification, brochures, highlights and papers** in the public download
   area did not open with our fetch tool [P2]. Next pass: try alternative links or ask
   Peter to download these public PDFs and add them to `Pietrols/QE-References`.
2. **The user manual and technical references are registration-only.** We will not use
   copies posted elsewhere. The model equations come from our owned textbooks and from
   standards.
3. **Element dialog fields and default values** are not public, except a few named in
   the FAQ.
4. **Independent user feedback** was not found.
5. **Remaining reading:** the rest of the public FAQ entries (about 70 tags) and the
   remaining white papers (CIM, LV analysis, GIS, network planning, smart meter data,
   UI customisation).
