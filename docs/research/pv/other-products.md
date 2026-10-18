# PV peers: HelioScope, SAM, PV*SOL and PlantPredict

WP-2.23, ChatGPT, accessed 2026-10-18. A lighter, public-source dossier covering
all nine template sections for each product through shared tables. S means a source
states it, not our runtime observation. U is unknown, not missing. I is our proposal.
No product, paid dataset or component library was installed, purchased or copied.

## 1. Identity, versions, licensing and platforms

| Product | S identity / version / access evidence | Unresolved identity boundary |
| --- | --- | --- |
| HelioScope | Aurora Solar-linked service; current help distinguishes V2 and Classic and Basic/Pro/Enterprise plans [HS1-HS3]. Subscription quotas and feature entitlements are documented [HS1] | No immutable SaaS engine build captured. V2 help is not proof that every Classic workflow matches |
| SAM | System Advisor Model, formerly NREL naming, current official site National Laboratory of the Rockies. Download identifies SAM 2026.7.3 / SSC 308 for Windows, macOS and Linux [SM1]. Desktop is a front end to SSC [SM3] | Exact downloaded binary not inspected or executed. Older sam.nrel.gov pages can lag the current sam.nlr.gov site |
| PV*SOL | Valentin Software; downloads list premium 2026 R8 and PV*SOL 2026 R6, distinct 3D versus 2D offers [VS1]. Official shop lists named-user subscriptions [VS2] | Exact platform/build requirements and legacy perpetual-contract rights need specific contract/requirements check; no inference from a current shop listing |
| PlantPredict | Terabase Energy utility-scale cloud service [PP1]. Public technical docs distinguish version-12+ shading features [PP3] | No immutable SaaS build captured. Pricing page simultaneously exposes inconsistent plan/API statements [PP2], so exact entitlement/price must come from an order form |

## 2. Sources

All accessed **2026-10-18**; all are primary vendor/project/publisher sources unless
explicitly stated. Technical algorithms are sourced to help, not marketing comparisons.

