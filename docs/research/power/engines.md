# Power engine inventory

WP-2.12, Claude, 2026-10-17. Every calculation engine the seven products imply, which
Quantic has, which it lacks, what we would build on and which owned books verify it.
Companion to [parity-matrix.md](parity-matrix.md). Research synthesis; the build order
at the end is a proposal for Peter, not an approved plan.

WP-2.22 independent re-review, ChatGPT, 2026-10-18: all E1-E37 rows checked
against the post-WP-2.20 matrix. Corrections were posted to Claude before editing.
Product lists below mean a **stated subset**, not complete engine equivalence.
The audit disposition and dated upstream licence checks are in sections 8-10.

## How to read it

- **Evidence.** This decomposition is inferred, not a recovered vendor implementation.
  Each row is an **I** (inferred) responsibility, derived from **S** (seen) evidence that a product offers
  the study the engine serves. The matrix rows carry that S evidence and its citations;
  this table cites them by row ID. "Engines implied" in each dossier (ETAP and
  PowerFactory section 8, PowerWorld section 8, other products section 8 per product)
  is the source of the split.
- **Quantic:** `done`, `partial` or `none` on `main` on 2026-10-17.
- **Base:** pp = pandapower (BSD-3-Clause, L1); DSS = alternative OpenDSS engine
  via DSS-Python (BSD wrapper, mixed backend/component terms, L2); VG =
  VeraGrid (MPL-2.0, L3); `arcflash-calc` (MIT, L4, approved by
  Peter 2026-10-15); own = implement ourselves. GPL tools (ANDES) run only as separate
  processes for verification (AGENTS.md rule 7).
- **Books** use the short names in [notes/engines-library-map.md](notes/engines-library-map.md).
  Book errata already found are listed in [notes/engine-index.md](notes/engine-index.md).
  These are existing owned-inventory/search locators, not newly page-verified sources.
  No owned material was copied or used to adopt a new formula in this review.
  "None" in a blocking-gap cell does not waive final standard editions, manufacturer
  data, source page checks, local rules or validation. See [mining-regulations.md](mining-regulations.md).
- **R-IDs** link to [reconstruction-requirements.md](reconstruction-requirements.md).

## 1. Network and steady state

