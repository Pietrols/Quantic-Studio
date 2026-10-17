# Power engine inventory

WP-2.12, Claude, 2026-10-17. Every calculation engine the seven products imply, which
Quantic has, which it lacks, what we would build on and which owned books verify it.
Companion to [parity-matrix.md](parity-matrix.md). Research synthesis; the build order
at the end is a proposal for Peter, not an approved plan.

## How to read it

- **Evidence.** This decomposition is inferred, not a recovered vendor implementation.
  Each row is an **I** (inferred) responsibility, derived from **S** (seen) evidence that a product offers
  the study the engine serves. The matrix rows carry that S evidence and its citations;
  this table cites them by row ID. "Engines implied" in each dossier (ETAP and
  PowerFactory section 8, PowerWorld section 8, other products section 8 per product)
  is the source of the split.
- **Quantic:** `done`, `partial` or `none` on `main` on 2026-10-17.
- **Base:** pp = pandapower (BSD); DSS = OpenDSS via DSS-Python (BSD-style); VG =
  VeraGrid (GridCal, licence to confirm per use); `arcflash-calc` (MIT, approved by
  Peter 2026-10-15); own = implement ourselves. GPL tools (ANDES) run only as separate
  processes for verification (AGENTS.md rule 7).
- **Books** use the short names in [notes/engines-library-map.md](notes/engines-library-map.md).
  Book errata already found are listed in [notes/engine-index.md](notes/engine-index.md).
- **R-IDs** link to [reconstruction-requirements.md](reconstruction-requirements.md).

## 1. Network and steady state

| # | Engine | Matrix rows | Products seen offering the study | Quantic | Base | Owned books | Blocking gap | R-IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | Network model, type library and topology processor (switch states, islands, identity maps) | D1 to D4, D11, G2, G7, S9, PW-D1 | all seven (D1) | partial | own on CC-3 contracts | Grainger94, Glover17 | none | R-001 to R-004 |
| E2 | Balanced AC load flow with controls (Q limits, taps, remote regulation, shunts, phase shifters, droop) | S1 to S9 | ETAP, PF, PW; others S1 only | partial (S1, S3 done) | pp | Glover17 ch. 6, Das02 ch. 11 to 13, Kundur94 | none | R-007, R-008, R-010 |
| E3 | Unbalanced phase-domain load flow | S10, F8 | ETAP (mod), PF, EasyPower, SKM (mod), NEPLAN | none | DSS | Das02 ch. 14 | Kersting (not owned) | R-013 |
| E4 | Physical DC network flow and AC/DC coupling | S12, PW-S1 | ETAP, PF, EasyPower, SKM (mod), NEPLAN | none | own | Das02 ch. 9 | none | R-013 |
| E5 | Line and cable constants from geometry, neutral reduction | S11, S8, C8 | ETAP, PF, PW | none | own | Grainger94, Gonen88, Arrillaga03 | none | R-031 to R-034 |
| E6 | Time-series and quasi-dynamic orchestrator | D8, S13 | ETAP (mod), PF (mod), PW, PSS/E (mod) | none | own on CC-4 time runner (WP-2.3) | none needed | profile data per site | R-012 |
| E7 | Sensitivities, distribution factors, contingency orchestrator, RAS | S15, S16, PW-S2 | ETAP (mod), PF, PW, NEPLAN, PSS/E | none | pp | Grainger94 ch. 14 | none | R-011 |
| E8 | Transfer capability and voltage stability (continuation P-V, Q-V, modal) | S17, PW-S3 | ETAP, PF, PW, PSS/E | none | VG CPF (licence to confirm) | Kundur94 ch. 14, Sauer06 | Q-limit handling check | R-011, R-012 |
| E9 | Optimisation: OPF, dispatch, unit commitment, reserves | S14, S26, PW-S4 | all except EasyPower and SKM (U) | none | pp OPF | Glover17, Grainger94 ch. 13, Das02 ch. 15 to 16 | none | R-012 |
| E10 | Probabilistic, hosting capacity, reliability | S19, S22, S23 | ETAP, PF | none | own | Glover17 (thin) | Billinton and Allan (not owned); ETAP patent E112 needs reading before any hosting-capacity method | R-050 |
| E11 | State estimation and load allocation | S18, S25 | ETAP, PF | none | pp estimation | Grainger94 ch. 15 | Abur and Exposito (not owned) | R-050 |
| E12 | Network reduction (Ward, REI) | S24 | ETAP, PF, PW | none | own | Grainger94 sec. 14.6 | none | R-004, R-032 to R-034 |

