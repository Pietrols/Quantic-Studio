# PVsyst

WP-2.23, ChatGPT, accessed 2026-10-18. All product descriptions below are S from
public documentation unless marked I/U. No application was installed or run.
No weather/component library, source project or paid reference was copied.
Deepened under WP-2.25 on 2026-10-18. Current public help takes precedence over
historical v7 descriptions where the two differ. This remains documentary research.

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

The public overview distinguishes preliminary monthly sizing from detailed hourly
or sub-hourly project simulations [PV51]. Grid-connected, stand-alone, pumping
and DC-grid paths have different loads, components and outputs; the presence of
one path does not establish another's storage or uncertainty behavior. The desktop,
CLI and weather-provider entitlements must be recorded independently [PV2-PV4].
The Meteonorm service currently markets a new web/Climate API generation; an
embedded weather generator in an existing PVsyst installation does not prove
that its data release, licence or algorithms match that service. See the dated
[resource inventory](resource-data.md) before choosing an input (I).

For version comparison (I), record installer/build, licence edition, component
file revision, weather hash, simulation interval and enabled model settings.
A report headed PVsyst 8 is insufficient to identify all of these. Exportability
of a report does not grant redistribution rights over its embedded weather or
component data. Exact seat, offline activation, virtualisation and server rights
remain the purchased contract's questions; the public pages establish no blanket
permission for a hosted Quantic service [PV2-PV4].

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
| PV28 | Bifacial procedure, current help | https://www.pvsyst.com/help/project-design/bifacial-systems/bifacial-systems-procedure.html |
| PV29 | 2D unlimited tracker backside model, help | https://www.pvsyst.com/help/project-design/bifacial-systems/bifacial-system-2-dimensional-unlimited-trackers.html |
| PV30 | 2D unlimited shed backside model, help | https://www.pvsyst.com/help/project-design/bifacial-systems/bifacial-system-2-dimensional-unlimited-sheds.html |
| PV31 | Backtracking strategy, help | https://www.pvsyst.com/help/project-design/shadings/backtracking-strategy/index.html |
| PV32 | Backtracking parameter management, help | https://www.pvsyst.com/help/project-design/shadings/backtracking-strategy/backtracking-parameter-management.html |
| PV33 | Soiling loss, help | https://www.pvsyst.com/help/project-design/array-and-system-losses/soiling-loss.html |
| PV34 | Ageing and module degradation, help | https://www.pvsyst.com/help/project-design/array-and-system-losses/ageing-pv-modules-degradation/index.html |
| PV35 | Array mismatch losses, help | https://www.pvsyst.com/help/project-design/array-and-system-losses/array-mismatch-losses/index.html |
| PV36 | Grid storage overview, help | https://www.pvsyst.com/help/project-design/grid-connected-system-definition/grid-systems-with-storage/index.html |
| PV37 | Storage self-consumption, help | https://www.pvsyst.com/help/project-design/grid-connected-system-definition/grid-systems-with-storage/self-consumption-with-storage.html |
| PV38 | Storage peak shaving, help | https://www.pvsyst.com/help/project-design/grid-connected-system-definition/grid-systems-with-storage/storage-powers-peak-shaving.html |
| PV39 | Storage power shifting, help | https://www.pvsyst.com/help/project-design/grid-connected-system-definition/grid-systems-with-storage/power-shifting-storage.html |
| PV40 | Weak-grid storage and islanding, help | https://www.pvsyst.com/help/project-design/grid-connected-system-definition/grid-systems-with-storage/storage-weak-grid-islanding.html |
| PV41 | Storage architecture, help | https://www.pvsyst.com/help/project-design/grid-connected-system-definition/grid-systems-with-storage/grid-storage-system-architecture.html |
| PV42 | Grid power limitation, help | https://www.pvsyst.com/help/project-design/grid-connected-system-definition/grid-power-limitation.html |
| PV43 | Batch parametric studies, help | https://www.pvsyst.com/help/project-design/simulation/batch-mode-parametric-studies.html |
| PV44 | Single-line diagram, help | https://www.pvsyst.com/help/project-design/grid-connected-system-definition/single-line-diagram.html |
| PV45 | Transient thermal model, help, equations and interval convention inspected | https://www.pvsyst.com/help/project-design/array-and-system-losses/array-thermal-losses/transient-thermal-model.html |
| PV46 | Multi-MPPT definition, help | https://www.pvsyst.com/help/project-design/grid-connected-system-definition/multi-mppt-inverters/index.html |
| PV47 | MPPT power sharing, help | https://www.pvsyst.com/help/project-design/grid-connected-system-definition/multi-mppt-inverters/power-sharing.html |
| PV48 | Far shading / horizon, help | https://www.pvsyst.com/help/project-design/shadings/far-shadings-horizon/index.html |
| PV49 | Simulation weather/irradiance variables, help | https://www.pvsyst.com/help/project-design/results/simulation-variables-meteo-and-irradiations.html |
| PV50 | Measured-data workflow, help | https://www.pvsyst.com/help/measured-data/index.html |
| PV51 | Product overview and study paths, help | https://www.pvsyst.com/help/index.html |
| PV52 | Near-shading main dialog, help | https://www.pvsyst.com/help/project-design/shadings/near-shadings-main-dialog/index.html |
| PV53 | Global scene tools, help | https://www.pvsyst.com/help/project-design/shadings/near-shadings-3d-construction/global-scene-building-tools.html |
| PV54 | CAD scene import, help | https://www.pvsyst.com/help/project-design/shadings/near-shadings-import/sketchup-and-other-cad-software.html |
| PV55 | Vendor validation index, catalogue only | https://www.pvsyst.com/help/validations/index.html |

