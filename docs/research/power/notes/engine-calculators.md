# Engine spec note: generator decrement (IEC 61363 style) and design calculators (WP-2.10)

This note covers matrix rows:

- F4: IEC 61363 transient decay;
- C3: cable pulling;
- C4: transformer sizing;
- C5: battery sizing;
- C7: panel schedules;
- C8: line sag and tension.

These are small engines, but clients use them often. ETAP sells most of them as separate
modules (dossier E21 and E41 to E42; 2026 release E91).

Paraphrased from owned references.

## 1. Generator fault decrement (F4)

**Source:** Das02 sec. 6.4.2 "Fault-decrement curve" (printed pp. 190 to 191, pdf pp. 205
to 206); Das10 ch. 10 (synchronous generator transients); Das02 ch. 7 analytical example
(`engine-ansi-short-circuit.md` sec. 5).

**The AC component** of a generator terminal fault current is the sum of a decaying
subtransient term, a decaying transient term and the steady state (eq. 6.13):

    iac(t) = (i''d − i'd)·e^(−t/T''d) + (i'd − id)·e^(−t/T'd) + id

where:

- i''d = E''/X''d and i'd = E'/X'd (eqs 6.14 and 6.16);
- the internal voltages are E'' = Va + X''d·sin φ and E' = Va + X'd·sin φ (prefault
  loading; eq. 6.15 and the transient analogue);
- the DC component decays with the armature time constant Ta;
- external reactance modifies the time constants (Das02 eqs 7.13 to 7.14,
  `engine-ansi-short-circuit.md`).

**IEC 61363-1** (ships and offshore; ETAP E12) builds the same per-machine decrement
curves (AC RMS, DC and peak against time) from a prefault load flow, then sums the
contributions. **Gap:** the standard is paid. The method is reproducible from the
machine equations above. The motor decrement follows Das02 sec. 6.10 and Das21 ch. 6.

**Uses in Quantic:**

- relay settings (decaying currents for generator-fed faults);
- the arc flash decaying-source integration (`engine-arc-flash.md` sec. 4);
- islanded mine power stations, where fault current collapses toward the steady state
  and overcurrent relays may not see it (voltage-restrained overcurrent, Das21
  sec. 7.12).

## 2. Line sag and tension (C8)

**Source:** Gonen88 ch. 10 "Sag and tension analysis" (printed pp. 623 to 650):

- temperature effects (sec. 10.2);
- catenary and parabolic methods for level supports (sec. 10.3.1, pp. 626 to 634);
- unequal supports (sec. 10.3.2);
- **ruling span** for unequal spans (sec. 10.4, p. 640);
- ice and wind loading (sec. 10.5, p. 641).

**Engine:**

- the catenary solution;
- a change-of-state equation between loading and temperature cases (to read in sec. 10.2
  and 10.5);
- the ruling span;
- clearance checks against DZS 418-1 Table 5-5 minimum heights, at the worst loading
  and temperature case as the code requires (no 11 kV row: see
  `zambia-regulatory-context.md`).

Pair it with `linerate` (MIT) for the ampacity side.

**What Gonen88 actually gives (read on the page images, pdf pp. 641 to 662,
2026-10-15):**

- Sec. 10.2 gives the two strain terms **separately**: thermal, Δl = l0·α·Δt
  (eq. 10.2), and elastic, Δl = l0·ΔT/(M·A) (eq. 10.3). It does **not** combine them
  into a change-of-state equation and has no worked change-of-state example.
- Combining them with the parabolic length l = L·(1 + w²L²/(24H²)) (eq. 10.8) gives the
  usual cubic in the new horizontal tension. That combination is **our derivation**,
  so it needs an external worked example before release (manufacturer stringing tables
  or a utility design manual; to fetch).
- Sec. 10.3 states the parabola error: under 0.5% in sag when sag is under 6% of span,
  about 2% at 10%. The engine should use the catenary throughout and report the
  parabolic value only as a check.
- Creep is treated qualitatively (sag template section, p. 650 onward): aluminium
  conductors creep for the life of the line, and the correction comes from
  **manufacturer creep curves**. Another manufacturer-data input.

**Worked examples recomputed:**

- Example 10.1 (p. 636): c = 1600 ft, L = 500 ft. Catenary length: book 502.032 ft,
  ours 502.037 ft (the book rounded sinh); parabolic length 502.0345 ft agrees exactly.
  Sag by catenary: 19.57 ft.
- Example 10.2 (p. 645, 795 kcmil ACSR, heavy loading): ice 0.9956 lb/ft, vertical
  2.0181 lb/ft, wind 0.6977 lb/ft, resultant 2.1353 lb/ft, design tension 14,250 lb
  (half the ultimate strength), sag 4.68 ft. All agree.

Both are in imperial units. The engine works in SI and the tests convert the inputs.

## 3. Transformer sizing and loading (C4)

- ETAP added "transformer load capability analysis" to IEEE C57.91 in 2026 (E91).
- **Method:** the C57.91 / IEC 60076-7 thermal model (top-oil and hot-spot rise with
  exponents and time constants; ageing acceleration factor). **Gap:** neither standard
  is owned. Our books cover transformer losses and sizing only partly; check Das10
  ch. 14 and the Schneider MV guide.
- **Simple sizing** (load list with demand and diversity factors, growth margin, and
  motor-start dip check) needs no standard and links to M1.

## 4. Battery sizing (C5)

- ETAP implements IEEE 485 duty-cycle sizing with temperature, ageing and design margin
  (E21, E41, E42).
- **Gap:** IEEE 485 is not owned. The method is a well-documented duty-cycle section
  calculation, but the cell-capacity factors (Kt) come from **manufacturer data**,
  which is the real input.
- Our books: Das02 ch. 9 (battery short circuit and internal resistance) and
  Masters04 (PV battery sizing for autonomy). **To read** for off-grid and UPS sizing
  in mine control rooms.

## 5. Panel schedules (C7) and cable pulling (C3)

- **Panel schedules:** ETAP's implementation is NEC-demand-based (dossier). For Zambian
  practice, use IEC/BS 7671-style demand and diversity. ETAP 2026 added BS 7671,
  IEC 60364 and NF C15-100 neutral and PE sizing (E91), which confirms the market wants
  IEC options. Low engineering risk, high convenience.
- **Cable pulling tension and sidewall pressure:** standard capstan-equation physics,
  with cable manufacturer limits. No owned source yet (gap; manufacturer pulling
  guides are public).

## 6. Gaps

1. IEC 61363-1, IEEE C57.91 / IEC 60076-7, IEEE 485 (paid).
2. Manufacturer battery Kt curves; cable pulling limits.
3. Gonen88 ch. 10 was read (sec. 2): it gives the strain components but no combined
   change-of-state equation or example. We need an external worked change-of-state
   case and manufacturer creep curves.