| ID | Title / type | URL |
| --- | --- | --- |
| HS1 | Plan/terms changes, official help, updated May 2026 | https://help-center.helioscope.com/hc/en-us/articles/18081975003539-Changes-to-HelioScope-s-Terms-of-Use-and-Pricing-Plans |
| HS2 | Condition Sets in V2, help, updated July 2026 | https://help-center.helioscope.com/hc/en-us/articles/8547624781459-Condition-Sets-in-HelioScope-V2 |
| HS3 | Production report summary, help | https://help-center.helioscope.com/hc/en-us/articles/8198806782483-Production-Report-Summary |
| HS4 | Hourly production CSV, help, updated June 2026 | https://help-center.helioscope.com/hc/en-us/articles/8536799301523-Hourly-Production-Report-CSV |
| HS5 | Wire-length limitation, help, updated March 2026 | https://help-center.helioscope.com/hc/en-us/articles/49398186817427-Why-do-my-wire-lengths-seem-inaccurate |
| HS6 | Shade modelling, official help | https://help-center.helioscope.com/hc/en-us/articles/7899937559443-Shade-Modeling |
| SM1 | SAM current download/version/platform page | https://sam.nlr.gov/download.html |
| SM2 | SAM photovoltaic models, official documentation | https://sam.nlr.gov/photovoltaic.html |
| SM3 | SSC SDK, PySAM and code generation, official documentation | https://sam.nlr.gov/software-development-kit-sdk.html |
| SM4 | SAM actual upstream licence file | https://github.com/NatLabRockies/SAM/blob/patch/LICENSE |
| VS1 | Current trial downloads / editions, vendor | https://valentin-software.com/en/downloads/ |
| VS2 | Subscription product catalogue, vendor | https://shop.valentin-software.com/en/collections/all |
| VS3 | System type, climate and grid, official help | https://help.valentin-software.com/pvsol/en/pages/system-type-climate-and-grid/ |
| VS4 | Characteristic curve models, official help | https://help.valentin-software.com/pvsol/en/calculation/pv-modules/characteristic-curve-models/ |
| VS5 | Inclined-plane irradiance, official help | https://help.valentin-software.com/pvsol/en/calculation/irradiation/irradiation-onto-inclined-plane/ |
| VS6 | Inverter calculation, official help | https://help.valentin-software.com/pvsol/en/calculation/inverters/ |
| VS7 | Results, official help | https://help.valentin-software.com/pvsol/en/pages/results/ |
| VS8 | P50/P90 bankability, official help | https://help.valentin-software.com/pvsol/en/pages/financial-analysis/bankability/ |
| VS9 | Project JSON / results CSV export, official help | https://help.valentin-software.com/pvsol/en/pages/presentation/export-simulation-results/ |
| PP1 | PlantPredict company/product identity, vendor | https://www.plantpredict.com/about |
| PP2 | Current pricing and API entitlements, conflicting page blocks | https://www.plantpredict.com/pricing |
| PP3 | Shading models overview, official technical documentation | https://docs.plantpredict.com/models/shading/overview |
| PP4 | DC performance overview, official technical documentation; legacy path | https://docs.plantpredict.com/models/dc-performance/dc_performance_overview |
| PP5 | Block hierarchy, official user guide | https://docs.plantpredict.com/user-guide/ui/power-plant-builder-block |
| PP6 | Transposition models, official technical documentation | https://docs.plantpredict.com/models/transposition/overview |
| PP7 | Uncertainty configuration, official user guide | https://docs.plantpredict.com/user-guide/ui/uncertainty-analysis |
| PP8 | P50 loss tree, official results guide | https://docs.plantpredict.com/user-guide/results/p50-loss-tree |
| PP9 | PVsyst project import, official workflow guide | https://docs.plantpredict.com/user-guide/workflows/import-pvsyst-project |
| OS1 | pvlib ModelChain 0.16.1, project API docs | https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.modelchain.ModelChain.html |
| OS2 | pvlib calcparams_pvsyst, project API docs | https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.pvsystem.calcparams_pvsyst.html |
| OS3 | pvlib actual upstream licence | https://github.com/pvlib/pvlib-python/blob/main/LICENSE |
| OS4 | SSC actual upstream licence | https://github.com/NatLabRockies/ssc/blob/patch/LICENSE |
| OS5 | SSC README with bundled dependency notices | https://github.com/NatLabRockies/ssc/blob/patch/README.md |
| BK1 | Masters, Renewable and Efficient Electric Power Systems, Wiley 2004, publisher metadata/contents | https://onlinelibrary.wiley.com/doi/book/10.1002/0471668826 |

PVsyst source IDs PV1-PV27 resolve in [pvsyst.md](pvsyst.md), not the power matrix.

## 3. Architecture and data model

| Product | S model structure | I interpretation / unresolved boundary |
| --- | --- | --- |
| HelioScope | Project designs and Condition Sets separate layout/component selection from weather, horizon, thermal and loss assumptions [HS2]; simulation report records assumptions [HS3] | Preserve design and conditions as separate immutable run inputs. Multi-user revision conflict semantics not established |
| SAM | Detailed PV separates module/inverter models and equipment selection; PVWatts deliberately uses fewer inputs [SM2]. SDK exposes simulation modules and typed inputs/outputs; code generator exports case inputs [SM3] | Do not confuse desktop case, SSC module version and financial model. Exact project schema/round-trip remains unverified |
| PV*SOL | System type selects active planning pages and climate/time resolution [VS3]; component model and results paths are documented [VS4, VS7] | Energy-flow system and 3D layout are different layers. No claim of power-system node-breaker or RMS state models |
| PlantPredict | Blocks contain arrays/inverters/DC fields in the plant builder [PP5]; predictions have uncertainty settings [PP7] and staged result aggregation [PP8] | Hierarchy multipliers, identities and electrical equivalence must be tested before import. Cloud build pinning remains U |

## 4. Element catalogue and parameter semantics

