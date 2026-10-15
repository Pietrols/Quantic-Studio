# Engine spec note: cable ampacity, sizing and withstand (WP-2.10)

This note covers matrix rows:

- C1: cable sizing;
- C2: ampacity to IEC 60287 and Neher-McGrath;
- C8: overhead line ampacity;
- S8: temperature-corrected resistance;
- P2 for cables: short-circuit withstand.

Mining extras come from Morley.

Paraphrased from owned references. No tables are reproduced.

## 1. Sources

| Key | Source | Where |
| --- | --- | --- |
| Anders05 | G. J. Anders, *Rating of Electric Power Cables in Unfavorable Thermal Environment*, IEEE Press/Wiley, 2005 | ch. 1 (printed pp. 1 to 70): a review of the IEC 60287 and Neher-McGrath method; ch. 2 to 5 for crossings, backfills, real-time rating |
| Morley | L. A. Morley, *Mine Power Systems*, US Bureau of Mines IC 9258, 1990 | ch. 8 (cables; ampacity at pdf pp. 220 to 222), ch. 10 (trailing-cable trip settings at pdf pp. 300 to 301). The text file has no printed page numbers, so pdf pages are cited |
| linerate | Statnett, `linerate` (PyPI, v5.0.0, 2026-08-19): CIGRE TB 601, TB 207, IEEE 738 overhead line ampacity | https://pypi.org/project/linerate (read 2026-10-15) |
| pypacity | Universidad de Cantabria, `pypacity`, IEEE 738 and CIGRE TB 601, **GPL-3.0-only**, alpha | https://pypi.org/project/pypacity/ (read 2026-10-15) |

Standards (not owned):

- IEC 60287-1-1, -2-1 and -3-1 (steady-state rating);
- IEC 60853 (cyclic and emergency);
- IEC 60949 (non-adiabatic short-circuit);
- IEC 60364-5-52 (LV installation tables);
- ICEA and NEC ampacity tables;
- IEEE 835;
- IEEE 738.

## 2. Steady-state rating (IEC 60287 form), Anders05 sec. 1.4

The lumped thermal ladder per unit length is:

- conductor losses Wc;
- dielectric losses Wd;
- sheath losses λ1·Wc;
- armour losses λ2·Wc;
- thermal resistances T1 (insulation), T2 (bedding), T3 (serving) and T4 (external).

**Rating equation, buried cable, no drying** (eq. 1.40, p. 21):

    I = sqrt( (Δθ − Wd [0.5 T1 + n (T2 + T3 + T4)]) /
              (R T1 + n R (1 + λ1) T2 + n R (1 + λ1 + λ2)(T3 + T4)) )

where:

- Δθ is the permitted conductor temperature rise above ambient;
- n is the number of loaded conductors;
- R is the ac resistance at maximum operating temperature.

**Variants:**

- **Partial soil drying** (two-zone model from CIGRE, adopted by IEC; eqs 1.46 to 1.51,
  pp. 22 to 24). Let v = ρ_dry / ρ_moist and Δθx = the critical isotherm rise. The
  numerator gains (v − 1)·Δθx, and T4 becomes v·T4 in both the numerator and the
  denominator.
- **Cables in air with solar gain** (p. 24). The numerator gains σ·De·H·T4*, where σ is
  solar absorption, De is the diameter and H is the irradiance. T4* is the in-air
  external resistance adjusted for sun.

## 3. Parameters (Anders05 sec. 1.6)

**Conductor ac resistance** (sec. 1.6.2, pp. 38 to 40):

- R' (dc at θ) = ρ20 / A · (1 + α20 (θ − 20)).
- R = R' (1 + ys + yp), or R' (1 + 1.5 (ys + yp)) in magnetic pipes or conduits.
- Skin and proximity factors ys and yp come from xs and xp, which depend on frequency,
  R' and the constants ks and kp (IEC 60287 table). The expressions apply for
  xp ≤ 2.8; beyond that, use the alternative formulas cited in Anders05.
- Material constants checked in Anders05 (p. 39):
  - copper: ρ20 = 1.7241e-8 Ω·m, α20 = 3.93e-3 /K;
  - aluminium: ρ20 = 2.8264e-8 Ω·m, α20 = 4.03e-3 /K.

  The same R(θ) is needed for load-flow temperature correction (S8).

**The remaining parameters:**

- Dielectric losses Wd (sec. 1.6.3): these matter only at high voltage.
- Sheath loss factor λ1 (sec. 1.6.4): depends on bonding (single-point, both-ends,
  cross-bonded), formation and transposition. It is large for both-ends-bonded
  single-core cables.
- Armour loss factor λ2 (sec. 1.6.5).
- Thermal resistances T1, T2 and T3 (sec. 1.6.6): logarithmic in diameters, with
  material resistivity.

