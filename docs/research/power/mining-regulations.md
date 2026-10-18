# Mine electrical rules: Zambia and South African comparators

WP-2.21, ChatGPT, checked 2026-10-18. Research inventory, not a compliance
certificate or a rule database. Public sources only. No paid standard, private
reference text, table or mine data is reproduced. Engine E numbers refer to
[engines.md](engines.md); capability IDs refer to [parity-matrix.md](parity-matrix.md).
Mappings below are Quantic design inferences (I), not instructions from a regulator.

## 1. Evidence and applicability

Record four separate facts: an instrument exists; it commenced; its edition applies
to this installation; its actual clause supports the proposed check. A published
standard is not automatically compulsory. A consultation draft is not the published
standard, even if its PDF header omits the D. A South African rule is not automatically
Zambian law or proof of customary Copperbelt practice. Contractual adoption and any
regulator exemption must be recorded separately.

**No numeric engineering limits are adopted in this inventory.** Dates, Act numbers,
standard designations and clause locators are identifiers, not design settings.
Every threshold still needing verification is a named gap in section 5. This avoids
silently inheriting numbers from an older note or from a search snippet.

S below means the indicated fact was seen in a public source, not that Quantic has
implemented it. U means unresolved, never absent. All sources were accessed
2026-10-18. Metadata-only retrieval is distinguished from reading an instrument.

## 2. Zambia: legal and grid instrument register

| Key | Instrument, edition and issuer | Access and status evidence | Proposed engine / row mapping | Clause or applicability gap |
| --- | --- | --- | --- | --- |
| ZM1 | Minerals Regulation Commission Act No. 14 of 2024; Parliament | Public enacted text [ZR1]. Section 97 repeals Act 11 of 2015 and saves specified authorisations/applications. SI 42 of 2025, para. 2, brings it into operation on publication, 13 June 2025 [ZR2]. S | E1/E36, D1/G11: legal context and approval provenance | ZG1: determine the full continuing subsidiary-legislation chain, not just saved licences |
| ZM2 | Minerals Regulation Commission (Amendment) Act No. 40 of 2026; Parliament | Public legal-repository metadata labels it uncommenced, dated 12 June 2026 [ZR3]. Text/commencement not independently established here; U for current operative effect | E1/E36, approval authority metadata | ZG2: obtain enacted amendment and any commencement event; do not substitute its Bill |
| ZM3 | Geological and Minerals Development Act No. 2 of 2025; Parliament | Public Act [ZR4]; SI 41 of 2025 para. 2 in the same Gazette commences it on publication [ZR2]. S for instrument, not an electrical design code | E36, G11: project/legal context only | ZG1: identify provisions actually relevant to an electrical installation |
| ZM4 | Mining Regulations 1971, SI 107 of 1971, with Mining (Amended) Regulations 1973, SI 95 of 1973; Government | ILO-hosted historical guide [ZR5] explicitly says it amalgamates these instruments and does not replace them. Part XIX, regs. 1901-1927 is the electrical locator. S historical text; U current consolidation | E13/E19/E31/E32/E36, F1/P1/C1/C6/G11 | ZG1: original Gazettes, later amendments and survival under current Acts |
| ZM5 | Electricity Act No. 11 of 2019; Parliament | Public enacted Act catalogued by Parliament [ZR6]; replaces the 1995 Act. S, but no assertion that this is a fully consolidated 2026 text | E2/E7/E19/E25/E36, S1/S15/P1/T1/G11 | ZG3: current amendments, licence and connection applicability |
| ZM6 | Energy Regulation Act No. 12 of 2019; Parliament / ERB | Public Act metadata [ZR7]; licensing and ERB mandate. S | E36, report authority and licence metadata, not solver equations | ZG3: installation-specific licence/permit and current amendments |
| ZM7 | Electricity (Transmission) (Grid Code) Regulations 2026, SI 4 of 2026; Minister of Energy | ZambiaLII lists publication/commencement at 9 January 2026, but also an anomalous 2025 history date [ZR8]. ERB's 2025 report, p. xvi, lists SI 4 of 2026 [ZR9]. PDF body did not load. S instrument existence; U clause content | E2/E7/E8/E13/E19/E25/E28, grid S/F/P/T/H rows | ZG4: signed Gazette, commencement and complete schedule including model submission and ride-through clauses |
| ZM8 | Electricity (Wayleave and Clearances) Regulations 2026, SI 2 of 2026; Minister of Energy | Public metadata dated 2 January 2026 [ZR10], also listed in ERB report p. xvi [ZR9]. Body not clause-audited | E33, C8: sag, geometry and clearance checks | ZG5: actual voltage/land-use tables, reference condition, sag temperature and exemptions |
| ZM9 | Zambia Distribution Grid Code, first issue May 2016; ERB | Public document route in the existing [context note](notes/zambia-regulatory-context.md), plus official code portal [ZR11]. Current revision/continuing applicability not established by this pass | E2/E13/E19/E24/E28/E32, S1/F1/P1/M1/H1/C6 | ZG6: verify current cl. 2.3.9.2, 2.4.9, 2.6.1-2.6.4 and 2.7 against actual current code and supply agreement |
| ZM10 | Electricity (Net Metering) Regulations 2024, SI 38 of 2024; Minister of Energy | Public ERB-hosted instrument [ZR12], also listed in report [ZR9]. No numeric eligibility or protection settings imported | E2/E19/E25/E36, S1/P1/T1; PV connection interface | ZG7: eligibility, approval, metering and interface-protection clauses; net metering is not permission for arbitrary islanding |
| ZM11 | System Operator Guidelines 2025; ERB | Public dated official PDF [ZR13]. Inventory-level source, not reviewed as a connection limit schedule | E7/E25/E36, S15/T1/G11 | ZG4: relationship to SI 4, operator data and study obligations |
| ZM12 | Revised Power Quality Management Framework, February 2026; ERB | Official stakeholder-consultation notice [ZR14]. S draft provenance, U final adoption | E28/E29/E36, H1-H3/S22/G11 | ZG8: final directive, PCC allocation, measurement period and applicable ZS 387 edition |
| ZM13 | Engineering Institution of Zambia Act No. 17 of 2010, amended by Act No. 28 of 2021; Parliament / EIZ | Public principal Act route in context note; enacted 2021 amendment [ZR15], not merely Bill 26. Professional authority is a separate issue from a solver's correctness | E36, G11: signatory and practising-status evidence | ZG9: consolidated current registration, organisation and certification provisions, including treatment of software products |

