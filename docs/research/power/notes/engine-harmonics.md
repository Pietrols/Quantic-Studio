# Engine spec note: harmonic load flow, frequency scan and filter design (WP-2.10)

This note covers matrix rows H1 (harmonic load flow and frequency scan) and H2 (filter
design and IEEE 519 / IEC 61000 limits). Flicker (H3) is not covered yet.

Mining relevance is high: large VFDs, cycloconverters on grinding mills, and power-factor
capacitor banks that resonate. Das02 ch. 17 lists cycloconverters and ASDs as sources.

Paraphrased from owned references. No tables or worked examples are reproduced.

## 1. Sources

| Key | Source | Where |
| --- | --- | --- |
| Das02 | J. C. Das, *Power System Analysis: Short-Circuit, Load Flow and Harmonics*, 2002 | ch. 17 (sources), ch. 18 (effects), ch. 19 (analysis, pdf pp. 634 to 680), ch. 20 (mitigation and filters, pdf pp. 680 onward) |
| Arrillaga03 | J. Arrillaga, N. R. Watson, *Power System Harmonics*, 2nd ed., Wiley, 2003 | to read for iterative harmonic load flow and converter models |
| OpenDSS | EPRI OpenDSS documentation, "Harmonic Flow Analysis" | https://opendss.epri.com/HarmonicFlowAnalysis.html (read 2026-10-15) |

The standards are IEEE 519 (limits), IEC 61000-3-6 and -2-x (planning and compatibility
levels), and IEEE 18 and IEEE 1036 (capacitor ratings). We do not own them, and their
limit tables are copyrighted.

## 2. Methods (Das02 sec. 19.1)

1. **Frequency-domain current injection** (sec. 19.1.1, the industry baseline):
   - Each non-linear load is a Norton harmonic current source from its spectrum.
   - Build Y(h) at each harmonic h with frequency-adjusted component models (sec. 3).
   - Solve V(h) = Z(h)·I(h) (eqs 19.1 to 19.6).
   - Branch currents come from the branch admittance times the voltage difference
     (eq. 19.8).
   - Superposition across harmonics.
   - Optional iteration: re-estimate injections from the computed harmonic voltages until
     they converge (p. 636). Near resonance, linearity is doubtful.
2. **Phase angles of injections** (sec. 19.1.4, eq. 19.9): θh = θh,spectrum +
   h·(θ1 − θ1,spectrum), where θ1 comes from the fundamental load flow. Treating all
   harmonics as cophasial is not always conservative.
3. **Frequency scan** (sec. 19.1.2): inject a unit current at a bus, sweep frequency, and
   plot the driving-point and transfer impedance magnitude and angle.
   - Peaks are parallel resonances.
   - Dips are series resonances.
   - Multiphase scans reveal resonances from single-phase capacitors.
4. **Voltage scan** (sec. 19.1.3): apply unit voltage and compute voltage transfer to
   other nodes.
5. **Harmonic Newton-Raphson** (sec. 19.1.5, eqs 19.10 to 19.13): couples fundamental and
   harmonic mismatches through converter firing and commutation variables. Use it for
   strong converter interaction. It is later work.
6. **Time domain** (secs 19.1.6 to 19.1.7): EMT simulation with FFT, and converter
   switching functions (Ia = Idc·Sa, eqs 19.14 to 19.17). This links to T4 (EMT).

## 3. Component models at harmonic h (Das02 sec. 19.2 to 19.3)

**Lines:**

- Use a long-line (distributed) model beyond about 150/h miles for overhead lines and
  90/h miles for cables (pp. 641 to 642).
- Resistance rises with frequency: R(h) = Rdc·g(h), eq. 19.18 (pdf p. 641, checked on
  the rendered page). The two branches are:
  - g = 0.035X² + 0.938 for X > 2.4;
  - g = 0.35X + 0.3 for X ≤ 2.4;
  - X = 0.3884·sqrt(fh/f)·sqrt(h/Rdc), eq. 19.21.

  The "y" printed before "X" in eqs 19.19 to 19.20 reads as a typesetting artefact for
  "for". The double use of h in X looks doubtful (its source is Das02 ref. 9). **Confirm
  against that reference before coding.**

**Filter reactors:**

- Rh = Rf·(0.115h² + 1)/1.15 for aluminium (eq. 19.22), where Rf is the
  fundamental-frequency resistance.
- Rh = Rf·(0.055h² + 1)/1.055 for copper (eq. 19.23). Checked on the rendered page.
- This sets the sharpness of tuning.

**Transformers:**

- Resistance rises with frequency (Das02 Fig. 19-3, curve only).
- The magnetising branch is usually omitted unless the transformer is itself a source.
- Core loss is Ke·B²·f² + Kh·B^s·f (eq. 19.24).
- Include winding capacitances for transmission studies.

