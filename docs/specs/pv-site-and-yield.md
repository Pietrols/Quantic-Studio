# CC-5: PV site and yield, version 0.1.0

The CC-3 manifest is unchanged. Register `model_type: pv.site` with a model
payload validated by `pv/site`. Register `study_type: pv.yield` with a request
validated by `pv/yield-request`, bound to that model. This is a contract and
engine-free validation slice. Execution, CLI/API routing and web views follow
in WP-2.3 to WP-2.5. It makes no IEC 61724-1 performance-monitoring claim.

## Site and stable assets

`site_id`, array IDs, module IDs and inverter IDs are stable model-local IDs.
The manifest asset representation uses element types `site`, `arrays`,
`modules`, `inverters` and the corresponding ID. A module entry represents an
authored equipment specification; `module_count` states its multiplicity.
Names and module counts never imply unprovided electrical equipment data.
IDs cannot contain dots because dots delimit output signal IDs.

Coordinates are latitude north positive, longitude east positive, degrees;
elevation is metres. Tilt is degrees from horizontal; azimuth is clockwise
from north, north 0 and south 180. Albedo is an explicit dimensionless fraction.
The fixed-tilt subset has one inverter per array, with no shared inverter,
tracking, string voltage model, bifacial model or inferred shading geometry.
Other topologies require a future approved Contract Change.

Every module explicitly declares reference DC watts, reference cell temperature
in Celsius and power temperature coefficient per kelvin. Temperature is either
`ross` with explicit `noct_c`, or `supplied_cell` from the weather file. All
arrays in one study use the same temperature input kind. Ross assumes steady
or slowly changing irradiance and nominal 1 m/s wind; this model does not infer
real wind cooling. No module, NOCT, albedo or loss defaults exist.

Every inverter declares DC input limit, AC rating, nominal efficiency and
reference efficiency. The PVWatts parameter identity is
`ac_rating_w = dc_input_limit_w * nominal_efficiency`, checked to relative
1e-12 numerical serialization tolerance. This is a model scaling limit, not an
absolute electrical voltage/current safety rating. Module reference DC rating
is independent: an authored 5 x 300 W array can feed a 1000 W DC / 900 W AC
inverter with nominal efficiency 0.9. These are hypothetical test inputs, not
manufacturer specifications or recommended equipment.

`losses` is an explicit ordered list of named fractions in [0,1], applied
sequentially within each stage (`irradiance`, `dc`, `ac`). An empty list explicitly
means no named losses. For stage input X, each row records `removed = X*f` and
passes `X*(1-f)` to the next row. Irradiance losses have W/m^2 outputs; DC/AC
losses have W outputs. Inverter conversion and clipping are combined in
`inverter_loss_w`, separate from named losses. Physical model equations and
adapter verification belong to WP-2.5; these validators do not execute a model.

## Request and local weather

`execution` embeds the frozen CC-4 time-stepped request. Its `model_id` and
`study_id` must equal the manifest binding. `model_file` must resolve to that
model file. `execution.input_series_file` resolves from the project root to a
separate CC-4 series file. Paths cannot escape the root through traversal,
absolute paths or symlinks. Weather cannot alias any model, request or manifest.
Weather is included in `Project.files` for the service's existing file limits.
No validator downloads weather or resolves URLs.

Weather metadata records the raw file SHA-256, `synthetic` or `observed`, a
readable citation, licence, UTC timezone, proleptic Gregorian calendar, named
GHI/DNI/DHI/temperature channels and `air` or `cell` temperature kind. Synthetic
also covers explicitly authored data; it must never be labelled observed.
Imported typical-year data needs a documented synthetic calendar mapping.
Committed external data additionally needs its rights in `docs/sources/entries`.
Tests generate small original synthetic data in temporary directories, offline.

The UTC origin must match the CC-4 series. Every weather row represents a
half-open interval `[time,end_time)`, with mean irradiance/temperature, aligned
to the fixed-second request grid. No naive/local timestamps, daylight-saving
transitions, leap-second strings or implicit gap filling are accepted. Timestamps
use uppercase T and Z, with at most six fractional digits. Non-leap and leap
calendar years are counted by their actual UTC boundaries, not a fixed 8760.
Gaps, missing and invalid cells remain visible to the runner and produce partial
or failed output; they are never silently replaced by zero. Negative valid
irradiance is rejected. Inputs use explicit compatible units (W/m^2 for
irradiance; Celsius-compatible temperature); the future adapter must perform
any explicit conversion, including offsets. Channels are real, input-causality
signals bound to the study model. All used temperature models must match them.

The request explicitly selects NREL SPA, isotropic transposition, PVWatts v5 DC
and inverter models and midpoint solar sampling for each weather interval.
SPA pressure in Pa, ambient temperature in Celsius, delta T in seconds and
atmospheric refraction in degrees are supplied, never defaulted. Midpoint
sun position combined with interval mean weather is a declared approximation;
it does not claim to reproduce SAM's sunrise-hour correction or all PVWatts.

