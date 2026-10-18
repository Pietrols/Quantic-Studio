# Solar resource and weather data for Zambia

WP-2.25, ChatGPT, 2026-10-18. Public documentary research only; no site file,
weather API, measurement dataset or yield simulation was downloaded or executed.
S means supported by the cited primary source; I is an original proposed workflow;
U means unresolved. Coverage, sampling interval, native spatial resolution,
validation and reuse rights are separate questions. All sources were accessed
2026-10-18. No purchase or provider contact was made.

## 1. Resource-source register

| ID / source | Zambia coverage and data kind | Resolution and vintage read | Access / licence status and limitation |
| --- | --- | --- | --- |
| RD-A PVGIS 5.3 | S: SARAH3 satellite footprint includes Africa; ERA5 is a global reanalysis alternative, RD1/RD3. Exact selected-site extraction untested | Hourly series; production page lists 2005-2023, RD1. Native solar and meteo grids differ. RD3 discusses historical ERA5 about 30 km and snapshot satellite timing; do not label every variable a site measurement | No-cost service. RD4 EU-owned website content CC BY 4.0 unless indicated, with third-party exceptions. Exact selected dataset notices remain a required check; EUPL code licence is not a dataset grant |
| RD-B PVGIS 6 beta | S: global service except poles, RD2; Zambia falls within geographic service scope | Hourly solar/meteo, elevation/horizon. About page says 2013-2024; other current JRC metadata says 2014-2024. Preserve the discrepancy, not a guessed start year | Beta API/code and schema differ from v5.3. RD4 general EU reuse policy applies to EU-owned content; underlying provider terms still need checking. No production migration approved |
| RD-C NASA POWER | S: global gridded solar and meteorology, RD5/RD7; appropriate Zambia coordinates are within scope, no actual request made | Source-dependent grids; documented solar 1° and meteorology 0.5° by 0.625°, RD7/RD8. Hourly/daily/monthly/climatology by parameter; historical daily records are not all hourly. Current processing is Data v10, RD5 | Public no-cost access, RD5/RD7. RD6 requires citation of service/version/access date and requests redistribution notification. No single SPDX licence or release-specific redistribution instrument retrieved; retain provider notices and resolve exact redistribution terms before bundling |
| RD-D NSRDB Meteosat Prime Meridian PSM v4 | S: Meteosat footprint covers Africa, RD11. Candidate for Zambia; exact point/year availability needs discovery, not assumed from GOES coverage | RD10 says 4 km/15 minutes. Its prose says 2017-2019 while year options list 2005-2022. Do not claim either is a successfully retrieved complete archive | RD9 explicitly says freely available/no cost. Formal per-artefact redistribution notice not retrieved (U); source processing code licence is separate. API key/email workflow is documented but was not used |
| RD-E Meteonorm Climate / Web / API | S: worldwide TMY/AMY service, RD12; successor to Meteonorm 8. Zambia site generation not requested | Provider advertises synthetic output down to one minute and mixed station/satellite/reanalysis inputs. Output interval does not establish one-minute measured weather or a uniform native grid. Exact selected-site source periods/grid U | Paid proprietary terms RD13, 24 April 2025. API integration and turnover restrictions, third-party transfer/resale limits; Web App excludes automation and general redistribution, with a specific client-order exception. Verify signed product terms, not an assumed open-data grant |
| RD-F Solargis commercial time series / assessment | S: Zambia regional adaptation demonstrated in RD16; current site assessment products in RD15 | Dataset/model/date and delivery interval must be specified in quote. Historical Zambia atlas model used 1 km mapping and 1994-2017 aggregation, RD16; that is not a current commercial product's guaranteed grid or period | Paid proprietary service. RD15 general service terms and region/product schedules govern use; a free-map licence does not cover purchased time series. Exact order, output-sharing and redistribution rights remain U until selected |
| RD-G Solargis free Zambia maps / GIS | S: Zambia page lists long-term GHI/DNI/diffuse/tilted/PVOUT and other GIS products, RD14 | Long-term monthly/yearly map products, not a chronological weather-year input. Vintage and native raster grid must be read from selected asset metadata, not PNG dimensions | Page specifically links CC BY-SA 4.0 and attribution, RD14, despite loosely calling it an Attribution licence. Preserve ShareAlike. No files copied |
| RD-H World Bank Global Solar Atlas | S: Zambia resource maps and country assessment route, RD16/RD17 | Screening and long-term map products. Selected dataset version, grid and temporal aggregation require its metadata. Not a replacement for a chronological site weather series | Download page's indexed text says CC BY 4.0, RD17; full dynamic licence text did not render. Keep per-asset notices; do not substitute RD14's different CC BY-SA grant |
| RD-I Zambia Meteorological Department | S: national station/request service, RD18. Exact solar sensors, continuity and accessible records at a Copperbelt site are U | Request form offers hourly through annual aggregation, but that is a request option, not evidence each station measures every quantity at that rate. Solar radiation is not listed among its visible checkbox parameters | Institutional review and data-sharing policies, RD18; fee, commercial use, redistribution and solar-series access U. No open licence inferred from a public station list |

