# Circuit/control peers and open tools

WP-2.27, ChatGPT, 2026-10-18. Lighter dossiers for Proteus, LTspice, PLECS,
PSIM, ngspice, Xcos and OpenModelica through shared sections. S is documented
subset, I our interpretation/proposal, U unresolved and never absent. No product,
model library, firmware or numerical case was installed, copied or executed.

## 1. Identity: versions, licences and platforms

| Product | Dated primary identity evidence | Entitlement/version boundary |
| --- | --- | --- |
| Proteus | Labcenter site advertises 9.2 and 64-bit v9 family [CP1] | Proprietary VSM/processor packages, advanced analysis and PCB functions must be distinguished. A free VSM Studio IDE is not a free simulation engine [CP2/CP3] |
| LTspice | Analog Devices describes free SPICE, schematic capture and waveform viewing [CP4] | Free price is not open source. Official support directs users to the installed EULA [CP5], which was not installed/read here; exact build/redistribution terms U |
| PLECS | Plexim Blockset for Simulink and independent Standalone, with separate Coder/RT Box routes [CP6]; manual 5.0 [CP30] | Proprietary licence/quote; target/platform/compiler and exact entitlements need selected product. Documentation version is not our tested binary |
| PSIM | Current Siemens Simcenter product and June 26, 2026 release article for 2026.1 [CP11/CP12] | Proprietary product. Older Altair help remains useful with date/version limits; exact packaging/licence route U |
| ngspice | Official manual 46, March 31, 2026 [CP14]; release news dates release 46 to March 29 [CP29] | Main source BSD with component exceptions; see dated audit below, not all-BSD shorthand. Current executable/build options untested |
| Xcos / Scilab | Scilab download advertises 2027.0.0 released October 15, 2026 [CP16]. Xcos help read is 2026.1.0 [CP18] | GPL-2.0 provider licence [CP17]; external process only. Do not infer new-version behavior from older help without a migration test |
| OpenModelica | Official indexed Windows page lists 1.27.1 [CP19]; current OMEdit source documentation read [CP20] | Source licence file now offers AGPL-3 or OSMC membership modes; runtime has separate alternatives [CP22/CP23]. Old web descriptions and generated-runtime terms do not license the whole compiler |

Exact binary hashes, local platform, optional libraries and commercial contracts
remain unverified for all seven. Open source and zero price answer different
questions. No recommended deployment stack is approved by this inventory.

## 2. Sources

All accessed 2026-10-18. Technical claims use primary vendor/project sources.
An indexed page or failed direct fetch is explicitly qualified.

