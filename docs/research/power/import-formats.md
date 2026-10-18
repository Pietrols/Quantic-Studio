# Power model interchange: formats, losses and independent fixtures

WP-2.24, ChatGPT, 2026-10-18. Research only. No application, importer,
converter, round trip or numerical comparison was executed. This is not a claim
of compatibility with any commercial product. S means documented evidence,
I an original proposal, U an unresolved question. Source IDs below are local to
this dossier. All linked sources and licence files were accessed 2026-10-18.
The [source ledger](../../sources/entries/power-import-formats-2026-10-18.yaml)
records provenance. Existing [R-037 to R-041](reconstruction-requirements.md)
remain the requirements; this document does not change a contract or approve a build.

## 1. Versioned format register

| Format | Public evidence and version | Structure and conventions | Explicit specification gap |
| --- | --- | --- | --- |
| PSS/E RAW / RAWX | S: IF1 introduces extensible RAWX in PSS/E 35; IF2 is historical ANDES 1.7.3 documentation for RAW 32/33 | RAW steady-state records have revision-specific fields. Reader source IF4 distinguishes system base, bus base kV, branch p.u. impedance and MVA ratings, transformer CW/CZ/CM interpretation flags and winding/pair bases. RAWX is not assumed to be interchangeable text RAW | U: current complete Siemens record specification, every supported revision, RAWX schema, extensions and sequence-data treatment were not retrieved from an official public specification |
| PSS/E DYR | S: IF2 documents slash-terminated dynamic records containing bus identity, quoted model name, device ID and model-specific parameters | Model dictionary and ordered parameters matter independently of RAW revision. A matching model name is not evidence of equivalent equations, limits, initialisation or binary execution | U: full current Siemens model dictionaries, user-model ABI and version compatibility. IF2's historical statement about DYR versions must not become a permanent versionless-format assumption |
| PowerWorld AUX | S: IF5, Simulator 24 specification updated 1 September 2026 | DATA/SCRIPT blocks; declared object/field lists, key fields, quoted values and typed SUBDATA. BusNum and generator bus/ID are examples of keys, not names alone. Units are field-specific. Display objects need additional identity when several views represent an asset | U: exact fields and study objects needed for an arbitrary older/newer case. The document is not a universal guarantee that every simulator state is serialised |
| PowerFactory DGS | S: IF8 documents ASCII/XML/CSV/ODBC variants; IF9 identifies vector support from DGS 7.0 | Typed objects and foreign-key references; dynamic import requires appropriate model-type definitions. Encoding or extension alone does not define class/attribute units or semantics | U: complete current DGS_Documentation.pdf, especially chapter 6.7 vector/matrix normalisation, is referenced in installed help but not retrieved publicly. Exact schema and revision-specific class mappings remain open |
| CIM / CGMES | S: IF10/IF11 distinguish CGMES 2.4.15 and 3.0.0. Public 2014 specification uses CIM16; the formal 3.0 IEC specifications are a separate source | Profile-based RDF/XML descriptions with identities and references across files. EQ, TP, SSH and SV are not interchangeable snapshots; boundary profiles matter. DY, DL and GL already occur in the 2.4.15 specification. IF12 describes datatype/unit and rdf:ID/rdf:about handling | U: complete formal IEC 61970-600-1/-2 text and every current profile/extension mapping were not read. A September 2026 NC profile bundle version 2.5 is not CGMES version 2.5 |
| OpenDSS scripts | S: IF15-IF19, living EPRI command documentation, not a pinned engine release | Ordered commands create/edit circuit objects. Bus node order and ground node 0 are explicit. LineCode supports sequence or matrix data with stated length units. Compile/Redirect and external shape files make file resolution part of the model | U: exhaustive release-specific grammar, every property/default and extension-engine difference. Living help and a product major-version label do not pin an executable |

RAW/DYR are separated because a successful static network import cannot establish
dynamic coverage. CGMES is a family of profiles and versions, not merely XML.
OpenDSS and AUX may contain commands: ingestion is not inherently passive parsing.

## 2. What survives a conversion?