## 2. Faults, protection and arc flash

| # | Engine | Matrix rows | Products seen offering the study | Quantic | Base | Owned books | Blocking gap | R-IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E13 | IEC 60909 fault engine (Ik'', ip, Ib, Ik, Ith; power station units) | F1 | all seven | partial (Ik'', ip, Ith) | pp plus own for Ib and Ik | Kasikci02, Das02 ch. 8 | IEC 60909-0 for q and lambda curves | R-023, R-024 |
| E14 | Sequence-network unbalanced faults and open conductors | F2, F8 | all seven (F2) | none | pp (1ph, 2ph) plus own (LLG) | Grainger94 ch. 11 to 12, Glover17 9.5 | none | R-023 to R-025 |
| E15 | ANSI C37 duty and device-rating check | F3, F7 | ETAP, PF, EasyPower, SKM, NEPLAN | none | own | Das02 ch. 5 and 7, Das21 | C37.010 curves | R-024 |
| E16 | Complete (superposition) fault from load flow | F6 | PF, NEPLAN, PW (part) | none | pp option | Kasikci02 | none | R-023 |
| E17 | Source decrement (IEC 61363, generator and motor decay) | F4, A5 | ETAP, PF; decay in EasyPower and SKM arc studies | none | own | Das02 sec. 6.4 | IEC 61363 | R-027 |
| E18 | DC fault engine (IEC 61660, IEEE 946) | F5 | ETAP, PF, EasyPower, SKM, NEPLAN | none | own time-domain RLC | Das02 ch. 9 | IEC 61660 curves (optional) | R-013 |
| E19 | TCC and device-timing engine with damage curves | P1, P2, P4 | ETAP, PF, EasyPower, SKM, NEPLAN | none | own | Alstom11 ch. 9, Das21 ch. 7 and 11 | manufacturer curve data | R-026, R-027 |
| E20 | Coordination rule checker and automatic settings | P3, P5, P9 | ETAP, PF, EasyPower (part), SKM | none | own | Alstom11 | site rules | R-026, R-030 |
| E21 | Distance and differential protection with CT and VT models | P6 to P8 | ETAP, PF, NEPLAN (P6) | none | own | Alstom11, Blackburn06 | none | none yet (matrix gap 2) |
| E22 | Arc-flash engine: IEEE 1584-2018, DGUV box test, DC and HV methods, integrated energy | A1 to A5 | ETAP, PF, EasyPower, SKM, NEPLAN | none | `arcflash-calc` plus own DGUV and integration | Das21 (Table 3.1 unreliable), DGUV-I 203-077 | none decided; IEEE 1584 purchase now optional | R-028 to R-030 |

## 3. Machines, dynamics and power quality

| # | Engine | Matrix rows | Products seen offering the study | Quantic | Base | Owned books | Blocking gap | R-IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E23 | Static motor-start dip | M1 | ETAP, PF, NEPLAN; EasyPower and SKM (part) | partial | pp | Das02 | none | R-009 |
| E24 | Motor acceleration, starters and parameter fitting | M2 to M4, X-4 | ETAP, PF, EasyPower, SKM, NEPLAN; PW (mod), PSS/E (part) | none | own ODE plus pp per step | Das02 sec. 12.10 to 12.11, Fitz03 ch. 6, Krause23, Bose02 | datasheet fitting source | R-015, R-016 |
| E25 | RMS dynamic solver: DAE, events, initialisation, user models | T1, T2, T5, T6 | all seven (T1) | none | own core; ANDES (GPL, separate process) to verify; FMI via FMPy | Kundur94 ch. 13, Sauer06 ch. 5 to 7 | IEEE 421.5 and IBR model sources | R-017 to R-022 |
| E26 | Small-signal and impedance-based stability, signal mode fitting | T3, X-3, PW-T1 | PF, NEPLAN; PW (SMIB) | none | own | Kundur94 ch. 12 | none | R-022 |
| E27 | EMT solver with measurement quantities and co-simulation | T4, X-1, X-2, X-7 | ETAP (mod), PF, NEPLAN (mod) | none | own MNA and trapezoidal core | Das10, Najm10 | frequency-dependent line models | R-020, R-044 |
| E28 | Harmonic load flow, frequency scan and filter design | H1, H2 | ETAP, PF, EasyPower, SKM, NEPLAN, PSS/E | none | DSS harmonic mode | Das02 ch. 19 to 20, Arrillaga03 | IEEE 519 limits as user data | R-014, R-034 |
| E29 | Flicker | H3 | ETAP, PF | none | own | none | IEC 61000-4-15 | R-051 |
| E30 | Geomagnetically induced currents | PW-S5 | PW, PSS/E | none | own | none | low priority for Zambia | R-036 |

