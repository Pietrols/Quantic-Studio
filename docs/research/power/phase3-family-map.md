# Phase 3 engine family map and learning index

WP-3.3, started and completed 2026-11-05 by the DeepSeek worker in OpenCode. This is a
navigation aid for the Phase 3 build, not a build order and not a claim of parity. It
maps every row of [parity-matrix.md](parity-matrix.md) to a Phase 3 work package or to
a recorded deferral, and it lists the book, standard and benchmark material each family
must read and verify.

Public sources only. The private reading map, the ETAP and PowerFactory survey paths
and the textbook fixtures stay in `Pietrols/QE-References` and are not reproduced here.
Where the public research names a book but not a section, the entry says so and the gap
is recorded in section 5. Where a standard is not owned, decision D18 and the relevant
engine note stand: the method can be built, the standard-grade constants and
certification cases wait for the purchase.

## 1. How to read this map

- **Parity rows** are the IDs in [parity-matrix.md](parity-matrix.md): D, G, S, F, P,
  A, M, T, H, C, PW and X.
- **Phase 3 WPs** are the WPs in `PLAN.md` sections 8 to 11.
- **Coverage labels** in the disposition tables:
  - `full`: the WP is written to cover the row as worded.
  - `partial`: the WP covers a named subset and the rest is called out.
  - `deferred`: no Phase 3 WP covers the row; a later milestone or a new WP is needed.
- **Private notes** means the private ETAP and PowerFactory survey covers the family.
  The survey paths and the per-WP reading pointers are in the private reading map and
  are not listed here.
- **Public benchmarks** are cases that are free to use or that we derive ourselves.
  MATPOWER case data has a licence caveat recorded in
  [notes/verification-benchmarks.md](notes/verification-benchmarks.md); WP-3.2 records
  the provenance before any case file enters the repository.
- **Private fixtures** are textbook worked examples. They load through `QE_REFERENCES`
  at test time and are never printed. Public CI runs public benchmarks only.

## 2. Book key

Short names follow [notes/engines-library-map.md](notes/engines-library-map.md).

| Short name | Book or standard |
| --- | --- |
| Alstom11 | Network Protection and Automation Guide, 2011 |
| Anders05 | Rating of Electric Power Cables, 2005 |
| Arrillaga03 | Power System Harmonics, 2003 |
| Blackburn06 | Protective Relaying: Principles and Applications, 2006 |
| Bose02 | Power Electronics and AC Drives, 2002 |
| Das02 | Power System Analysis, 2002 |
| Das10 | Transients in Electrical Systems, 2010 |
| Das21 | Arc Flash Hazard Analysis and Mitigation, 2021 |
| DGUV-I 203-077 | DGUV Information 203-077, arc flash |
| DZS 691 | Zambian draft grounding standard, owned draft |
| Fitz03 | Electric Machinery, 2003 |
| Glover17 | Power System Analysis and Design, 6th edition, 2017 |
| Gonen88 | Transmission Engineering, 1988 |
| Grainger94 | Power System Analysis, 1994 |
| Kasikci02 | Short Circuits in Power Systems, 2002 |
| Krause23 | Analysis of Electric Machinery and Drive Systems, 2023 |
| Kundur94 | Power System Stability and Control, 1994 |
| Morley | Mine Power Systems, IC 9258 |
| Najm10 | Circuit Simulation, 2010 |
| Sauer06 | Power System Dynamics and Stability, 2006 |

## 3. Engine family map

