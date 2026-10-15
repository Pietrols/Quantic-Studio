# Verification benchmarks: what ETAP validates against, and what Quantic can reproduce (WP-2.10)

Sources:

- E36: ETAP's QA verification and validation page, read 2026-10-15. It lists 23 case
  documents and a combined PDF (E94).
- E92 and E93: two case documents read in detail.

Purpose: Quantic's tests must reproduce published references with recorded provenance
(AGENTS.md sec. 3.4). Using the **same public benchmarks** as ETAP lets us claim
like-for-like accuracy. We reproduce the original publications, not ETAP's documents.

## ETAP's benchmark list [E36]

| Study | Benchmark source | Kind | Quantic access |
| --- | --- | --- | --- |
| Arc flash | IEEE 1584-2018 annex results | standard | paid (gap); `arcflash` reproduces Annex D1 and D2 |
| Arc flash (HV ArcFault) | IEEE C2-2023 (NESC) | standard | paid |
| Arc flash | DGUV-I 203-077, example 5.1 | German accident-insurance guide | **owned** (QE-References); reproduced 2026-10-15 |
| DC arc flash | DGUV-I 203-077, example 5.8 | same | same |
| Harmonics | IEEE 519-1992, example 13.1 | standard | paid (old edition; may be obtainable) |
| Load flow | Anderson and Fouad, *Power System Control and Stability* (WSCC 9-bus) | textbook | data public; pandapower ships `case9` |
| Load flow | R. N. Dhar, *Computer Aided Power System Operation and Analysis* | textbook | not owned |
| Load flow | IEEE 399-1997 (Brown Book) | standard | paid |
| Load flow | IEEE 3002.2-2018 | standard | paid |
| Motor starting | hand calculations; ETAP TS | internal | n/a (we use Das02 and Fitz03 instead) |
| ANSI short circuit | GE *Short-Circuit Current Calculations for Industrial and Commercial Power Systems* | vendor publication | Das02 ch. 9 cites it as ref. 1; to locate |
| ANSI unbalanced | P. M. Anderson, *Analysis of Faulted Power Systems* (1973), pp. 38 to 40 [E93] | textbook | not owned (also our F8 gap) |
| ANSI duty | IEEE 399-1997 sec. 7.7, 44-bus | standard | paid |
| IEC short circuit | IEC TR 60909-4:2021, example 4, sec. 9 [E92] | technical report | paid; **highest-value purchase for F1** |
| Transient stability | field data; IEEJ standard benchmark; Anderson and Fouad 9-bus; PSS/E comparison | mixed | IEEJ benchmark models are published by IEEJ (to check); 9-bus is public |
| Unbalanced load flow | IEEE 13-node test feeder | public benchmark | free from IEEE PES test feeder site |

## What ETAP's documents show about tolerances [E92, E93]

- **IEC (TR 60909-4 example):**
  - Ik'', Ib and Ik agree within about 0.01% to 0.1%;
  - peak ip with method C differs by up to about 1.15% at one bus, while the document
    states a 0.6% allowance and does not explain the larger figure;
  - LG peak differs by up to 0.53%.
  - Edition references are inconsistent inside the document (60909-4:2021 against
    60909-0:2016).
- **Anderson unbalanced fault:** fault current matches exactly; sequence voltages differ
  by up to 0.5%, which ETAP attributes to Anderson's constant-impedance load
  contributing to the fault.
- Lesson for Quantic: publish our tolerance per quantity *before* running the case. When
  a difference comes from a modelling choice (load as a fault contributor, method C
  frequency), state it in the trace. Our AGENTS rule "do not loosen a tolerance to pass"
  is stricter than this practice, and that is a selling point.

## Benchmarks Quantic can run now (owned or free)

| Case | Source we have | Engine |
| --- | --- | --- |
| Das02 Examples 7.1 and 7.2 (ANSI duties; errata noted) | Das02 | F3 |
| Das02 sec. 8.7 IEC against ANSI comparison | Das02 | F1, F3 |
| Grainger94 Examples 12.1 to 12.5 (unbalanced faults with Δ-Y shift) | Grainger94 | F2 |
| Glover17 sec. 9.5 examples | Glover17 | F2 |
| Kasikci02 worked networks (already used in D11) | Kasikci02 | F1 |
| Das02 Example 9.2 (battery IEC; with the decimal erratum) | Das02 | F5 |
| Das02 Examples 19.1 and 20.1 (harmonics and filter) | Das02 | H1, H2 |
| Das21 Tables 3.8 and 3.9 (IEEE 1584-2018 examples) | Das21 | A1 |
| Kundur94 Example 12.6 two-area system: data complete, 24 eigenvalues published (Tables E12.3, E12.4); mode f and ζ recomputed | Kundur94 | T3, T1 |
| Kundur94 Example 13.1 critical clearing (0.0865 s, 52.2°); our equal-area recomputation gives 0.0868 s | Kundur94 | T1 |
| Gonen88 Examples 10.1 and 10.2 (catenary length, loaded sag); recomputed and agree | Gonen88 | C8 |
| Das10 ch. 6 capacitor energisation: use the analytic RLC (eqs 6-6 to 6-9) only; printed Example 6-5 current is 4% off | Das10 | T4 |
| WSCC 9-bus (Anderson and Fouad data, public) | pandapower `case9` and literature | S1, T1 |
| IEEE 13-node feeder | IEEE PES (free) | S10 |
| Anders05 "model cable No. 1" | Anders05 | C2 |
| Morley ground-bed example (10 kA into 5 Ω gives 50 kV GPR, a sanity check) | Morley | C6 |
| DZS 691 Table 5 (Kinyon, five substations): eq. 41 reproduces all five Rg values | DZS 691 (QE-References) | C6 |
| DGUV-I 203-077 Example 5.1 (630 kVA station, 694.9 kJ, APC 2 insufficient); recomputed exactly | DGUV guide (QE-References) | A2 (IEC method) |

## Recommendation

Add a "benchmarks" section to WP-2.12 `engines.md` with one row per engine:

- the benchmark;
- source and page;
- the tolerance we commit to.

Each engine WP then makes its benchmark a required test. The two purchases with the most
verification value are IEC TR 60909-4 (IEC short circuit) and IEEE 399 (ANSI duty and
load flow).
