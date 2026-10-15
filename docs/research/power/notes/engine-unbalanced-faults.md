# Engine spec note: unbalanced (unsymmetrical) shunt faults (WP-2.10)

This note covers matrix rows F2 (SLG, LL and LLG faults) and part of F1 (the IEC 60909
unbalanced currents). ETAP and PowerFactory both offer all three fault types in the ANSI
and IEC methods (see `etap.md` and `powerfactory.md`). Quantic has only the three-phase
fault.

Everything here is paraphrased from the owned books, which were used to verify only.
Equations are standard results. Each one cites where it was checked.

## 1. Sources

| Key | Book | Where |
| --- | --- | --- |
| Grainger94 | J. J. Grainger and W. D. Stevenson, *Power System Analysis*, international ed., McGraw-Hill, 1994 | ch. 11 (from printed p. 416), ch. 12 (printed pp. 470 to 509) |
| Glover17 | J. D. Glover, T. J. Overbye, M. S. Sarma, *Power System Analysis and Design*, 6th ed., Cengage, 2017 | sec. 9.5, printed pp. 567 to 569 |
| Kasikci02 | I. Kasikci, *Short Circuits in Power Systems: A Practical Guide to IEC 60909*, Wiley-VCH, 2002 | ch. 11, printed pp. 92 to 96 |
| pandapower | pandapower short-circuit docs, `calc_sc` | https://pandapower.readthedocs.io/en/latest/shortcircuit/run.html (read 2026-10-15) |

## 2. Method (Zbus superposition), Grainger94 ch. 12

1. Build three sequence networks (section 3) and their bus impedance matrices Z1, Z2, Z0.
   Prefault voltage Vf is in the positive network only, and prefault load current is
   neglected (industry practice, printed p. 475).
2. For a fault at bus k, each network reduces to its Thevenin impedance, the diagonal
   element Zkk(n) (pp. 472 to 474).
3. Interconnect the Thevenin equivalents as the fault type dictates and solve for the
   sequence fault currents If(0), If(1), If(2) (section 4).
4. Treat −If(n) as an injection at bus k. Then for every bus j:
   - Vj(1) = Vf − Zjk(1) If(1)
   - Vj(2) = −Zjk(2) If(2)
   - Vj(0) = −Zjk(0) If(0)

   Only column k of each matrix is needed (eqs 12.4 to 12.6, pp. 475 to 476).
5. Branch sequence currents come from the sequence voltage difference across the branch
   divided by its sequence series impedance. Phase quantities come from the
   symmetrical-component matrix A (a = 1∠120°): [Va, Vb, Vc] = A [V0, V1, V2].
6. **Phase shift.** The sequence Zbus matrices omit Δ-Y phase shifts. Their results are
   referred to the side of the network that contains the fault. For buses on the other
   side of a Δ-Y or Y-Δ transformer, shift positive and negative sequence quantities
   separately before combining them:
   - ANSI convention: stepping from LV to HV, advance positive sequence by 30° and retard
     negative sequence by 30° (eq. 11.88, pp. 456 to 459);
   - stepping down reverses both.

   This is required for correct phase values on the far side of the transformer
   (pp. 498 to 499). The engine should take the vector group from the transformer data,
   not assume ANSI. The IEC vector group clock number gives the shift.

**Glover17 eqs 9.5.1 to 9.5.8 (pp. 568 to 569)** state the same per-fault-type
equations in Zbus form. They are a second check.

## 3. Sequence network construction (Grainger94 ch. 11)

- **Positive network:** the usual network, with machines at subtransient, transient or
  steady-state reactance as the study demands.
- **Negative network:** the same as positive, with machine negative-sequence impedances
  and no sources (p. 463).
- **Zero network:**
  - Neutral impedance Zn appears as 3Zn, because all three phases' zero-sequence current
    flows through it (sec. 11.3; machines sec. 11.7).
  - Neutral impedances are absent from the positive and negative networks (p. 463).
- **Transformers:** the zero-sequence path depends on the winding connection. Grainger94
  Fig. 11.17 (p. 450, checked visually) gives five cases:
  1. **Y-Y, both neutrals grounded:** series path P to Q through the leakage impedance
     plus 3ZN and 3Zn.
  2. **Y-Y, one neutral grounded:** open between P and Q, so no zero-sequence current
     flows.
  3. **Δ-Δ:** isolated on both sides.
  4. **Grounded Y-Δ:** the grounded-Y side is connected to reference through the leakage
     impedance (plus 3ZN); the Δ side is open.
  5. **Ungrounded Y-Δ:** open on both sides.

  Series impedances of all sequences are usually taken as equal for transformers
  (p. 459). Three-winding transformers and zigzag grounding banks need their own cases.
  **Gap:** not in this chapter, so read Grainger94 sec. 2.7 or Glover17 next.
- **Lines:** the zero-sequence impedance comes from geometry, earth return and ground
  wires. This is linked to matrix S11 (line constants, Grainger94 ch. 4 to 6, sec. 11.6).

## 4. Fault equations (Zf is the fault impedance)