| Family | Parity rows covered | Phase 3 WPs | Books and standards (id and section) | Public benchmarks | Private notes | Open gaps |
| --- | --- | --- | --- | --- | --- | --- |
| Network model, types and topology | D1, D2, D3, D4, D11, G2, G7, S9, PW-D1 | WP-3.4, WP-3.5, WP-3.13, WP-3.51, WP-3.54 | Grainger94 and Glover17 for network equations; section pointers are in the private reading map, not in the public research | Coupler station case; three-terminal radial feeder | Yes, ETAP and PowerFactory survey | D5, D7 to D10, D15 and D17 deferred; bay detail and composite networks deferred |
| Study preparation, per unit, sparse Ybus and factorization | D2, S1, S5, S11 | WP-3.1 | Grainger94 and Glover17 for per unit; Kundur94 for transformer modelling; section pointers are in the private reading map | MATPOWER case9, case14, case30 and case118 Ybus; hand two-terminal, tapped transformer, phase shifter and three-winding cases | Yes, ETAP and PowerFactory survey | Line constants from geometry (S11) deferred; section-level pointers not public |
| Balanced AC load flow | S1, S2, S3, S6, S9, G13 | WP-3.10, WP-3.11, WP-3.17, WP-3.18 | Glover17 ch. 6; Das02 ch. 11 to 13; Kundur94 | MATPOWER case9 to case118; two-bus and three-bus analytical cases; IEEE 4-node feeder | Yes, ETAP and PowerFactory survey | MATPOWER case licence recorded by WP-3.2; nothing else for the method |
| Load-flow controls | S3, S4, S5, S6, S7 | WP-3.12 | Kundur94; Glover17; Sauer06; Das02 ch. 12 | ZIP against pandapower; hand three-node distributed slack | Yes, ETAP and PowerFactory survey | Droop and secondary control deferred; phase-shifter control not a separate WP-3.12 item |
| Topology and islands | S9, G7 | WP-3.13, WP-3.57 | Grainger94; no specific public section recorded | Two-busbar station with a closed and open coupler; island with no source | Yes, ETAP and PowerFactory survey | None for the Phase 3 scope |
| DC power flow, sensitivities and contingency | PW-S1, S15, S16, PW-S2, PW-S3 | WP-3.14, WP-3.15, WP-3.17, WP-3.33 | Grainger94 ch. 14 | MATPOWER case9 to case118 DC; case30 N-1 full AC and screened | Yes, ETAP and PowerFactory survey | PTDF not a separate item; RAS, full transfer refinement and N-2 groups deferred |
| Sequence networks and faults | F1, F2, F6, F8 | WP-3.20, WP-3.29 | Grainger94 ch. 11 to 12; Glover17 9.5; Kasikci02 | WSCC 9-bus with public data; analytical sequence cases | Yes, ETAP and PowerFactory survey | Open-conductor faults and sweeps deferred; Anderson not owned |
| IEC 60909 short circuit | F1, F6 | WP-3.20, WP-3.21 | Kasikci02; Das02 ch. 8; IEC 60909-0:2016; IEC TR 60909-4:2021 | No public benchmark registered; analytical cases only | Yes, ETAP and PowerFactory survey | IEC 60909-0:2016 and IEC TR 60909-4:2021 not owned; c, q and lambda curves wait for them |
| ANSI fault duties | F3, F7 | WP-3.27 | Das02 ch. 5 and 7; Das21; IEEE C37.010 | No public benchmark registered; Das02 examples are private fixtures | Yes, ETAP and PowerFactory survey | IEEE C37.010 and device rating data not owned |
| Motor starting and acceleration | M1, M2, M3, M4, X-4 | WP-3.22 | Das02 sec. 12.10 to 12.11; Fitz03 ch. 6; Krause23; Bose02 | pandapower static motor start; own ODE case | Yes, ETAP and PowerFactory survey | M4 parameter fitting source not owned |
| Harmonics and filters | H1, H2, H3 | WP-3.23, WP-3.24 | Das02 ch. 19 to 20; Arrillaga03 | No public benchmark registered | Yes, ETAP and PowerFactory survey | IEEE 519, IEC 61000-4-15 and measurement standards not owned; flicker (H3) deferred |
| Protection and coordination | P1 to P9 | WP-3.23, WP-3.25 | Alstom11 ch. 9; Das21 ch. 7 and 11; Blackburn06; IEEE C37.112 | No public benchmark registered; Alstom and Das examples are private fixtures | Yes, ETAP and PowerFactory survey | Manufacturer curve data, C37.112 and local mine rules not owned; P6 to P9 deferred |
| Arc flash | A1 to A5 | WP-3.23, WP-3.25 | Das21 ch. 3, 5 and 6 (Table 3.1 is unreliable); DGUV-I 203-077; IEEE 1584-2018; IEEE C2 | DGUV-I 203-077 example 5.1 and 5.8 are private fixtures; no public annex case | Yes, ETAP and PowerFactory survey | IEEE 1584-2018, IEEE C2 and local rules not owned; A3 and A4 deferred |
| Unbalanced three-phase load flow | S10 | WP-3.30 | Das02 ch. 14; Kersting (not owned) | IEEE 4-node and IEEE 13-node feeders | Yes, PowerFactory survey documents the current formulation | Kersting not owned |
| Transient stability | T1 to T6, X-10 | WP-3.31 | Kundur94 ch. 13; Sauer06 ch. 5 to 7; IEEE 421.5; IEC 61400-27 | WSCC 9-bus with public data | Yes, ETAP and PowerFactory survey | IEEE 421.5 and IBR models not owned; user models, EMT, small-signal and wind models deferred |
| Optimal power flow and dispatch | S14, S26, PW-S4 | WP-3.32 | Glover17; Grainger94 ch. 13; Das02 ch. 15 to 16 | MATPOWER case9 and case14 published OPF results | Yes, PowerFactory survey | Unit commitment and reserves are not in WP-3.32; security-constrained dispatch deferred |
| Voltage stability and transfer capability | S17, PW-S3 | WP-3.33 | Kundur94 ch. 14; Sauer06; Ajjarapu (not owned) | Continuation on case9 and case14, no published reference | Yes, PowerFactory survey | Q-limit handling check; Q-V and modal analysis deferred |
| Planning tools | S20, C5 | WP-3.34 | Das02 ch. 9; Gonen88 ch. 10; IEEE 485; IEEE C57.91 | No public benchmark registered | Yes, ETAP survey; PowerFactory partial | IEEE 485 and IEEE C57.91 not owned; other calculators deferred |
| Import, export and interchange | D16 | WP-3.41, WP-3.45 | No book; PSS/E RAW and DYR format specifications | MATPOWER cases; IEEE PES feeders | Yes, PowerFactory DGS and ETAP survey | PSS/E specifications, CIM and CGMES schemas and ETAP interchange not owned |
| Equipment libraries | D11, C1 to C8 | WP-3.42, WP-3.54 | Anders05 ch. 1; Gonen88 ch. 10; IEC 60287; IEEE 738; manufacturer datasheets | No public benchmark; every type needs its source | Yes, ETAP and PowerFactory catalogues; data must be sourced again | Every type needs a source and redistribution permission; IEC 60287, IEEE 738 and IEEE 80 not owned |
| Reports, results and provenance | G11, G13 | WP-3.1, WP-3.7, WP-3.18, WP-3.43, WP-3.57 | Kasikci02 for worked examples; no standard | Golden Markdown and PDF outputs; trace snapshots | Yes, ETAP and PowerFactory survey | Template designer, plots and recovery bin deferred |
| Workbench and workflow | G1 to G10, D3, D4, D6, D12, D13, D14, D18 | WP-3.50 to WP-3.57, WP-3.59 | No book; PowerFactory workflow is in the private survey | Playwright fixtures; case9 built through the UI | Yes, PowerFactory UI and ETAP workflow survey | G2, G3, G4 and G12 deferred; batch automation D15 deferred |
| Verification and benchmark harness | G13, D11, D12 | WP-3.2, WP-3.16, WP-3.19, WP-3.58 to WP-3.61 | All benchmark books and standards named above | MATPOWER cases; IEEE 4-node and 13-node feeders; analytical cases | Yes, ETAP validation list in the private survey | Private fixtures need `QE_REFERENCES`; public CI runs public cases only |

