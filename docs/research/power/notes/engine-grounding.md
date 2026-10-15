# Engine spec note: grounding systems and ground grids (WP-2.10)

This note covers matrix row C6 (ground grid design to IEEE 80, FEM, soil model) and
system grounding choices that feed F2 and the protection engine.

Mining relevance is direct. Mine grounding is regulated (safety ground beds,
high-resistance grounding for portable equipment), and surface substations and shovel
and dragline supplies need ground-bed design. Peter's sites (Copperbelt) are typical
clients.

Paraphrased from owned references. No tables are reproduced.

## 1. Sources

| Key | Source | Where |
| --- | --- | --- |
| Morley | L. A. Morley, *Mine Power Systems*, US Bureau of Mines IC 9258 | ch. 7 "Grounding", pdf pp. 184 to 206 (printed page = pdf page − 25; checked on rendered pdf pp. 188 and 194 = printed 163 and 169) |
| Das21 | J. C. Das, *Arc Flash Hazard Analysis and Mitigation*, 2nd ed., 2021 | ch. 4: system grounding and arc flash (solid, low and high resistance, ungrounded, resonant) |
| Das10 | J. C. Das, *Transients in Electrical Systems*, 2010 | grounding grid in transient contexts (lightning, GPR waves); to read when doing EMT |

The standards are IEEE 80 (AC substation grounding safety), IEEE 81 (soil and ground
impedance measurement), IEEE 142 (Green Book), IEC 60479 (effects of current on the
body) and the national mine regulations. We do not own them.

## 2. System grounding methods (Morley pdf pp. 185 to 186; Das21 ch. 4)

| Method | Fault current | Notes |
| --- | --- | --- |
| Ungrounded | very small, capacitive | No trip on the first fault and hard to locate. Transient overvoltages are amplified by distributed capacitance |
| Solidly grounded | thousands of amperes | Fast relaying, but flash and explosion hazard; avoid in explosive atmospheres |
| Low-resistance grounded | about 50 to 600 A, commonly about 400 A | Least sensitive ground relay should respond to 10% of maximum ground-fault current |
| High-resistance ("safety ground") | 50 A or less in general; 25 A or less where line-to-neutral voltage is 1,000 V or less; above 1,000 V, the grounding-circuit drop outside the resistor is 100 V or less | Required by US coal regulations for portable and mobile equipment. Needs sensitive relaying (a few amperes). No line-to-neutral loads |

The values in this table are Morley's statements of **US** practice (30 CFR).
**Zambian and South African mine rules must be sourced separately.** This is the same gap
as in `engine-cables.md` sec. 5.

**Engine implications:**

- The neutral grounding resistor sizes the ground-fault current, which feeds the zero
  sequence (3Rn, `engine-unbalanced-faults.md`).
- A rule-check module tests the chosen grounding scheme against the selected
  jurisdiction's limits, stored as data with citation.
- Ground-check monitoring and relay sensitivity tie into protection.

## 3. Body current limits (Morley pdf pp. 186 to 188)

Morley summarises the work of Dalziel and others:

- perception at about 1 mA AC;
- let-go limits (9 mA AC for men, 6 mA for women, 99.5% of the sample);
- respiratory paralysis at about 18 to 22 mA;
- fibrillation risk from about 50 to 500 mA.

Fibrillation current is proportional to body weight and inversely proportional to the
square root of shock duration (Dalziel). IEEE 80 builds its tolerable touch and step
voltages on this I = k/√t relation, with body weight 50 kg or 70 kg.

**Gap:** the exact k constants and the touch and step formulas (with surface-layer
derating Cs) are in IEEE 80. Morley's text gives the principle; the formula on the next
page has not been read cleanly. **Do not code limits until checked against IEEE 80 or a
clean page.**

## 4. Electrode and grid resistance (Morley pdf pp. 193 to 196)

- **Single driven rod and multi-rod beds:**
  - formulas for rods spaced much wider than their length, and much closer than their
    length (geometric-mean spacing);
  - mutual resistance makes a group worse than parallel resistors unless the spacing is
    large (Figs 7.22 to 7.23).
