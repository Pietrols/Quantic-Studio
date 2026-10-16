# PowerWorld Simulator research dossier

Research dates: 2026-10-15 to 2026-10-16. Owner: Lane B, ChatGPT. WP-2.11, including authorized deepening passes.

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

Access dates are recorded per entry. `Help` means a vendor-published online help
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

| W106 | Glover, Overbye and Sarma, Power System Analysis and Design, 6th ed., Cengage, 2017 | Owned book, page-tagged text plus 30 private page renders inspected | 2026-10-15 |
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

| W165 | [Power-flow bus equations](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/PowerFlow%20Equation%20Basics.htm) | Vendor help | 2026-10-16 |
| W166 | [Remote voltage regulation](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/PowerFlow%20Remote%20Regulation.htm) | Vendor help | 2026-10-16 |
| W167 | [Mvar sharing](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/PowerFlow%20Mvar%20Sharing%20between%20Generators.htm) | Vendor help | 2026-10-16 |
| W168 | [Voltage setpoint tolerance](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/PowerFlow%20Voltage%20Setpoint%20Tolerance.htm) | Vendor help | 2026-10-16 |
| W169 | [Voltage droop with deadband](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/PowerFlow%20Voltage%20Droop%20Control%20with%20Deadband.htm) | Vendor help | 2026-10-16 |
| W170 | [James Weber, Detailed Documentation of Software Implementation of Voltage Droop With Deadband in Power Flow Calculation, November 2018](https://www.powerworld.com/WebHelp/Content/Other_Documents/VoltageDroopControl_Software_Implementation.pdf) | Vendor technical paper; pp. 2, 4 and 19 visually inspected | 2026-10-16 |
| W171 | [Full-topology model](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/TP_Full_Topology_Model.htm) | Vendor help | 2026-10-16 |
| W172 | [FixedNumBus features](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/FixedNumBus_Features.htm) | Vendor help | 2026-10-16 |
| W173 | [Sub-interval integration models](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transient_Stability_Integration_Subinterval_Models.htm) | Vendor help | 2026-10-16 |
| W174 | [Bus plant controller REPC_D](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Bus%20REPC_D.htm) | Vendor model help | 2026-10-16 |
| W175 | [July 7, 2023 patch](https://www.powerworld.com/patch/july-7-2023) | Historical vendor patch | 2026-10-16 |
| W176 | [October 25, 2023 patch](https://www.powerworld.com/patch/october-25-2023) | Historical vendor patch | 2026-10-16 |
| W177 | [MATPOWER manual: branch model, section 3.2](https://matpower.app/manual/matpower/Branches.html) | Independent engine's mathematical documentation | 2026-10-16 |
| W178 | [MATPOWER manual: AC power flow, section 4.1](https://matpower.app/manual/matpower/ACPowerFlow.html) | Independent engine's mathematical documentation | 2026-10-16 |
| W179 | [MATPOWER manual: continuation power flow, chapter 5](https://matpower.app/manual/matpower/ContinuationPowerFlow.html) | Independent engine's mathematical documentation | 2026-10-16 |
| W180 | [MATPOWER manual: event detection, section 5.5](https://matpower.app/manual/matpower/EventDetectionandLocation.html) | Independent engine's mathematical documentation | 2026-10-16 |
| W181 | [MATPOWER manual: standard AC OPF, section 6.1](https://matpower.app/manual/matpower/StandardACOPF.html) | Independent engine's mathematical documentation | 2026-10-16 |
| W182 | [MATPOWER manual: standard DC OPF, section 6.2](https://matpower.app/manual/matpower/StandardDCOPF.html) | Independent engine's mathematical documentation | 2026-10-16 |
| W183 | [SUNDIALS IDA mathematical considerations](https://sundials.readthedocs.io/en/latest/ida/Mathematics_link.html) | Solver author's DAE documentation | 2026-10-16 |
| W184 | [ANDES 2.0.0 time-domain tutorial](https://docs.andes.app/en/v2.0.0/tutorials/04-time-domain.html) | Independent engine's workflow documentation | 2026-10-16 |
| W185 | [ANDES DAE formulation](https://docs.andes.app/en/latest/modeling/concepts/dae-formulation.html) | Independent engine's mathematical documentation; latest label is mutable | 2026-10-16 |
| W186 | [pandapower three-phase power flow](https://pandapower.readthedocs.io/en/stable/powerflow/ac_3ph.html) | Adapter candidate's public method/limitations | 2026-10-16 |
| W187 | [pandapower short-circuit currents](https://pandapower.readthedocs.io/en/stable/shortcircuit/currents.html) | Adapter candidate's public method/limitations | 2026-10-16 |
| W188 | [pandapower state estimation](https://pandapower.readthedocs.io/en/stable/estimation.html) | Adapter candidate's public method/limitations | 2026-10-16 |
| W189 | [OpenDSS harmonic flow](https://opendss.epri.com/HarmonicFlowAnalysis.html) | EPRI method/workflow documentation | 2026-10-16 |
| W190 | [PyPSA 1.1.1 unit commitment](https://docs.pypsa.org/v1.1.1/user-guide/optimization/unit-commitment/) | Independent optimization framework documentation | 2026-10-16 |
| W191 | [ANDES licence](https://github.com/CURENT/andes/blob/master/LICENSE) | Upstream licence, mutable branch | 2026-10-16 |
| W192 | [MATPOWER licence and case-file exclusion](https://github.com/MATPOWER/matpower/blob/master/LICENSE) | Upstream licence, mutable branch | 2026-10-16 |
| W193 | [SUNDIALS IDA introduction and licence](https://sundials.readthedocs.io/en/latest/ida/Introduction_link.html) | Upstream implementation/licence documentation | 2026-10-16 |
| W194 | [DSS-Python project and licensing notes](https://github.com/dss-extensions/DSS-Python) | Binding author's primary repository | 2026-10-16 |
| W195 | [OpenDSS circuit reduction, version 8.5](https://opendss.epri.com/CircuitReductionforVersion85.html) | Historical EPRI method/limitations | 2026-10-16 |
| W196 | [ETAP combined Getting Started demo guide](https://etap.com/docs/default-source/whats-new/etap_gettingstarted_demo.pdf?sfvrsn=60ea6a7c_39) | Public vendor tutorial; printed pp. 71, 75 and 76 visually inspected | 2026-10-16 |
| W197 | [PowerFactory dynamic numerical integration method](https://www.digsilent.de/index.php/en/faq-reader-powerfactory/what-is-the-numerical-integration-method-applied-in-dynamic-simulation-i-e-rms-stability-emt-electro-magnetic-transients.html) | Vendor FAQ | 2026-10-16 |
| W198 | [PowerFactory unexpected high damping](https://www.digsilent.de/en/faq-reader-powerfactory/what-can-be-the-reason-of-unexpected-high-damping-during-a-simulation.html) | Vendor FAQ; printed oscillation formula not adopted | 2026-10-16 |
| W199 | [PowerFactory DSL initialization hints](https://www.digsilent.de/index.php/en/faq-reader-powerfactory/do-you-have-some-hints-to-correctly-initialise-a-dsl-dynamic-model.html) | Vendor FAQ | 2026-10-16 |
| W200 | [PowerFactory internal solver co-simulation example](https://www.digsilent.de/en/faq-reader-powerfactory/do-you-have-an-example-for-the-internal-solver-co-simulation-emt-emt-or-rms-emt.html) | Public FAQ HTML recovered with curl; model attachment not executed | 2026-10-16 |
| W201 | [PowerFactory EMT-derived measurement quantities](https://www.digsilent.de/en/faq-reader-powerfactory/How-can-I-calculate-transformed-phasor-quantities-from-an-EMT-simulation-using-a-DSL-model.html) | Vendor FAQ | 2026-10-16 |
| W202 | [PowerFactory SMA EMT comparison against PSCAD, v3.0, December 11, 2025](https://www.digsilent.de/files/content/interne_downloads/PowerFactory_SMA_EMT_Model_Comparison_and_Benchmarking_against_PSCAD.pdf) | Public vendor benchmark; sections 3.1 and 3.2 inspected, printed p. 10 visually checked | 2026-10-16 |
| W203 | [FMI specification 3.0.2, November 27, 2024](https://fmi-standard.org/docs/3.0.2/) | Primary interface specification, selected clauses | 2026-10-16 |
| W204 | [ETAP Feeder Hosting Capacity](https://etap.com/product/feeder-hosting-capacity) | Vendor product page | 2026-10-16 |
| W205 | [ETAP hosting-capacity patent announcement, March 25, 2025](https://etap.com/company/news/corporate-news/2025/03/25/etap-granted-us-patent-for-advanced-hosting-capacity-analysis) | Vendor announcement; not a patent-scope or legal assessment | 2026-10-16 |
| W206 | [GIC modelling data requirements](https://www.powerworld.com/knowledge-base/gic-modeling-data-requirements) | Vendor input/assumption guidance, 2014 with 2017 template update | 2026-10-16 |
| W207 | [GIC and substation coordinates for line taps](https://www.powerworld.com/knowledge-base/gic-line-taps) | Vendor modelling note, 2015 | 2026-10-16 |
| W208 | [GIC sensitivity analysis](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/GIC_Analysis_Sensitivity_Analysis.htm) | Vendor help | 2026-10-16 |
| W209 | [TransLineCalc version 2 manual, April 22, 2013](https://www.powerworld.com/files/TransLineCalcHelp2.pdf) | Historical vendor mathematical documentation; printed p. 15 visually checked | 2026-10-16 |
| W210 | [OpenDSS LineGeometry](https://opendss.epri.com/LineGeometry.html) | Independent engine's primary geometry documentation | 2026-10-16 |
| W211 | [OpenDSS LineCode](https://opendss.epri.com/LineCode1.html) | Independent engine's primary matrix/reduction documentation | 2026-10-16 |
| W212 | [OpenDSS line model revision, 2006 with 2010 update](https://opendss.epri.com/LineModelRevision.html) | Historical engine note, not a current binary-version guarantee | 2026-10-16 |
| W213 | [PowerFactory four-wire cable modelling](https://www.digsilent.de/en/faq-reader-powerfactory/How_to_model_a_4_wire_cable_in_PowerFactory.html) | Vendor FAQ; linked model/calculation attachments not adopted | 2026-10-16 |
| W214 | [ETAP line constants](https://etap.com/product/line-constants) | Vendor product capability page | 2026-10-16 |
| W215 | [NERC, Application Guide: Computing GIC in the Bulk-Power System, December 2013](https://www.nerc.com/globalassets/standards/projects/2013-03/gic-application-guide-2013_approved.pdf) | Public technical guide, chapter 2 selected sections; printed pp. 16 and 18 visually checked | 2026-10-16 |
| W216 | [PowerWorld GIC calculation example and earth-model discrepancy](https://www.powerworld.com/knowledge-base/example-of-geomagnetic-induced-current-gic-calculations) | Vendor qualification of a historical benchmark | 2026-10-16 |
| W217 | [GIC time-varying electric-field inputs](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/GIC_Analysis_TimeVaryingElectricField.htm) | Vendor help; coarse-grid format wording is incomplete | 2026-10-16 |

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
| Release-name ambiguity | REGC_D versus bus-attached REPC_D | Release material names REGC_D, but detailed bus-model help and another patch name REPC_D. The latter has a readable schema; an alias between the tokens is not established. See section 8.3E. [W2][W174][W175][W176] |
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
algebraic network solutions, with second-order Runge-Kutta or selectable Euler and special handling for
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

**Visual follow-up, 2026-10-16:** inspected 30 privately supplied page renders.
This closes the blanket image-access gap recorded in the first pass. **V** below
means the stated result/derivation is legible on the inspected page, not that a
Simulator run reproduced it or that all inherited network data are verified.
**A** remains an analytical benchmark candidate; **B** requires supplied case data;
**C** is primarily qualitative/graphical. All numerical case inputs and answers stay
private. Uninspected prerequisite/output pages are named below. [W106]

| Chapter, location and case identifier | Simulator feature demonstrated | Printed-result assessment |
| --- | --- | --- |
| Ch. 1, pp. 22 to 28 (42 to 48), Examples 1.1 to 1.3 | Animated flow, changing load/generation, opening elements, saving case versus diagram | C. Introductory interaction; do not treat the historical textbook edition's bus limit as today's demo entitlement. |
| Ch. 2, p. 51 (71), Example 2.3 | Active/reactive-power visualization | C. Supports the conceptual display workflow, not a large-system benchmark. |
| Ch. 3, pp. 133 to 135 (153 to 155), Example 3_12 | Load-tap-changing transformer control | C. Animated control behavior; check control settings in the supplied file. |
| Ch. 3, pp. 137 to 139 (157 to 159), Example 3_13 | Off-nominal transformer ratio and Ybus | A candidate. Analytic admittance comparison; the tap-side convention must match before comparing entries. |
| Ch. 5, p. 281 (301), Example 5_4 | Distributed/lossless line behavior and voltage profile with load | A for the analytic line model, C for the animated screen alone. |
| Ch. 5, pp. 287 to 288 (307 to 308), Example 5_8 | Parallel-line configuration and reactive charging | B. The text explicitly distinguishes the Simulator model's charging from the simplified preceding analysis. Do not demand identical numbers across those models. |
| Ch. 5, pp. 292 to 293 (312 to 313), Example 5_10 | Series compensation and transfer | B. Capacitor bypass status is essential to identifying the operating point. |
| Ch. 6, pp. 346 to 349 (366 to 369), Example 6_9 | Five-bus model data, network admittance, case tables | A candidate. Printed input tables and network diagram form the small-case anchor for subsequent examples. |
| Ch. 6, pp. 352 to 353 (372 to 373), Example 6_10 | Single-stepping Gauss-Seidel and inspecting mismatches | A candidate for iterations; historical educational-edition support is explicit. This is not evidence of current commercial V24 Gauss-Seidel entitlement. |
| Ch. 6, pp. 356 to 359 (376 to 379), Example 6_11 | Newton steps, Jacobian and final bus/branch output tables | A candidate. Simulator retains voltage-control rows that a reduced textbook Jacobian may eliminate, so compare equivalent systems rather than matrix dimensions alone. |
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
| Ch. 7, pp. 453 to 454 (473 to 474), Example 7_6 | Adding a branch and recomputing fault impedances/voltages | A candidate, derived from Example 7_5 with a stated network alteration. |
| Ch. 9, pp. 554 to 564 (574 to 584), Example 9_3 and Examples 9.4 to 9.6 | Sequence data, SLG/LL/DLG selection and transformer phase effects | A candidate for the small sequence-network calculations. Check phase/reference conventions; later examples reuse the same case rather than proving separately named case files. |
| Ch. 9, pp. 574 to 575 (594 to 595), Example 9_8 | Five-bus SLG fault sweep, current contributions and bus voltages | A candidate. The passage identifies input Tables 9.1 to 9.3 and output Tables 9.4 to 9.5. It does not establish an all-fault-type sweep. |
| Ch. 11, pp. 699 to 702 (719 to 722), Example 11_4 and 11_4b | Classical rotor-angle transient with and without damping | A for the analytic setup; C for precise values read from a plot. Damping distinguishes the two cases. |
| Ch. 11, pp. 703 to 704 (723 to 724), Example 11_5 | Fault/event simulation and angle trajectory | A/C. Compare analytical setup or stability outcome; plotted precision must first be established. |
| Ch. 11, pp. 705 to 707 (725 to 727), Example 11_6 | Equal-area stability boundary and fault clearing | A candidate for analytic stability boundary; a clearing-time benchmark additionally needs the stated inertia/frequency and event interpretation. |
| Ch. 11, p. 709 (729), Example 11_7 | Angle/speed traces and phase portrait | A for the stated Euler calculation, C for equality to Simulator. The text explicitly says Simulator's second-order integration gives slightly different results. |
| Ch. 11, pp. 715 to 717 (735 to 737), Example 11_8 and 11_8A | Multimachine reduced network and relative rotor angles | A/B. The small-system reduction is promising; capture reference-frame choice, dynamic loads and damping. |
| Ch. 11, p. 718 (738), Example 11_9 | Larger multimachine line fault and clearing search | B. Requires the supplied larger case's dynamic records; a plotted boundary is not a fully printed model. |
| Ch. 11, pp. 721 to 722 (741 to 742), Example 11_10 | Two-axis synchronous-machine initialization and fault response | A candidate for initial-state calculation, B for exact transient reproduction until all case settings are checked. |
| Ch. 11, pp. 725 to 726 (745 to 746), Example 11_11 | Induction-generator wind-machine initialization and response | A candidate for the stated machine initial conditions; not a switching-level converter benchmark. |
| Ch. 11, pp. 729 to 730 (749 to 750), Example 11_12 | Type 3 doubly-fed generator initialization | A candidate for the stated algebraic initial conditions; transient control settings still matter. |
| Ch. 12, pp. 758 to 759 (778 to 779), Example 12_1 | Exciter/AVR initialization and transient voltage response | A candidate for initial states, B/C for complete dynamics and plotted values. Inherits the two-axis machine example. |
| Ch. 12, p. 760 (780), Example 12_2 | Type 3 reactive-power control and limits | A/C. Controller setup and qualitative recovery are established; inspect the plotted trajectory before choosing tolerances. |
| Ch. 12, pp. 764 to 766 (784 to 786), Example 12_4 | Governor droop, load step and frequency response | A/B. The text distinguishes finite-duration simulation from the eventual analytic equilibrium; do not equate them. Complete network/control files remain to check. |
| Ch. 14, pp. 911 to 912 (931 to 932), Figure 14_22 | Primary-loop feeder switching/restoration | B/C. Requires the supplied feeder case. This does not demonstrate a native unbalanced three-phase load-flow engine. |

**Page verification ledger for every A/A-B/A-C candidate:**

| Candidate | Image evidence and promotion decision |
| --- | --- |
| 3_13, 5_4 | Remain A: PDF 157 to 159 and 301 were not among the supplied renders; earlier text-only completeness assessment is unchanged. |
| 6_9 | PDF 369 verifies the Ybus/display and analytic continuation, but input Tables 6.1 to 6.4 on earlier pages were not visually checked. Remains A for complete-case reconstruction. |
| 6_10 | PDF 373 verifies the displayed iteration result and historical Gauss-Seidel workflow. V for that continuation only; preceding calculation on PDF 372 uninspected, so remains A as a full iteration benchmark. |
| 6_11 | PDF 377 verifies final bus-output Table 6.6; PDF 379 verifies transformer Table 6.8. V for these outputs. Line-output Table 6.7 on PDF 378 and original inputs remain uninspected. |
| 6.12, 6_14 | PDF 379 and 385 respectively verify the stated redispatch/loading and shunt-effect results. V for printed outcomes; inherited complete input verification remains A. |
| 6_17 | PDF 393 contains a legible reduced DC matrix, injection vector and solved angle vector on one page. Promoted V for a self-contained reduced linear-system check; does not certify the preceding AC-to-DC model derivation or a Simulator run. |
| 6_20 | PDF 402 verifies the heading and preceding Example 6.19 dispatch table, not complete three-generator case inputs or later output. Remains A/B; do not misattribute Table 6.10 to Example 6.20. |
| 6.22 | PDF 406 verifies the first penalty-factor/optimality calculation; its continuation and pictured network on PDF 407 are uninspected. V for that calculation only, A/B for the complete case. |
| 7_5 | PDF 470 verifies the three input tables and assumptions. Fault-output Table 7.7 and other continuation pages were not supplied; remains A for a full input/output benchmark. |
| 7_6 | Heading is PDF 473, not 472. The alteration and reference to output Tables 7.8/7.9 are legible, but those tables on PDF 474 were not inspected. Remains A. |
| 9_3 and 9.4 to 9.6 | PDF 576, 579 and 584 verify selected phase-domain results, the LL sequence calculation and transformer-phase explanation. V for those selected passages; complete inherited sequence data and the intervening DLG derivation remain uninspected. |
| 9_8 | PDF 594 verifies fault-current Table 9.4. Voltage Table 9.5 on PDF 595 and complete inputs on preceding pages remain uninspected. V for the current outputs, A for complete case reconstruction. |
| 11_4/11_4b | PDF 721 verifies the undamped analytic continuation and plotted behavior. PDF 719 to 720 and damping page 722 were not supplied. V for undamped continuation only; damping/full-case assessment remains A/C. |
| 11_5 | PDF 724 verifies the explicit clearing-time calculation and plot. V for the analytic continuation; preceding setup on PDF 723 remains uninspected. |
| 11_6 | PDF 727 verifies the critical-angle calculation. V for that continuation; heading/setup start on PDF 725 and remaining derivation on 726 need visual checking before full reconstruction. |
| 11_7 | PDF 729 verifies the integration-method distinction and case conditions, but the numerical answer table on later pages was not supplied. Remains A/C for a numerical trajectory benchmark. |
| 11_8/11_8A | PDF 736 verifies partitioned admittance matrices and event/reference-frame description. V for those matrices, A/B for a complete reduced-network/dynamic check; PDF 735 and 737 uninspected. |
| 11_10 | PDF 741 verifies machine inputs and initial-state calculations. V for the displayed initialization calculation, A/B for inherited network and transient response; continuation PDF 742 uninspected. |
| 11_11 | PDF 745 verifies the induction-machine parameters and stated initial conditions. V for their legibility; the antecedent operating point and continuation PDF 746 were not inspected, so remains A for an independently reconstructed initialization check. |
| 11_12 | PDF 750 verifies the final initial-state calculation. V for that continuation; heading and preceding calculation on PDF 749 were not rendered. |
| 12_1 | PDF 779 verifies AVR initial-state calculation; PDF 780 verifies explicitly stated timed voltage results. V for those passages. Full controller definition on PDF 778 and preceding control diagram remain uninspected. |
| 12_2 | PDF 780 verifies the listed controller settings, initial-state and fault reactive-output calculation. V for that local algebraic check; inherited machine model and trajectory still require prior pages/case data. |
| 12_4 | PDF 786 verifies model names, disturbance description and the distinction between finite-duration and equilibrium results. V for those statements; full setup/defaults beginning PDF 784 remain uninspected, so A/B for complete numerical reproduction. |

Also inspected PDF 381, 391, 410, 738 and 931: the larger-case, sparsity, OPF,
multimachine and restoration descriptions retain B/C status. Their pictured outputs
do not make complete machine-readable input cases. No source artwork or worked
case data is distributed with this ledger. [W106]

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

### 8.3 Mechanism-level reconstruction notes

Peter's 2026-10-16 instruction extends the research from capability names to how
the products work. The following separates documented Simulator behaviour from
our proposed engineering architecture. It does not establish ETAP or PowerFactory
internals, and does not copy vendor pseudocode, diagrams or source implementations.

#### A. Topology is a numerical preprocessing problem and an identity problem

Simulator's detailed model distinguishes lines, transformers, series compensation
and several switching-device types. Only eligible closed switching/very-low-
impedance branches can be consolidated. Even an eligible branch can be retained
because it participates in monitoring, an action, a condition or another special
relationship. Consequently a generic rule that merges every short branch is not
equivalent to the documented topology processor. Modelling an ideal switch as a
tiny arbitrary reactance instead also introduces ill-conditioning. [W171]

A SuperBus is a connectivity-derived voltage group. FixedNumBus is a user/file
identity grouping and can contain connection points with different voltage
phasors. Assignment can harmonize metadata or change conflicting IDs; RAW subnode
mapping is another distinct concern. **Inference:** Quantic should keep immutable
asset identity, physical terminals, numerical-node membership and foreign-file
identifiers separate. Switching should invalidate connectivity-dependent results
without renaming the installed equipment. Never use a diagram's bus number as the
only persistent asset identity. [W172]

**Proposed acceptance:** split and rejoin a fictional double-bus substation, test
normally open ties and retained event targets, and check that every result maps
back to the original terminals. Test identity collisions as explicit import
diagnostics, not silent overwrites. This is our test design, not an observed vendor
test suite. [W171][W172]

#### B. Equation choice belongs to the controller configuration

PowerWorld's bus category describes which equations are active, not just an
immutable equipment class. Ordinary PQ, PV and slack cases select power balances,
voltage or angle constraints; limits and special controllers alter that selection.
For standard polar power-balance equations, the Newton correction solves
`J(x) delta_x = -g(x)`. PowerWorld documents equation/control selection; MATPOWER's
independent manual documents the basic Newton formulation and alternative
coordinate/balance choices. These sources do not establish identical internal
state layouts. [W165][W178]

Remote regulation replaces local-only logic with a group relationship: one
participant supplies the remote voltage constraint, other participants satisfy
sharing equations, and the regulated load bus still satisfies its own power
balance. The regulated bus can therefore display PQ while its voltage is
controlled elsewhere in the equation system. **Inference:** the UI needs both an
equipment type and an active-equation/limit explanation; colouring every generator
bus as permanently PV hides essential behaviour. [W166]

Mvar allocation has three documented policies: normalized bus-average factors,
equal relative position in each generator's reactive range, or normalized sums of
factors. These need not produce the same individual outputs. Range-based sharing
can give both positive and negative generator Mvar even when the total is zero.
Limit saturation then redistributes responsibility within and between buses.
Matching total reactive injection is not sufficient to verify generator-level
parity. The chosen policy must be an explicit study input. [W167]

Nonzero voltage-setpoint tolerance replaces a hard voltage target with a sloping
relation between reactive limits. An original expression of the documented line,
for positive tolerance `dV` and before saturation, is
`Q(V) = Qmin + (Qmax-Qmin)*(Vset+dV-V)/(2*dV)`.
Its endpoints are maximum Q at the low-voltage edge and minimum Q at the
high-voltage edge. Zero tolerance requires a different PV formulation, not division
by zero. **Proposed tests:** endpoint substitution, negative slope, limit activation
and return from a limit. Values must be scenario inputs, not assumed grid-code
requirements. [W168]

#### C. Plant droop is measured at an interface, not necessarily at a machine

The deadband controller can regulate reactive flow arriving at the point of
interconnection, including intervening feeder/transformer effects, rather than
generator terminal Mvar. It supports multiple groups, individual machine limits
and topology checks. Overlapping control networks, an unreachable regulated bus
or conflicting voltage controls can be invalid configurations. The advertised
piecewise QV curve is not always the precise numerical curve: the help acknowledges
corner smoothing and restrictions on transitions and slopes. [W169]

Weber's public November 2018 paper explains the resulting residual in a simple
plant as `Q_arriving(V,theta) - Q_characteristic(Vreg) = 0`, with derivative
contributions from both the branch and the characteristic. It further treats
distributed groups, limits and low-impedance connections. Printed pp. 2, 4 and 19
were visually checked against extraction; only this mathematical description is
recorded, not its implementation pseudocode. **Inference:** compare values and
derivatives near corners, preserve requested versus effective curves, and report
any regularization. Reproducing an undocumented offset by loosening tolerances is
not a valid verification strategy. [W170]

#### D. Dynamic initialization, stepping and state changes are distinct stages

The current options page allows RK2 or Euler, so the general RK2 description is
not a guarantee of the method selected in every case. Initial limit violations
can abort, temporarily modify limits, or leave limits active and cause immediate
state movement. Network mismatch settings are separate from ordinary power-flow
settings. The page also documents frequency-measurement filtering, imported-format
saturation conventions, omission of small new islands and numerical island
resynchronization that can instantaneously change machine speed. These are
modelling choices, not physical evidence that an island synchronized. An
equivalence record must include them. [W60]

Zero-time-constant blocks can cease to be differential states and propagate inputs
algebraically. Fast selected models can use sub-interval integration with network
variables held fixed between full network solutions. Smaller internal state steps
do not imply equally frequent algebraic network updates or preserved fast
waveforms. This is a partitioned approximation whose adequacy needs a timestep
study for the quantities of interest. [W59]

Per-model sub-interval counts may be automatic or explicitly selected from the
documented discrete set. **Inference:** record requested and effective counts,
network step and output-sample interval separately. An export with fewer samples
cannot establish integration error, and a numerically stable trace alone cannot
establish waveform accuracy. [W173]

#### E. A controller's attachment and measurement direction are part of its model

The REPC_D detailed help attaches the plant controller to a bus, with separate
voltage/frequency buses, branch measurement terminals and incoming/outgoing-flow
flags. It distributes real/reactive commands to downstream generators and can
control switched shunts. Parameters include PI gains, measurement/filter times,
deadbands, output/rate limits, low/high-voltage freezing and MVA base. Auto-correction
can alter signs, swap limits or change small time constants. Merely importing its
parameter names does not prove the intended signals or limits were simulated.
No parameter table or block image is reproduced here. [W174]

**Naming conflict, not an alias assertion:** the July 7, 2023 patch calls the bus
controller REGC_D; the October 25, 2023 patch and detailed help call a bus controller
REPC_D. The latter explicitly documents attachment and fields. This closes the
bus-controller discovery gap but does not prove REGC_D and REPC_D are interchangeable
in all builds/files. Preserve the original token and require the exact build's
import/export evidence before making a translation rule. [W175][W176][W174]

#### F. Import/export is semantic translation, not just text parsing

Simulator documents differences in generator AVR treatment, reactive capability
files, shunt representation, transformer/star-bus representation, IDs, interchange
and DC groupings. An export can transform the model structure rather than preserve
every native record one-for-one. The vendor's comparison is scope/version evidence,
not a universal specification for all later RAW/EPC revisions. **Proposed import
ledger:** input format/build, original identifiers, created objects, transformed
fields, defaults, unsupported records and unresolved references. A round-trip test
must check physical behaviour and intentional losses, not byte equality alone.
[W11]

### 8.4 Independent mathematical references and complementary engines

These sources explain reproducible mathematics missing from feature lists. They
are not evidence that PowerWorld, ETAP or PowerFactory uses the named open engine.
They do not authorize dependency adoption. Versioned documentation should be pinned
again in a future implementation WP; mutable stable/latest pages are observations
of the accessed content.

#### A. Common AC branch stamp and its invariants

For series admittance `y`, total charging susceptance `b`, and a complex from-side
tap `t`, the independent MATPOWER branch formulation gives
`Yff=(y+j*b/2)/|t|^2`, `Yft=-y/conj(t)`,
`Ytf=-y/t`, `Ytt=y+j*b/2`.
Terminal currents are the two-port matrix times terminal voltages. This makes the
tap side, phase-shift sign, shunt splitting and pu base choices testable. With a
phase-shifting tap the matrix is not generally symmetric. In our proposed tests,
real terminal power loss must equal the resistive loss for a passive branch;
charging affects reactive power and should not create real loss. These are
mathematical invariants, not equipment acceptance limits. [W177]

The standard AC formulation solves active mismatch at non-reference buses and
reactive mismatch at PQ buses. MATPOWER also describes full Newton,
fast-decoupled and alternative coordinate/current-balance formulations. Its
reactive-limit outer loop uses fixed Q bounds and does not automatically enforce
the full trapezoidal capability curve. **Inference:** independently compare
Jacobian derivatives, power balance and controller transitions, not just rounded
voltage tables. Solver names alone do not establish limit-policy equivalence.
[W178]

#### B. Static loadability and event location

MATPOWER's continuation formulation augments network residuals with a transfer
parameter and a parameterization equation. Prediction and correction trace the
solution family rather than repeatedly relying on an ordinary solve with a
larger load. It is an independently documented candidate method; PowerWorld's
PV help did not establish this exact algorithm. [W179]

The continuation event mechanism locates zero crossings for a target transfer,
nose, generator limits, bus voltage or branch loading, using controlled step
refinement. A reactive-limit event can switch PV to PQ and change the continuation
problem. **Proposed result taxonomy:** physical limit reached, model/control event,
search bound, numerical nonconvergence and unresolved event bracket. The last
converged point is not automatically the collapse point. [W180]

#### C. Optimization problems must be stated before choosing a solver

The independent AC OPF formulation optimizes generation cost subject to nonlinear
real/reactive balances, limits at both branch ends and bounds on voltages,
generation and reference angles. It distinguishes apparent-power, real-power and
current flow constraints. These are different feasible sets; an MVA thermal
constraint cannot silently become MW. This formulation is not a guarantee of a
unique global optimum in a nonconvex AC network. [W181]

With DC network assumptions and suitable quadratic costs, voltage magnitudes and
reactive powers disappear and the problem becomes a quadratic program with linear
constraints. That is a different model, not merely a faster linear-algebra backend
for the same AC problem. [W182]

PowerWorld's documented primal-LP loop repeatedly linearizes around solved
operating points, introduces penalized feasibility variables, changes controls and
resolves the nonlinear flow. **Inference:** report both final nonlinear residuals
and remaining penalty/slack use. A successful LP subproblem is not sufficient
evidence of an acceptable final network point. [W54]

#### D. DAE initialization and integration alternatives

SUNDIALS IDA documents residual-form DAEs `F(t,y,ydot)=0`, consistent initial
conditions, variable-order BDF integration and Newton/Krylov or direct linear
solution. Its step Jacobian includes derivatives with respect to state and state
derivative. Absolute/relative error weights differ from a network MVA mismatch.
It is a candidate general numerical foundation, not an electrical machine library
or a chosen Quantic dependency. **Inference:** define differential/algebraic
variables and initialization residuals before picking an integrator. After a
discrete topology change, restoring algebraic consistency is separate from
integrating continuous states. [W183]

ANDES' versioned tutorial documents implicit trapezoidal TDS starting from a
converged flow and an initialized dynamic system. It also explains that dynamic
models take over linked static injections, so changing the disabled static
generator during TDS is not equivalent to changing a governor reference. This is
a useful independent workflow comparison, not proof of identical models or a
reason to import ANDES code. A later benchmark should inspect equilibrium drift,
event timing, state continuity and algebraic residuals separately. [W184]

#### E. Full-system modes are not the same as fitted signal modes

For a regular semi-explicit DAE, linearization gives
`M dx/dt = fx*x + fy*y`, `0 = gx*x + gy*y`.
If the algebraic block is invertible after reference/constraint handling, eliminate
`y` by solving with `gy` and obtain
`A = M^-1*(fx - fy*gy^-1*gx)`.
This is a Schur-complement identity, not a direction to form dense inverses.
Zero-mass states need algebraic treatment; a singular algebraic block cannot be
silently inverted. ANDES documents this class of formulation. [W185]

**Proposed interpretation:** eigenvalues describe the selected equilibrium and
model Jacobian. Fitted oscillations from recorded signals additionally depend on
observation channels, event/window choice and fitting. A SMIB result removes
inter-machine network interactions. Keep these as three different study types,
with distinct acceptance cases. PowerWorld's available evidence remains SMIB plus
signal fitting, not demonstrated full-grid eigenanalysis. [W63][W89][W185]

#### F. Phase-domain distribution and standardized faults

pandapower's public three-phase method uses Newton for positive sequence and
current injection for zero/negative sequences. The documentation marks several
options, including reactive-limit enforcement, as not tested with three-phase
flow. A balanced convergence test cannot establish their coverage. **Proposed
tests:** independent single-phase loading, transformer neutral/vector behaviour,
phase permutation and phase/sequence reconstruction. Preserve the method's
documented option limits in any adapter rather than copying its API as a promise.
[W186]

Its short-circuit documentation separates equivalent-source and prefault-
superposition methods, notes LU-based alternatives to full admittance inversion,
and lists three-phase, two-phase and single-line-to-ground support while excluding
the earthed two-phase fault on the accessed page. This is different from
PowerWorld's four named fault types. Source corrections and edition-specific
constants still need their owned standard/reference. Neither library's successful
execution is blanket standards certification. [W187]

#### G. State estimation is a measurement problem

pandapower documents WLS estimation using measured quantities, their standard
deviations, branch side and network connectivity. It distinguishes zero-injection
constraints, bus-switch fusion and bad-data tests, and warns that its bad-data
removal is not robust. A sufficient count of measurements does not itself prove
observability; the relevant measurement Jacobian must have suitable rank.
**Proposed tests:** deliberately unobservable placements, unit/sign/terminal
errors, redundant noisy measurements and interacting bad data. This is not a
PowerWorld-native estimator claim and not a certified SCADA pipeline. [W188]

#### H. Harmonics require frequency-specific network and source models

OpenDSS initializes harmonic sources from a solved operating point, solves selected
source frequencies and records monitors. Source phase/sequence behaviour and the
load's series/parallel shunt equivalent affect resonance damping. A frequency scan
and a harmonic injection study answer different questions. **Proposed tests:**
known linear RLC response, phase/sequence cases, source-angle changes, damping and
resonance-grid refinement. THD alone cannot explain whether a resonance peak was
missed. This independent frequency-domain engine is not proof of native general
harmonic/filter parity in PowerWorld. [W189]

#### I. Commitment and reliability need information absent from snapshot dispatch

PyPSA's versioned unit-commitment documentation uses binary operating status,
start/stop decisions, ramp constraints, minimum up/down times and pre-horizon
history. Those intertemporal constraints are not supplied by a set of independent
OPF snapshots or a reserve allocation. **Proposed tests:** horizon boundaries,
initial status, startup/shutdown ramps and deliberately infeasible schedules.
This is a reference for a separate future study, not evidence of PowerWorld unit
commitment. [W190]

EPRI's version 8.5 reduction note ties predictive reliability to radial EnergyMeter
zones and identifies reduction cases that discard losses or leave other objects
without references. **Inference:** reliability and reduction require explicit
assumptions and preservation checks. Neither a contingency count nor a collapsed
network is a reliability index without failure/repair/customer and restoration
modelling. This source does not establish a full meshed adequacy Monte Carlo
engine. [W195]

#### J. Code, bindings, cases and documentation have separate permissions

The current MATPOWER licence covers code under BSD-3 but explicitly excludes
bundled case files. Therefore a statement that a case is BSD merely because it
ships with MATPOWER is insufficient. Existing and future case provenance must
identify its own permission/terms; this observation does not decide the status of
any particular fixture. No data were downloaded or redistributed for this pass.
[W192]

ANDES' current licence is GPL-3.0-or-later. Under AGENTS.md it must not be imported
into Quantic packages. Its documented equations/methods were studied, not its
implementation copied. A separately executed comparison is a different integration
decision and still needs a scoped WP and distribution review. [W191]

SUNDIALS documents BSD-3 licensing for its packages. External sparse solvers,
bindings and optional integrations still need their own notices checked. Its
documented C implementation is independent evidence about SUNDIALS, not evidence
about any proprietary power-program language. [W193]

DSS-Python describes a custom OpenDSS-derived engine/API route on Windows, Linux
and macOS, while explicitly directing readers to the underlying DSS C-API licence
as well as its own BSD terms. API compatibility is not proof of bit-for-bit
numerical equivalence to EPRI COM. Pin engine, binding and build independently if
this route is later adopted. [W194]

### 8.5 Proposed verification ledger for our own implementation

This is an original research-derived test specification, not completed product
functionality. It intentionally tests invariants and transitions before large
commercial-style network examples. Engineering references, constants, tolerances,
input rights and the responsible WP must be approved before implementation.

| Test family | What must be controlled | Evidence required beyond a plausible picture |
| --- | --- | --- |
| Branch stamp | Tap side/phase, bases, shunts and status | Terminal-current identities and passive real-loss balance. [W177] |
| Newton Jacobian | Coordinates, injection signs and active equations | Analytical/independent derivative comparison; residual history. [W165][W178] |
| Reactive limits | AVR, capability, allocation policy and release logic | Per-generator bounds and controller transitions, not only total Q. [W167] |
| Remote control | Regulated terminal and participating devices | Equation/measurement mapping and correct response to a participant outage. [W166] |
| Plant droop | POI branch direction, deadband, smoothing and limits | Requested/effective curve and boundary/derivative checks. [W169][W170] |
| Topology | Ideal switches, retained devices and identity groups | Split/rejoin mapping and stale-result invalidation. [W171][W172] |
| DC sensitivities | Loss approximation, phase-shifter policy, source/sink | Perturbation check under the same assumptions; explicit islanding failure. [W34][W42][W43] |
| Contingency runs | Base state, make-up policy, RAS and controller options | Restore invariance, event/action ledger and terminal-specific violations. [W37][W40] |
| Continuation | Transfer direction, limits and parameterization | Event brackets, refinement history and distinct failure reasons. [W179][W180] |
| OPF/SCOPF | Objective, constraint units, penalty slack and contingency set | Final nonlinear feasibility and remaining violations, not LP status alone. [W54][W181] |
| Dynamic equilibrium | Static/dynamic ownership, initial limits and saturation | Initialization residuals and no-event drift before disturbances. [W60][W184] |
| Dynamic event | Timing, network/state steps and model substitutions | Before/after states, algebraic consistency and step-refinement error. [W59][W173][W183] |
| Small-signal modes | Reference, algebraic regularity and limit state | Reduced-model validity and independent perturbation/decay checks. [W185] |
| Unbalanced/fault study | Phases, neutral, sequence and fault definition | Independent phase/sequence results and unsupported-case diagnostics. [W186][W187] |
| Meter estimation | Measurement sides, units, covariance and observability | Residual/rank/bad-data assessment, not measurement count alone. [W188] |
| Harmonics | Frequency dependence, source phases and damping | Frequency refinement and primitive-network reference. [W189] |
| Interchange | Exact revision, object identity and translation policy | Loss/default ledger plus physical round-trip comparisons. [W11][W172] |
| Public benchmark use | Code licence versus case/archive terms | Per-dataset permission/provenance before redistribution. [W192] |

### 8.6 Arithmetic checks performed during this research pass

Five original dimensionless checks were run in scratch, outside the product code:
branch real-loss identity, complex-injection angle derivative, voltage-tolerance
endpoints/slope, scalar DAE elimination and second-order midpoint refinement.
Inputs were authored mathematical scenarios, not equipment defaults or vendor/book
case data. Results: branch identity error `3.730e-17`, central-difference derivative
error `1.760e-10`, endpoint/slope PASS, eliminated eigenvalue `-0.5`, and successive
midpoint error ratios `4.158771` and `4.077143` under step halving. The latter is
consistent with second-order convergence for that scalar equation only.

These checks support our algebraic transcription and proposed test families. They
do not validate a commercial solver, a production Quantic implementation, a power
equipment model or standards compliance. Future WPs still need committed original
fixtures, independent engineering references and justified engineering tolerances.

### 8.7 Cross-product checks that affect a faithful comparison

These checks support comparison of Simulator with ETAP and PowerFactory, not
replacement of Claude's owned dossiers or proof that one vendor uses another's
implementation. Each proposed test below is our inference from the cited evidence.

| Question | Public evidence and boundary | Proposed independent check |
| --- | --- | --- |
| What does a transient step mean? | Simulator documents explicit RK2 and selectable Euler; PowerFactory documents damping-factor endpoints of trapezoidal and backward Euler, with intermediate generalized-theta settings. Its FAQ does not establish a formula mapping the UI factor to a mathematical theta. ETAP's recovered tutorial exposes simulation and plot steps, but does not identify an integrator. [W60][W196][W197] | Compare fixed mathematical problems with declared method, internal step, output cadence and event alignment. Do not apply a universal step-size tolerance across these methods. |
| Why did oscillations decay? | PowerFactory distinguishes physical damping from numerical damping and discusses factor/step effects. Its example's printed oscillation-frequency expression is dimensionally suspect, so it is not an adopted reference equation. [W198] | Use authored lossless and damped systems, vary step and method independently, measure amplitude and phase error, and reject a match obtained only through extra numerical dissipation. |
| How are dynamics initialized? | PowerFactory initializes DSL signals from load-flow results, orders models by known/unknown signals and reports dependency deadlocks. Its FAQ describes Verify Initial Conditions as RMS-only. These statements are documented workflow, not a universal guarantee for every model or release. [W199] | Test missing setpoints, cycles, saturation and static/dynamic double counting. Record residuals and no-event drift, not simply a successful dialog dismissal. |
| Are events and samples the same object? | ETAP tutorial sections 7.7 and 7.8 distinguish frequency-scan/harmonic solves, selected plot elements, transient events with actions, machine-model selection and time-indexed result display. The printed screenshots are historical workflow evidence, not 2026 defaults. [W196] | Keep event time/action payload, numerical step, stored sample and display selection separate. Changing plot selection must not silently change the network being solved. |
| What does co-simulation demonstrate? | PowerFactory's public example separates sequential EMT, EMT-EMT and RMS-EMT cases, using ComInc for sequential initialization and ComCosim for co-simulation. We inspected the instructions, not an executed attachment or a documented coupling-error bound. [W200] | Compare monolithic versus partitioned authored networks, exchange cadence, event localization and energy/interface residuals before claiming equivalence. |
| Can identical physics produce different plotted traces? | The SMA/DIgSILENT report uses PowerFactory 2023 SP5 and PSCAD 5.0.2 with named model revisions. Sections 3.1.2 and 3.2.3 distinguish derived-meter dynamics from internal inverter signals; fault-ride-through retrigger timing can also magnify discrepancies. This is a specific model benchmark, not universal engine equivalence. [W202] | Compare raw electrical/internal signals before derived meters; align filtering, reference frame, window, frequency estimator and event state. A matching steady state does not validate a transient meter. |
| Which EMT quantity is being compared? | PowerFactory's current FAQ describes built-in current/voltage/power measurement devices providing instantaneous, true-RMS and sequence-phasor outputs with frequency tracking from 2022; the benchmark footnote mentions 2023. Preserve this source/version discrepancy rather than silently harmonizing it. [W201][W202] | Require quantity kind, phase/sequence, RMS/peak convention, frequency/reference angle, window and latency in the comparison record. |
| Does a common interface make engines interchangeable? | FMI 3.0.2 sections 1.2.1-1.2.3 distinguish external integration, co-simulation and scheduled partitions. Section 4.2.1 says Co-Simulation Step-Mode algebraic-loop iterations require restored state and repeated stepping; get/set alone is insufficient. Early return is capability-negotiated, section 4.1.3. [W203] | Declare supported interface/version/capabilities, rollback and event semantics. Our existing FMI-shaped lifecycle is not an FMI-conformance claim. |
| Is hosting capacity one universal number? | ETAP's dedicated page identifies nodal, stochastic and impact options, voltage/thermal constraints and smart-inverter functions. No public optimizer equations or universal constraint defaults were established here. A separate vendor announcement identifies patent 12244141; this dossier makes no patent-scope, permission or adoption decision. [W204][W205] | Define network state, DER location/type, uncertainty, operating policy and active constraints. Research of general power-flow-constrained methods is distinct from approval to implement a particular advertised method. |

An original scalar check explains why the integration distinction matters. For
`x' = lambda*x`, the independently defined theta rule
`x[n+1] = x[n] + h*((1-theta)*lambda*x[n] + theta*lambda*x[n+1])`
has amplification `R(z) = (1 + (1-theta)*z)/(1-theta*z)`, `z=h*lambda`.
For a purely imaginary `z`, theta `0.5` preserves amplitude in exact arithmetic,
whereas theta `1` damps it. This is our algebraic derivation, **not** a recovered
PowerFactory damping-factor mapping. It supports step/phase/amplitude tests, not
an engineering stability or proprietary-algorithm claim. [W197][W198]

Public PDF retrieval notes and limits are recorded in
`docs/sources/entries/power-cross-product-mechanisms-2026-10-16.yaml`.
The ETAP guide and SMA report were read only; no screenshots, vendor models,
parameter tables or worked cases were copied into this repository.

### 8.8 Lines, neutrals and grounding need study-specific reductions

This pass examines a failure mode in independent implementations: using one stored
impedance or one ground flag across studies whose electrical boundary conditions
differ. The proposed architecture and checks here are our inferences, not an added
implementation, equipment default or permission to copy a vendor model.

#### A. Preserve the input representation before calculating a line

TransLineCalc v2 separates conductor/tower records, geometry, bundle count,
temperature, frequency, distributed parameters, long-line equivalent parameters and
per-unit results. Its published historical equations use different effective radii
for inductance and capacitance, and assume distributed shunt conductance zero.
The manual exposes reverse lookup as a ranking of candidate conductors against
parameters. That does not establish unique identification of a physical conductor.
The 2013 database/editor details are historical, not a current backend claim.
[W209]

ETAP publicly advertises phase/sequence matrices, mutual coupling, transposition,
short/long-line models and multilayer soil within its line-constants module. This
is broader advertised input/model scope than a balanced scalar parameter
calculator; its detailed earth-return algorithm and solver accuracy are not
established by that page. [W214]

OpenDSS LineGeometry makes conductor positions, heights, units, phase count and
neutral treatment explicit. It references separate conductor/cable types and
allows neutrals to remain explicit or be reduced. [W210] Its historical revision
note says geometry supersedes earlier impedance definitions and parameters can be
recomputed when frequency changes. This motivates an import diagnostic for
representation precedence, rather than retaining inconsistent definitions silently.
[W212]

**Proposed record:** keep source data, matrix conductor order, temperature, frequency,
length units, soil/return assumptions and reduction history separate from the
derived network stamp. Diagram coordinates alone do not supply conductor geometry.
Derived caches should be keyed by these inputs, not just equipment name.

#### B. A long-line equivalent is not simple length multiplication

For uniform scalar distributed series impedance `z` and shunt admittance `y` per
unit length, the manual gives `gamma=sqrt(z*y)`, `Zc=sqrt(z/y)`,
`Zpi=Zc*sinh(gamma*l)`, and `Ypi=2*tanh(gamma*l/2)/Zc`.
`Ypi` is the total shunt admittance, split equally between ends of the equivalent
pi; the manual's repeated label "series admittance" is not adopted as circuit
semantics. The branch must not apply the total shunt at each end. [W209]

Our algebraic verification uses a two-port with a consistently directed through
current: `A=D=cosh(gamma*l)`, `B=Zpi`, `C=sinh(gamma*l)/Zc`. The reconstructed pi
must satisfy `A=1+Zpi*Ypi/2`, `C=Ypi*(1+Zpi*Ypi/4)` and `A*D-B*C=1`.
Two half-length two-ports must cascade to the full line. These identities test
signs, factors and units without copying a reference network.

**Implementation inference:** select consistent complex square-root branches;
handle small arguments using stable `sinh(q)/q` and `tanh(q/2)/(q/2)` limits.
Check both series and shunt short-line limits. A lossy distributed model with
zero distributed `G` need not yield zero real part of its exact equivalent shunt.
Balanced scalar formulas are not a substitute for a coupled multiphase model.

#### C. Eliminating a neutral has a boundary condition

OpenDSS LineCode describes neutral Kron elimination with zero neutral voltage at
both ends. It warns about reducing a base-frequency matrix before later
earth-return frequency adjustments; those adjustments also do not supply conductor
skin effect. A stored reduction therefore needs the boundary/frequency assumptions
that produced it. [W211]

For our block relation `dV=Z*I`, partition phase and neutral coordinates:
`dVp=Zpp*Ip+Zpn*In`, `dVn=Znp*Ip+Znn*In`. Under `dVn=0`, elimination gives
`Zred=Zpp-Zpn*solve(Znn,Znp)`. Merely deleting the neutral row and column instead
sets `In=0`, a different condition. Finite grounding impedances or a floating neutral
generally require the neutral/earth network to remain in the assembled problem.
Our matrix example checks this algebra, not a physical cable.

PowerFactory's four-wire FAQ distinguishes an explicit neutral from a three-wire
model whose zero-sequence impedance already includes a chosen return path. In the
explicit representation it says to remove the neutral's contribution from that
zero-sequence definition. Adding an explicit neutral to an already reduced return
model risks double counting. The FAQ attachment fetch failed, so no cable-specific
calculation or parameter values were adopted. [W213]

#### D. GIC is a resistive physical network, not DC power flow

PowerWorld's input guide requires shared substation grounds, winding connections,
DC coil resistances and autotransformer identity. It distinguishes measured data
from estimates; a zero shunt-resistance input is documented as an open GIC path,
not a physical zero-ohm earth bond. It also cautions that ground resistance cannot
be reliably estimated. An independent data model should distinguish missing,
estimated, blocked and explicit physical values instead of inheriting ambiguous
sentinels. [W206]

The NERC guide describes a resistive nodal network with induced sources and
ground connections. In its aggregate representation, three phase paths are
parallel: winding/line resistances become one third of per-phase values, while
the shared earth resistance does not. Aggregate branch currents and physical
neutral-to-earth current are distinct from per-phase winding current. This guide
is a historical method reference, not a current compliance determination. [W215]

Our independent incidence formulation fixes the sign convention first. Let each
row of `A` be `+1` at the branch's from node and `-1` at its to node; positive
source `e` drives current from-to. With `D=diag(1/r)` and earth conductance matrix
`Gg`, use `i=D*(A*u+e)` and KCL `A.T*i+Gg*u=0`. Therefore solve
`(A.T*D*A+Gg)*u=-A.T*D*e`, then recover signed branch and ground currents.
No explicit dense inverse is needed. This is our notation and derivation from
Kirchhoff's laws, not vendor source code.

For positive resistances, a conductive reference in every connected component
removes the constant-voltage nullspace. An ungrounded component needs explicit
reference/compatibility handling; do not hide singularity with an arbitrary tiny
ground. Circulating currents may still exist in source-driven floating loops,
so "no earth reference" does not universally mean "zero branch current".
This resistive model is not the susceptance/angle approximation called DC power
flow and is not an industrial battery DC fault solver. [W34]

#### E. Geography, field sampling and coupled effects have separate limits

PowerWorld's line-tap note explains why a tap with no ground path should preserve
series induced voltage and current when segments are combined consistently.
It also reports geographical/numerical effects in actual coordinate calculations.
[W207] Its benchmark note attributes a discrepancy with the historical NERC
example to spherical versus WGS84 earth modelling. Choose and record the same
geodesy before treating a result difference as solver error. [W216]

Our Cartesian uniform-field identity is `e=E.dot(displacement)`, additive across
segments. For a spatially varying field, use the path integral with specified
interpolation and quadrature; the value at one endpoint is insufficient. This is
a mathematical design inference, not a recovered Simulator interpolation rule.
The vendor's field-input help lists coarse/fine grids and north/east files but
contains uncertain wording for coarse-grid coordinates. That page is insufficient
to implement an exact compatible file reader without a verified schema/sample.
[W217]

PowerWorld documents GIC sensitivities to field and line inputs. For our fixed
linear resistive matrix, multiple source vectors can share a factorization; after
topology, resistance or grounding changes the matrix must be updated. This is an
optimization inference, not a claim about the vendor's sparse backend. [W208]
The AC coupling help separately models transformer reactive demand using
effective GIC and a stated model coefficient. A correct resistive solution alone
does not validate core saturation, harmonic spectra, temperature rise or device
tripping. Those need independent sourced models and coupled-study checks. [W68]

#### F. Original arithmetic evidence and follow-up tests

Authored normalized scratch checks, with no vendor/book parameter data, passed:

| Check | Result | What it establishes |
| --- | --- | --- |
| Aggregate network versus three equal phase paths | KCL PASS; source/dissipation residual `3.553e-15` | Correct shared-earth and factor-of-three algebra for this circuit |
| Add an ungrounded series tap | Current difference `8.882e-16` | This normalized topology reduction preserves the solution |
| Source-current sensitivity | Central-difference error `4.742e-12` against analytic derivative | Fixed-topology linear response, not transformer magnetic sensitivity |
| Floating two-node matrix | Rank one | Absolute voltage reference is missing |
| Neutral Schur elimination versus full matrix | Phase-drop residual `4.578e-16`; naive deletion differs by `6.758e-03` | The chosen algebraic boundary condition matters |
| Exact pi versus distributed two-port | Residual `1.682e-16` | Scalar two-port conversion consistency |
| Two half-lines versus full line | Residual `3.469e-18`; reciprocity PASS | Cascade identity in the authored normalized case |
| Uniform field segment sum and nonuniform counterexample | PASS | Endpoint-only spatial sampling is not generally sufficient |

These are algebra checks, not a validated physical engine or measured vendor
benchmark. Later implementation should commit original fixtures with provenance,
exercise explicit/floating/finite grounds, blockers and connection changes, compare
phase and sequence representations under matching assumptions, and test frequency,
temperature, unit and base conversions. The source/inspection record is
`docs/sources/entries/power-line-grounding-2026-10-16.yaml`.

## 9. Gaps, qualification ledger and parity handoff

### 9.1 Coverage and stopping rule

The review covers the public product/add-on descriptions, current major-version and
patch documentation, the named help topics in section 2, vendor training figures,
two utility-authored conference presentations, owned Glover17 text, individual
practitioner observations, university documents and Texas A&M dataset pages. It does not claim to have read every
page of the continually changing web-help tree or every historical release. Source
counts are not a substitute for closed capability questions. The 2026-10-16 pass
adds 31 primary sources on detailed controls/topology, independent mathematical
engines and licence boundaries, plus original verification requirements in
sections 8.3 to 8.6. A further ten sources support the cross-product comparison in
section 8.7. Twelve further sources deepen line/neutral/grounding mechanisms and
original arithmetic checks in section 8.8, bringing the ledger to 217 entries. This does not
claim that an unbounded web corpus is exhausted.

The following gaps name why this research cannot turn them into supported product
claims. An absent capability in this dossier means **unknown/no evidence**, unless a
source explicitly establishes a narrower limitation. It never silently means no.

### 9.2 Explicit unresolved questions

| Gap | Sources checked / observed boundary | Why unresolved; consequence |
| --- | --- | --- |
| Textbook numerical benchmarks | Glover17 map, section 8.1 | Thirty page images are now inspected; section 8.1 distinguishes verified legibility/local calculations from remaining prerequisite pages and full simulation reproduction. Supplied cases have not been cleared for redistribution. [W106] |
| Public-case archive fidelity/terms | Texas A&M publisher pages, section 8.2 | Availability and use permission established, archive files, bundled terms and dynamic-model compatibility not inspected. MATPOWER does not carry dynamics. [W150][W152][W158] |
| Generic benchmark-code licence versus data permission | MATPOWER upstream licence | Bundled case files are explicitly outside the code's BSD grant. Per-case terms remain necessary; do not infer clearance from the engine licence. [W192] |
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
| Exhaustive dynamic-model/default inventory | Named inventory, support screenshots and detailed model help | Bus-attached REPC_D now has primary schema evidence, but its relationship to release token REGC_D is unresolved. Exhaustive current/import-only flags still need actual-build export; PTIST3 remains a partial-feature example. [W92][W107][W108][W120][W174][W175][W176] |

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
