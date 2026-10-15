# PowerWorld Simulator research dossier

Research date: 2026-10-15. Owner: Lane B, ChatGPT. WP-2.11.

This is a public-documentation study, not an executable-product benchmark. Statements
about availability describe the cited documentation; no licensed Simulator instance
was run. The coverage ledger in section 9 records unresolved limits. Capability IDs
match Claude's WP-2.10 draft where the scope matches; `PW-*` identifies additional
PowerWorld distinctions. Interpretation and proposed Quantic implications are marked
as such. This dossier grants no implementation or standards-compliance approval.

## 1. Identity: vendor, current version, editions and licensing, platforms

PowerWorld Corporation develops Simulator for interconnected power-system analysis,
with an emphasis on transmission operation, planning and visualization. The public
product overview advertises cases up to 250,000 buses. That is a vendor capacity
statement, not our measured runtime or a guaranteed capacity for every study. [W1]

Version 24 is the latest major version identified in the sources read on the research
date. Its announcement and software-key page place the release in March 2025; patch
history extends into 2026. Major version and patch build must both accompany a
reproducibility record because the patch history includes solver, importer and
results-storage fixes. We do not infer an unreleased Version 25. [W2][W3][W5]

| Configuration | Documented boundary | Sources |
| --- | --- | --- |
| Commercial base | Licensed Simulator, with power flow, contingency analysis, sensitivities, fault analysis and time-step simulation | [W1][W36][W74] |
| Optional study licences | ATC, PVQV, OPF, SCOPF, reserves, transient stability, GIC and integrated topology processing | [W4] |
| Automation and orchestration | SimAuto, Scheduled Actions and distributed-analysis licences have separate purchase entries | [W4] |
| Demonstration | Free 13-bus evaluation includes ATC, PVQV and OPF/SCOPF; it is not evidence that every add-on is unlocked | [W1] |
| Educational editions | University teaching/research configurations are offered; terms must be checked for the intended use | [W1] |
| Viewer | Separate freeware for exchanging and displaying cases; its existence does not confer an editing or simulation licence | [W1] |

The accessed pricing page lists the commercial base starting at US$11,000 and
separate add-on prices. It describes single, site and corporate configurations and
maintenance. These are a dated public-price observation, not a quotation for Peter.
No proprietary source-code licence was found. [W4]

The documented automation platform is Windows COM. Current UDM instructions describe
64-bit DLLs after the move to 64-bit-only Simulator. These establish a Windows/native
DLL dependency for these integration paths, not a verified current Windows-version
support matrix. Native macOS/Linux support and exact current minimum RAM/OS remain
unverified in section 9. [W6][W7]

## 2. Sources: numbered table

Every entry was accessed on 2026-10-15. `Help` means a vendor-published online help
topic. Product pages are capability/licensing evidence, not independent performance
validation. Historical utility presentations are dated observations. Only paraphrases
and citations are committed; downloaded source files stay outside this repository.

