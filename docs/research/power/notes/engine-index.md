# Engine index: what each engine needs, what to build on, what blocks it (WP-2.10)

This is the summary of the `engine-*.md` spec notes, written as input to WP-2.12
`engines.md`. Status reflects main on 2026-10-15. The priority column is a proposal for
Peter. It weighs value to mining and industrial clients (Quantic's market) against
effort.

## Table

**Base column codes:** pp = pandapower; DSS = OpenDSS via DSS-Python; VG = VeraGrid
(GridCal); own = implement ourselves.

| Engine | Spec note | Matrix rows | Book basis | Base | Blocking gap | Mining value | Proposed priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Balanced load flow and controls | engine-load-flow-extensions | S1 to S9 | Das02 ch. 11 to 13, Glover17 ch. 6 | pp (done for S1, S3) | none | high | 1 (finish taps, shunts, islands) |
| IEC 60909 Ib and Ik | engine-iec60909-extensions | F1 | Das02 ch. 8, Kasikci02 | pp for Ik'', ip, Ith and power station units; own for Ib and Ik (pp 3.5.6 has Ib commented out and no Ik) | q at tmin ≥ 0.25 s; λ curves (IEC 60909) | high | 1 |
| Unbalanced faults | engine-unbalanced-faults | F2 | Grainger94 ch. 11 to 12, Glover17 9.5, Kasikci02 | pp (1ph, 2ph only; LLG rejected by `calc_sc`) + own (LLG, ANSI) | none | high | 1 |
| Motor starting and acceleration | engine-motors | M1 to M4, S7 | Das02 12.10 to 12.11, Fitz03 ch. 6, Krause23 | own ODE + pp per step | datasheet fitting source | very high | 1 |
| Protection, TCC | engine-protection-tcc | P1 to P5 | NPAG ch. 9, Das21 ch. 7, 11 | own (pp protection reviewed: teaching model only) | C37.112 form; manufacturer curve data | very high | 2 |
| Arc flash | engine-arc-flash | A1 to A4 | Das21 ch. 3, 5, 6 (tables unreliable); DGUV-I 203-077 | `arcflash-calc` (MIT, verified against Annex D.1; approved by Peter 2026-10-15); DGUV method own | none (decided); DGUV kP check against DGUV-I 203-077 text | very high (paid service) | 2 |
| Cable sizing and ampacity | engine-cables | C1, C2, C8, S8 | Anders05 ch. 1, Morley ch. 8 | own (IEC 60287); linerate (licence to check) for overhead | IEC 60287 tables; K constants; local mine rules | high | 2 |
| ANSI C37 duty | engine-ansi-short-circuit | F3, F7 | Das02 ch. 5, 7; Das21 ch. 5, 7 | own | C37.010 local curves; X/R 15 or 17 | medium (US-style plants) | 3 |
| Grounding and ground grid | engine-grounding | C6 | Morley ch. 7 | own (analytic now, MoM later) | IEEE 80; local mine rules | high | 3 |
| Harmonics and filters | engine-harmonics | H1, H2 | Das02 ch. 19 to 20 | DSS | IEEE 519 tables (user data) | high (VFDs, mills) | 3 |
| DC short circuit | engine-dc-short-circuit | F5, S12 | Das02 ch. 9 | own (time-domain RLC) | IEC 61660 curves (optional) | medium (traction, batteries) | 4 |
| Unbalanced and distribution load flow | engine-load-flow-extensions | S10, F8 | Das02 ch. 14 | DSS | Kersting | medium | 4 |
| Transient stability | engine-transient-stability | T1 to T3, T5 | Kundur94 ch. 13, Sauer06 ch. 5 to 7 | own core; ANDES (external) to verify; Dynawo later | IEEE 421.5 models; WECC and IEC 61400-27 IBR models; genset governors | high (islanded mines) | 4 |
| EMT (switching, inrush, TRV, lightning) | engine-emt | T4 | Das10, Najm10 | own MNA and trapezoidal core shared with qe_circuit; VeraGrid EMT to evaluate | frequency-dependent line models; TRV envelopes | high (capacitor and VFD interaction, inrush) | 5 |
| Generator decrement and calculators (sag, transformer, battery, panel, pulling) | engine-calculators | F4, C3 to C5, C7, C8 | Das02 6.4, Gonen88 ch. 10 | own; linerate | IEC 61363, C57.91, IEEE 485; manufacturer data | medium (convenience features) | 4 |
| Contingency, PTDF, LODF | engine-planning-operations | S15, S16, S24 | Grainger94 ch. 14 | pp DC and AC | none | medium | 5 |
| Voltage stability | engine-planning-operations | S17 | Kundur94 ch. 14 | VG CPF | Q-limit handling check | medium to high (weak feeds) | 5 |
| State estimation | engine-planning-operations | S18 | Grainger94 ch. 15 | pp estimation | Abur and Expósito | low | 6 |
| OPF, dispatch, microgrid | engine-planning-operations | S14, S26 | Das02 ch. 15 to 16, Grainger94 ch. 13 | pp OPF, VG | none | medium (genset, PV, BESS) | 6 |
| Reliability | engine-planning-operations | S23 | Glover17 (thin) | own | Billinton and Allan; IEEE 493 data | high as a sales argument | 6 |

## Cross-cutting findings

1. **Book errata found while re-computing** (recorded in each note, so we do not copy
   them into tests):
   - Das02 Table 7-5 row F1 (crest and rms multipliers);
   - Das02 Example 9.2 (1/δ printed 15.6 ms, actually 1.56 ms);
   - Das21 eq. 5.7 (1/S missing);
   - Das21 eq. 7.1 typesetting (1/I_PKP);
   - Das02 eq. 19.31 (r2h) and eq. 19.21 (X) are doubtful as printed;
   - Das02 Example 7.1 motor M3 multiplier class;
   - Das21's 2021 claim about arc flash decay is out of date for ETAP.
   - Das10 eq. 6-1 source inductance (5.08 × 10⁻⁴ H printed, 0.533 mH from the stated
     impedance) and Example 6-5 inrush (1633 A printed, 1565 A from eq. 6-7);
   - Gonen88 Example 10.1 catenary length (502.032 ft printed, 502.037 ft; rounding).
   - **Das21 Table 3.1 (IEEE 1584 arcing-current coefficients) has errors that put MV
     arcing current off by 30 to 60%.** Proven against IEEE Annex D.1 values
     (`engine-arc-flash.md` sec. 6b). Never key coefficients from Das21.
2. **Corrupt pages in our Das02 copy:** pdf pp. 236 and 298 are blank, and pp. 293 and
   297 render blank but have a text layer. Ask whether a cleaner copy exists.
3. **Paid standards block constants, not methods.** Every engine can be built from the
   books and open libraries; the standards are needed for certification-grade constants
   and verification cases. Suggested purchase order:
   1. IEEE 1584-2018 (now optional: Peter approved `arcflash-calc` on 2026-10-15);
   2. IEC 60909-0:2016;
   3. IEEE 80;
   4. IEEE C37.010;
   5. IEC 60287-1-1.

   Books to add: Kersting (distribution), Billinton and Allan (reliability).
4. **Local regulations are a real gap for the home market:** Zambian and South African
   mine electrical rules (grounding limits, trailing cables, protection). They decide
   pass or fail in reports for Peter's actual clients.
5. **The differentiator is not new physics.** ETAP 2026 already covers almost every
   study. Quantic's edges are:
   - an open, documented JSON contract;
   - the worked trace with equations and sources (G13);
   - verified reproductions of textbook and standard examples, published as tests;
   - mining-specific packaging (trailing cables, reeled-cable derating, ground beds,
     mill and conveyor starts, islanded gensets);
   - price.

## Suggested build order (for the parity matrix and Peter's approval)

| Wave | Contents | Why |
| --- | --- | --- |
| A | IEC Ib and Ik, unbalanced faults, motor acceleration, load-flow controls | Small, mostly built on pandapower, and the base for everything else |
| B | Protection and TCC, arc flash, cable sizing | The mining study package that clients pay for (short circuit, coordination, arc flash labels, cable checks) |
| C | Grounding, harmonics (OpenDSS), ANSI duty | Second-tier studies that complete an industrial study report |
| D | Transient stability, DC systems, unbalanced load flow | Larger engines, needed for islanded mines and traction |
| E | Planning and operations (contingency, voltage stability, SE, OPF, reliability) | Platform parity |
