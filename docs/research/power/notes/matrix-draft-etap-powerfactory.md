# Draft capability matrix: ETAP and PowerFactory (WP-2.10 working note)

This is a draft. WP-2.12 merges it with ChatGPT's PowerWorld dossier into
`parity-matrix.md`.

**Cell values:** `yes` (the source states it), `module` (a separately licensed add-on),
`?` (not found yet). Sources are in `etap.md` and `powerfactory.md`.

**Quantic status** reflects main as of 2026-10-15:
- balanced load flow with Q-limit handling (pandapower);
- IEC 60909 three-phase short circuit with worked traces;
- static motor-start voltage dip;
- a basic single-line editor;
- JSON contracts, CLI, API, and Markdown and PDF reports.

## Platform and data

| ID | Capability | ETAP | PowerFactory | Quantic | Verifying source |
|---|---|---|---|---|---|
| D1 | One project database shared by all studies | yes | yes | partial (manifest + model files) | - |
| D2 | Element and type split (shared type data, library types) | yes (library Quick Pick) | yes (element vs type objects) | none | - |
| D3 | Multiple diagrams/presentations of the same network | yes (presentations) | yes (many diagrams per element) | none | - |
| D4 | Operating states separate from network (switching, dispatch, loading) | yes (configurations) | yes (operation scenarios) | none | - |
| D5 | Engineering alternatives and timeline (revisions; variations with expansion stages) | yes (revision data) | yes (variations, stages, Gantt) | none | - |
| D6 | Study cases holding calculation options | yes | yes | partial (request files) | - |
| D7 | Loading categories and diversity or demand factors | yes | partial (scaling, characteristics) | none | Das 2002 |
| D8 | Time characteristics and profiles on any parameter | yes (time-domain LF) | yes | none | - |
| D9 | Versions, derived projects, compare and merge, multi-user | yes (NetPM) | yes (team edition) | partial (git) | - |
| D10 | User data extension (custom attributes) | yes (user fields) | yes | none | - |
| D11 | Engineering libraries from manufacturer data | yes (140,000+ models stated) | yes | none | - |
| D12 | Pre-run data checking with jump to faulty element | yes (error viewer, 5 levels) | yes (output window) | partial (diagnostics with element and field) | - |
| D13 | Undo, recovery bin | yes (dumpster) | yes (database rollback) | none | - |
| D14 | Scripting API (Python) | yes (etapPy) | yes (Python, DPL, C++) | partial (CLI and REST API) | - |
| D15 | Batch study automation (scenario and study wizards; task automation) | yes | yes | none | - |
| D16 | Import PSS/E RAW, CIM/CGMES, other tools | partial (CIM via ArcFM, SKM) | yes (PSS/E, CGMES, UCTE, NEPLAN and more) | none | - |
| D17 | GIS views and import | yes | yes | none | - |
| D18 | Interface profiles and customisable toolbars | yes (themes) | yes (profiles) | none | - |

## Diagram and results

| ID | Capability | ETAP | PowerFactory | Quantic | Source |
|---|---|---|---|---|---|
| G1 | Single-line editor with palettes, auto connect, IEC or ANSI symbols | yes | yes | partial | - |
| G2 | Detailed substation (bays, breakers) and simplified views | yes | yes (three detail levels) | none | - |
| G3 | Auto layout from data (feeders, neighbourhood) | yes (auto-build) | yes (layout tool) | none | - |
| G4 | Composite networks (nesting) | yes | yes (composite models) | none | - |
| G5 | Result boxes or datablocks on the diagram | yes | yes | none | - |
| G6 | Colouring and contouring by results, heatmap | yes | yes | none | - |
| G7 | Continuity and island colouring | yes | yes (isolated areas) | none | - |
| G8 | Spreadsheet view of all elements and results | yes (Network Manager 2026) | yes (Network Model Manager) | none | - |
| G9 | Alert view with marginal and critical limits | yes | yes (colouring and reports) | none | - |
| G10 | Result analyzer comparing cases and baselines | yes | yes (comparison mode) | none | - |
| G11 | Report generator with templates and export (PDF, Word, Excel) | yes (Crystal) | yes (report designer) | partial (Markdown, PDF) | - |
| G12 | Plots: time series, TCC, R-X, spectra, eigenvalues | yes | yes | none | - |
| G13 | Worked equations shown in reports | no evidence | no evidence | **done (D11)** | Kasikci 2002 |