| Product | Selected sourced inputs / units and meaning | Outputs / missing depth |
| --- | --- | --- |
| HelioScope | Weather irradiance W/m², air temperature °C, wind m/s; horizon angle degrees; module/inverter characterisations and loss assumptions [HS2, HS4] | Hourly grid_power and loss-stage quantities [HS4]; exact bypass/half-cell solver parameters not yet traced |
| SAM | Detailed PV requires component specifications, module/inverter counts and layout/loss choices [SM2]; SDK variable metadata is the authoritative unit/type route [SM3] | SSC module output fields, annual/timestep electrical performance; not every parameter documented in this inventory |
| PV*SOL | Manufacturer/low-light module characteristic parameters [VS4], inverter efficiency/MPP constraints [VS6], climate and load/system type [VS3] | Yield/economic outputs [VS7], export units with each selected data point [VS9]; full parameter catalogue remains U |
| PlantPredict | Module effective irradiance, temperature, diode parameters, wiring resistance [PP4]; block/array/inverter/DC field association [PP5]; uncertainty percentages [PP7] | Stage results and energy at interconnection [PP8]; exact current-field units need variable-by-variable import audit |

Common Quantic proposal (I): data objects should distinguish a reusable equipment
type, installed count/topology, geometry and run assumptions. Separate irradiance
W/m², irradiation Wh/m², average power W and integrated energy Wh; preserve each
source's interval/area conventions before aggregation. No contract changed here.

## 5. Studies and modules: shared capability table

These 14 rows are scoped evidence, not a league table. A cell proves only its stated
subset. PVsyst column references the companion dossier.

| ID | Capability | PVsyst | HelioScope | SAM | PV*SOL | PlantPredict |
| --- | --- | --- | --- | --- | --- | --- |
| PV-C01 | Variant/case assumptions | S project/VCi [PV6] | S designs/conditions [HS2] | S case/code export [SM3] | S system configuration [VS3] | S predictions/hierarchy [PP5,PP7] |
| PV-C02 | Weather and interval handling | S weather/time shifts [PV8,PV9] | S imported weather/hourly results [HS2,HS4] | S timestep model/API [SM3]; detailed source convention U here | S hourly/minute selection [VS3] | S sub-hourly advertised [PP2]; immutable build U |
| PV-C03 | Transposition | S Hay/Perez [PV10,PV11] | S Hay/Perez [HS2] | U model choices not traced in this pass | S Hay-Davies/Liu-Jordan/Klucher [VS5] | S model choices [PP6] |
| PV-C04 | Horizon / distant shade | S [PV12] | S horizon profile [HS2] | S shading options [SM2]; separate horizon detail U | S horizon input [VS3]; detailed method U here | S horizon model [PP3] |
| PV-C05 | Near shade geometry | S 3D scene [PV12,PV13] | S obstructions [HS6] | S shading options [SM2]; full arbitrary 3D U here | S premium 3D; other edition 2D [VS1] | S site 3D/row models [PP3] |
| PV-C06 | Electrical mismatch due to shade | S layout/partition alternatives [PV13,PV14] | S electrical mismatch stages [HS3] | U detailed algorithm not traced | S module curves [VS4]; shade coupling U here | S linear/fractional/step-fractional options [PP3] |
| PV-C07 | Module I-V / performance | S one-diode family [PV15,PV16] | S PAN characterisation [HS2]; exact solver U | S detailed module options [SM2] | S empirical/two-diode [VS4] | S diode/extensions [PP4] |
| PV-C08 | Temperature | S steady-state plus inertia [PV17,PV18] | S Sandia/diffusion [HS2] | S module temperature effect [SM2]; precise choice U here | U thermal algorithm not read | S temperature input/model stage [PP4] |
| PV-C09 | Inverter efficiency and limits | S [PV19,PV20] | S constrained DC/AC output [HS3] | S separate inverter model [SM2] | S efficiency/MPPT constraints [VS6] | S DC-AC model stage [PP4]; current details U |
| PV-C10 | Bifacial | S constrained 2D [PV26] | S fixed/tracker subset [HS2] | U scope not read here | S listed feature [VS7 navigation]; detailed method U | U rear algorithm not read here |
| PV-C11 | Annual energy and staged losses | S [PV21-PV23] | S report and CSV [HS3,HS4] | S detailed PV losses/output [SM2] | S results [VS7] | S P50 loss tree [PP8] |
| PV-C12 | P50/P90 | S annual Gaussian assumptions [PV24] | S Pro/Enterprise probability [HS1,HS3]; algorithm U | U annual quantile workflow not read | S full-feed-in profitability scope [VS8] | S P-values/user uncertainty [PP7] |
| PV-C13 | Programmatic runs | S separately licensed CLI [PV3,PV25] | U public API not established | S SSC/PySAM/code generation [SM3] | U automation API not established | S REST/Python advertised, exact entitlement conflicting [PP2] |
| PV-C14 | Reusable results/exchange | S CLI CSV/report, internal-file caveat [PV7,PV25] | S PDF/hourly CSV [HS3,HS4] | S generated inputs/programs [SM3] | S overview JSON/time CSV [VS9] | S PVsyst import workflow, loss tree/nodal results [PP8,PP9]; losslessness U |