This table is documentary scope, not a tested capability matrix. A U is not a
claim that the format lacks the feature. Preservation depends on both endpoints.

| Format | Topology and reusable types | Dynamics / protection | Diagrams and principal loss risks |
| --- | --- | --- | --- |
| RAW / RAWX | S: bus/branch/equipment connectivity and revision-specific electrical records; not a general native object-library reconstruction | RAW alone does not establish DYR/SEQ/user-model coverage; complete protection representation U | Native diagram preservation U. Transformer base/flag interpretation, status, circuit keys and device aggregation can change behavior without changing element counts |
| DYR | Model records refer to network equipment and named dynamic models | S: IF2 maps supported models and rejects unknown models in that reader. Full relay catalogue and user binary behavior U | Diagram scope U. Dropped models, parameter order, model aliases, missing RAW devices or silently substituted models are critical losses |
| AUX | S: case data and separately handled display objects use the AUX family, IF6/IF7 | S: transient-stability help explicitly supports AUX dynamic data. Complete protection/control coverage needs object/field-level verification | S: display AUX has different objects/commands. Electrical identity must not be merged with view identity; SCRIPT execution is an additional risk |
| DGS | S: object/class/type references, IF8/IF9; exact terminal and attribute mappings need the selected schema | S: documented dynamic-model import route depends on pre-existing types. A DGS dynamic object is not proof that DSL source or external models are executable | Converter-dependent layout and class coverage U. Shared types, missing references, normalised vectors and unsupported classes require loss entries |
| CGMES | S: equipment, connectivity/topology and state are distributed over profiles; boundary sets can be necessary | S: DY profile exists in 2.4.15. This does not establish arbitrary proprietary controls, relay logic or binary model portability | S: DL/GL profiles address layout/location. Missing profiles, mRID/URI confusion, absent boundaries and mismatched solved-state/tap representations are distinct losses |
| OpenDSS | S: ordered circuit commands, explicit nodes, sequence/matrix data, external-file dependencies | Full mapping of relay, controller and dynamic classes is U in this dossier; no claim that a static importer preserves them | Complete native schematic interchange U. Phase reduction, neutral elimination, command order, include paths and external shape loss can alter the electrical model |

Specific evidence behind these cautions:

- IF2's historical reader converted switched shunts to fixed shunts, did not
  convert HVDC and supported only some three-winding transformer flags. Those
  are ANDES 1.7.3 limitations, not assertions about all readers today (S).
- IF20 includes historical fixes to PowerWorld's PSS/E transformer CW/CZ handling.
  This establishes a concrete class of conversion error, not a current unfixed
  defect in PowerWorld (S).
- IF13 section 3.2 identifies the ACLineSegment BaseVoltage association used for
  p.u. conversion. Arbitrarily taking a terminal's nominal or solved voltage is
  not an equivalent rule. Section 2.2 distinguishes transformer/tap quantities (S).
- IF14 warns against deriving exchange metadata from human-readable filenames.
  IF12 explains that profile descriptions can add properties to an existing
  identified object; treating each description as a new object is unsafe (S).
- IF17 distinguishes Compile directory behavior from Redirect. IF18 identifies
  external load-shape files. IF19's sequence/matrix and length-unit distinctions
  prevent treating every line number as the same unit system (S).

## 3. Open implementations and rights checks

The following are candidates for evaluation, not selected dependencies. Licence
files were actually read on 2026-10-18; paths and blob identities are retained
in section 7. Documentation versions, upstream test claims, installed versions
and Quantic tests are separate columns. No converter tests were run here.