Rights statements above are dated source findings, not a legal approval. A service
may be free to query yet impose output conditions; an open software engine can
consume a restricted weather file. Keep these grants separate.

## 2. Sampling and metadata discrepancies

PVGIS 6 is described as beta on its own About page. That page's 2013 start year
disagrees with the JRC landing/publication metadata's 2014 start year (S, RD2).
The 5.3 page still calls that version production (S, RD1). Pin the endpoint,
database name and actual response metadata; do not silently upgrade an existing
study because a newer interface exists (I).

RD3 compares satellite snapshots with suitably averaged ground measurements.
An hourly timestamp does not necessarily mean an hourly-average irradiance in
every provider. POWER's time guidance says the hour starts at its timestamp and
defaults hourly/daily to Local Solar Time unless UTC is requested (S, RD19).
Local Solar Time is not a civil time zone. The interval, units and source reference
must be resolved before combining weather with a mine's meter profile (I).

NSRDB's current endpoint page contains conflicting period text and selection
options (S, RD10). Its public processing repository also describes a wider
Meteosat period than that page's introductory prose (S, RD20). This inventory
does not claim a download succeeded. A later authorised retrieval must verify
available years, location ID, grid coordinates, fill flags, leap-day policy and
the permitted temporal options rather than copy an example request (I).

POWER's methodology distinguishes older SRB, CERES and near-real-time FLASHFlux
sources and warns about discontinuities in trend analysis (S, RD8). A recent
value and a reprocessed historical value may have different lineage. Record
the source for each period rather than labelling a concatenation homogeneous (I).

For Meteonorm, one-minute synthetic output is an output capability, not evidence
of the temporal resolution of the underlying observations (I from RD12). A TMY
is suitable for typical-condition comparison; it cannot by itself supply the
distribution of independent annual yields needed for a multi-year exceedance
assessment (I). Do not count a TMY month as an additional measured year.

## 3. Validation evidence, including Zambia

RD16 is the April 2019 World Bank/Solargis validation report. It documents a
24-month campaign at six Zambia stations during 2015-2017 and regional model
adaptation. Its executive summary describes 1 km map-based series aggregated
over 1994-2017. Sections 3-4 discuss calibration, maintenance, time reference,
quality control and comparison with station instruments. Regional adaptation
reduces a documented overestimation pattern. Those results concern that model,
measurement set and period; they are not a universal error bound for a future
mine-site file. Section 5 excludes interannual variability from its uncertainty
estimate. The report's copyright page allows attributed noncommercial reproduction;
its charts, values and measurement records are not copied here (S).

JRC publishes a PVGIS 5.3 dataset update with BSRN comparisons (RD1/RD21);
RD3's older validation discussion includes southern African stations but is not
a Zambia-only calibration of every current product. NASA publishes solar-flux
assessment against ground observations (RD22). No quoted global statistic is
adopted as a Kitwe/Mufulira uncertainty, and no independent validation of these
providers was performed here (U for exact project accuracy).

RD11 is a laboratory announcement describing extension of high-resolution
Meteosat data across Africa/Europe. It establishes the product's purpose and
geographic family, not a guarantee of every point's quality. Meteonorm and
Solargis describe validation/assessment services, but marketing use of the word
bankable does not establish acceptance by a particular lender (I).

## 4. What a finance-facing mine-site study needs (I)

This is an original evidence plan, not a statutory minimum campaign duration,
a lender's checklist or a certification. Agree the required independent review
and uncertainty method with the project's actual stakeholders.