| # | Engine | Matrix rows | Products seen offering the study | Quantic | Base | Owned books | Blocking gap | R-IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | Network model, type library and topology processor (switch states, islands, identity maps) | D1 to D4, D11, G2, G7, S9, PW-D1 | all seven D1; type/instance and topology breadth qualified per D2/G2/S9 | partial | own on CC-3 contracts | Grainger94, Glover17 | none | R-001 to R-004 |
| E2 | Balanced AC load flow with controls (Q limits, taps, remote regulation, shunts, phase shifters, droop) | S1 to S9 | all seven S1; control subsets S3-S9 only, not every control in every product | partial (S1, S3 done) | pp | Glover17 ch. 6, Das02 ch. 11 to 13, Kundur94 | none | R-007, R-008, R-010 |
| E3 | Unbalanced phase-domain load flow | S10, F8 | ETAP (mod), PF, EasyPower, SKM (mod), NEPLAN (S10); open-conductor faults are E14, not unbalanced LF | none | DSS | Das02 ch. 14 | Kersting (not owned) | R-013 |
| E4 | Physical DC network flow and AC/DC coupling | S12; PW-S1 approximation is separate | ETAP, PF, EasyPower, SKM (mod), NEPLAN (S12); PW HVDC is partial, not general physical DC | none | own | Das02 ch. 9 | none | R-013 |
| E5 | Line and cable constants from geometry, neutral reduction | S11, S8, C8 | ETAP, PF, PW, NEPLAN S11; SKM calculator subset; C8 geometry/thermal breadth separate | none | own | Grainger94, Gonen88, Arrillaga03 | none | R-031 to R-034 |
| E6 | Time-series and quasi-dynamic orchestrator | D8, S13 | ETAP (mod), PF (mod), PW, NEPLAN (part), PSS/E (mod), S13 | none | own on CC-4 time runner (WP-2.3) | none needed | profile data per site | R-012 |
| E7 | Sensitivities, distribution factors, contingency orchestrator, RAS | S15, S16, PW-S2 | PF/PW/NEPLAN/PSS/E S15-S16; ETAP contingencies only, S16 U; EasyPower manual what-if only | none | pp | Grainger94 ch. 14 | none | R-011 |
| E8 | Transfer capability and voltage stability (continuation P-V, Q-V, modal) | S17, PW-S3 | ETAP, PF, PW, NEPLAN (part), PSS/E S17; PW-S3 transfer modes separately qualified | none | VG CPF (MPL-2.0; L3), candidate | Kundur94 ch. 14, Sauer06 | Q-limit handling check | R-011, R-012 |
| E9 | Optimisation: OPF, dispatch, unit commitment, reserves | S14, S26, PW-S4 | ETAP/PF S14+S26; PW dispatch/reserves and NEPLAN dispatch partial; PSS/E OPF only, commitment U | none | pp OPF | Glover17, Grainger94 ch. 13, Das02 ch. 15 to 16 | commitment/reserve/ramp constraints beyond basic pp OPF; independent validation | R-012 |
| E10 | Probabilistic, hosting capacity, reliability | S19, S22, S23 | PF S19/S22/S23; ETAP S19/S23, S22 U; NEPLAN hosting/reliability; EasyPower/SKM reliability only | none | own | Glover17 (thin) | Billinton and Allan (not owned); ETAP patent E112 needs reading before any hosting-capacity method | R-050 |
| E11 | State estimation and load allocation | S18, S25 | ETAP/PF/NEPLAN S18/S25, with ADMS/module and feeder-scaling scope retained | none | pp estimation | Grainger94 ch. 15 | Abur and Exposito (not owned) | R-050 |
| E12 | Network reduction (Ward, REI) | S24 | ETAP, PF, PW (variants U), NEPLAN S24 | none | own | Grainger94 sec. 14.6 | none | R-004, R-032 to R-034 |

## 2. Faults, protection and arc flash

