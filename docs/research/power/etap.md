# ETAP

Dossier for WP-2.10. Paraphrased from public sources only. Every bracket such as [E2]
refers to `notes/etap-sources.md`. Fuller working notes:
- `notes/etap-studies.md`: study by study.
- `notes/etap-platform.md`: data model, interface, automation and reviews.

## 1. Identity

- **Vendor:** ETAP (Operation Technology, Inc.).
- **Current release:** ETAP 2026 [E26].
- **Product families:** ETAP sells its products under five groups, Design, Build,
  Operate, Automate and Digital transformation, plus data management [E1, E22]:
  - **Network design and analysis:** "ETAP Power Simulator".
  - **LV design:** Caneco.
  - **Schematics and panels:** SEE Electrical.
  - **Real-time platform:** SCADA, PMS, ADMS, GMS, load shedding, microgrid and plant
    controllers.
- **Platform and licensing:** Windows desktop, licensed per module. Hardware dongles and
  a licence manager are used, rebuilt in 2026 with automated key exchange [E26, E48].
- **Trial:** a 30-day cloud demo exists [E2]. The older demo was limited to 12 AC buses
  and 10 DC buses, and could not save [E34].
- **Quality assurance:** ETAP states it follows nuclear QA standards: 10 CFR 50 Appendix
  B, 10 CFR 21, ASME NQA-1, ISO 9001 and IEEE 730.1 [E9, E22].

## 2. Sources

83 numbered sources are listed in `notes/etap-sources.md`, accessed 2026-10-15:
- vendor product pages and fact sheets;
- vendor tutorials (getting started, load flow, element properties);
- the vendor's V&V case list;
- the 2026 release page;
- a reseller listing;
- user reviews and one forum thread.

The full user guide is not published by ETAP. Copies on document-sharing sites are
unauthorised uploads, so they were not used.

## 3. Architecture and data model

**One project database.** A single database holds everything [E34, E25]:
- Network data is stored once and every study reads it. "What-if" work never needs
  copies of the project.
- Each element carries electrical, logical, mechanical and physical attributes together.
  For example, a cable's routing feeds its ampacity derating.

**Three independent dimensions**, freely combined [E34]:

| Dimension | Holds |
|---|---|
| Presentations | Unlimited views of the same network, each with its own layout, symbols, colours, visible devices, zoom and last mode |
| Configurations | Operating states: switches open or closed; loads and motors continuous, intermittent or spare; generator mode (swing, voltage control, Mvar, PF); MOV states. Any configuration attaches to any presentation |
| Revision data | Base data (revision 0) plus unlimited engineering revisions of nameplate and settings, compared, then merged into base. Topology changes only in base |

**Study cases** hold calculation options separately from the network [E6, E34]:
- method and convergence settings;
- loading and generation categories;
- diversity factors;
- per-element-type tolerances and temperature adjustments;
- alert limits;
- for faults and arc flash, the buses to fault.

**Loading categories** are project-level names. Each element holds a percent loading per
category, and demand factors apply for continuous, intermittent and spare operation
[E7, E35].

**Libraries** [E27]:
- **Master libraries:** cables (with fire protection), lines, wind, PV, transformers,
  motors, VSDs, batteries, control devices; system data such as reliability and
  interruption costs; protective devices (fuses, relays, reclosers, breakers, trip
  units, MCPs, overload heaters, RCD/GFI).
- **Equipment warehouse:** a project-linked subset of the master libraries.
- **Library management:** merge, project library file, change tracking.
- **Scale:** the 2026 release claims more than 23,000 library models [E26]. The older
  guide cites more than 50,000 TCC curves [E34].

**Other data features** [E25]:
- Client-server access with user permissions.
- NetPM: multi-user change control, review and approval.
- etapAPP: field data collection with geotags and photos.

## 4. Element catalogue

Elements named across the sources [E7, E9, E21, E23, E24, E25, E27, E34]:

| Group | Elements and noted parameters |
|---|---|
| Nodes | Bus (nominal kV, connects along its whole length), node (auto-inserted), panel, UPS, single-phase buses. Composite network and composite motor (nested sub-diagrams) |
| Branches | Cable (ID, buses, length, library, impedance page, routing), transmission line (line constants and coupling; sag, tension and ampacity modules), reactor, impedance, bus duct |
| Transformers | 2- and 3-winding, phase shifter, LTC and voltage regulator with regulated bus, grounding of windings. Rating page: primary and secondary kV, kVA or MVA, maximum rating, impedance or typical value [E35] |
| Sources | Utility or grid (swing, voltage-regulated, unregulated); synchronous generator with governor (isochronous or droop) and exciter (AVR, Mvar or PF control) |
| Renewables and storage | Wind turbine generators (types incl. 4), PV arrays (5,000+ models), batteries (lead-acid, lithium-ion), energy storage, inverters |
| Loads | Induction and synchronous motors (single cage, deep bar, double cage, characteristic model; torque-speed; load torque polynomial or curve); lumped load (static and motor split by slider; constant P, Z, I or a function of V and f [E9]); static load; capacitor; harmonic filter; MOV; DC loads |
| Drives and DC | VFD (V/Hz, ten frequency settings, multi-pulse input, dynamic model), soft starter, charger, UPS, DC converter, DC motor, battery |
| Protection and instruments | Fuse, LV and HV breaker, recloser, relay (overcurrent, directional, voltage restrained, differential, distance), trip unit, MCP, overload heater, contactor, CT, VT, ground switch, maintenance switch, arc sensors |
| Other | Ground grid, underground raceway, control circuit diagram elements (contacts, relays, solenoids) |

Common editor pattern [E34, E35]:
- **Info page:** ID, service status, connections, quantity, equipment information.
- **Nameplate or Rating page.**
- **Study-specific pages:** impedance, tap, loading, protection and others.
- **Library and Quick Pick buttons** fill values from manufacturer data.
- **Navigation buttons** step through all elements of the same type.

## 5. Studies and modules