The old [context note](notes/zambia-regulatory-context.md) is a dated research record,
not an operative legal baseline. In particular, transmission code "pending" must not
override ZM7. Mining-law summaries citing only the 2015 Act miss ZM1. Neither the
guide's age nor a ministry overview proves its electrical regulations were repealed:
the continuity question remains ZG1.

Historical electrical locators from [ZR5], printed pp. 123-130, include 1905
(plans), 1910 (protection), 1914 (earthing), 1915-1916 (cables/flexible cables),
1918 (switchgear), and 1925-1926 (overhead lines). These are search routes for
the current instrument, not an assertion that those historical clauses apply today.

## 3. Zambian technical standards and owned-reference crosswalk

The private-reference inventory and prior reading are recorded in
[zambia-regulatory-context.md](notes/zambia-regulatory-context.md), "Standards read
in full". This WP does not reread or export the owned copies. Public provenance and
publication status must be checked independently of possession.

| Key | Standard / issuer | Public versus paid; edition evidence | Proposed engine / rows | Remaining clause or edition gap |
| --- | --- | --- | --- | --- |
| ZS1 | DZS 691:2023, Safety in AC Substation Earthing; ZABS | Public draft cover and contents read [ZR16]. **A final ZS 691 was published**, according to ERB 2024 report Appendix 1, printed p. 65: Gazette Notice 983, 13 September 2024 [ZR17]. Final edition/body and purchase terms not retrieved. Owned draft is not that final | E32/E13/E19, C6/F1/P1 | ZG10: final ZS 691 edition, corrigenda and adoption. Draft cl. 8/11/13-16 and IEEE 80 dependency must be reconciled before calculation checks |
| ZS2 | DZS 387 parts 1-4:2022, Power Quality and Reliability; ZABS | Public ERB consultation/ZIP [ZR18]; owned draft inventory records parts 1-4. ERB 2025 report refers to ZS 387 for monitoring, but that alone does not establish which revision was published [ZR9] | E28/E29/E10/E36, H1-H3/S22/G11 | ZG8: final parts/editions, cl. 5 of part 1 and planning/emission allocation in part 3; exact comparators and aggregation windows |
| ZS3 | DZS 418-1 and -2:2024, Electrical Safety Code, construction/installation/commissioning and operations/maintenance; ZABS | Public draft notice [ZR19]; owned two-part inventory. ERB 2024 report says submitted to ZABS for publication, not proof of publication [ZR17]. Final access/edition U | E19/E31/E32/E33/E36, P1/C1/C6/C8/G11 | ZG11: final edition, mine applicability and incorporation; part 1 cl. 5.5.4/Table 5-5 clearance categories. Prior note flags missing voltage category; never interpolate |
| ZS4 | DZS 1191-2:2026, Inverter Systems for Embedded Generation; ZABS | ERB public consultation dated 12 August 2026 [ZR20]. Owned draft is listed in prior inventory. No final publication verified | E2/E19/E25/E28, S1/P1/T1/H1; PV inverter interface | ZG12: final category-dependent response, anti-islanding, reactive capability and Annex A settings, including applicable point of connection |

