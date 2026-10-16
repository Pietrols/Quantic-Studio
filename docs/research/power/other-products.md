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
Sparse solver, integration scheme, implementation language and numerical tolerances
remain unknown. [EP6][EP7][EP8][EP9][EP10][EP11][EP12][EP13][EP14]

## 9. Explicit gaps

| Gap | Why it remains open / action |
|---|---|
| Current numeric price and exact entitlement | Sales page directs to a quote; Revit purchase wording conflicts with tier presentation. Obtain a scoped offer. [EP1][EP15] |
| Versioned protection/dynamic library completeness | Feature pages give categories rather than a release-specific inventory, defaults and model equations. [EP7][EP13] |
| Detailed arc-method applicability and standards editions | Marketing spans methods and voltage ranges; the range of the overall product cannot be assigned to one standard. [EP8] |
| Solver tolerances, iteration/integration details and independent current benchmarks | Public pages read do not expose these. No licensed evaluation was run. [EP6][EP10][EP13] |
| D9, D13, D14 breadth; P6; T3/T4; C2/C3/C5/C6/C8 | No sufficient public evidence was found in the sources read. This is not evidence of absence. |

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
| SK3 | [SKM support](https://www.skm.com/support.html) | Vendor public page/help | 2026-10-16 |
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
| A1-A3: Arc Flash | Device clearing and contribution-dependent energy accumulation; parallel sources, current limitation, differential/ZSI representation and selectable induction contribution | Energy, boundary, labels/permits and AC/DC studies; DC requires its module. The generic page's standard names alone do not establish the current edition and every range. [SK6] |
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
| D9/D14/D16 breadth, P6/P8, T3/T4, H3, C2/C3/C8 | No sufficient public source was read. Unknown, including whether other SKM offerings cover these rows. |