The equations below use Zkk(1), Zkk(2) and Zkk(0) for the Thevenin impedances seen at bus k.

**Single line-to-ground, phase a** (eq. 12.12, p. 484): the three networks are in series
with 3Zf.

    If(0) = If(1) = If(2) = Vf / (Zkk(1) + Zkk(2) + Zkk(0) + 3Zf)

**Line-to-line, phases b and c** (eq. 12.17, p. 490): positive and negative networks in
parallel through Zf. Zero sequence is inactive.

    If(1) = −If(2) = Vf / (Zkk(1) + Zkk(2) + Zf),   If(0) = 0

**Double line-to-ground, b and c to ground** (eqs 12.24 to 12.26, pp. 495 to 496): the
negative network in parallel with (zero network + 3Zf).

    If(1) = Vf / (Zkk(1) + Zkk(2)(Zkk(0)+3Zf) / (Zkk(2)+Zkk(0)+3Zf))
    If(2) = −If(1) (Zkk(0)+3Zf) / (Zkk(2)+Zkk(0)+3Zf)
    If(0) = −If(1) Zkk(2) / (Zkk(2)+Zkk(0)+3Zf)

With Zf infinite, this reduces to the LL case (p. 496).

## 5. IEC 60909 unbalanced currents (Kasikci02 ch. 11)

The IEC method uses the equivalent voltage source c·Un/√3 at the fault point. The voltage
factor c is already handled in our IEC three-phase engine (F1). In the impedance terms
below, the sequence impedances are the IEC-corrected ones.

| Fault | Current | Where |
| --- | --- | --- |
| Line-to-line, no earth | Ik2'' = c Un / \|Z1 + Z2\| | eq. 11.10, p. 94 |
| Line-to-line with Z1 = Z2 | Ik2'' = (√3/2) Ik3'' | eq. 11.11, p. 94 |
| Line-to-line-to-earth, earth current | IkE2E'' = √3 c Un / \|Z1 + 2Z0\| (with Z1 = Z2) | eq. 11.9, p. 93 |
| Single line-to-earth | Ik1'' = √3 c Un / \|Z1 + Z2 + Z0\| | eqs 11.15 to 11.18, p. 95 |

Kasikci02 (p. 94) notes that a line-to-line fault without earth contact can exceed the
three-phase current near large asynchronous motors.

**Minimum single-phase current** (p. 95): this is used for protection checks, the
disconnection condition under IEC 60364 and maximum cable lengths. It uses:

- the minimum voltage factor;
- motors neglected;
- LV conductors at their elevated end-of-fault temperature;
- the network state that yields the smallest current.

**Which fault is largest** (p. 96, Fig. 11.5): this depends on the ratio of Z0 to Z1 and
the neutral treatment. The figure's validity needs the impedance angles within 15° of
each other. Our engine should simply compute all fault types and report the maximum, not
rely on the chart.

Peak ip and thermal Ith for unbalanced faults use the same κ and m and n approach as the
three-phase case, applied to the unbalanced Ik''. **To verify against IEC 60909-0 before
coding:** we do not own the standard.

## 6. Open-source foundation

pandapower `calc_sc` supports `fault` values `3ph`, `2ph` and `1ph`, with `case` max or
min, fault impedance (`r_fault_ohm`, `x_fault_ohm`), `ip`, `ith`, `branch_results`,
and a superposition variant (`use_pre_fault_voltage`) (docs read 2026-10-15). It does
**not** list a double line-to-ground fault.

The plan for Quantic:

1. Reuse pandapower for IEC `2ph` and `1ph` (same engine as our F1).
2. Add our own Zbus sequence solver for LLG, for ANSI-mode unbalanced faults, and for
   the Grainger-style post-fault bus voltages with Δ-Y phase shifts.
3. Cross-check the two on common cases.

The data each element needs for zero sequence (pandapower field names such as
`r0_ohm_per_km`, `vector_group`, `x0x_max`) goes to the contract WP.

## 7. Reference cases for tests (results only, cited, not copied)

- Grainger94 Examples 12.1 to 12.5 (pp. 478 to 499): a two-generator system with
  sequence Zbus. The examples give SLG, LL and LLG currents, plus remote-bus voltages
  with and without the Δ-Y shift. This is the best end-to-end check, including the
  phase-shift step.
- Glover17 sec. 9.5 examples (pp. 569 onward): a second independent set.
- Kasikci02 ch. 19 worked networks: the IEC 60909 unbalanced values.

The test fixtures record inputs and expected values with page numbers in
`docs/sources/entries/`, as for D11.

## 8. Gaps

1. Open-conductor (series) faults and simultaneous faults (matrix F8): Grainger94
   sec. 11.9 covers unsymmetrical series impedances only. We need a source such as
   P. M. Anderson, *Analysis of Faulted Power Systems*, which we do not own.
2. Three-winding and zigzag transformer zero-sequence models: read Glover17 and Das02
   ch. 2 next.
3. IEC 60909-0 itself (paid) for the unbalanced ip and Ith, and for the transformer
   correction factor KT on the zero sequence.
