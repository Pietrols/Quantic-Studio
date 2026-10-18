# PLC products and comparison with qe_plc

WP-2.28, ChatGPT, accessed 2026-10-18. S = documented, I = our inference or
proposal, U = unresolved. No vendor application, runtime, program or fieldbus
was executed. Current web documentation is not evidence of a tested release.

## 1. Identity and licensing

| Product | Documented identity and boundary | Licence/access finding |
| --- | --- | --- |
| Siemens | S: STEP 7 Basic and Professional in TIA Portal are distinct; Basic catalogue currently describes V21, while PLCSIM Advanced is a separate simulation product. Its developer page names S7-1500 and ET 200SP families, not universal Siemens CPU coverage. A1-A4 | S: commercial product/upgrade and trial offers; WinCC Unified engineering/runtime simulation has a separately advertised trial. U: exact purchased bundle, installed EULA, supported firmware and current Advanced manual. A1-A4,A7 |
| Rockwell | S: Studio 5000 Logix Designer help 38.01/38.03; legacy Logix Emulate and FactoryTalk Logix Echo are distinct. Help says versions 37 onward do not support emulated 5560/5570. A8-A12 | S: Emulate has commercial/operator-training activation described by its guide; no price or entitlement inferred for Echo/Designer/HMI. U: exact purchased edition, activation and protected-content rights. A9,A12,A14 |
| CODESYS | S: Development System 3 store currently lists 3.5.22.30; simulation runs in the development environment and is not physical I/O. A15-A18 | S: IDE use is free under EULA; runtime systems and add-ons have separate licensing. Free is not open source. A15,A16 |
| OpenPLC | S: current v4 runtime is headless, paired with Editor v4; do not carry v3 web-UI descriptions into v4. Runtime README describes editor-side STruC++ generation, native compilation and dynamic program loading. A20 | S: runtime main LICENSE is MIT; Editor main LICENSE is GPLv3. Different components, not one blanket licence. Exact release, dependencies, compiler and generated-code terms remain U. A21,A22 |
| Beremiz | S: IDE/CLI, Python reference runtime and C++ target runtime are distinct; no release pin inferred from master. A23 | S: README says IDE GPLv2-or-later, Python runtime LGPL and C++ runtime GPLv3-or-later. Actual files are GPL2, LGPL2.1 and GPL3 respectively. Website's shorter runtime description must not erase the C++ distinction. A23-A27 |

## 2. Primary source index

All accessed 2026-10-18. Indexed snippets are explicitly weaker than full pages.
Git blob IDs pin the content read, not a packaged release or dependency audit.

