# PV reconstruction requirements

WP-2.26, ChatGPT, 2026-10-18. Every requirement below is an original Quantic
proposal (I) derived from the cited documentary evidence. Acceptance checks are
future obligations; none was run or passed here. S evidence describes only the
documented product subset in the [matrix](parity-matrix.md). U product cells and
source gaps remain U. No contract change or implementation is authorised.

P0: utility-scale and Copperbelt mine-site energy studies, with lawful site data
and clearly bounded results. P1: detailed geometry, storage and lifetime depth.
P2: specialised pumping/optimiser and broader workflows. Priority is a research
proposal, not a replacement of PLAN.md. No engineering constant, site default,
legal threshold, uncertainty percentage or numerical tolerance is invented.

## Requirements and original acceptance proposals

| ID / priority | Proposed behavior and evidence basis | Original acceptance check, unrun |
| --- | --- | --- |
| PV-R-001 / P0 | Stable project, variant, equipment-type, installed object and orientation identities; PVC-001/050/054, PVE-14, PV6/PV28/PV46 | Clone/reorder a synthetic project with duplicate displayed names; preserve physical/electrical keys and dependencies. Changing geometry must not silently change string mapping |
| PV-R-002 / P0 | Weather manifest binds product/model/version, source period, returned grid/elevation, hash and rights; PVC-002/052/057/059, PVE-01, resource RD1-RD22 | Supply missing, contradictory and denied-use metadata; identify affected field/capability and block unauthorised packaging. Retain raw and transformed hashes |
| PV-R-003 / P0 | Explicit time/quantity semantics; PVC-003/045, PVE-01, PV8/HS4/VS9/RD19 | Author identical intervals under UTC/civil/solar labels and W versus Wh input. Convert correctly or diagnose ambiguous convention; preserve integrated energy with gaps/leap days explicit |
| PV-R-004 / P0 | Select and version solar/transposition/IAM/spectral methods and retain component quantities; PVC-004/005/017, PVE-02, PV10/PV11/PV21/VS5/PP6 | On an original unobstructed plane compare independent angle/component references. Change only transposition model; all unchanged inputs retain provenance and stage differences remain inspectable |
| PV-R-005 / P1 | Distinguish horizon, near optical shading and embedded source corrections; PVC-005-008, PVE-03, PV48/PV52 | Use authored distant skyline and near rectangular occluder; verify geometry/time crossing and flag possible double-applied horizon. Check CAD units/origin/orientation before acceptance |
| PV-R-006 / P1 | Electrical shade treatment declares approximation, cell/submodule/string mapping and bypass assumptions; PVC-009/010/021/040, PVE-06, PV13/PV14/PV35/PP3 | Equal shaded area on different authored electrical connections yields separately explainable I-V responses against an independent small-circuit reference. Unsupported topology cannot receive a detailed-solver success label |
| PV-R-007 / P1 | Tracker law, limits, reference geometry and terrain applicability are explicit; PVC-011/012/056, PVE-04, PV31/PV32 | Equal original rows and deliberately unequal pitch/elevation cases expose angle and residual shade. Do not apply a regular-row law to irregular terrain without an applicability diagnostic |
| PV-R-008 / P1 | Bifacial output identifies front/rear contributions, albedo source, geometry approximation and rear mismatch uncertainty; PVC-013/014, PVE-04/06, PV26/PV28-PV30/PV35 | Author zero-rear and finite-edge cases, then change only albedo/height. Retain terms separately; a 2D model must not claim finite 3D validation or a calibrated rear-mismatch factor without evidence |
| PV-R-009 / P0 | Module technology, fit data and I-V model are versioned with applicability; PVC-015/016/020/054, PVE-05, PV15/PV16/VS4/PP4 | Compare original current/voltage/temperature/irradiance sweeps against independent equations/characterisations. Flag underdetermined fits and unsupported reverse/low-light regions rather than manufacture parameters |
| PV-R-010 / P0 | Thermal model distinguishes steady, transient, cell/module and average states; PVC-018/019, PVE-07, PV17/PV18/PV45 | Independently integrate an authored irradiance step under declared wind/mass; compare interval means and history/reset behavior. Missing/invalid mass or coefficient is a named diagnostic, not an unrecorded fallback |
| PV-R-011 / P0 | Soiling, quality, initial degradation, mismatch and availability have separate provenance/denominators; PVC-020-024/030, PVE-09, PV21/PV33-PV35 | A supplied loss estimate that already includes uneven-dirt mismatch cannot be silently applied twice. Toggle one mechanism at a time and reconcile the stage ledger |
| PV-R-012 / P1 | Mean degradation, dispersion and warranty bounds are distinct; PVC-023/024, PVE-06/09/12, PV34 | Use original uniform/dispersed populations with recorded seed and model. Check module versus AC-energy evolution when clipping changes; do not derive an expected rate directly from a warranty floor |
| PV-R-013 / P0 | Inverter efficiency and input/current/voltage/power constraints are distinct with common physical inverter identity; PVC-025-027, PVE-08, PV19/PV20/PV46/PV47/VS6 | Drive separate constraints with authored profiles and change MPPT sharing. Compare independent operating-point references and retain binding constraint and curtailed DC/AC quantities |
| PV-R-014 / P0 | DC/AC wiring, transformers, auxiliaries and meter boundary are explicit; PVC-028-031/051, PVE-09, PV21/PV22/PV42/HS5/PP8 | Include a vertical wire run and separate delivery losses; reconcile current-dependent loss and boundary energy against independently derived original cases. Missing geometry cannot be silently treated as measured length |
| PV-R-015 / P0 | Export constraints declare kW/kVA, power factor, boundary and allocation; PVC-031, PVE-08/09, PV42 | Hold input constant while changing limit units and downstream losses. Verify the intended boundary and distinguish ordinary clipping, export curtailment, local use and storage diversion |
| PV-R-016 / P0 | Mine demand and outage series preserve meter boundary, chronology, critical loads and provenance; PVC-032/037/052, PVE-01/10, PV36/PV40 | Shift an original load/outage trace relative to weather; report import/export/unmet demand correctly. Exclude any claim about real plant behavior without lawful site evidence |
| PV-R-017 / P1 | Storage topology, state, efficiencies, charge/discharge power and dispatch mode are explicit; PVC-033-037, PVE-10, PV36-PV41 | Original empty/full and power-limited intervals conserve energy. A mode forbidding battery export must never export battery energy; report unmet load separately from unmet charging/export targets |
| PV-R-018 / P1 | Storage strategies have declared objective and admissible actions; PVC-034-037, PVE-10, PV37-PV40 | Compare self-consumption, export peak shaving, scheduled shifting and outage cases under identical assets. Reject unsupported combinations rather than silently substitute an optimiser or generic efficiency factor |
| PV-R-019 / P0 | Energy ledger distinguishes irradiance, effective irradiance, DC availability/usage, AC output and delivered energy; PVC-041/044/045, PVE-09/14, PV21-PV23/HS3/PP8 | Reconcile an authored simple run at every interval and aggregation boundary with independently justified tolerances. Opposing stage errors cannot pass solely because annual totals cancel |
| PV-R-020 / P1 | Annual uncertainty separates variability, bias, measurement/model uncertainty, dependence, horizon and exceedance meaning; PVC-042, PVE-12, PV24/PP7/VS8/RD16 | Use original distributions with known quantiles and dependencies. Verify P90 ordering and annual versus long-term-mean interpretation; reject a blanket P90=0.9P50 rule and unsupported confidence percentages |
| PV-R-021 / P1 | Financial/tariff calculations state their boundary and do not redefine electrical validation; PVC-043, PVE-13, SM3/VS7/VS8/PV51 | Original tariff and battery-replacement scenarios expose cash flows, units and assumptions. A profitability result cannot certify grid compliance or physical-model accuracy |
| PV-R-022 / P0 | Run/report automation records resolved inputs, versions, warnings and output hashes; PVC-044-048/053/059, PVE-14, PV25/PV43/PV50/HS4/VS9/SM3 | Permute an original batch with missing weather and conflicting variants; stop/diagnose affected jobs, preserve successful records, and disclose any selected/synthetic replacement before results are accepted |
| PV-R-023 / P1 | Import/export retains identity, units, model selection and a loss ledger; PVC-007/046/050, PVE-14, PV7/PV44/PV54/PP9/VS9 | Authored round trip preserves physical quantities or names each unsupported/defaulted/dropped item and affected study. A JSON/CSV parse or equal object count does not establish model preservation |
| PV-R-024 / P0 | Independent reference and measured-data validation are distinct from same-backend comparison; PVC-049/052/053, all PVE engines, PV50/RD16/RD22 | Keep authored analytical references and hold-out measurements with calibration/exclusion metadata. Compare intermediate stages and out-of-sample periods; no passed-status claim for unrun cases |
| PV-R-025 / P2 | Standalone, pumping, DC-grid, optimisers and reduced preliminary modes declare output and fidelity limits; PVC-038-040/055, PVC-060, PVE-05/10/11, PV51/SM2 | Original unmet-load/water-demand/DC-grid and reduced-versus-detailed cases identify unsupported physics. Do not report a preliminary monthly sizing result as a detailed chronological simulation |
| PV-R-026 / P0 | Capability/licence gating distinguishes source, wrapper, binary, model, weather and client grants; PVC-057/058, PVE-14, dated engine licence table/RD13-RD18 | A synthetic manifest with a missing component or redistribution grant disables the relevant operation with a diagnostic. A permissive parser grant cannot authorise restricted data or GPL package import |
| PV-R-027 / P0 | Yield study eligibility is separate from fault, grounding, voltage, protection and dynamics; PVC-031/037, PVE-10/14, PVG9/PG9 and mine-rules research | A project requiring interconnection or islanding studies remains incomplete when only energy yield exists. Link required power-suite studies and source jurisdiction; never fabricate a compliance verdict |

## Completeness and evidence gates

PVC-001 through PVC-060 each occur in at least one requirement scope, including
operational/reuse questions as well as numerical engines. The numbered requirements
can share an engine; the same engine can support several workflows. None of the
product-specific algorithm choices is mandatory merely because a vendor uses it.

Original verification ladder: source and rights checks, dimensional/time/identity
checks, analytical stage checks, independent coupled checks, then calibrated site
comparison across the intended envelope. Source citations support methods;
product matching and site accuracy require their own evidence. Numerical tolerance
and acceptance thresholds must be justified before running comparisons, never
loosened to obtain a pass.

B0 topics and unverified Masters pages in the matrix are named acquisition or
reference gaps. The resource inventory's RDG1-RDG8, dossier PVG1-PVG9 and PG1-PG9
remain active. Building, licensed product runs and dataset acquisition remain
outside this research WP.