## 4. Phase 3 work package index

Every Phase 3 WP in `PLAN.md` appears once. Track and kind are from the plan; the family
column points to section 3 or to the process row.

| WP | Track | Kind | Family or process |
| --- | --- | --- | --- |
| WP-3.0 | V | Process | Workflow dry run; verification and harness |
| WP-3.1 | E | Core engine | Study preparation, per unit, Ybus; network model |
| WP-3.2 | V | Verification | Verification and benchmark harness |
| WP-3.3 | V | Research index | This map |
| WP-3.4 | D | Contract | Network model, types and topology |
| WP-3.5 | D | Contract | Network model, topology and workbench contracts |
| WP-3.6 | D | Migration | Network model and import |
| WP-3.7 | D | Results service | Reports, results and provenance |
| WP-3.9 | PO | Plan adoption | Process and plan history |
| WP-3.10 | E | Engine | Balanced AC load flow |
| WP-3.11 | E | Engine | Balanced AC load flow |
| WP-3.12 | E | Engine | Load-flow controls |
| WP-3.13 | E | Engine | Topology and islands |
| WP-3.14 | D | Contract | DC power flow, sensitivities and contingency |
| WP-3.15 | E | Engine | DC power flow, sensitivities and contingency |
| WP-3.16 | PM | Audit | Verification and harness |
| WP-3.17 | E | Engine | DC power flow, sensitivities and contingency |
| WP-3.18 | E | Engine and report | Balanced AC load flow; reports |
| WP-3.19 | V | Verification | Verification and benchmark harness |
| WP-3.20 | E | Engine | Sequence networks and faults |
| WP-3.21 | E | Engine | IEC 60909 short circuit |
| WP-3.22 | E | Engine | Motor starting and acceleration |
| WP-3.23 | D | Contract | Harmonics, protection and arc flash |
| WP-3.24 | E | Engine | Harmonics and filters |
| WP-3.25 | E | Engine | Protection and coordination; arc flash |
| WP-3.26 | PM | Audit | Verification and harness |
| WP-3.27 | E | Engine | ANSI fault duties |
| WP-3.28 | U | UI | Workbench and workflow |
| WP-3.29 | V | Verification | Verification and benchmark harness |
| WP-3.30 | E | Engine | Unbalanced three-phase load flow |
| WP-3.31 | E | Engine | Transient stability |
| WP-3.32 | E | Engine | Optimal power flow and dispatch |
| WP-3.33 | E | Engine | Voltage stability and transfer capability |
| WP-3.34 | E | Engine | Planning tools |
| WP-3.35 | PM | Audit | Verification and harness |
| WP-3.36 | PM | Audit | Verification and harness |
| WP-3.40 | none | Superseded | Workbench and workflow; replaced by WP-3.50 to WP-3.59 |
| WP-3.41 | D | Import | Import, export and interchange |
| WP-3.42 | D | Libraries | Equipment libraries |
| WP-3.43 | D | Report | Reports, results and provenance |
| WP-3.44 | PM | Audit | Verification and harness |
| WP-3.45 | D | Import | Import, export and interchange |
| WP-3.49 | D | API | Network model; reports, results and provenance |
| WP-3.50 | U | UI | Workbench and workflow |
| WP-3.51 | U | UI | Workbench and workflow |
| WP-3.52 | U | UI | Workbench and workflow |
| WP-3.53 | U | UI | Workbench and workflow |
| WP-3.54 | U | UI and libraries | Equipment libraries; workbench |
| WP-3.55 | U | UI | Workbench and workflow |
| WP-3.56 | U | UI | Workbench and workflow |
| WP-3.57 | U | UI and results | Workbench; reports, results and provenance |
| WP-3.58 | V | Verification | Verification and benchmark harness |
| WP-3.59 | PM | Audit and retirement | Verification and harness |
| WP-3.60 | PO | Plan refresh | Process and plan history |
| WP-3.61 | PM | Release | Verification and harness |