| Candidate and documented direction | Version evidence and limits | Dated licence finding | Quantic execution status |
| --- | --- | --- | --- |
| VeraGrid file operations, RAW/RAWX, DGS and CGMES read/write | IF21 docs 6.7.13 list RAW 29-35 and CGMES 2.4.15/3.0. Foreign formats are not fully lossless; steady-state snapshots and profile points differ. Internal normalisation can remap bus numbers. Newer source directories alone do not prove tested support | IF25 engine MPL-2.0, read 2026-10-18; data files and other packages require separate review | None; no end-to-end reader/writer or electrical round trip validated |
| pandapower CGMES import | IF22 docs 4.0.0 list 2.4.15/3.0 and upstream development/testing on Python 3.11. Optional repairs, topology transformations, diagram and state/control selections affect semantics | IF26 BSD-3-Clause, read 2026-10-18 | None; repository lock remains 3.5.6, not upgraded to documentation 4.0.0 |
| pandapower PowerFactory import | IF23 uses installed PowerFactory's Python Application API, not a stand-alone DGS parser. PF2022 SP1/Python 3.10 is a documented configuration example, not a 2026 compatibility test | IF26 for converter; proprietary PowerFactory runtime rights separate, read 2026-10-18 | None; installed/vendor runtime not exercised |
| pandapower OpenDSS import | IF24 docs 4.0.0 require OpenDSSDirect.py, compile/solve and produce balanced positive-sequence data. Phase/split-phase reduction and solved taps are not preservation of every original controller | IF26 plus IF29 custom OpenDSSDirect.py terms and backend/component obligations, read 2026-10-18 | None; not an unbalanced lossless importer claim |
| ANDES RAW + DYR reader | IF2 explicitly describes 1.7.3 RAW 32/33 support; IF3 current 2.0.0 documentation describes RAW/DYR ingestion without establishing every current RAW revision | IF27 GPL-3.0-or-later, read 2026-10-18. Repository rule permits only a separate process, never package import or parser-code copying | None; historic supported-model lists are not a current test certificate |
| DSS-Python / DSS C-API script interpreter route | EPRI scripts and extension-engine compatibility require a pinned wrapper, backend and engine. No complete source-preserving writer or export-version matrix established here | IF28 wrapper BSD-3-Clause; EPRI-derived C-API notice and own licence; IF30 backend mixed BSD/LGPL components, all read 2026-10-18 | None; native command execution must not be mislabelled passive parsing |
| OpenDSSDirect.py, optional bridge used by IF24 | Exact installed release and engine compatibility U; current default-branch licence is not automatically every historic release's terms | IF29 custom Alliance licence, not a stock BSD-only conclusion. Includes source-publication conditions for research-entity redistribution, modified-name restrictions and acknowledgement requirements, read 2026-10-18 | None; release-specific legal/dependency review required before adoption |

No open AUX reader with verified licence and revision coverage was selected (U).
This is not evidence that none exists. A vendor automation API would additionally
require its own runtime/licence and does not become open-source because a client
wrapper is open. Similarly, IF8's proprietary PSS/E converter documents RAW,
RAWX, SEQ and DYR versions 27-35, with export separately licensed; that is not
the coverage of DGS or of the open readers above.

IF4 source metadata itself needs review: the transformer SBASE property annotation
and its descriptive text disagree about units. The branch CKT label is also not
a reliable semantic dictionary. These source-read findings are reasons to require
the authoritative revision specification, not to copy an annotation into Quantic.

## 4. Original proposed import and loss behavior (I)

These proposals explain the existing requirements; they are not new contracts.

1. Identify the revision, profile set, model dictionary and importer build before
   interpretation. Reject unsupported revisions with an explicit diagnostic;
   preserve original identities separately from generated internal keys.
2. Keep source field values, units, base choices, orientation, phase order,
   transformer connection/tap semantics, status and shared-type references.
   Do not replace an unknown unit or model with a plausible default.
3. Record every unsupported, defaulted, reduced, repaired or dropped item with
   original identity, target representation, reason and affected studies.
   Missing dynamics may leave static studies eligible; it must not mark a
   transient study complete. Make eligibility study-specific.
4. Compare a structural/electrical round trip, not byte equality: connectivity,
   bases, parameters, status, connection groups, controls and solved quantities
   where independently available. Keep layouts and electrical identities separate.
5. Default to data-only intake. Do not execute AUX SCRIPT blocks, arbitrary
   OpenDSS commands, external DLLs or imported DSL just to inspect a file.
   Any later engine-assisted route needs explicit command/file capabilities,
   bounded dependency resolution and isolated runtime permissions. This research
   has executed none of them.