[ZR16] explicitly limits its scope to AC substation earthing and excludes DC-specific
earthing and quantitative lightning-surge treatment. Its contents identify conductor,
soil, grid-current and safety checks. That is not a universal earth-resistance test
or a substitute for protection clearing time. The previous note also records a
suspected Schwarz-expression erratum: resolve against the final edition and its
normative references before implementation, rather than encode the draft equation.

For Peter: the acquisition list is **final editions and amendments**, especially
ZS 691, ZS 387 parts 1-4 and ZS 418 parts 1-2; DZS 1191-2 stays a draft until
publication is verified. No purchase is authorised by this research. A public draft
remains copyrighted. No PDF, tables or source case files belong in this repository.

## 4. South Africa: comparators, not automatic Zambian requirements

The public MHSC landing page identifies a consolidation last updated January 2026,
posted 29 September 2026 [SR1]. Its electrical chapter still identifies GN R332 of
24 April 2015. The original Gazette is independently public [SR2]. Distinguish
**regulations Chapter 3 (Electricity)** from Act Chapter 3 (worker representation).

| Key | Instrument / issuer / edition | Evidence and access | Proposed engine / rows | Boundary / clause gap |
| --- | --- | --- | --- | --- |
| SA1 | Mine Health and Safety Act 29 of 1996, as amended; Parliament | Public MHSC January 2026 consolidation [SR1] | E36, risk and competent approval provenance | SG1: site-specific applicability, later amendments, mandatory codes of practice |
| SA2 | MHSA Electricity Regulations Chapter 3, GN R332, Gazette 38708, 24 April 2015; Minister of Mineral Resources | Public original [SR2] and 2026 consolidation pp. 134-143 [SR1] | E13/E19/E22/E31/E32/E36, F/P/A/C/G families | SG1: confirm operative text at installation date and site-specific requirements |
| SA3 | SANS 10142-1:2006, wiring of premises; SABS | Paid/restricted standard text not retrieved. Dated reference appears in reg. 3.30, for surface residential/commercial buildings [SR1, SR2]. This is not a general mine-wide design scope | E31/E19, C1/P1; constrained buildings | SG2: obtain incorporated edition, clause content, applicable amendments and legal substitution rule; latest catalogue edition is a separate question |
| SA4 | SANS 10280:1995, overhead power lines; SABS | Text not retrieved, catalogue/current edition U. Dated reference in reg. 3.31 [SR1, SR2] | E33, C8 | SG3: incorporated line-design/clearance clauses and site conditions. This standard is **not** an earthing standard |
| SA5 | SANS 10222 Part 3:2002, non-lethal electrical security fences; SABS | Text not retrieved. Dated reference in reg. 3.32 [SR1, SR2] | E36, separate installation checklist, outside current physics engines | SG4: fence-specific provisions; not a substitute for substation ground-grid analysis |

Public electrical clause routes [SR2]: competent design/installation 3.1; electrical
and arc risks 3.2; extensions and alternate supplies 3.3; current diagrams 3.5;
cable overload/earth-fault discrimination 3.7; earth-conductor fault withstand
3.16/3.19/3.20; flexible/trailing cable screening 3.23-3.24; overhead-line contact
risks 3.28; hazardous-area apparatus certification 3.37-3.39. No numerical relay,
touch-voltage or incident-energy setting is inferred from these duties.

The SANS references above are the dated editions in the public regulation, **not a
claim that those are the latest SABS publications**. Both public versions exclude
the normative references of the cited standards in regs. 3.30-3.32. Automatically
following every normative reference, or silently substituting the latest edition,
would therefore be unsafe. SABS catalogue searches did not yield reliable current
records in this pass; acquisition and legal interpretation remain SG2-SG4.