## 5. Parity row disposition

Each row of [parity-matrix.md](parity-matrix.md) appears once. A deferred row is not
cancelled; it is outside the first Phase 3 batch and needs a later WP or a milestone
expansion.

### 5.1 Platform and data

| Row | Disposition | Coverage | Note |
| --- | --- | --- | --- |
| D1 | WP-3.4, WP-3.7, WP-3.49 | partial | Network v1 containers, result store and API; one database for every study not yet proven |
| D2 | WP-3.4, WP-3.42, WP-3.54 | full | Type and element split, libraries and library UI |
| D3 | WP-3.5, WP-3.51 | full | Diagrams separate from topology |
| D4 | WP-3.4, WP-3.7, WP-3.55 | full | Operating scenarios as overlays |
| D5 | Deferred | none | Revisions, variations and expansion stages have no Phase 3 WP |
| D6 | WP-3.5, WP-3.55 | full | Study cases and command options |
| D7 | Deferred | none | Loading categories and diversity are not in WP-3.12 |
| D8 | Deferred | none | Time characteristics and profiles are not in Phase 3 |
| D9 | Deferred | none | Versions, derived projects, merge and multi-user |
| D10 | Deferred | none | User-defined attributes |
| D11 | WP-3.42, WP-3.54 | partial | Library mechanism; manufacturer data needs sources and permissions |
| D12 | WP-3.4, WP-3.52, WP-3.53, WP-3.56 | full | Named validation diagnostics and jump to element |
| D13 | WP-3.51 | partial | Diagram undo and redo; recovery bin deferred |
| D14 | WP-3.49 | partial | REST API; Python scripting surface stays CLI |
| D15 | Deferred | none | Batch study automation has no Phase 3 WP |
| D16 | WP-3.41, WP-3.45 | partial | PSS/E RAW and PowerFactory DGS; CIM and CGMES deferred |
| D17 | Deferred | none | GIS views and import |
| D18 | WP-3.50 | partial | Panel and toolbar preferences; group profiles deferred |