6. Keep ABI/compiler/runtime compatibility separate from parameter parsing.
   Keep source-code, engine, binding, model library, relay-curve and dataset rights
   separate. An open parser licence does not grant a proprietary case licence.

## 5. Original fixture proposals for R-037 to R-041 (I)

All fixtures below are to be authored independently from a small declarative
network, not copied or adapted from vendor examples, public test systems or
client projects. They are proposals, not checked-in test inputs or passed tests.
No numerical acceptance tolerance is guessed here. Future numerical comparisons
need source-backed model equations, solver provenance and justified tolerances.

| ID | Original stimulus and expected oracle | Requirement |
| --- | --- | --- |
| FMT-01 | Distinct buses/devices share names; record order is permuted. Version-supported imports preserve explicit keys/connectivity; unknown revision produces a revision diagnostic, not guessed interpretation | R-037 |
| FMT-02 | Author transformer/line data with deliberately distinct system, winding and pair bases, CW/CZ-style flags and explicit length units. Independent dimensional/base conversion must preserve the authored physical impedances; a flag or unit mutation must be detected | R-037, R-039 |
| FMT-03 | RAW-like static network plus one supported and one deliberately unknown DYR model. Retain the unknown record and report dynamic ineligibility; no dummy substitution, DLL loading or claim that model-name recognition establishes ABI compatibility | R-038, R-040 |
| FMT-04 | AUX-like data with repeated display instances and a harmless marker SCRIPT command. Data-only intake preserves asset/view identities separately and reports non-execution of commands; the marker must never be executed | R-037, R-038, R-040 |
| FMT-05 | DGS-like shared type referenced by two devices, one missing foreign key and a vector requiring a selected schema revision. Preserve sharing, diagnose the missing key and reject unsupported vector representation rather than flatten it silently | R-037, R-038 |
| FMT-06 | CGMES-like authored objects split across equipment/topology/state descriptions with matching identity but repeated names. Profile reordering does not duplicate assets; absent required boundary/profile gives a completeness diagnostic | R-037, R-038, R-039 |
| FMT-07 | CGMES-like line BaseVoltage intentionally differs from another nearby voltage association; tap state and position are distinct. Conversion uses the declared profile rule, never the nearest numeric voltage or filename metadata | R-037, R-039 |
| FMT-08 | OpenDSS-like node permutation, explicit neutral/ground distinction, alternate equivalent length units and an external authored load-shape dependency. Preserve phase/neutral semantics and resolve only authorised dependencies; positive-sequence reduction must carry a loss entry | R-037, R-038, R-039 |
| FMT-09 | Round trip reverses branch terminal ordering while preserving equivalent physical orientation, then deliberately changes a vector group, controller or in-service flag. First transformation preserves physical meaning; second is detected even with unchanged object counts | R-039 |
| FMT-10 | Synthetic model manifest separates parser, engine, optional binding, external model and dataset grants. A denied/missing grant or incompatible ABI blocks only the relevant capability and cannot be bypassed by successful static parsing | R-040, R-041 |

For each future fixture, capture authored source hash, exporter/importer version,
normalised graph, transformations/loss ledger and eligibility before comparing a
result. Metamorphic identity/unit/order checks supplement, not replace, independent
electrical references. Textual export equality is insufficient.

## 6. Named open gates

- IFG1: obtain an authorised revision-specific Siemens RAW/RAWX/DYR specification
  and required model dictionaries before implementing those records.
- IFG2: obtain the selected installed DGS specification, including chapter 6.7;
  verify class/terminal/unit mappings and model-type prerequisites.
- IFG3: pin AUX object/field dictionaries and distinguish case data, diagrams,
  dynamic records and commands for the target Simulator version.
- IFG4: pin the CGMES profile/extension/header set and boundary requirements;
  formal IEC access and profile-specific unit mappings remain source gates.
- IFG5: pin OpenDSS engine and extension builds, command/property support,
  external-file rules and controller/protection/dynamic coverage.
- IFG6: no reader, writer or fixture above has Quantic runtime validation.
  Upstream examples, test statements and source directory names are not our passes.
- IFG7: dependency approval is not granted. Review exact release artefacts and
  bundled components, especially custom OpenDSSDirect.py and LGPL backends;
  keep GPL ANDES process-only. Do not redistribute vendor cases/model libraries.