Other potentially relevant families, not yet verified as applicable instruments:
trailing-cable product standards, hazardous-area installation standards, arc PPE
standards and NRS grid-quality / embedded-generation specifications. These are
search targets SG5, not guessed standard numbers or evidence of a Zambian mandate.
No evidence found establishes how commonly South African specifications are adopted
in actual Copperbelt contracts; client specifications remain required.

## 5. Explicit verification queue

All gaps below are U. An unresolved check must show "not assessed", not pass.

| Gap | Required evidence before a compliance check | Affected responsibility |
| --- | --- | --- |
| ZG1 | Current mine electrical SI consolidation; amendment/repeal/savings chain from 1971 through current legislation, including scope of ZM1 s. 97 | Mine approval, electrical protection, cables and earthing |
| ZG2 | Enacted 2026 amendment text and commencement record, reconciled with uncommenced metadata | Authority / legal baseline |
| ZG3 | Current Electricity/Energy Regulation Act amendments, licence and connection conditions for the specific mine | Legal context / E36 |
| ZG4 | SI 4 actual signed Gazette and full Grid Code schedule; resolve metadata date anomaly; connection category, models, study cases, dynamic and quality limits with clauses | E2/E7/E8/E13/E19/E25/E28 |
| ZG5 | SI 2 clearance schedules and applicability clauses, temperature/load condition and land-use category | E33 |
| ZG6 | Current Distribution Grid Code and agreement; clause-audited PF, earthing/GPR, coordination, generation and study obligations | E2/E13/E19/E24/E28/E32 |
| ZG7 | SI 38 net-metering eligibility/interface clauses and approved settings, not tariff-as-technical-limit | E2/E19/E25 |
| ZG8 | Current ZS 387 parts and final PQ directive; emission versus compatibility limits, PCC allocation and measurement windows | E28/E29/E10 |
| ZG9 | Current consolidated EIZ requirements and regulator clarification of relevant service/product category | Signatory / E36 |
| ZG10 | Published ZS 691 cover, edition, corrigenda, normative references and cl. 8/11/13-16 equivalents | E32, fault duration coupling |
| ZG11 | Published ZS 418 revision and applicability; conductor-clearance table's exact categories, without invented interpolation | E31/E32/E33 |
| ZG12 | Final inverter standard, category, anti-islanding and ride-through clauses/settings | PV interface / E25 |
| SG1 | Latest South African Gazette changes and mine code of practice; any actual Zambian contractual adoption | E13/E19/E22/E31/E32 |
| SG2 | SANS wiring incorporated edition and actual cable/protection clause values, obtained lawfully | E31/E19 |
| SG3 | SANS overhead-line incorporated edition and actual design clause values, obtained lawfully | E33 |
| SG4 | SANS security-fence incorporated edition and relevant clauses, obtained lawfully | Separate checklist |
| SG5 | Official current catalogue identities/editions for trailing cables, hazardous apparatus, arc PPE and NRS specifications; contract/adoption evidence | Product verification beyond network solver |

## 6. Proposed software boundary (I)

Do not bake jurisdiction into a load-flow or fault solver. A versioned rule profile
would cite issuer, instrument/edition, clause, effective interval, adoption basis,
installation category, agreed departures and source-verification state. Thresholds
would carry units, measurement location, aggregation interval and comparator.

The study result would separately identify model/solver versions, input hash,
scenario, uncertainty and the rule-profile version. A compliant numerical quantity
cannot certify competent installation, isolation procedures, apparatus certification
or professional registration. Rule gaps invalidate the affected check only, but
prevent a blanket compliance certificate. This proposal maps to E36/G11 and
R-042 to R-046; it does not create or change a software contract.

## 7. Public sources

All accessed 2026-10-18; direct links are provenance, not redistributed content.

