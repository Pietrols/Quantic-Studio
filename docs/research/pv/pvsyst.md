# PVsyst

WP-2.23, ChatGPT, accessed 2026-10-18. All product descriptions below are S from
public documentation unless marked I/U. No application was installed or run.
No weather/component library, source project or paid reference was copied.

## 1. Identity: vendor, version, editions and licensing

PVsyst SA publishes PVsyst 8; the release list read here starts at **8.1.7,
30 September 2026** [PV1]. Professional is subscription-based, with separate
education/classroom/student/training-research conditions and report qualifications
[PV2]. PVsystCLI has a separate subscription and documented server/remote use;
being bundled in the installer does not make its licence included [PV2, PV3].
PVsystBasic is separately listed for direct solar pumping, not a cheaper edition
with demonstrated parity to the full desktop product [PV2].

The product page identifies Windows desktop execution and unsupported remote/server
environments for the desktop product, and warns against a live workspace on shared
or synchronised folders [PV4]. Record the exact machine/licence contract before any
future licensed comparison. No prices, seats or licences were purchased.

## 2. Sources

All accessed **2026-10-18**. Help pages are public vendor documentation, not evidence
of our execution. Public access does not grant redistribution of their datasets.

| ID | Title / type | URL |
| --- | --- | --- |
| PV1 | Release notes, vendor | https://www.pvsyst.com/help/release-notes/index.html |
| PV2 | Shop / editions, vendor | https://secure.pvsyst.com/en/shop/ |
| PV3 | PVsystCLI licensing, vendor help | https://www.pvsyst.com/help-cli/licensing/index.html |
| PV4 | PVsyst 8 product/platform requirements, vendor | https://secure.pvsyst.com/en/products/pvsyst/ |
| PV5 | User data/workspace, help | https://www.pvsyst.com/help/getting-started/file-organisation/user-data/index.html |
| PV6 | Projects and PV components, help | https://www.pvsyst.com/help/getting-started/file-organisation/user-data/projects-and-pv-components/index.html |
| PV7 | Format of PVsyst files, help | https://www.pvsyst.com/help/getting-started/file-organisation/user-data/format-of-pvsyst-files.html |
| PV8 | Time Definition in PVsyst, help | https://www.pvsyst.com/help/physical-models-used/time-definition-in-pvsyst.html |
| PV9 | Meteorological data sources, historical v7 help | https://www.pvsyst.com/help-pvsyst7/meteo_datasources.htm |
| PV10 | Transposition models, help | https://www.pvsyst.com/help/physical-models-used/irradiation-models/transposition-model.html |
| PV11 | Perez transposition model, help | https://www.pvsyst.com/help/physical-models-used/irradiation-models/perez-transposition-model.html |
| PV12 | Shadings, help | https://www.pvsyst.com/help/project-design/shadings/index.html |
| PV13 | Electrical shadings, Module Layout, help | https://www.pvsyst.com/help/project-design/shadings/electrical-shadings-module-layout/index.html |
| PV14 | Electrical shadings, partitions, help | https://www.pvsyst.com/help/project-design/shadings/electrical-shadings-module-strings/index.html |
| PV15 | One-diode module model, help | https://www.pvsyst.com/help/physical-models-used/pv-module-standard-one-diode-model/index.html |
| PV16 | Parameters besides datasheets, help | https://www.pvsyst.com/help/physical-models-used/pv-module-standard-one-diode-model/parameters-besides-datasheets.html |
| PV17 | Array thermal losses summary, help | https://www.pvsyst.com/help/project-design/array-and-system-losses/array-thermal-losses/index.html |
| PV18 | Steady-state thermal model, help | https://www.pvsyst.com/help/project-design/array-and-system-losses/array-thermal-losses/steady-state-thermal-model.html |
| PV19 | Inverter efficiency model, help | https://www.pvsyst.com/help/physical-models-used/grid-inverter/inverter-model-efficiency.html |
| PV20 | Inverter operating limits, help | https://www.pvsyst.com/help/physical-models-used/grid-inverter/inverter-operating-limits.html |
| PV21 | Irradiance and PV array simulation process, help | https://www.pvsyst.com/help/project-design/simulation/simulation-process-irradiance-and-pv-array.html |
| PV22 | Grid simulation process, help | https://www.pvsyst.com/help/project-design/simulation/simulation-process-grid-system.html |
| PV23 | Loss diagram, help | https://www.pvsyst.com/help/project-design/results/loss-diagram.html |
| PV24 | P50-P90 evaluations, help | https://www.pvsyst.com/help/project-design/p50-p90-evaluations.html |
| PV25 | PVsystCLI simulation use cases, help | https://www.pvsyst.com/help-cli/use-cases/simulation.html |
| PV26 | Bifacial 2D model conditions, help | https://www.pvsyst.com/help/project-design/bifacial-systems/2d-bifacial-model-conditions.html |
| PV27 | P50/P90 user question, forum indexed excerpt only; direct read returned 403 | https://forum.pvsyst.com/topic/2103-help-estimation-p50-p90/ |