### 5.2 Diagram and results

| Row | Disposition | Coverage | Note |
| --- | --- | --- | --- |
| G1 | WP-3.51 | full | Single-line editor with IEC symbols |
| G2 | Deferred | none | Detailed bay and simplified views |
| G3 | Deferred | none | Auto layout |
| G4 | Deferred | none | Composite and nested networks |
| G5 | WP-3.57 | full | Result boxes on the diagram |
| G6 | WP-3.57 | full | Colouring and contouring by results |
| G7 | WP-3.13, WP-3.57 | full | Island computation and continuity colouring |
| G8 | WP-3.53 | full | Data Manager grid |
| G9 | WP-3.18, WP-3.57 | partial | Violation report and colour bands; marginal and critical alert tiers not explicit |
| G10 | WP-3.57 | full | Compare two runs |
| G11 | WP-3.43 | partial | Markdown and PDF reports; template designer deferred |
| G12 | Deferred | none | Plots for time series, TCC, R-X, spectra and eigenvalues |
| G13 | WP-3.1, WP-3.10, WP-3.18, WP-3.43 | full | Worked trace extended from the Phase 2 capability |

### 5.3 Steady state

| Row | Disposition | Coverage | Note |
| --- | --- | --- | --- |
| S1 | WP-3.10 | full | Newton-Raphson |
| S2 | WP-3.11 | full | Gauss-Seidel and fast decoupled |
| S3 | WP-3.10 | full | Q limits and PV to PQ switching |
| S4 | WP-3.12 | full | Taps, shunts and remote voltage |
| S5 | WP-3.1, WP-3.12 | partial | Phase-shifter stamp; phase-shifter control is not a separate item |
| S6 | WP-3.12 | partial | Distributed slack by generation; droop and secondary control deferred |
| S7 | WP-3.12 | full | ZIP and exponential loads |
| S8 | Deferred | none | Temperature correction of resistance |
| S9 | WP-3.13 | full | Several islands, each with a source |
| S10 | WP-3.30 | full | Unbalanced three-phase load flow |
| S11 | Deferred | none | Line constants from geometry and mutual coupling |
| S12 | Deferred | none | Physical DC networks with batteries and chargers; PW-S1 is separate |
| S13 | Deferred | none | Time-series and quasi-dynamic load flow |
| S14 | WP-3.32 | full | Optimal power flow |
| S15 | WP-3.14, WP-3.15 | full | Contingency analysis |
| S16 | WP-3.15 | partial | LODF screening; PTDF is not a separate item |
| S17 | WP-3.33 | partial | Continuation P-V; Q-V and modal analysis deferred |
| S18 | Deferred | none | State estimation; Abur is not owned |
| S19 | Deferred | none | Hosting capacity |
| S20 | WP-3.34 | full | Capacitor placement |
| S21 | Deferred | none | Switching, tie-point optimisation and phase balancing |
| S22 | Deferred | none | Probabilistic load flow |
| S23 | Deferred | none | Reliability indices; Billinton and Allan are not owned |
| S24 | Deferred | none | Network reduction |
| S25 | Deferred | none | Load allocation from meters |
| S26 | Deferred | none | Unit commitment and economic dispatch; WP-3.32 is OPF only |