PV28-PV55 were added/read for WP-2.25. Public help is mutable and sometimes retains
older feature descriptions. The inspected page, scope and retrieval date are
evidence, not proof of the exact behavior of an unrun binary. Reports/PDFs linked
by a catalogue are not treated as fully read validation studies.

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

The model has several identities that must remain distinct (I, grounded in
PV6/PV28/PV46/PV52): a physical module's position; its electrical string and MPPT;
an orientation group; an aggregate homogeneous subarray; a reusable component
definition; and a simulation variant. Joining these by a displayed name alone
would lose important relationships. Shared orientation groups can share a bifacial
definition [PV28], whereas multi-MPPT allocation can connect homogeneous subarrays
to one physical inverter [PV46]. Thus an MPPT count is not an inverter count.

Near-shade scene data belongs to a calculation variant; a scene may also be saved
as SHD for reuse [PV52]. A horizon profile is separately reusable as HOR [PV48].
The single-line view is generated from the variant and represents grouped physical
objects [PV44]. An external CAD scene contributes geometry, not automatically a
verified electrical wiring model [PV54]. For Quantic (I), preserve mappings and
transformations explicitly when importing geometry or cloning a variant.

Weather, albedo, user demand, grid availability and dispatch schedules have
different meanings and references [PV8/PV28/PV36/PV39/PV40]. A repeated monthly
albedo value is not a measured sub-hourly series. Synthetic weather and measured
weather need separate provenance; neither may be silently substituted during a
batch. For comparisons (I), bind all dependent inputs by hash and retain the
sampling convention, missing-data decisions and source licence.

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
| Tracker orientation | Axis and angle convention; width/pitch ratio; reference pair or array; mechanical orientation group | PV31/PV32, same computed angle within an orientation; terrain-specific residual shading needs inspection |
| Rear irradiance | Ground albedo, dimensionless; pitch/width/height, m; number of cross-sectional rows; bifaciality and rear losses | PV28-PV30; table count in cross section is distinct from finite row length |
| Soiling | Monthly attenuation factors applied to irradiance | PV33; no default mining-dust factor inferred from another climate |
| Ageing | Selected operating year, mean module degradation and dispersion | PV34; warranty floor is not the expected average degradation of the array |
| Storage | Battery pack, charge/discharge converter power and efficiency curves, strategy and schedules, load/outage series where required | PV36-PV41; energy capacity, power capability and availability are distinct |
| Export constraint | Limit at inverter or delivery boundary, active kW or apparent kVA, downstream losses | PV42; MPPT allocation and power factor affect what binds |
| Single-line group | Multiplicity, children, DC/AC cable representation and injection point | PV44; this is not proof of a full bus/branch network solver |

An original parameter-review checklist (I) for mine-site studies follows. It
contains no vendor defaults or engineering limits:

- Fix axes, origin, north reference, elevations, tilt and azimuth conventions
  before interpreting a scene. Verify one physical reference direction on export.
- Match the module's electrical subdivision and bypass arrangement to the chosen
  string layout. Keep bifaciality distinct from ground albedo and rear irradiance.
- Attach the inverter's voltage/current/power limits and MPPT sharing configuration
  to a revision of its characterisation, rather than only an AC nameplate.
- Record dust/cleaning observations, module coefficient provenance and degradation
  distributions. A manufacturer warranty is a bound with conditions, not a fitted
  site distribution.
- Identify battery chemistry/characterisation, usable-state bounds, converter
  placement, demand priority, charging source and allowed grid reinjection.
- Tie the export restriction to a physical measurement boundary and units. Keep
  active, reactive and apparent power definitions visible in the report.

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
[PV21/PV51]. Storage and dispatch are deepened below; optimiser, pumping and
financial internals still have named gaps.
No claim of current IEC/IEEE electrical-safety certification follows from a yield run.

### Optical geometry, trackers and bifacial coupling

Far shading uses a horizon profile and a field-wide beam visibility decision;
hourly horizon crossing is weighted before transposition. Its diffuse treatment
integrates the visible sky, and albedo uses a documented approximation with a
user adjustment [PV48]. Nearby obstructions need a scene whose shadow varies over
the collecting area [PV12/PV52]. Horizon data embedded in weather is therefore an
important provenance question: applying another identical obstruction may double
count attenuation (I).

Linear shade models irradiance deficit. The partitions approach approximates
electrical effects; detailed Module Layout uses the actual layout/string mapping
[PV13/PV14/PV52]. These have different assumptions and computational costs.
Electrical shade loss depends on where a shadow falls, how cells/submodules are
connected and which strings share an MPPT; matching shaded area alone does not
establish equivalent power (I from those model distinctions).

Backtracking changes orientation to avoid mutual beam shading. PVsyst does not
optimise its tracking law for diffuse irradiance. It trades electrical shade
against incidence/cosine and other optical effects. The help documents one angle
for every tracker in an orientation, obtained from a reference width/pitch ratio
[PV31]. For built-in arrays the reference selection uses the highest ratio;
independently imported trackers use automatic/custom reference-pair management
[PV32]. A nonuniform scene can therefore require inspection beyond its orientation
label. The separate PR denominator changes with tracker orientation [PV31/PV49];
compare delivered energy as well as PR (I).

The backside calculation uses an approximate unlimited-row cross section for
each eligible orientation, not the full finite 3D scene [PV26/PV29/PV30]. The
procedure permits multiple orientation models, monthly or time-series albedo,
and explicit geometric inputs, but states that fixed east-west bifacial systems
are not currently supported by its assumptions [PV28]. Ground shade, view of sky,
reflected ground irradiance and rear nonuniformity are separate from the front
shade calculation. The mismatch help explicitly leaves the evaluation of its
rear-irradiance mismatch parameter without a reliable general model [PV35].
Do not infer a calibrated rear mismatch factor from an albedo entry (I).

### Losses, ageing and thermal state

Soiling is a monthly irradiance attenuation in the documented basic treatment
[PV33]. This does not predict mine dust deposition, rain cleaning or partial-cell
obscuration from first principles. Uneven dirt can also affect mismatch; the
mismatch help associates different mechanisms with different parts of the model
[PV35]. A Quantic loss ledger must identify whether a supplied estimate already
contains the electrical effect before applying another factor (I).

The ageing tool distinguishes mean module degradation from dispersion between
modules. It evaluates additional mismatch with a Monte Carlo treatment under
stated assumptions about module degradation rates/distribution. A warranty curve
describes a guaranteed individual lower bound, not the expected array mean.
Ageing may reduce inverter overload, so delivered AC energy need not decline by
exactly the module degradation multiplier [PV34]. No numeric degradation rate is
adopted for Zambia.

PV45 now provides a specific public transient-thermal explanation: a modified
Prilliman weighted-history model using wind and module mass per area. PVsyst
adapts start-of-interval temperature to its interval-average convention and changes
the history cutoff. Its help identifies fallback handling for unavailable or
invalid mass. These are product choices, not Quantic defaults. Retain both
steady-state and transient temperatures and the original interval meaning.
The summary notes that displayed temperatures average subarrays/orientations,
although simulation uses their separate temperatures [PV17]. Aggregates alone
cannot validate a particular hot subarray (I).