| # | Engine | Matrix rows | Products seen offering the study | Quantic | Base | Owned books | Blocking gap | R-IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E13 | IEC 60909 fault engine (Ik'', ip, Ib, Ik, Ith; power station units) | F1 | ETAP, PF, EasyPower, SKM, NEPLAN, PSS/E F1; PW flat IEC 909 subset, edition/full duty U | partial (Ik'', ip, Ith) | pp plus own for Ib and Ik | Kasikci02, Das02 ch. 8 | IEC 60909-0 for q and lambda curves | R-023, R-024 |
| E14 | Sequence-network unbalanced faults and open conductors | F2, F8 | all seven F2; only PF full F8, ETAP/PW partial; unbalanced faults do not prove open conductors | none | pp documented fault subsets; own missing open-conductor/sequential logic | Grainger94 ch. 11 to 12, Glover17 9.5 | none | R-023 to R-025 |
| E15 | ANSI C37 duty and device-rating check | F3, F7 | ETAP, PF, EasyPower, SKM, NEPLAN F3; F7 workflow/rating coverage qualified per product | none | own | Das02 ch. 5 and 7, Das21 | C37.010 curves | R-024 |
| E16 | Complete (superposition) fault from load flow | F6 | PF, NEPLAN F6; PW pre-fault-profile subset, not full-method equivalence | none | pp option | Kasikci02 | none | R-023 |
| E17 | Source decrement (IEC 61363, generator and motor decay) | F4, A5 | ETAP, PF, SKM F4; EasyPower/SKM A5 decay evidence is not by itself IEC 61363 evidence | none | own | Das02 sec. 6.4 | IEC 61363 | R-027 |
| E18 | DC fault engine (IEC 61660, IEEE 946) | F5 | PF/NEPLAN standard-specific F5; ETAP IEEE 946 (IEC 61660 U); EasyPower/SKM DC fault subsets | none | own time-domain RLC | Das02 ch. 9 | IEC 61660 curves (optional) | R-013 |
| E19 | TCC and device-timing engine with damage curves | P1, P2, P4 | ETAP, PF, EasyPower, SKM, NEPLAN P1/P2/P4; PW/PSS/E timed-event subsets P4 only | none | own | Alstom11 ch. 9, Das21 ch. 7 and 11 | manufacturer curve data | R-026, R-027 |
| E20 | Coordination rule checker and automatic settings | P3, P5, P9 | ETAP/PF/EasyPower/SKM P3/P5; NEPLAN distance-setting subset P5, general checks U; P9 scope per cell | none | own | Alstom11 | site rules | R-026, R-030 |
| E21 | Distance and differential protection with CT and VT models | P6 to P8 | ETAP/PF/NEPLAN P6/P7; EasyPower differential only; CT/VT saturation breadth qualified per P8 | none | own | Alstom11, Blackburn06 | none | R-025, R-053, R-054 |
| E22 | Arc-flash engine: IEEE 1584-2018, DGUV box test, DC and HV methods, integrated energy | A1 to A5 | ETAP/PF/EasyPower/SKM/NEPLAN A1; other A rows are method/range-specific subsets, not universal coverage | none | `arcflash-calc` plus own DGUV and integration | Das21 (Table 3.1 unreliable), DGUV-I 203-077 | current local rules, method/range validation and timing coupling; library approval is not compliance certification | R-028 to R-030 |

## 3. Machines, dynamics and power quality

| # | Engine | Matrix rows | Products seen offering the study | Quantic | Base | Owned books | Blocking gap | R-IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E23 | Static motor-start dip | M1 | ETAP, PF, NEPLAN M1; EasyPower/SKM partial | partial | pp | Das02 | none | R-009 |
| E24 | Motor acceleration, starters and parameter fitting | M2 to M4, X-4 | all seven M2 with PW module/PSS/E subset; M3 starter breadth qualified; M4 datasheet fitting only ETAP/EasyPower/NEPLAN | none | own ODE plus pp per step | Das02 sec. 12.10 to 12.11, Fitz03 ch. 6, Krause23, Bose02 | datasheet fitting source | R-015, R-016 |
| E25 | RMS dynamic solver: DAE, events, initialisation, user models | T1, T2, T5, T6 | all seven T1; T2/T5/T6 subsets differ, including PF RMS-only diagnostics and ETAP T6 U | none | own core; ANDES (GPL, separate process) to verify; FMI via FMPy | Kundur94 ch. 13, Sauer06 ch. 5 to 7 | IEEE 421.5 and IBR model sources | R-017 to R-022 |
| E26 | Small-signal and impedance-based stability, signal mode fitting | T3, X-3, PW-T1 | PF/NEPLAN T3; PW SMIB only; X-3 impedance-based analysis PF only, fitted signal modes separate | none | own | Kundur94 ch. 12 | none | R-022 |
| E27 | EMT solver with measurement quantities and co-simulation | T4, X-1, X-2, X-7 | ETAP/PF/NEPLAN T4; PSS/E external companion only; PF X-1/X-2, NEPLAN partial; X-7 ETAP/NEPLAN | none | own MNA and trapezoidal core | Das10, Najm10 | frequency-dependent line models | R-020, R-044 |
| E28 | Harmonic load flow, frequency scan and filter design | H1, H2 | ETAP/PF/EasyPower/SKM/NEPLAN H1/H2; PSS/E H1 only; PW GIC/external GICHarm subset, general harmonics U | none | DSS harmonic mode | Das02 ch. 19 to 20, Arrillaga03 | IEEE 519 limits as user data | R-014, R-034 |
| E29 | Flicker | H3 | ETAP, PF, NEPLAN H3 | none | own | none | IEC 61000-4-15 | R-051 |
| E30 | Geomagnetically induced currents | PW-S5 | PW, PSS/E PW-S5 | none | own | none | low priority for Zambia | R-036 |

