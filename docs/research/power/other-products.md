# Industrial and transmission competitors: EasyPower, SKM, NEPLAN and PSS/E

WP-2.13. Public-source research checked 2026-10-16. This is a capability dossier,
not an evaluation licence test or a purchase quotation. Each product has the nine
sections in the research template. References use product prefixes and numbers;
shared user reports are registered once in the EasyPower source table.

**Evidence rules.** A vendor description establishes an advertised capability, not
numerical correctness, measured speed or certification. Historical manuals and user
reports keep their dates. `Unknown` means public evidence did not close the question;
it never means the product lacks the feature. Methods, parameter units and defaults
are recorded only where read. Proposed Quantic implications are explicitly inferences.
No commercial software was executed and no vendor library or example dataset is copied.

The shared row IDs refer to the [working capability matrix](notes/matrix-draft-etap-powerfactory.md).
The final table supplies evidence for the next matrix WP; it does not change Quantic's
implementation status or extend the approved build scope.

# EasyPower

## 1. Identity, versions, editions, licensing and platform

EasyPower is a Bentley company. Current public help documents EasyPower 2026;
the main sales page still promotes 2025, so the landing-page banner alone is not a
release authority. The FAQ describes 64-bit Windows 10/11. [EP2][EP3]

Base covers model editing; Standard adds faults, protection and arc flash;
Professional adds power flow; Advanced adds harmonics. Analysing tiers are sold at
several bus capacities; Base is unlimited. Motor starting and dynamics are optional
on the higher tiers. The page offers annual subscriptions and perpetual licences
with SELECT support/pooling, plus cloud-hosted entitlement. No numeric current
price was available in the public sales material read; request the module, bus,
seat and region-specific quote. Legacy FAQ hardware-key arrangements should not be
substituted for a current offer. [EP1][EP2]

## 2. Sources

