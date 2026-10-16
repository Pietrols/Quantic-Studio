# Pricing and licensing: ETAP and PowerFactory (WP-2.10 working note)

Why this matters: Quantic is a business. Its price and licence model must make sense
against what mines and consultancies in Zambia and southern Africa pay today. Vendors
do not publish price lists, so every figure here is labelled with its evidence quality.

## PowerFactory

**Licence structure [P83] (vendor page, reliable):**

- **Editions:**
  - Single-User (local SQLite);
  - Multi-User (licence server, concurrent seats; an optional floating licence of up to
    30 days offline);
  - Team (shared Oracle, SQL Server or PostgreSQL database with versioning and merge).
  - "Engine" licences (no GUI, API only) are available for commercial and research use.
- **Commercial licences** are configured module by module on a Base Package, with node
  limits of 100, 250, 500 or unlimited.
- **Academic licences:**
  - Research (unlimited nodes, publicly funded research only);
  - Education (50 nodes, courses of up to 25 students);
  - Student (50 nodes, cloud, 12 months);
  - Thesis (cloud, up to 12 months).
  - A free 28-day demo, with a browser streaming version.
- **Licence technology:**
  - a softkey bound to one PC (movable twice a year, no virtual machines);
  - a USB dongle (extra cost);
  - a cloud softkey (needs a permanent internet connection; hosted in Germany).
- **Models:**
  - perpetual, with the first year of maintenance included;
  - subscription of 6 or 12 months, only for Single-User Commercial on a cloud softkey;
  - time-limited commercial licences of 6 or 12 months.

**A real price [P84] (public procurement record, reliable for that configuration and
date):**

- Buyer and date: VSB-Technical University of Ostrava, offer 2025-03-10, order
  2025-04-24.
- Configuration: PowerFactory Multi-User Edition, **250 nodes, 1 concurrent user,
  Base Package only**.
- Price: **EUR 7,160** net, plus a EUR 500 administrative fee; 12 months' maintenance
  included.
- After that, maintenance is **16% of list price per year**.
- Training is quoted from EUR 2,060 per day.
- **Scope of this figure (corrected 2026-10-16 after ChatGPT's dispute 5bf6d26):** it
  is the price this university paid for this configuration on this date. The absence of
  a stated academic discount does not prove there was none. The general commercial list
  price is **unknown**.
- Advanced modules (stability, protection, harmonics and so on) are extra and not
  priced here.

**Training in southern Africa [P85] (regional vendor list, reliable for 2024):**

- DIgSILENT Buyisa (South Africa) prices per delegate, excluding VAT, from about
  **ZAR 9,300 (3-day Basic, online)** to ZAR 12,850 (3-day EMT, classroom).
- Most 2-day courses are ZAR 9,100 to 11,400.
- Courses carry CPD points.
- This is South African pricing. Whether Zambian engineers pay the same is not
  established.

## ETAP

**Official price structure, 2007 [E99] (a US GSA schedule filed by Operation
Technology, Inc., ETAP's maker; price tables dated 2007-01-24; USD). These are GSA
net prices to the US government, not ordinary commercial list prices (ChatGPT review,
2026-10-15; the module sums below were independently reproduced):**

- **Pricing is per module, in bus-count tiers:** 50, 100, 200, 300, 500, 1,000, 2,000,
  5,000, 10,000, 20,000 and unlimited.
- Separate lease (term) and perpetual prices, with lower prices for the 2nd to 7th and
  8th copies.
- **Maintenance is a percentage per year:** 12% for a single licence, 15% for nuclear,
  and 15% plus per-copy fees for site licences.
- **Example (first perpetual copy, 2007 prices):** a typical mining or industrial study
  package (base, load flow, ANSI and IEC short circuit, arc flash, Star protection and
  motor acceleration) cost **USD 5,169 at 50 buses** and **USD 18,227 unlimited**.
- Adding transient stability and harmonics brings the unlimited package to USD 26,152.
- Individual modules ranged from about USD 300 to 6,000.
- **These are 2007 prices.** Adjust with an official CPI series before quoting them, and
  expect list prices and packaging to have changed since (ETAP is now part of Schneider
  Electric via AVEVA, whose ETAP software schedule of February 2024 appeared in search
  but was not read).
- The *structure* (modules times bus tiers, plus a maintenance percentage) matches what
  buyers still describe today.

**Recent figures:** no vendor price list. The only figures found are a third-party estimate [E98]
  ("starts at about USD 5,000 per user per year"; maintenance 15 to 20%). It gives no
  source and is internally inconsistent. **Indicative only; do not quote it to clients.**
- **Licence facts from the dossier:** modules are sold separately. The bus-count and
  module tiers are a known buyer frustration, also seen for EasyPower in the forums
  [E96].
- **To find:** a public tender or contract record for ETAP (as with P84), for example in
  African or EU procurement portals. A next search target.

## What this suggests for Quantic (proposal for Peter, not a decision)

1. **Observed price points, each tied to its own source and configuration** (no
   general list price is established for any of the three):
   - PowerFactory: EUR 7,160 for a 250-node, one-user Base Package bought by a
     university in 2025, plus 16% a year maintenance [P84];
   - ETAP: USD 5,169 (50 buses) to USD 18,227 (unlimited) for an industrial study
     package at 2007 US GSA net prices [E99];
   - PowerWorld: US$11,000 for the commercial base package, plus listed add-on prices
     and renewal at 28% of the licence price, from the vendor's public pricing page
     (`powerworld.md`, W4, read 2026-10-15).

   Advanced modules are extra in all three. The size of that extra is not established
   for PowerFactory (no module prices were read). For a Zambian consultancy or mine,
   even the base figures are a large outlay. That is the gap Quantic's pricing can
   target.
2. **Licence frictions Quantic can remove:**
   - PC-bound softkeys and no virtual machines;
   - a permanent-internet cloud key;
   - node limits;
   - module-by-module tiers.

   An open core (the engines and CLI under a permissive licence) plus paid services
   (verified study reports, training, support, hosted workbench) avoids all of these.
3. **Training is a revenue line in its own right.** DIgSILENT runs a regional training
   business with CPD points. Quantic's learning notes and worked traces are the start
   of a training product. Engineering Institution of Zambia CPD accreditation would be
   a lever (to research).
4. **Academic licences build users for life:** Student and Thesis licences, a free demo
   and browser streaming. Quantic being free for students is the equivalent, and
   cheaper for us.

## Gaps

1. A recent ETAP price from a public record. The 2007 GSA list is the best found so
   far. A Guam Power Authority tender (GPA-019-25, ETAP upgrades and support) exists,
   but the page did not load.
2. Prices for PowerFactory advanced modules.
3. Engineering Institution of Zambia (EIZ) CPD rules for training providers.