## 3. Architecture and data model

The workspace contains user-created projects/components and can be switched,
imported or exported [PV5]. A project is a set of files: PRJ project, VCi simulation
variants, Cmi comparison variants, MET weather, DAM measured data, and separate
PAN module / OND inverter definitions; batteries, regulators and pumps have their
own component types [PV6]. This is not proof of a shared multi-user network database.

Text formats replaced older binary files, followed by variant-format and UTF-8
changes. The vendor explicitly calls the format internal and unsupported for manual
editing [PV7]. A text file is therefore not a stable public interoperability contract
(I). Preserve source version and use documented export routes first (I).

Weather inputs, project geometry and electrical subarrays are different layers
[PV6, PV13, PV21]. Time definitions distinguish averaged weather intervals and solar
position timing; source time shifts must be resolved rather than guessed [PV8].
The older v7 source catalogue includes imported/synthetic and paid/free resources
[PV9]; it does not establish current coverage or redistribution rights for every
provider. Proposed Quantic weather provenance fields are in the README (I).

## 4. Element catalogue: selected verified parameter semantics

This is a scoped catalogue, not every field in the application.

| Object | Parameter / units / meaning | Source and boundary |
| --- | --- | --- |
| Weather | Global/diffuse horizontal irradiance, W/m²; ambient temperature, °C; wind, m/s; interval/time reference | PV8/PV21; distinguish measured input from derived diffuse |
| Orientation / shade scene | Collector geometry, nearby objects; horizon line for distant obstructions; physical positions tied to strings | PV12/PV13; angular conventions and every import unit still need fixture verification |
| Module | Isc, Impp in A; Voc, Vmpp in V; series/shunt resistance, Ω; diode and temperature-dependent parameters | PV15/PV16; datasheet points alone do not uniquely establish all fitting parameters |
| Thermal model | Uc, W/(m² K); Uv, W s/(m³ K); absorptance/efficiency dimensionless; wind, m/s | PV18; coefficients are site/installation inputs, no defaults adopted |
| Inverter | Efficiency versus power and optionally DC voltage; power threshold; voltage/current/power operating envelope | PV19/PV20; efficiency and clipping are separate mechanisms |
| Electrical subarray | Module/string association and inverter input mapping | PV13/PV21; physical shade area is not electrical loss |
| Bifacial geometry | Regular row-based 2D representation with geometric applicability checks | PV26; arbitrary 3D backside scenes not inferred |

## 5. Studies and modules: calculation chain and boundaries

| Stage / purpose | Method, inputs and outputs stated publicly | Scope / alert / verification issue |
| --- | --- | --- |
| Weather to collector irradiance | Hay-Davies or Perez transposition uses horizontal components and geometry [PV10]. Perez splits diffuse sky contributions; its sub-hourly coefficient treatment changed in v8.1.0 [PV11] | Model name alone is insufficient for version equivalence; derived diffuse and interval timing matter |
| Distant/near shading | Horizon and nearby-object treatments are distinct [PV12]. Detailed Module Layout combines per-module/string I-V behaviour [PV13]; partition-based electrical shading is an alternative approximation [PV14] | Detailed layout has documented capacity warnings/errors [PV13]; no capacity default adopted here. Scene-to-string assignment must be validated |
| Module conversion | Shockley one-diode basis with technology-dependent treatment [PV15]; additional resistance/low-light and temperature parameters may require fitting beyond datasheet values [PV16] | Same STC wattage does not imply identical low-light yield (I) |
| Temperature | Absorbed irradiance minus electrical output balances heat transfer [PV18]. Current help describes steady-state TArrSS plus a thermal-inertia layer producing TArray; measured array temperature can replace the model [PV17] | Historical steady-state-only approximations cannot be assumed identical to current simulation. Fit coefficients; preserve model choice |
| Inverter | Efficiency curve interpolation may depend on power and DC voltage [PV19]. Operating limits shift the array I-V working point and distinguish power, voltage and current losses [PV20] | Clipping is not simply an efficiency multiplier; simultaneous constraints can mask one another |
| Full array/system losses | Optical corrections precede module conversion; effective irradiance, temperature/irradiance effects, mismatch and wiring feed array MPP/used energy [PV21]. Grid stage treats conversion and system delivery [PV22] | Keep stage quantities and units; no vendor default is a mine-site assumption |
| Bifacial | Simplified 2D geometry has explicit regularity/applicability conditions [PV26] | Do not extrapolate to arbitrary irregular 3D terrain without separate validation |
| Reporting | Annual loss diagram identifies mechanisms [PV23]; output variables and aggregation belong to the simulation process [PV21, PV22] | Compare absolute energy and reference denominator, not only rounded loss percentages (I) |
| Yield uncertainty | Annual-yield Gaussian model; combined component uncertainties use quadrature; default centre is simulated yield, optional mean shift [PV24] | Inputs are user assumptions, not generated proof of confidence; unsupported for stand-alone/pumping. Monthly/hourly P90 not established by this annual method |

