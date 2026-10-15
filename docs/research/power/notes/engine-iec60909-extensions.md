# Engine spec note: IEC 60909 extensions (breaking and steady-state currents) (WP-2.10)

This note covers matrix row F1, where Quantic has Ik'', ip and Ith but lacks Ib and Ik.
It also covers F6 (superposition with load flow) and the IEC/ANSI comparison that ETAP
and PowerFactory both expose.

Paraphrased from owned references. Equations re-checked across two books where possible.

## 1. Sources

| Key | Source | Where |
| --- | --- | --- |
| Das02 | J. C. Das, *Power System Analysis*, 2002 | ch. 8, pdf pp. 282 to 310 |
| Kasikci02 | I. Kasikci, *Short Circuits in Power Systems: A Practical Guide to IEC 60909*, 2002 | ch. 11, printed pp. 92 to 104 |

The standard is IEC 60909-0 (2001 and 2016 editions), which we do not own. Some Das02
pages in our copy render blank in the PDF (corrupt streams), but their text layer is
intact (pdf pp. 293 and 298 for example), so the equations below come from the text
layer and are cross-checked with Kasikci02.

## 2. Terms and the ANSI mapping (Das02 sec. 8.1, Table 8-1)

| IEC | ANSI equivalent |
| --- | --- |
| Ik'' (initial symmetrical) | first-cycle symmetrical |
| ip (peak) | close and latch crest |
| Ib (symmetrical breaking, at minimum time delay tmin) | interrupting duty |
| Ik (steady state) | 30-cycle current |

IEC has no K factor and no post-multipliers. The asymmetry at tmin is computed directly
(pp. 282 to 284). Making capacity is 1.8·√2 (about 2.55) times the rated symmetrical breaking capacity (p. 283).

## 3. Far from and near to generator (Das02 secs 8.3 to 8.4)

**Far from generator:** Ik = Ib = Ik'' (eq. 8.1).

**Near to generator:** this applies when either:

- at least one synchronous machine contributes more than twice its rated current; or
- motors contribute more than 5% of Ik'' without motors (p. 290).

**Peak factor:** κ = 1.02 + 0.98·e^(−3R/X) (Kasikci02 eq. 11.23, p. 98).

**Meshed networks:**

- **Method A:** κ from the smallest R/X of the branches carrying 80% of the current;
  capped at 1.8 in LV.
- **Method B:** 1.15·κ from the fault-point R/X; capped at 1.8 in LV and 2.0 in HV.
- **Method C:** the equivalent-frequency method. Excite at 20 Hz (50 Hz systems) or
  24 Hz (60 Hz systems), then R/X = (Rc/Xc)·(fc/f).

Sources: Das02 sec. 8.3.2, pp. 289 to 290; Kasikci02 pp. 98 to 99. pandapower exposes
`kappa_method` B or C (see `engine-unbalanced-faults.md` sec. 6), which matches.

**Correction factors** (Das02 sec. 8.4):

- KG for generators directly connected (eq. 8.11).
- KG,PSU and KT,PSU for power station units on the LV side (eqs 8.13 to 8.16), and KPSU
  on the HV side with the tap and transformation ratios (eqs 8.17 to 8.19).
- Generator R from X''d: 0.05 (above 1 kV, 100 MVA or more), 0.07 (above 1 kV, under
  100 MVA), 0.15 (1 kV or less) (eq. 8.12). These also stand in for ac decay in the
  first half-cycle.
- The factors do **not** apply to negative- or zero-sequence impedances (p. 292).
- pandapower implements KG and KT. Check that it implements KPSU too.

**Motors** (Das02 secs 8.4.3 and 8.5):

- ZM from the locked-rotor current.
- R/X is 0.10, 0.15 or 0.42 for HV motors of at least 1 MW per pole pair, HV motors
  below that, and LV motor groups, respectively (eq. 8.20).
- An LV group is one equivalent motor with ILR/IrM = 5 and R/X = 0.42 (eq. 8.34).
- Neglect rules: motors behind two-winding transformers may be neglected below a
  ratio test (eq. 8.33).

## 4. Symmetrical breaking current Ib (new for Quantic)

**Single generator:** Ib = μ·Ik'' (eq. 8.21). μ depends on I''kG/IrG and the minimum
time delay tmin (Das02 eq. 8.22, p. 293; Kasikci02 Fig. 11.7, p. 100):

| tmin | μ |
| --- | --- |
| 0.02 s | 0.84 + 0.26·e^(−0.26·x) |
| 0.05 s | 0.71 + 0.51·e^(−0.30·x) |
| 0.10 s | 0.62 + 0.72·e^(−0.32·x) |
| 0.25 s or more | 0.56 + 0.94·e^(−0.38·x) |