## Steady state

| ID | Capability | ETAP | PowerFactory | Quantic | Verifying book |
|---|---|---|---|---|---|
| S1 | Balanced AC load flow (NR) | yes | yes | done | Glover 2017, Grainger 1994 |
| S2 | Gauss-Seidel and fast decoupled methods | yes | ? (NR only stated) | none | Glover 2017 |
| S3 | Generator Q limits and PV to PQ switching | yes | yes (capability curves) | done | Glover 2017 |
| S4 | LTC and regulator control (local, remote bus) | yes | yes | none | Kundur 1994, Glover 2017 |
| S5 | Phase-shifting transformers | yes | yes | none | Grainger 1994 |
| S6 | Station or distributed slack, droop, primary and secondary control | partial | yes | none | Kundur 1994 |
| S7 | Voltage-dependent loads (ZIP, exponential) | yes | yes | none | Sauer 2006, Kundur 1994 |
| S8 | Temperature correction of conductor R | yes | yes | none | Anders 2005 |
| S9 | Multiple islands, each with its own slack | yes | yes | ? | - |
| S10 | Unbalanced three-phase load flow (1, 2, 3 phase; 3 and 4 wire) | module | yes | none | **gap: Kersting** |
| S11 | Line constants from geometry, mutual coupling | yes | yes | none | Grainger 1994, Arrillaga 2003 |
| S12 | DC load flow (batteries, chargers) and AC/DC unified | yes | yes | none | - |
| S13 | Time-series and quasi-dynamic load flow | module | module | none | - |
| S14 | Optimal power flow (AC interior point) | module | module | none | Glover 2017, Das 2002 |
| S15 | Contingency analysis (N-1, N-2, screening, RAS) | module | module | none | Grainger 1994 |
| S16 | Sensitivities and distribution factors (PTDF, LODF) | ? | yes | none | Grainger 1994 |
| S17 | Voltage stability P-V and Q-V, modal | module | module | none | Kundur 1994 |
| S18 | State estimation | yes (ADMS) | module | none | Grainger 1994; gap Abur |
| S19 | Hosting capacity | yes (2026) | module | none | - |
| S20 | Optimal capacitor placement | module | module | none | - |
| S21 | Switching and tie-point optimisation, phase balancing | module | module | none | - |
| S22 | Probabilistic load flow | ? | module | none | - |
| S23 | Reliability indices and restoration | module | module | none | Glover 2017 (thin); gap Billinton |
| S24 | Network reduction (Ward, REI) | ? | module | none | - |
| S25 | Load allocation from meters | yes | yes (feeder scaling) | none | - |
| S26 | Unit commitment and economic dispatch | yes (GMS) | module | none | Glover 2017, Grainger 1994 |

## Faults and protection