### Inverter constraints and grid delivery

Multi-MPPT modeling distinguishes independent inputs, nominal power sharing and
special unbalanced inputs [PV46/PV47]. Clipping must be interpreted with the
physical inverter's common output capacity and the individual input limits. An
underused MPPT under an independent-input assumption can change the available
output rating [PV46]. No universal DC:AC ratio or maximum loss percentage is
adopted here.

Grid limits can be specified as active or apparent power. Since v7.3, the help
describes pre-evaluating MPPT power ceilings at each step, accounting for sharing,
temperature, power factor, local use, battery charging and downstream losses.
Most heavily loaded MPPTs are reduced first. It distinguishes the grid-limit
contribution from ordinary inverter overload through an additional calculation
[PV42]. Thus clipping attribution is an algorithm/version question, not merely
subtracting the annual export above a line (I).

### Storage modes and the mine-site interpretation

Current help lists four strategies and simplified sizing guidance [PV36]. These
are not interchangeable optimisers. The following scope is S; the last column is
an original validation question (I), not a tested result.

| Strategy | Documented dispatch scope | Proposed discriminating check |
| --- | --- | --- |
| Self-consumption | Stores PV surplus after demand and serves later demand; battery output is not reinjected. Charge/discharge power and conversion/storage losses apply [PV37] | Shift an identical demand profile relative to solar; account separately for direct use, grid import, battery state and export |
| Peak shaving | Captures PV beyond grid injection limits and later exports it; no internal consumption in this mode [PV38] | Force battery-full and charger-power-limited intervals; distinguish recovered clipping from remaining unused energy |
| Power shifting | Scheduled charging/discharging for grid delivery; selectable fraction, fixed charging power or fixed export. Current help excludes local self-consumption [PV39] | Compare a schedule with a binding export limit; record the reference quantity for the charging fraction |
| Weak-grid recovery | Requires grid-availability and user-load profiles, with suitable islanding architecture [PV40] | Introduce an outage while energy is available but inverter power is insufficient; distinguish unmet demand from energy shortage |

The architecture help describes a central battery with generic conversion stages
and discusses approximations for alternative AC/DC arrangements [PV41]. A product
yield result cannot establish the dynamics of an actual hybrid controller, island
formation, protection or black start (I). For a mine, equipment starting peaks,
outage duration, export agreements and critical/noncritical loads need separate
input and power-system studies. No assertion about real Copperbelt plant settings
or storage operation is made.

## 6. Workflow and interface

Documented path: define project/weather and a simulation variant, choose components
and array configuration, specify geometry/shading and losses, simulate, inspect
stage outputs/loss report, then compare variants [PV6, PV13, PV21, PV23]. This is a
source-based workflow, not an observed click-through.

PVsystCLI runs prepared workspace/project/variant inputs, can vary weather or batch
parameters and produces CSV/batch/report outputs [PV25]. Its active subscription is
separate [PV3]. CLI output is an automation interface, not a public source-code API.
Do not rely on manual editing of internal files as a guaranteed supported route [PV7].

### Project, scene and result workflow in public help

The documented overview separates preliminary sizing, project design, databases,
tools and measured-data analysis [PV51]. This is not a pixel-accurate observation
of a running Windows installation. The useful interaction relationships are:

| Work area | Documented operation and feedback | Evidence / qualification |
| --- | --- | --- |
| Project / variant | Define orientation and system, then add detailed losses and shading; preserve comparison variants | PV6/PV51; source-based workflow |
| Component/system configuration | Select module/inverter, series/parallel configuration and MPPT allocation | PV46; physical inverter count differs from input count |
| Horizon | Edit height/azimuth points over the sun-path plot, import or save a profile | PV48; distant-field applicability still needs judgement |
| Near shading dashboard | Construction/Perspective opens scene editor; scene is checked against orientation and required area; Table computes shading tables and enables iso-shading inspection | PV52 |
| 3D construction | Creation, history, selection, viewpoint, rendering, measurement, modification and reference controls | PV53; command inventory, not copied icon artwork |
| CAD intake | Geometry import has a dedicated workflow | PV54; units, object classes and electrical mapping still need original tests |
| Electrical layout | Bind modules to strings/inverters before detailed shade-loss calculation | PV13; approximate partitions are a separate option |
| Simulation and results | Inspect time series, loss stages, report and variant comparisons | PV21-PV23/PV49; aggregate reports can hide opposing errors |
| Measurement analysis | Replace variant weather with a measured file, inspect tables/graphs, then compare simulated and measured variables | PV50; warnings can be acceptable or blocking, not silently discarded |

