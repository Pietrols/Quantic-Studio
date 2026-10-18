# PV capability and evidence matrix

WP-2.26, ChatGPT, 2026-10-18. Research scope: Zambian utility-scale and mine-site
solar, with residential, standalone and pumping capabilities retained for coverage.
Every product cell starts S, I or U. S is documentary support for the stated
subset; U is unresolved, never feature absence. No commercial runtime was tested.
The products are PVsyst, HelioScope, SAM, PV*SOL and PlantPredict in that order.

Source IDs PV1-PV55 resolve in [PVsyst](pvsyst.md#2-sources); HS, SM, VS, PP and
OS IDs resolve in [peer sources](other-products.md#2-sources). Resource IDs resolve
in [resource-data.md](resource-data.md#7-primary-sources-and-exact-read-scope).
Source dates are 2026-10-18. Qualifiers survive the move from the dossiers.

Quantic column **N** means no implemented end-to-end PV capability on main at
020367a. The source is [UnavailablePVEngine](../../../packages/py/qe_pv/src/qe_pv/engine.py),
which reports ENGINE_UNAVAILABLE; the adapter boundary is reserved. Schemas,
service routing and the shared runner do not constitute a numerical PV engine.
This is a source inspection, not a runtime test. All rows remain build proposals.

Book key **B1**: owned Masters, Renewable and Efficient Electric Power Systems,
2004, identified by the existing [library map](../power/notes/engines-library-map.md).
PV electrical fundamentals are a verification lead; exact pages/equations must
be checked before implementation. B1 does not verify current product behavior,
modern bifacial models, dispatch, uncertainty or standards. **B0**: no applicable
owned-book verification established; use the named primary source and record a
reference gap. This explicit gap is preferable to inventing a verifying book.

## Matrix

| ID | Capability and exact comparison scope | PVsyst | HelioScope | SAM | PV*SOL | PlantPredict | Quantic | Book |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PVC-001 | Reusable project / case / condition assumptions | S PRJ/variants [PV6] | S design/conditions [HS2] | S cases/code export [SM3] | S configuration [VS3] | S prediction/hierarchy [PP5,PP7] | N | B0 |
| PVC-002 | Weather source intake | S weather files [PV6,PV9] | S condition weather [HS2] | S model weather [SM2] | S climate selection [VS3] | S prediction inputs [PP2]; source detail U | N | B1 |
| PVC-003 | Interval and time-reference handling | S explicit convention [PV8] | S hour-beginning CSV [HS4] | S timestep interface [SM3]; convention U | S hourly/minute [VS3] | S sub-hourly offer [PP2]; convention U | N | B0 |
| PVC-004 | Transposition | S Hay/Perez/version distinction [PV10,PV11] | S Hay/Perez [HS2] | U precise model not traced | S named model options [VS5] | S documented options [PP6] | N | B1 |
| PVC-005 | Horizon / distant shading | S beam/diffuse treatment [PV48] | S horizon conditions [HS2] | S shade options [SM2]; horizon algorithm U | S horizon input [VS3]; algorithm U | S horizon treatment [PP3] | N | B1 |
| PVC-006 | Near-shading geometry | S scene/dashboard [PV12,PV52] | S obstructions [HS6] | S shade options [SM2]; arbitrary 3D U | S premium 3D/other 2D [VS1] | S row/site models [PP3] | N | B0 |
| PVC-007 | External CAD geometry intake | S documented route [PV54]; field preservation U | U import coverage not traced | U import coverage not traced | U import coverage not traced | U import coverage not traced | N | B0 |
| PVC-008 | Irradiance-only shadow calculation | S linear option [PV52] | S geometric shade [HS6] | U precise algorithm not traced | U precise algorithm not traced | S linear shade [PP3] | N | B0 |
| PVC-009 | Partition electrical shade approximation | S partitions/fraction [PV14] | U partition equivalence not traced | U partition equivalence not traced | U partition equivalence not traced | S fractional/step options [PP3]; equivalence U | N | B0 |
| PVC-010 | Detailed shade-to-electrical mapping | S Module Layout [PV13] | S mismatch stage [HS3]; solver detail U | U detailed coupling not traced | S module curves [VS4]; shade coupling U | S electrical shade options [PP3] | N | B1 |
| PVC-011 | Tracker geometry / operation | S orientation/tracker [PV29,PV31] | S tracker condition subset [HS2] | U exact tracker scope not traced | U exact tracker scope not traced | S row/tracker scope [PP3] | N | B1 |
| PVC-012 | Backtracking control assumptions | S common angle/reference GCR [PV31,PV32] | U exact law not traced | U exact law not traced | U exact law not traced | U exact law not traced | N | B0 |
| PVC-013 | Bifacial production | S constrained 2D/multiple orientation [PV26,PV28] | S fixed/tracker subset [HS2] | U scope not traced | S feature listed [VS7]; algorithm U | U rear model not traced | N | B0 |
| PVC-014 | Ground albedo variation | S constant/monthly/time-series [PV28] | U temporal scope not traced | U temporal scope not traced | U temporal scope not traced | U temporal scope not traced | N | B1 |
| PVC-015 | Module electrical performance | S one-diode family [PV15] | S PAN model [HS2]; equations U | S detailed module choices [SM2] | S empirical/two-diode [VS4] | S diode/extensions [PP4] | N | B1 |
| PVC-016 | Parameter fitting / characterisation | S extra parameters beyond datasheet [PV16]; full fit U | U exact fit not traced | S component model choices [SM2]; fitting U | S curve characterisation [VS4] | S model parameters [PP4]; fitting U | N | B1 |
| PVC-017 | Optical/IAM/spectral loss staging | S optical correction chain [PV21] | S condition/report loss stages [HS2,HS3]; exact models U | S detailed losses [SM2]; exact models U | S irradiance model [VS5]; all corrections U | S DC preprocessing [PP4]; all corrections U | N | B1 |
| PVC-018 | Steady thermal conversion | S fitted U-values [PV18] | S temperature choices [HS2] | S temperature effects [SM2] | U algorithm not read | S temperature stage [PP4] | N | B1 |
| PVC-019 | Thermal inertia / interval averaging | S modified Prilliman [PV45] | U transient model not traced | U transient model not traced | U transient model not traced | U transient model not traced | N | B0 |
| PVC-020 | Module quality / initial degradation | S loss chain [PV21] | S report/conditions [HS2,HS3]; exact LID U | S losses [SM2]; exact LID U | U detail not traced | S DC loss staging [PP4]; exact LID U | N | B1 |
| PVC-021 | Module/string mismatch distinct from shade | S I-V/dispersion [PV35] | S mismatch stage [HS3] | U algorithm not traced | S module curves [VS4]; array mismatch U | S DC mismatch stage [PP4] | N | B1 |
| PVC-022 | Soiling and uneven-dirt assumptions | S monthly irradiance loss [PV33,PV35] | S loss assumptions [HS2]; spatial law U | S detailed losses [SM2]; spatial law U | U detail not traced | S DC reductions [PP4]; spatial law U | N | B0 |
| PVC-023 | Long-term module degradation | S selected year/mean [PV34] | U lifetime treatment not traced | U lifetime method not traced | U lifetime method not traced | U lifetime method not traced | N | B1 |
| PVC-024 | Degradation dispersion and mismatch | S Monte Carlo assumptions [PV34] | U not traced | U not traced | U not traced | U not traced | N | B0 |
| PVC-025 | Inverter conversion efficiency | S power/voltage curve [PV19] | S DC/AC stages [HS3] | S separate inverter [SM2] | S efficiency [VS6] | S conversion stage [PP4]; detail U | N | B1 |
| PVC-026 | Input voltage/current/power limits | S operating point constraints [PV20] | S constrained output [HS3]; individual limits U | S inverter model [SM2]; individual limits U | S MPPT constraints [VS6] | S DC stage [PP4]; individual limits U | N | B1 |
| PVC-027 | Multi-MPPT identity / power sharing | S configurable [PV46,PV47] | U exact sharing not traced | U exact sharing not traced | U exact sharing not traced | S inverter hierarchy [PP5]; sharing U | N | B0 |
| PVC-028 | DC wiring losses | S chain [PV21] | S wire/report stage [HS3,HS5] | S losses [SM2] | U exact method not traced | S resistance input [PP4] | N | B1 |
| PVC-029 | AC/transformer delivery losses | S delivery chain [PV22,PV42] | S report boundary [HS3]; transformer detail U | S losses [SM2]; transformer detail U | U detail not traced | S interconnection loss tree [PP8] | N | B1 |
| PVC-030 | Auxiliary / unavailability staging | S delivery chain [PV22,PV37] | U detailed allocation not traced | S loss choices [SM2]; allocation U | U detailed allocation not traced | S loss tree [PP8]; allocation U | N | B0 |
| PVC-031 | Grid export kW/kVA boundary | S MPPT ceilings/delivery boundary [PV42] | U algorithm not traced | U algorithm not traced | U algorithm not traced | U algorithm not traced | N | B0 |
| PVC-032 | Demand / self-consumption energy | S user needs [PV36,PV37] | U scope not traced | U scope not traced | S load/system context [VS3,VS7] | U scope not traced | N | B1 |
| PVC-033 | Battery/converter topology and state | S generic architecture [PV36,PV41] | U scope not traced | U detailed storage not traced | S system context [VS3]; battery detail U | U scope not traced | N | B0 |
| PVC-034 | Battery self-consumption dispatch | S surplus/deficit, no battery export [PV37] | U not traced | U not traced | U not traced | U not traced | N | B0 |
| PVC-035 | Battery export peak shaving | S export-oriented [PV38] | U not traced | U not traced | U not traced | U not traced | N | B0 |
| PVC-036 | Battery scheduled power shifting | S specified charge/discharge [PV39] | U not traced | U not traced | U not traced | U not traced | N | B0 |
| PVC-037 | Weak-grid/outage energy balance | S availability/load profiles [PV40] | U not traced | U not traced | U not traced | U not traced | N | B0 |
| PVC-038 | Standalone sizing / unmet load | S separate path [PV51]; full dispatch U | U not traced | U not traced | U not traced | U not traced | N | B1 |
| PVC-039 | Solar pumping / unmet water demand | S separate path [PV51]; detailed solver U | U not traced | U not traced | U not traced | U not traced | N | B1 |
| PVC-040 | Optimiser-specific modeling | U full model not reviewed, PVG6 | U full model not reviewed, PG6 | U full model not reviewed, PG6 | U full model not reviewed, PG6 | U full model not reviewed, PG6 | N | B0 |
| PVC-041 | Annual energy / staged loss ledger | S loss diagram [PV21-PV23] | S report [HS3] | S detailed PV output [SM2] | S results [VS7] | S P50 loss tree [PP8] | N | B1 |
| PVC-042 | Annual exceedance / P50-P90 | S Gaussian assumptions [PV24] | S plan-qualified [HS1,HS3]; method U | U quantile workflow not traced | S full-feed-in profitability [VS8] | S user uncertainty/P-values [PP7] | N | B0 |
| PVC-043 | Financial/lifetime interpretation | S economic path [PV51]; full method U | U detailed finance not traced | S financial core [SM3]; exact model U | S finance/results [VS7,VS8] | U detailed finance not traced | N | B0 |
| PVC-044 | Human-readable engineering report | S report/losses [PV23,PV51] | S PDF report [HS3] | U report details not read | S results/presentation [VS7,VS9] | S result tree [PP8]; PDF detail U | N | B0 |
| PVC-045 | Time-series result export | S CLI outputs [PV25] | S hourly CSV [HS4] | S SDK outputs [SM3] | S selected CSV [VS9] | S nodal outputs [PP8]; format detail U | N | B0 |
| PVC-046 | Project import / structured exchange | S files/exports [PV6,PV7]; internal schema caveat | U complete project exchange not traced | S code/input export [SM3]; round trip U | S overview JSON [VS9]; round trip U | S PVsyst import [PP9]; losslessness U | N | B0 |
| PVC-047 | Programmatic simulation | S separate CLI [PV3,PV25] | U API not established | S SSC/PySAM [SM3] | U automation API not established | S API advertised [PP2]; entitlement contradictory | N | B0 |
| PVC-048 | Batch / parametric comparison | S CSV batch/weather resolution [PV43] | S condition/design comparisons [HS2,HS3]; batch API U | S generated programmes [SM3]; GUI batch U | U batch not traced | S prediction workflow [PP7,PP8]; batch API U | N | B0 |
| PVC-049 | Measured-data validation workflow | S import/compare [PV50] | U workflow not traced | U workflow not traced | U workflow not traced | U workflow not traced | N | B0 |
| PVC-050 | Electrical single-line / layout grouping | S grid-only, storage excluded [PV44] | U electrical diagram scope not traced | U electrical diagram scope not traced | U electrical diagram scope not traced | S plant hierarchy [PP5]; diagram equivalence U | N | B0 |
| PVC-051 | Wire-length quantity estimation | U full take-off coverage not traced | S documented vertical-height caveat [HS5] | U not traced | U not traced | U not traced | N | B0 |
| PVC-052 | Weather quality / time provenance | S time/measurement checks [PV8,PV50] | S recorded assumptions [HS2,HS4]; raw-QC detail U | S SDK inputs [SM3]; raw-QC detail U | S climate selection [VS3]; raw-QC detail U | S inputs [PP2]; raw-QC detail U | N | B0 |
| PVC-053 | Input warnings and model applicability | S blocking/acceptable warnings [PV50] | U precise diagnostics not traced | U precise diagnostics not traced | U precise diagnostics not traced | U precise diagnostics not traced | N | B0 |
| PVC-054 | Reusable component definitions | S PAN/OND/etc. [PV6] | S component/condition choices [HS2] | S module/inverter choices [SM2] | S manufacturer models [VS4,VS6] | S component hierarchy [PP4,PP5] | N | B1 |
| PVC-055 | Reduced preliminary model | S monthly preliminary sizing [PV51] | U reduced engine not traced | S PVWatts versus detailed PV [SM2] | U reduced engine not traced | U reduced engine not traced | N | B1 |
| PVC-056 | Terrain/nonuniform tracker applicability | S reference-geometry caveats [PV31,PV32] | U terrain control law not traced | U terrain control law not traced | U terrain control law not traced | S 3D shade [PP3]; controller law U | N | B0 |
| PVC-057 | Data/model redistribution rights | S separate editions/CLI [PV2,PV3]; component/weather grant U | S plan terms [HS1]; dataset grant U | S source licence [SM4]; dataset grant U | S subscription offer [VS2]; dataset grant U | S paid service [PP2]; dataset grant U | N | B0 |
| PVC-058 | Calculation-core reuse boundary | U proprietary core unavailable | U proprietary core unavailable | S SSC SDK [SM3]; component terms separate | U proprietary core unavailable | U proprietary core unavailable | N | B0 |
| PVC-059 | Release / run provenance | S release list/files [PV1,PV7]; run hash U | S V2/Classic [HS2]; immutable build U | S version/download [SM1]; executed binary U | S dated release offer [VS1]; executed binary U | S version-qualified help [PP3]; immutable build U | N | B0 |
| PVC-060 | DC-grid specialised system path | S separate path [PV51]; detailed traction/network model U | U not traced | U not traced | U not traced | U not traced | N | B0 |

## Coverage reconciliation and open evidence

The 14 original peer rows PV-C01 to PV-C14 map respectively to PVC-001,
002/003/052, 004, 005, 006/007, 008-010/021, 015/016, 018/019,
025-027, 013/014, 041/044/045, 042/043, 047/048, and 046/059.
Peer architecture/element/workflow differences additionally map to PVC-050/051/054.
The PVsyst deepening adds PVC-011/012/017/020/022-024/028-040/049/053/056.
Edition, licence and open-core questions map to PVC-057/058/059.
The separately documented DC-grid path maps to PVC-060.
User satisfaction is an evidence-quality discussion, not a numerical capability;
its unavailability is retained in both dossiers rather than scored as absence.

No product cell is promoted on analogy with another product. Cells tagged S with
an internal U qualifier support only the stated subset. U rows, B0 references and
unverified B1 pages are concrete research debt. The [engine inventory](engines.md)
and [PV requirements](requirements.md) turn these distinctions into original,
testable proposals. Product execution, full project round trips and bankability
of any particular site remain U.