| Study stage | Evidence to obtain and preserve | Free and paid routes / unresolved question |
| --- | --- | --- |
| Screening | Coordinates/elevation, usable area, broad GHI/DNI pattern, known obstruction/land constraints | RD-A/C/G/H can support initial comparison; a map does not establish chronological export or firm supply |
| Resource assessment | Versioned multi-year chronological GHI/DHI/DNI and relevant temperature/wind, source metadata and quality flags | Compare applicable PVGIS/POWER/NSRDB products; evaluate a paid Solargis/Meteonorm file where justified. Shared satellite/reanalysis inputs mean providers are not automatically independent |
| Site verification | Calibrated on-site irradiance and weather records, cleaning/maintenance logs, horizon/albedo and soiling observations | Project-owned campaign and lawfully obtained ZMD records; equipment, operation and access may cost money. Exact site history remains U |
| Long-term adjustment | Overlap/QC analysis, documented bias correction, retained validation period and uncertainty of the adjustment | Public methods and RD16 give a starting rationale; qualified assessment/service may be paid. Never tune all data and call the same samples an independent validation |
| Engineering yield | Lawful module/inverter characterisations, geometry/wiring, tracker/backtracking, thermal, loss and availability assumptions | Manufacturer records, original surveys and appropriate simulation. Detailed rear mismatch or dust losses need specific evidence |
| Mine/grid integration | Demand at a known meter boundary, critical-load split, outages, export limits, storage power/state and operating policy | Client-owned records under agreed use; separate network/fault/protection/dynamic studies as required |
| Risk / finance | Explicit uncertainty components, dependence, degradation horizon, annual variability and sensitivity scenarios | Independent review and project-specific commercial requirements. No default P90 factor follows from a free API or paid report |

No paid provider is declared mandatory solely because it is paid. Source choice
must follow the project's location, data quality, model applicability, rights
and review requirements. Public data can support reproducible development;
the evidence needed for a particular investment decision is a project question.

## 5. Proposed data acceptance and original checks (I)

1. Store provider, product/model/version, coordinate request and returned grid
   point, elevation, retrieval date, source period, file hash and licence notice.
2. Store physical quantity and units, accumulation versus average, interval
   duration and timestamp reference, UTC/civil/solar time and missing-data flags.
3. Test chronology, duplicates, gaps, leap days and energy-conserving resampling.
   Never silently coerce missing irradiance to zero or observed gaps to weather.
4. Distinguish original, provider gap-filled, synthesised and site-adjusted data;
   keep transformations, calibration provenance and excluded intervals.
5. Compare coincident variables at matching time support and measurement geometry.
   Inspect bias by season/time/irradiance regime as well as annual energy.
6. Keep uncertainty in resource, instruments, site adaptation, models, losses
   and annual variability separate; document any dependence assumption.
7. Label an original test series as synthetic and independent of the providers.
   Proposed cases: identical physical intervals in UTC and civil labels; leap-day
   removal; one missing daylight interval; mean-power versus accumulated-energy
   conversion; conflicting source version; denied redistribution grant. None run.

## 6. Open gates

| Gap | Closure needed |
| --- | --- |
| RDG1 | Selected PVGIS version/period, underlying dataset licence and response metadata; beta versus production ambiguity preserved |
| RDG2 | Exact POWER parameter/source-period metadata and any dataset-specific redistribution notice before packaging |
| RDG3 | NSRDB Zambia point/year availability, conflicting period text and full per-asset terms; no API key/email request submitted |
| RDG4 | Meteonorm selected-site input lineage and contract for Quantic's intended use; no automation under a manual Web licence |
| RDG5 | Current commercial Solargis product/order, source grid/period, export rights and site validation; free-map grant cannot substitute |
| RDG6 | ZMD solar series, station instruments/history, QC, fees, commercial/republication terms; national station existence alone insufficient |
| RDG7 | Ground campaign/current mine-site evidence, client data rights and independent assessment; 2019 regional calibration is historical evidence |
| RDG8 | Project-specific lender/utility criteria, electrical interconnection studies and validated uncertainty model; no bankability assertion here |

## 7. Primary sources and exact read scope