Here x = I''kG/IrG; μ = 1 if x ≤ 2 (eq. 8.23). This is valid for turbine and
salient-pole generators and compensators with rotating exciters, or static exciters
under conditions; otherwise μ = 1 (p. 293). For asynchronous motors, use I''kM/IrM
(eq. 8.24).

**Asynchronous motors:** Ib = μ·q·Ik''. q depends on m = rated power per pole pair (MW)
and tmin. Kasikci02 (p. 102, OCR) lists:

| tmin | q |
| --- | --- |
| 0.02 s | 1.03 + 0.12·ln m |
| 0.05 s | 0.79 + 0.12·ln m |
| 0.10 s | 0.57 + 0.12·ln m |
| 0.25 s | 0.26 + 0.12·ln m |

q is capped at 1. **Discrepancy to resolve:** recollections of IEC 60909-0 give 0.10
(not 0.12) as the ln m coefficient for tmin ≥ 0.25 s. Das02's q equation (eq. 8.36) is
on pdf p. 298, which is blank in both the render and the text layer of our copy. **Do not code q at 0.25 s
until checked against IEC 60909-0 or a clean Das02 page.**

**Non-meshed networks:** sum the branch Ib values (eq. 8.28).

**Meshed networks:**

- Conservative: Ib = Ik'' (eq. 8.29).
- More accurate: Das02 eq. 8.30 subtracts per-machine decay terms weighted by the
  initial voltage differences ΔU''Gi and ΔU''Mj at the machine terminals (eq. 8.31).
  This needs per-source contribution tracking, which the engine needs anyway for device
  duties.

## 5. Steady-state current Ik

- **Generators:** Ik = λ·IrG, with λmax and λmin from IEC curves against Xd,sat (the
  inverse of the short-circuit ratio) and the excitation type (Series One and Series
  Two) (Das02 eqs 8.25 to 8.27, Fig. 8-7). **Gap: λ curves are figure data from IEC.**
- **Meshed networks:** Ik = Ik'' with motors neglected (eq. 8.32).
- **Asynchronous motors** contribute to Ik only for unbalanced faults (p. 296).

## 6. Superposition ("complete") method (F6)

IEC uses the equivalent voltage source c·Un/√3 and does not need a load flow (Das02
p. 286). For distribution and for validation against measurements, the superposition
method uses load-flow prefault voltages and load currents (Das02 p. 507; ETAP and
PowerFactory both offer it). pandapower supports it with `use_pre_fault_voltage`
("type C" in its docs). Quantic can expose IEC, ANSI and complete as three methods on
one network, which is what PowerFactory does.

## 6a. What pandapower 3.5.6 actually provides (source review, 2026-10-15)

Read from the installed package (`pandapower/shortcircuit/`), not from its docs:

- `calc_sc` accepts only `fault` in `["3ph", "2ph", "1ph"]` (`calc_sc.py` line 108).
  **There is no two-phase-to-earth (LLG) fault.** Quantic adds it from the sequence
  networks (`engine-unbalanced-faults.md`).
- Results are Ik'' (`ikss_ka`), ip (`ip_ka`) and Ith (`ith_ka`) for buses, lines and
  bus-bar switches.
- **Ib is not available.** `_calc_ib_generator` in `currents.py` (lines 235 to 299) is
  commented out in full. Its μ expressions match Das02 eq. 8.22, so the intended
  method is the one in sec. 4 above, but we must implement and test it ourselves.
- **Ik (steady state) is not computed.** No λ-based result exists. Sec. 5 stays an
  own implementation.
- **Power station unit correction is present:** `ppc_conversion.py` builds K_G, K_SG,
  K_T and K_ST from `gen.power_station_trafo` and `pg_percent`, with separate paths for
  on-load and off-load tap changers (lines 211 to 266). Quantic can reuse this for
  generator-transformer units instead of re-deriving the KS and KSO factors.

Consequence for wave A: pandapower supplies the impedance network, correction factors
and Ik'', ip and Ith. Quantic adds Ib (μ and q), Ik (λ) and LLG on top, reading
pandapower's ppci matrices rather than forking the package.

## 7. Verification cases

- Das02 Example 8.x and sec. 8.7 compare IEC and ANSI on the same network (pdf
  pp. 300 to 310). These are good cross-method tests.
- Kasikci02 ch. 19 worked networks (some of which our D11 IEC trace already uses).

## 8. Gaps

1. IEC 60909-0 itself, for λ curves, the q coefficient at tmin ≥ 0.25 s, and the 2016
   edition changes (for example, wind and PV full-converter source models). Recommended
   purchase.
2. Das02 pdf p. 298 (motor q equation, eqs 8.35 to 8.36) is missing from our copy. A clean copy or the standard is needed.