| Study | Method and options | Outputs | Standards | Sources |
|---|---|---|---|---|
| Load flow | Newton-Raphson, adaptive NR, fast decoupled, accelerated Gauss-Seidel. User iterations and precision. LTC and AVR action, phase shifters, temperature correction. Loading categories, diversity factors. Combined 3-phase, 1-phase, panel and UPS solution. All islands in one run. AutoRun on change | Voltages, flows, currents, PF, losses, voltage drop. Critical and marginal alerts. Overload warnings. Result analyzer with baseline deviations | (vendor V&V vs IEEE 399, IEEE 3002.2, textbooks) | E2, E6, E7, E16 |
| Unbalanced load flow | Current injection. 1-, 2- and 3-phase, 3- and 4-wire. Line constants and mutual coupling. Winding connections, grounding, sequence impedances | Phase and sequence results, unbalance factors and alerts | IEEE 13-node feeder (V&V) | E9, E36 |
| Time-domain and quasi-dynamic load flow | Unlimited profiles (hourly or minute steps, CSV import, 8,760-hour years, seasons, customer classes, irradiance). Multi-year growth. Devices switched in and out over the period. The quasi-dynamic add-on adds controllers: POI active power control, peak shaving, Q, V and PF control, storage, smoothing, islanded energy management, smart-inverter Q-V and P-V droop, user logic with communication delays, DNP3 hardware in the loop | Time series of current, drop, losses, demand, yield. Progress bar | - | E22, E71, E75 |
| Optimal power flow | Interior point with log barrier on full AC flow. Objectives: losses, fuel or energy cost, shedding, security indices, multi-objective. Controls: generator P and Q, taps, capacitors | Optimal settings and changes | - | E8 |
| Short circuit ANSI/IEEE | Three networks (1/2, 1.5 to 4, 30 cycles). Separate R and X for X/R, multiplying factors, NACD. Contact parting time | Momentary, interrupting, closing and latching duty. Symmetrical vs total rated. LV at maximum voltage. Generator breakers | IEEE C37.04, C37.010, C37.13, C37.013, C37.20.1, IEEE 399/141/242, UL 489 | E3, E10 |
| Short circuit IEC | IEC 60909-0:2016. ip method A, B or C. User c. Max and min, near and far. KT, KG, KSO. Meshed Ib from machine contributions | Ik'', ip, Ib, Ik, idc. Device duty incl. 1- and 2-pole. LV service or ultimate capacity | IEC 60909, 62271-100/200/203, 60947-1/2, 60282-2, 60781 | E11 |
| Transient short circuit | IEC 61363 decay curves from a prefault load flow | idc, iac, ip versus time | IEC 61363 | E12 |
| Other SC | GOST R 52735 and R 28249. Distribution (unbalanced over time). DC (IEEE 946: contributions, rise and decay) | Duty checks | - | E3, E22, E43 |
| Arc flash | IEEE 1584-2018, NFPA 70E, DGUV-I 203-077, ENA NENS 09. Auto clearing time from source device with decay. Enclosure editor. Multi-source. Mitigation devices. HV ArcFault 1 to 800 kV. DC methods (max power, Stokes-Oppenlander, Paukert) | Incident energy at buses and load terminals, boundaries, PPE, labels, work permits | as listed | E13, E14 |
| Protection coordination (Star) | TCCs from libraries. Auto-evaluation by rule book. Zone and path detection. Sequence of operation (27, 49, 50, 51, 51V, 59, 67, 79, 87) with failure-backup. Normalised TCC. ZSI. Energy curves | Violations, settings reports, animated sequence | NEC, IEEE, IEC practice | E15, E28, E29 |
| Distance protection (StarZ) | Mho with polarisation and expansion, distance, differential, load encroachment. CT, VT, breaker blind spots. Out-of-step with stability | R-X, time-distance, settings export | - | E30 |
| Motor acceleration | Static and dynamic. Event sequences. Starters: autotransformer, reactors, resistors, capacitors, star-delta, part winding, soft starter (4 modes), VFD. LTC and capacitor switching during start | Speed, torque, V, I, P, Q vs time. Worst-case analyzer | (V&V vs hand calc) | E4, E23, E24 |
| Harmonics | Harmonic load flow (NR or GS fundamental) and frequency scan. Source library incl. interharmonics. Filters: single-tuned, high-pass, band-pass. Rule book of limits | THD, IHD, TIF, I*T, TDD, TRD, K-factor, spectra, waveforms | IEEE 519, IEC 61000-3-6/3-14, IEEE 1547, 2800 | E5 |
| Transient stability | Synchronous and induction machines, exciters, governors, PSS, SVC, HVDC, IBR, relays. Unlimited events. User time step. Critical clearing time, fast bus transfer, load shedding, islanding, ride-through | Live plots, plot analyzer | (V&V vs Anderson-Fouad 9-bus, PSS/E, field data) | E16 |
| Other dynamics | UDM block-diagram models. eMT (PSCAD EMTDC engine). eMTCoSim. Inrush. Generator start-up (cold and black start, saturation, field flashing, load pick-up). Parameter estimation (NERC MOD-026/027). MotorPro | - | - | E17, E38, E39, E26, E77 |
| Operations | PMS: live monitoring, alarms, data reconciliation, predictive simulation, event playback, energy accounting, forecasting. Intelligent load shedding computes the shed set from the live model (vendor claims about 80 ms, against about 2 s for frequency relays) | Advisory actions | - | E73, E76 |
| Voltage stability | P-V curves, Q-V curves, Q-V sensitivity, Q-V modal (eigenvalue) analysis | Loadability limit | - | E22, E72 |
| Contingency | N-1 and N-2 with fast screening and ranking (voltage, overload, delta P and Q indices), then AC runs | Lost load, lost generation, customers, cost | - | E33 |
| Reliability | State-based with switching restoration and load transfer. IEEE 493 and 3006.8 data, CDF costs | SAIFI, SAIDI, CAIDI, ASAI, EENS, ECOST and more. Sensitivity ranking | IEEE 493, 3006.8 | E31 |
| Optimisation | Optimal capacitor placement, switching optimisation, VVO, hosting capacity | - | - | E22, E26 |
| Cables | Sizing by ampacity, drop, motor-start voltage, short circuit, device, harmonics, let-through. Ampacity by 10 standards. Underground raceway thermal (Neher-McGrath, IEC 287) in steady state and transient (dynamic thermal circuit), for duct banks and direct-buried cables, with heat sources, uniform-ampacity or uniform-temperature optimisation and rule-book auto layout. Pulling and tension. Shock protection. PE sizing | Optimal and alternative sizes, temperatures, thermal resistances, EMF | IEEE 399, NEC, ICEA P-54-440, IEC 60502, 60364, 60092, BS 7671, NF C15-100, C13-200, AS/NZS 3008 | E18, E19, E22, E70, E74 |
| Transformer sizing | Load with growth, ambient, altitude, cooling stages. Impedance and BIL checks. Tap optimisation | MVA and impedance | ANSI C57.12/.92/.96, IEC 60076, 60726 | E20 |
| DC and batteries | DC load flow (NR). Battery sizing (IEEE 485 duty cycle, aging, temperature, design margin). Discharge | Cells, strings, profiles | IEEE 308, 485, 946 | E21, E41, E42 |
| Grounding | IEEE 80 and 81, IEEE 665. FEM for irregular grids. Two-layer soil from Wenner data | Step, touch, surface potentials, 3D plots | IEEE 80, 81, 665, EN 50522 | E32 |
| Panels | NEC demand factors, load code tables | Panel schedules | NEC, ANSI, IEC | E40 |
| Lines | Impedance and coupling, sag and tension, ampacity | - | IEEE 738 | E22 |