| ID | Source |
| --- | --- |
| RD1 | JRC [Using PVGIS 5](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/using-pvgis-5_en), 5.3 production/data/validation description |
| RD2 | JRC [PVGIS 6 About](https://photovoltaic-geographic-information-system.ec.europa.eu/en/about-pvgis-6), beta and 2013-2024; [JRC landing page](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis_en) and [2026 publication metadata](https://publications.jrc.ec.europa.eu/repository/handle/JRC145834), indexed 2014-2024; discrepancy retained |
| RD3 | JRC [data sources and calculation methods](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/general-information/data-sources-calculation-methods_en), source grid/timing and older validation scope; not all current-version metadata |
| RD4 | European Commission [legal notice](https://commission.europa.eu/legal-notice_en), copyright/reuse exceptions; [PVGIS 6 API](https://photovoltaic-geographic-information-system.ec.europa.eu/api/v6/redoc), indexed code licence only, not a blanket data licence |
| RD5 | NASA [POWER docs](https://power.larc.nasa.gov/docs/), current Data v10 and lineage/release distinctions |
| RD6 | NASA [POWER referencing guide](https://power.larc.nasa.gov/docs/referencing/), service/version/date citation and redistribution notification request |
| RD7 | NASA [POWER methodology](https://power.larc.nasa.gov/docs/methodology/), global products and source grid resolutions |
| RD8 | NASA [energy fluxes](https://power.larc.nasa.gov/docs/methodology/energy-fluxes/), SRB/CERES/FLASHFlux, native solar grid and discontinuity warning |
| RD9 | NLR [NSRDB API index](https://developer.nlr.gov/docs/solar/nsrdb/), no-cost access, distinct satellite product families |
| RD10 | NLR [Meteosat Prime Meridian PSM v4 endpoint](https://developer.nlr.gov/docs/solar/nsrdb/nsrdb-msg-v1-0-0-download/), full text, contradictory introductory years versus selectable names, 4 km/15 minutes |
| RD11 | NLR [2024 Africa/Europe high-resolution data announcement](https://www.nlr.gov/news/detail/program/2024/game-changing-high-resolution-solar-data-enables-renewable-energy-expansion-across-two-continents), footprint and purpose, not independent validation |
| RD12 | Meteotest [Climate](https://meteonorm.com/climate/), current service, worldwide TMY/AMY, advertised temporal output, source families, successor to v8 |
| RD13 | Meteotest [Web App/API terms](https://meteonorm.com/meteonorm_agb_en.pdf), 2025-04-24, five pages, rights of use and contract restrictions; no licence purchased |
| RD14 | Solargis [free Zambia maps/GIS](https://solargis.com/resources/free-maps-and-gis-data?locality=zambia), explicit linked CC BY-SA 4.0, product list; assets not downloaded |
| RD15 | Solargis [legal index](https://solargis.com/legal) and [general service terms](https://solargis.com/legal/general-service-terms/general-service-terms-sro), current regional contract route; no signed order or product schedule |
| RD16 | World Bank [Zambia Solar Model Validation Report](https://documents1.worldbank.org/curated/en/528251556199357703/pdf/Solar-Resource-and-PV-Potential-of-Zambia-Solar-Model-Validation-Report.pdf), April 2019; copyright, executive summary, sections 3-5 inspected, not reproduced |
| RD17 | World Bank/Solargis [Global Solar Atlas download](https://globalsolaratlas.info/download), indexed licence text only; dynamic direct content did not render |
| RD18 | ZMD [data request](https://zmd.gov.zm/data-request/) and [official site](https://zmd.gov.zm/), institutional review, visible parameters/aggregation choices; no request submitted |
| RD19 | NASA [POWER time guidance](https://power.larc.nasa.gov/docs/faqs/other/) and [hourly API documentation](https://power.larc.nasa.gov/docs/services/api/temporal/hourly/), time standard/interval and parameter-specific metadata |
| RD20 | NLR [NSRDB source README](https://github.com/NatLabRockies/nsrdb), indexed release-period metadata only; no code or dataset copied, no software adoption |
| RD21 | JRC [PVGIS 5.3 Dataset Update](https://joint-research-centre.ec.europa.eu/document/download/aa763480-b092-48af-a7f8-42913b43d305_en?filename=Report_2024_PVGIS_5.3_Datasets_Update.pdf), JRC139355, 2024; cover/contents and validation route, no statistics adopted |
| RD22 | NASA [solar-flux validation](https://power.larc.nasa.gov/docs/methodology/energy-fluxes/solar-validation/), global ground-comparison tables; no Zambia-specific error bound inferred |

No atlas image, report table, station record or weather series is committed. A
failed URL or inaccessible rights statement is an explicit gate above, not an
invitation to infer permission from another provider's licence.