| ID | Source and inspected scope |
| --- | --- |
| CP1 | Labcenter [Proteus simulation](https://www.labcenter.com/simulation/), current product/version, SPICE/MCU interaction and instruments |
| CP2 | Labcenter [Advanced Simulation](https://www.labcenter.com/advancedsim/), optional graph analyses and stimulus/probe workflow |
| CP3 | Labcenter [VSM Studio](https://www.labcenter.com/vsmstudio/), compiler/debug and schematic synchronization |
| CP4 | ADI [LTspice product](https://www.analog.com/en/resources/design-tools-and-calculators/LTspice-simulator.html), free simulator/capture/viewer; no downloaded binary |
| CP5 | ADI [installed EULA location](https://support.analog.com/en-US/knowledgebase/article/ka-16982), indexed official text only, direct fetch failed. Full exact installed terms unavailable |
| CP6 | Plexim [products](https://www.plexim.com/products), Standalone/Blockset/Coder/RT Box and licensing route |
| CP7 | Plexim [MOSFET model, 5.0](https://docs.plexim.com/plecs/5.0/components-by-category/mosfet/), ideal switch and optional on-resistance/thermal parameters |
| CP8 | Plexim [thermal simulation](https://www.plexim.com/products/plecs/thermal), loss/thermal treatment without detailed switching-waveform solve |
| CP9 | Plexim [code generation, 5.0](https://docs.plexim.com/plecs/5.0/codegeneration/), simulation/target/code boundary |
| CP10 | Plexim [Standalone workflow, 5.0](https://docs.plexim.com/plecs/5.0/using-plecs/using-plecs-standalone/), new model/save and Blockset schematic import |
| CP11 | Siemens [PSIM 2026.1 changes](https://blogs.sw.siemens.com/simcenter/simcenter-psim-2026-1/), 2026-06-26, nonlinear components/motor reference and FMU co-simulation import |
| CP12 | Siemens [Simcenter PSIM](https://www.siemens.com/en-us/products/simcenter/systems-simulation/psim/), power electronics, losses, control, code and verification product claims |
| CP13 | Altair [Twin Activate/PSIM co-simulation](https://help.altair.com/twinactivate/help/en_us/topics/math_solutions/psim_cosim_c.htm), link nodes, port order, model reload and schematic association, current help footer 2025 |
| CP14 | Project [ngspice 46 manual](https://ngspice.sourceforge.io/docs/ngspice-46-manual.pdf), cover/analysis contents and chapter 29.2-29.4 licence scope; no full 755-page read claimed |
| CP15 | Project [ngspice FAQ](https://ngspice.sourceforge.io/faq.html), dated 2018, Spice3/Cider/XSPICE origins, not current feature certification |
| CP16 | Scilab [download](https://www.scilab.org/download), 2027.0.0 release date/platform list/GPL notice |
| CP17 | Scilab [open-source licence](https://www.scilab.org/about/scilab-open-source-software), provider GPL-2.0 statement and toolbox explanation |
| CP18 | Scilab [Xcos 2026.1.0 help](https://help.scilab.org/docs/2026.1.0/en_US/xcos.html) and [Xcos product](https://www.scilab.org/software/xcos), hybrid block-model editing |
| CP19 | OpenModelica [Windows download](https://openmodelica.org/download/download-windows/), indexed official release 1.27.1; direct fetch timed out |
| CP20 | OpenModelica [OMEdit source docs](https://github.com/OpenModelica/OpenModelica/blob/master/doc/UsersGuide/source/omedit.rst), blob 252aaf8b7fb3b1f14c158c8b9fcf12b65f1d8d67, introductory editor/library/variables/messages sections read; no example copied |
| CP21 | Modelica Association [language specification 3.6](https://specification.modelica.org/maint/3.6/), 2023-03-09, abstract and equation/connection/unit/DAE organization; language is distinct from tool/library rights |
| CP22 | OpenModelica [OSMC-License.txt](https://github.com/OpenModelica/OpenModelica/blob/master/OSMC-License.txt), blob 1cf14a985ad18c92407ec89c95dd1dfd626a96e3, AGPL-3 / OSMC-PL 1.8 modes |
| CP23 | OpenModelica [runtime licence](https://github.com/OpenModelica/OpenModelica/blob/master/OSMC-Runtime-License.txt), blob 662f79d64f5461a0fee5f54fb8c39b0378cfd800, separate BSD-new/AGPL/OSMC alternatives for designated runtime files |
| CP24 | [python-control docs](https://python-control.readthedocs.io/en/latest/), 0.10.2 development documentation, response/interconnection/control analysis scope |
| CP25 | [python-control LICENSE](https://github.com/python-control/python-control/blob/main/LICENSE), fbfc42c670132862f4d6998add25451214023574, actual file read |
| CP26 | [SciPy LICENSE.txt](https://github.com/scipy/scipy/blob/main/LICENSE.txt), 1032aece8a8109d67f238de6865d8b08e750a8c0, actual main source licence read; no numerical API qualification |
| CP27 | [SymPy LICENSE](https://github.com/sympy/sympy/blob/master/LICENSE), 0744f229d697ca3ed1b1b257bfdb70e3eecf0b9e, main licence and notices inspected; no dependency addition |
| CP28 | [ngspice GitHub COPYING](https://github.com/ngspice/ngspice/blob/master/COPYING), e266da0141a06637b8119d8ce7e53318ab1eee12, explicitly historical ngspice 26/2014 material; not treated as current 46 licence proof |
| CP29 | Project [ngspice news](https://ngspice.sourceforge.io/news.html) and [documentation index](https://ngspice.sourceforge.io/docs.html), current release/manual distinction |
| CP30 | Plexim [PLECS 5.0 documentation](https://docs.plexim.com/plecs/5.0/), study/domain/manual organization; selected linked pages only |

## 3. Architecture and data model

| Product | Documented structure (S) | Interpretation / unresolved boundary |
| --- | --- | --- |
| Proteus | Schematic plus firmware assigned to supported MCU, with synchronised circuit/processor debugging [CP1/CP3] | I: firmware binary, processor variant/clock and external circuit must be separate run dependencies. No universal MCU/peripheral accuracy inferred |
| LTspice | Schematic capture, SPICE simulation and waveform viewer [CP4] | U: full current internal file schema, solver implementation and every vendor-model licence. A readable netlist is not a complete design-history format |
| PLECS | Electrical/control schematic, selectable editions, parameterised switches and thermal description [CP6/CP7/CP30] | I: switch law and loss model are distinct; finite-edge electromagnetic behavior requires another fidelity model |
| PSIM | Power/control schematic and motor-drive design; external link nodes in co-simulation [CP11-CP13] | I: pin port order, motor angle definitions and model versions. Code interpreted by C-block is a different capability from compiled embedded code |
| ngspice | Netlist/model/analysis organization, with mixed-signal origins [CP14/CP15] | I: preserve netlist dialect, model/includes and compiled options separately. A GUI is not the circuit solver |
| Xcos | Graphical block editor for hybrid dynamical models [CP18] | U: exact selected release's event ordering, solver coverage and model migration; old-help availability not current test evidence |
| OpenModelica | Modelica classes/connections and OMEdit library/variable/message views [CP20/CP21] | I: equation compilation, library version and run configuration are separate from diagram placement. Compiler/runtime/library grants differ |

## 4. Element catalogue and model fidelity

| Family | Sourced semantics | Independent input evidence still needed |
| --- | --- | --- |
| SPICE devices / sources | ngspice model/subcircuit/analysis structure [CP14]; LTspice analog circuit role [CP4] | Exact semiconductor law, model level, process/temperature units, instance/model distinction and lawful includes |
| MCU / peripherals | Proteus connects firmware execution with supported circuit/peripheral activity [CP1/CP3] | Exact architecture, executable/debug formats, timing and peripheral subset; do not substitute a generic board name |
| Switch / thermal model | PLECS MOSFET ideal switching with optional on-resistance, thermal parameters [CP7]; separate loss characterization [CP8] | I-V and switching-energy conditions, junction/case/heatsink definitions; Kelvin versus Celsius and thermal K/W units |
| Nonlinear passives / motor reference | PSIM 2026 models differential capacitance/inductance and separates rotor reference/initial angles [CP11] | Units and constitutive interpretation; a differential curve is not an arbitrary static multiplier |
| Signal control blocks | Xcos hybrid models [CP18], python-control state/transfer/interconnection operations [CP24] | Timebase, state, direct feedthrough, update clock, delay and saturation/reset semantics |
| Acausal multiphysics | Modelica differential/algebraic/discrete equations with connections and unit language [CP21] | Selected library/component equations, initial conditions and physical reference nodes; syntax support not numerical equivalence |

No device default or time-step tolerance is adopted. Displayed symbol and model
name do not establish identical equations or validity range (I).

## 5. Shared study/capability table

Each cell starts S or U. S supports only the named subset; U means not established
in this pass. The [Simulink dossier](simulink.md) records that product separately.

| Capability | Proteus | LTspice | PLECS | PSIM | ngspice | Xcos | OpenModelica |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Circuit/signal model entry | S schematic [CP1] | S schematic [CP4] | S schematic [CP6] | S schematic [CP13] | S netlist [CP14] | S blocks [CP18] | S classes/connections [CP20] |
| Transient analysis | S analog/digital/mixed [CP2] | S analog simulation [CP4]; exact menu U | S switching system [CP6] | S power/control [CP12] | S transient [CP14] | S hybrid dynamics [CP18] | S simulation [CP20]; exact solver U |
| DC/AC/noise/sweeps | S optional analyses [CP2] | U exact selected modes not traced | U complete modes not traced | U complete modes not traced | S named analysis families [CP14] | U complete modes not traced | U complete modes not traced |
| Firmware/circuit co-debug | S supported MCU/IDE [CP1,CP3] | U not traced | U MCU emulator not traced | U MCU emulator not traced | U MCU emulator not traced | U MCU emulator not traced | U MCU emulator not traced |
| Power-converter modeling | S SPICE circuit scope [CP1]; specialised solver U | S analog scope [CP4]; fidelity U | S power systems [CP6,CP7] | S specialised design [CP12] | S circuit scope [CP14]; chosen models U | U selected libraries not traced | S multidomain language [CP21]; libraries U |
| Device/thermal loss | U full loss method not traced | U full loss method not traced | S separate thermal model [CP8] | S conduction/switching/core [CP12] | U selected thermal model not traced | U selected thermal model not traced | U selected thermal library not traced |
| Motor/control system | U full drive libraries not traced | U full drive libraries not traced | S drive/control role [CP6] | S motor templates [CP11,CP12] | U complete system not traced | S hybrid blocks [CP18]; libraries U | S multidomain/OMEdit [CP20,CP21]; library validation U |
| Waveforms / measurement | S scope/probes [CP1,CP2] | S waveform viewer [CP4] | S scope route [CP6] | S co-sim/SimView [CP13] | S analysis outputs [CP14] | U viewer depth not traced | S variable plotting [CP20] |
| Embedded code / HIL | U not established by firmware import | U not traced | S Coder/RT Box [CP6,CP9] | S control C generation [CP12] | U target generation not traced | U target qualification not traced | U target qualification not traced |
| External co-simulation | S MCU/circuit [CP1]; FMI U | U FMI not traced | S Simulink Blockset [CP6]; FMI U | S 2026.1 FMU CS import [CP11], link nodes [CP13] | U external protocol not qualified | U external protocol not qualified | U current FMI modes not fully read |
| Custom behaviour | S firmware/IDE [CP3], EasyHDL [CP2] | U full extension terms not traced | U full extension ABI not traced | S interpreted C-block [CP12] | S code-model origins [CP15]; current ABI U | S hybrid model editing [CP18]; external ABI U | S user classes [CP20,CP21] |
| Open core reuse | U proprietary core | U free price only [CP4] | U proprietary core | U proprietary core | S component-qualified [CP14] | S GPL-2 provider [CP17] | S qualified AGPL/OSMC [CP22] |

Do not rank accuracy by feature count. A fast ideal-switch/loss-table calculation
and a detailed semiconductor transient answer different questions (I, CP7/CP8).
PSIM 2026.1's FMU co-simulation import does not establish every FMI version or
Model Exchange export capability (S boundary, CP11).

## 6. Workflow, reports, automation and exchange

Proteus: draw/connect, attach supported compiled/debug firmware, place stimuli
and probes, run/debug and inspect traces. Advanced Simulation is an additional
graph-analysis option [CP2/CP3]. Its schematic/debug synchronization is useful
for embedded interactions; production PCB/hardware correctness still needs its
own validation (I).

LTspice: schematic and waveform viewing are documented [CP4]. Complete current
batch syntax, file/model compatibility and raw-waveform exchange remain U here;
no claim of being an open or unrestricted redistributable engine. The installed
EULA is a named access gate [CP5].

PLECS: Standalone creates a model with save/autosave workflow and imports Blockset
schematics [CP10]. Coder/RT Box or Blockset/Simulink dependencies are separate
deployment configurations [CP6/CP9]. Round-trip model preservation and target
timing remain untested.

PSIM/Twin Activate: link nodes define exchanged signals; documented setup specifies
their order and reloads interfaces after model changes [CP13]. Current FMU import
is a different co-simulation route [CP11]. Communication step, interpolation,
events and stability require tests; port names alone are insufficient (I).

ngspice: netlist, analysis and commands form the primary simulation route [CP14].
Xcos offers a graphical hybrid-model environment [CP18]. OMEdit provides library,
documentation, variable and message browsers plus simulation and plotting [CP20].
For independent adapters (I), retain model hashes, included resources, version,
solver/options, time/unit conventions, exit status and diagnostics before importing
waveforms. No netlist or imported command was executed in this WP.

## 7. User value and complaints

No representative user survey, comparative benchmark or support-quality dataset
was read. Inferred value (I): Proteus joins firmware/circuit inspection; LTspice
lowers entry cost; PLECS/PSIM focus converter/drive workflows; ngspice exposes a
documented circuit engine; Xcos/OpenModelica expose editable models [CP1/CP3/CP4/
CP6/CP12/CP14/CP18/CP20]. These are our assessments, not measured user sentiment.

Documented boundaries worth surfacing to users: optional Proteus advanced analysis
[CP2]; ideal-switch versus thermal waveform assumptions [CP7/CP8]; PSIM's revised
rotor-angle definitions and FMU addition [CP11]; older Xcos help versus a new release
[CP16/CP18]; model/compiler/runtime licences that differ [CP22/CP23]. Performance,
bug prevalence and industrial accuracy remain U. Vendor adjectives about speed or
convergence are not independent validation results.

## 8. Engines, open licences and owned references

The independent split is I: typed schematic/signal/physical model; equation or
netlist generation; DC/nonlinear operating point; time integration/event scheduler;
small-signal and frequency analysis; device/model library; firmware/peripheral
coordinator; thermal/loss calculation; control algebra/analysis; waveform and
provenance; optional code/FMI interfaces. Each needs its own validated scope.

### Dated licence audit, 2026-10-18

| Candidate | Actual evidence / findings | Boundary before adoption |
| --- | --- | --- |
| ngspice | CP14 chapter 29 documents modified BSD with tclspice/numparam LGPLv2 and XSPICE public-domain exceptions. CP28's actual COPYING read is historical v26, not current v46 proof | Qualify selected release/source/build options and all component files. Manual and engine grants differ; subprocess candidate, not approved package import |
| Xcos/Scilab | CP16/CP17 provider GPL-2.0 notice read; exact release archive/component files not downloaded | External process only; toolbox, compiler and library terms separately checked. Provider toolbox explanation does not override repository GPL policy |
| OpenModelica compiler | Actual CP22 offers AGPL-3 or OSMC-PL 1.8 membership modes, not a simple permissive/GPL-only grant | Treat as external-process candidate pending exact-release, selected mode and service/distribution review. A process boundary alone is not a full AGPL hosting assessment |
| OpenModelica runtime | Actual CP23 offers BSD-new/AGPL/OSMC alternatives for files marked as runtime | Does not license the compiler/editor/model libraries. Generated artifacts still need component/library-rights review |
| python-control | Actual CP25 BSD-3-Clause | Control analysis candidate; optional dependencies and supported functions require separate qualification |
| SciPy | Actual CP26 BSD-3-Clause source licence | Numerical primitives candidate, not a general DAE/event/compiler implementation. Exact binary bundled libraries not audited |
| SymPy | Actual CP27 main BSD-3 with additional contributor/component notices | Symbolic algebra candidate; not a complete physical-network or simulator code generator. Retain component notices |

The three proprietary peers and free-price LTspice have no open-core reuse grant
established. Vendor examples, semiconductor/thermal models and firmware can have
different rights from the executable or language specification. No library import,
redistribution or commercial contract was approved here.

Owned-book leads from [existing inventory](../power/notes/engines-library-map.md):
Pillage 1995/Najm 2010/Vlach 1983 for circuit solution; Astrom/Murray 2008 for
control; Mohan 1995/Rashid 2014/Bose 2002 for converters/drives. Page-level
verification remains future work, not a copied derivation or current software
specification. Exact device coefficients and safety/EMC limits require their own
readable sources.

Original fixture proposals (I, all unrun): analytic RC/RLC and diode operating
points; a known switching instant between display samples; equal averaged energy
but different ripple in averaged/switched models; sampled control with explicit
hold/delay; known thermal RC energy balance; original firmware toggling a supported
pin with a declared clock; port-order and FMI-time mismatches; denied model-library
grant. Keep independent equations/measurements and justified tolerances.

## 9. Gaps and closure routes

| Gap | Closure needed |
| --- | --- |
| CG1 | Exact installed build/licence/platform/compiler and optional module of each proprietary product; none executed |
| CG2 | Current LTspice EULA and model redistribution terms from a lawful installed/authorised copy; generic ADI terms are not silently substituted |
| CG3 | Exact ngspice 46 source-component audit; historical GitHub COPYING not current proof; optional libraries/build settings unverified |
| CG4 | OpenModelica release-specific compiler/runtime/model library terms, membership mode and hosting obligations; current default-branch files differ from older web shorthand |
| CG5 | Scilab 2027.0 versus Xcos 2026.1 help, exact solvers/events/extensions and third-party components |
| CG6 | Current FMI versions/modes/ABI/clock handling and model exchange loss for each tool, including PSIM 2026.1 CS import; no execution |
| CG7 | MCU/peripheral timing, firmware formats, device/thermal parameters and semiconductor-model applicability/rights |
| CG8 | Independent benchmarks, original coupled fixtures, HIL timing and measured device/plant validation; no accuracy or speed ranking |
| CG9 | Owned-reference page verification and current standards before engineering constants; no copied vendor/book cases |

Public-source access gaps are recorded explicitly. No unsigned quote, public
download button or successful syntax parse is treated as licence or numerical
qualification. Building remains parked.