## 6. Workflow and interface

**Modes** [E34]:
- **Edit mode** builds the network.
- **Study modes**: 27 in version 16, one per study. Each has its own toolbar with run,
  display options, alert view, report manager and result analyzer.
- The **Mode toolbar** and **Study Case toolbar** sit beside the one-line.

**Main window** [E34]:
- One-line canvas.
- Project tree: presentations, configurations, study cases, libraries and components,
  plus a recovery bin.
- Message logger.
- Help line describing the active field.
- Active error viewer that lists bad data before a run and opens the faulty editor.

**Drawing** [E34, E44]:
- Element palettes, with repeat placement.
- Connections by pin drag or from the editor.
- Protective devices dropped onto an existing branch.
- ANSI or IEC symbols.
- Composite networks.
- Continuity check that greys out de-energised parts.
- Rule-based auto-build and AI auto-complete [E26].
- Themes coloured by voltage, area, phase, grounding or earthing system.

**Results** [E34, E44, E7]:
- Datablocks on the one-line, from templates per device type, showing input and results
  of several studies.
- Contouring of voltage or flow.
- Live plots on the diagram.
- Result precision and visibility that change with zoom.
- Alert views split into marginal and critical.
- Result analyzers comparing reports, cases and projects against a baseline.

**Report detail** [E51 to E54, E64]:
- Load flow: input, detailed and summary reports.
- Short circuit: per-source contribution reports (symmetrical, asymmetrical, zero
  sequence), phase and sequence profiles, impedance reports.
- Motor starting alerts: failure to start; low voltage at motors, MOVs and buses (by bus
  type and voltage level); generator and prime mover overload.
- Alert views can be filtered by area, zone or region.
- Alerts are critical at 100 % of a rating or more, and marginal above a user limit.

**Reports** [E34, E37]:
- 250+ Crystal Reports formats in six languages.
- PDF, Word, Access and Excel export.
- Schedules for bus, branch, load and cable.

**Automation** [E34, E46, E26]:
- **Scenario wizard:** saves presentation, revision, configuration, mode, study case and
  report together.
- **Study wizard:** macros of scenarios.
- **Project wizard:** runs macros across projects.
- **Output comparison** against a benchmark database.
- **etapPy (Python):** batch studies and result retrieval; REST, with one-line creation
  in 2026.

**Exchange** [E45, E26]:
- Excel and Access mapping.
- CIM XML (ArcFM).
- ArcGIS.
- SKM converter.
- Revit, AVEVA, SmartPlant, AutoCAD, ERACS, CanecoBT.
- MultiSpeak.
- DXF, EMF and WMF drawings.
- ODBC.

**2026 interface** [E26]:
- Network Manager matrix for bulk editing.
- 3D network view.
- Editing inside revisions, and revision comparison.
- AI copilot for natural-language queries and edits.

**Study setup patterns** [E63, E64, E66]:
- Short-circuit and arc flash cases split buses into "Fault" and "Don't Fault" groups,
  or set them by right-click on the one-line.
- Arc flash data can be set globally in the study case, so each bus needs only an
  equipment type. Clearing times come from device TCCs.
- Motor starting uses events holding actions: by load, by starting category, and load
  transition.
- Static starting needs only no-load and full-load acceleration times. Dynamic starting
  needs a model, a load model and inertia.

**Training order** [E67 to E69]: model, load flow, cable sizing, ANSI then IEC short
circuit and duty, motor starting, coordination and sequence of operation, arc flash,
harmonics, cable thermal, ground grid. This is the industrial study chain users expect
first.

## 7. What users value and dislike

**Valued** [E47, E48]:
- Approachable drag-and-drop modelling with defaults.
- The breadth of studies in one database.
- An inspectable database.
- Responsive support and training.

