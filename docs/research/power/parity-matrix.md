# Power parity matrix

WP-2.12, Claude, 2026-10-17. Research synthesis, not a build order and not a claim of
parity. It merges the ETAP and PowerFactory dossiers (WP-2.10), the PowerWorld dossier
(WP-2.11), the EasyPower, SKM, NEPLAN and PSS/E dossier (WP-2.13) and the reconstruction
requirements (WP-2.14). The engine inventory is in [engines.md](engines.md).

## How to read it

**Evidence class (Peter, 2026-10-17).** Every product cell starts with one class:

- **S** seen: stated in a cited primary source or observed in the product. The words
  after the class qualify it: `yes`, `mod` (separately licensed or packaged module) or
  `part` (narrower than the row's full wording).
- **I** inferred: our reasoning from cited evidence.
- **U** unknown: not established by any source read. **Unknown is not absent.** A U cell
  never means the product lacks the feature.

No product cell is I: every inference was kept out of the product columns and lives in
the engine inventory, the Quantic column and the WP-2.14 requirements, where it is
labelled. This keeps the product columns to what a source says.

**Citations.** Bracketed IDs resolve in each dossier's source table: E (ETAP) in
[notes/etap-sources.md](notes/etap-sources.md), P (PowerFactory) in
[notes/powerfactory-sources.md](notes/powerfactory-sources.md), W in
[powerworld.md](powerworld.md) section 2, and EP, SK, NP, PS in
[other-products.md](other-products.md). WP-2.18 audited all 199 previously S cells in
the ETAP/PowerFactory columns and attached cell-level E/P IDs. The 198 retained S
cells each name an indexed primary source. New E113/E114 resolve in the
[WP-2.18 source entry](../../sources/entries/power-matrix-cell-audit-2026-10-17.yaml),
which also records rechecks and scope qualifications. In product cells P numbers
are PowerFactory sources; in the ID column P rows are protection. A citation
supports only the cell's stated subset, not every word of a broad capability row.

**Quantic now** is the state of `main` on 2026-10-17: balanced load flow with
reactive limits, IEC 60909 three-phase short circuit with worked traces, static motor
start, a generic diagram canvas, JSON contracts, CLI, REST API and Markdown and PDF
reports. Building is paused for research (Peter, 2026-10-15).

**Owned book** names the book in `Pietrols/QE-References` that will verify the row
(short names as in [notes/engines-library-map.md](notes/engines-library-map.md)). A
`gap` names a source we do not own. Book errata found so far are in
[notes/engine-index.md](notes/engine-index.md); never key constants from a flagged
table.

**R-IDs** link each row to the requirements in
[reconstruction-requirements.md](reconstruction-requirements.md). Matrix D11 means
manufacturer libraries; PLAN decision D11 (show your working) is row G13.

## Summary

118 rows, 826 product cells: S 511, I 0, U 315.

| Product | S cells | U cells |
| --- | ---: | ---: |
| ETAP | 99 | 19 |
| PowerFactory | 99 | 19 |
| PowerWorld | 68 | 50 |
| EasyPower | 60 | 58 |
| SKM | 61 | 57 |
| NEPLAN | 91 | 27 |
| PSS/E | 33 | 85 |

Reading the counts: ETAP and PowerFactory have the most S cells because they were
researched first and longest, not only because they do more. PSS/E and SKM U cells
mostly mean "not in the sources read". For PSS/E that is expected (our reading, class
I): it is a transmission planning tool, so industrial rows such as arc flash, cables
and TCC sit outside its market.

**Quantic against the field.** Of 118 rows, Quantic has 3 done (S1, S3, G13),
10 partial, 1 untested and 104 not started. Every competitor covers far more. The one
row where Quantic may be ahead is G13: no product's public material read so far shows
worked equations with substituted values (U for all seven, which is not proof they
lack it). It is our clearest candidate differentiator, alongside the mining focus and
price (see the engine inventory). WP-2.15 comparison runs can test it.

**Rows that decide the Copperbelt market (P0 in WP-2.14).** Motor starting (M1 to M4),
faults (F1, F2, F7), protection (P1 to P5, P9), arc flash (A1 to A5), drive harmonics
(H1, H2), grounding (C6) and islanded generation (S6, S9, T1, T5). ETAP, EasyPower and
SKM are seen on most of them; PowerWorld and PSS/E on few. The industrial
competitors, not PowerWorld, are the bar for these rows.

**New distinctions this synthesis adds.** P9 (design versus as-found and maintenance
settings, from SKM and EasyPower), A5 (arc energy integrated over a changing current,
seen in EasyPower, partly in ETAP and SKM), T6 (dynamic initialisation diagnostics) and the X rows for
product-specific capabilities that had no shared ID.

## Platform and data

| ID | Capability | ETAP | PowerFactory | PowerWorld | EasyPower | SKM | NEPLAN | PSS/E | Quantic now | Owned book to verify | Requirement R-IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | One project database shared by all studies | S yes [E25][E34] | S yes [P6] | S yes [W8][W10] | S yes [EP4] | S yes [SK18] | S yes [NP5] | S part, linked network and module data [PS3][PS8] | partial (manifest and model files; CC-3 asset identity) | - | R-001 |
| D2 | Element and type split (shared type data, library types) | S part, libraries/Quick Pick; shared type-instance semantics U [E27] | S yes (element and type objects) [P5][P39] | S part, conductor, tower and model types [W96][W92] | S part, libraries; type split U [EP1] | S part, device libraries; type split U [SK5] | S yes [NP6] | S part, dynamic categories [PS4] | none | - | R-002 |
| D3 | Several diagrams of the same network | S yes (presentations) [E34] | S yes [P8][P35] | S yes [W9] | U | S yes, new one-lines from shared components [SK30] | S yes, multiple diagrams of shared elements [NP24] | U | none | - | R-001 |
| D4 | Operating states separate from the network (switching, dispatch, loading) | S yes (configurations) [E34] | S yes (operation scenarios) [P6] | S part, case and reference states [W12][W77] | S yes, ScenarioManager [EP5] | S part, study setups [SK18] | S yes, operating states [NP5] | S part, study automation [PS3] | none | - | R-003, R-030, R-046 |
| D5 | Engineering alternatives and timeline (revisions, expansion stages) | S yes (revision data) [E34][E26] | S yes (variations, stages) [P6] | S part, scheduled actions only [W77] | S part, revision breadth qualified [EP5] | U | S yes, variant tree [NP5] | U | none | - | R-003 |
| D6 | Study cases holding calculation options | S yes [E6][E34] | S yes [P6] | S yes [W10][W62] | S yes [EP5] | S yes [SK18] | S yes [NP5] | S part [PS3] | partial (request files) | - | R-003, R-042 |
| D7 | Loading categories, diversity and demand factors | S yes [E7][E35] | S part (scaling, characteristics) [P3][P59] | U (ZIP and scaling are narrower) [W22] | S part, load scaling/diversity; category breadth U [EP24] | S part, demand/design load analysis; diversity breadth U [SK27] | S part, predefined/user scaling; diversity categories U [NP7] | U | none | Das02 | R-003 |
| D8 | Time characteristics and profiles on any parameter | S part, time-domain profiles; arbitrary parameter scope U [E71] | S yes [P5][P16] | S part, time-step and weather data [W74][W75] | U | U | S part, synthetic profiles and timed network state; arbitrary fields U [NP4][NP5] | U | none | - | R-003 |
| D9 | Versions, derived projects, compare and merge, multi-user | S part, multi-user change control; derived-project merge breadth U [E25] | S yes (team edition) [P6][P36] | S part, case comparison [W12] | U | S part, project merging and multi-user; derived hierarchy U [SK27] | S yes, deployment-dependent [NP21] | U | partial (git) | - | R-005 |
| D10 | User data extension (custom attributes) | S part, protection user fields; general schema extension U [E15] | S yes [P6][P24] | S yes [W18] | U | S yes, user-defined fields [SK27] | U | U | none | - | R-002 |
| D11 | Engineering libraries from manufacturer data | S yes, vendor states 140,000+ models and sizes [E61] | S yes [P11][P5] | S part, coverage U [W96][W92] | S yes, manufacturer libraries [EP1] | S yes [SK5] | S yes [NP6] | S part, breadth U [PS4] | none | - | R-002, R-016, R-026, R-041 |
| D12 | Pre-run data checking with jump to the faulty element | S yes (error viewer) [E34] | S part, diagnostic output; jump-to-element behavior U [P9][P34] | S yes [W13][W61] | S yes [EP3][EP16] | S part [SK18] | S yes [NP5] | S part, dynamic data [PS4] | partial (diagnostics name element and field) | - | R-002, R-006, R-016, R-017, R-018, R-037, R-038, R-043, R-045, R-052 |
| D13 | Undo and recovery bin | S yes [E34] | S yes (database rollback) [P6] | S part, graphical undo [W14][W15] | S part, multistep undo; recovery-bin scope U [EP31] | S part, one-line undo; recovery bin U [SK28] | U | U | none | - | R-005 |
| D14 | Scripting API (Python) | S yes (etapPy) [E46] | S yes (Python, DPL, C++) [P24][P47] | S mod SimAuto (COM) and AUX [W6][W94] | U | U | S yes, Python and C# [NP20] | S yes, Python and IPLAN [PS3] | partial (CLI and REST API) | - | R-005 |
| D15 | Batch study automation | S yes [E34][E46] | S yes [P24] | S yes [W94][W74][W73] | U | U | S yes, web services [NP20] | S yes [PS3] | none | - | R-005, R-041 |
| D16 | Import PSS/E RAW, CIM/CGMES and other tools | S part (CIM via ArcFM, SKM) [E45][E26] | S yes (PSS/E, CGMES 2.4.15 and 3.0.0 [P61], UCTE, NEPLAN) [P25] | S yes RAW, EPC, dynamic formats; CGMES U [W10][W65] | S part, Revit; RAW and CGMES U [EP15] | S part, SPEL bidirectional exchange; RAW/CGMES U [SK31] | S yes, RAW, SEQ, DYR [NP15] | S yes, RAW and DYR [PS8] | none | - | R-037, R-038, R-039, R-040, R-041 |
| D17 | GIS views and import | S yes [E25][E45] | S yes (one way, GIS to PF [P62]) | S yes, geographic views [W93] | U | U | S yes [NP3] | U | none | - | R-036 |
| D18 | Interface profiles and customisable toolbars | S part, themes/tool managers; group profiles U [E61] | S yes (profiles, user groups [P58]) | S part [W8][W86] | S part, tab/tool options; group profiles U [EP3] | U | U | U | none | - | R-055 |

## Diagram and results

| ID | Capability | ETAP | PowerFactory | PowerWorld | EasyPower | SKM | NEPLAN | PSS/E | Quantic now | Owned book to verify | Requirement R-IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 | Single-line editor with palettes, auto connect, IEC or ANSI symbols | S yes [E34][E44] | S yes [P8] | S yes; symbol standards U [W9][W79] | S yes [EP4] | S yes [SK18] | S yes [NP3] | S part [PS2] | partial (generic canvas, WP-1.6) | - | R-001 |
| G2 | Detailed substation (bays, breakers) and simplified views | S yes [E25][E30] | S yes (three detail levels) [P8][P35] | S mod ITP [W71][W72][W81] | U | U | S yes, detailed stations and bays [NP24][NP4] | U | none | - | R-001, R-004 |
| G3 | Auto layout from data | S yes (auto-build) [E26][E61] | S yes [P8][P35] | S yes [W81][W93] | S yes, auto layout (2026) [EP3] | U | U | U | none | - | R-056 |
| G4 | Composite networks (nesting) | S yes [E25][E34] | S yes [P8] | U [W58] | U | U | S part, hierarchical substations; arbitrary composite semantics U [NP4] | U | none | - | R-057 |
| G5 | Result boxes on the diagram | S yes [E34][E44] | S yes [P34] | S yes [W91][W79] | S yes [EP4] | S yes [SK18] | S yes [NP3] | S part [PS2] | none | - | R-044 |
| G6 | Colouring and contouring by results | S yes [E44][E7] | S yes [P8] | S yes [W78][W93] | S part, voltage/overload highlighting; contour breadth U [EP24] | S part, arc-flash result coloring (V8) [SK33] | S yes, result ranges and overload coloring [NP24] | U | none | - | R-045 |
| G7 | Continuity and island colouring | S yes [E34] | S yes [P41][P8] | S part [W33][W104] | S part, isolated-subsystem display [EP26] | U | S yes, islands and unsupplied network coloring [NP24] | U | none | - | R-004 |
| G8 | Spreadsheet view of all elements and results | S yes (Network Manager 2026) [E26] | S yes (Network Model Manager) [P6][P34] | S yes [W8] | S part, editable database spreadsheet; full result breadth U [EP27] | S yes, Data Visualizer inputs/results across scenarios [SK29] | S yes, table-oriented Data Manager [NP5] | U | none | - | R-058 |
| G9 | Alert view with marginal and critical limits | S yes [E53][E7] | S part, limit-violation display; marginal/critical tiers U [P34] | S yes; tier conventions U [W35] | S yes [EP16] | S yes [SK18] | S yes [NP7] | S part [PS4] | none | - | R-045 |
| G10 | Result analyzer comparing cases and baselines | S yes [E51] | S yes (comparison mode) [P9] | S yes [W12] | U | S yes, Data Visualizer scenario comparison [SK29][SK30] | S yes, result/variant comparison [NP5] | U | none | - | R-003, R-039, R-046, R-049 |
| G11 | Report generator with templates and export | S yes (Crystal) [E34][E37] | S yes (report designer) [P9][P34] | S part, AUX and spreadsheet export [W53][W94] | S yes; breadth qualified [EP16] | S yes [SK18] | S yes [NP7] | S part [PS2] | partial (Markdown and PDF, WP-1.7) | - | R-042, R-045, R-046, R-052 |
| G12 | Plots: time series, TCC, R-X, spectra, eigenvalues | S part, time, TCC, R-X, spectra; eigenvalue plots U [E5][E16][E30] | S yes [P9][P11][P14][P27] | S part, PV/QV, transient and modal [W50][W62][W89] | S part, TCC, time, harmonics [EP7][EP11][EP12] | S part, TCC, time, scan [SK5][SK11][SK12] | S yes, TCC, R-X, time, scan [NP10][NP11][NP13][NP16] | S part, time, PV/QV [PS2][PS4] | none | - | R-020, R-044 |
| G13 | Worked equations with substituted values in reports | U | U | U [W8][W96] | U | U | U | U | **done (decision D11, WP-1.11)** | Kasikci02 | R-007, R-042, R-043, R-047, R-052 |

## Steady state

| ID | Capability | ETAP | PowerFactory | PowerWorld | EasyPower | SKM | NEPLAN | PSS/E | Quantic now | Owned book to verify | Requirement R-IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Balanced AC load flow (Newton-Raphson) | S yes [E7] | S yes [P3] | S yes [W30] | S yes; method U [EP10] | S yes; method U [SK8] | S yes [NP7] | S yes [PS3] | done | Glover17, Grainger94 | R-006, R-007, R-043, R-047, R-048 |
| S2 | Gauss-Seidel and fast decoupled methods | S yes [E7] | U (non-decoupled NR and linear DC only stated) | S part, fast decoupled [W30][W106] | U | U | S yes, alternatives [NP7] | U | partial (pandapower offers them; not exposed) | Glover17, Das02 ch. 11 to 12 | R-007 |
| S3 | Generator Q limits and PV to PQ switching | S part, reactive capability limits; PV/PQ transition rule U [E114] | S part, reactive capability limits; PV/PQ transition rule U [P3] | S yes [W20][W32] | S yes, PV/PQG limits and return switching [EP25] | S part, generator VAR limits in TMS load flow; PV/PQ rule U [SK11] | S part, OPF reactive limits; LF PV/PQ transition U [NP17] | U | done | Glover17 | R-008 |
| S4 | Tap changer and regulator control (local, remote bus) | S yes [E2] | S yes [P3][P66] | S yes [W19] | S yes, automatic LTC and local/remote PV control [EP24] | U | S yes, local/remote OLTC control [NP7] | U | none | Kundur94, Glover17 | R-008 |
| S5 | Phase-shifting transformers | S yes [E7] | S yes [P5] | S yes [W19] | U | U | S yes, phase-shifter power control [NP7] | U | none | Grainger94 | R-008 |
| S6 | Distributed slack, droop, primary and secondary control | S part, isochronous/droop governor models; distributed slack breadth U [E7] | S yes [P3] | S part, AGC and island slack [W30][W33] | S part, multiple swing-source sharing; secondary breadth U [EP24][EP25] | S part, frequency-sensitive island load flow (V8); secondary control U [SK33] | S part, distributed slack and secondary control; full breadth U [NP7][NP4] | U | none | Kundur94 | R-008, R-010 |
| S7 | Voltage-dependent loads (ZIP, exponential) | S yes [E9] | S yes [P39] | S yes, ZIP; exponential U [W22] | S yes, constant MVA/I/Z mixture [EP24] | S yes, constant kVA/I/Z loads [SK8] | S part, constant-current/power and composite loads; full ZIP U [NP4] | U | none | Sauer06, Kundur94 | R-007, R-009, R-019 |
| S8 | Temperature correction of conductor resistance | S yes [E2] | S yes [P3] | S part [W96] | U | S yes, cable resistance temperature adjustment (V8) [SK33] | U | U | none | Anders05 | R-007 |
| S9 | Multiple islands, each with its own slack | S yes [E6] | S yes [P3][P41] | S yes [W33] | S yes, islanded systems with swing sources [EP24][EP26] | S part, independent/frequency-sensitive islands; slack policy U [SK8][SK33] | U | U | untested (pandapower supports islands) | - | R-004, R-010 |
| S10 | Unbalanced three-phase load flow | S mod [E9] | S yes [P3] | U [W31][W95] | S yes [EP10] | S mod [SK14] | S yes [NP7] | U | none | Das02 ch. 14; gap Kersting | R-013, R-025, R-033 |
| S11 | Line constants from geometry, mutual coupling | S yes [E9][E22] | S yes [P5] | S yes [W96][W28] | U | S part, line parameter calculators; geometry/mutual breadth U [SK8] | S yes, geometry and mutual coupling [NP4] | U | none | Grainger94, Arrillaga03 | R-025, R-031, R-032, R-033, R-034, R-035, R-036, R-048 |
| S12 | DC load flow (batteries, chargers) and AC/DC | S yes [E21][E71] | S yes [P3][P5] | S part, HVDC only [W25][W26][W27] | S yes [EP10] | S mod, DC Systems [SK15] | S yes [NP7] | U | none | - | R-013, R-036 |
| S13 | Time-series and quasi-dynamic load flow | S mod [E59][E71] | S mod [P16] | S yes [W74] | U | U | S part, advertised [NP3] | S mod [PS3] | none | - | R-012 |
| S14 | Optimal power flow | S mod [E8] | S mod (interior point) [P20] | S mod, sequential LP [W54] | U | U | S mod [NP17] | S mod; backend U [PS6] | none | Glover17, Das02 | R-012 |
| S15 | Contingency analysis (N-1, N-2, screening, RAS) | S part, N-1/N-2 screening; RAS breadth U [E22][E59] | S mod [P15][P37] | S yes [W36][W41][W40] | S part, manual contingency/what-if states; automatic N-k/RAS U [EP24][EP5] | U | S mod [NP7] | S yes [PS3] | none | Grainger94 | R-005, R-011 |
| S16 | Sensitivities and distribution factors (PTDF, LODF) | U (Q-V sensitivity only) | S yes [P10] | S yes [W42][W43][W44] | U | U | S mod [NP7] | S mod, Advanced Linear [PS7] | none | Grainger94 ch. 14 | R-011 |
| S17 | Voltage stability P-V and Q-V, modal | S mod [E72] | S mod [P23][P10] | S mod PVQV [W50] | U | U | S part [NP2][NP3] | S yes, PV and QV [PS3] | none | Kundur94 | R-012 |
| S18 | State estimation | S yes (ADMS) [E22] | S mod [P26] | U [W99][W104] | U | U | S mod, State Estimator advertised (2019 brochure) [NP26] | U | none | Grainger94; gap Abur | R-050 |
| S19 | Hosting capacity | S yes (2026; E111; patent E112) [E111][E112] | S mod (P63) [P63][P22] | U [W45] | U | U | S mod, hosting capacity advertised (2019 brochure) [NP26] | U | none | - | R-050 |
| S20 | Optimal capacitor placement | S mod [E86] | S mod [P22] | U [W23] | U | U | S mod, radial optimal capacitor placement [NP30] | U | none | - | R-059 |
| S21 | Switching and tie-point optimisation, phase balancing | S part, switching/tie-point optimisation; phase balancing U [E88] | S mod [P22] | U [W39] | U | U | S mod, switching and phase balance advertised (2019/current catalog) [NP26][NP1] | U | none | - | R-060 |
| S22 | Probabilistic load flow | U | S mod [P44] | U [W75] | U | U | U | U | none | - | R-050 |
| S23 | Reliability indices and restoration | S mod [E31] | S mod [P21] | U [W36] | S part, IEEE 493 cut-set reliability; chronological restoration U [EP28] | S yes, reliability indices with repair/replace/switching [SK34] | S mod, reliability and restoration [NP31] | U | none | Glover17 (thin); gap Billinton | R-050 |
| S24 | Network reduction (Ward, REI) | S yes (2026, E91) [E91] | S mod [P43] | S yes; variants U [W88] | U | U | S mod, Ward/extended Ward/REI-DIMO [NP29] | U | none | Grainger94 sec. 14.6 | R-032, R-033, R-034 |
| S25 | Load allocation from meters | S yes [E59] | S yes (feeder scaling) [P3][P59][P64] | U [W82] | U | U | S yes, measurement import/load allocation [NP7] | U | none | - | R-061 |
| S26 | Unit commitment and economic dispatch | S yes (GMS) [E22] | S mod [P45] | S part, dispatch and reserves [W54][W57] | U | U | S part, economic dispatch/MOPF; unit commitment U [NP17] | U | none | Glover17, Grainger94 | R-012 |

## Faults

| ID | Capability | ETAP | PowerFactory | PowerWorld | EasyPower | SKM | NEPLAN | PSS/E | Quantic now | Owned book to verify | Requirement R-IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | IEC 60909 three-phase with ip, Ith, Ib, Ik | S yes [E11] | S yes [P4] | S part, flat IEC 909; edition U [W91] | S yes; editions qualified [EP6] | S mod [SK10] | S yes [NP8] | S mod [PS3] | partial (Ik'', ip, Ith with traces) | Kasikci02 | R-006, R-023, R-043, R-047 |
| F2 | Unbalanced faults (SLG, LL, LLG) | S yes [E3][E11] | S yes [P4] | S yes [W95] | S yes [EP6] | S mod [SK9][SK10] | S yes [NP8] | S mod [PS3] | none | Grainger94, Glover17 | R-013, R-023, R-025, R-035, R-047 |
| F3 | ANSI C37 three networks, X/R multipliers, duty | S yes [E10] | S yes [P4] | U [W91] | S yes [EP6] | S mod [SK9] | S yes [NP8] | U | none | Das02, Das21; gap C37.010 | R-023 |
| F4 | IEC 61363 transient decay | S yes [E12] | S yes [P4] | U [W91] | U | S mod, IEC 61363 decay and initial conditions [SK32] | U | U | none | - | R-023 |
| F5 | DC faults (IEC 61660, IEEE 946) | S part, IEEE 946 DC faults; IEC 61660 coverage U [E43] | S yes [P4] | U [W91] | S yes; method U [EP6] | S mod [SK15] | S yes, IEC 61660 [NP8] | U | none | Das02 ch. 9 | R-013 |
| F6 | Complete (superposition) method from load flow | U | S yes (P88) [P88] | S part, pre-fault profile [W91] | U | U | S yes [NP8] | U | none (pandapower supports it) | Kasikci02 | R-023 |
| F7 | Device duty against library ratings | S yes [E3] | S part, standard-specific duty; full library-rating workflow U [P4] | U [W95] | S yes [EP6] | S mod [SK2][SK9] | S part [NP8] | U | none | Das02, Das21 | R-024, R-029 |
| F8 | Multiple and open-conductor faults, fault sweeps | S part, simultaneous/sliding faults; open-conductor scope U [E59][E30] | S yes [P4] | S part, locations and batches [W90][W95] | U | U | U | U | none | Das02 sec. 2.8 and 14.1 | R-024 |

## Protection and arc flash

| ID | Capability | ETAP | PowerFactory | PowerWorld | EasyPower | SKM | NEPLAN | PSS/E | Quantic now | Owned book to verify | Requirement R-IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | TCC plotting with device libraries | S yes [E15][E27] | S yes [P11] | U [W58][W92] | S yes [EP7] | S yes, CAPTOR [SK5] | S yes [NP10] | U | none | Alstom11, Das21 | R-025, R-026 |
| P2 | Damage curves (cable, transformer, motor start) | S yes (E102) [E102] | S yes [P11] | U | S yes [EP7] | S yes [SK5] | S yes [NP10] | U | none | Alstom11, Das21 ch. 11 | R-026 |
| P3 | Automatic coordination checks by rules | S yes [E28] | S yes [P11] | U | S part, SmartPDC radial [EP9] | S yes, Auto Coordination [SK7] | U | U | none | Alstom11 | R-026 |
| P4 | Sequence of operation with backup | S yes [E29] | S yes [P11] | S part, timed events and relay response [W58][W62] | S yes [EP13] | S yes [SK13] | S yes [NP10] | S part, dynamic relays [PS4] | none | Blackburn06 | R-021, R-024, R-027, R-029, R-030, R-048 |
| P5 | Automatic setting calculation | S part (AFAS, 2026, E91) [E91] | S yes [P11] | U | S part [EP9] | S yes [SK7] | S part, distance only [NP11] | U | none | Alstom11 | R-026 |
| P6 | Distance protection, R-X, zones | S mod [E30] | S mod [P11] | U | U | U | S yes [NP11] | U | none | Alstom11, Blackburn06 | R-053 |
| P7 | Differential protection | S yes [E30] | S yes [P11] | U | S yes, differential/partial/ground differential [EP7] | U | S yes, differential relay model [NP4] | U | none | Alstom11 | R-054 |
| P8 | CT and VT models with saturation | S part, CT saturation and CT/VT placement; VT saturation U [E30][E113] | S yes [P11] | U | U | U | S part, current-transformer saturation module; VT breadth U [NP25] | U | none | Alstom11 | R-025 |
| P9 | Design versus as-found and maintenance settings as separate states | S yes (eProtect, E104) [E104] | U | U | S part, main included or excluded [EP20] | S yes, main failure and maintenance [SK21] | S part, PDMS setting history; explicit as-found/maintenance modes U [NP19] | U | none | - | R-030 |
| A1 | Arc flash IEEE 1584-2018 with automatic clearing time | S mod [E14] | S mod (P87) [P87] | U [W4][W82] | S yes [EP8][EP20] | S mod [SK6] | S mod, 2018 stated [NP9] | U | none (arcflash-calc approved) | Das21 (Table 3.1 unreliable); DGUV-I 203-077 | R-024, R-027, R-028, R-029, R-030, R-043, R-048, R-049 |
| A2 | Arc flash labels and work permits | S yes [E13][E14] | S yes (labels) [P12][P87] | U | S yes [EP16] | S mod [SK6] | S mod [NP9] | U | none | Das21 | R-028, R-030, R-046 |
| A3 | DC arc flash | S yes (E106) [E106] | S yes (NFPA 70E, DGUV; P87) [P87] | U | S part [EP8] | S part [SK6] | S part [NP9] | U | none | Das21 ch. 15; DGUV-I 203-077 | R-028 |
| A4 | HV arc flash (above 15 kV) | S yes (1 to 800 kV, E106) [E55][E106] | S part (EPRI listed; range U; P87) [P87] | U | S part [EP8] | U | S part [NP9] | U | none | Das21 | R-028 |
| A5 | Arc energy integrated over changing source current and device sequence | S part (decay and time-varying clearing, E13 and E14; integration method U) [E13][E14] | U | U | S yes, Integrated method [EP20][EP22] | S part, changing contributions [SK23] | U | U | none | Das21 sec. 6.9 | R-027, R-029 |

## Dynamics and power quality

| ID | Capability | ETAP | PowerFactory | PowerWorld | EasyPower | SKM | NEPLAN | PSS/E | Quantic now | Owned book to verify | Requirement R-IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M1 | Static motor start (voltage dip) | S yes [E4][E63] | S yes [P19] | U [W97] | S part [EP12] | S part [SK11] | S yes [NP12] | U | partial (WP-1.4) | Das02 | R-006, R-009, R-043, R-047 |
| M2 | Dynamic motor acceleration with torque-speed models | S yes [E4][E23] | S yes (P79) [P19][P79] | S mod, Transient Stability [W97] | S yes [EP12] | S yes, TMS [SK11] | S yes [NP12] | S part, motor events [PS4] | none | Das02, Fitz03, Krause23 | R-015, R-017, R-019, R-021, R-047, R-048, R-049 |
| M3 | Starters: autotransformer, star-delta, reactor, soft starter, VFD | S yes [E24] | S yes (P79) [P79] | U [W97] | S part [EP12] | S part, reactor, autotransformer, star-delta, solid-state; VFD breadth U [SK11] | S yes [NP12] | U | none | Bose02, Krause23 | R-009, R-015, R-021 |
| M4 | Motor parameter estimation from datasheet | S yes, MotorPro and historical 2007 parameter-fitting tutorial [E87][E26] | U, generic parameter identification [P49] does not establish motor fitting from datasheet | U [W97] | S yes [EP12] | U | S yes [NP12] | U | none | Krause23, Fitz03 | R-016 |
| T1 | RMS transient stability with machines, exciters, governors, PSS | S mod [E16] | S mod (theta method, P89) [P17][P89] | S mod, RK2 or Euler [W58][W59][W60] | S yes [EP13] | S yes, I*SIM [SK13] | S yes [NP13] | S yes [PS4] | none | Kundur94, Sauer06 | R-015, R-017, R-018, R-019, R-020, R-022, R-044, R-049 |
| T2 | User-defined dynamic models | S yes (UDM) [E39] | S yes (DSL, Modelica, FMI) [P17][P18] | S part, UDM DLLs [W64][W92] | U | S yes, custom controls [SK13] | S yes [NP13] | S yes, GMB [PS5] | none (FMI-shaped lifecycle only) | Ogata02 | R-017, R-018, R-019, R-020, R-022, R-038, R-040 |
| T3 | Small-signal eigenvalue analysis | U (2026 frequency response only, E91) | S mod [P27] | S part, SMIB only [W63][W89] | U | U | S yes [NP13] | U | none | Kundur94 ch. 12 | R-022 |
| T4 | EMT simulation | S mod (PSCAD engine) [E38] | S mod [P18] | U [W59] | U | U | S mod [NP14] | S part, external companion [PS2] | none | Das10, Najm10 | R-022, R-040, R-044, R-049 |
| T5 | Load shedding, fast bus transfer, generator start | S yes [E16][E77] | S part, UFLS and RMS switching; generator-start/fast-transfer breadth U [P74][P17] | S part [W58][W62] | S yes [EP13] | S yes [SK13] | S yes [NP13] | S yes [PS4] | none | Kundur94 | R-010, R-020, R-021, R-027 |
| T6 | Dynamic initialisation checks and diagnostics | U | S yes (RMS only; P91) [P91] | S yes [W61] | S yes, initialization DState criterion and logs [EP29] | U | S part, automatic dynamic initialization; diagnostic detail U [NP14] | S yes, dynamic data checking [PS4] | none | Kundur94 | R-017, R-018 |
| H1 | Harmonic load flow and frequency scan | S mod (E110) [E5][E110] | S mod [P14] | S part, GIC with external GICHarm; general harmonics U [W70][W102] | S mod [EP11] | S yes, HI_WAVE [SK12] | S mod [NP16] | S mod [PS3] | none | Das02 ch. 19 to 20, Arrillaga03 | R-014, R-034, R-044, R-048 |
| H2 | Filter design and IEEE 519 or IEC 61000 limits | S yes [E5] | S yes [P14] | U [W102] | S mod [EP11] | S yes [SK12] | S mod [NP16] | U | none | Arrillaga03, Das10 | R-014 |
| H3 | Flicker | S yes (2026) [E26] | S yes [P14] | U | U | U | S mod, Pst/Plt flicker analysis [NP27] | U | none | - | R-051 |

## Design calculators

| ID | Capability | ETAP | PowerFactory | PowerWorld | EasyPower | SKM | NEPLAN | PSS/E | Quantic now | Owned book to verify | Requirement R-IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Cable sizing (ampacity, drop, short circuit, motor start) | S yes [E18] | S mod (P77, P78) [P13][P77][P78] | U [W4][W96] | S part, SmartDesign [EP14] | S part, DAPPER [SK8] | S part, cable sizing [NP18] | U | none | Anders05, Morley | R-031, R-051 |
| C2 | Cable ampacity, Neher-McGrath and IEC 60287, duct banks | S mod [E19][E70][E74] | S mod (P77) [P13][P77] | U | U | S yes, vendor method claim [SK24] | U | U | none | Anders05 | R-031, R-051 |
| C3 | Cable pulling and tension | S mod [E22] | U | U | U | S yes, Cable-3D [SK25] | U | U | none | - | R-051 |
| C4 | Transformer sizing | S mod [E20] | U | U | S part [EP14] | S part [SK8] | U | U | none | - | R-051 |
| C5 | Battery sizing (IEEE 485) and discharge | S mod [E41][E42] | U | U | U | S yes, DC Systems [SK15] | U | U | none | gap IEEE 485; Das02 ch. 9 | R-051 |
| C6 | Ground grid (IEEE 80, FEM, soil model) | S mod (E107) [E107] | U | U | S part, partner XGSLab [EP23] | S yes, GroundMat [SK16] | S part, substation grounding advertised; FEM/soil method U [NP26] | U | none | Morley ch. 7; DZS 691 | R-035, R-048, R-051 |
| C7 | Panel schedules (NEC demand) | S mod [E40] | U | U | S part [EP14] | S part [SK8] | U | U | none | - | R-051 |
| C8 | Line sag, tension and ampacity (IEEE 738) | S mod [E22] | U | S part, line parameters only [W96] | U | U | U | U | none | Gonen88 ch. 10 | R-031, R-051 |

## Product-specific distinctions to retain

| ID | Capability | ETAP | PowerFactory | PowerWorld | EasyPower | SKM | NEPLAN | PSS/E | Quantic now | Owned book to verify | Requirement R-IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PW-D1 | Full-topology consolidation with planning and operations identity mapping | U | U | S mod ITP [W104] | U | U | U | U | none | - | R-004 |
| PW-S1 | DC transmission approximation kept separate from HVDC models | U | S yes (linear DC) [P3] | S yes [W34][W25] | U | U | S yes, decoupled active-power DC load flow [NP7] | U | none | Grainger94 | R-007, R-013 |
| PW-S2 | Primary and secondary contingency reference states, reusable RAS | U | U | S yes [W41][W40] | U | U | U | S part, Python RAS [PS1] | none | - | R-011 |
| PW-S3 | Transfer capability: linear, iterated linear, full-contingency refinement | U | S yes, transfer capacity (P23) [P23] | S mod ATC [W45][W46][W47][W48] | U | U | S part, NTC security-limited transfer; refinement modes U [NP32] | U | none | - | R-011, R-012 |
| PW-S4 | Security-constrained dispatch and reserves | U | U | S mod OPF, SCOPF, Reserves [W56][W57] | U | U | S part, AC SC-OPF and economic dispatch; reserves U [NP17] | U | none | - | R-012 |
| PW-S5 | Geomagnetically induced current network with AC and harmonic feedback | U | U | S mod GIC [W68][W102] | U | U | U | S mod, Advanced [PS1] | none | - | R-036 |
| PW-T1 | SMIB eigenvalue check kept separate from fitted signal modes | U | U | S yes [W63][W89] | U | U | U | U | none | Kundur94 | R-022 |
| PW-X1 | Distributed independent study jobs | U | S yes (engine licences, server ICA [P63]) [P32] | S yes [W73][W2] | U | U | U | U | none | - | R-005 |
| X-1 | Co-simulation inside one tool (EMT-EMT, RMS-EMT) | U | S yes (P92) [P92] | U | U | U | S part, hybrid RMS and EMT [NP14] | U | none | - | R-022 |
| X-2 | EMT measurement quantities (instantaneous, true RMS, sequence phasors) | U | S yes (P93) [P93] | U | U | U | S part, instantaneous ABC/COMTRADE; RMS/phasor meters U [NP14] | U | none | Das10 | R-044 |
| X-3 | Impedance-based stability of inverter-based resources | U | S yes (P27) [P27] | U | U | U | U | U | none | - | R-022 |
| X-4 | Dynamic model parameter identification from measurements | U (motor estimation only, M4) | S yes (P49) [P49] | U | U | U | U | U | none | - | R-016 |
| X-5 | Techno-economic comparison of alternatives (NPV) | U | S yes (P46) [P46] | U | U | U | S mod, investment present-value assessment (2019 brochure) [NP26] | U | none | - | R-012 |
| X-6 | Real-time operation: PMS, intelligent load shedding, ADMS | S yes (E73, E76) [E73][E76][E22] | S part, separate PFM monitoring product; native PMS/ADMS U [P71] | U (separate real-time products [W99]) | U | U | S part, SCADA integration; native PMS/ILS/ADMS U [NP26] | U | none | - | R-021 |
| X-7 | Transformer inrush study | S yes (E84) [E84] | U | U | U | U | S yes, transformer energization/inrush in EMT [NP14] | U | none | Das10 | R-020 |
| X-8 | DC control circuit diagram and voltage drop | S yes (E85) [E85] | U | U | U | U | U | U | none | - | R-062 |
| X-9 | Railway traction power (eTraX) | S mod (E90) [E90] | U | U | U | U | U | U | none | - | R-063 |
| X-10 | Wind turbine generator models | S yes (E89) [E89] | S yes [P5][P17] | S part, generic dynamic models [W92] | U | U | S yes, wind generation models [NP4] | S part [PS4] | none | - | R-019 |

## Known gaps in this matrix

1. **Cell-level citation gap closed by WP-2.18.** All retained ETAP/PowerFactory S
   cells name primary-source IDs. PowerFactory M4 is now U: P49 supports generic
   measurement-based identification, not the row's motor-from-datasheet workflow.
   Narrowed cells retain explicit U qualifications; citations do not prove execution.
2. **Missing requirements closed by WP-2.16.** R-053 to R-063 cover P6, P7, D18, G3,
   G4, G8, S20, S21, S25, X-8 and X-9; their row links are populated here. Existing
   requirements retain their original IDs. Source/method gaps inside them remain open.
3. **No product cell is observed in the running product.** Every S is a documented
   statement. WP-2.15 defines the comparison cases that would add observed evidence.
4. **U cells are research leads, not gaps in the products.** WP-2.20 searched the
   213 formerly U EasyPower/SKM/NEPLAN cells by capability family and promoted
   71 with primary evidence, including partial and historical qualifications.
   The completed log lists all remaining U cells and search routes. PSS/E industrial
   rows and the untouched product columns retain their earlier scope.
5. **Version drift.** Cells reflect sources read on 2026-10-15 to 2026-10-17. Refresh
   every six or so WPs, as Peter asked, before using a cell in a sales or design claim.