Important differences: PV*SOL documents an empirical curve model or two-diode model,
not simply "the same diode engine as PVsyst" [VS4]. Its bankability tool changes
profitability using an exceedance choice with a full-feed-in scope [VS8]. HelioScope
probability is plan-qualified [HS1, HS3]. PlantPredict distinguishes geometric shade
from electrical shade effects and its published DC overview applies some reductions
before the diode solve [PP3, PP4]. These differences require intermediate-stage
comparison, not just annual-energy matching (I).

## 6. Workflow, reporting, automation and exchange

| Product | S documented path | Boundary |
| --- | --- | --- |
| HelioScope | Choose design/Condition Set, run simulation, inspect PDF report and hourly CSV [HS2-HS4] | CSV is hour-beginning and uses power units for hourly intervals [HS4]. Conversion to smaller intervals is not new measured variability (I) |
| SAM | Select performance/equipment inputs, use desktop model, generate a complete SDK program/input set or use PySAM [SM2,SM3] | SDK configuration and library version must match. No whole-app UI clone implied |
| PV*SOL | Select system/climate/time resolution, configure equipment, simulate, inspect monthly/technical/economic results [VS3,VS7]; export overview JSON and selected time-series CSV [VS9] | Finer exported intervals depend on minute-resolution simulation. CSV separator/decimal settings matter [VS9] |
| PlantPredict | Build hierarchy/prediction, configure uncertainty, inspect loss tree [PP5,PP7,PP8]; public PVsyst import workflow [PP9] and REST/Python marketing [PP2] | An importer workflow is not a guarantee of preserving every PVsyst field. The pricing page contradicts itself on API inclusion; contract verification required |

## 7. User value and complaints

No independent representative user survey was read. Strengths below are our
inferences, not aggregated sentiment: HelioScope makes assumptions visible beside
layout results [HS2,HS3]; SAM exposes a programmable calculation core [SM3]; PV*SOL
connects yield, loads and economics [VS3,VS7]; PlantPredict exposes model/loss
documentation [PP3,PP8].

One concrete vendor-acknowledged limitation: HelioScope's March 2026 wire-length note
says field-segment vertical height is not included and describes a manual workaround
[HS5]. Treat it as a geometry/quantity-survey caveat, not evidence of all wire losses
being wrong. Current software limitation frequency and user satisfaction remain U.
Vendor "bankable" wording [PP1] is not our independent validation result.

## 8. Engines implied, open candidates and books

Architecture below is I, derived from the sourced studies above. Library API presence
is S; complete numerical parity with any product is U.