- IFG8: full dynamic/protection/diagram round trips and unsupported-object
  preservation remain U until object-level tests and independently justified
  electrical or behavioral oracles exist.

## 7. Primary sources and inspected scope

| ID | Source and inspected scope |
| --- | --- |
| IF1 | Siemens [PSS/E version 35](https://www.siemens.com/en-us/products/pss-software/psse-version-35/), indexed official feature description only; full direct page fetch timed out. RAWX introduction, not record specification |
| IF2 | ANDES [PSS/E formats, v1.7.3](https://docs.andes.app/en/v1.7.3/getting_started/formats/psse.html), full page; supported revisions, DYR record description and converter caveats |
| IF3 | ANDES [data and formats, stable 2.0.0](https://docs.andes.app/en/stable/tutorials/05-data-and-formats.html), public ingestion documentation; current revision guarantee not inferred |
| IF4 | VeraGrid source, [circuit](https://github.com/SanPen/VeraGrid/blob/master/src/VeraGridEngine/IO/raw/psse_circuit.py), blob 172377c402ef9ac04405737993117c0bb4373ef7; [bus](https://github.com/SanPen/VeraGrid/blob/master/src/VeraGridEngine/IO/raw/versioned/base/bus.py), 16a504b3c3b4dc76773b29e4e6e274caf3982fe2; [branch](https://github.com/SanPen/VeraGrid/blob/master/src/VeraGridEngine/IO/raw/versioned/base/branch.py), 858c811b08bc2209ddd738ddf7c75b89102af816; [transformer](https://github.com/SanPen/VeraGrid/blob/master/src/VeraGridEngine/IO/raw/versioned/base/transformer.py), 1e8f8be2ff2ad75dd63991cc1f4b0070b49904e1. Field metadata inspected, no parser code copied |
| IF5 | PowerWorld [Auxiliary File Format](https://www.powerworld.com/WebHelp/Content/Other_Documents/Auxiliary-File-Format.pdf), Simulator 24, updated 2026-09-01; printed pp. 15, 157-165, 216-218 and contents inspected |
| IF6 | PowerWorld [Auxiliary files](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Auxiliary_Files.htm), case/display distinction |
| IF7 | PowerWorld [transient stability case information](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transient_Stability_Case_Info_Menu.htm), AUX dynamic-data support |
| IF8 | DIgSILENT [data converters](https://www.digsilent.de/en/data-converter.html), DGS variants and separate PSS/E converter scope/licensing |
| IF9 | DIgSILENT [dynamic models via DGS](https://www.digsilent.de/en/faq-reader-powerfactory/how-can-i-import-dynamic-models-via-dgs.html), DGS 7.0 vectors, installed-document reference, model types. Attachments not copied or executed |
| IF10 | ENTSO-E [CIM for grid model exchange](https://www.entsoe.eu/data/cim/cim-for-grid-models-exchange/), public profile/version index and September 2026 NC bundle metadata |
| IF11 | ENTSO-E [CGMES 2.4.15 specification](https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/Grid_Model_CIM/140807_ENTSOE_CGMES_v2.4.15.pdf), 2014, 41 pages; cover/approval, scope, profile structure and versioning |
| IF12 | ENTSO-E [RDF syntax user guide 2.0.0](https://www.entsoe.eu/Documents/CIM_documents/Grid_Model_CIM/RDF-SyntaxUserGuide_v_2-0-0.pdf), public 2026 release; sections 2.2.1.1-2.2.1.2 and header handling |
| IF13 | ENTSO-E [CGMES 2.4.15 implementation guide](https://www.entsoe.eu/Documents/CIM_documents/Grid_Model_CIM/150630_ImplementationGuide_CGMES_2_4_15.pdf), 2015-06-30, six pages, sections 2.2 and 3.2 |
| IF14 | ENTSO-E [CIM/CGMES implementation Q&A 1.0.1](https://www.entsoe.eu/Documents/CIM_documents/Grid_Model_CIM/QandA_on_CIM_CGMES_based_data_exchange_implementation_v1-0-1.pdf), 2024-04-25, section 6.6 metadata caveat |
| IF15 | EPRI [scripting language basics](https://opendss.epri.com/BasicsoftheOpenDSSScriptingLangu.html) and [executive](https://opendss.epri.com/Executive2.html), living command help |
| IF16 | EPRI [bus definition](https://opendss.epri.com/BusDefinition.html), indexed official text; direct page fetch failed, node-order/ground discussion only |
| IF17 | EPRI [Compile technical note](https://opendss.epri.com/TechNoteCompile.html), full short note, Compile/Redirect directory behavior |
| IF18 | EPRI [including external files](https://opendss.epri.com/IncludingExternalFiles.html), external shape-file dependencies |
| IF19 | EPRI [LineCode](https://opendss.epri.com/LineCode1.html), sequence/matrix parameters and length units |
| IF20 | PowerWorld [Simulator 22 patch releases](https://www.powerworld.com/patch-releases/simulator-22), historical transformer CW/CZ export fixes, not a current defect claim |
| IF21 | VeraGrid [file operations](https://veragrid.readthedocs.io/en/latest/md_source/file_operations.html), docs 6.7.13, supported versions/directions and conversion caveats |
| IF22 | pandapower [CGMES converter](https://pandapower.readthedocs.io/en/latest/converter/cgmes.html), docs 4.0.0, supported versions, Python statement and transformation options |
| IF23 | pandapower [PowerFactory converter](https://pandapower.readthedocs.io/en/latest/converter/powerfactory.html), docs 4.0.0, installed Application API, example runtime and class scope |
| IF24 | pandapower [OpenDSS converter](https://pandapower.readthedocs.io/en/latest/converter/opendss.html), docs 4.0.0, positive-sequence import and approximation reporting |
| IF25 | VeraGridEngine [LICENSE.txt](https://github.com/SanPen/VeraGrid/blob/master/src/VeraGridEngine/LICENSE.txt), blob 14e2f777f6c395e7e04ab4aa306bbcc4b0c1120e, MPL-2.0 |
| IF26 | pandapower [LICENSE](https://github.com/e2nIEE/pandapower/blob/develop/LICENSE), blob 3768e1ffd742ff0a04dfb673741ad0099a433a77, BSD-3-Clause |
| IF27 | ANDES [LICENSE](https://github.com/cuihantao/andes/blob/master/LICENSE), blob 74ae8d9ead6c7ad2baa3f68d8146cc00eecdadf6, GPL-3.0-or-later |
| IF28 | DSS-Python [LICENSE](https://github.com/dss-extensions/DSS-Python/blob/master/LICENSE), e445e1fbeb4176321e9c2ce2bd3468ceea604e0c; C-API [OpenDSS notice](https://github.com/dss-extensions/dss_capi/blob/master/OPENDSS_LICENSE), b6ed217a22c977284209e1ac8cb1dd4881790074; [own licence](https://github.com/dss-extensions/dss_capi/blob/master/LICENSE), ce5c7dfad25854f20324f7e859ee01b37c289d28 |
| IF29 | OpenDSSDirect.py [LICENSE](https://github.com/dss-extensions/OpenDSSDirect.py/blob/master/LICENSE), blob a3675ca48617ab5ca4e08a4e39f53fad0158b966, custom Alliance terms; actual text read, not inferred from metadata |
| IF30 | DSS backend [BSD file](https://github.com/dss-extensions/dss_python_backend/blob/master/LICENSE.BSD3), 750348e90641035588b84e52b74334c8dd40f14a; [LGPL file](https://github.com/dss-extensions/dss_python_backend/blob/master/LICENSE.LGPL3), 0a041280bd00a9d068f503b8ee7ce35214bd24a1; [README](https://github.com/dss-extensions/dss_python_backend/blob/master/README.md), 6dcde493ceb00befce04f3aa08a83225d8124b53, bundled-component distinction |

Source files, vendor examples, attachments, standards text and dataset records
are not redistributed. Default-branch links are mutable; retained blob identities
identify the inspected licence/source content. No full licensed specification is
reconstructed from unofficial manual mirrors.