| No. | Title and public URL | Type | Accessed |
| --- | --- | --- | --- |
| W1 | [Simulator overview](https://www.powerworld.com/products/simulator/overview) | Vendor public page | 2026-10-15 |
| W2 | [Version 24 changes](https://www.powerworld.com/products/simulator/whats-new) | Vendor public page | 2026-10-15 |
| W3 | [Simulator 24 patch history](https://www.powerworld.com/patch-releases/simulator-24) | Vendor public page | 2026-10-15 |
| W4 | [Simulator pricing](https://www.powerworld.com/download-purchase/how-to-purchase/pricing) | Vendor public page | 2026-10-15 |
| W5 | [Software keys](https://www.powerworld.com/download-purchase/software-keys) | Vendor public page | 2026-10-15 |
| W6 | [SimAuto](https://www.powerworld.com/products/simulator/add-ons-2/simauto) | Vendor public page | 2026-10-15 |
| W7 | [UDM quick start](https://www.powerworld.com/UserDefinedModelDocumentation/Quick_Start_for_User_Defined_Models.pdf) | Public PDF | 2026-10-15 |
| W8 | [Model Explorer](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Model_Explorer.htm) | Help | 2026-10-15 |
| W9 | [Display objects versus model](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Relationship_Between_Display_Objects_and_the_Power_System_Model.htm) | Help | 2026-10-15 |
| W10 | [Case formats](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Case_Formats.htm) | Help | 2026-10-15 |
| W11 | [Format differences](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Differences_In_File_Formats.htm) | Help | 2026-10-15 |
| W12 | [Difference Case](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Difference_Flows.htm) | Help | 2026-10-15 |
| W13 | [Data Check overview](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Data_Check_Overview.htm) | Help | 2026-10-15 |
| W14 | [Undo command](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Undo_Command.htm) | Help | 2026-10-15 |
| W15 | [Solution storage](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Power_Flow_Solution_Storage.htm) | Help | 2026-10-15 |
| W16 | [Bus edit dialog](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Bus_Options_Edit_Mode.htm) | Help | 2026-10-15 |
| W17 | [Branch parameters](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transmission_Line_Transformer_Options_Parameters.htm) | Help | 2026-10-15 |
| W18 | [Branch edit dialog](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transmission_Line_Transformer_Options_Edit_Mode.htm) | Help | 2026-10-15 |
| W19 | [Transformer control](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transmission_Line_Transformer_Options_Transformer_Control.htm) | Help | 2026-10-15 |
| W20 | [Generator power and voltage](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Generator_Information_Power_and_Voltage_Control.htm) | Help | 2026-10-15 |
| W21 | [Generator fault parameters](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Generator_Options_Fault_Parameters.htm) | Help | 2026-10-15 |
| W22 | [Load information](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Load_Options_Load_Information.htm) | Help | 2026-10-15 |
| W23 | [Switched shunt control](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Switched_Shunt_Control.htm) | Help | 2026-10-15 |
| W24 | [SVC control](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Switched_Shunt_SVC_Control_Mode.htm) | Help | 2026-10-15 |
| W25 | [VSC DC line](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/VSC%20DC%20Line%20Dialog.htm) | Help | 2026-10-15 |
| W26 | [LCC converter parameters](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/DC_Line_Options_Rectifier_Parameters.htm) | Help | 2026-10-15 |
| W27 | [Multi-terminal DC line](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Multi_Terminal_DC_Line_Information.htm) | Help | 2026-10-15 |
| W28 | [Mutual impedance](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Mutual_Impedance_Record_Dialog.htm) | Help | 2026-10-15 |
| W29 | [Three-winding transformer](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Three_Winding_Transformer_Information.htm) | Help | 2026-10-15 |
| W30 | [Solving power flow](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Solving_the_Power_Flow.htm) | Help | 2026-10-15 |
| W31 | [Power-flow solution theory](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/PowerFlow%20Solution%20Theory.htm) | Help | 2026-10-15 |
| W32 | [Power-flow common options](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Power_Flow_Solution_Common_Options.htm) | Help | 2026-10-15 |
| W33 | [Power-flow advanced options](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Power_Flow_Solution_Advanced_Options.htm) | Help | 2026-10-15 |
| W34 | [DC approximation options](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Power_Flow_Solution_DC_Options.htm) | Help | 2026-10-15 |
| W35 | [Limit monitoring](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Limit_Monitoring_Settings.htm) | Help | 2026-10-15 |
| W36 | [Contingency introduction](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/contingency_analysis_an_introduction.htm) | Help | 2026-10-15 |
| W37 | [Contingency modeling](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Contingency_Options_Tab_Modeling.htm) | Help | 2026-10-15 |
| W38 | [Contingency DC screening](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Contingency_Options_Tab_DC_and_Screening_Options.htm) | Help | 2026-10-15 |
| W39 | [Contingency actions](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Contingency_Analysis_Available_Contingency_Actions.htm) | Help | 2026-10-15 |
| W40 | [Contingency remedial actions](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Contingency_Remedial_Actions.htm) | Help | 2026-10-15 |
| W41 | [Contingency combinations](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/contingency_combo_analysis_dialog.htm) | Help | 2026-10-15 |
| W42 | [PTDF dialog](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Power_Transfer_Distribution_Factors_Dialog.htm) | Help | 2026-10-15 |
| W43 | [LODF calculation](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Line_Outage_Distribution_Factors_LODFs.htm) | Help | 2026-10-15 |
| W44 | [Loading relief sensitivities](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transmission_Loading_Relief_Sensitivities.htm) | Help | 2026-10-15 |
| W45 | [ATC analysis](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/ATC_Analysis.htm) | Help | 2026-10-15 |
| W46 | [ATC single linear step](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/ATC_Analysis_Methods_Single_Linear_Step_SL_.htm) | Help | 2026-10-15 |
| W47 | [ATC iterated linear](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/ATC_Analysis_Methods_Iterated_Linear_Step_IL_.htm) | Help | 2026-10-15 |
| W48 | [ATC full-contingency iteration](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/ATC_Analysis_Methods_Iterated_Linear_Step_IL_then_Full_CTG_Solution.htm) | Help | 2026-10-15 |
| W49 | [Transfer limiters](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transfer_Limiters_Display.htm) | Help | 2026-10-15 |
| W50 | [PVQV overview](https://www.powerworld.com/products/simulator/add-ons-2/simulator-pvqv) | Vendor public page | 2026-10-15 |
| W51 | [PV curves](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/PV_Curves.htm) | Help | 2026-10-15 |
| W52 | [QV curves](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/QV_Curves.htm) | Help | 2026-10-15 |
| W53 | [OPF product](https://www.powerworld.com/products/simulator/add-ons-2/simulator-opf) | Vendor public page | 2026-10-15 |
| W54 | [OPF primal LP](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/OPF_Primal_LP.htm) | Help | 2026-10-15 |
| W55 | [OPF constraints](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/OPF_Equality_and_Inequality_Constraints.htm) | Help | 2026-10-15 |
| W56 | [SCOPF overview](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Security_Constrained_OPF_Overview.htm) | Help | 2026-10-15 |
| W57 | [Reserve optimization](https://www.powerworld.com/products/simulator/add-ons-2/simulator-opf/opf-reserves) | Vendor public page | 2026-10-15 |
| W58 | [Transient overview](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transient_Stability_Overview.htm) | Help | 2026-10-15 |
| W59 | [Numerical integration](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transient_Stability_Integration.htm) | Help | 2026-10-15 |
| W60 | [Dynamic power-system options](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transient_Stability_Dialog_Options_Power_System_Model.htm) | Help | 2026-10-15 |
| W61 | [Dynamic validation](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transient_Stability_Dialog_Validation.htm) | Help | 2026-10-15 |
| W62 | [Transient study dialog](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transient_Stability_Dialog.htm) | Help | 2026-10-15 |
| W63 | [SMIB eigenvalues](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transient_Stability_Dialog_SMIB.htm) | Help | 2026-10-15 |
| W64 | [User-defined dynamic models](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transient_Stability_User_Defined_Models.htm) | Help | 2026-10-15 |
| W65 | [Dynamic interchange](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transient_Stability_Data_GEDYD.htm) | Help | 2026-10-15 |
| W66 | [Dynamic results storage](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transient_Stability_Dialog_Results_To_Save.htm) | Help | 2026-10-15 |
| W67 | [GIC product](https://www.powerworld.com/products/simulator/add-ons-2/simulator-gic) | Vendor public page | 2026-10-15 |
| W68 | [GIC calculations](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/GIC_Analysis_Form.htm) | Help | 2026-10-15 |
| W69 | [GIC tables and results](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/GIC_Analysis_TablesResults.htm) | Help | 2026-10-15 |
| W70 | [GICHarm integration](https://www.powerworld.com/knowledge-base/powerworld-simulator-epri-gicharm-integration) | Vendor public page | 2026-10-15 |
| W71 | [ITP product](https://www.powerworld.com/products/retriever/add-ons/integrated-topology-processing) | Vendor public page | 2026-10-15 |
| W72 | [Topology processing](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Topology_Processing_Dialog.htm) | Help | 2026-10-15 |
| W73 | [Distributed computing](https://www.powerworld.com/products/simulator/add-ons-2/distributed-computing) | Vendor public page | 2026-10-15 |
| W74 | [Time-step simulation](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Time_Step_Simulation.htm) | Help | 2026-10-15 |
| W75 | [Weather features](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Weather_Related_Features.htm) | Help | 2026-10-15 |
| W76 | [Weather model dialog](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Weather_Related_Models_Info_Dialog.htm) | Help | 2026-10-15 |
| W77 | [Scheduled actions](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Scheduled_Actions_Dialog.htm) | Help | 2026-10-15 |
| W78 | [Contouring](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Contouring_Topic.htm) | Help | 2026-10-15 |
| W79 | [Oneline overview](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Oneline_Diagram_Overview.htm) | Help | 2026-10-15 |
| W80 | [Display Explorer](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Display_Objects_Case_Information_Display.htm) | Help | 2026-10-15 |
| W81 | [Bus view](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Bus_View_Display.htm) | Help | 2026-10-15 |
| W82 | [Training syllabus](https://www.powerworld.com/training/courses/introduction-to-powerworld-simulator) | Vendor public page | 2026-10-15 |
| W83 | [Avista 64-bit experiences, June 2017](https://www.powerworld.com/files/weccconf_June2017/PWS_64bit.pdf) | Public PDF | 2026-10-15 |
| W84 | [BPA event-based RAS, 2013 conference](https://www.powerworld.com/files/10OBrien_RAS.pdf) | Public PDF | 2026-10-15 |
| W85 | [Conference material index](https://www.powerworld.com/training/client-meetings/past-conference-materials) | Vendor public page | 2026-10-15 |
| W86 | [Environment options](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Environment_Options.htm) | Help | 2026-10-15 |
| W87 | [Generator cost models](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Generator_Load_Cost_Models.htm) | Help | 2026-10-15 |
| W88 | [Network equivalents](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Equivalents_Topic.htm) | Help | 2026-10-15 |
| W89 | [Modal analysis theory](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transient_Stability_Dialog_ResultAnalysisModalAnalysis.htm) | Help | 2026-10-15 |
| W90 | [Fault dialog](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Fault_Analysis_Dialog.htm) | Help | 2026-10-15 |
| W91 | [Fault options](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Fault_Analysis_Dialog_Options.htm) | Help | 2026-10-15 |
| W92 | [Generator model support](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transient_Stability_Data_Model_Explorer.htm) | Help | 2026-10-15 |
| W93 | [Geographic data view](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Geographic_Data_View.htm) | Help | 2026-10-15 |
| W94 | [Auxiliary files](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Auxiliary_Files.htm) | Help | 2026-10-15 |
| W95 | [Fault single-study](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Fault_Analysis_Single_Fault.htm) | Help | 2026-10-15 |
| W96 | [Line parameter calculator](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transmission_Line_Parameter_Calculator.htm) | Help | 2026-10-15 |

## 3. Architecture and data model

### 3.1 Case database versus diagram

**D1, D3, G1.** Simulator distinguishes the electrical model from its display objects.
One bus, branch or generator can have zero, one or several graphical representations,
including on different diagrams. A diagram can therefore show only a subset of a
larger solved system. Deleting a symbol offers a choice between removing the display
and removing its underlying record. Diagram coordinates are not electrical
connectivity. [W9][W79]

The model is bus-oriented: generators, loads and shunts attach to buses; branches
connect buses. Model Explorer organizes physical records, aggregations, calculation
options, solution matrices and transient models. It exposes the same data without
requiring an oneline. This supports a study database with several coordinated views,
not a screenshot serving as the network definition. [W8][W9]

**D4, D6, D9.** Difference Case stores a Base and compares it with Present, with
Difference and Change display modes. Identity matching can use primary keys,
secondary keys or labels. Additions/removals need the topological-difference view.
This is evidence of case comparison, not evidence of a multi-user version-controlled
project database with mergeable engineering branches. [W12]

**D10.** Element dialogs include custom fields, labels and memo information. These
extend an element record rather than creating a new solver model automatically.
The branch memo is stored in PWB. A study plugin must still implement the physics of
any new type. The last sentence is an inference from the distinction between model
records and their display/custom attributes. [W18][W9]

### 3.2 Files, identity and interoperability

| Representation | Role and important boundary | Sources |
| --- | --- | --- |
| PWB | Compact binary case with electrical/economic data, options and screen customizations; not readable as plain text | [W10] |
| PWD | Diagram representation, separate from the electrical case; exact persistence/version contract requires its own format inspection | [W9][W79], inferred file-role cross-check pending |
| AUX | Text records for model data, selected results, options and scripts. An arbitrary AUX may be a partial update, not a complete project | [W10][W94] |
| Primary/secondary/label keys | Numeric identity, bus-name/nominal-voltage identity or labels can identify exported records; key selection matters when applying updates | [W10][W12] |
| RAW and EPC | External planning-case exchange with format-specific import behavior; import success does not prove model equivalence | [W10][W11] |
| DYR, DYD, SWI | Dynamic-model exchange with PSS/E, PSLF and BPA conventions, respectively; export retains only supported model mappings | [W65] |
| SEQ and AUX fault data | Additional sequence-network and mutual data for faults; load-flow input alone may be incomplete | [W90] |

**D16.** Import conversion has explicit semantic differences. For example, the help
notes that a PSLF tertiary bus omitted from its representation is written as two
2-winding transformers when exporting to RAW. Dynamic export similarly depends on
the model support table. A future Quantic importer should report translation losses;
that is our design inference, not a claim that all vendor importers do so. [W11][W65]

### 3.3 Units, validation and safe recovery

**D12.** Data Checks combine an object type with a filter to identify records of
interest, expose per-record results and aggregate counts, and support exemptions.
They are configurable checks, so the existence of a check framework is not a promise
that every erroneous engineering input is automatically caught. [W13]

**D13.** Graphical Undo only reverses oneline changes. Separately, the power-flow
storage options distinguish restoring the last successful solution from restoring
the state immediately before a failed solve. The first can discard intervening input
edits; the second retains them. This separation is important for an honest Quantic
undo/save design. [W14][W15]

Physical units vary by object: bus kV, generator MW/Mvar, branch system-base per-unit
parameters, converter ohms and current units. Environment settings allow SI or
Imperial system measurements. A unit toggle must not be assumed to change the
underlying per-unit base or foreign-file conventions. [W16][W17][W26][W86]

## 4. Element catalogue and key parameters

The tables identify model families and engineering fields, not an exhaustive list of
every AUX field. No manufacturer library content is reproduced. Base selection,
sign conventions, regulation state and rating enablement are part of the model.

### 4.1 Buses, branches and transformers

| Element | Key parameters and units | Meaning, controls and outputs | Sources |
| --- | --- | --- | --- |
| Bus | Number/name/labels; nominal kV; area/zone/substation; voltage pu and angle degrees | Node identity and voltage base. A guessed starting voltage differs from a generator voltage setpoint | [W16] |
| AC line | From/to bus and circuit ID; R/X/G/B pu; status; length; MVA ratings | Series impedance, charging and shunt terms. B is total charging, not the single-end B/2 value | [W17][W18] |
| Line shunt | End-associated conductance/susceptance pu | Separate shunt contribution at either branch end | [W17] |
| 2-winding transformer | Branch parameters, off-nominal tap ratio, phase angle degrees; magnetizing G/B; winding configuration for faults | Voltage conversion plus fixed or automatic control; tapped-side orientation matters | [W17][W18][W19] |
| LTC transformer | Regulated bus, voltage band pu, tap limits/steps and enabled control | Changes ratio to satisfy a voltage range; device, area and global control settings all matter | [W19] |
| Mvar controller / phase shifter | Reactive-flow band Mvar or MW-flow band; phase-angle range and step degrees | Changes tap or phase to regulate flow; phase shifter can be enabled for OPF only | [W19] |
| 3-winding transformer | Three terminal buses, winding data and ratings; common transformer record | Dedicated object in the model, with representations/import translations examined in its dialog | [W29][W11] |
| Sequence mutual coupling | Two branch identifiers, coupled sections, mutual R/X pu | Additional zero-sequence coupling for fault analysis; not a general geometric line-constant solver | [W28] |

### 4.2 Generation, demand and reactive compensation

| Element | Key parameters and units | Meaning, controls and outputs | Sources |
| --- | --- | --- | --- |
| Generator | MW output/setpoint, MW bounds, AGC flag and participation | Actual output is zero when disconnected, while the reconnect setpoint can remain stored | [W20] |
| Generator voltage control | Mvar bounds/capability curve, AVR flag, regulated bus, voltage target pu and tolerance | Reactive output supports local or remote voltage until capability is exhausted | [W20] |
| Generator fault source | Positive/negative/zero-sequence internal impedances; neutral impedance | Fault model is additional information, not merely the dispatch MW value | [W21] |
| Generator economics | Cubic or piecewise-linear cost; load benefit curves | Used by OPF/SCOPF, not a machine dynamic characteristic | [W87] |
| ZIP load | Constant-P, constant-I and constant-Z real/reactive components in MW/Mvar at 1 pu | Voltage sensitivity is explicit; embedded distributed generation can be subtracted from demand | [W22] |
| Switched shunt | Nominal Mvar, fixed/discrete/continuous/SVC mode, regulation range and enabled controls | Capacitor/reactor output and switching respond to voltage/reactive conditions according to mode | [W23] |
| SVC | Continuous limit in susceptance or reactive-current form, selected SVSMO type, controlled fixed-shunt entries | Coordinated variable and switched compensation; the power-flow and dynamic models must agree at initialization | [W24] |

### 4.3 DC links, aggregations and dynamics

| Element | Key parameters and units | Meaning and boundaries | Sources |
| --- | --- | --- | --- |
| LCC HVDC rectifier/inverter | Bridge count; AC base kV; transformer ratio/tap/range; commutating R/X ohms; firing-angle limits | Converter controls couple a DC transfer with AC real/reactive demand; not a household DC circuit solver | [W26] |
| VSC HVDC link | Terminal buses; DC-line resistance; DC voltage/power mode; AC voltage/power-factor mode; loss coefficients; MVA/current/Mvar limits | Separate P/Q controls with converter constraints; AC-side and DC-side MW setpoints differ when losses exist | [W25] |
| Multi-terminal DC branch | DC-bus endpoints, circuit ID, resistance ohms; stored inductance mH | Help explicitly says inductance is not used in load flow. A stored field is not proof of simulated dynamics | [W27] |
| Areas, zones, owners, substations | Membership IDs and control/monitoring flags | Organize dispatch, interchange, reporting and limit selection; geographic grouping is distinct from topology | [W8][W35] |
| Injection group / transfer direction | Participating source and sink groups and their dispatch rules | Defines how an MW transfer is distributed, so sensitivities depend on more than two map coordinates | [W42][W45] |
| Machine/control model | Machine, exciter, governor, stabilizer and model-specific parameters/states | Dynamic records attach to network objects; a listed model may have import/export support before numerical support | [W58][W92] |
| Dynamic load and renewable model | Composite loads, motors, renewable converter/plant controls, distributed generation | Separate dynamic model families; parameters and model-specific implementation require technical references | [W58][W92] |
| GIC network additions | Grounding resistance ohms, winding/DC resistance, transformer core/connection, coordinates and electric field | Needed for induced DC current and associated AC impact; defaults must not masquerade as measured data | [W68][W69] |