### 5.4 Faults

| Row | Disposition | Coverage | Note |
| --- | --- | --- | --- |
| F1 | WP-3.20, WP-3.21 | full | IEC 60909 quantities |
| F2 | WP-3.20 | full | Unbalanced faults |
| F3 | WP-3.27 | full | ANSI duty |
| F4 | Deferred | none | IEC 61363 transient decay is not in WP-3.21 |
| F5 | Deferred | none | DC faults |
| F6 | WP-3.20 | partial | Superposition from a load-flow result is not an explicit item |
| F7 | WP-3.27, WP-3.42 | partial | Duty checks and library ratings; the full device workflow is open |
| F8 | WP-3.20 | partial | Multiple faults and open conductors are not explicit; sweeps deferred |

### 5.5 Protection and arc flash

| Row | Disposition | Coverage | Note |
| --- | --- | --- | --- |
| P1 | WP-3.25, WP-3.42 | partial | Curves and device data; TCC plotting deferred with G12 |
| P2 | WP-3.25 | partial | Damage curves |
| P3 | WP-3.25 | full | Coordination checks |
| P4 | WP-3.25 | partial | Sequence of operation and backup logic |
| P5 | WP-3.25 | partial | Automatic setting calculation |
| P6 | Deferred | none | Distance protection |
| P7 | Deferred | none | Differential protection |
| P8 | Deferred | none | CT and VT models with saturation |
| P9 | Deferred | none | Design, as-found and maintenance states |
| A1 | WP-3.25 | full | IEEE 1584-2018 method |
| A2 | WP-3.25 | partial | Labels and work-permit workflow |
| A3 | Deferred | none | DC arc flash |
| A4 | Deferred | none | HV arc flash above 15 kV |
| A5 | WP-3.25 | partial | Integrated energy with changing current |

### 5.6 Machines, dynamics and power quality

| Row | Disposition | Coverage | Note |
| --- | --- | --- | --- |
| M1 | WP-3.22 | full | Static motor start |
| M2 | WP-3.22 | full | Dynamic acceleration |
| M3 | WP-3.22 | full | Starter types |
| M4 | Deferred | none | Motor parameter fitting from datasheet |
| T1 | WP-3.31 | full | RMS transient stability |
| T2 | Deferred | none | User-defined dynamic models |
| T3 | Deferred | none | Small-signal eigenvalue analysis |
| T4 | Deferred | none | EMT simulation |
| T5 | WP-3.31 | partial | Generic events; load shedding and fast transfer not explicit |
| T6 | WP-3.31 | partial | Initialisation checks |
| H1 | WP-3.24 | full | Harmonic load flow and frequency scan |
| H2 | WP-3.24 | partial | Harmonic flow and filter support; IEEE 519 limits are user data |
| H3 | Deferred | none | Flicker |

