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
| ZGC | Zambian Grid Code (transmission). Referenced by the ZDGC for generators above 10 MVA. An amended draft with VRE connection requirements was submitted to the ERB on 2022-07-22 (ZESCO System Operator news, 2023-08-01); no public link found | amended draft pending | https://systemoperator.zesco.co.zm/blog/3 |
| PQMF | ERB *Revised Power Quality Management Framework*, February 2026, for stakeholder consultation. Ten directives for licensees; limits deferred to ZS 387 | consultation draft | https://www.erb.org.zm/wp-content/uploads/files/Power-Quality-Management-Framework.pdf |

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

## Who may do and sign the studies: EIZ Act 2010 (paraphrased; read 2026-10-15)

Source: Engineering Institution of Zambia Act No. 17 of 2010,
https://portal.eiz.org.zm/portal_assets/media/doc/EIZ_ACT.pdf. This is research, not
legal advice; confirm with EIZ.

- **Individuals:**
  - categories are Engineer, Technologist, Technician and Craftsperson (R.Eng, R.Teg,
    R.Tec, R.Cra) (s.2, s.17, s.20);
  - practising needs EIZ membership plus registration (s.15) **and** an annual practising
    certificate (s.25, s.26, s.29);
  - regulations may tie certificates to CPD (s.31(b)).
- **Organisations:**
  - an engineering organisation or unit **may not provide any engineering service or
    product unless registered** (s.18(1)), with titles R.Eng.O and R.Eng.U;
  - registration requires an office in Zambia and declared fields of practice (for
    example electrical, mining);
  - **consulting firms must belong to the Association of Consulting Engineers of Zambia
    and have registered engineers as partners with suitable experience** (s.19).
- **Penalties:** practising, or an organisation providing services, while unregistered
  carries heavy fines in penalty units and possible imprisonment (s.15(2), s.18(2),
  s.25(2), s.41).

**Implication for Quantic Engineering Limited:** selling study *services* (connection
studies, arc flash, protection) in Zambia needs the company registered with the Board
(and ACEZ membership if it acts as a consulting firm), with studies signed by a
registered and practising engineer. Selling the *software* may also count as an
"engineering product" under s.18(1); confirm with EIZ. This is a business prerequisite
to plan alongside the software.

## Power quality framework (PQMF, February 2026; paraphrased)

- **Limits:** none of its own. All power quality limits (voltage regulation, harmonics,
  flicker, dips, unbalance) **defer to ZS 387**. The only figure it states itself is
  that a generator must keep its negative-sequence voltage contribution at the point of
  connection below 1% unless agreed (cl. 2.3.1).
- **Large customers (mines):**
  - emission limits are set under ZS 387, calculated by the utility with ZS 387 methods
    if the contract is silent, negotiable, with appeal to the ERB (cl. 2.7.1 to 2.7.2);
  - customers must not pollute beyond ZS 387, must provide their own surge protection,
    and should design for dip immunity.
- **Renewable generators above 5 MW** must measure the ZS 387 parameters, including
  harmonics (Directive 10).
- No reference to NRS 048 or IEC 61000 by name. Benchmarking against international
  standards is promised (cl. 3.1).
- **Implication:** a harmonic study for a mine (VFDs, mills) is judged against ZS 387
  emission limits allocated by ZESCO. **ZS 387 is the key document to obtain** (the
  DZS 387 ZIP above). The harmonics engine (`engine-harmonics.md`) must take ZS 387
  emission allocation as data.

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
   - DZS 387-1 voltage, harmonic, flicker, unbalance and frequency limits (read, see the section on standards read in full);
   - DZS 691 touch and step limits.
4. **Synergy with the PV suite (WP-2.5):** embedded generation connection studies need
   PV and inverter models, plus the anti-islanding and ride-through settings above.

## Standards read in full (QE-References, 2026-10-15)

Peter added nine PDFs to QE-References (commit 0784309): DZS 387 parts 1 to 4,
DZS 418 parts 1 and 2, DZS 691, DZS 1191-2 and DGUV-I 203-077. All have good text
layers. Findings by document:

**DZS 387-1:2022, *Power Quality and Reliability, Part 1: minimum standards*.**

- **Status:** the pages carry a "Draft standard for public comment" watermark.
- **Edition:** the cover says second edition. The foreword says "this third edition
  cancels and replaces the second edition (ZS 387-1:2011)". Cite it as "DZS 387-1:2022
  (draft)" until ZABS publishes the final.
- **Lineage:** it lists NRS 048-2:2015 (South Africa) as a reference, and the dip
  windows (S, T, X, Y, Z) follow the NRS 048 scheme.

Limits apply at the **point of supply to consumers** and are assessed over at least
7 days at the 95% level (cl. 4.2, 5). Read on the page images:

| Parameter | Limit | Clause, printed page |
| --- | --- | --- |
| Voltage THD, LV and MV (to h = 40) | 8%, with individual harmonic levels in Table 1 (for example h5 6%, h7 5%, h11 3.5%, h13 3%) | 5.1.1.1, p. 14 |
| Voltage THD, HV and EHV | 4%, with individual levels in Table 2 (from CIGRE TB 261) | 5.1.1.2, p. 15 |
| Flicker, LV | Pst 1.0, Plt 0.8 (IEC 61000-4-15 meter). No MV or HV levels | 5.2.1, p. 16 |
| Voltage unbalance | 2% (up to 3% where single- and two-phase consumers dominate) | 5.3.1, p. 17 |
| Voltage dips | Maximum dips per year by window category and network (Table 4) | 5.4, pp. 18 to 21 |
| Interruptions | Forced interruptions per year by network category (Table 5) | 5.7, p. 22 |
| Voltage regulation | ±10% below 11 kV, ±5% at 11 kV and above, for no longer than 10 consecutive minutes | 5.8, Table 6, p. 24 |
| Frequency | 49 to 51 Hz on the grid; 47.5 to 52.5 Hz on islanded networks | 5.9.1, p. 24 |

**Text-layer warning:** the QE-References text of DZS 387-1 drops "<", "≥" and "±".
Table 6 reads "11000 / 11000" in the text. Always confirm limits on the page image.

**DZS 387-3 (application guide):**

- The utility enforces emission limits on its consumers.
- New plant should be immune to the Table 1 compatibility levels.
- Capacitor installations must avoid resonance at dominant harmonics.
- Planning levels are in cl. 4.5.
- It names **crushers** and motor starting as flicker sources.
- Rapid voltage changes have no limits in the standard, only contract guidance
  (Annex F).

For Quantic, a mine's harmonic and flicker study is judged at the PCC against
utility-allocated emission limits, with Table 1 as the ceiling. Both go into
`engine-harmonics.md` as limit data.

**DZS 418-1:2024, *Electrical Safety Code Part 1*.**

- The committee includes the Mines Safety Department and Mopani Copper Mines Plc, and
  the code may be adopted with mine rules (cl. 1, note 1).
- Table 5-5 (cl. 5.5.4, printed p. 20) sets minimum heights to the lowest conductor:
  - 5.1 m for bare LV and 5.0 m for insulated LV (open country);
  - 5.3 m at 33 kV in open country and 5.5 m in other areas;
  - rising to 7.8 m at 400 kV.
- **The table has no 11 kV row.** Whether 11 kV takes the 33 kV value is not stated;
  ask a Zambian practitioner before encoding it.
- The note says the height "shall be maintained under any conditions of loading and
  temperature": exactly the sag engine's worst case (`engine-calculators.md` sec. 2).

**DZS 691:2023 (earthing):** read in full; see `engine-grounding.md` sec. 1b. In
short, it gives the acceptance limits but defers mesh and step voltage factors, Df
and conductor sizing to IEEE 80 and ZS IEEE 837, and its Schwarz Rm is misprinted.

**DZS 1191-2:2026, *Inverter systems for embedded generation*:**

- draft for public comment;
- its foreword says it "draws from" IEC and IEEE standards rather than adopting one;
- it covers anti-islanding (Annex A set-point form, IEC 62116), voltage and
  frequency ride-through by inverter category, reactive capability (0.85 lagging to
  0.95 leading), a 49.5 to 50.5 Hz continuous band, and a requirement for
  connection studies.

Read it in detail with the PV suite (WP-2.5), not now.

**DGUV-I 203-077 (2021 English):** read; see `engine-arc-flash.md` sec. 6a.

## Gaps and next steps

1. Peter to download into QE-References (the workspace cannot fetch these files):
   - DZS 387 ZIP;
   - DZS 691 and DZS 418 PDFs;
   - the Zambian Grid Code (transmission);
   - the ERB Power Quality Directive;
   - the embedded-generation inverter standard;
   - the mining regulations' electrical part.
2. Confirm which drafts have become final ZS standards (ZABS catalogue).
3. ~~Read ZS 387 for the numeric limits~~: done (draft DZS 387-1:2022). Still open:
   whether a final ZS 387 has been published, and the DZS 387-3 planning levels in cl. 4.5.
4. EIZ: confirm the organisation registration route for Quantic, Peter's own category
   and route to R.Eng, the CPD rules, and whether software counts as an "engineering
   product" under s.18.
5. Draft **DZS 1191-2, *Inverter Systems for Embedded Generation*** (ERB call for
   comments, 2026-08-12, comments closed 2026-09-11): LV (230/400 V) grid-following,
   multi-mode and grid-forming inverters below 1,000 kVA for mini-grids and embedded
   generation. ZIP:
   https://www.erb.org.zm/wp-content/uploads/files/call_for_comments/standards-to-govern-inverter-systems-for-embedded-generation.zip.
   Relevant to the PV suite and to mine solar.