- **Grounding mesh** (Schwarz form, Morley eq. 7.10, printed p. 169, checked on the
  rendered page):

      R = ρ/(πL) · [ ln(2L/√(2az)) + k1·L/√B − k2 ]

  where:
  - L is the total length of buried conductor;
  - a is the conductor radius (the radius symbol is not defined in the page's where-list,
    but it is used in the formula);
  - z is the burial depth;
  - B is the enclosed area;
  - k1 and k2 are shape coefficients read from curves (Figs 7.24 and 7.25) against the
    length-to-width ratio and depth. For a roughly square mesh a few feet deep, Morley
    gives k1 ≈ 1.3 and k2 ≈ 6.
- **Combined rods and mesh:** R = (R1·R2 − Rm²)/(R1 + R2 − 2Rm) (eq. 7.11), with
  mutual resistance Rm = ρ/(πL)·[ ln(2L/ℓ) + k1·L/√B − k2 + 1 ] (eq. 7.12), where ℓ is
  the length of one rod. Checked on the rendered page. Adding a mesh to a rod bed seldom cuts resistance more than 10 to 15% in
  uniform soil, but it smooths potential gradients.
- **Quick estimate (Laurent, eq. 7.13):** R ≈ ρ/(4r) + ρ/L, where r is the equivalent
  radius (about half the longest diagonal) and L is the total buried conductor length.
  Checked on the rendered page.
- **Other shapes** (Morley Table 7.3, after Dwight): stars, rings, strips and plates.
  **The table is not to be copied.** Dwight's 1936 paper (AIEE) is the original and is
  old enough that it may be public domain in the US. To check.
- **Contact resistance** can add about 20% in new beds (p. 194).
- **Always verify by measurement** with an earth tester.

Equations 7.10 to 7.13 were checked on the rendered page (2026-10-15). The multi-rod
formulas and Table 7.3 shapes were not checked yet.

**US mine practice** (printed p. 163):

- safety and system ground beds are kept separate;
- bed resistance is maintained at 5.0 Ω or less ("low-resistance ground bed");
- the step and touch circuits around a grounded structure are shown in Morley's
  Figs 7.7 and 7.8.

**Check in the engine:** GPR = I × Rg. Morley's example is 10 kA of lightning into
5 Ω, giving 50 kV.

## 5. Soil (Morley pdf pp. 196 to 200)

- **Two-layer earth** changes both resistance and surface potentials. Morley's Fig. 7.26
  shows potentials for a mesh in the top layer.
- **Wenner four-electrode method:** ρ = 2πaR, valid when the electrode depth is much
  less than the spacing a (pdf p. 199).
  - Practical issues: stray currents, natural electrolysis currents, polarisation (avoid
    DC), lead inductance and leakage.
  - Apparent resistivity against spacing gives the layer structure. Fitting a two-layer
    model to a Wenner curve is a standard inverse problem, done by least squares in
    commercial tools.
- **Seasonal variation:** deeper rods and meshes are more stable.

## 6. Engine design (C6)

1. **Soil model:** uniform, or two-layer fitted from Wenner data. Show the fit residuals
   in the trace.
2. **Grid geometry:** conductors and rods in 3D.
3. **Method A (analytic, IEEE 80 style):** Rg, mesh voltage Em and step voltage Es from
   empirical factors, then compare with tolerable touch and step limits. **Needs IEEE 80
   (gap).**
4. **Method B (numerical):** subdivide conductors into segments and apply a
   method-of-moments or boundary element solution with Green's functions for layered
   soil. This gives the current distribution, ground potential rise (GPR), surface
   potentials and the touch and step maps. This is what the "FEM" options in ETAP and
   CDEGS are. Fully implementable from published physics; verify against IEEE 80 annex
   examples.
5. **Split factor:** the fraction of fault current flowing into the grid as opposed to
   overhead ground wires and cable sheaths. It uses the unbalanced-fault engine's
   zero-sequence currents.
6. **Outputs:**
   - Rg and GPR;
   - touch and step voltage contour maps;
   - pass or fail against limits;
   - conductor sizing for fault current (I²t, as in `engine-cables.md` sec. 4).

## 7. Gaps

1. IEEE 80 (paid): tolerable limits, Cs derating, Em/Es factors, annex examples. A
   recommended purchase, alongside IEEE 1584, IEC 60909 and C37.010.
2. Zambian and South African mine grounding rules.
3. Clean reads of Morley's ground-bed equations (render pdf pp. 193 to 195).
4. Open-source: no permissive ground grid solver was identified in this pass. To
   search (for example, Python method-of-moments grounding codes on GitHub).