- ZR1: [Parliament, Act 14 of 2024, ss. 95-97](https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2014%20of%202024%20The%20Mineral%20Regulation%20Commission.pdf).
- ZR2: [Government Gazette, 13 June 2025, SI 42 para. 2 and SI 41 para. 2, PDF pp. 14-15](https://media.zambialii.org/media/legislation/44311/source_file/6851ed15a19c99e8/minerals-regulation-commission-act-2024-commencement-order-2025.pdf). Gazette reproduction, text read.
- ZR3: [ZambiaLII, Act 40 of 2026](https://zambialii.org/akn/zm/act/2026/40/eng%402026-06-12). Indexed metadata only; direct fetch restricted.
- ZR4: [Geological and Minerals Development Act 2 of 2025](https://media.zambialii.org/media/legislation/44115/source_file/3761cf75dee04c6a/2025-2.pdf). Instrument identity; no electrical clause claimed.
- ZR5: [ILO NATLEX, Guide to the Mining Regulations](https://natlex.ilo.org/dyn/natlex2/natlex2/files/download/17345/ZMB17345.pdf), introduction p. 3 and Part XIX. Historical compilation, not current Gazette consolidation.
- ZR6: [Parliament, Electricity Act 11 of 2019](https://www.parliament.gov.zm/node/8267). Official catalogue/abstract.
- ZR7: [Parliament, Energy Regulation Act 12 of 2019](https://www.parliament.gov.zm/node/8268). Official catalogue/abstract.
- ZR8: [ZambiaLII, SI 4 of 2026](https://zambialii.org/akn/zm/act/si/2026/4/eng%402026-01-09). Metadata retrieved, schedule unavailable in this pass.
- ZR9: [ERB, Energy Sector Report 2025](https://www.erb.org.zm/wp-content/uploads/files/esr2025.pdf), printed pp. xvi, 37 and 53. Read regulatory context, not engineering settings.
- ZR10: [ZambiaLII, SI 2 of 2026](https://zambialii.org/akn/zm/act/si/2026/2/eng%402026-01-02). Metadata, clauses unverified.
- ZR11: [ZESCO System Operator, Grid Code portal](https://systemoperator.zesco.co.zm/gridcode). Indexed route; direct retrieval failed, current text not verified.
- ZR12: [ERB-hosted SI 38 of 2024](https://www.erb.org.zm/wp-content/uploads/SI-38-of-2024-Net-Metering.pdf). Source route, clause audit pending.
- ZR13: [ERB, System Operator Guidelines, 2025](https://www.erb.org.zm/wp-content/uploads/files/20250808_SystemOperatorGuidelines.pdf). Source route, clause audit pending.
- ZR14: [ERB, February 2026 PQ framework consultation](https://www.erb.org.zm/revised-pqms-framework-for-the-esi-in-zambia-for-stakeholder-consultation/).
- ZR15: [Parliament, EIZ Amendment Act 28 of 2021](https://www.parliament.gov.zm/node/8997). Enacted PDF also inspected; assent 19 May 2021.
- ZR16: [ERB public DZS 691:2023 draft](https://www.erb.org.zm/wp-content/uploads/files/standards/Draft-Zambian-Standard-DZS-691.pdf), cover, scope cl. 1 and contents. No formula or numeric limit adopted.
- ZR17: [ERB, Energy Sector Report 2024](https://www.erb.org.zm/wp-content/uploads/files/esr2024.pdf), Appendix 1, printed p. 65 / PDF p. 84, table image checked. ZS 691 publication and DZS 418 submission distinguished; the table heading anomalously says status at December 2025, so use its explicit Gazette date, not the heading as an effective date.
- ZR18: [ERB, DZS 387 parts 1-4 consultation](https://www.erb.org.zm/request-for-public-comments-on-draft-zambian-standard-for-power-quality-and-reliability-standard-dzs-387-parts-1-4/).
- ZR19: [ERB, DZS 418:2024 consultation](https://www.erb.org.zm/request-for-public-comments-on-the-revised-draft-zambian-standards-dzs-418-2024/).
- ZR20: [ERB, DZS 1191-2 consultation, 12 August 2026](https://www.erb.org.zm/standard-to-govern-inverter-systems-for-embedded-generation/).
- SR1: [MHSC current regulation index](https://mhsc.org.za/promulgated-regulations/) and [January 2026 consolidation](https://mhsc.org.za/wp-content/uploads/2026/09/Mine-Health-and-Safety-Act_2026Regulations-updated.pdf), electrical regulations pp. 134-143. Selected chapter read, not every page audited.
- SR2: [Government of South Africa, GN R332, Gazette 38708, 24 April 2015](https://www.gov.za/sites/default/files/gcis_document/201504/38708rg10415gon332.pdf), regs. 3.1-3.39 and dated incorporation clauses. Original public instrument read; no standard text copied.
