# PV engine inventory and independent validation boundaries

WP-2.26, ChatGPT, 2026-10-18. The engine split is I, inferred from sourced product
functions; it is not a recovered commercial architecture. Each engine has a
source, matrix scope and independent acceptance need. None is newly implemented.
All PVC IDs refer to the [matrix](parity-matrix.md). All product source IDs resolve
in [PVsyst](pvsyst.md#2-sources) or [peer sources](other-products.md#2-sources).

## Engines and open candidates

| ID | Original responsibility / matrix scope | Documentary basis | Open base to evaluate and validation gate |
| --- | --- | --- | --- |
| PVE-01 | Weather ingestion, units, chronology and provenance; PVC-002/003/052/059 | PV8/PV50; RD1-RD22 in resource-data.md | pvlib IO functions are candidates, not a data licence. Independently test interval energy, UTC/solar/civil distinctions, missing data and source version |
| PVE-02 | Solar position, transposition, incidence and spectrum; PVC-004/005/017 | PV10/PV11/PV21/PV48, VS5, PP6 | pvlib selectable models; validate angle conventions and components separately. Named Perez variants and coefficients are versioned |
| PVE-03 | Scene geometry, horizon and front optical shadow; PVC-006-008/056 | PV12/PV48/PV52-PV54, HS6, PP3 | Independent geometry plus suitable open numerical primitives; full arbitrary 3D engine not established by basic ModelChain. Compare analytical authored occluders and finite edges |
| PVE-04 | Tracker geometry/control and rear irradiance; PVC-011-014/056 | PV26/PV28-PV32, HS2, PP3 | pvlib tracking/bifacial methods require individual review. 2D regular rows, finite edges, terrain and actual tracker law are distinct validation cases |
| PVE-05 | Module parameter fitting and I-V solution; PVC-015/016/020/054 | PV15/PV16/PV35, VS4, PP4 | pvlib/SSC candidate models. Parameter identifiability, technology limits and measured sweeps required. Datasheet STC points alone do not validate all low-light/reverse behavior |
| PVE-06 | Shade/mismatch electrical assembly and MPPT; PVC-009/010/021/024/027/040 | PV13/PV14/PV35/PV46/PV47, PP3 | Author independent small circuits before large aggregate models. Geometry fraction, electrical partition, bypass state and optimiser behavior cannot be substituted silently |
| PVE-07 | Cell/module thermal state; PVC-018/019 | PV17/PV18/PV45, HS2, PP4 | pvlib steady/transient candidates need exact function review. Verify coefficients, mass/wind meaning, initial history and interval average against independent integration and measurement |
| PVE-08 | Inverter efficiency, operating constraints and sharing; PVC-025-027/031 | PV19/PV20/PV42/PV46/PV47, VS6 | pvlib/SSC candidates cover subsets. Distinguish DC input constraints, common AC rating, reactive/apparent limits, export curtailment and off-MPP operation |
| PVE-09 | Soiling, ageing, wiring and delivery ledger; PVC-020-024/028-030/041/051 | PV21-PV23/PV33-PV35/PV37, HS5, PP8 | Independent ledger with selected pvlib/SSC functions. No single annual percentage represents spatial dust, degradation dispersion or current-dependent wiring losses |
| PVE-10 | Demand/storage/grid availability and dispatch; PVC-032-038 | PV36-PV41, VS3 | SSC storage is a candidate requiring dedicated method/source review. Define topology, state bounds, converter limits, load/export priority and unserved demand before optimization |
| PVE-11 | Pumping/DC-grid/other specialised energy use; PVC-039/040/060 | PV51; PVG6/PG6 gaps | No qualified complete open base selected here. Obtain hydraulic/optimiser/DC-grid equations and manufacturer characterization before coverage claims |
| PVE-12 | Annual variability, uncertainty and lifetime statistics; PVC-023/024/042 | PV24/PV34, PP7, VS8; RD16 scope | Independent statistical implementation. Distinguish annual distribution from uncertainty in long-term mean, covariance from independence, warranty from expected degradation |
| PVE-13 | Economics and tariffs; PVC-043/055 | PV51, SM3, VS7/VS8 | SSC financial modules are candidates, with exact configuration/version needed. Discounting, tariff rules and battery replacement are not power-physics validation |
| PVE-14 | Scenario orchestration, interface, exchange and reporting; PVC-001/044-050/053/054/057-059 | PV6/PV7/PV25/PV43/PV44/PV50, SM3, VS9, PP9 | Existing Quantic metadata/runner infrastructure is partial foundation only. Preserve IDs, files, licence capabilities and loss manifests; reject false success from unavailable engines |

Every engine's book route is the matrix's B1 or B0. Masters 2004 is an owned
fundamentals lead, not proof of current vendor numerics. Exact page verification
and modern references for bifacial, thermal adaptation, uncertainty and dispatch
remain pre-implementation gates. Existing power books may support network and
machine studies but cannot verify a PV cell/shading model by association.

## Dated licence reads and source/version limits

The actual files below were read on 2026-10-18 in this WP. No source code,
library or data was copied into Quantic and no dependency changed.

| Candidate | Actual primary licence/source file and inspected blob | Reuse boundary |
| --- | --- | --- |
| pvlib Python | [LICENSE](https://github.com/pvlib/pvlib-python/blob/main/LICENSE), e66a4aa98ebef6b9ef2926f4ce01f8b725f70950, BSD-3-Clause | Preserve notices/non-endorsement. Exact dependency/build and dataset rights separate |
| SSC | [LICENSE](https://github.com/NatLabRockies/ssc/blob/patch/LICENSE), 7857d8d8df93252977a67c6a725e6f4b2d4726b5, BSD-3-Clause | [README](https://github.com/NatLabRockies/ssc/blob/patch/README.md), 48c16cd8243cd9a0bee65f414218ffa0c77586f1, names bundled NLopt/lp_solve LGPL and splinter MPL components. Full binary/build audit still needed |
| SAM application | [LICENSE](https://github.com/NatLabRockies/SAM/blob/patch/LICENSE), same licence blob 7857d8d8df93252977a67c6a725e6f4b2d4726b5 | Open application licence is distinct from SSC, wrappers, optional dependencies, weather and component grants |

Current [pvlib ModelChain docs](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.modelchain.ModelChain.html)
identify 0.16.1 and selectable DC/AC/temperature/optical models. They do not establish
full scene, current-sharing, dispatch or numerical parity with PVsyst 8. The named
PVsyst parameter function explicitly references v6 (OS2). SAM's
[PV overview](https://sam.nlr.gov/photovoltaic.html) distinguishes detailed PV from
PVWatts; its [SDK page](https://sam.nlr.gov/software-development-kit-sdk.html)
describes core simulation and programmatic access. Function availability is S;
equivalence to a full product or site measurement is U.

The repository pins pvlib 0.16.1 but its reserved PV adapter does not import it.
No wrapper or binary has been qualified for these proposed engines. GPL packages
must remain separate processes under AGENTS.md; LGPL/MPL components need their
own exact-release/linking assessment. No broad all-permissive stack assertion.

## Proposed dependency order (I)

First qualify PVE-01 and PVE-14 provenance/units, then validate simple PVE-02/05/07/08
chains with explicit losses. Add PVE-03/04/06 geometry and mismatch with independent
small cases; add PVE-10 only with trusted mine demand/outage and storage inputs.
Use PVE-12/13 after the physics, resource basis and financial boundary are explicit.
This is research prioritization, not build approval; WP-2.5 stays parked.

Counter-checks must not compare the same backend against itself. Use authored
analytical cases, independent circuit/thermal integration, justified reference
equations and calibrated site observations. Record reference provenance and
tolerances before accepting results. No such tests were run here.
