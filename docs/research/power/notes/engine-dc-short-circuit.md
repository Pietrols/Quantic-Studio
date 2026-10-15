# Engine spec note: DC short-circuit currents (IEC 61660 and classical methods) (WP-2.10)

This note covers matrix rows:

- F5: DC faults;
- S12: DC systems, partially;
- C5: battery sizing, partially;
- A3: DC arc flash, which needs these currents.

Mining relevance: DC traction (trolley haulage and locomotives), DC drives on older
hoists and mills, and substation battery systems.

Paraphrased from the owned book. No figures or worked examples are reproduced. The two
worked results quoted below are re-computed here as checks.

## 1. Sources

| Key | Source | Where |
| --- | --- | --- |
| Das02 | J. C. Das, *Power System Analysis: Short-Circuit, Load Flow and Harmonics*, 2002 | ch. 9, pdf pp. 317 to 342 |
| Das21 | J. C. Das, *Arc Flash Hazard Analysis and Mitigation*, 2nd ed., 2021 | ch. 15 (DC short circuit and DC arc flash), to read |

**Standards:**

- **IEC 61660-1 (1997):** DC auxiliary installations in power plants and substations.
  Not traction.
- **IEEE 946:** DC auxiliary systems.
- **ANSI/IEEE C37.14:** DC power circuit breakers.
- **IEEE 485:** battery sizing.
- **General Electric publication** (Das02 ref. 1): the classical method.

Das02 states there is no ANSI/IEEE calculation standard for DC short circuit (p. 317).

## 2. IEC 61660 standard current shape (Das02 sec. 9.1)

Each source's current is approximated by:

- a rise from zero to the peak ip at time tp, with rise time constant τ1 (eq. 9.1):
  i1(t) = ip (1 − e^(−t/τ1)) / (1 − e^(−tp/τ1));
- after the peak, a decay toward the quasi steady-state current Ik (the value at 1 s)
  with time constant τ2 (eq. 9.2): i2(t) = ip [(1 − α) e^(−(t − tp)/τ2) + α], where
  α = Ik/ip (eq. 9.3).

If a source has no distinct peak, as with a rectifier with a smoothing reactor, eq. 9.1
alone applies.

## 3. Sources and their parameters

**Lead-acid battery** (sec. 9.3):

- **Classical model:** EB behind (RB + connector R) and the cell-circuit and cell-row
  inductances.
  - i = EB/R · (1 − e^(−Rt/L)) (eq. 9.5);
  - maximum current EB/R;
  - initial di/dt = EB/L.
- **Internal resistance RB:**
  - from manufacturer data (preferred);
  - from IEEE plate-resistance data (eqs 9.8 to 9.9);
  - from rule-of-thumb formulas (eqs 9.10 to 9.11).

  Das02 Example 9.1 shows a factor-of-three spread between methods, so **manufacturer
  data is required** (p. 323).
- **Connector and cell-row inductances:**
  - two round conductors: L = (μ0/π)(0.25 + ln(d/r)) per metre of loop (eq. 9.12);
  - cell rows treated as parallel bus bars (eq. 9.13).
- **IEC method** (pp. 324 to 326):
  - multiply RB by 0.9 for the maximum case;
  - if the open-circuit voltage is unknown, EB = 1.05·UnB, with UnB = 2.0 V per cell
    for lead-acid;
  - ipB = EB / RBBr, where RBBr is the total resistance with 0.9·RB (eq. 9.14);
  - time to peak and rise time constant come from IEC curves, entered with
    1/δ = 2/(RBBr/LBBr + 1/TB) and TB = 30 ms (eq. 9.15);
  - decay τ2B = 100 ms;
  - Ik = 0.95·EB / (RBBr + 0.1·RB) (eq. 9.16).
  - **Check:** with the book's inputs (RBBr = 18.238 mΩ, EB = 1.05 × 120 V), ipB = 6909 A
    and IkB = 5956 A, matching Das02 Example 9.2. Re-computed 2026-10-15.
  - **Book slip:** Example 9.2 prints 1/δ = 15.6 ms, but its own eq. 9.15 gives
    2/(18.238e-3/14.61e-6 + 1/30e-3) = 1.56 ms. The curve readings it then uses (tp about
    4.3 ms, τ1 about 0.75 ms) fit 1.56 ms, so the printed 15.6 is a decimal slip. Checked
    on the rendered pdf p. 325.
  - Inductances in this example are in µH. The text extraction shows "mH"; the rendered
    page shows µH.