## 4. Design calculators

| # | Engine | Matrix rows | Products seen offering the study | Quantic | Base | Owned books | Blocking gap | R-IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E31 | Cable sizing and thermal ampacity (IEC 60287, Neher-McGrath) | C1, C2 | ETAP/PF/SKM C2; all five industrial products C1 with EasyPower/SKM/NEPLAN sizing subsets; NEPLAN C2 U | none | own | Anders05 ch. 1, Morley ch. 8 | IEC 60287 tables, installation/material data and local mine rules | R-031, R-051 |
| E32 | Ground grid and earthing (IEEE 80 analytic, then field solver) | C6 | ETAP/SKM C6; EasyPower partner XGSLab; NEPLAN advertised grounding only, FEM/soil method U | none | own | Morley ch. 7 (eq. 7.12 for Rm), DZS 691 | IEEE 80; final ZS 691 versus owned draft reconciliation; local applicability | R-035 |
| E33 | Other calculators: transformer sizing, battery (IEEE 485), panel schedules, cable pulling, sag and tension | C3 to C5, C7, C8 | ETAP C3-C5/C7/C8; SKM C3-C5/C7; EasyPower sizing/panel subsets C4/C7; battery and sag breadth not implied | none | own; linerate for thermal ampacity only (MIT; L5), mechanical sag/tension own | Gonen88 ch. 10 | IEEE 485, C57.91 | R-051 |
| E34 | Techno-economic comparison | X-5 | PF, NEPLAN X-5 | none | own | none | none | R-012 |

## 5. Cross-cutting services (not physics, but every engine depends on them)

| # | Service | Matrix rows | Quantic | R-IDs |
| --- | --- | --- | --- | --- |
| E35 | Import and export with a loss ledger (RAW, DYR, AUX, DGS, CGMES) | D16 | none | R-037 to R-041 |
| E36 | Worked-trace and provenance reporting | G11, G13 | G13 done (CC-7, WP-1.11); general G11 reporting partial | R-042 to R-046 |
| E37 | Scenario, study-case and batch runner | D4 to D6, D15, PW-X1 | partial | R-003, R-005 |

## 6. What this shows

1. **Base libraries cover the network core, not the industrial engines.** pandapower and
   OpenDSS carry E2, E3, E7, E9, E11 and E28. The engines that sell to mines (E19, E20,
   E22, E24, E31, E32) are own builds, which is also where the margin is.
2. **Three blocking sources dominate:** IEC 60909-0 (E13), IEEE 80 (E32) and IEC 60287
   (E31). Tables, methods, scope, editions and applicability still require checking;
   an open implementation is not authority to claim standards compliance. Peter's ruling
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

## 8. Independent row audit, 2026-10-18

All rows above were compared to their cited matrix rows. Book names were checked
against existing research inventories/engine notes only, not against newly fetched
owned pages. Bases remain candidate designs (I), not executed capabilities. No
standard-compliance conclusion follows from a licence or book title.