The single-line editor displays injection, transformers, inverters, combiner
boxes, MPPTs, strings and cable information. Nodes can group identical child
structures. Its current help warns that some complex systems cannot be converted,
that storage is absent from the diagram and that editing is mainly grouping
without undo. Grouping behavior can change after system edits [PV44]. This is a
specific documented limitation, not a statement that every current build always
fails on large plants. It argues for stable identity and recoverable edits in
Quantic (I).

### Batch, CLI and reproducibility

Desktop batch mode creates parameter/result CSV files, one row per simulation,
with selected yearly outputs. Parameters include weather/sites, variant bases,
orientation, shade geometry and system data; saving variants and hourly output
is selectable. Its weather/site options can select nearby weather or generate
synthetic data when absent [PV43]. An automated comparison must therefore record
the actual resolved weather and coordinates, not only the requested location (I).

CLI documentation supports simulation of prepared variants, batch parameter
files and weather substitutions with reports/time-series outputs [PV25]. Keep
CLI/desktop model version and subscription distinct [PV3]. The original proposed
run record (I) is: project/variant identifiers, dependent file hashes, resolved
weather and coordinates, batch row, enabled models, warnings, export boundary,
software version and output hashes. No command or licensed simulation was run.

## 7. User value and complaints

Public help gives unusually specific modelling explanations and loss-stage reporting
[PV10-PV24]. Calling this useful for traceability is our evaluation (I), not a user
survey. One indexed forum question asks how to choose uncertainty values over plant
life [PV27]; full thread was inaccessible, so no prevalence, resolution or sentiment
claim is made. Independent customer satisfaction, support quality and defect rate
remain U. Release-note corrections [PV1] are vendor maintenance evidence, not proof
that every older case was materially wrong.

The deeper pass adds specific vendor-acknowledged constraints rather than new
customer testimony: fixed east-west bifacial assumptions [PV28], common tracker
angles [PV31/PV32], uncertain backside mismatch estimation [PV35], limited
single-line editing/storage representation [PV44], and distinct dispatch scopes
[PV37-PV41]. Their relevance to a proposed mine project is our judgement (I).
None quantifies customer satisfaction or defect prevalence.

Useful qualities for an engineer (I) are the named intermediate variables,
explicit physical-model pages, separate geometric/electrical shading and variant
comparison [PV13/PV21/PV49/PV51]. These support investigating why a yield changes.
Their value depends on parameter evidence; readable reports do not validate
unmeasured soiling, albedo or uncertainty assumptions. Vendor validation papers
are catalogued at PV55, but their complete inputs, raw measurements and suitability
for the present versions remain U in this pass.

Original lessons for Quantic (I): show model applicability next to its selection;
show whether weather is synthetic or measured; expose MPPT sharing and export
boundary; provide an inspectable energy ledger; retain reversible geometry edits;
make missing measurement support visible in uncertainty reports. These are product
requirements to evaluate, not claims about undocumented PVsyst internals.

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

| Independently implementable area (I) | Evidence basis and possible open foundation | Required distinction before validation |
| --- | --- | --- |
| Weather/time ingestion | PV8 and resource inventory; pvlib readers as candidates | Interval start/middle/end, irradiance versus irradiation, source model and licence |
| Optical geometry | PV10-PV14/PV28-PV32/PV48; pvlib tracking/transposition as candidate methods | Horizon, front shadow, backside view factors, finite edges and tracker control law |
| I-V assembly / constraints | PV15/PV16/PV20/PV35/PV46/PV47; pvlib/SSC methods to evaluate | Submodule connection and shared MPPT state; independently justified parameter fit |
| Thermal state | PV17/PV18/PV45; pvlib temperature functions as candidates | Steady versus transient, mass/wind conventions and interval averaging |
| Storage / delivery | PV36-PV42; SSC dispatch as a candidate, not an equivalent control implementation | Topology, local load, schedule, grid availability, usable battery state and flow boundary |
| Ageing / uncertainty | PV24/PV34; independent statistical implementation | Expected degradation versus warranty; distribution, dependence, time horizon and calibration |
| Reporting / comparison | PV23/PV43/PV49/PV50 | Same input hashes and state definitions; compare stages and independent observations |