P50 is the median and P90 is an exceedance energy, not "90% of P50" [PV24].
For Quantic (I), keep meteorological variability, measurement/model uncertainty,
systematic bias, degradation horizon and correlations separate. A covariance-aware
extension would require new evidence; it is not claimed as PVsyst's algorithm.

The product documents grid-connected, stand-alone, DC-grid and pumping paths
[PV21]. Detailed storage/dispatch, optimiser, pumping and financial internals are
outside this first pass and listed as gaps rather than reconstructed from menus.
No claim of current IEC/IEEE electrical-safety certification follows from a yield run.

## 6. Workflow and interface

Documented path: define project/weather and a simulation variant, choose components
and array configuration, specify geometry/shading and losses, simulate, inspect
stage outputs/loss report, then compare variants [PV6, PV13, PV21, PV23]. This is a
source-based workflow, not an observed click-through.

PVsystCLI runs prepared workspace/project/variant inputs, can vary weather or batch
parameters and produces CSV/batch/report outputs [PV25]. Its active subscription is
separate [PV3]. CLI output is an automation interface, not a public source-code API.
Do not rely on manual editing of internal files as a guaranteed supported route [PV7].

## 7. User value and complaints

Public help gives unusually specific modelling explanations and loss-stage reporting
[PV10-PV24]. Calling this useful for traceability is our evaluation (I), not a user
survey. One indexed forum question asks how to choose uncertainty values over plant
life [PV27]; full thread was inaccessible, so no prevalence, resolution or sentiment
claim is made. Independent customer satisfaction, support quality and defect rate
remain U. Release-note corrections [PV1] are vendor maintenance evidence, not proof
that every older case was materially wrong.

## 8. Engines implied and independent implementation routes

The decomposition is I from the sourced study chain: weather ingestion/time QA;
solar position and decomposition; component-resolved transposition; geometry/shadow
calculation; electrical mismatch/I-V assembly; temperature; module parameter fitting;
inverter constraints/conversion; system losses and dispatch; uncertainty; and
versioned reporting. It is not a recovered proprietary architecture.

The [peer dossier section 8](other-products.md#8-engines-implied-open-candidates-and-books)
maps pvlib and SSC model coverage, actual dated licences and Masters 2004. In
particular, pvlib's documented PVsyst parameter model refers to v6, not blanket
PVsyst 8 numerical parity. Original stage-by-stage fixtures and measurement validation
are needed before choosing defaults or claiming equivalent yields (I).

Proposed validation (I): zero-shade optical case; one moving obstruction with known
string assignment; hot/cold module sweeps; separate inverter current/voltage/power
constraints; irregular time intervals; energy-ledger closure; and uncertainty
quantile ordering. Author our own geometry/parameters, record model versions and
compare intermediate quantities before annual totals. No fixture has been run here.

## 9. Gaps and closure routes

| Gap | Why unresolved / evidence needed |
| --- | --- |
| PVG1 | Full current private file schema and version migration are not public supported contracts; obtain lawful original exports and document field loss before import work |
| PVG2 | Current weather-provider coverage, prices and reuse terms differ; verify each contracted dataset and its timestamp conventions, never copy bundled weather |
| PVG3 | All current technology-specific fit details and coefficient provenance not traced; inspect public model papers and lawful datasheets, not inferred STC-only fits |
| PVG4 | Detailed shading, bypass/half-cell/reverse behaviour and irregular bifacial geometry need original numerical fixtures; no runtime access in this WP |
| PVG5 | Thermal-inertia coefficients, integration details and version-specific effects require public model-page/paper review and measurement validation |
| PVG6 | Storage dispatch, off-grid unmet load, pumping, optimiser and lifetime financial model internals not fully reviewed; use their dedicated help before claiming parity |
| PVG7 | Uncertainty component distributions, dependence and site calibration need independent sources; no default percentage justified for a Zambian mine |
| PVG8 | User survey and full forum thread unavailable; no generalised sentiment. Licensed runtime comparison and precise version provenance remain unperformed |
| PVG9 | Local interconnection, earthing, faults and ride-through require the separate power study/rule profile, not an energy-yield report; see [mine rules](../power/mining-regulations.md) |