| Engine | Audit disposition: evidence, base and remaining verification |
| --- | --- |
| E1 | D1 is S for all seven, but shared database does not prove uniform type/instance semantics. Own contracts are a partial base; topology and import identities still need fixtures. |
| E2 | Corrected stale "others S1 only"; controls are product-specific. pp runpp documents reactive limits, distributed slack and voltage-dependent loads [B1], but Quantic exposes a subset. Book locators retained, algorithm/options must be pinned. |
| E3 | S10 supports the five industrial products; F8 is a different fault responsibility. DSS is a candidate phase-domain base with component-licence review L2 and missing dedicated distribution reference. |
| E4 | Removed PW-S1 as proof of physical DC networks: linear DC approximation differs from batteries/chargers and converter coupling. Own formulation, DC material/validation gaps remain. |
| E5 | Added NEPLAN geometry/mutual evidence and SKM calculator subset. Existing Grainger/Gonen/Arrillaga locators are leads; reduction conventions and sequence/phase bases need validation. |
| E6 | Added NEPLAN partial S13. Quasi-dynamic is an operating-point orchestrator, not dynamic DAE; own runner still needs profile/time/convergence semantics. |
| E7 | ETAP S16 is U, so contingencies cannot imply PTDF/LODF. EasyPower manual what-if is not N-k/RAS automation. pp is a candidate, not a complete RAS engine. |
| E8 | Added NEPLAN partial S17 and qualified transfer modes. VG licence now verified, CPF/Q-limit behaviour and book page authority remain to check. |
| E9 | OPF, dispatch, commitment and reserves are distinct. PSS/E S14 does not establish commitment; pp OPF does not supply a validated unit-commitment scheduler. Added constraint gap. |
| E10 | ETAP S22 U retained; added NEPLAN hosting/reliability and EasyPower/SKM reliability only. Billinton gap and patent-review gate retained; no patented method reconstructed. |
| E11 | Added NEPLAN S18/S25. Estimation versus feeder scaling/load allocation differ. pp estimation candidate; observability, bad-data and Abur reference gaps remain. |
| E12 | Added NEPLAN Ward/REI evidence; PW variants remain U. Own implementation and reduction/identity fixtures required. |
| E13 | Qualified PW flat IEC/edition-U subset. Current upstream pp docs advertise 1/2/3-phase supported short-circuit options [B2], not every duty quantity; pinned Quantic implementation is narrower. IEC curves and generator-duty gaps retained. |
| E14 | F2 is not open-conductor/sweep support. Replaced overspecific pp fault list with version-dependent documented subsets [B2]; missing switching/open-conductor logic remains own work. |
| E15 | F3/F7 qualifications retained: standard duty is not every manufacturer's device-rating workflow. C37 and device data remain gaps. |
| E16 | PF/NEPLAN complete method and PW pre-fault subset kept separate. pp pre-fault voltage option [B2] is only a candidate; motor/converter assumptions require comparison. |
| E17 | Added SKM IEC 61363 F4. Arc decay evidence cannot establish that standard. Own decrement source/edition and arc-timing coupling remain gaps. |
| E18 | Kept IEEE 946/IEC 61660 product distinctions, especially ETAP IEC U. Own RLC concept is not standards compliance; DC source/time-constant data missing. |
| E19 | Added PW/PSS/E timed-event subsets without implying TCC libraries. Manufacturer tolerances, settings and clearing decomposition remain blocking data. |
| E20 | Added NEPLAN distance-only settings; general rules remain U. Automatic settings, coordination checking and maintenance modes cannot be conflated. Site rules required. |
| E21 | Added EasyPower differential subset; ETAP CT saturation does not prove VT saturation. Corrected missing requirement claim to R-025/R-053/R-054. CT/VT and relay data remain necessary. |
| E22 | All five A1 sources support different method/range subsets. MIT implementation approval is not jurisdictional compliance or a complete DC/HV/box-test engine; local rules and timing validation added as gaps. |
| E23 | Existing M1 subsets retained; pp snapshot dip is not acceleration or contactor ride-through. Actual load/motor and acceptance criteria remain needed. |
| E24 | Split M2 acceleration, M3 starter sets and M4 fitting. PF M4 U remains despite generic X-4 identification. Own ODE/network coupling and datasheet-fit authority remain gaps. |
| E25 | T1 all seven retained; initialisation/user-model breadth differs. ANDES external only L6, FMPy host L7 does not supply licensed plant models. Machine/governor/IBR sources and event validation remain gaps. |
| E26 | PF/NEPLAN eigenvalues, PW SMIB and PF impedance analysis are not interchangeable. Own linearisation, reference-frame/model bandwidth and mode fitting require separate checks. |
| E27 | Added PSS/E external companion and NEPLAN hybrid/measurement subsets. MNA/theta proposal is I, not vendor internals; frequency-dependent line data and inrush/measurement oracles remain gaps. |
| E28 | Kept PSS/E H1 only and qualified PW external GIC-harmonics. DSS harmonic solve is not a complete filter-design/limit-allocation workflow; site impedance, spectra and current ZS 387 still required. |
| E29 | Added NEPLAN Pst/Plt evidence. Meter implementation/aggregation and IEC 61000-4-15 source remain gaps; annual yield or RMS variance is not flicker. |
| E30 | PW/PSS/E S evidence retained, own base. "Low priority" is a proposal, not proof of negligible site risk; geography/ground-conductivity data and physical method remain unverified. |
| E31 | NEPLAN/EasyPower sizing does not establish duct-bank/IEC 60287 thermal solving. Added local rules and installation/material gaps; Anders/Morley inventory locators retained. |
| E32 | Added NEPLAN advertised grounding, method U. Final ZS 691 versus owned DZS and IEEE 80 dependencies are explicit; an earth-resistance result alone cannot certify touch/step safety. |
| E33 | Product subsets qualified. linerate README [B3] establishes overhead thermal rating, not a mechanical sag solver. Own mechanical model, manufacturer properties, IEEE 485/C57.91 and clearance rules remain gaps. |
| E34 | Added NEPLAN investment present-value subset; PF source X-5 retained. Own financial assumptions/cashflow timing and tariff provenance still required. |
| E35 | D16 remains partial per product. No converter chosen or tested here; loss ledger, supported schema versions and R-037-R-041 fixtures remain prerequisites (WP-2.24). |
| E36 | Corrected blanket done: G13 trace capability done, G11 general reports partial. Existing CC-7/WP-1.11 are provenance, not a regulatory certificate. Rule-profile gaps remain explicit. |
| E37 | D4-D6/D15/PW-X1 support the orchestration responsibility, not equal revision/merge semantics in every product. Quantic partial, distributed runner and scenario reproducibility still unbuilt. |

