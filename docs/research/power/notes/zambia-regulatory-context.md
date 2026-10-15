# Zambian regulatory context for Quantic's power studies (WP-2.10)

Quantic's first clients are mines and industrial plants in Zambia. The reports Quantic
produces must check against Zambian rules, not only IEEE and IEC. This note records
what was found on 2026-10-15. All documents are public on the Energy Regulation Board
(ERB) website or a World Bank (ESMAP) mirror. They are paraphrased here, not copied.

## Documents found

| Key | Document | Status | Where |
| --- | --- | --- | --- |
| ZDGC | Zambia Distribution Grid Code, ERB, first issue May 2016 | in force (a "live document") | https://rise.esmap.org/data/files/library/zambia/Electricity Access/Zambia_Distribution Grid Code.pdf |
| DZS691 | DZS 691:2023, *Safety in AC Substation Earthing* (technically equivalent to IEEE 80-2013) | draft for comment | https://www.erb.org.zm/wp-content/uploads/files/standards/Draft-Zambian-Standard-DZS-691.pdf |
| DZS418 | DZS 418-1 and -2:2024, *Electrical Safety Code* (construction, installation and commissioning; operation and maintenance) | draft for comment; replaces ZS 418:2013 | https://www.erb.org.zm/wp-content/uploads/files/standards/Draft-Revised-Standard-DZS-418-Part-1-2024-Draft-for-Public-Comments.pdf |
| DZS387 | DZS 387 parts 1 to 4, *Power Quality and Reliability* (supply quality; measurement and reporting; application guide; instrument requirements) | draft, comments closed 2022-05-27 | https://www.erb.org.zm/request-for-public-comments-on-draft-zambian-standard-for-power-quality-and-reliability-standard-dzs-387-parts-1-4/ (ZIP: https://www.erb.org.zm/wp-content/uploads/DZS_387.zip) |
| DZS397 | DZS 397:2023, *Quality of Consumer Service* | draft; replaces ZS 397:2017 | https://www.erb.org.zm/wp-content/uploads/files/standards/Draft-Zambian-Standard-DZS-397-2023.pdf |
| ZGC | Zambian Grid Code (transmission). Referenced by the ZDGC for generators above 10 MVA | to find | - |

Also found but not read: Statutory Instrument No. 2 of 2026 under the Electricity Act
(zambialii); the Mines and Minerals Development (General) Regulations 2016 (the PDF did
not load); an ERB draft standard on inverter systems for embedded generation (ERB
post `?p=6865`).

## What the Distribution Grid Code requires (paraphrased; clause numbers from the code)

**Connection studies:**

- A new or modified connection needs load flow studies covering short-circuit infeed,
  protection coordination, power quality and environmental impact (2.3.9.2).
- The distribution network service provider (DNSP) may refuse a connection on the
  results (2.3.9.3, 2.4.12).
- A **Distribution System Impact Assessment** covers large loads, embedded generation
  and major modifications: voltage impact, loading, fault currents, protection
  coordination, quality of supply and upgrades (2.4.9).
- The customer may pay for augmentation if its generation causes overloads, fault-level
  excess, voltage or protection breaches (2.4.10).

**Customer obligations:**

- Customers above 100 kVA keep power factor at or above 0.92 lagging, not leading unless
  agreed (2.6.4.1). This drives capacitor sizing and placement (S20).
- Protection must coordinate with the DNSP's, with test certificates before
  commissioning and tests every two years (2.6.1).

**Earthing:**

- Substation earth resistance below 10 Ω (2.6.2.1.1).
- Notify affected parties where calculated GPR exceeds 5 kV (2.6.2.2.4).
- Links to the grounding engine and DZS 691.

**Embedded generation (for example a mine solar plant):**

- A breaker and visible isolation at the connection point.
- Two-stage under- and over-voltage protection on all phases.
- Dead-line detection, agreed islanding and anti-islanding, and tripping on momentary
  supply loss.
- Balanced three-phase inverters.
- Fault-level contribution within the agreed value.
- Generators above 10 MVA must also meet the Zambian Grid Code (2.7).

**Power quality:** comply with ZS 387 and the ERB Power Quality Directive (harmonics,
interharmonics, flicker, unbalance, dips, regulation, surges) (2.6.3.1). The numeric
limits are in ZS 387, not the code.

## What this means for Quantic

1. **There is a regulated demand for studies.** Every mine or industrial site adding
   load or generation (especially solar, which is fast-growing in Zambian mining) must
   submit load flow, short-circuit, protection coordination and power quality studies.
   That is Quantic's service product, and the engines in `engine-index.md` waves A to C
   cover it.
2. **Report templates should map to the code's clauses.** A "ZDGC connection study"
   report type would list each 2.3.9.2 and 2.4.9 item with pass or fail and the
   evidence. That is a strong differentiator against ETAP and PowerFactory, which do not
   ship Zambian templates.
3. **Rule data needed as checkable limits:**
   - PF ≥ 0.92 lagging;
   - earth resistance < 10 Ω;
   - the 5 kV GPR notification threshold;
   - ZS 387 voltage and harmonic limits (to read);
   - DZS 691 touch and step limits.
4. **Synergy with the PV suite (WP-2.5):** embedded generation connection studies need
   PV and inverter models, plus the anti-islanding and ride-through settings above.

## Gaps and next steps

1. Peter to download into QE-References (the workspace cannot fetch these files):
   - DZS 387 ZIP;
   - DZS 691 and DZS 418 PDFs;
   - the Zambian Grid Code (transmission);
   - the ERB Power Quality Directive;
   - the embedded-generation inverter standard;
   - the mining regulations' electrical part.
2. Confirm which drafts have become final ZS standards (ZABS catalogue).
3. Read ZS 387 for the numeric voltage, harmonic and flicker limits.
4. Engineering Institution of Zambia (EIZ) rules: who may sign such studies (registered
   engineer). This matters for Quantic's service model and for Peter's own registration.