| Responsibility | Public open candidate coverage | What Quantic still needs |
| --- | --- | --- |
| Weather to PV power | pvlib ModelChain accepts weather time series, system and location and exposes selectable transposition/DC/AC/AOI/spectral/temperature models [OS1] | Explicit model selection, timezone/interval QA, dataset rights and reproducible weather manifest; no silent model inference |
| Module parameter model | pvlib calcparams_pvsyst returns single-diode parameters from effective irradiance and cell temperature and explicitly describes a **PVsyst v6** model [OS2] | Current-v8 technology/thermal/fit differences, original sweep fixtures, manufacturer parameter provenance |
| Inverter and temperature choices | ModelChain lists Sandia/ADR/PVWatts AC and SAPM/PVsyst/Faiman/Fuentes/NOCT-SAM temperature options [OS1] | Multi-MPPT/constraint/current-limit and thermal-inertia equivalence separately tested, not inferred from matching model names |
| Detailed yield / reduced preliminary model | SAM/SSC exposes detailed PV with separate components and PVWatts as a simpler route [SM2,SM3] | Do not use reduced-model defaults as site evidence; distinguish performance module, financial model and API version |
| Shadow geometry / electrical mismatch | Peer help establishes separate geometry, partition and electrical behaviours [PV13,PP3] | A complete scene editor, robust geometry and current half-cell/bypass coupling are not established by basic ModelChain; design and validate independently |
| Loss ledger and uncertainty | Reports expose staged quantities [HS3,PP8]; uncertainty tools require assumptions [PV24,VS8,PP7] | Original stage ledger, correct denominators and intervals; correlated uncertainty/lifetime treatment needs a sourced method |

### Actual licence files, read 2026-10-18

| Candidate | Licence evidence / exact file blob | Conditions / unresolved component scope |
| --- | --- | --- |
| pvlib Python | BSD-3-Clause [OS3], blob e66a4aa98ebef6b9ef2926f4ce01f8b725f70950 | Retain notices/non-endorsement; no automatic grant for weather, PAN files, third-party models or dependencies |
| SSC | BSD-3-Clause [OS4], blob 7857d8d8df93252977a67c6a725e6f4b2d4726b5 | README [OS5] explicitly lists bundled NLopt/lp_solve LGPL and splinter MPL terms. Exact build/linking/component obligations require review before redistribution |
| SAM application | BSD-3-Clause [SM4], same licence blob as SSC above | Application, SSC, wrappers, optional libraries and datasets require separate inventory; no binary installed here |

These are current upstream file reads, not a pinned-release or full binary licence
audit. No GPL import or dependency addition is performed. PySAM's specific release
licence/dependency set remains a separate pre-build check.

Owned book crosswalk: existing [power library map](../power/notes/engines-library-map.md)
identifies **Masters 2004** as owned. Publisher metadata [BK1] confirms title/year
and the PV materials/electrical-characteristics chapter, pp. 445-504. It is a
physics-verification lead, not authority for present vendor defaults or a copied
worked example. Semiconductor, solar geometry and system-yield methods should be
page-verified in the owned edition when implementation is authorised. Modern
bifacial geometry, current module technologies, uncertainty and model updates need
their own papers. No book chapter text or figure was read/copied in this WP.

## 9. Gaps and closure routes

| Gap | Unresolved issue / closure evidence |
| --- | --- |
| PG1 | Immutable HelioScope/PlantPredict engine build and exact entitlement; capture licensed run metadata/order terms before comparison, not marketing-page inference |
| PG2 | SAM/SSC current binary versus model source/version and PySAM release matching; inspect exact chosen build, not older NREL download snippets |
| PG3 | PV*SOL platform/version requirements, exact shade and thermal implementation; dedicated help/requirements pages and original runtime fixtures needed |
| PG4 | Independent user evidence lacking. Vendor support caveats are not survey or performance measurements |
| PG5 | Dataset/component rights, manufacturer characterisations and current weather-provider terms remain per-file checks; no library-wide assumed grant |
| PG6 | Full bypass/half-cell/optimiser/multi-MPPT/bifacial and irregular terrain parity needs public methods plus stage-by-stage original validation |
| PG7 | Battery dispatch/lifetime/financial details not exhaustively researched; dedicated sources and original scenarios required before feature claims |
| PG8 | Product import/export losses, arbitrary field coverage and diagram semantics not tested. Use a loss ledger, retain unresolved input and compare quantities, not file counts |
| PG9 | Electrical faults, grounding, dynamic grid response and Zambian connection acceptance remain separate power-engine studies; PV yield is not a grid certificate |

No reviewed tool was executed and no annual yield accuracy or product superiority
is asserted. Gaps name bounded research or access needs; they are not proof of
feature absence.