## Outputs, working and energy

`pv_output_units(site)` lists the frozen real output inventory. The request
must declare exactly these signal IDs and canonical units, with output
causality and its model ID. For each array, prefix `<array_id>.`:

| Signal suffix | Unit |
| --- | --- |
| sun_zenith_deg, sun_azimuth_deg | degree |
| poa_beam_w_m2, poa_sky_w_m2, poa_ground_w_m2 | W/m^2 |
| poa_global_w_m2, poa_effective_w_m2 | W/m^2 |
| cell_temperature_c | degC |
| dc_gross_w, dc_net_w, ac_gross_w, ac_net_w, inverter_loss_w | W |
| loss.<loss_id> | W/m^2 at irradiance stage, otherwise W |

`site.ac_power_w` is the sum of array net AC outputs. Sun values describe the
interval midpoint; power/irradiance values are the interval's model estimate
from the supplied mean weather. `sampling: interval_mean` is required for energy.
Unavailable output has a CC-4 null cell with diagnostics, not a fabricated number.

The result embeds the unchanged CC-4 `execution` result: operation trace,
requested/reached times, diagnostics, solver/version/input hash provenance,
individual model/request/weather hashes and model versions. It preserves the
request's weather metadata and data-file hash. It requires nonempty `working`
when any valid interval was calculated. Under D11 the adapter must independently
compute/check the working against the engine, and reports must show every
governing equation, its bibliography/edition/page, substituted values and result.
The common trace format does not by itself prove physical correctness.

Energy is `E_Wh = sum(P_ac_W * interval_seconds / 3600)`. Power is generation,
nonnegative, after all named losses. Only intervals with every required output
cell valid contribute to the conservative covered-period total. `coverage`
records requested start/end, expected/valid/missing/invalid counts. A row with
any invalid cell is invalid; other unavailable rows and unreached intervals
are missing. Counts partition the requested grid. The runner must also diagnose
weather gaps and propagate input validity, even if it reaches the requested end.

`period` spans the requested bounds and sums only valid contributions; its
`complete` flag reports whether valid samples cover the full interval. `monthly`
has one entry per intersected UTC month, clipped to requested bounds. A sample
crossing a month boundary is split proportionally by elapsed seconds under the
interval-mean assumption. Missing contributions are excluded with incomplete
coverage, so a partial sum is never presented as a complete period total.
`annual` is null unless the complete successful result covers exactly January 1
through next January 1 of one UTC year, with every interval valid. A valid
full year must include its annual total. No extrapolation, rescaling or
"typical year" label is invented. An incomplete run requires diagnostics.

## Validation and compatibility

Call `validate_pv_site`, `validate_pv_request(site=...)`,
`validate_pv_weather(request=...,site=...,raw_bytes=...)`, and
`validate_pv_result(request=...,site=...)` for semantic checks.
`qe_core.validate` alone checks schema/finite numbers, not these bindings.
`load_project` invokes the model/request/weather validators, checks assets,
confines paths and verifies the weather hash. It does not execute a PV engine.
Result validation verifies CC-4 traces, bound signals, file identity, coverage,
monthly splits and energy sums. It does not certify equation accuracy, equipment
suitability or weather quality. TS exports mirror all three payload schemas;
existing power, time and manifest schemas are preserved byte for byte.

## Readable reference and independent oracle

- Gilman, *SAM Photovoltaic Model Technical Reference*, NREL/TP-6A20-64102
  (2015), pp. 18-19 (fixed surface angles), p. 51 Eq. 11.2 (inverter DC/AC
  scaling), pp. 55-56 (net AC and hourly delivered energy). Readable page-tagged
  reference verified. No source text or worked example is reproduced.
- pvlib 0.16.1 documentation, `pvsystem.pvwatts_dc`, `inverter.pvwatts`,
  `irradiance.isotropic`, `temperature.ross`: parameter meanings and equations;
  the pages cite Dobos, *PVWatts Version 5 Manual*, NREL/TP-6A20-62641 (2014),
  and Ross (1981). This CC imports no pvlib code. Future imports stay in
  `qe_pv/adapters/pvlib/` under BSD-3.
- Independent original oracle in `test_pv_contracts.py`: 100 W for two hours
  gives 200 Wh; leap 2024 has 366 days, so 878400 Wh at constant 100 W;
  February contributes 29 x 24 x 100 = 69600 Wh. Hypothetical ratings and
  independently declared signal inventory test dimensions and references.

Paid standards, separately: IEC 61724-1 is unavailable and no monitoring or
performance-class conformance is claimed. IEC 61215/61730 module qualification
and IEC 62109 inverter safety are outside this simulation contract; no test or
safety compliance is inferred. Work proceeds using explicit authored equipment
inputs and the readable model references above. Duffie and Beckman is not held
and is not cited as a directly read source.