| ID | URL and title | Type | Accessed |
|---|---|---|---|
| EP1 | [EasyPower product tiers and licensing](https://www.easypower.com/products/easypower) | Vendor public page/help | 2026-10-16 |
| EP2 | [EasyPower support FAQ](https://www.easypower.com/support/faqs) | Vendor public page/help | 2026-10-16 |
| EP3 | [EasyPower 2026 release details](https://help.easypower.com/ezp/26.0/Content/96_Release_Notes/2026_Release_Details.htm) | Vendor public page/help | 2026-10-16 |
| EP4 | [Integrated one-line diagrams](https://www.easypower.com/products/features/integrated-one-line-diagrams) | Vendor public page/help | 2026-10-16 |
| EP5 | [ScenarioManager](https://www.easypower.com/products/features/scenariomanager) | Vendor public page/help | 2026-10-16 |
| EP6 | [ShortCircuit](https://www.easypower.com/products/features/shortcircuit) | Vendor public page/help | 2026-10-16 |
| EP7 | [Protection and Coordination](https://www.easypower.com/products/features/protection-coordination) | Vendor public page/help | 2026-10-16 |
| EP8 | [ArcFlash](https://www.easypower.com/products/features/arcflash) | Vendor public page/help | 2026-10-16 |
| EP9 | [SmartPDC](https://www.easypower.com/products/features/smartpdc) | Vendor public page/help | 2026-10-16 |
| EP10 | [PowerFlow](https://www.easypower.com/products/features/powerflow) | Vendor public page/help | 2026-10-16 |
| EP11 | [Harmonics](https://www.easypower.com/products/features/harmonics) | Vendor public page/help | 2026-10-16 |
| EP12 | [Transient Motor Starting](https://www.easypower.com/products/features/transient-motor-starting) | Vendor public page/help | 2026-10-16 |
| EP13 | [Dynamic Stability](https://www.easypower.com/products/features/dynamic-stability) | Vendor public page/help | 2026-10-16 |
| EP14 | [SmartDesign](https://www.easypower.com/products/features/smartdesign) | Vendor public page/help | 2026-10-16 |
| EP15 | [Revit Integrator](https://www.easypower.com/products/features/revit-integrator) | Vendor public page/help | 2026-10-16 |
| EP16 | [2026 help: Arc Flash Analysis tutorial](https://help.easypower.com/ezp/26.0/Content/98_Tutorials/Arc_Flash_Analysis.htm) | Vendor public page/help | 2026-10-16 |
| EP17 | [2026 help: User Clearing Times](https://help.easypower.com/ezp/26.0/Content/16_Arc_Flash_Hazard_Analysis/User_Clearing_Times.htm) | Vendor public page/help | 2026-10-16 |
| EP18 | [2026 help: Store Arc Flash Results](https://help.easypower.com/ezp/26.0/Content/05_ANSI_Short_Circuit/ANSI_Store_Arc_Flash_Results.htm) | Vendor public page/help | 2026-10-16 |
| EP19 | [2026 help: Busway specifications](https://help.easypower.com/ezp/26.0/Content/13_Database_Technical_Ref/Busway/Specifications_tab.htm) | Vendor public page/help | 2026-10-16 |
| EP20 | [2026 help: Arc Flash Hazard Options](https://help.easypower.com/ezp/26.0/Content/16_Arc_Flash_Hazard_Analysis/Arc_Flash_Hazard_Options.htm) | Vendor public help | 2026-10-16 |
| EP21 | [2026 help: The Integrated Method](https://help.easypower.com/ezp/26.0/Content/16_Arc_Flash_Hazard_Analysis/Integrated_Method.htm) | Vendor public help | 2026-10-16 |
| EP22 | [2026 help: Advanced Arc Flash Options](https://help.easypower.com/ezp/26.0/Content/05_ANSI_Short_Circuit/ANSI_Adv_Arc_Flash_Hazard_Options.htm) | Vendor public help | 2026-10-16 |
| EP23 | [XGSLab grounding solution and modules](https://www.easypower.com/products/xgslab-grounding) | Vendor partner-product page | 2026-10-16 |
| U1 | [Eng-Tips: DC VFD and DC motor modelling, June to July 2026](https://www.eng-tips.com/threads/easypower-modeling-of-a-dc-vfd-and-dc-motor-or-skm-or-etap-as-a-sidebar.587365/) | Independent author/developer | 2026-10-16 |
| U2 | [Eng-Tips: SKM and EasyPower arc-flash results, December 2013](https://www.eng-tips.com/threads/skm-and-easypower-results-for-arc-flash.356401/) | Independent author/developer | 2026-10-16 |
| U3 | [Eng-Tips: Electrical Analysis/Design Software, December 2007](https://www.eng-tips.com/threads/electrical-analysis-design-software.204703/) | Independent author/developer | 2026-10-16 |

## 3. Architecture and data model

**D1, D3, G1.** A shared database connects the graphical network to analyses;
one-line equipment carries the engineering data and warnings. A library choice
and an installed item should remain distinct in our interpretation, but the full
internal object schema is not public. [EP4]

**D4, D5, D6.** ScenarioManager stores operating alternatives, including breaker
states, changed equipment data, protective settings and diagram differences. It
highlights changed values and can identify the scenario responsible for worst
arc-flash results. This supports scenario comparison, not evidence of concurrent
revision merging or a multi-user transaction model. [EP5]

**D11, D12.** Manufacturer libraries and database browsing assist data entry.
The 2026 release notes describe a CSV import validation report with old/new values
and navigation to affected equipment. Neither a library selection nor successful
import proves field data has been independently verified. [EP1][EP3]

## 4. Element catalogue and parameters

This is a sourced catalogue of modelling responsibilities, not a complete export
schema. Units below belong to the identified help fields; unsourced defaults and
conversion constants are deliberately omitted.

| Element/data family | Parameters and meaning evidenced publicly | Qualification |
|---|---|---|
| Busway | Manufacturer/type; length in ft or m; ampacity in A; conductor material; positive/zero-sequence impedance per 100 ft or 100 m | These are the busway help's conventions, not universal units for every branch. [EP19] |
| Protective device | Phase/ground curve, pickup/settings and device operating characteristic | TCC manipulation updates the model; field settings still require verification. [EP7] |
| Motor and driven load | Torque/speed characteristic, starting arrangement, inertia-related acceleration model and scheduled start events | Additional data is needed for dynamic starting compared with a voltage-dip study. [EP12] |
| Generator and controls | Machine, excitation/AVR and governor response; fault, clearing and switching events | The public page does not enumerate the complete versioned control-model library. [EP13] |
| Arc-flash location | Working distance, selected fault/clearing arrangement and source contributions | The tutorial's available user times are options, not prescribed actual trip times. [EP16][EP17] |
| Harmonic source/filter | Source spectrum and filter representation, including non-integer components | Exact public parameter schema and default spectra remain unknown. [EP11] |

## 5. Studies and modules

| IDs / study | Purpose, method, options and inputs | Outputs, reports and limits |
|---|---|---|
| F1-F3, F5, F7: ShortCircuit | ANSI and IEC 60909 AC analysis, single-phase and DC networks; source and equipment impedances, earthing and ratings | Momentary/interrupting currents, relay currents and equipment-duty comparisons. SmartDuty considers line/load-side exposure. Exact standard editions and backend implementation are not established here. [EP6] |
| P1, P2, P7: coordination | Plot manufacturer TCCs with network fault currents; edit phase/ground settings; compare backup intervals and equipment curves. Differential schemes are advertised | Linked curve/network results. A differential scheme claim does not establish a full distance-relay engine. [EP7] |
| P3, P5: SmartPDC | Radial setting assistance using modelled devices and coordination constraints | Suggested settings with reasons; the page limits LV scope to 600 V and MV feeders to two series relays. It does not prove global optimal selectivity. [EP9] |
| A1-A4: ArcFlash | Vendor describes time-domain accumulation with decaying currents and a flux model, protection interaction, AC/DC/single-phase and HV methods | Incident energy, boundary, labels and permits. The advertised upper range of 800 kV must not be attributed to IEEE 1584 itself. Exact method/range selection needs the applicable help/standard. [EP8] |
| S1, S10, S12: PowerFlow | Balanced/unbalanced AC, single-phase and physical DC network power flow; load, source and branch data | Voltage, branch P/Q/current, losses, loading, taps and violation filtering. A particular Newton implementation is not stated on this feature page. [EP10] |
| H1, H2: Harmonics | Integer/non-integer source spectra, triplen/zero-sequence considerations and filters | Harmonic voltages/currents, distortion and filter assessment; IEEE 519 is named without a confirmed edition here. [EP11] |
| M2-M4: transient motor starting | Timed motor starts, motor/load torque characteristics and parameter fitting; protective-device response requires the relevant modules | Voltage, current, speed and torque traces; contactor/relay operation. Verify PowerFlow and protection dependencies in a quote. [EP12] |
| T1, T5: Dynamic Stability | Machine/control interaction with faults, clearing, transfer, reacceleration and shedding | Time response and protection interaction. Public feature evidence does not establish EMT switching waveforms or a named integration formula. [EP13] |
| C1, C4, C7: SmartDesign | Rule-driven equipment/cable/device/transformer sizing, design sheets and NEC context | Design and schedule outputs. This does not establish Zambian code compliance or a detailed IEC 60287 thermal engine. [EP14] |

## 6. Workflow and interface

A traceable industrial workflow reconstructed from the public tutorial is:

1. Open/build the one-line and correct missing input diagnostics before analysis.
2. Select the operating configuration and short-circuit/arc-flash options.
3. Fault the target bus or a set of buses, inspect energy and boundary results,
   and retain the device-specific clearing assumptions.
4. Review coordination and generate the selected labels/report outputs. [EP16]

The help explicitly prefers actual protection clearing characteristics over legacy
user-fixed clearing times. Stored arc-flash results can be inspected in the database
and used in downstream outputs. **Inference:** Quantic should associate those stored
outputs with the scenario, input hash and protective settings to prevent stale labels;
this is a proposed requirement, not an observed EasyPower implementation guarantee.
[EP17][EP18]

The graphical editor supports data warnings, snapping and CAD output. Revit Integrator
maps families/instances and supports review of model differences before exchange.
Its separate product page describes an additional purchase, while the tier chart
includes its name; entitlement needs clarification in the actual quote. [EP4][EP15][EP1]

### 6.1 Arc-flash calculation state, not just a label

**A1/A2, P4.** The 2026 help distinguishes bus/load-side exposure from the
incoming side of a main device. Including the main permits its clearing action;
excluding it uses upstream protection. Detailed output additionally covers
downstream device terminals. Worst-case selection compares estimated and reduced
arc current: the 2018 method derives reduction from system inputs, whereas the
older method exposes user ratios. Maximum duration can truncate a calculated TCC
time. A cap is a study assumption, not evidence that a breaker opens then.
Opening older files also replaces the obsolete enhanced methods with the latest
IEEE selection, so unchanged equipment does not guarantee unchanged calculations.
[EP20]

The Integrated method advances fault and device states together, accumulating
energy over successive intervals. It recalculates bus/device currents, integrates
device memory from the TCC and opens qualifying devices at step boundaries;
relay-operated breakers add opening delay. Its documented ANSI approximation uses
momentary current through cycle one, interrupting current for cycles two through
eight, then 30-cycle current. This establishes a discrete sequence, not a published
step size, error bound or continuous flux-solver equivalence. [EP21]

Advanced options expose bounded upstream search, minimum relay time, enclosure
correction, current-limiting fuse treatment and out-of-range method selection.
With 2018 selected, remote device current uses its bolted-current share of bus
arcing current. The HV open-air choice uses a separate NFPA 70E 2009 Annex D.8
route and overrides other methods; it does not extend IEEE 1584's validated range.
A switch extending a low-voltage DC equation above 1 kV is documented, but its
physical validity is not established by this dossier. [EP22]

**Inference for Quantic:** persist method/version, fault location relative to the
device, normal/reduced-current branch, search limits, cap and fallback. Integrated
studies need a time-ordered trip/current/energy ledger. These are proposed research
requirements, not approval to build the engine. [EP20][EP21][EP22]

### 6.2 Grounding is a partner-product boundary

**C6.** EasyPower offers SINT's XGSLab separately and describes its representation
arrangement for the USA and Canada. This does not establish included entitlement
or sales coverage for Zambia. The page distinguishes static equipotential GSA from
frequency-dependent GSA_FD, above/below-ground XGSA_FD, FFT/PEEC/IFFT transient
XGSA_TD, a conductor/earth-path NETS solver and lightning shielding. PEEC methods
are advertised; none were independently run. Record a partner route, with native
EasyPower ground-grid scope still unknown. [EP23]

## 7. Dated user evidence

`wbd`, Eng-Tips, 8-9 December 2013, compared an older SKM report with EasyPower 9.5:
reported energy differences accompanied different clearing times despite similar
arcing currents. `dpc` suggested checking device curves, current seen by the upstream
device and study options. The thread did not resolve the cause. It supports a
need for auditable clearing-time provenance, not a verdict about either current
product's correctness. [U2]

`2esingeek`, 26 June 2026, described migrating a pulp/paper model from SKM to
EasyPower and asked how a DC drive/motor's contribution propagates through a
rectifier. Replies on 1 July suggested modelling routes but did not establish a
resolved defect. **Inference:** converter directionality and explicit contribution
paths need review during migration. [U1]

## 8. Engines implied

The documented studies imply separate network assembly, fault-current/duty,
TCC/device-time, arc-energy accumulation, load-flow, harmonic and dynamic
machine/control responsibilities. SmartPDC adds a constrained rule/setting layer;
SmartDesign adds design rules and library selection. Those are architectural
inferences from the advertised workflows, not claims about Bentley's code layout.
Sparse solver, exact integration scheme, implementation language and numerical tolerances
remain unknown; section 6.1 documents a discrete sequence without those numerical details. [EP6][EP7][EP8][EP9][EP10][EP11][EP12][EP13][EP14]

## 9. Explicit gaps

| Gap | Why it remains open / action |
|---|---|
| Current numeric price and exact entitlement | Sales page directs to a quote; Revit purchase wording conflicts with tier presentation. Obtain a scoped offer. [EP1][EP15] |
| Versioned protection/dynamic library completeness | Feature pages give categories rather than a release-specific inventory, defaults and model equations. [EP7][EP13] |
| Arc-method validity and numerical precision | Section 6.1 closes selection/clearing workflow gaps. Solver step size/error control and independent validity of fallbacks remain unverified. [EP20][EP21][EP22] |
| Solver tolerances, iteration/integration details and independent current benchmarks | Public pages read do not expose these. No licensed evaluation was run. [EP6][EP10][EP13] |
| D9, D13, D14 breadth; P6; T3/T4; C2/C3/C5/C8 | No sufficient public evidence was found in the sources read. Native C6 remains unknown; XGSLab is a documented partner route. [EP23] |

# SKM PowerTools for Windows

## 1. Identity, versions, editions, licensing and platform

SKM Systems Analysis markets PTW as modular PowerTools for Windows. Its home page
announces version 11.0.1.1 on 6 August 2026. The 2026 price list calls for Windows
10 or newer; older downloads/support text should not set current platform requirements.
[SK1][SK2][SK20]

Selected advertised USD prices below were visually read on price-list page 4.
They are package observations dated 2026, not an annual subscription comparison.

| Package | 50 buses | 300 buses | 12,000 buses |
|---|---:|---:|---:|
| Power*Pack: DAPPER, CAPTOR and Arc Flash | 6,195 | 12,195 | 33,995 |
| Combo*Pack I, including additional ANSI/IEC fault and equipment evaluation modules | 7,995 | 12,875 | 36,795 |

Page 7 includes first-year updates/support, then separate renewal conditions;
LAN/WAN, concurrency and site arrangements change the offer. These base package
figures are not a floating, multi-site or maintenance-inclusive lifetime quote.
MySKM cloud service is separately listed at USD 1,500/year on page 6. [SK2]

## 2. Sources

| ID | URL and title | Type | Accessed |
|---|---|---|---|
| SK1 | [SKM home and version news](https://www.skm.com/) | Vendor public page/help | 2026-10-16 |
| SK2 | [SKM 2026 price list, seven pages](https://skm.com/SKM_2026_Price_List.pdf) | Vendor public PDF | 2026-10-16 |
| SK4 | [PTW product catalogue](https://www.skm.com/product.html) | Vendor public page/help | 2026-10-16 |
| SK5 | [CAPTOR](https://www.skm.com/captor.html) | Vendor public page/help | 2026-10-16 |
| SK6 | [Arc Flash Evaluation](https://www.skm.com/arcflash.html) | Vendor public page/help | 2026-10-16 |
| SK7 | [Auto Coordination and Evaluation](https://www.skm.com/coordination-evaluation.html) | Vendor public page/help | 2026-10-16 |
| SK8 | [DAPPER](https://www.skm.com/Dapper.html) | Vendor public page/help | 2026-10-16 |
| SK9 | [A_FAULT ANSI fault analysis](https://www.skm.com/afault.html) | Vendor public page/help | 2026-10-16 |
| SK10 | [IEC 60909 fault analysis](https://www.skm.com/iec60909.html) | Vendor public page/help | 2026-10-16 |
| SK11 | [Transient Motor Starting](https://www.skm.com/tms.html) | Vendor public page/help | 2026-10-16 |
| SK12 | [HI_WAVE](https://www.skm.com/hiWave.html) | Vendor public page/help | 2026-10-16 |
| SK13 | [I*SIM](https://www.skm.com/iSim.html) | Vendor public page/help | 2026-10-16 |
| SK14 | [Unbalanced/Single Phase](https://www.skm.com/phaseStudies.html) | Vendor public page/help | 2026-10-16 |
| SK15 | [DC System Analysis](https://www.skm.com/dcSystemAnalysis.html) | Vendor public page/help | 2026-10-16 |
| SK16 | [GroundMat](https://www.skm.com/groundMat.html) | Vendor public page/help | 2026-10-16 |
| SK17 | [FAQ: comprehensive fault study versus standard fault study](https://www.skm.com/faq_ptw19.html) | Vendor public page/help | 2026-10-16 |
| SK18 | [PTW Tutorial, historical interface and workflow](https://www.skm.com/PTW%20Tutorial.pdf) | Vendor public PDF | 2026-10-16 |
| SK19 | [FAQ: breaker opening time in arc-flash evaluation](https://www.skm.com/faq_breakerOpeningTime.html) | Vendor public page/help | 2026-10-16 |
| SK20 | [PTW downloads](https://www.skm.com/downloads.html) | Vendor public page/help | 2026-10-16 |
| SK21 | [V7.0 arc-flash main-failure and maintenance-mode options](https://www.skm.com/Arc_Flash_Two_Powerful_Options.html) | Vendor historical article | 2026-10-16 |
| SK22 | [Additional utility data in arc-flash analysis](https://www.skm.com/Using_Additional_Utility_Data_Arc_Flash.html) | Vendor undated article | 2026-10-16 |
| SK23 | [Generator decrement and protective-device pickup](https://support.skm.com/KB/View/3939-why-does-my-protective-device-not-pick-up-the-fault-after-checking-both-apply-to-generators-and-recalculate-trip-time-using-reduced-current-in-the-arc-flash-options-menu-) | Vendor undated knowledge base | 2026-10-16 |
| SK24 | [Cable Ampacity](https://www.skm.com/cable-ampacity.html) | Vendor module page, introduced for V8 | 2026-10-16 |
| SK25 | [Cable-3D pulling analysis](https://www.skm.com/cable3D.html) | Vendor module page | 2026-10-16 |
| SK26 | [Johnny Ma: SKM IEEE Certification 2026, 20 January 2026](https://support.skm.com/KB/View/4939-ieee-certification-) | Vendor statement, not independent certification | 2026-10-16 |

## 3. Architecture and data model

**D1, D3, G1.** PTW combines a component database, one-lines, study setups,
reports and CAPTOR coordination views. The public tutorial demonstrates shared
component edits and selectable result datablocks. It is historical interface
material; its arc-flash defaults must not be treated as version 11 recommendations.
[SK18]

**D11, P1.** CAPTOR manufacturer curves remain editable; settings changes on a
curve propagate to the associated device. Phase/ground plots and as-found versus
recommended settings are supported. This is stronger evidence than an isolated
image of a TCC, but does not establish field-setting verification. [SK5]

## 4. Element catalogue and parameters

| Family | Publicly documented fields / modelling responsibility | Limits |
|---|---|---|
| Utility, generator, transformer and cable | Utility equivalent and X/R; machine representation; transformer sequence/earthing; branch impedance and ratings | DAPPER's conventional fault study and A_FAULT's decay/duty treatment are distinct. [SK8][SK9] |
| Transformer rating | Tutorial's Nominal kVA field; impedance editing and library selection | The tutorial's example values are not engineering defaults. [SK18] |
| Protective device | Manufacturer curve, valid pickup/time settings, phase/ground functions, opening time | For some LV devices the manufacturer's curve already includes opening time. [SK5][SK19] |
| Starting motor | Torque-speed/load characteristic, inertia, starter and scheduled events | Network voltage feeds back into acceleration. [SK11] |
| Battery/DC system | Chemistry/discharge curve, duty cycle, rectifier, UPS/converter and DC loads | Battery sizing and DC fault calculations are separately selected studies. [SK15] |
| Ground grid | Conductor/grid and rod geometry, soil measurements/model, fault-current input and shock duration | GroundMat's field solution is not a substitute for a network fault-current study. [SK16] |

## 5. Studies and modules

| IDs / module | Method, options and required data | Outputs, standards and limits |
|---|---|---|
| S1, S3, S7, S9, C1/C4/C7: DAPPER | Network power flow with ZIP loads, regulated generation and islands; demand/loading and sizing data | Voltages/angles, P/Q, losses, feeder/transformer sizes and schedules. Its basic fault method omits machine AC decay; do not substitute it for every duty study. [SK8] |
| F3, F7: A_FAULT | ANSI C37 duty, separate LV/MV/HV treatment, AC/DC decay, local/remote generation and X/R treatment | E/X and E/Z related quantities and duty/decay results. Exact applicable editions must be checked. [SK9] |
| F1, F2: IEC 60909 | Equivalent-source and sequence networks for three-phase, SLG, LL and LLG faults; voltage factors, taps and earthing | Initial, peak, breaking, steady and DC-component results; public page does not settle the implemented standard edition. [SK10] |
| P1, P2: CAPTOR | Manufacturer TCCs, fault-current termination, equipment damage/inrush and backup interval review | Coordinated diagrams, settings and DXF/PDF outputs. [SK5] |
| P3, P5: Auto Coordination and Evaluation | Rule-driven setting/frame adjustments, minimum-change attempts and review/revert; requires DAPPER and CAPTOR | Pass/fail/warning reports. Automatic proposals require engineering review; no mathematical global optimum is established. [SK7] |
| A1-A3: Arc Flash | Device clearing and contribution-dependent energy accumulation; parallel sources, current limitation, differential/ZSI representation and selectable induction contribution | Energy, boundary, labels/permits and AC/DC studies; DC requires its module. SK26 names IEEE 1584-2018 and NFPA 70E-2024; method/range and option validation remain separate. [SK6][SK26] |
| M2, M3: TMS | Repeated network solution coupled to motor acceleration, inertia/load torque and multiple start sequences | Voltage, speed, torque, current and P/Q traces, stalled/reaccelerating motors and start times. [SK11] |
| H1, H2: HI_WAVE | Frequency-dependent current-injection network solution, source phases, sequence transformation and filter data | Impedance scans, distortion and frequency/time displays. Sparse-matrix current injection is stated; exact numerical library is not. [SK12] |
| T1, T2, T5: I*SIM | Flux-based machine/control models, excitation/governor/PSS library, graphical custom controls and switching/fault events | Time traces and interaction with islands/load transfer. This does not establish instantaneous EMT switching support. [SK13] |
| S10, F2/F8: Unbalanced | One-, two- and three-phase/sequence representations, special transformers and simultaneous faults | Unbalanced load-flow and fault results. A separate module, not proof every balanced case is converted without review. [SK14] |
| S12, F5, C5: DC Systems | Physical DC load flow, duty-cycle battery sizing and transient fault models; battery/rectifier/load data | IEEE 485/1115 battery-sizing and IEEE 946/IEC 61660 fault functions are named. Exact revisions and chemistry coverage require confirmation. [SK15] |
| C6: GroundMat | Finite-element grid/rod/soil potential calculation | Step/touch and surface-potential outputs; IEEE 80 and IEC 479 are named without verified current editions. [SK16] |

## 6. Workflow and interface

A defensible PTW workflow is to enter and check component data, choose the study
setup, run studies, apply a selected result datablock, then create a CAPTOR TCC and
reports. The public tutorial illustrates component editing, library selection and
report management, not a benchmark for the current solver. [SK18]

For arc flash, SKM's FAQ distinguishes trip delay from breaker opening time and
warns that the LV TCC may already include the latter. Another FAQ explains why a
larger bolted current need not produce the largest incident energy: device timing
and the current seen by the device matter. **Inference:** our review display should
show total arcing current, device contribution, curve segment, opening-time treatment
and the scenario that set the reported worst case. [SK17][SK19]

### 6.1 Main failure, maintenance settings and changing contributions

**A1/A2, P4.** The explicitly V7.0 article separates normal load-side exposure,
upstream clearing when a main fails, and the maintenance-function selection. Its
algorithmic main designation follows the greatest share of fault contribution;
a tie or feeder can qualify. This is not necessarily the device an engineer
calls the incomer. Maintenance settings are a distinct operating state and can
sacrifice selectivity. These are historical documented semantics, not proof of
every V11 dialog/default. [SK21]

The utility-data article shows why source impedance and available current are
insufficient: service-transformer primary protection and upstream conductors also
matter. Depending on its characteristic and the chosen duration cap, including
primary protection can either alter energy or leave the result unchanged. Its old
hazard-category language is not adopted as present-day safety guidance. [SK22]

The generator-decrement knowledge-base example compares the duration of an initial
current level with relay operation plus breaker opening. If current falls before
that interval completes, pickup/clearing can differ; subsequent operation is
re-evaluated at the reduced contribution. It demonstrates an option interaction,
not a universal generator decrement law or independently tested relay-memory model.
**Inference:** trace the contribution timeline, protective state, opening delay and
any time cap separately; a final trip-time scalar loses the reason for the result.
[SK23]

### 6.2 Thermal cable analysis and mechanical installation are separate

**C2.** Cable Ampacity advertises steady-state temperature from current or ampacity
from a conductor-temperature limit, including neighbouring cables and external
heat. It names IEC 60287 and Neher-McGrath where the former does not apply, including
non-unity load factor. Air, duct-bank and buried installations are listed. These
are vendor method/compliance claims, not independent certification or evidence of
transient thermal ageing. Exact standard edition, constants and detailed soil/
boundary inputs remain unverified. [SK24]

**C3.** Cable-3D calculates cumulative tension, per-segment sidewall pressure,
clearance/fill and jam ratios, for forward/reverse pulls and several cable
arrangements. It has cable/raceway/lubricant libraries and a 3D profile view.
This closes the advertised pulling-capability gap; the source does not provide
friction equations, every unit/default, or a complete reproducible benchmark.
A pulling profile is not an overhead sag study. [SK25]

### 6.3 A dated vendor standards statement

The page titled SKM IEEE Certification 2026 is signed by Johnny Ma of SKM and
dated 20 January 2026. It states in-house validation and lists IEEE 1584-2018,
NFPA 70E-2024, IEEE 519-2014 and IEEE 80-2000 among its references. IEC 60909 is
listed without an edition. Treat this as a vendor declaration with named editions,
not an independent IEEE-issued certificate, public test report or proof that all
modules implement the latest revision. [SK26]

## 7. Dated user evidence

`gepman`, 11 December 2007, reported finding SKM coordination easier than ETAP
in their own use. `dpc` recommended trying real models, reports and database work
before choosing. These are attributed historical preferences, not a current usability
ranking or evidence of unsupported ETAP functionality. [U3]

The 2013 arc-flash comparison in EasyPower section 7 involved an old SKM report,
not a repeatable test with matched input files. It remains unresolved and cannot
establish which result was right. [U2]

## 8. Engines implied

The advertised module split implies a shared network/data layer, demand and power
flow, several fault formulations, TCC interpolation and operation logic, setting
rules, arc-energy accumulation, harmonic frequency solution, machine/control DAE
simulation, DC discharge/fault models and a separate earthing field solver. These
are inferred responsibilities, not reverse-engineered SKM architecture. [SK8][SK9][SK10][SK5][SK7][SK6][SK12][SK13][SK15][SK16]

## 9. Explicit gaps

| Gap | Why it remains open / action |
|---|---|
| Site-specific total price | Bus count, package, network/concurrency, maintenance and separate services affect the public list. Obtain a scoped offer. [SK2] |
| Version 11 standard editions and complete model inventory | Several module pages are undated; the older tutorial cannot close edition/model-default questions. [SK4][SK18] |
| Solver integration, tolerances and current reproducible validation cases | Not exposed in the public module pages read; no licence test was run. [SK11][SK13] |
| D9/D14/D16 breadth, P6/P8, T3/T4, H3, C8 | No sufficient public source was read. C2 thermal and C3 pulling now have advertised module evidence, with numerical/schema gaps retained in section 6.2. [SK24][SK25] |

# NEPLAN

## 1. Identity, versions, editions, licensing and platform

PSI Neplan AG offers NEPLAN V10 on premises and NEPLAN 360 in the cloud. The
public family descriptions establish client-server deployment and modular licensing,
not the exact current executable build. The electricity portfolio spans industrial,
distribution and transmission studies. [NP1][NP3]

V10 is described as purchased software with optional maintenance after the first
year; 360 is leased with annual support/updates. SQL Server/Express and Microsoft
Azure cloud hosting are documented. Standalone, intranet and hosted deployments
have different access arrangements. Exact current supported desktop OS versions
were not established from a release-specific requirements document. [NP2][NP21]

An undated public order form lists the cloud Engineering Package at EUR 2,750 per
licence for 50 nodes and EUR 3,950 for 100 nodes. The PDF does not specify the price
period, tax treatment or issue date. Its `/2023/07/` URL path is not proof of a current
2026 quote. The general annual cloud description does not settle that form's exact
commercial term. [NP23][NP2]

**Conflicting demo limits:** the licensing page says 15 nodes; the dedicated
free-demo/student page says 50 nodes for six months, noncommercial cloud use.
Do not silently choose one as universally current; confirm the offered entitlement.
[NP2][NP22]

## 2. Sources

| ID | URL and title | Type | Accessed |
|---|---|---|---|
| NP1 | [NEPLAN Electricity overview](https://neplan.ch/neplanproduct/en-electricity/) | Vendor public page/help | 2026-10-16 |
| NP2 | [NEPLAN licensing](https://neplan.ch/informationbox/licensing-2/) | Vendor public page/help | 2026-10-16 |
| NP3 | [PSI: NEPLAN V10 and 360](https://www.psi.de/en/solutions/products/neplan-v10-360) | Vendor public page/help | 2026-10-16 |
| NP4 | [Network Modelling](https://neplan.ch/description/network-modelling-2/) | Vendor public page/help | 2026-10-16 |
| NP5 | [Data and Study Case Handling](https://neplan.ch/description/data-and-study-case-handling-2/) | Vendor public page/help | 2026-10-16 |
| NP6 | [Libraries](https://neplan.ch/description/library-manager-2/) | Vendor public page/help | 2026-10-16 |
| NP7 | [Load Flow and Contingency Analysis](https://neplan.ch/description/load-flow/) | Vendor public page/help | 2026-10-16 |
| NP8 | [Short Circuit Analysis](https://neplan.ch/description/short-circuit-analysis-3/) | Vendor public page/help | 2026-10-16 |
| NP9 | [Arc Flash Calculation](https://neplan.ch/description/arc-flash-calculation-2/) | Vendor public page/help | 2026-10-16 |
| NP10 | [Overcurrent Protection](https://neplan.ch/description/overcurrent-protection-2/) | Vendor public page/help | 2026-10-16 |
| NP11 | [Distance Protection](https://neplan.ch/description/distance-protection-2/) | Vendor public page/help | 2026-10-16 |
| NP12 | [Motor Starting](https://neplan.ch/description/motor-starting-3/) | Vendor public page/help | 2026-10-16 |
| NP13 | [Stability Analysis RMS](https://neplan.ch/description/rms-calculation-2/) | Vendor public page/help | 2026-10-16 |
| NP14 | [EMT Analysis](https://neplan.ch/description/emt-calculation-2/) | Vendor public page/help | 2026-10-16 |
| NP15 | [PSS/E and other import/export interfaces](https://neplan.ch/description/psse-import/) | Vendor public page/help | 2026-10-16 |
| NP16 | [Harmonic Analysis](https://neplan.ch/description/harmonic-analysis-2/) | Vendor public page/help | 2026-10-16 |
| NP17 | [Optimal Power Flow](https://neplan.ch/description/optimal-power-flow/) | Vendor public page/help | 2026-10-16 |
| NP18 | [Cable Sizing](https://neplan.ch/description/cable-sizing-2/) | Vendor public page/help | 2026-10-16 |
| NP19 | [Protection Data Management System](https://neplan.ch/description/protection-data-management-system-pdms/) | Vendor public page/help | 2026-10-16 |
| NP20 | [Programming Library](https://neplan.ch/description/neplan-programming-library-cc-2/) | Vendor public page/help | 2026-10-16 |
| NP21 | [NEPLAN technologies](https://neplan.ch/informationbox/technologies-2/) | Vendor public page/help | 2026-10-16 |
| NP22 | [Free demo and student request](https://neplan.ch/en-demo-request/) | Vendor public page/help | 2026-10-16 |
| NP23 | [Engineering Package order form, undated PDF](https://www.neplan.ch/wp-content/uploads/2023/07/EngineeringPackage_OrderForm.pdf) | Vendor public PDF | 2026-10-16 |
| U4 | [Eng-Tips: NEPLAN convergence issues, August 2019](https://www.eng-tips.com/threads/resolving-converge-issues-in-neplan.456820/) | Independent author/developer | 2026-10-16 |

## 3. Architecture and data model

**D1, D4-D6, D12.** Study modules share a database. Equipment dialogs check
plausibility and indicate fields required by different analyses. Variants form a
parent/child tree storing differences, with operating switch/loading states,
time-dependent component availability and comparison/merge operations. Results
from two variants can share a diagram label or comparison chart. [NP5]

**D9.** SQL-backed client-server work includes user/group rights and locking to
reduce overwrite conflicts. Standalone needs no internet; intranet and cloud access
use managed accounts. Versioning and variant merge are documented, but conflict
resolution granularity is not fully public. The OEM C# interface is evidence of an
API, not proof that the entire solver is written in C#. [NP21]

**D2, D11.** The library manager supports standard equipment, manufacturer protection,
machine/control models, harmonic sources and profiles, with network-to-library
exchange and updates from changed library data. Category-level vendor claims do
not establish a complete release-specific inventory or each manufacturer's current
curve revision. [NP6]

## 4. Element catalogue and parameters

| Element family | Publicly established parameters/meaning | Units or schema limit |
|---|---|---|
| Network/node and switching | Phase/neutral/earth configuration; grounded/isolated/resonant earthing; area/zone/feeder/substation; breaker/disconnector state | One-, two-, three-phase AC and physical DC are distinguished. [NP4] |
| Line/cable/transformer | Tower/conductor geometry and mutual effects; two/three/four-winding and phase-shifting transformers, tap control | Complete dialog units/defaults require the detailed manual. [NP4] |
| Sources, loads and converters | Synchronous/asynchronous machines, external grid, composite/profile loads, HVDC/VSC, storage and DC motors/loads | The presence of a component does not establish every study's model fidelity. [NP4] |
| Overcurrent device | Pickup and time settings; directional phase/earth functions; point/formula characteristic and permitted setting ranges | Curves can be referenced across voltage levels; exact curve constants are not reproduced. [NP10] |
| Distance relay | R-X reach/shape, zone delays, CT/VT transformation, primary or secondary impedance, binary signalling | Mho, polygon and point-defined shapes; detailed parameter units/schema remain manual-dependent. [NP11] |
| Motor/load | Torque, current and power factor versus slip; starter and load-torque curve; saturation/loss options | Least-squares parameter identification is documented, without copying fitted example values. [NP12] |
| Arc-flash location | Working distance, arcing-current contribution, device clearing and selected method | Energy and clearing-time outputs are documented; full electrode/enclosure input schema is not established here. [NP9] |

## 5. Studies and modules

| IDs / study | Method, options and inputs | Outputs, standards and limits |
|---|---|---|
| S1, S4-S7, S10-S12, S16: load flow | Newton/extended Newton, current iteration and per-phase backward/forward sweep; linear DC power flow is distinct from physical DC network analysis. Tap/remote control, distributed slack, converters and scaling are described | Violations, sortable/filterable tables, network graphics, sensitivities and scenario comparison; convergence controls and erroneous-data indication. [NP7] |
| S15: contingencies | Outage lists, common-mode failures and load-flow re-solves; optional remedial event logic | Severity ranking and violations. RAS is separately licensed with load flow/contingency modules. [NP7] |
| F1-F6, F8: faults | IEC 60909 editions including 2016, ANSI C37, IEC 61363 and IEC 61660; superposition from prefault load flow; sequence coupling, earthing and converter contributions | Initial/peak/breaking/steady/thermal and DC quantities; phase/sequence lists, diagram results and rating warnings. Multiple/open-conductor and user-defined fault configurations are advertised. [NP8] |
| P1, P2, P4: overcurrent selectivity | Manufacturer or custom point/formula TCCs; directional/non-directional phase/earth settings; damage/start curves; fault-clearing sequence in meshed networks | Editable TCCs, current markers, setting diagrams and PDF/Word/PNG exports. Curve dragging alone does not prove automatic optimal settings. [NP10] |
| P5, P6: distance protection | Network impedances, coupling, infeed, relay shapes/zones and CT/VT; manual/automatic setting and protection interaction | R-X plots, tripping schedules/times, fault-location estimates and RIO exchange. Dynamic signalling such as permissive transfer trip is described. [NP11] |
| A1-A4: arc flash | Coupled to faults and overcurrent protection; reduced/unreduced arcing current and individual contributions; IEEE 1584-2018, NFPA, DC methods and Lee fallback are advertised | Energy, clearing time, labels, diagrams and Word/Excel tables. Page also says `IEEE 1584-2013`, an unverified edition label; do not adopt it as a standard. Lee fallback is not proof of universal HV validity. [NP9] |
| M1-M4: motor starting | Initial voltage-dip option or time-dependent multiple starts; least-squares motor fitting, torque/slip curves and starter models | Voltage/current/P/Q, motor/load torque and slip/time plots, violation alerts and spreadsheet-ready results. [NP12] |
| T1-T3, T5: RMS | Symmetrical DQ0 or asymmetrical ABC, AC/DC hybrid continuous/discrete events, fixed/variable stepping; NSL-SymDef or block models compiled to DLLs | Machine/control/protection traces, FFT, event groups and eigenvalue/sensitivity applications. Exact integrator and tolerances are not public here. [NP13] |
| T4: EMT | Instantaneous phase-domain hybrid simulation; shares user-modelling framework and requires RMS | Switching, inrush/ferroresonance and related transient studies, waveforms/FFT and COMTRADE exchange. No independently checked numerical benchmark is supplied by this dossier. [NP14] |
| H1, H2: harmonics | Frequency-dependent phase/sequence networks, source spectra, filter and adaptive frequency scan | Harmonic voltages/currents, resonance/distortion, TIF and filter assessment. Exact standard editions/default limits remain unverified. [NP16] |
| S14: OPF | AC constraints, configurable generation/tap/shunt/HVDC controls; cost/loss objectives, N-1 and multi-period storage/ramping variants | Dispatch, binding limits and network displays. The page describes primal-dual interior-point methods as typical; this does not identify the shipped backend unconditionally. [NP17] |
| C1: cable sizing | Library cable/protection data; ampacity, voltage drop, fault/disconnection and motor-start criteria with selected IEC/VDE/NEC context | Selected cable and constraint assessment; not proof of a detailed thermal installation model or Zambian compliance. [NP18] |

## 6. Workflow and interface

Engineers can build schematic or geographical projects, choose operating states and
planning variants, run a selected study and inspect labelled/coloured results,
charts and tables. Import/export includes GIS, CIM/CGMES, UCTE, tabular and proprietary
XML routes. Python/C# scripting and web services support automation. These are
advertised interfaces; preservation of every foreign model is a separate question.
[NP3][NP20]

The PSS/E interface specifically lists RAW, sequence and dynamic data. **Inference:**
interchange acceptance should separately count imported buses/branches, sequence
records, model names and rejected/defaulted parameters, then check initialization.
Format support alone cannot establish equal results. [NP15][PS8][PS9]

**NP-P1, field-setting management:** PDMS is a browser-based protection-data system
with role/history management, CT/VT and relay information, documents and disturbance
records, linked to the desktop analysis model. This is separate from plotting a
TCC or computing a trip time. **Inference:** Quantic should keep installed settings,
proposed settings and calculation snapshots distinct. [NP19]

## 7. Dated user evidence

`KAPAKAPA`, Eng-Tips, 15 August 2019, reported AC7B/UEL connection and initialization
problems when transferring parameters from a PSS/E model, plus different responses
after edits. No reproducible file, version-specific diagnosis or resolution appears
in the thread read. This is a useful migration/initialization concern, not proof of
a current NEPLAN defect or an unsupported current AC7B model. [U4]

## 8. Engines implied

The sources imply a phase/sequence AC/DC network model, multiple load-flow methods,
standard-specific fault solvers, TCC/relay-state logic, arc-energy methods,
nonlinear motor identification/acceleration, hybrid RMS and EMT simulation,
linearization/eigenanalysis, frequency-domain harmonics, constrained AC optimization
and cable selection rules. SQL, web services and model DLLs are separate data and
integration responsibilities. These are inferred boundaries, not claims about
NEPLAN's internal source modules. [NP7][NP8][NP10][NP11][NP9][NP12][NP13][NP14][NP16][NP17][NP18][NP21]

## 9. Explicit gaps

| Gap | Why it remains open / action |
|---|---|
| Current complete commercial quote | Engineering form is undated and omits term/tax; full-module prices are not established. [NP23] |
| Demo limit | Public pages conflict, 15 versus 50 nodes; confirm at enrolment rather than choosing silently. [NP2][NP22] |
| Exact executable build, OS/compiler requirements and library defaults | Family/module descriptions are not a versioned installation or model reference. [NP3][NP6] |
| Arc-method edition and applicability | Vendor's 2013 label is unresolved; generic fallback wording does not close voltage/range limits. [NP9] |
| Integrator/backend identity and current independently reproducible accuracy | Algorithms are described selectively; OPF wording is qualified, RMS/EMT pages do not expose all details. [NP13][NP14][NP17] |
| P3/P7/P8 full breadth, H3, C2-C8 | Some component/module names exist, but sufficient scoped method/parameter evidence was not read. Unknown, not absent. |

# Siemens Gridscale X PSS/E

## 1. Identity, versions, editions, licensing and platform

Siemens markets Gridscale X PSS/E, with the public release page listing version
36.3.1 and Intel oneAPI 2025.1 IFX support. This concerns supported model-build tools;
it does not reveal the language of the whole solver. Public product material targets
large system planning, including node-breaker representation. [PS2]

The monthly package page displayed these prices on 2026-10-16. EUR and USD are
vendor-listed alternatives, not our currency conversion. [PS1]

| Monthly package | EUR/month | USD/month | Advertised increment |
|---|---:|---:|---|
| Base | 3,415 | 3,830 | Power flow, contingencies, PV/QV, scripting, GUI/contours |
| Standard | 5,300 | 5,940 | Adds line properties, short circuit and dynamics |
| Advanced | 8,835 | 9,900 | Adds Python RAS, OPF, GIC and advanced linear analysis |
| Expert | 11,660 | 13,070 | Adds harmonics and time-series power flow |

The June 2025 product sheet limits monthly licensing to one fixed physical PC,
without moves or VM installation. It separately describes longer term and network,
movable and borrowable licences, subject to the order. Thus the monthly restriction
must not be applied to all PSS/E deployments. Exact current Windows/Python
installation requirements were not independently established here. [PS3]

## 2. Sources

| ID | URL and title | Type | Accessed |
|---|---|---|---|
| PS1 | [Siemens PSS/E version 36 monthly packages](https://www.siemens.com/en-us/products/pss-software/psse-version-36/) | Vendor public page/help | 2026-10-16 |
| PS2 | [Gridscale X PSS/E product, modules and releases](https://www.siemens.com/en-us/products/pss-software/gridscale-x-pss-e/) | Vendor public page/help | 2026-10-16 |
| PS3 | [PSS/E On Premise Product Sheet, effective 25 June 2025](https://assets.ctfassets.net/17si5cpawjzf/2bmyCWcftF05pQ5w9nQjca/26f7b562e1201962c0c08ead2bfa9666/PSS-E-Product-Sheet.pdf) | Vendor public PDF | 2026-10-16 |
| PS4 | [Dynamic Simulation datasheet, 2014](https://assets.new.siemens.com/siemens/assets/api/uuid:4b1f3ce6b48087b038f806c74f8f05f623b09a4a/pti-ff-en-swpe-dynsimul-1412.pdf) | Vendor public PDF | 2026-10-16 |
| PS5 | [Graphical Model Builder datasheet, 2018 copyright](https://assets.new.siemens.com/siemens/assets/api/uuid:128b63efc3e8be0c56782bdf48b7121a5647f1c2/pti-ff-en-sw-gmb-1411.pdf) | Vendor public PDF | 2026-10-16 |
| PS6 | [Optimal Power Flow datasheet, 2014](https://assets.new.siemens.com/siemens/assets/api/uuid:27e9879f51bca33eea4616f85925b1ae69286bf2/pti-ff-en-swpe-optpowflow-1412.pdf) | Vendor public PDF | 2026-10-16 |
| PS7 | [Advanced Linear Analysis datasheet, 2020](https://assets.new.siemens.com/siemens/assets/api/uuid:b03ee865-001e-4d2c-9e32-9cdfd407bc6b/pss-e-adv-lin-analysis-module-datasheet-EN-v1.pdf) | Vendor public PDF | 2026-10-16 |
| PS8 | [ANDES 1.7.3: PSS/E RAW and DYR](https://docs.andes.app/en/v1.7.3/getting_started/formats/psse.html) | Independent author/developer | 2026-10-16 |
| PS9 | [Hantao Cui: CURENT WECC verification, revised 23 May 2020](https://docs.andes.app/en/stable/verification/andes-wecc-verification.html) | Independent author/developer | 2026-10-16 |

## 3. Architecture and data model

**D1, D6, D14.** The base platform combines steady-state network data,
contingencies, voltage-stability workflows, scripting and graphics, with separate
licensed simulation modules. The product sheet makes the order form authoritative
for module configuration and deployment. A generic FAQ mentioning dynamics should
not override the explicit package split. [PS3][PS1]

**D16.** RAW contains steady-state network data; DYR contains dynamic model
parameters. They are complementary rather than interchangeable complete cases.
The ANDES 1.7.3 importer supports RAW 32/33 and only models implemented in ANDES;
it documents limitations for switched shunts, transformer flags and HVDC, and
errors on unknown DYR models. These are that importer's limits, not limits of
native PSS/E 36. [PS8]

## 4. Element catalogue and model library

| Family | Evidence and key modelling information | Boundary |
|---|---|---|
| Bus, branch, generator, load and substation | Power-flow network with node-breaker topology, large-network capacity and renewable/FACTS representation | Public capacity is a vendor limit claim, not a measured runtime. Detailed version 36 field/default schema was not obtained. [PS2] |
| Machine and controls | Synchronous machine, exciter, turbine-governor, PSS, excitation limiters and turbine-load controls | 2014 category catalogue remains historical evidence, not a complete 36.3.1 list. [PS4] |
| Renewable/control devices | Wind mechanical, pitch and electrical controls; HVDC, FACTS/SVC and tap/phase controls | Generic category support does not prove compatibility with every supplied user DLL. [PS4] |
| Protection/load dynamics | Load and line relays, loads and disturbance actions | Dynamic relay simulation is not proof of an industrial TCC, arc-flash or field-setting management package. [PS4] |
| Named models in independent comparison | GENROU, TGOV1, IEEEG1, EXST2, EXDC2, ESST3A, IEEEST, ST2CUT and ESDC2A | Cui's 2020 study exercises these names; no model equations, defaults or dataset are copied here. [PS9] |
| DYR identity and parameters | GENCLS record links bus and generator ID to inertia H and damping D | The importer maps inertia conventions, M = 2H, and retrieves base data from the linked machine. Do not mistake a positional record for a self-contained model definition. [PS8] |

For a release-specific model library, names alone are insufficient. **Inference:**
an interoperable model contract needs version, parameter order/units/bases, limiter
and saturation conventions, initialization equations and linked IDs, plus any
required DLL. The documented importer and comparison show why these distinctions
matter. A complete public version 36 model reference was not found. [PS8][PS9]

## 5. Studies and modules

| IDs / study | Purpose, method, options and inputs | Outputs and limits |
|---|---|---|
| S1, S15, S17: core planning | Power-flow network, contingency list/corrective actions, transfer and PV/QV studies; node-breaker topology | Violations, curves and graphical/contour results. Exact current NR/decoupled method choices and convergence defaults are not established by these product pages. [PS2][PS3] |
| F1-F3: short circuit | Separately licensed balanced/unbalanced fault calculation using network/fault data | Standard package includes the module; exact IEC/ANSI editions, duty corrections and report fields require the module manual. Do not assert complete F1-F3 parity from the name alone. [PS1][PS2] |
| T1, T5: Dynamic Simulation | Machine/control library and user models; initialization checks, fault/trip/start events, long-term response | Time channels/plots, interruption/restart and automation; 2014 brochure describes variable stepping for extended runs. It does not establish every current integrator setting. [PS4] |
| T2: Graphical Model Builder | Separate companion for block models, initialization, mathematical/logic functions and DLL interfaces | Open/closed-loop debugging and documentation. Portfolio brochure's no-external-compilation workflow must not be generalized to directly compiled PSS/E user DLLs. [PS5][PS2] |
| S14: OPF | Generation, shunt/tap and other controls with cost/loss/transfer objectives; voltage, branch, interface and generation limits | Optimized operating point and constraint assessment. Historical brochure does not identify a solver backend; its unique-global-optimum marketing claim is not adopted as an AC nonconvex guarantee. [PS6] |
| S15, S16: Advanced Linear Analysis | Linear sensitivity/impact analysis, transfer capability and security-constrained redispatch | FCITC and preventive/corrective SCED workflows. This is not itself a nonlinear transient assessment. [PS7] |
| S13, H1/H2: time series/harmonics | Optional modules, included in monthly Expert package; repeated power-flow time points and harmonic assessment are advertised | Exact harmonic network models, scans, limits and report schema require the module reference. [PS1][PS2] |
| PS-S1: GIC | Optional geomagnetically induced-current network assessment | Do not equate this specialized DC phenomenon with industrial battery/charger load flow or DC faults. [PS2] |
| T4: external EMT route | Product lists E-TRAN/PSCAD conversion and co-simulation companion extensions | Evidence of an interface, not a native PSS/E EMT solver or universal model conversion. [PS2] |

## 6. Workflow and interface

The dynamic-study sequence evidenced by the brochure is to edit/check model data,
prepare disturbances, run the simulation and inspect/export plotted quantities.
Response files and Python recording support repetition; block-model tools add
isolated/open/closed-loop testing. This is a documented workflow, not a completed
hands-on evaluation. [PS4][PS5]

**Inference for import review:** first solve the steady-state model; resolve dynamic
IDs and unsupported names; inspect machine/control initialization and limits;
apply a defined event; compare like-for-like quantities on the same bases. A RAW
load-flow match alone cannot validate a dynamic model. [PS8][PS9]

### 6.1 Dynamic user-model compatibility has a version boundary

Siemens' version 36 page describes VINDP user-model DLLs and a converter that
upgrades existing dynamic-model source to the new format. Its forward-compatibility
claim applies to DLLs created with the version 36 architecture; it is not a promise
that every earlier binary loads unchanged or that source is always available.
The API/format promise also does not establish equivalent initialization, limiter
behaviour or trajectories in another solver. [PS1]

**Inference:** distinguish source conversion, binary loading and numerical model
validation in the import ledger. Record the model format/version and unavailable
custom dependencies before claiming dynamic interoperability. Keep RAW/DYR parsing
separate from executing a vendor DLL. [PS1][PS8][PS9]

## 7. Dated independent evidence

Hantao Cui's CURENT WECC comparison, last revised 23 May 2020, reports matching
power-flow and GENROU initialization across ANDES, TSAT and PSS/E, but divergent
responses for some disturbances. It identifies machine/system current bases and
possible saturation implementation differences. The study used PSS/E's default
second-order Adams-Bashforth method in that test; it is not evidence that every
current PSS/E study uses that integrator. This is a reproducible-study discussion,
not a user-satisfaction survey or a version 36 benchmark. [PS9]

## 8. Engines implied

The documented functions imply network/topology processing, nonlinear power flow,
contingency and transfer sweeps, voltage-stability analysis, fault calculation,
machine/control dynamic equations and initialization, constrained optimization,
linear sensitivities/redispatch, harmonic networks, time sequencing and GIC.
Model compilation/import/automation are separate concerns. These are inferred
responsibilities; the vendor's closed numerical backend and complete model
implementation are not exposed by these sources. [PS2][PS3][PS4][PS5][PS6][PS7]

## 9. Explicit gaps

| Gap | Why it remains open / action |
|---|---|
| Complete current model equations, defaults and DLL compatibility | Public categories and historical brochures are not the licensed version 36 model manual. Obtain authorized reference access for any implementation-specific comparison. [PS2][PS4] |
| Exact OS/Python/compiler deployment matrix and full-term quote | Monthly and other licences differ; order/installation documents control. IFX support is only one release fact. [PS2][PS3] |
| Fault standards/duty completeness and harmonic schema | Module names do not establish every shared matrix sub-capability. Public detailed reference was not found/read. [PS2] |
| Current independent accuracy/usability benchmark | The independent technical comparison is dated 2020, not a test of 36.3.1. No licensed software was run. [PS9] |
| Industrial P1-P8/A1-A4 and C1-C8 | Dynamic relay models, an advanced protection companion or GIC do not prove an industrial coordination/arc-flash/design suite. Public native breadth remains unknown. [PS2][PS4] |
| T3 and native T4; D5/D9/D11 full breadth | The sources read do not close eigenanalysis, native EMT, collaborative revision or manufacturer-library breadth. Unknown, not absent. |

# Shared capability evidence for the parity matrix

This table selects rows for which this dossier adds useful evidence. Grouped rows
share a topic, not a claim that every part has identical coverage. `Module` means
advertised optional/packaged functionality; `partial` qualifies the evidence and
must not be converted into a blanket yes. All omitted shared rows remain unknown
for this WP. G13 is the matrix's substituted-equation reporting capability, not
PLAN decision D11 or matrix D11 manufacturer libraries.

| Shared IDs / capability | EasyPower | SKM PTW | NEPLAN | PSS/E |
|---|---|---|---|---|
| D1 shared model | Yes [EP4] | Yes [SK18] | Yes [NP5] | Partial, linked network/module data [PS3][PS8] |
| D2/D11 libraries/types | Manufacturer libraries, internal type split unknown [EP1] | Device libraries [SK5] | Equipment/control libraries [NP6] | Dynamic categories; manufacturer breadth unknown [PS4] |
| D4-D6 scenarios/studies | ScenarioManager, revision breadth partial [EP5] | Study setups; revision breadth unknown [SK18] | Variant tree and operating states [NP5] | Study automation; revision breadth unknown [PS3] |
| D9 multi-user/version merge | Unknown | Unknown | Yes, deployment-dependent [NP21] | Unknown |
| D12 validation | Import/model diagnostics [EP3][EP16] | Tutorial data workflow, full pre-run checker unknown [SK18] | Plausibility and required fields [NP5] | Dynamic-data checking [PS4] |
| D14/D15 automation | Unknown breadth | Unknown breadth | Python/C# and web services [NP20] | Python/IPLAN and repeated studies [PS3] |
| D16 interchange | Revit route, RAW/CGMES unknown [EP15] | Full foreign-format breadth unknown | RAW/SEQ/DYR and other interfaces [NP15] | RAW/DYR documented, foreign-model fidelity conditional [PS8] |
| D17 GIS | Unknown | Unknown | Yes [NP3] | Full GIS breadth unknown |
| G1/G5/G9/G11 diagram/results/reports | Yes, detailed reporting breadth qualified [EP4][EP16] | Yes [SK18] | Yes [NP3][NP7] | Yes, export breadth qualified [PS2][PS4] |
| G12 plots | TCC/time/harmonics, not every plot [EP7][EP11][EP12] | TCC/time/scan [SK5][SK11][SK12] | TCC/R-X/time/scan [NP10][NP11][NP13][NP16] | Time/PV/QV, full plot set unknown [PS2][PS4] |
| G13 substituted working | Unknown | Unknown | Unknown | Unknown |
| S1 balanced AC flow | Yes; NR identity unknown [EP10] | Yes; method identity unknown [SK8] | Yes, NR and alternatives [NP7] | Yes; current method options unverified [PS3] |
| S10 unbalanced flow | Yes [EP10] | Module [SK14] | Yes [NP7] | Unknown phase-domain breadth |
| S12 physical DC flow | Yes [EP10] | Module DC Systems [SK15] | Yes [NP7] | Unknown, GIC is distinct [PS2] |
| S13 time series | Unknown | Unknown | Advertised portfolio, details unverified [NP3] | Module [PS3] |
| S14 OPF/interior point | Unknown | Unknown | Module AC OPF; backend qualification in section 5 [NP17] | Module OPF; backend unknown [PS6] |
| S15/S16 contingencies/sensitivities | Unknown full breadth | Unknown full breadth | Modules, detailed options qualified [NP7] | Core plus Advanced Linear/RAS [PS3][PS7] |
| S17 PV/QV/modal | Unknown | Unknown | Voltage/eigenanalysis portfolio, detailed breadth unknown [NP2][NP3] | PV/QV, modal breadth unknown [PS3] |
| F1/F2/F3 faults | Advertised, editions qualified [EP6] | Separate IEC/ANSI modules [SK9][SK10] | Multiple explicit methods [NP8] | Module, detailed parity unverified [PS3] |
| F5 physical DC faults | Yes, method detail unknown [EP6] | Module [SK15] | IEC 61660 advertised [NP8] | Unknown |
| F6 superposition from load flow | Unknown | Unknown full method | Advertised [NP8] | Unknown |
| F7 rating/duty check | Yes [EP6] | Module/package-dependent [SK2][SK9] | Rating warnings, full duty scope qualified [NP8] | Unknown full scope |
| P1/P2 TCC/damage | Yes [EP7] | CAPTOR [SK5] | Overcurrent Protection [NP10] | Unknown native industrial scope |
| P3/P5 rule checks/settings | SmartPDC, limited radial scope [EP9] | Auto Coordination [SK7] | Distance settings yes; generic OC automation unknown [NP11] | Unknown native industrial scope |
| P4/P6 operation/distance | Protection interaction; distance unknown [EP13] | Simulation; distance unknown [SK13] | Both advertised [NP10][NP11] | Dynamic relays; industrial sequence/R-X breadth unknown [PS4] |
| A1/A2 AC arc/labels | Yes, exact editions qualified [EP8][EP16] | Module, exact edition qualified [SK6] | Module with 2018 stated [NP9] | Unknown |
| A3/A4 DC/HV arc | Advertised, ranges/methods conditional [EP8] | DC advertised, HV range unknown [SK6] | DC/fallback advertised, HV validity conditional [NP9] | Unknown |
| M1-M4 starting/fitting/starters | Dynamic starting/fitting, exact starter breadth qualified [EP12] | TMS, fitting breadth unknown [SK11] | Both static/dynamic and fitting [NP12] | Motor events, full industrial study unknown [PS4] |
| T1/T2/T5 RMS/custom/events | Dynamics; custom block breadth unknown [EP13] | I*SIM, custom controls [SK13] | RMS/NSL/blocks/events [NP13] | Dynamics plus GMB companion [PS4][PS5] |
| T3 eigenanalysis | Unknown | Unknown | Advertised [NP13] | Unknown |
| T4 EMT | Unknown | Unknown | Module [NP14] | External companion route; native unknown [PS2] |
| H1/H2 harmonics/filters/limits | Module [EP11] | HI_WAVE [SK12] | Module [NP16] | Module; detailed filter/scan breadth unknown [PS3] |
| H3 flicker | Unknown | Unknown | Unknown | Unknown |
| C1/C4/C7 cable/transformer/schedule design | SmartDesign, scope qualified [EP14] | DAPPER, scope qualified [SK8] | Cable sizing; other rows unknown [NP18] | Unknown |
| C5 battery sizing | Unknown | DC Systems [SK15] | Unknown | Unknown |
| C6 ground grid | Partner XGSLab; native unknown [EP23] | GroundMat [SK16] | Unknown | Unknown |
| C2 thermal ampacity | Unknown | Cable Ampacity, vendor method claim [SK24] | Unknown | Unknown |
| C3 cable pulling | Unknown | Cable-3D; numerical details unverified [SK25] | Unknown | Unknown |
| C8 overhead sag | Unknown | Unknown | Unknown | Unknown |

**Implications for Quantic, inferred from these workflows:** industrial parity needs
an auditable chain from source contribution through device timing to energy/labels,
with design and as-found settings separated. Transmission parity needs topology,
steady-state and dynamic-model initialization checked independently, plus transparent
import losses. These are research inputs for WP-2.12, not approval to implement new
engines. [EP16][SK17][SK19][NP19][PS8][PS9]
