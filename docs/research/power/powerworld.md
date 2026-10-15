# PowerWorld Simulator research dossier

Research date: 2026-10-15. Owner: Lane B, ChatGPT. WP-2.11, including authorized deepening pass.

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
date. The vendor release announcement places the release in March 2025; patch
history extends into 2026. Major version and patch build must both accompany a
reproducibility record because the patch history includes solver, importer and
results-storage fixes. We do not infer an unreleased Version 25. [W2][W3][W5]

| Configuration | Documented boundary | Sources |
| --- | --- | --- |
| Commercial base | Licensed Simulator, with power flow, contingency analysis, sensitivities, fault analysis and time-step simulation | [W1][W36][W74] |
| Optional study licences | ATC, PVQV, OPF, SCOPF, reserves, transient stability, GIC and integrated topology processing | [W4] |
| Automation and orchestration | SimAuto, Scheduled Actions and distributed-analysis licences have separate purchase entries | [W4] |
| Demonstration | Free 13-bus evaluation. Overview names ATC/PVQV/OPF/SCOPF; pricing page additionally names Reserves, Transient Stability and GIC. Exact installer entitlement should be checked rather than assuming all add-ons | [W1][W4] |
| Educational editions | University teaching/research configurations are offered; terms must be checked for the intended use | [W1] |
| Viewer | Separate freeware for exchanging and displaying cases; its existence does not confer an editing or simulation licence | [W1] |

### 1.1 Commercial price snapshot

USD, accessed 2026-10-15; grouped names have identical prices. Blank vendor cells
are shown as `n/a`, not zero. Add-on prices exclude the base. [W4]

| Product | First | Additional, each | Site | Corporate |
| --- | ---: | ---: | ---: | ---: |
| Base | 11,000 | 5,500 | 33,000 | 66,000 |
| ATC, PVQV, Reserves, SimAuto, Scheduled Actions | 5,500 | 2,750 | 16,500 | 33,000 |
| OPF | 8,800 | 4,400 | 26,400 | 52,800 |
| SCOPF | 3,300 | 1,650 | 9,900 | 19,800 |
| ITP, Transient Stability, GIC | 11,000 | 5,500 | 33,000 | 66,000 |
| TransLineCalc | 2,200 | 1,100 | 6,600 | 13,200 |
| Distributed Contingency | n/a | n/a | 0 | 0 |
| Distributed ATC, Distributed QV | n/a | n/a | 16,500 | 33,000 |
| Distributed Transient Stability | n/a | n/a | 33,000 | 66,000 |