| ID | Primary source and URL | Read scope |
| --- | --- | --- |
| A1 | [Siemens STEP 7 Basic catalogue](https://sieportal.siemens.com/en-us/products-services/10314828) | Indexed V21 product, Basic/Professional upgrade boundary |
| A2 | [Siemens STEP 7 Professional catalogue](https://sieportal.siemens.com/en-th/products-services/10348750) | Indexed language/GRAPH catalogue |
| A3 | [Siemens controller selection](https://www.siemens.com/en-us/products/simatic/controller-configurator/) | Indexed CPU-dependent languages |
| A4 | [PLCSIM Advanced developer overview](https://developer.siemens.com/s7-plcsim-advanced/overview.html) | Full feature, family, API/co-simulation sections |
| A5 | [S7-1500 cyclic OBs, V21 help](https://docs.tia.siemens.cloud/r/en-us/v21/functional-description-of-s7-1500-cpus-s7-1500/organization-blocks-s7-1500/description-of-all-types-of-organization-blocks-s7-1500/cyclic-obs-s7-1500) | Indexed process-image ordering |
| A6 | [Process image overview, S7-1500/ET 200MP collection 20](https://docs.tia.siemens.cloud/r/simatic_s7_1500_et_200mp_manual_collection_enus_20/basic-information/automation-system/configuring/configuring-the-cpu/process-images-and-process-image-partitions/process-image-overview) | Indexed PIP0/OB1 and output update |
| A7 | [WinCC Unified product](https://www.siemens.com/en-us/products/simatic-wincc/unified/) | Indexed engineering and runtime simulation trial |
| A8 | [Create a routine, Logix Designer 38.00](https://www.rockwellautomation.com/en-us/docs/studio-5000-logix-designer/38-00/contents-ditamap/studio-5000-logix-designer/navigating-the-application/-product_name_rsl5k--application-main-window/create-a-routine.html) | Indexed four language choices |
| A9 | [Emulated controller differences, 38.01](https://www.rockwellautomation.com/en-us/docs/studio-5000-logix-designer/38-01/contents-ditamap/studio-5000-logix-designer/emulated-controller/emulated-controller-differences.html) | Full Echo differences, families and limitations |
| A10 | [Tasks, 37.01](https://www.rockwellautomation.com/en-pl/docs/studio-5000-logix-designer/37-01/contents-ditamap/studio-5000-logix-designer/tasks--programs--and-routines/tasks.html) | Full scheduling, priority, I/O and watchdog sections |
| A11 | [Timer and counter instructions, 38.01](https://www.rockwellautomation.com/en-us/docs/studio-5000-logix-designer/38-01/contents-ditamap/instruction-set/timer-and-counter-instructions.html) | Full language-specific instruction table and time base |
| A12 | [Logix Emulate product](https://www.rockwellautomation.com/en-pl/products/software/factorytalk/designsuite/studio-5000/studio-5000-logix-emulate.html) | Indexed simulation and commercial consultation scope |
| A13 | [Studio 5000 family](https://www.rockwellautomation.com/en-ca/products/software/factorytalk/designsuite/studio-5000.html) | Indexed View Designer/PanelView 5000 distinction |
| A14 | [Logix Emulate Getting Results, LGEM5K-GR016M](https://literature.rockwellautomation.com/idc/groups/literature/documents/gr/lgem5k-gr016_-en-p.pdf) | Indexed OTS activation; historical guide, not latest release qualification |
| A15 | [CODESYS Development System store](https://store.codesys.com/en/codesys.html?___store=en) | Version, zero-price listing and EULA context |
| A16 | [CODESYS licensing](https://www.codesys.com/ecosystem/discover-codesys/licensing/) | IDE versus runtime/add-on licensing |
| A17 | [CODESYS simulation command](https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_cmd_simulation.html) | Full simulation/physical-target difference table |
| A18 | [CODESYS task object](https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_f_reference_task.html) | Full task types, jitter, priorities, watchdog and program order |
| A19 | [Standard library TON](https://content.helpme-codesys.com/en/libs/Standard/Current/Timer/TON.html) | Full interface, input-edge, Q and ET descriptions |
| A20 | [OpenPLC v4 runtime README](https://github.com/Autonomy-Logic/openplc-runtime/blob/main/README.md) | Full architecture/workflow; blob 8cd6a21f23306f2d61c5a526584c1a8dce6e9f1f |
| A21 | [OpenPLC runtime LICENSE](https://github.com/Autonomy-Logic/openplc-runtime/blob/main/LICENSE) | Actual MIT file, blob 5beb2fa4269744ddf18d710abfe49f319c826e08 |
| A22 | [OpenPLC Editor LICENSE](https://github.com/Autonomy-Logic/openplc-editor/blob/main/LICENSE) | Actual GPL3 file, blob f288702d2fa16d3cdf0035b15a9fcbc552cd88e7 |
| A23 | [Beremiz README](https://github.com/beremiz/beremiz/blob/master/README.md) | Full component licence statements, blob 1611cc90851927a0a347bb694b4f619cc91f66d8 |
| A24 | [Beremiz IDE licence](https://github.com/beremiz/beremiz/blob/master/COPYING_for_IDE) | Actual GPL2, blob d159169d1050894d3ea3b98e1c965c4058208fe1 |
| A25 | [Beremiz Python runtime licence](https://github.com/beremiz/beremiz/blob/master/COPYING_for_Python_Runtime) | Actual LGPL2.1, blob 4362b49151d7b34ef83b3067a8f9c9f877d72a0e |
| A26 | [Beremiz C++ runtime licence](https://github.com/beremiz/beremiz/blob/master/COPYING_for_C_Runtime) | Actual GPL3, blob 94a9ed024d3859793618152ea559a168bbcbb5e2 |
| A27 | [Beremiz getting started](https://beremiz.org/getting-started) | Full project, language, build, runtime, debug and SVGHMI workflow |
| A28 | [Siemens Sentinel reference](https://references.siemens.com/de/reference/sentinel) | Search index names Zambia, drives and PCS7; direct page returned language shell, so historical lead only |
| A29 | [KCM official site](https://kcm.co.zm/) | Indexed Copperbelt operation identity; no PLC/SCADA inventory |

## 3. Architecture and data model

S: Siemens organizes controller execution around organization blocks and process
images; PIP0 is automatically associated with OB1. That is a CPU-specific mechanism,
not a generic claim that every PLC samples every channel once at scan entry. A5,A6.
S: Logix tasks schedule ordered programs; continuous, periodic and event scheduling
can preempt one another. Its documented platform differences include an I/O task
for the CompactLogix scope of the 37.01 page. A10. S: CODESYS task configuration
supplies priority, cyclic/event/external/freewheeling/status modes, ordered program
calls and target-dependent watchdogs. A18.

S: OpenPLC v4 splits REST/debug management from a native runtime, with editor-side
generation and runtime-side compilation/loading. Its README claims deterministic
scan cycles and real-time scheduling; those are provider descriptions, not our
measured jitter or deadline guarantee. A20. S: Beremiz project resources specify
tasks and POUs; MatIEC generates C before native compilation, and runtime selection
is separate from the IDE. Projects use PLCopen TC6 XML. A27.

I: our data model should preserve resource/task/program/block-instance identity,
I/O sampling policy, execution and output-commit times, initialization and retained
state as separate fields. Existing contracts remain untouched; this is a proposal
from the documented differences A5,A10,A18,A20,A27.

## 4. Languages, elements and timer semantics

| Product | S: documented language/element boundary | Evidence limit |
| --- | --- | --- |
| Siemens | Basic catalogue lists LAD, FBD and SCL; selection guide differentiates CPUs with STL/GRAPH support. A1-A3 | U: per-CPU instruction set, IEC edition/conformance, IEC versus legacy timer details |
| Rockwell | Routine choices include LD, FBD, ST and SFC. Timer table distinguishes LD TON/TOF/RTO/CTU/CTD/RES from FBD/ST TONR/TOFR/RTOR/CTUD, with millisecond base in that help version. A8,A11 | Similar names do not imply matching instance members, enables, reset, prescan or counter saturation |
| CODESYS | Store describes IEC language editors; Standard TON accepts IN/PT and exposes Q/ET. Falling IN resets, Q requires IN and elapsed PT. A15,A19 | U: changing PT, conditional omission, repeated calls, restart and target clock behaviour |
| OpenPLC | Runtime README names LD, FBD, ST and other IEC languages through Editor v4. A20 | U: exact supported subset and v4 compiler/library corner cases; do not infer from v3 |
| Beremiz | Getting-started describes five IEC languages, mixed-language POUs and native compile chain. A27 | U: edition conformance, compiler/library version and exact timer/counter traces |

## 5. Simulation, HMI and SCADA

S: PLCSIM Advanced offers an API for simulated PLC instances and plant co-simulation;
its overview also describes communication and WinCC visualizations. That does not
establish firmware-perfect cycle duration or licence bundling. A4. S: Echo retains
supported family project properties without controller-type substitution, but most
configured I/O modules fault; produced/consumed tags between emulated controllers
are a documented exception. Protected-content and network limitations apply. A9.
S: View Designer targets PanelView 5000; it is a separate HMI design environment,
not evidence that a PLC emulator includes SCADA. A13.

S: CODESYS simulation does not evaluate I/O configuration or fieldbus stacks and
does not send bus telegrams. External implementations may require substitute IEC
code; a successful simulation can omit hardware-dependent behaviour. A17. Its
runtime/add-on licensing must be checked separately for visualization. A16.
S: Beremiz documents SVGHMI, variable monitoring/forcing and communication
extensions; no alarm historian or enterprise SCADA parity inferred. A27. U:
OpenPLC v4 HMI/SCADA package and licensing, since the read runtime README documents
headless management/debugging rather than a complete supervisory application. A20.

## 6. Workflow and exchange

S: Siemens API workflow transfers a STEP 7 program into a simulated instance and
couples a machine model. A4. S: Logix uses controller-specific projects and routines;
Echo compatibility is family-specific. A8,A9. S: CODESYS allows simulation in the
engineering environment, subject to external-code and I/O limitations. A17.
S: OpenPLC v4 builds in Editor, uploads a package, compiles in runtime, controls
execution and monitors variables over its debug interface. A20. S: Beremiz separates
build, transfer and run, supports CLI operation, and exposes project XML. A27.

I: import/export must report unsupported instructions, types, task timing and
retention explicitly; text syntax or PLCopen XML alone cannot establish semantic
round trips. Proposed application of [exchange research](../power/import-formats.md),
subject to that file's format and rights gaps.

## 7. User value and Copperbelt adoption

I: priority for a mining engineer is inspectable interlock behaviour, timer/event
ordering and readable traces, followed by documented device and SCADA boundaries.
This is our assessment, not surveyed customer demand or a measured adoption rate.
No independent complaint study was performed; product claims in A4,A12,A16 are
provider descriptions, not customer testimonials.

U: a current, verified installed base at Mufulira, Kitwe, Ndola, Chingola or
Chililabombwe was not established. A29 confirms KCM's Copperbelt identity but no
controller models. A28 is a historical indexed Sentinel PCS7/drive lead in Zambia;
the direct page was inaccessible beyond its language shell. It does not establish
a Copperbelt Province installation, a TIA Portal project, or current firmware.
Global Rockwell mine case studies are not evidence of Zambian adoption.

I: close this gap with an authorized, dated plant/subsystem inventory: CPU order
code/firmware, IDE version, I/O/fieldbus, HMI/runtime, SCADA/DCS and migration status.
Do not obtain client programs or configuration files for the public repository.

## 8. Current qe_plc findings and implied engines

Local file paths below are relative to `packages/py/qe_plc/` unless stated.
These are static findings at main fb58ccf, not new executed tests or code changes.

| Finding | Actual implementation evidence | Documented comparison / implication |
| --- | --- | --- |
| AF1 Language subset | `src/qe_plc/lexer.py` KEYWORDS/UNSUPPORTED; `parser.py` ELEMENTARY and statements | BOOL/INT/REAL/TIME, assignments, IF and six built-in blocks only. No LD/FBD/SFC, loops, arrays, user FBs or full vendor dialect. A1-A3,A8,A15,A20,A27; preserve `quantic-st-0.1` identity |
| AF2 One ideal cyclic task | `scan.py` ScanEngine.scan; `study.py` LIMITATIONS | Fixed whole-ms increments, no preemption, jitter, event task or watchdog model. Contrast A10,A18; simulated logical time is not target execution time |
| AF3 I/O order and scope | `scan.py` scan captures inputs then statements then output_image; `study.py` run_scan_study labels start/commit | Study commits at next boundary; S7-1500 documents output transfer before input refresh/cyclic execution, and Logix has platform-specific I/O scheduling. A5,A6,A10. Need explicit boundary mapping before trace comparison |
| AF4 Public study versus low-level API | `study.py` LIMITATIONS and validation; `scan.py` run_program event type checks | Public study says digital I/O only; internal typed variables and low-level event API also handle numeric types. Do not advertise analog field channels from numeric parser support |
| AF5 TON | `blocks.py` TON.call uses elapsed now-start, caps ET at PT and resets on false; `scan.py` run_statements | Broad on-delay/reset shape agrees with A19, but whole-ms evaluation and untested vendor corner cases prevent parity claim |
| AF6 Skipped/repeated calls | `scan.py` run_statements calls only selected IF branch; each call uses same time_ms; `blocks.py` Timer | State remains untouched when skipped; later active call uses elapsed timestamp. Multiple calls in one scan mutate the same instance at the same timestamp. U: vendor-equivalent conditional/repeated-call behaviour; requires exact manuals and fixture traces |
| AF7 Omitted arguments | `parser.py` call/_Checker only validates supplied names; `blocks.py` call defaults | Missing inputs use Python call defaults each invocation; they do not retain prior supplied argument values automatically. Vendor omission semantics not qualified. Do not silently translate calls |
| AF8 Counter policy | `blocks.py` CTU/CTD/CTUD; `tests/test_function_blocks.py` handwritten expectations | CTU stops at PV; CTD stops at zero; CTUD reset/load/edge priority and bounds are declared subset choices. A11 language-specific Logix instructions are not substitutes |
| AF9 Restart/retention | `scan.py` constructor initializes values/blocks; lexer rejects RETAIN | No warm/cold restart or persisted memory model. Library and controller-specific restart evidence remains U |
| AF10 Numeric behaviour | `scan.py` _real/_int/_time and value; `lexer.py` TIME range | Binary32 assignment, bounded INT/TIME and explicit faults are local policies; do not generalize to every vendor type/overflow mode |
| AF11 Plant coupling | `process.py` MotorStarter.advance; `study.py` process.advance after output image | Authored discrete coil/overload/feedback table with one-scan feedback lag. No contactor delay, motor dynamics or safety qualification; not PLCSIM/Echo device fidelity. A4,A9 |
| AF12 Existing evidence | `tests/test_function_blocks.py`, `test_language_and_scan.py`, `test_scan_study.py`; `docs/specs/structured-text-subset.md` | Handwritten local traces and named subset choices exist; vendor differential runs, IEC certification and target deadline testing do not follow from them |

I: architecture candidates are a dialect parser/type checker, explicit task and
I/O scheduler, versioned instruction libraries, restart/state manager, deterministic
event/trace engine, plant coupling and an HMI/SCADA interface. Derivation: AF1-AF12.
Keep current authored qe_plc isolated from optional external validation runtimes.
OpenPLC's MIT runtime is a candidate only after dependency/generated-code audit;
its GPL Editor and Beremiz GPL components are process-only under repository rules.
A20-A26. No package dependency or contract changes here.

## 9. Gaps and original fixture proposals

| ID | Missing evidence / proposed closure |
| --- | --- |
| AG1 | Current PLCSIM Advanced manual URLs 109989787 and 109997788 returned 403. Obtain public readable exact version/CPU support, timing and timer instruction documentation; no substitute hardware timing claim |
| AG2 | Exact Rockwell Designer/Emulate/Echo edition, activation and controller/firmware matrix; historical OTS guide is insufficient for a current purchase or runtime test |
| AG3 | IEC 61131-3 edition-specific language/library requirements are not fully read. Obtain the exact edition before a conformance claim; free vendor help only documents selected products |
| AG4 | OpenPLC v4 release and dependency/compiler/generated-program licences; Editor GPL/runtime MIT distinction alone does not clear a complete integration |
| AG5 | Beremiz exact IDE/Python/C++ release, MatIEC and extension licences, generated-code rights and repeatable timing; do not flatten LGPL/GPL components |
| AG6 | Current Copperbelt plant/subsystem inventory and right to use a validation trace, as section 7; no installed-base guess |
| AG7 | Original unrun fixtures: input change between boundaries; sequential dependent assignments; two tasks with preemption; watchdog overrun; warm/cold restart and retained variable |
| AG8 | Original unrun timer/counter fixtures: zero/changed preset; omitted arguments; skipped/repeated calls; PT boundary; simultaneous reset/load/edges; count beyond PV/type bound. Expected vendor results remain U until sourced or measured with authorized software |
| AG9 | Original unrun plant/HMI fixtures: coil/feedback lag, overload/reset conflict, disconnect/stale quality, alarm acknowledgement and historian timestamp. No safety certification or SCADA parity implied |

These are research findings and future acceptance proposals, not changes to the
engine, contracts, build order or an assertion that all sources are exhausted.