## 9. Dated upstream licence audit

Every file below was read through its upstream repository on **2026-10-18**.
Blob SHA identifies the exact text read, not an installed package version. No
dependency is added or approved by this table. A moving default branch must be
rechecked against the exact release and its dependency notices before shipping.

| ID | Library / actual upstream file | Observed licence and reuse boundary | File blob SHA |
| --- | --- | --- | --- |
| L1 | [pandapower LICENSE](https://github.com/e2nIEE/pandapower/blob/develop/LICENSE) | BSD-3-Clause; preserve attribution/notices and non-endorsement condition. Does not license all third-party code or datasets automatically | 3768e1ffd742ff0a04dfb673741ad0099a433a77 |
| L2a | [DSS-Python LICENSE](https://github.com/dss-extensions/DSS-Python/blob/master/LICENSE) | BSD-3-Clause wrapper for an alternative OpenDSS implementation, not identical to EPRI's binary | e445e1fbeb4176321e9c2ce2bd3468ceea604e0c |
| L2b | [DSS C-API OPENDSS_LICENSE](https://github.com/dss-extensions/dss_capi/blob/master/OPENDSS_LICENSE) and [LICENSE](https://github.com/dss-extensions/dss_capi/blob/master/LICENSE) | EPRI-derived notice and C-API BSD-style terms both read. Binary dependency/component licences still matter | b6ed217a22c977284209e1ac8cb1dd4881790074; ce5c7dfad25854f20324f7e859ee01b37c289d28 |
| L2c | [backend LICENSE.BSD3](https://github.com/dss-extensions/dss_python_backend/blob/master/LICENSE.BSD3), [LICENSE.LGPL3](https://github.com/dss-extensions/dss_python_backend/blob/master/LICENSE.LGPL3), [README](https://github.com/dss-extensions/dss_python_backend/blob/master/README.md) | Backend explicitly mixes BSD3/LGPL3 source and LGPL libraries (including KLUSolveX/KLU). Review exact binary, linking/replacement, source/notice duties and per-file SPDX; do not call the full stack all-BSD | BSD3 750348e90641035588b84e52b74334c8dd40f14a; LGPL3 0a041280bd00a9d068f503b8ee7ce35214bd24a1 |
| L3 | [VeraGrid engine LICENSE.txt](https://github.com/SanPen/VeraGrid/blob/master/src/VeraGridEngine/LICENSE.txt), identical to root LICENSE.md | MPL-2.0. File-level source obligations for covered modifications; separate-file integration is not a blanket exemption from notices or bundled dependencies | 14e2f777f6c395e7e04ab4aa306bbcc4b0c1120e |
| L4 | [arcflash-calc upstream LICENSE.txt](https://github.com/LiaungYip/arcflash/blob/main/LICENSE.txt) | MIT; preserve notice. Package identity is arcflash-calc, not unrelated packages named arcflash; exact version validation still needed | a4b47544d19c7c75755dae3d6c83c806b969acbe |
| L5 | [linerate LICENSE](https://github.com/statnett/linerate/blob/main/LICENSE) | MIT; preserve notice. Thermal capability boundary independently checked in README, not inferred from licence | e0e8e71cc70edb3130cbf64da37c0e3ff1dad89b |
| L6 | [ANDES LICENSE](https://github.com/cuihantao/andes/blob/master/LICENSE) | GPL-3.0-or-later, explicit project preamble. AGENTS rule 7: separate process only, never import. Process separation is not a waiver of distribution duties | 74ae8d9ead6c7ad2baa3f68d8146cc00eecdadf6 |
| L7 | [FMPy LICENSE.txt](https://github.com/CATIA-Systems/FMPy/blob/main/LICENSE.txt) | Core BSD-2-Clause; file also includes CC BY 4.0/MIT asset notices, FMI header/schema terms with modification condition, and SUNDIALS BSD notices. FMUs have their own licences | 579c4250fc9f48cf38b0c72b70a1f7d3c44be733 |

Actual upstream files support these descriptions, not a legal opinion or blanket
shipping approval. Existing Quantic lock pins pandapower 3.5.6; online latest docs
read here identify 4.0.0. No claim is made that every current upstream option exists
in that pin, and no update is performed.

## 10. Base evidence and source-index closure

- B1: [pandapower balanced AC power flow, latest docs, 4.0.0](https://pandapower.readthedocs.io/en/latest/powerflow/ac.html), accessed 2026-10-18. Methods/options vary by solver; Q-limit enforcement and fallback behaviour require pinned-version tests. No documented numeric default adopted.
- B2: [pandapower short-circuit currents, latest docs, 4.0.0](https://pandapower.readthedocs.io/en/latest/shortcircuit/currents.html), accessed 2026-10-18. Supported fault/pre-fault options are not all fault-device/transient duties.
- B3: [linerate README](https://github.com/statnett/linerate/blob/main/README.md), blob f0b444f4537d35f3a369096632e6673942fe88a0, accessed 2026-10-18. Thermal ampacity/temperature purpose, not demonstrated mechanical sag/tension.

E113 and E114 are now indexed in [notes/etap-sources.md](notes/etap-sources.md)
with the original WP-2.18 date and this recheck date. Scanning source-entry YAML
IDs against [notes/powerfactory-sources.md](notes/powerfactory-sources.md) found no
unindexed P IDs; a dated closure note is added there without inventing new IDs.
No matrix cells, book-derived formulas, contracts, build waves or dependency pins
were changed by this audit.