| ID | Capability | ETAP | PowerFactory | Quantic | Verifying book |
|---|---|---|---|---|---|
| F1 | IEC 60909 three-phase with ip, Ith, Ib, Ik | yes | yes | partial (Ik'', ip, Ith) | Kasikci 2002 |
| F2 | Unbalanced faults (SLG, LL, LLG) | yes | yes | none | Grainger 1994, Glover 2017 |
| F3 | ANSI C37 three networks, X/R multipliers, duty | yes | yes | none | Das 2002, Das 2021; spec in engine-ansi-short-circuit.md; gap C37.010 local curves |
| F4 | IEC 61363 transient decay | yes | yes | none | - |
| F5 | DC faults (IEC 61660, IEEE 946) | yes | yes | none | Das 2002 ch. 9; spec in engine-dc-short-circuit.md; gap IEC 61660 curves |
| F6 | Complete (superposition) method on load flow | ? | yes | none | Kasikci 2002 |
| F7 | Device duty against library ratings | yes | partial | none | Das 2002, Das 2021 (LV test X/R) |
| F8 | Multiple and open-conductor faults, fault sweeps | partial | yes | none | Grainger 1994 |
| P1 | TCC plotting with device libraries | yes | yes | none | Alstom 2011, Das 2021; spec in engine-protection-tcc.md; pandapower protection as base |
| P2 | Damage curves (cable, transformer, motor start) | ? | yes | none | Alstom 2011 |
| P3 | Automatic coordination checks or audit by rules | yes | yes | none | Alstom 2011 |
| P4 | Sequence of operation with animation and backup | yes | yes (short-circuit trace) | none | Blackburn 2006 |
| P5 | Automatic setting calculation | ? | yes | none | Alstom 2011 |
| P6 | Distance protection, R-X, zones | module | module | none | Alstom 2011, Blackburn 2006 |
| P7 | Differential protection | yes | yes | none | Alstom 2011 |
| P8 | CT and VT models with saturation | yes | yes | none | Alstom 2011 |
| A1 | Arc flash IEEE 1584-2018 with auto clearing time | module | module | none | Das 2021; spec in engine-arc-flash.md; candidate engine arcflash (MIT) |
| A2 | Arc flash labels and work permits | yes | yes (labels) | none | Das 2021 |
| A3 | DC arc flash | yes | yes | none | Das 2021 |
| A4 | HV arc flash (above 15 kV) | yes | ? | none | Das 2021 |

## Dynamics and power quality

| ID | Capability | ETAP | PowerFactory | Quantic | Verifying book |
|---|---|---|---|---|---|
| M1 | Static motor start (voltage dip) | yes | yes | partial | Das 2002 |
| M2 | Dynamic motor acceleration with torque-speed models | yes | yes | none | Das 2002, Fitzgerald 2003, Krause 2023; spec in engine-motors.md |
| M3 | Starters: autotransformer, star-delta, reactor, resistor, capacitor, soft starter, VFD | yes | yes (most) | none | Bose 2002, Krause 2023 |
| M4 | Motor parameter estimation from datasheet | yes | yes | none | Krause 2023, Fitzgerald 2003 |
| T1 | RMS transient stability with machines, exciters, governors, PSS | module | module | none | Kundur 1994, Sauer 2006; spec in engine-transient-stability.md |
| T2 | User-defined dynamic models (block diagrams) | yes (UDM) | yes (DSL, Modelica) | none | Ogata 2002 |
| T3 | Small-signal eigenvalue analysis | ? | module | none | Kundur 1994 |
| T4 | EMT simulation | module (PSCAD engine) | module | none | Das 2010 |
| T5 | Load shedding, fast bus transfer, generator start | yes | yes | none | Kundur 1994 |
| H1 | Harmonic load flow and frequency scan | module | module | none | Das 2002 ch. 19 and 20, Arrillaga 2003; spec in engine-harmonics.md; base OpenDSS harmonic mode |
| H2 | Filter design and IEEE 519 or IEC 61000 limits | yes | yes | none | Arrillaga 2003, Das 2010 |
| H3 | Flicker | yes (2026) | yes | none | - |

## Design calculators

| ID | Capability | ETAP | PowerFactory | Quantic | Verifying book |
|---|---|---|---|---|---|
| C1 | Cable sizing (ampacity, drop, short circuit, motor start) to many standards | yes | module | none | Anders 2005, Morley |
| C2 | Cable ampacity Neher-McGrath and IEC 60287, duct banks | module | module | none | Anders 2005; spec in engine-cables.md; no permissive library, implement |
| C3 | Cable pulling and tension | module | ? | none | - |
| C4 | Transformer sizing | module | ? | none | - |
| C5 | Battery sizing (IEEE 485) and discharge | module | ? | none | **gap** |
| C6 | Ground grid (IEEE 80, FEM, soil model) | module | ? | none | Das 2010 (partial) |
| C7 | Panel schedules (NEC demand) | module | ? | none | - |
| C8 | Line sag, tension and ampacity (IEEE 738) | module | ? | none | Gonen 1988; candidate linerate (licence to check) |