Maintenance: first year included; renewal 28% of then-current licence price.
Site: unlimited installations/concurrent instances within 1,000 m; corporate:
organization-wide. SCOPF/Reserves require OPF. Distributed studies require site
SimAuto plus the corresponding site study licence; Distributed Contingency requires
site Simulator/SimAuto. Demo: 13 buses with ATC, PVQV, OPF/SCOPF/Reserves, TS and
GIC. These are dated public prices, not a project quote. [W4]

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
| W5 | [Version 24 release announcement](https://www.powerworld.com/simulator-v24-release) | Vendor public page | 2026-10-15 |
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
| W95 | [Fault single-study](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Fault_Analysis_Dialog_Single_Fault.htm) | Help | 2026-10-15 |
| W96 | [Line parameter calculator](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transmission_Line_Parameter_Calculator.htm) | Help | 2026-10-15 |

| W97 | [Motor starting tutorial, July 2013](https://www.powerworld.com/knowledge-base/motor-load-starting-using-transient-stability) | Vendor public page | 2026-10-15 |
| W98 | [Oneline Viewer](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Oneline_Viewer.htm) | Help | 2026-10-15 |
| W99 | [Real-time product boundary](https://www.powerworld.com/solutions/real-time-operations) | Vendor public page | 2026-10-15 |
| W100 | [Typed rectangular SimAuto retrieval](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/GetParamsRectTyped_Function.htm) | Help | 2026-10-15 |
| W101 | [Per-column typed SimAuto retrieval](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/GetParamsTypedCols_Function.htm) | Help | 2026-10-15 |
| W102 | [GICHarm technical presentation, July 2025](https://www.powerworld.com/files/OverbyeGICHarmIntegrationJuly2025.pdf) | Public PDF | 2026-10-15 |
| W103 | [Fault-analysis training, 2024](https://www.powerworld.com/files/I13FaultAnalysis.pdf) | Public PDF | 2026-10-15 |
| W104 | [Integrated topology overview](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Topology_Processing_Overview.htm) | Help | 2026-10-15 |

| W105 | [SVC steady-state/dynamic consistency](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Switched_Shunt_SVC_Control_Mode_Transient_Simulation.htm) | Help | 2026-10-15 |

| W106 | Glover, Overbye and Sarma, Power System Analysis and Design, 6th ed., Cengage, 2017 | Owned book, page-tagged text; PDF images unavailable | 2026-10-15 |
| W107 | [Stability data management, 2024, slides 14 and 31](https://www.powerworld.com/files/T02StabilityDataManagement.pdf) | Public PDF, page images inspected | 2026-10-15 |
| W108 | [Large-scale simulation examples, 2025, slide 4](https://www.powerworld.com/files/T14LargeExamples.pdf) | Public PDF, page image inspected | 2026-10-15 |
| W109 | [Web Help topic index](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Table_Of_Contents_For_Printed_Output.htm) | Vendor help index | 2026-10-15 |
| W110 | [ESST1A_GE](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Exciter%20ESST1A%20and%20ESST1A_GE.htm) | Vendor model help | 2026-10-15 |
| W111 | [AC1C](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Exciter%20AC1C.htm) | Vendor model help | 2026-10-15 |
| W112 | [ST1C](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Exciter%20ST1C.htm) | Vendor model help | 2026-10-15 |
| W113 | [DEGOV](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Governor%20DEGOV.htm) | Vendor model help | 2026-10-15 |
| W114 | [TGOV1D](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Governor%20TGOV1%20and%20TGOV1D.htm) | Vendor model help | 2026-10-15 |
| W115 | [GGOV1D](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Governor%20GGOV1%20and%20GGOV1D.htm) | Vendor model help | 2026-10-15 |
| W116 | [HYGOVD](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Governor%20HYGOV%20and%20HYGOVD.htm) | Vendor model help | 2026-10-15 |
| W117 | [W2301](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Governor%20W2301.htm) | Vendor model help | 2026-10-15 |
| W118 | [PSS2A](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Stabilizer%20PSS2A.htm) | Vendor model help | 2026-10-15 |
| W119 | [PSS2C](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Stabilizer%20PSS2C.htm) | Vendor model help | 2026-10-15 |
| W120 | [PTIST3](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Stabilizer%20PTIST3.htm) | Vendor model help | 2026-10-15 |
| W121 | [PAUXSS1A](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Paux%20Controller%20PAUXSS1A.htm) | Vendor model help | 2026-10-15 |
| W122 | [CMPLDW](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Load%20Characteristic%20CMPLDW.htm) | Vendor model help | 2026-10-15 |
| W123 | [CMPLDWNF](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Load%20Characteristic%20CMPLDWNF.htm) | Vendor model help | 2026-10-15 |
| W124 | [MOTORW](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Load%20Characteristic%20MOTORW.htm) | Vendor model help | 2026-10-15 |
| W125 | [IEEL](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Load%20Characteristic%20IEEL.htm) | Vendor model help | 2026-10-15 |
| W126 | [CLOD](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Load%20Characteristic%20CLOD.htm) | Vendor model help | 2026-10-15 |
| W127 | [REGC_A](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Machine%20Model%20REGC_A.htm) | Vendor model help | 2026-10-15 |
| W128 | [REGC_B](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Machine%20Model%20REGC_B.htm) | Vendor model help | 2026-10-15 |
| W129 | [REGC_C](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Machine%20Model%20REGC_C.htm) | Vendor model help | 2026-10-15 |
| W130 | [REGFM_A1](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Machine%20Model%20REGFM_A1.htm) | Vendor model help | 2026-10-15 |
| W131 | [REGFM_B1](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Machine%20Model%20REGFM_B1.htm) | Vendor model help | 2026-10-15 |
| W132 | [REGFM_C1](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Machine%20Model%20REGFM_C1.htm) | Vendor model help | 2026-10-15 |
| W133 | [REECA1](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Exciter%20REEC_A.htm) | Vendor model help | 2026-10-15 |
| W134 | [REECB1](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Exciter%20REEC_B.htm) | Vendor model help | 2026-10-15 |
| W135 | [REEC_C](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Exciter%20REEC_C.htm) | Vendor model help | 2026-10-15 |
| W136 | [REEC_D](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Exciter%20REEC_D.htm) | Vendor model help | 2026-10-15 |
| W137 | [REEC_E](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Exciter%20REEC_E.htm) | Vendor model help | 2026-10-15 |
| W138 | [REPCTA1](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Plant%20Controller%20REPC_A.htm) | Vendor model help | 2026-10-15 |
| W139 | [REPC_B100](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Plant%20Controller%20REPC_B.htm) | Vendor model help | 2026-10-15 |
| W140 | [REPC_C](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Plant%20Controller%20REPC_C.htm) | Vendor model help | 2026-10-15 |
| W141 | [DISTRELAY](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Line%20Relays%20DISTRELAY.htm) | Vendor model help | 2026-10-15 |
| W142 | [TIOCR1](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Line%20Relays%20TIOCR1.htm) | Vendor model help | 2026-10-15 |
| W143 | [TLIN1O](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Line%20Relays%20TLIN1O.htm) | Vendor model help | 2026-10-15 |
| W144 | [LDSH](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Load%20Relays%20LDSH.htm) | Vendor model help | 2026-10-15 |
| W145 | [LVS3](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Load%20Relays%20LVS3.htm) | Vendor model help | 2026-10-15 |
| W146 | [GP1](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Relay%20Model%20GP1.htm) | Vendor model help | 2026-10-15 |
| W147 | [GP3](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Relay%20Model%20GP3.htm) | Vendor model help | 2026-10-15 |
| W148 | [GENOF](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Relay%20Model%20GENOF.htm) | Vendor model help | 2026-10-15 |
| W149 | [April 10, 2026 patch: REGFM and plant-controller connection](https://www.powerworld.com/patch/april-10-2026) | Vendor patch note | 2026-10-15 |
| W150 | [ACTIVSg200](https://electricgrids.engr.tamu.edu/electric-grid-test-cases/activsg200/) | Texas A&M dataset publisher | 2026-10-15 |
| W151 | [ACTIVSg500](https://electricgrids.engr.tamu.edu/electric-grid-test-cases/activsg500/) | Texas A&M dataset publisher | 2026-10-15 |
| W152 | [ACTIVSg2000](https://electricgrids.engr.tamu.edu/electric-grid-test-cases/activsg2000/) | Texas A&M dataset publisher | 2026-10-15 |
| W153 | [ACTIVSg10k](https://electricgrids.engr.tamu.edu/electric-grid-test-cases/activsg10k/) | Texas A&M dataset publisher | 2026-10-15 |
| W154 | [ACTIVSg25k](https://electricgrids.engr.tamu.edu/electric-grid-test-cases/activsg25k/) | Texas A&M dataset publisher | 2026-10-15 |
| W155 | [ACTIVSg70k](https://electricgrids.engr.tamu.edu/electric-grid-test-cases/activsg70k/) | Texas A&M dataset publisher | 2026-10-15 |
| W156 | [Texas2k Series24](https://electricgrids.engr.tamu.edu/activsg2000-dynamics-cases-2024/) | Texas A&M dataset publisher | 2026-10-15 |
| W157 | [Texas2k Series25](https://electricgrids.engr.tamu.edu/texas2k-series25/) | Texas A&M dataset publisher | 2026-10-15 |
| W158 | [Case formats](https://electricgrids.engr.tamu.edu/file-formats/) | Texas A&M dataset publisher | 2026-10-15 |
| W159 | [Annual time series](https://electricgrids.engr.tamu.edu/activsg-time-series-data/) | Texas A&M dataset publisher | 2026-10-15 |
| W160 | [Eng-Tips practitioner comparison, November to December 2011](https://www.eng-tips.com/threads/power-system-simulation-software-recommendations.309917/) | Independent forum, individual observations | 2026-10-15 |
| W161 | [Paras Mandal, UTEP syllabus, revised September 12, 2021](https://digitalmeasures.utep.edu/ai/pmandal/schteach/EE43955390_PowerSysAnalysis_Syllabus_Fall2021_v3-1.pdf) | University course document | 2026-10-15 |
| W162 | [M. R. Jamieson and K. R. W. Bell, March 20, 2024, Choosing appropriate power system simulation models for different events](https://strathprints.strath.ac.uk/88584/1/Jamieson-Bell-2024-Choosing-Appropriate-Power-System-Simulation-Models.pdf) | University research report | 2026-10-15 |
| W163 | [Reddit, Transfer into Power Industry, August 5 to 6, 2023](https://www.reddit.com/r/PowerSystemsEE/comments/15j8rjs/) | Search record only; comment author unavailable | 2026-10-15 |
| W164 | [Reddit, Dynamics/Transient Studies, July 29, 2026](https://www.reddit.com/r/PowerSystemsEE/comments/1v9je2i/dynamicstransient_studies/) | Search record only; comment author unavailable | 2026-10-15 |

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
| PWD | Oneline file with display metadata; distinct from the electrical case and from text display AUX | [W98] |
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
| AC line | From/to bus and circuit ID; R/X/G/B pu; status; length; MVA ratings | Series impedance, charging and shunt terms. B is total charging, not the single-end half-charging value | [W17][W18] |
| Line shunt | End-associated conductance/susceptance pu | Separate shunt contribution at either branch end | [W17] |
| 2-winding transformer | Branch parameters, off-nominal tap ratio, phase angle degrees; magnetizing G/B; winding configuration for faults | Voltage conversion plus fixed or automatic control; tapped-side orientation matters | [W17][W18][W19] |
| LTC transformer | Regulated bus, voltage band pu, tap limits/steps and enabled control | Changes ratio to satisfy a voltage range; device, area and global control settings all matter | [W19] |
| Mvar controller / phase shifter | Reactive-flow band Mvar or MW-flow band; phase-angle range and step degrees | Changes tap or phase to regulate flow; phase shifter can be enabled for OPF only | [W19] |
| 3-winding transformer | Three terminal buses, winding data and ratings; common transformer record | Dedicated object in the model, with representations/import translations examined in its dialog | [W29][W11] |
| Sequence mutual coupling | Two branch identifiers and zero-sequence mutual data | Additional zero-sequence coupling for fault analysis; not a general geometric line-constant solver | [W28] |

### 4.2 Generation, demand and reactive compensation

| Element | Key parameters and units | Meaning, controls and outputs | Sources |
| --- | --- | --- | --- |
| Generator | MW output/setpoint, MW bounds, AGC flag and participation | Actual output is zero when disconnected, while the reconnect setpoint can remain stored | [W20] |
| Generator voltage control | Mvar bounds/capability curve, AVR flag, regulated bus, voltage target pu and tolerance | Reactive output supports local or remote voltage until capability is exhausted | [W20] |
| Generator fault source | Positive/negative/zero-sequence internal impedances; neutral impedance | Fault model is additional information, not merely the dispatch MW value | [W21] |
| Generator economics | Cubic or piecewise-linear cost; load benefit curves | Used by OPF/SCOPF, not a machine dynamic characteristic | [W87] |
| ZIP load | Constant-P, constant-I and constant-Z real/reactive components in MW/Mvar at 1 pu | Voltage sensitivity is explicit; embedded distributed generation can be subtracted from demand | [W22] |
| Switched shunt | Nominal Mvar, fixed/discrete/continuous/SVC mode, regulation range and enabled controls | Capacitor/reactor output and switching respond to voltage/reactive conditions according to mode | [W23] |
| SVC | Continuous limit in susceptance or reactive-current form, selected SVSMO type, controlled fixed-shunt entries | Coordinated variable and switched compensation; the power-flow and dynamic models must agree at initialization | [W24][W105] |

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

### 4.4 Named dynamic models and the strength of support evidence

This is a selected, named inventory for parity planning, not a claim to enumerate
every build's models. Names were cross-checked against the public topic index. [W109]
The Model Explorer makes three separate distinctions:
PowerWorld numerical support, foreign-format interchange, and whether an assigned
model is active. Gray text means unused in this case. Red means interchange is
available but numerical integration is not; green means numerical support. A format
column such as GE or PTI does not answer the PowerWorld support question. [W92]

The codes below describe evidence, not a certification:

- **S:** a vendor training screenshot explicitly shows PowerWorld Support = YES.
  The dated screenshots are historical support snapshots, not an execution of V24.
- **N:** the model page or patch describes runtime numerical behavior.
- **D:** a model page documents validation and/or a block diagram, but the exact
  installed build's Fully Supported flag was not inspected.
- **U:** only a parameter/catalogue entry was established here. Numerical status is
  unresolved. U does not mean import-only or unsupported.

| Family | Named models | Evidence and practical distinction |
| --- | --- | --- |
| Synchronous machines | GENCLS, GENROU, GENSAL, GENROE, GENSAE, GENTPF, GENTPJ, GENTRA, GENPWFluxDecay, GENPWTwoAxis | S, all show YES in slide 31. Classical, transient and subtransient alternatives must not be collapsed into one generic machine. Screenshot spelling is retained for GENPWFluxDecay; the help index calls its page GENFluxDecay. [W107] |
| Induction and converter machines | CIMTR1, CIMTR2, CIMTR3, CIMTR4, MOTOR1, GENIND, WT1G, WT1G1, WT2G, WT2G1, WT3G, WT3G1, WT3G2, WT4G, WT4G1, PV1G, PVD1, DER_A, CBEST | S, YES in the same dated support table. An induction-machine model is not proof of a full industrial starting-study package. [W107] |
| Exciters in a large-system example | ESAC1A, ESAC6A, ESDC1A, ESDC2A, ESST4B, EXAC1, EXAC2, EXPIC1, IEEET1, SCRX | S, YES in the ACTIVSg10K example. This is direct named numerical-support evidence. [W108, slide 4] |
| Additional IEEE-style excitation | ESST1A, ESST1A_GE, AC1C, ST1C | D, model-specific validation and control diagrams; retain the GE suffix because variant behavior differs. This establishes named coverage relevant to IEEE 421.5, not conformance to every model/edition. [W110][W111][W112] |
| Conventional governors | GGOV1, HYGOV, IEEEG1 | S, YES in the large-system example. [W108, slide 4] |
| Steam, hydro and general governor variants | TGOV1, TGOV1D; HYGOV, HYGOVD; GGOV1, GGOV1D | N, pages describe valve/gate/control-limit treatment during simulation. D-suffixed variants carry additional deadband data. Keep the selected variant and turbine base in the case provenance. [W114][W116][W115] |
| Genset and mechanical controls | DEGOV; W2301 | N, engine delay / governor controls and runtime limit handling are documented. A named diesel governor is stronger evidence for genset modelling than an unspecified generic governor claim. [W113][W117] |
| Stabilizers | IEEEST; PSS2A, PSS2C; PTIST3 | IEEEST: S. PSS2A/PSS2C: D. PTIST3: N with an explicit limitation: its NCL limit function is ignored and produces a warning. This is partial model behavior, not merely import-only support. [W108][W118][W119][W120] |
| Supplementary control | PAUXSS1A | D, named auxiliary stabilizing signal model; V24 release notes also name its addition. [W2][W121] |
| Composite and motor loads | CMPLDW, CMPLDWNF, MOTORW | D. CMPLDWNF omits the distribution-equivalent portion of CMPLDW; MOTORW has motor/inertia/trip inputs. Composite-load parameter sets and aggregation levels are separate from ordinary ZIP power-flow loads. [W122][W123][W124] |
| Algebraic/composite load entries | IEEL, CLOD | U in this review: named parameter pages, without an independently inspected Fully Supported row. [W125][W126] |
| Renewable converter interface | REGC_A, REGC_B, REGC_C | S, YES in slide 31; individual pages document distinct converter parameter sets. REGCA1 is a PTI-format name for REGC_A, not a separate proof of a new model family. [W107][W127][W128][W129] |
| Newer converter interface | REGC_D | V24 release notes name it. A direct model-help URL guessed from its name returned 404, so its exact current parameter schema/flag remains unverified; do not invent one. [W2] |
| Renewable electrical control | REECA1, REECB1, REEC_C, REEC_D, REEC_E | D for the first four; REEC_E: N, including runtime current/control-limit logic. These are electrical-control records under the exciter family, not synchronous exciters. [W133][W134][W135][W136][W137] |
| Renewable plant control | REPC_A, REPCA1, REPCTA1; REPC_B, REPC_B100; REPC_C | REPC_A/REPCA1/REPCTA1: N; B/B100/C: D. The A variants have explicit runtime treatment; the April 2026 patch explains that REPCA1 and REPCTA1 use the same internal controller, with signal routing dependent on the attached torque/electrical controls. [W138][W139][W140][W149] |
| Grid-forming converters | REGFM_A1, REGFM_B1, REGFM_C1 | A1/B1: N, the April 2026 fix addresses their connection to plant controls. C1: D, page dates its addition to May 1, 2025. These establish RMS model families, not switching-level EMT equivalence. [W130][W131][W132][W149] |
| Generator protection | GP1, GP3, GENOF | GP1: U; GP3: N, page explicitly describes implemented generator protection; GENOF: U, PowerWorld attribution alone does not establish the current numerical flag. [W146][W147][W148] |
| Branch and load protection | DISTRELAY, TIOCR1; TLIN1O; LDSH, LVS3 | DISTRELAY: D, distance-zone shapes/timing; TIOCR1: N, documented contingency timing/tripping logic and reference to transient operation; this does not certify all transient integration details. TLIN1O/LDSH/LVS3: U from the pages inspected. Load shedding and transient relay entries do not establish an industrial TCC equipment library. [W141][W142][W143][W144][W145] |

**Import-only boundary:** none of the inspected public sources supplies a complete,
current, machine-readable list of red-icon models by name. Therefore this dossier
names no particular current model as import-only without its support row. Export
Model Support Status and Models in Use from the target build before using a case as
an oracle. Include active flags, support flags, interchange translations, parameter
normalizations and initialization diagnostics. A historical YES or a block diagram
cannot replace that case/build check. [W92][W107][W108]

**Quantic implication, inferred:** split machine, excitation, governor, stabilizer,
electrical converter and plant-controller responsibilities. Verify state initialization,
saturation/limits, parameter bases, measured-bus selection and signal wiring separately.
The DEGOV and WECC families are concrete future parity targets, not permission to
implement from a help page or to copy standard coefficients. [W106][W113][W137][W138]

## 5. Studies and modules

For each study below, the method is the one directly documented, not a guess about
closed-source implementation. A limit violation and a numerical failure are different
outcomes. Monitor selection also matters: limits are checked only when device, limit
group, area and zone settings permit monitoring. [W35]

### 5.1 Balanced AC power flow: S1 to S7, S9

- **Purpose and inputs:** solve a network operating point from topology, branch
  admittances, generation/load dispatch and voltage controls. [W30][W31]
- **Method:** full Newton-Raphson with an optimal multiplier; the overview also names
  fast decoupled solution. The numerical inner solve sits inside voltage-controller
  and MW-control loops. Closing a branch may trigger angle smoothing before solving.
  A bare Newton iteration is therefore not feature parity with the whole solve. [W30]
- **Options:** MVA mismatch tolerance, iteration cap, generator reactive-limit
  handling, enabled tap/shunt/phase-shifter controls, AGC and controller-oscillation
  handling. Some settings can deliberately suppress engineering limits. [W32]
- **Inputs to regulation:** local/remote voltage targets, Mvar capability and sharing,
  transformer bands and shunt modes. Multiple islands can be assigned their own slack
  behavior according to the advanced options. [W20][W19][W23][W33]
- **Outputs:** bus voltages/angles and flows, generator dispatch/reactive output,
  control states and convergence messages. Equation-only theory deliberately excludes
  the enclosing regulation algorithms. [W30][W31]
- **Limits:** failure to converge is not proof that a physical blackout occurred or
  that no mathematical solution exists. The UI can gray the case and display a blackout
  indication on a failed solve. [W30][W32]

**Quantic implication, inferred:** regression cases must exercise limit release as
well as limit activation, conflicting controls and isolated islands. Solver convergence
must not be treated as an equipment-rating pass. [W32][W33][W35]

### 5.2 DC approximation and sensitivities: S16, PW-S1

DC power flow is a linear approximation of the AC transmission problem here; it is
not the same feature as HVDC converter modeling. Options distinguish ignoring series
resistance from ignoring series conductance, transformer correction treatment and
load adjustments for losses. These choices also affect sensitivity tools. [W34]

| Calculation | Inputs and method | Outputs and limits | Sources |
| --- | --- | --- | --- |
| PTDF | Seller/buyer, participation and monitored devices; linearized AC Jacobian or lossless DC, with phase-shifter variants | Incremental flow response to the defined transaction; AC option includes losses | [W42] |
| LODF / LCDF | Solved network and opening/closing branch | Redistribution factor from an outage or closure; a linear estimate, not a full post-event solve | [W43] |
| OTDF | Transfer factors combined with outage factors | Post-outage transfer sensitivity; depends on the selected outage and source/sink | [W43] |
| TLR / GSF | A monitored device and candidate source/sink groups | Identifies which injection changes aggravate or relieve that device; reverses the one-transfer/many-monitors orientation of PTDF | [W44] |

For a single line outage, the help explicitly gives the relation
`OTDF_x = PTDF_x + LODF_xy * PTDF_y`. This is a documented mathematical relationship,
not a copied worked example. The source also defines the corresponding first-order
post-outage flow relationship. [W43]

### 5.3 Contingency analysis and RAS: S15, P4, PW-S2

Base Simulator runs contingencies containing equipment outages and operating actions.
The input is a solved case, contingency definitions, monitoring settings, make-up
power rules and post-event controls. The study records violations and failed solves,
not just a list of open branches. [W36][W37]

**Methods and options.** Full Power Flow can use AC or DC according to solution
settings. Separate linearized lossless-DC methods estimate contingency effects;
phase-shifter treatment differs. AC analysis can use screening before full solves.
Screening assumes how reactive flows behave, so its rankings depend on the selected
approximation. A monitored MVA limit compared only with MW omits part of the loading.
[W37][W38]

**Actions and logic.** Branches, generators, loads, shunts, DC links and groups support
opening/closing or changed setpoints. Remedial-action containers group conditional
responses independently from individual contingencies. Reference-state conditions,
arming and post-action evaluation need explicit semantics. A static contingency RAS
is not evidence of relay time-domain coordination. [W39][W40]

**Combination analysis.** Primary/secondary contingency combinations retain the
post-primary state as an optional reference for the secondary events. The documented
combination dialog requires Full Power Flow with AC mode; its restriction must not be
replaced with an assumed DC capability. Outputs are contingency/violation tables and
summary counts. [W41]

**Limits and reporting.** Make-up generation, inherited solution options and
remedial actions change the answer. Report the analysis method and balancing policy
alongside an overload; otherwise the same outage name can conceal different studies.
This reporting recommendation is our inference from the documented options. [W37]

### 5.4 Available transfer capability: PW-S3

ATC is separately licensed. It increases a defined source-to-sink MW transaction and
finds the element/contingency combinations that constrain it. Its setup reuses PTDFs,
LODFs, contingency data and monitoring limits. Outputs identify transfer direction,
limiting object, contingency and limiting transfer. [W45][W49]

| Documented method | Behavior | Limitation | Sources |
| --- | --- | --- | --- |
| Single Linear Step | Predicts transfer limits from the present operating point | Fixed linearization does not follow changing controllers | [W46][W47] |
| Iterated Linear Step | Ramps, resolves and recalculates to include operating-point/control changes | Remaining contingency effects can still be linear approximations; reserve/abort/divergence conditions matter | [W47] |
| Iterated Linear then Full CTG | Carries selected limiters into explicit contingency solutions | More expensive; limiter count, iteration policy and ramp location affect results | [W48] |

The transfer-limiter table differentiates equipment limits, reserves and convergence
outcomes. A divergence-limited result must not be relabeled as a proven thermal
rating or a certified voltage-collapse point. [W49]

### 5.5 Static voltage stability: S17

PVQV is an add-on. Here PV means real-power transfer versus voltage, not photovoltaic
energy. The analyst defines source/sink participation, monitored buses, contingencies,
step/ramp options and quantities to track. The PV workflow solves successive operating
points; QV varies a bus voltage/reactive-support condition to determine reactive
margin. Live diagrams and curves update during ramping. [W50][W51][W52]

PV output includes voltage trajectories versus transfer, limits and failure points.
QV output relates reactive support to voltage and can include reserve considerations.
The public overview allows tracking other quantities such as generator output and
voltage sensitivity. [W50][W52]

**Method boundary:** the sources read describe repeated power-flow continuation in
operating conditions. They do not establish that a particular predictor-corrector
continuation formulation is implemented. Static margin is also distinct from
short-term dynamic voltage recovery. These are deliberate unknowns, not inferred
capabilities. [W50][W51]

### 5.6 OPF, SCOPF and reserves: S14, S26, PW-S4

OPF dispatches controllable resources while respecting selected network constraints;
outputs include dispatch and locational marginal prices. Results can be displayed on
onelines/contours or exported as tables, text and AUX. It is an optional licence.
[W53]

**Documented method.** Primal LP OPF alternates a solved power flow with a linearized
optimization of controls/constraints. It updates the controls and resolves the
nonlinear network until the change criterion is met. Feasibility slack variables
carry penalties. This is sequential linear programming, not evidence of a vendor
AC interior-point solver. [W54]

**Constraints and economics.** Power-flow equations and regulation enforce some
constraints; the LP enforces others. The help explicitly distinguishes equalities
from potentially binding inequalities. Cost/benefit data, enabled controls and
monitoring rules belong to the study inputs. Different cost representations can
produce different dispatch behavior. [W55][W87]

SCOPF combines OPF with solving the specified contingencies to find a pre-contingency
dispatch subject to security constraints. Both OPF and SCOPF licences are required.
This is not synonymous with running a separate corrective OPF after each outage.
[W56][W37]

Reserves optimization adds resource bids and area/zone requirements for regulation,
spinning and supplemental services. It jointly considers energy and reserve markets
and needs OPF. Outputs include allocation and marginal prices reflecting reserve
requirements. The module is not evidence of full mixed-integer unit commitment with
start-up/minimum-up/down constraints. [W57]

### 5.7 Fault analysis: F2, F6 and qualified F1

The fault dialog depends on a solved load-flow case plus sequence impedances,
transformer grounding/phase data and optional mutual coupling. Single and multiple
fault definitions are available. Generator impedances and branch sequence data are
additional to steady-state dispatch. [W90][W21][W28]

The single-fault page supports three-phase, single-line-to-ground, line-to-line and
double-line-to-ground faults at a bus or along a branch. Inputs include fault
impedance/location. Outputs include phase/subtransient currents, angles and detailed
bus/branch/generator results, in amperes or pu. [W95]

Options select solved-power-flow, Flat Classical or Flat IEC-909 pre-fault profiles,
with controls for taps, charging and shunts. The UI can substitute phase fault
voltages/currents for the usual flow fields. This needs a visible study mode so a
reader does not mistake fault-current values for normal MW. [W91][W103]

**Important data warning.** The help documents fallback sequence data and winding
assumptions when explicit inputs are absent. Those are vendor behaviors, not sourced
engineering values authorized for Quantic. Transformer winding configuration controls
grounding; phase shift is taken from the load-flow branch phase data, so one does not
replace the other. [W90][W18]

**Standard boundary.** A menu called Flat IEC-909 does not establish complete
IEC 60909-0:2016/2026, ANSI C37 device duty, breaking-current decay or thermal-duty
compliance. This dossier makes no such certification claim. The public help read does
not provide that full clause-by-clause coverage. [W91]

### 5.8 Transient stability and dynamic models: T1, T2, T5

The add-on studies machine/network response to timed disturbances. Inputs include a
consistent solved initial condition, dynamic models, start/end times, timestep,
events and performance criteria. Machines, excitation, governors, stabilizers, loads,
renewables, relays, shunts and DC links have separate model families. [W58][W62]

The documented numerical scheme alternates explicit differential integration with
algebraic network solutions, using second-order Runge-Kutta and special handling for
ignored states and fast sub-interval models. The options expose network convergence
and failure handling. These facts do not reveal the proprietary sparse matrix
backend or establish an EMT switching solver. [W59][W60]

The study dialog leads from event definition through options, storage, plots, results,
limit monitors and validation. Output storage can target RAM, disk, both or neither;
stored samples can be less frequent than integration steps, while performance
monitors are checked during simulation. Thus plot decimation is not the same as a
larger integration timestep. [W62][W66]

**Validation caveat.** Validation and auto-correction are separate operations.
Auto-correction permanently changes model inputs. Unsupported models can be treated
as errors, warnings or inactive models according to options. A successful run is not
proof that every imported model participated. [W61][W92]

**T2, user-defined models.** UDMs are compiled DLLs with a defined interface, parameters
and states, attached to model instances. The public help names C++, Fortran and Pascal
as possible DLL implementation languages. This does not identify the language of the
entire proprietary Simulator core, nor establish FMI/FMU compatibility. [W64][W7]

### 5.9 Motor starting, small-signal and modal analysis: M2, qualified T3

PowerWorld publishes an induction-motor start tutorial using transient stability and
CIM5/CIM6 models. It emphasizes start-capable models, mechanical torque definition and
small integration steps during low-speed electrical transients. This establishes a
dynamic starting workflow, not a comprehensive industrial starter-selection package.
The 2013 tutorial's restrictions are historical and are not automatically current
Version 24 restrictions. [W97]

SMIB Eigenvalues linearizes an individual machine with its controls against an
infinite bus. It exposes eigenvalues/eigenvectors, state participation and the A
matrix for model checking. It is not evidence of a full interconnected-system
small-signal eigenvalue solver. [W63]

The transient Result Analyzer fits damped sinusoids to recorded signals over a chosen
time window. Its documented method is Iterated Matrix Pencil, with detrending and
selection of additional poorly fitted signals. It warns that discontinuities such as
fault application/clearing can make a fitted window misleading. Signal-derived modes
and network state-matrix modes must remain distinct matrix rows. [W89]

### 5.10 GIC, GMD and the GICHarm integration: PW-S5, qualified H1

GIC is an add-on for geomagnetic disturbance and HEMP E3 analysis. Required inputs
include topology, coordinates, line/winding DC resistance, grounding and an electric
field or time-varying induced-voltage series. Uniform and spatial/time-varying field
modes are documented. Outputs include line/neutral/effective currents and transformer
reactive impact. [W67][W68][W69]

The induced-DC network can be solved alone or coupled to AC power flow/transient
stability, with GIC-related transformer reactive demand included. The help exposes
used/assumed grounding values, which matters when field data are incomplete. These
are low-frequency network effects, not a general earthing step/touch-voltage design
study. [W68][W69]

Version 24 integrates EPRI GICHarm: solve GIC, solve the GIC-enhanced operating point,
calculate harmonics, check device tripping and repeat if equipment is removed.
This is positive evidence for that coupled workflow; it is insufficient evidence of
a standalone general-purpose harmonic/filter-design package with every IEEE 519
reporting function. The July 2025 presentation describes external GICHarm v6 with its bundled OpenDSS,
OpenDSS-file export, external batch execution and imported bus THDv. It labels the
then-current functionality beta. The presentation calls those EPRI tools open source;
exact distribution licence obligations were not independently established here.
[W70][W102]

### 5.11 Integrated topology processing: G2, PW-D1

ITP links node-breaker/full-topology and planning representations. The documented
implementation maintains the detailed topology and an equivalent consolidated view;
controls expose consolidation and breaker behavior. Full-topology studies should
use topology processing to avoid a large ill-conditioned network of switching
connections. It is separately licensed. [W71][W72][W104]

The implication for Quantic is a distinction between physical connection points,
switching devices and numerical buses, with stable mapping back to original assets.
This is our architectural inference, not a proposal to copy PowerWorld's internals.
[W104]

### 5.12 Time, weather, scheduling and distributed runs: D8, D15, S13

| Feature | Inputs and behavior | Outputs and boundaries | Sources |
| --- | --- | --- | --- |
| Time-Step Simulation | Explicit time points, changing dispatch/load and options; solves successive power flows, or licensed OPF/SCOPF | Time-indexed operating points and prices; not differential integration | [W74] |
| Weather models | Weather stations and measured/forecast inputs modify branch/generator limits and weather-dependent generation | Wind/solar/temperature model families; does not establish detailed PV geometry/shading or a bankable energy model | [W75][W76] |
| Scheduled Actions | Start/end/view times, resolution, action groups and operating changes | Gantt view and case snapshots; scheduling an outage is not optimizing a construction project | [W77] |
| Distributed analyses | Master process dispatches independent jobs to SimAuto instances via Distributed COM | Contingency, ATC, transient and QV licensing/configuration; it is not proof that a single Newton solve is distributed | [W73][W2] |

The distributed-computing product page contains an old sentence about QV being
planned while its own licence list and the Version 24 changes describe Distributed
QV. The later explicit release notes take precedence for current feature availability;
this inconsistency is recorded rather than silently merged into a fictional version.
[W73][W2]

### 5.13 Reduction and line-parameter calculations: S11, S24, qualified C8

Network equivalencing retains a study subsystem and reduces the external system by
bus-admittance matrix reduction. Equivalent boundary connections and shunts/loads
approximate the original behavior. What is retained affects validity under later
operating changes; it is not a universal replacement of the full case. [W88]

The overhead transmission-line calculator uses conductor data and tower configuration
to produce distributed, total and per-unit R/X/B/G, with MVA/kV bases and intermediate
GMR/GMD results. It has editable conductor and tower data. That establishes reusable
line-parameter types, not a verified broad manufacturer equipment library or an
underground-cable ampacity solver. [W96]

## 6. Workflow and interface

### 6.1 How the engineer moves through a study

The documented interface separates Edit and Run activities. The oneline offers
interactive equipment views; the Model Explorer gives hierarchical access to the
underlying tables, filters, fields and solution details. An engineer can work from
records even when no diagram exists. This is a particularly useful distinction for
large imported cases. [W8][W9]

A representative documented workflow is:

1. Open/import a case and inspect its object tables, parameters and key mappings.
   Check the format-specific conversion rules. [W10][W11]
2. Set model data, controls, solution options and the monitored limits. Define data
   checks for suspect records. [W13][W32][W35]
3. Solve and inspect convergence plus engineering violations. Retain a base solution
   for later comparison. [W30][W12]
4. Open a study-specific dialog, define scenarios/events and select what to store.
   Contingencies, dynamic events and time-step points are different inputs.
   [W37][W62][W74]
5. Examine tables, curves, oneline fields and comparisons. Export data together with
   the method/options needed to interpret it. The need to retain those settings is
   our reproducibility recommendation. [W12][W53][W66]

### 6.2 Diagram and table behavior

**G3, G5, G6, G8.** Bus View automatically presents a bus and its connected devices;
Geographic Data Views place supported objects from coordinates and style attributes
from data fields. Display Explorer edits graphical properties separately from the
model. Contouring maps voltage, angles, loading and other quantities across a view.
These are complementary views of one network. [W81][W93][W80][W78]

**D18.** Model Explorer has a navigation tree, field pane, recent tabs, toolbar,
search and filtering controls. The field pane controls table columns; user-defined
views can expose another selection of fields. This is evidence for configurable
information views, not a promise that every menu arrangement is stable across builds.
[W8]

**G10.** Difference display affects oneline and table values. A field showing a small
voltage difference is not necessarily showing absolute voltage. The base/present/
difference/change mode must remain evident to avoid incorrect readings. [W12]

**D17, G6.** Geographic views require coordinates and a valid map projection. Their
appearance can encode field-driven color, size, rotation and visibility. This does
not turn screen geometry into impedance or establish a geographic routing design
engine. [W93]

### 6.3 Concrete fault-study screen anatomy

The 2024 training material shows the fault dialog with a navigation tree on the left,
location/type/impedance/current controls above, and detailed results in grids below.
Single-fault subviews include buses, lines, generators, loads, switched shunts and
Y-bus matrices. The options page changes the pre-fault profile and which phase results
appear on the oneline. These are observations of the published training figures,
not a test of a locally installed Version 24 build. [W103, slides 12 and 17][W91]

For Quantic, the useful interaction principle is to preserve one clear selected
study and its units across every result panel. Reusing a normal-flow numeric field
for fault current requires an explicit visible mode. This recommendation is inferred
from the vendor's documented field substitution, not a copied screen design. [W91][W103]

### 6.4 Curves, alerts and export

| Result surface | What it communicates | Boundary | Sources |
| --- | --- | --- | --- |
| Power-flow message/convergence display | Numerical success, failures and controller progress | Successful solving alone does not enforce every rating | [W30][W32] |
| Limit-monitor tables | Branch, interface, voltage and bus-angle criteria | Disabled groups/areas/zones exclude limits | [W35] |
| ATC limiter tables | Limiting transfer, element, direction/scenario and contingency | Reserve and divergence outcomes need separate interpretation | [W49] |
| PV/QV plots | Voltage response, transfer/reactive margin and tracked signals | Static response, not a transient time trace | [W50] |
| Transient plots/results | Time signals, events and performance-monitor outcomes | Stored sampling may be coarser than integration | [W62][W66] |
| AUX, text and spreadsheet exports | Selected data/results for further processing | A partial AUX is not necessarily a restorable whole case | [W53][W10] |
| PWD / AXD views | Diagram metadata or text-based graphical objects | Different files from electrical-model AUX | [W98][W94] |

**G13.** Model Explorer can expose Y-bus/Jacobian information and a line calculator
shows intermediate quantities. This is not evidence that every study automatically
produces substituted, independently recomputable equations in its report. Mark the
full Quantic D11 working-report requirement as unverified for PowerWorld. [W8][W96]

### 6.5 Scripting, SimAuto and model extensions

**D14, D15.** AUX combines DATA and SCRIPT sections for text-based updates and batch
actions. AXD uses similar syntax for graphical objects but is a separate display
interface. This is a documented automation route even without assuming all studies
use the same options or all script commands are licence-independent. [W94]

SimAuto is a Windows COM automation server that can read/change case data, run
Simulator functions and return results to a calling program. Version 24's typed
retrieval calls reduce reliance on parsing numeric strings. `GetParamsRectTyped`
returns an object-by-field array with a requested common type; `GetParamsTypedCols`
permits per-column types. Both return an error channel that callers must check.
A COM API is not a cross-platform REST service. [W6][W100][W101]

UDM DLLs extend dynamic model physics. They are a different integration surface from
SimAuto, which orchestrates cases and studies. Supporting one does not imply support
for the other or for FMI co-simulation. [W64][W6]

## 7. What users value and what they complain about

### 7.1 Evidence quality

This section distinguishes utility-authored experience from vendor claims. The
public conference collection supplies attributable utility presentations, but it is
vendor-hosted and curated. It is not a representative customer-satisfaction survey.
No numerical satisfaction rating or claim about typical users is made. [W85]

### 7.2 Attributable observations

| Source and date | Reported value or friction | Careful interpretation for Quantic |
| --- | --- | --- |
| Tracy Rolstad, Avista, June 2017 | Describes the value of large contingency tables and 64-bit memory capacity, while reporting burdensome large files, paging and failed large runs | Historical experience under that hardware/version, not a benchmark against Version 24. Plan storage and job-size limits as first-class design requirements. [W83, slides 7 to 14] |
| James O'Brien, BPA, 2013 conference | Describes repeated manual editing when RAS logic is embedded in individual contingencies and topology changes; argues for condition/expression-based event logic | Shows why reusable action logic matters to study maintenance. It does not prove a current product defect; modern remedial-action containers address a related workflow. [W84, slides 3 to 24][W40] |
| Vendor distributed-computing notes | Independent jobs can benefit from multiple cores/computers; actual gains depend on workload, memory and communication | Useful execution architecture evidence, not an independent speedup measurement. [W73] |
| Vendor patch history | Documents corrections to imports, automation and result handling | An engineering tool needs patch-level provenance and regression fixtures. A bug list does not establish comparative reliability. [W3] |

### 7.3 Findings that remain uncertain

The deepening pass adds independent observations below. They are identifiable
individuals or institutions, not a representative sample. Old comparisons do not
establish today's relative features, regional acceptance or support quality.

| Author and date | Observation or use | Evidence limit |
| --- | --- | --- |
| Eng-Tips `tlrols`, 2011-11-16 and 2011-12-01 | Favors PowerWorld's support and data browsing/editing alongside PSLF/PSS/E; distinguishes transmission interconnection work from plant studies | Self-described multi-tool practitioner who says they do not work for PowerWorld. Identity/employment unverified, strongly favorable anecdote. Broad capability/industry-acceptance assertions are not adopted as facts. [W160] |
| Justin Chebahtah (`Chebahtah`), 2011-12-07 | Reports finding the trial intuitive after prior PSLF/PSS/E experience, and useful for personal planning/oversight | First-person experience after returning to the product, not a completed comparative solver test. [W160] |
| Eng-Tips `dpc`, 2011-11-28 | Emphasizes utility-required dynamics data and distinctions between transmission and industrial tools | Useful counterweight: accepted formats/customer requirements can drive selection independently of ease of use. Historical, not a current procurement rule. [W160] |
| Paras Mandal, UTEP, syllabus revised 2021-09-12 | Requires PowerWorld assignments/projects with Glover sixth edition, and provides a named software coordinator | Independent institutional adoption evidence. It measures neither satisfaction nor superiority over another package. [W161, pp. 1 to 2 and 6] |
| M. R. Jamieson and K. R. W. Bell, University of Strathclyde, 2024-03-20 | Lists PowerWorld with PowerFactory, PSS/E and other load-flow tools, discussing model choice for different phenomena | Primary academic comparison of modelling scope, not a product ranking or speed/accuracy benchmark. Non-exhaustive lists cannot prove absence of unlisted features. [W162, pp. 3 and 14] |

Reddit searches found two relevant **r/PowerSystemsEE** records, rather than an
established source set in the requested r/PowerSystemsEngineering: *Transfer into
Power Industry* (comments dated 2023-08-06) describes PowerWorld as a learning route;
*Dynamics/Transient Studies* (2026-07-29) praises documentation/training. Direct
threads/API retrieval failed and the retrieved records omit comment usernames.
Author: unavailable. They remain search leads, excluded from the attributable
sentiment conclusions. The first also overstates free access without distinguishing
licence editions; section 1 supplies the verified entitlement instead. [W163][W164]

No robust current sample of PowerWorld-specific complaints or independent current
head-to-head testing against ETAP/PowerFactory was established. Do not manufacture
negative reviews to balance the favorable anecdotes, or infer present market share,
reliability, satisfaction scores or buyer consensus from these sources.

**Our synthesis, inferred:** users need both fast exploration and maintainable,
replayable studies. A pleasant animated oneline without dependable input mapping,
limit interpretation, reusable scenario logic and manageable result storage would
miss the engineering workflow reflected in these sources. [W84][W83][W12][W66]

## 8. Engines implied by the documented capabilities

This inventory describes mathematical responsibilities. It does not identify
proprietary implementation languages, third-party numerical libraries or licences
that the vendor has not publicly disclosed. The suggested verification work is for a
future approved WP, not implementation performed here.

| Engine or subsystem | Directly documented mathematics/behavior | Independent verification required for Quantic | Sources |
| --- | --- | --- | --- |
| AC network solver | Nonlinear power balance, Newton iterations and enclosing controller/MW loops | Authored networks, independent solver and controller-limit cases | [W30][W31][W32] |
| Linear/DC solver | Admittance approximation with selectable resistance/conductance treatment | Analytical small networks with explicitly fixed conventions | [W34] |
| Network sensitivities | Jacobian/linear response, PTDF, LODF, OTDF and TLR | Perturb-and-resolve checks plus singular/islanding cases | [W42][W43][W44] |
| Security-analysis orchestrator | Apply events, balance changes, solve, monitor and restore; optional screening/RAS | Deterministic event/state tables and invariants for untouched cases | [W37][W38][W40] |
| Transfer-limit search | Linear prediction, repeated ramping and explicit contingency resolution | Independently bracketed transfer limits with controls and reserves | [W46][W47][W48] |
| Voltage-margin engine | Repeated power flows under transfer and reactive/voltage variation | Small-network curves and an independently defined collapse/margin criterion | [W51][W52] |
| Economic optimization | Sequential primal LP around solved operating points; security/reserve extensions | Analytic economic-dispatch cases, constraint feasibility and dual-price checks | [W54][W55][W56][W57] |
| Sequence fault solver | Sequence-network data and phase-resolved fault calculation | Hand-derived balanced/unbalanced fault references; standards-specific methods separately sourced | [W90][W91][W95] |
| Phasor-domain dynamic solver | Differential/algebraic integration, RK2 and sub-interval handling | Machine/control analytic responses, event timing and timestep convergence | [W59][W60] |
| Motor acceleration model | Start-capable induction-machine/load dynamics and mechanical torque | Sourced equivalent circuit and torque/speed/inertia reference | [W97] |
| Small-signal model checker | SMIB state linearization/eigenvectors and participation | Independent Jacobian and known eigenvalues; no full-grid claim | [W63] |
| Signal modal estimation | Detrended damped-sinusoid fitting, Iterated Matrix Pencil | Authored signals with known modes, noise and discontinuity cases | [W89] |
| GIC engine | Induced-source resistive network, transformer effective currents and AC reactive impact | Linear DC reference plus sourced magnetic/thermal/VAR models | [W68][W69] |
| Harmonic co-analysis | External GICHarm/OpenDSS execution and THDv feedback to equipment state | Independent harmonic case and coupled-event termination checks | [W102] |
| Topology processor | Detailed connectivity and electrically consolidated numerical representation | Switch-state graph cases and equivalent-network equality checks | [W104][W72] |
| Network reduction | Admittance-matrix elimination with boundary equivalents | Schur-complement and retained-terminal comparisons | [W88] |
| Line-parameter engine | Conductor/tower-derived R/X/B/G and base conversion | Independent electromagnetic formulas and sourced conductor data | [W96] |
| Time-series orchestrator | Operating-point series with weather/scheduled actions | Calendar/step alignment, repeatability and study-state preservation | [W74][W75][W77] |
| Visualization/query layer | Multiple displays, tables, geographic styling and contours | Asset identity, unit/mode labels and query/result consistency | [W9][W8][W78][W93] |

**Language boundary.** C++/Fortran/Pascal UDM examples and COM callability are public
extension facts. They do not justify asserting that the entire application, Newton
engine or optimizer was written in any one of those languages. Sparse factorization
vendor, LP backend and internal parallelization remain unknown. [W64][W6]

### 8.1 Glover17 chapter and Simulator-case map

Source: Glover, Overbye and Sarma, *Power System Analysis and Design*, 6th edition,
2017. Page numbers below are printed pages, with one-based PDF page numbers in
parentheses. This is an index and verification assessment, not a reproduction of
worked examples, inputs, output tables, screenshots or case files. [W106]

**Verification boundary:** page-tagged text was read, including example headings and
cross-references. The private PDF is stored through Git LFS and its page images could
not be retrieved in this environment. Thus no numerical answer from the book is
listed or asserted verified here. The table distinguishes text-indicated completeness
from image legibility; every numerical benchmark remains a candidate until its PDF
pages and case-file permissions are checked. A request for private page access is
recorded in the agent channel. This limitation must travel into WP-2.12. [W106]

Assessment codes: **A** = text identifies input data and numerical answer tables or
an analytic calculation, promising for a small independently reconstructed check;
**B** = relies materially on the supplied case/diagram or dynamic settings, so the
printed passage alone is not established as a complete benchmark; **C** = primarily
a qualitative interaction/plot, useful for behavior but insufficient for a precise
numerical oracle. All have PDF-image legibility pending. [W106]

| Chapter, location and case identifier | Simulator feature demonstrated | Printed-result assessment |
| --- | --- | --- |
| Ch. 1, pp. 22 to 28 (42 to 48), Examples 1.1 to 1.3 | Animated flow, changing load/generation, opening elements, saving case versus diagram | C. Introductory interaction; do not treat the historical textbook edition's bus limit as today's demo entitlement. |
| Ch. 2, p. 51 (71), Example 2.3 | Active/reactive-power visualization | C. Supports the conceptual display workflow, not a large-system benchmark. |
| Ch. 3, p. 135 (155), Example 3_12 | Load-tap-changing transformer control | C. Animated control behavior; check control settings in the supplied file. |
| Ch. 3, pp. 138 to 139 (158 to 159), Example 3_13 | Off-nominal transformer ratio and Ybus | A candidate. Analytic admittance comparison; the tap-side convention must match before comparing entries. |
| Ch. 5, p. 281 (301), Example 5_4 | Distributed/lossless line behavior and voltage profile with load | A for the analytic line model, C for the animated screen alone. |
| Ch. 5, p. 288 (308), Example 5_8 | Parallel-line configuration and reactive charging | B. The text explicitly distinguishes the Simulator model's charging from the simplified preceding analysis. Do not demand identical numbers across those models. |
| Ch. 5, p. 293 (313), Example 5_10 | Series compensation and transfer | B. Capacitor bypass status is essential to identifying the operating point. |
| Ch. 6, pp. 347 to 349 (367 to 369), Example 6_9 | Five-bus model data, network admittance, case tables | A candidate. Printed input tables and network diagram form the small-case anchor for subsequent examples. |
| Ch. 6, p. 353 (373), Example 6_10 | Single-stepping Gauss-Seidel and inspecting mismatches | A candidate for iterations; historical educational-edition support is explicit. This is not evidence of current commercial V24 Gauss-Seidel entitlement. |
| Ch. 6, pp. 357 to 359 (377 to 379), Example 6_11 | Newton steps, Jacobian and final bus/branch output tables | A candidate. Simulator retains voltage-control rows that a reduced textbook Jacobian may eliminate, so compare equivalent systems rather than matrix dimensions alone. |
| Ch. 6, p. 359 (379), Example 6.12 using Example 6_9 | Generation redispatch and transformer loading | A candidate based on the preceding small system; retain the monitored rating and dispatch rule. |
| Ch. 6, pp. 361 to 362 (381 to 382), Example 6_13 | Larger network exploration, outage loading and low-voltage identification | B. The passage does not establish a complete printed branch/generator dataset; supplied case needed. |
| Ch. 6, p. 365 (385), Example 6_14 | Shunt switching and voltage/loss changes | A candidate built from Example 6_9; check shunt status and voltage dependence. |
| Ch. 6, pp. 366 to 367 (386 to 387), Example 6_15 | Transformer tap changes following outages | B. Inherits the larger case and its controls. |
| Ch. 6, p. 371 (391), Example 6.16 using Example 6_13 | Ybus/Jacobian sparsity visualization | C. This example demonstrates sparse matrices, not a sensitivity-result benchmark. |
| Ch. 6, p. 373 (393), Example 6_17 | DC power-flow approximation and angle solution | A candidate. Fix resistance, loss, tap and phase-shift conventions independently of the AC check. |
| Ch. 6, pp. 382 to 384 (402 to 404), Example 6_20 | Lossless economic dispatch with generator bounds | A/B. Analytic preceding dispatch tables are useful; full transmission-case completeness still requires checking the case. |
| Ch. 6, p. 386 (406), Example 6.22 | Dispatch including losses and penalty factors | A for the stated optimality calculation, B for recreating the exact pictured network. |
| Ch. 6, pp. 390 to 392 (410 to 412), Example 6_23 | Sequential-LP OPF and binding network limits | B. Identify the active constraints and costs from the supplied case. It is not an interior-point example. |
| Ch. 7, pp. 450 to 451 (470 to 471), Example 7_5 | Balanced faults and Zbus on the small network | A candidate. Machine, line and transformer input tables and fault results are identified. Prefault operating assumptions differ from ordinary loaded power flow. |
| Ch. 7, pp. 452 to 453 (472 to 473), Example 7_6 | Adding a branch and recomputing fault impedances/voltages | A candidate, derived from Example 7_5 with a stated network alteration. |
| Ch. 9, pp. 555 to 564 (575 to 584), Example 9_3 and Examples 9.4 to 9.6 | Sequence data, SLG/LL/DLG selection and transformer phase effects | A candidate for the small sequence-network calculations. Check phase/reference conventions; later examples reuse the same case rather than proving separately named case files. |
| Ch. 9, pp. 573 to 575 (593 to 595), Example 9_8 | Five-bus SLG fault sweep, current contributions and bus voltages | A candidate. The passage identifies input Tables 9.1 to 9.3 and output Tables 9.4 to 9.5. It does not establish an all-fault-type sweep. |
| Ch. 11, pp. 701 to 702 (721 to 722), Example 11_4 and 11_4b | Classical rotor-angle transient with and without damping | A for the analytic setup; C for precise values read from a plot. Damping distinguishes the two cases. |
| Ch. 11, p. 704 (724), Example 11_5 | Fault/event simulation and angle trajectory | A/C. Compare analytical setup or stability outcome; plotted precision must first be established. |
| Ch. 11, pp. 706 to 707 (726 to 727), Example 11_6 | Equal-area stability boundary and fault clearing | A candidate for analytic stability boundary; a clearing-time benchmark additionally needs the stated inertia/frequency and event interpretation. |
| Ch. 11, p. 709 (729), Example 11_7 | Angle/speed traces and phase portrait | A for the stated Euler calculation, C for equality to Simulator. The text explicitly says Simulator's second-order integration gives slightly different results. |
| Ch. 11, pp. 715 to 717 (735 to 737), Example 11_8 and 11_8A | Multimachine reduced network and relative rotor angles | A/B. The small-system reduction is promising; capture reference-frame choice, dynamic loads and damping. |
| Ch. 11, p. 718 (738), Example 11_9 | Larger multimachine line fault and clearing search | B. Requires the supplied larger case's dynamic records; a plotted boundary is not a fully printed model. |
| Ch. 11, pp. 721 to 722 (741 to 742), Example 11_10 | Two-axis synchronous-machine initialization and fault response | A candidate for initial-state calculation, B for exact transient reproduction until all case settings are checked. |
| Ch. 11, pp. 724 to 726 (744 to 746), Example 11_11 | Induction-generator wind-machine initialization and response | A candidate for the stated machine initial conditions; not a switching-level converter benchmark. |
| Ch. 11, pp. 729 to 730 (749 to 750), Example 11_12 | Type 3 doubly-fed generator initialization | A candidate for the stated algebraic initial conditions; transient control settings still matter. |
| Ch. 12, pp. 758 to 759 (778 to 779), Example 12_1 | Exciter/AVR initialization and transient voltage response | A candidate for initial states, B/C for complete dynamics and plotted values. Inherits the two-axis machine example. |
| Ch. 12, p. 760 (780), Example 12_2 | Type 3 reactive-power control and limits | A/C. Controller setup and qualitative recovery are established; inspect the plotted trajectory before choosing tolerances. |
| Ch. 12, p. 766 (786), Example 12_4 | Governor droop, load step and frequency response | A/B. The text distinguishes finite-duration simulation from the eventual analytic equilibrium; do not equate them. Complete network/control files remain to check. |
| Ch. 14, pp. 911 to 912 (931 to 932), Figure 14_22 | Primary-loop feeder switching/restoration | B/C. Requires the supplied feeder case. This does not demonstrate a native unbalanced three-phase load-flow engine. |

All rows above are indexed to [W106]; none is a newly released public benchmark.
The best first candidates are the small power-flow, sequence-fault, machine
initialization and analytic dispatch cases. Supplied textbook PWB/PWD files remain
subject to their own licence. Neither ownership of the book nor permission to read
it authorizes copying those files or its worked data into Quantic. For public large
systems, the separately published synthetic datasets below are the stronger route.

### 8.2 Texas A&M synthetic-grid verification candidates

The dataset publisher explicitly permits commercial and non-commercial use without
charge and encourages registration and paper citation. The visible download form
requires an email. We did not submit a form or invent contact details. No SPDX, CC or
MIT label, express redistribution grant, warranty or liability clause was established
from the pages read. Record these actual terms; do not relabel the datasets
public-domain or transfer PowerWorld's software licence to them. Any archive's bundled
terms still need inspection before redistribution. [W150][W152]

| Dataset | Formats described on its own page | Dynamics availability established by that page | Suggested role, inferred |
| --- | --- | --- | --- |
| ACTIVSg200, Illinois footprint | PowerWorld, MATPOWER, PSS/E RAW, PSLF EPC, corresponding dynamic files | Explicitly included | First manageable dynamic/network interoperability candidate. [W150] |
| ACTIVSg500, South Carolina footprint | PowerWorld, MATPOWER, RAW, EPC | Not stated in the page read; do not infer from family membership | Intermediate steady-state regression. [W151] |
| ACTIVSg2000, Texas footprint | PWB/PWD, AUX, MATPOWER, RAW, EPC | Explicit transient-stability and GMD data | Power-flow/contingency/OPF plus a separate dynamic verification profile. [W152] |
| ACTIVSg10k, western US footprint | PWB/PWD, AUX, MATPOWER, RAW, EPC | Explicit transient-stability and GMD data | Larger sparse-network and event workloads; vendor training also uses this family. [W153][W108] |
| ACTIVSg25k, northeast/mid-Atlantic footprint | PWB/PWD, AUX, MATPOWER, RAW, EPC | Explicit transient-stability and GMD data | Scaling and multi-area checks after smaller cases pass. [W154] |
| ACTIVSg70k, eastern US footprint | PWB/PWD, AUX, MATPOWER, RAW, EPC | Page cites dynamics-extension work but does not explicitly enumerate dynamic files in the current download | Large power-flow candidate; archive inspection required for dynamic claims. [W155] |
| Texas2k Series24 | PWB, AUX, MATPOWER, RAW, EPC | Six dynamics cases: original summer peak, original low-load, updated summer peak, updated low-load, high renewables, and low-load with grid-forming inverters | Modern IBR and low-inertia stress cases, with distinct dataset/version hashes. [W156] |
| Texas2k Series25 | PWB, AUX, MATPOWER, RAW, EPC | Updated summer-peak dynamics; page also describes expansion-planning variants/candidates | Current-generation mix and expansion scenarios, not interchangeable with the original Texas case. [W157] |
| Annual ACTIVSg time series | CSV for the 2,000- and 10,000-bus cases | Load/renewable time series, not dynamic model definitions | Time-step/scenario inputs. [W159] |

The publisher's format guide distinguishes `.m` (power flow and generator costs),
`.raw` (power flow) and `.dyr` (dynamics), and similarly `.epc` versus `.dyd`.
PWB/AUX can hold multiple study types; PWD is the diagram and TSB time series.
Consequently a MATPOWER export alone cannot verify the transient solver. The guide
identifies RAW v33, with possible conversion for v34. [W158]

**Proposed verification process, not work performed:** retain download date, archive
hash, dataset revision, exact file list and terms; inspect dynamic model names/support
flags before converting; normalize units, sign conventions, controls and event timing;
then compare residuals, flows and explicitly chosen event observables. Independent
implementations must agree on the model and initial state before numeric differences
are interpreted as solver defects. No archive was downloaded or simulator run in this
pass, so the table records publisher availability rather than tested round trips.
The cases are synthetic, not representations of the actual regional grids. [W150][W152][W158]

## 9. Gaps, qualification ledger and parity handoff

### 9.1 Coverage and stopping rule

The review covers the public product/add-on descriptions, current major-version and
patch documentation, the named help topics in section 2, vendor training figures,
two utility-authored conference presentations, owned Glover17 text, individual
practitioner observations, university documents and Texas A&M dataset pages. It does not claim to have read every
page of the continually changing web-help tree or every historical release. Source
counts are not a substitute for closed capability questions.

The following gaps name why this research cannot turn them into supported product
claims. An absent capability in this dossier means **unknown/no evidence**, unless a
source explicitly establishes a narrower limitation. It never silently means no.

### 9.2 Explicit unresolved questions

| Gap | Sources checked / observed boundary | Why unresolved; consequence |
| --- | --- | --- |
| Textbook numerical benchmarks | Glover17 map, section 8.1 | Page-tagged text was available, PDF page images were not. No numerical answer is released as verified, and supplied cases have not been cleared for redistribution. [W106] |
| Public-case archive fidelity/terms | Texas A&M publisher pages, section 8.2 | Availability and use permission established, archive files, bundled terms and dynamic-model compatibility not inspected. MATPOWER does not carry dynamics. [W150][W152][W158] |
| Exact contemporary OS/build support and machine sizing | Windows COM, 64-bit UDM guide, public overview | No current authoritative OS/RAM matrix found. Do not repurpose old Windows requirements or historical Avista hardware as current minimums. [W6][W7][W1][W83] |
| Full proprietary solver internals | Solution theory, LP and integration help | These disclose methods, not source code, sparse factorization library or optimization backend. Leave implementation language/backend unknown. [W31][W54][W59] |
| Full-system eigenvalue analysis | SMIB and transient modal-analysis topics | SMIB is per machine; signal fitting is measurement/trace analysis. Neither source establishes full-grid state-matrix eigenanalysis. [W63][W89] |
| IEC/ANSI duty coverage | Fault help and training | Flat IEC-909 is documented, but current standard editions, correction tables and complete device-duty coverage are not established. No compliance claim or copied constant. [W103] |
| Industrial TCC/protection coordination breadth | Study/add-on index, transient model families | Relay simulation/RAS does not establish fuse/breaker libraries, grading audit, CT saturation, distance plots or automatic settings. Detailed protection-library parity is unknown. [W58][W40][W4] |
| General harmonic and filter design | GICHarm integration and technical presentation | External harmonic workflow is established, but broad IEEE 519 reports/filter optimization are not. EPRI package licence/version must be checked at its own primary distribution before reuse. [W70][W102] |
| Native DC industrial-network, cable/earthing/arc-flash design | Base/add-on list, converter and line-calculator help | HVDC, GIC and overhead parameters cannot establish battery sizing, cable ampacity, IEEE 80 or IEEE 1584 features. These remain unknown. [W4][W25][W68][W96] |
| Unbalanced distribution steady-state load flow / EMT | Power-flow and transient help | Unbalanced faults and effective sequence faults in phasor dynamics are not a three-phase unbalanced load-flow or EMT proof. [W31][W59][W95] |
| Manufacturer device library completeness | Editable conductor/tower types and dynamic model catalogue | A parameter/type editor and named generic dynamic models do not prove an exhaustive current manufacturer library. [W96][W92] |
| Native revision timelines and collaborative merge | Difference Case, files and Scheduled Actions | Case comparisons and an outage Gantt are documented; a versioned multi-user engineering database is not established. [W12][W10][W77] |
| State estimation versus consuming its results | ITP and real-time product descriptions | Reading EMS/state-estimator data does not establish a Simulator-native estimator. Retriever is a distinct product. [W104][W99] |
| Unit commitment, probabilistic reliability, hosting capacity | OPF/reserves, weather and ATC help | Dispatch/reserves and transfer heatmaps do not establish integer commitment, adequacy Monte Carlo, reliability indices or distribution hosting-capacity standards. [W54][W57][W75][W45] |
| End-to-end substituted equation reports | Matrix/intermediate displays and export help | Public evidence supports some internal quantities and exports, not full D11 working for every result. [W8][W96][W53] |
| Current representative customer sentiment | Utility presentations, dated Eng-Tips practitioners, independent syllabus and academic comparison | Independent examples now supplement curated talks, but no representative current sample or current comparative product benchmark. Reddit authors unavailable. [W83][W84][W160][W161][W162][W163][W164] |
| Runtime performance and format round-trip fidelity | Vendor capacity statements and conversion notes | No licensed product was executed. Vendor examples are not our measured benchmarks; exact build/format fixtures need a later authorized test. [W1][W11] |
| Exhaustive dynamic-model/default inventory | Named inventory in section 4.4, support-table screenshots and model pages | Selected named models are now mapped; exhaustive current flags, import-only names and REGC_D schema remain unverified. Export support/active flags from the actual build; PTIST3 demonstrates a documented partial feature. [W92][W107][W108][W120][W2] |

### 9.3 Capability IDs for WP-2.12

These are evidence-scoped handoff cells, not Quantic implementation statuses. `partial`
means the row's full ETAP/PowerFactory wording is broader than the established
PowerWorld capability. `unknown` never means proved absent.

| Shared ID | PowerWorld evidence-scoped cell | Sources / qualification |
| --- | --- | --- |
| D1 | yes, case model shared across studies | [W8][W10] |
| D2 | partial, reusable conductor/tower and model types | No full shared equipment-type system established. [W96][W92] |
| D3 | yes, multiple diagrams per model element | [W9] |
| D4 | partial, case/reference states and operating actions | Not a claim of a separate persistent scenario-object architecture. [W12][W77] |
| D5 | partial, scheduled actions/time view | Not native revision/expansion-stage management. [W77] |
| D6 | yes, stored study options and definitions | [W10][W62] |
| D7 | unknown, industrial diversity categories | ZIP/scaling is narrower. [W22] |
| D8 | partial, time-step and weather-driven data | Not proven arbitrary time functions on every parameter. [W74][W75] |
| D9 | partial, case comparison | No multi-user merge database established. [W12] |
| D10 | yes, custom element fields/memos | [W18] |
| D11 | partial, conductor and dynamic-model catalogues | Manufacturer coverage unknown. [W96][W92] |
| D12 | yes, configurable checks and dynamic validation | Scope/options must be retained. [W13][W61] |
| D13 | partial, graphical undo and solve-state restore | Not universal model-data undo. [W14][W15] |
| D14 | module SimAuto, plus AUX scripting | Windows COM, not a native Python solver API. [W6][W94] |
| D15 | yes, scripts and repeated studies; distributed licences optional | [W94][W74][W73] |
| D16 | yes for RAW/EPC/dynamic formats; CIM/CGMES unknown | Avoid treating a compound row as universal format coverage. [W10][W65] |
| D17 | yes, geographic data views | GIS design breadth not established. [W93] |
| D18 | partial, configurable views/options | Full theme/profile compatibility not asserted. [W8][W86] |
| G1 | yes, interactive oneline/model editing | Exact IEC/ANSI symbol-library coverage unknown. [W9][W79] |
| G2 | module ITP and detailed/bus views | [W71][W72][W81] |
| G3 | yes, bus and geographic view generation | [W81][W93] |
| G4 | unknown, composite nested network containers | Dynamic composite loads are a different feature. [W58] |
| G5 | yes, live oneline result fields | [W91][W79] |
| G6 | yes, contours and field-driven styling | [W78][W93] |
| G7 | partial, topology/island analysis | Specific island-coloring interaction not verified. [W33][W104] |
| G8 | yes, tabular case information | [W8] |
| G9 | yes, monitored violations | Particular marginal/critical tier conventions unknown. [W35] |
| G10 | yes, base/present/difference/change | [W12] |
| G11 | partial, AUX/text/spreadsheet and diagram export | Full PDF/Word template-report parity unverified. [W53][W94] |
| G12 | partial, PV/QV and transient/modal plots | Do not imply TCC/R-X/spectrum/eigenvalue plot parity. [W50][W62][W89] |
| G13 | unknown, universal substituted-equation reports | Matrices/intermediates alone insufficient. [W8][W96] |
| S1 | yes, balanced AC Newton power flow | [W30] |
| S2 | partial, fast decoupled documented; historical educational Gauss-Seidel | Glover17 Example 6_10 establishes that older educational workflow, not current V24 commercial availability. [W30][W106] |
| S3 | yes, Q limits and capability behavior | [W20][W32] |
| S4 | yes, tap/remote regulation | [W19] |
| S5 | yes, phase shifters | [W19] |
| S6 | partial, AGC and island slack/control | Full primary/secondary/droop row requires model-specific evidence. [W30][W33] |
| S7 | yes, ZIP loads | Exponential family not inferred from ZIP. [W22] |
| S8 | partial, conductor data at temperature | Not a claim of automatic study-wide correction. [W96] |
| S9 | yes, multiple-island slack options | [W33] |
| S10 | unknown, unbalanced load flow | Fault capability does not establish it. [W31][W95] |
| S11 | yes, overhead conductor/tower parameter calculation | Mutual fault data also supported. [W96][W28] |
| S12 | partial, AC network with HVDC models | Not industrial battery/charger DC load flow. [W25][W26][W27] |
| S13 | yes, base time-step simulation | Licensed OPF/SCOPF can run per point. [W74] |
| S14 | module OPF, sequential LP | Does not satisfy the row's specific interior-point method. [W54] |
| S15 | yes, base contingency analysis | Includes separate AC combination workflow and RAS. [W36][W41][W40] |
| S16 | yes, transfer/outage sensitivities | [W42][W43][W44] |
| S17 | module PVQV | Static margins; modal distinction in T3. [W50] |
| S18 | unknown, native state estimator | Consumers of EMS estimates are not estimator evidence. [W99][W104] |
| S19 | unknown, full hosting-capacity workflow | ATC is not sufficient evidence. [W45] |
| S20 | unknown, optimal capacitor placement | Voltage-controlled shunts alone insufficient. [W23] |
| S21 | unknown, distribution reconfiguration/phase balancing | Switching actions alone insufficient. [W39] |
| S22 | unknown, probabilistic load flow | Weather inputs alone insufficient. [W75] |
| S23 | unknown, reliability indices/restoration optimization | Security contingencies alone insufficient. [W36] |
| S24 | yes, admittance-matrix network reduction | Particular Ward/REI variants require more evidence. [W88] |
| S25 | unknown, allocation from meter measurements | Scaling does not establish estimation/allocation. [W82] |
| S26 | partial, dispatch and reserve optimization | Unit commitment not established. [W54][W57] |
| F1 | partial, Flat IEC-909 option | No verified edition/duty completeness. [W91] |
| F2 | yes, SLG/LL/LLG | [W95] |
| F3, F4, F5 | unknown, complete ANSI/IEC 61363/DC-fault methods | Public fault profiles insufficient. [W91] |
| F6 | partial, solved-power-flow pre-fault profile | Complete-method equivalence not claimed. [W91] |
| F7 | unknown, broad device-duty library audit | Subtransient current output insufficient. [W95] |
| F8 | partial, bus/line fault locations and batches | Open-conductor/multiple simultaneous faults unverified. [W90][W95] |
| P1, P2, P3, P5, P6, P7, P8 | unknown as full protection-design rows | Relay model existence does not establish library/coordination/design parity. [W58][W92] |
| P4 | partial, timed dynamic events and relay/RAS responses | Backup coordination animation not separately established. [W58][W62] |
| A1, A2, A3, A4 | unknown, AC/DC/HV arc flash and labels | Not in inspected study/add-on descriptions. [W4][W82] |
| M1 | unknown, dedicated static motor-start tool | Dynamic starting established separately. [W97] |
| M2 | module Transient Stability, motor starting | Start-capable models and timestep caveats. [W97] |
| M3, M4 | unknown, comprehensive starters/parameter estimation | Motor model parameters are not a selection/estimation tool. [W97] |
| T1 | module Transient Stability | [W58][W59] |
| T2 | partial, UDM DLLs and model-family views | Not proven graphical model authoring or FMI. [W64][W92] |
| T3 | partial, SMIB eigenvalues and signal modes | Full-system eigenvalue analysis unverified. [W63][W89] |
| T4 | unknown, general EMT solver | Phasor transient integration insufficient. [W59] |
| T5 | partial, event/load/relay response | Full fast-bus-transfer/generator-start row not established. [W58][W62] |
| H1 | module GIC with external EPRI GICHarm | General harmonic/frequency-scan breadth unverified. [W70][W102] |
| H2, H3 | unknown, full filter/compliance/flicker package | GIC-harmonic integration insufficient. [W102] |
| C1, C2, C3, C4, C5, C6, C7 | unknown, industrial design calculators | Neither fault studies nor line constants establish these. [W4][W96] |
| C8 | partial only for line parameters | Mechanical sag/tension/ampacity design not established. [W96] |

PowerWorld-specific distinctions to retain as additional rows:

| ID | Capability | Evidence |
| --- | --- | --- |
| PW-D1 | Full-topology consolidation with planning/operations identity mapping | Module ITP. [W104] |
| PW-S1 | DC transmission approximation separately from actual HVDC models | Base options plus converter models. [W34][W25] |
| PW-S2 | Primary/secondary contingency reference-state logic and reusable RAS | Base security workflow. [W41][W40] |
| PW-S3 | ATC single-linear, iterated-linear and full-contingency refinement | Module ATC. [W45][W46][W47][W48] |
| PW-S4 | Security-constrained dispatch and reserve markets | Modules OPF/SCOPF/Reserves. [W56][W57] |
| PW-S5 | Electric-field-induced quasi-DC network with AC/GICHarm feedback | Module GIC, external harmonic engine. [W68][W102] |
| PW-T1 | SMIB eigenvalue validation versus fitted trace modes | Separate capabilities, not one generic stability checkbox. [W63][W89] |
| PW-X1 | Distributed independent study jobs through SimAuto | Separate licence/configuration boundary. [W73][W2] |

### 9.4 Research handoff, not permission to build

The dossier can supply PowerWorld cells and engine distinctions to WP-2.12. Questions
about absent features remain unknown; the matrix must not change them to no. A future
implementation WP needs its own independent numerical references, explicit standard
editions and owned paths. No engine code, existing contract, power adapter, UI or
licence dependency has been changed by this research.
