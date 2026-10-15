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
- The document mentions no academic discount, so treat this as the commercial Base
  Package list price in 2025.
- Advanced modules (stability, protection, harmonics and so on) are extra and not
  priced here.

**Training in southern Africa [P85] (regional vendor list, reliable for 2024):**

- DIgSILENT Buyisa (South Africa) prices per delegate, excluding VAT, from about
  **ZAR 9,300 (3-day Basic, online)** to ZAR 12,850 (3-day EMT, classroom).
- Most 2-day courses are ZAR 9,100 to 11,400.
- Courses carry CPD points.
- This is the price level Zambian engineers already pay for training.

## ETAP

- **No vendor price list.** The only figures found are a third-party estimate [E98]
  ("starts at about USD 5,000 per user per year"; maintenance 15 to 20%). It gives no
  source and is internally inconsistent. **Indicative only; do not quote it to clients.**
- **Licence facts from the dossier:** modules are sold separately. The bus-count and
  module tiers are a known buyer frustration, also seen for EasyPower in the forums
  [E96].
- **To find:** a public tender or contract record for ETAP (as with P84), for example in
  African or EU procurement portals. A next search target.

## What this suggests for Quantic (proposal for Peter, not a decision)

1. **The anchor price is about EUR 7,000 for a basic, single-seat commercial tool**
   (load flow and short circuit), plus about 16% a year, before any advanced modules.
   Full study packages (protection, arc flash, stability) cost several times that.
   For a Zambian consultancy or mine, that is a large outlay. It is the gap Quantic's
   pricing can target.
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

1. ETAP actual prices from a public record.
2. Prices for PowerFactory advanced modules.
3. Engineering Institution of Zambia (EIZ) CPD rules for training providers.