**Induction motors:**

- Xh = h·Xf (approximate).
- Stator R scales with the square root of h (eq. 19.28).
- Harmonic slip: sh = (h − 1)/h for positive-sequence harmonics and (h + 1)/h for
  negative sequence (eqs 19.29 to 19.30, checked on pdf p. 644).
- The rotor resistance is printed as r2h = sqrt(1 ± h)/sh (eq. 19.31). As printed it has
  no r2 factor, so it is probably a typesetting slip for r2·sqrt(1 ± h)/sh or similar.
  **Do not code it before checking Das02 ref. 7.**

**Generators:**

- The average of Ld'' and Lq'' is the harmonic inductance (eq. 19.32).
- Rh = Rdc·(1 + 0.1·(hf/f)^1.5) (eq. 19.33). This form is also used for copper
  transformers and cables.

**Loads** (sec. 19.3):

- **Parallel RL from P, Q** (eq. 19.34): R = V²/(S cos φ), L = V²/(2πf·S sin φ). Checked on
  pdf p. 645.
- **CIGRE type C** (eq. 19.35), valid from the 5th to the 30th harmonic:
  - Rs = V²/P;
  - Xs = 0.073·h·Rs;
  - Xp = h·Rs / (6.7·(Q/P) − 0.74).

  Checked on pdf p. 645.
- **Load representation choice controls resonance sharpness.** OpenDSS makes the same
  point: its default load equivalent splits 50/50 between series and parallel R-L.

**System impedance** (sec. 19.4): the impedance spiral in the R-X plane can be bounded by
a circle and 75° tangents (pp. 645 to 646). Use this for envelope studies when the system
is uncertain.

## 4. Filters (Das02 ch. 20)

**Single-tuned shunt filter** (sec. 20.2):

- Current divider: If = ρf·Ih, with ρf = Zs/(Zf + Zs) (eqs 20.1 to 20.4). A good design
  has |ρf| ≈ 0.995.
- Tuned frequency: ωn = 1/sqrt(LC) (eq. 20.6), with quality factor Q.

**Practical design** (sec. 20.3):

- Tune slightly below the target harmonic (for example 4.7 for the 5th).
- **The parallel resonance always shifts below the tuned frequency:**
  f = 1/(2π·sqrt((Ls + L)·C)) (eq. 20.14), with its own Q from (Rs + R) (eq. 20.15).
- Iterate filter count and tuning until the distortion indices meet the limits.
- Splitting a bank into 5th and 7th filters can worsen the 5th-harmonic TDD (p. 686).

**Other filter types** (secs 20.9 to 20.12): double-tuned, damped and high-pass
(second-order design in sec. 20.11), and zero-sequence traps.

**Component duty checks for capacitors** (IEEE 18 / 1036 limits on voltage, current,
kvar and peak): **gap, needs the standard or Das02 ch. 18 values; read next.**

## 5. Indices and limits

- THD, TDD (IEEE 519 uses demand current at the PCC with the Isc/IL ratio), TIF, IT and
  kVT (Das02 sec. 18.11). These are computed by the engine.
- **Limit tables (IEEE 519, IEC 61000) are copyrighted.** The engine loads them as user
  or library data with citation; it does not ship them.

## 6. Open-source foundation

**OpenDSS harmonic mode:**

- `Solve mode=harmonics`, after a converged snapshot power flow (or a direct solve to
  initialise).
- Spectra attach to Load, Generator, Vsource, Isource, PVSystem and Storage, with
  defaults.
- Sequence handling: positive, zero or none.
- A choice of harmonics.
- Monitors capture the results.

This makes OpenDSS (BSD-3 via DSS-Python; KLUSolve LGPL as a separate library) the
natural base for H1. We would add Quantic's own frequency-scan plots, filter designer,
indices and worked trace on top.

**Verify against:** Das02 Example 19.1 and 20.1 results (pdf pp. 660 to 690). These are
cited references for tests and are not copied.

## 7. Gaps

1. IEEE 519 and IEC 61000-3-6 limit data (paid): user-supplied.
2. Capacitor and filter component rating checks (IEEE 18, IEEE 1531): Das02 ch. 18 and
   20 to read in detail.
3. Arrillaga03 converter models and iterative harmonic power flow: to read.
4. Flicker (H3): IEC 61000-4-15 flickermeter, arc furnace models (Das02 sec. 17.13).
   To read.
5. Equations checked on the rendered pages (2026-10-15): 19.18 to 19.23 and 19.27 to
   19.35. Doubtful as printed: X in eq. 19.21 and r2h in eq. 19.31. Confirm in Das02
   refs 7 and 9.