## 4. Design calculators

| # | Engine | Matrix rows | Products seen offering the study | Quantic | Base | Owned books | Blocking gap | R-IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E31 | Cable sizing and thermal ampacity (IEC 60287, Neher-McGrath) | C1, C2 | ETAP, PF, SKM; EasyPower and NEPLAN (part) | none | own | Anders05 ch. 1, Morley ch. 8 | IEC 60287 tables | R-031, R-051 |
| E32 | Ground grid and earthing (IEEE 80 analytic, then field solver) | C6 | ETAP, SKM; EasyPower via partner | none | own | Morley ch. 7 (eq. 7.12 for Rm), DZS 691 | IEEE 80 (DZS 691 defers to it) | R-035 |
| E33 | Other calculators: transformer sizing, battery (IEEE 485), panel schedules, cable pulling, sag and tension | C3 to C5, C7, C8 | ETAP, SKM | none | own; linerate for sag (licence to check) | Gonen88 ch. 10 | IEEE 485, C57.91 | R-051 |
| E34 | Techno-economic comparison | X-5 | PF | none | own | none | none | R-012 |

## 5. Cross-cutting services (not physics, but every engine depends on them)

| # | Service | Matrix rows | Quantic | R-IDs |
| --- | --- | --- | --- | --- |
| E35 | Import and export with a loss ledger (RAW, DYR, AUX, DGS, CGMES) | D16 | none | R-037 to R-041 |
| E36 | Worked-trace and provenance reporting | G11, G13 | done (CC-7, WP-1.11) | R-042 to R-046 |
| E37 | Scenario, study-case and batch runner | D4 to D6, D15, PW-X1 | partial | R-003, R-005 |

## 6. What this shows

1. **Base libraries cover the network core, not the industrial engines.** pandapower and
   OpenDSS carry E2, E3, E7, E9, E11 and E28. The engines that sell to mines (E19, E20,
   E22, E24, E31, E32) are own builds, which is also where the margin is.
2. **Three blocking sources dominate:** IEC 60909-0 (E13), IEEE 80 (E32) and IEC 60287
   (E31). Each blocks constants, not methods (as in the engine index). Peter's ruling
   stands: no paid standards until release.
3. **Two owned books need care:** Das21 Table 3.1 is wrong for arc current coefficients,
   and our Das02 copy has corrupt pages. Both are recorded in the engine index.
4. **E36 is the differentiator to protect.** It already works, and no product's public
   material shows it (matrix G13).

## 7. Proposed build waves (for Peter's approval after research)

Updated from [notes/engine-index.md](notes/engine-index.md) with the WP-2.14 P0 order.
Each wave lists engines in the order they would be built.

| Wave | Engines | Why |
| --- | --- | --- |
| A | E2 (finish controls), E13 (Ib, Ik), E14, E23 then E24 | Mostly on pandapower; every industrial study needs them |
| B | E19, E20, E22 with E17 | The protection and arc-flash package mines pay for |
| C | E31, E32, E28 | Cable, earthing and drive harmonics complete an industrial study report |
| D | E25, E4, E18, E3 | Islanded gensets, DC systems and unbalanced networks |
| E | E7, E8, E9, E10, E11, E12, E26, E27, E5 and the rest | Platform parity with ETAP and PowerFactory |

E1, E35, E36 and E37 grow alongside every wave. WP-2.15 supplies the comparison cases
each engine must pass before it is called equivalent to a product.