Each foundation remains subject to the actual dated licences recorded in
[other-products.md](other-products.md#actual-licence-files-read-2026-10-18).
No new package or code is selected here. A library offering a function named after
a PVsyst model does not cover the full geometry, loss, MPPT or dispatch chain.

Additional original validation proposals (I, all unrun):

- PVF-01: two identical authored rows with and without backtracking; inspect angle,
  front/rear irradiance and electrical shade loss before energy and PR.
- PVF-02: same row cross section but different finite lengths and edge conditions;
  explicitly identify where a 2D approximation is no longer an independent oracle.
- PVF-03: equal total shading on different submodules/strings; compare I-V maxima
  and bypass state to a separately derived small circuit.
- PVF-04: irradiance step and constant wind with declared thermal mass; compare
  interval-average temperature with an independently integrated thermal model.
- PVF-05: identical DC availability with different MPPT sharing and export boundary;
  distinguish input current/voltage limits, ordinary clipping and grid curtailment.
- PVF-06: storage-full, storage-empty, charge-limited and discharge-limited events;
  prove energy conservation and dispatch eligibility for each strategy.
- PVF-07: uniform versus dispersed original degradation, fixed random seed and
  identical weather; distinguish module loss from changing clipping/mismatch.
- PVF-08: same raw time series under explicit interval/time representations and
  batch weather resolution; require equivalent physical energy after conversion.

These tests need authored parameters, lawful component characterisations and
justified tolerances. A numerical pass against an open engine that shares our
model code is not independent verification. Site measurements add a different
validation obligation and must preserve calibration and exclusion provenance.

## 9. Gaps and closure routes

| Gap | Why unresolved / evidence needed |
| --- | --- |
| PVG1 | Full current private file schema and version migration are not public supported contracts; obtain lawful original exports and document field loss before import work |
| PVG2 | Provider coverage/rights and conflicting version metadata are now inventoried in resource-data.md; exact site files, their contracts and timestamp checks remain unperformed |
| PVG3 | All current technology-specific fit details and coefficient provenance not traced; inspect public model papers and lawful datasheets, not inferred STC-only fits |
| PVG4 | Detailed shading, bypass/half-cell/reverse behaviour and irregular bifacial geometry need original numerical fixtures; no runtime access in this WP |
| PVG5 | Public transient equations/interval adaptation now read at PV45; independent numerical verification, source-paper comparison and measurement calibration remain open |
| PVG6 | Four grid-storage strategies and architecture now documented at PV36-PV41. Exact battery chemistry/lifetime, off-grid/pumping, optimiser and financial implementation remain incomplete |
| PVG7 | Uncertainty component distributions, dependence and site calibration need independent sources; no default percentage justified for a Zambian mine |
| PVG8 | User survey and full forum thread unavailable; no generalised sentiment. Licensed runtime comparison and precise version provenance remain unperformed |
| PVG9 | Local interconnection, earthing, faults and ride-through require the separate power study/rule profile, not an energy-yield report; see [mine rules](../power/mining-regulations.md) |

Closure priorities (I): obtain a lawful site weather/measurement package with
quality and rights metadata; pin module/inverter characterisations; validate the
energy chain on simple original cases; then add mine demand, export restrictions
and storage. Complex bifacial terrain and model-fit uncertainty need dedicated
references and measurement validation. Neither this pass nor a vendor's
"bankable" description establishes lender acceptance or an engineering certificate.

The comparison with the ETAP dossier is by topic depth, not by identical module
counts. This dossier now traces identity/licensing, 55 sources, model identities,
parameter semantics, eleven detailed study families, documented interface areas,
automation, user-evidence limits, independent engine boundaries and named closure
routes. ETAP's fault/protection fields do not become PVsyst fields by analogy.