**DC motors and generators** (sec. 9.4):

- **Classical model** (eq. 9.17): two exponentials. The armature decrement controls the
  rise and peak; the field decrement controls the decay.
  - peak = e0/r'd per unit;
  - di/dt depends on the unsaturated armature inductance L'a = 19.1·Cx·V/(P·N·Ia)
    (eq. 9.23);
  - Cx is 0.4 or 0.1 for motors (without or with pole-face windings) and 0.6 or 0.2 for
    generators (p. 329).
  - The transient resistance r'd comes from 1950 AIEE graphical data (Das02 ref. 5).
    **Gap:** not in our library.
- **IEC method:** RMB, LMB and τM (eqs 9.27 to 9.28), and the quasi steady-state current
  scaled by the field inductance ratio LF/L0F (eq. 9.29). The rest is from IEC curves.

**Rectifiers** (sec. 9.5):

- The peak occurs about half a cycle after the fault, from AC-side DC offset. A smoothing
  reactor can remove it.
- The equivalent resistance comes iteratively from the rectifier regulation curve, using
  the commutating impedance on the rectifier transformer base (pp. 333 to 338).

**Charged capacitors** (sec. 9.6):

- ipC = κC·EC / RCBr (eq. 9.58).
- κC, tpC and the factors for τ1C and τ2C come from IEC curves entered with
  1/δ = 2·LCBr/RCBr and ω0 = 1/sqrt(LCBr·C) (eqs 9.59 to 9.61).
- If LCBr = 0, then κC = 1 and tpC = 0.
- Steady-state current is zero.

**Total current** (sec. 9.7):

- At a fault with no common branch: sum the partial time functions.
- With a common branch: add its R and L to each source circuit, then apply an IEC
  correction factor σj to each source's ip and Ik (eq. 9.62).
- The book's combined example peaks at about 9 ms, with the rectifier dominant. Profiles
  must be summed in time, not by peaks (p. 340).

**Maximum and minimum conditions** (pp. 320 to 321):

| Condition | Maximum | Minimum |
| --- | --- | --- |
| Conductor resistance | at 20 °C | at maximum temperature |
| Joint resistance | ignored | included |
| Rectifier current limiting | ineffective | rated short-circuit current |
| Decoupling diodes | neglected | included |
| Battery | fully charged | at final voltage |

Fuse and device current limiting is included in both cases.

## 4. Engine design

**Inputs:**

- a DC network: sources by type, branches with R and L, a common branch;
- source data, with the manufacturer's RB and inductances;
- the maximum or minimum case.

**Outputs:**

- per source: ip, tp, τ1, τ2, Ik and the i(t) curve;
- the total i(t) at the fault;
- the peak and the time to peak;
- device duty checks: DC breaker peak and short-time rating, per ANSI C37.14 or IEC.

**IEC curve factors.** κ, tp, τ1 and τ2 factors for battery, capacitor, rectifier and
motor come from IEC 61660-1 figures. **Gap: we need the standard (paid). The curves
cannot be copied from Das02 figures.** Until then:

- the classical R-L methods (battery, motor) and a direct time-domain RLC simulation
  (capacitor and battery are linear) are fully implementable now;
- a time-domain ODE solve of the DC network gives i(t) without curve factors, and is
  arguably more accurate. Das02 (p. 317) notes that simplified methods "should be
  verified by an actual simulation".

**Recommendation:** implement the time-domain DC network simulation first, with the
IEC 61660 shape fitting as an optional report format once we own the standard.

## 5. Gaps

1. IEC 61660-1 curve data (κC, tp, τ1 and τ2 factors, and σj correction).
2. DC motor transient resistance data (AIEE 1950 report).
3. Rectifier regulation-curve method: finish reading Das02 pp. 333 to 338.
4. DC arc flash (Das21 ch. 15) and DC traction systems (outside IEC 61660).
5. IEEE 485 battery sizing (C5): not in our library.