### 5.7 Design calculators

| Row | Disposition | Coverage | Note |
| --- | --- | --- | --- |
| C1 | Deferred | none | Cable sizing |
| C2 | Deferred | none | Cable ampacity |
| C3 | Deferred | none | Cable pulling and tension |
| C4 | Deferred | none | Transformer sizing |
| C5 | WP-3.34 | full | Battery sizing |
| C6 | Deferred | none | Ground grid |
| C7 | Deferred | none | Panel schedules |
| C8 | Deferred | none | Line sag and tension |

### 5.8 Product-specific and cross-cutting distinctions

| Row | Disposition | Coverage | Note |
| --- | --- | --- | --- |
| PW-D1 | Deferred | none | Topology consolidation with planning and operations identity |
| PW-S1 | WP-3.17 | full | Linear DC approximation kept separate from HVDC |
| PW-S2 | WP-3.15 | partial | Contingency reference states; reusable RAS deferred |
| PW-S3 | WP-3.33 | partial | Transfer capability; full-contingency refinement deferred |
| PW-S4 | WP-3.32 | partial | OPF; security-constrained dispatch and reserves deferred |
| PW-S5 | Deferred | none | Geomagnetically induced current |
| PW-T1 | Deferred | none | SMIB eigenvalue check |
| PW-X1 | Deferred | none | Distributed independent study jobs |
| X-1 | Deferred | none | EMT and RMS co-simulation |
| X-2 | Deferred | none | EMT measurement quantities |
| X-3 | Deferred | none | Impedance-based stability of inverter-based resources |
| X-4 | Deferred | none | Dynamic model parameter identification |
| X-5 | Deferred | none | Techno-economic comparison |
| X-6 | Deferred | none | Real-time PMS and ADMS |
| X-7 | Deferred | none | Transformer inrush |
| X-8 | Deferred | none | DC control circuit diagram |
| X-9 | Deferred | none | Railway traction power |
| X-10 | Deferred | none | Wind turbine generator models |

## 6. Gaps and follow-ups

1. **Private reading map pointers are not reproduced.** This run had no
   `QE_REFERENCES`. The family table names the books and standards that the public
   research records, and keeps the exact chapter and page pointers in the private
   reading map. Where the public research names a book without a section, the table
   says so. The PM can add the section pointers from the private map before the
   milestone audit.
2. **Private fixtures are not available in public CI.** WP-3.2 and WP-3.19 load them
   through `QE_REFERENCES` and skip with a visible message when the variable is absent.
3. **Paid standards remain gaps per D18.** IEC 60909-0, IEC TR 60909-4, IEEE 1584-2018,
   IEEE C37.010, IEEE 485, IEEE 80, IEEE 519, IEEE 738, IEC 60287, IEC 61363, IEC 61660,
   IEEE 946 and IEEE 421.5 are not owned. The methods can be built; certification-grade
   constants and cases wait for the purchase list in
   [../acquisition-list.md](../acquisition-list.md).
4. **Deferred rows need later WPs.** Section 5 lists 55 deferred parity rows. The
   largest groups are design calculators (C1 to C4 and C6 to C8), advanced dynamics
   (T2 to T4, X-1 to X-10), planning and operations (S18 to S26, PW-D1, PW-S5, PW-T1,
   PW-X1) and the remaining protection models (P6 to P9). WP-3.60 expands M3.2 onward
   after the M3.1 audit and a research refresh.
5. **Coverage is not parity.** A `full` label means the WP is written to cover the row.
   It is not evidence that the built engine matches a reference product. The milestone
   audits and the benchmark harness decide that.