**External thermal resistance T4** (sec. 1.6.6.5, pp. 60 to 64). This is over 70% of the
temperature rise for buried cables.

- **Single buried cable:** a log of 4L/De form, where L is depth to axis and De is the
  outer diameter. It comes from the image method under an isothermal ground surface.
- **Groups:** a mutual heating factor F, which is a product over the other cables of
  image-distance over distance ratios. The hottest cable governs. Cables must be at least
  two diameters apart for superposition to hold. The sheath-loss inequality modifies F
  for flat single-core formations.
- **Load factor:** a separate T4 is computed for joule losses using the loss-load factor
  μ = 0.3·LF + 0.7·LF² (p. 60). It acts beyond a diameter set by soil diffusivity
  (about 211 mm for a daily cycle and typical soil).
- **Backfill or duct bank:** a geometric factor added for the different resistivity
  envelope (Neher and McGrath, later extended). It is valid for length-to-width ratio
  below 3 (p. 62).
- **Ducts and pipes:** T4 = T4' (air gap, with constants U, V and Y per installation
  type) + T4'' (duct wall) + T4''' (outside duct) (p. 63).

**Transient and cyclic** (sec. 1.5, pp. 24 to 35): two-loop ladder reduction, step
response, superposition for variable load, and the cyclic rating factor. This is the
IEC 60853 basis.

## 4. Sizing workflow (C1)

For each cable, the engine checks every criterion and reports the governing one.

1. **Ampacity:** derated for installation, grouping, ambient, soil and depth. Use the
   IEC 60287 calculation (above) or tabulated methods. **Gap:** IEC 60364-5-52 and NEC
   tables are copyrighted, so the user or library supplies them, as with ETAP's
   "many standards".
2. **Voltage drop:** at full load and at motor starting (links to M1 and M2).
3. **Short-circuit withstand:** the adiabatic I²t ≤ K²S² with a material and insulation
   constant K, or non-adiabatic per IEC 60949. **Gap:** K constants and the IEC 60949
   method are not in our books yet; Das21 or Morley may have the ICEA form. Read next.
   The protective device clearing time comes from the protection engine.
4. **Earth-fault loop impedance** for disconnection time (IEC 60364-4-41): links to the
   unbalanced fault engine (Kasikci02 p. 95, minimum single-phase current).

## 5. Mining-specific (Morley, US Bureau of Mines IC 9258)

- **Ampacity basis** (pdf pp. 220 to 221): mining practice uses insulation temperature
  classes 75 °C and 90 °C, with 60 °C legacy, at 40 °C ambient. ICEA ratings are
  preferred for engineered systems. Morley states NEC ampacities are about 25% higher
  than ICEA for comparable cases.
- **Trailing cables on reels:** derating by number of layers wound (ICEA and Australian
  factors), and heating on reels (pdf pp. 221 to 222). Mining machines (shuttle cars,
  draglines) run cables on reels, so this is a real client need.
- **Trailing-cable instantaneous trip limits** by conductor size and system voltage
  (ch. 10, the 'recommended instantaneous trip settings' tables for ac and dc trailing cables, pdf pp. 300 to 301). These come from US 30 CFR practice. A rule-check
  feature for US-regulated mines.
  - **Gap:** Zambian and South African equivalents (Mines Health and Safety Act
    regulations, SANS 10108 and others) need sourcing for our home market.
- **Licence note:** Morley is a US government publication. Its tables abstract ICEA
  data, so treat the table values as third-party data, not public domain, until checked.

## 6. Overhead line ampacity (C8)

- **linerate** (Statnett): CIGRE TB 601, TB 207 and IEEE 738, steady-state and
  transient. **Licence not shown on PyPI: check the repository before use.** It is a
  strong candidate dependency if it is permissive.
- **pypacity:** GPL-3.0-only, so it can only run as a separate process (AGENTS.md
  rule 7). Prefer linerate.
- Sag and tension: Gonen 1988 (owned) to read.

## 7. Open-source status for underground cables

No permissive IEC 60287 Python library was found (search 2026-10-15). The commercial
tools are CYMCAP (Eaton) and ETAP UGS, both cited in the dossiers. We implement IEC 60287
ourselves from Anders05 sec. 1.4 to 1.6. We verify against Anders05's model-cable
numerical examples (ch. 1, "model cable No. 1", pp. 18 to 19) and, if Peter buys it,
IEC TR 62095 or the IEC 60287 worked examples. Finite-element verification (as
SINTEF and Anders do) is a later step.

## 8. Gaps

1. Copies of IEC 60287-1-1, -2-1 and -3-1 (paid) for exact tables (ks, kp, material
   thermal resistivities, U, V and Y). Anders05 quotes some, which is enough to verify
   but not to copy.
2. Short-circuit K constants and IEC 60949 adiabatic and non-adiabatic method.
3. Zambian and South African mining regulations for cable protection.
4. linerate licence.