**Disliked** [E47, E48, E49]:
- Incomplete libraries, with slow additions through support tickets.
- Expensive add-on modules and maintenance.
- Dongle and licence-manager trouble.
- Files that won't open in older versions.
- Unclear errors and occasional calculation bugs.
- A real learning curve.
- Slow runs on a few hundred buses without a progress bar.
- Weak printing and difference reporting.
- Some missing devices, such as bus duct entered as Z%.

**Lessons for us:**
- Open libraries anyone can extend.
- One price.
- Forward- and backward-readable files.
- Explicit progress reporting and plain-language errors.
- Strong diff and compare tools.

## 8. Engines implied

These are the calculation engines ETAP's modules imply. Status against our code is in
`engines.md` (WP-2.12).

| Area | Engines |
|---|---|
| Steady state | Balanced NR, fast decoupled and Gauss-Seidel load flow with controls (LTC, AVR, phase shifter, Q limits, swing selection, islands, temperature correction). Unbalanced phase-frame load flow by current injection with line constants and coupling. DC load flow. Unified AC/DC. Time-series and quasi-dynamic flow. Interior point OPF. Continuation P-V and Q-V. Contingency screening and ranking |
| Faults | ANSI three-network with X/R multipliers and NACD. IEC 60909 with K factors and methods A, B, C. IEC 61363 time decay. IEC 61660 / IEEE 946 DC. Unbalanced faults by sequence networks. Device duty checks against library ratings |
| Protection | TCC curve library and evaluation. Path and zone detection. Rule-book checks. Time-ordered sequence-of-operation simulation. Distance characteristics in R-X. Arc flash IEEE 1584-2018 with clearing-time iteration and decay |
| Dynamics | Phasor-domain stability with machine, exciter, governor, PSS, IBR models and a block-diagram model compiler. Motor acceleration (dynamic and static). EMT (third-party engine) |
| Power quality | Harmonic load flow, frequency scan, filter design, IEEE 519 indices |
| Planning | Reliability by state enumeration with restoration. Optimal capacitor placement. Switching optimisation. Hosting capacity |
| Design calculators | Cable sizing and ampacity per many standards. Neher-McGrath and IEC 60287 thermal. Transformer sizing. Battery sizing (IEEE 485). Ground grid (IEEE 80 analytic and FEM). Line sag-tension and IEEE 738 ampacity. Panel schedule demand calculation |

## 9. Related working notes

- `notes/matrix-draft-etap-powerfactory.md`: draft capability matrix with our status.
- `notes/engines-library-map.md`: engines against Peter's books.
- `notes/open-source-foundations.md`: open engines we can build on.
- Comparisons with PowerFactory and SKM are in `notes/etap-platform.md`.

## 10. Gaps

1. **Full user guide and editor field lists are not public.** Only a few editor pages are
   known [E35]. Close by:
   - reading ETAP's own tutorial PDFs (`etap.com/docs/default-source/faqs-tutorials/`);
   - reading public university lab manuals that use ETAP;
   - using the public standards themselves to define the parameters we need.
2. **Numeric defaults are not public.** This covers convergence tolerances, iteration
   limits and alert thresholds. We must set our own and document them; we will not copy
   ETAP's.
3. **Read in later passes:** result analyzer, reports, motor-start alerts, ArcFault, DC
   arc flash, distribution packages, grid code, PV array, time-domain and quasi-dynamic
   flow, voltage stability, cable thermal and raceway, PMS, ILS, generator start-up.
   **Read 2026-10-15** (see `notes/etap-2026-and-remaining-modules.md`, E84 to E91):
   capacitor placement, distribution optimisation package, wind turbine generators,
   eTraX, transformer inrush, motor parameter estimation, control system diagram, and
   the 2026 release notes (hosting capacity and microgrid controller items).
   **Still unread:** a dedicated hosting capacity product page (only release notes and
   webinars found), and the transient stability and harmonics tutorials (fetch failed).
4. **Forum feedback:** two older threads were read (E96 from 2019, E97 from 2009;
   summary in `notes/etap-platform.md`). Recent (2023 to 2026) threads are still
   missing: search results surface mostly Capterra and old forum posts.
5. **ETAP's V&V cases** were catalogued 2026-10-15 (23 cases, E36, E92 to E94) and
   mapped to what Quantic can reproduce in `notes/verification-benchmarks.md`. Two
   documents were read in detail. The rest of the combined PDF (E94) is still unread.
