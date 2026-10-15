# Engine spec note: ANSI/IEEE C37 short-circuit duty (WP-2.10)

Matrix rows: F3 (ANSI three networks, X/R multipliers, duty), F7 (device duty against
ratings). Both ETAP and PowerFactory offer this method (see `etap.md` and
`powerfactory.md`). Quantic has nothing yet.

Everything below is paraphrased from the owned books, which were used to verify
formulas and results only. No tables, figures or worked examples are reproduced. Every
equation was re-derived or re-computed in Python in this session, and the check results
are in section 7.

## 1. Sources

| Key | Book | Where |
| --- | --- | --- |
| Das02 | J. C. Das, *Power System Analysis: Short-Circuit, Load Flow and Harmonics*, 1st ed., Marcel Dekker, 2002 | ch. 5 (pdf pp. 160 to 166) and ch. 7 (pdf pp. 234 to 262) |
| Das21 | J. C. Das, *Arc Flash Hazard Analysis and Mitigation*, 2nd ed., Wiley/IEEE, 2021 | ch. 5 (printed pp. 135 to 161), ch. 7 (printed pp. 232 to 234, 242 to 243) |

The governing standards are IEEE C37.010 (application guide for HV breakers rated on a
symmetrical current basis), IEEE C37.04 and C37.06 (ratings), IEEE C37.13 (LV power
circuit breakers), UL 489 (MCCBs) and IEEE C37.41 (fuses). We do not own any of them.
The books quote them, and every figure the engine needs is labelled below as either
"verified in book" or "gap: needs the standard".

## 2. What the engine computes

There are four calculation types (Das02 p. 234, Das21 p. 133):

1. **First-cycle duty for LV devices** (fuses, LV breakers): this needs the
   symmetrical current, the fault-point X/R and the LV test-X/R correction.
2. **First-cycle (close and latch) duty for MV/HV breakers**: the symmetrical current,
   then the asymmetrical rms and peak from the fault-point X/R.
3. **Interrupting (contact parting) duty for breakers above 1 kV**: the symmetrical
   current times a multiplying factor that depends on X/R, contact parting time and
   the remote or local mix (NACD).
4. **Currents for time-delayed relaying (30 cycles)**: these feed protection
   coordination.

Each type uses its own network, built by scaling the rotating machine impedances
(section 3). The static branches (lines, cables, transformers, reactors) are the same in
every network. Each network reduces to a Thevenin impedance at the faulted bus, with the
prefault voltage at rated value and no load current (Das02 pp. 235, 237).

## 3. Network construction per calculation type

**Rotating machine multipliers.** Machine impedances are scaled by a factor that
depends on machine type, rating, speed and calculation type. The factor applies to R
and X together, so the machine X/R is unchanged (Das02 p. 237). The categories are:

- turbo and hydro machines with amortisseur windings and condensers;
- hydro machines without amortisseurs, which use the transient reactance;
- synchronous motors;
- induction motors banded by hp and speed;
- in multivoltage studies, a single combined first-cycle network that keeps motors
  under 50 hp with their own factor.

Values are verified in Das21 Table 5.1, printed p. 135, sourced from IEEE C37.010. The
same table in Das02 (Table 7-1, pdf p. 236) is a **blank page in our copy**, so cite Das21.

**Thirty-cycle network** (Das21 p. 161):

- utility sources unchanged;
- dc component zero;
- all motor contributions removed;
- generators use the transient reactance or a higher value.

Excitation supply affects the real 30-cycle generator current; the book treats this
qualitatively only.

**Resistances.** Resistances come from manufacturer data where available (Das02 p. 238).
The standard's typical approximations, verified in Das02 Table 7-2 (p. 239), are:

- generator "effective resistance" from the negative-sequence reactance and armature
  time constant: R = X2v / (2π f Ta3), eq. 7.12;
- induction motors: about 1.2 times the dc armature resistance;
- transformers: ac load-loss resistance;
- lines, cables and reactors: ac resistance.

Typical X/R by rating appears only as curves (Das02 Figs 7-2 to 7-4). Those are not
digitised. They are a gap for defaults only, and the engine must require user data or
library data.

## 4. Fault-point values

**Symmetrical current.** The engine computes either the E/Z complex reduction (industry
standard, Das02 p. 247) or E/X (conservative). Building R and X from separate networks
and treating them as one impedance gives results higher than the complex method, by up
to about 5 to 6% (Das02 p. 247; Das21 p. 152 says up to 5%). A matrix (Zbus) solution
is acceptable (Das02 Example 7.2, p. 262).

**X/R ratio.** X/R always comes from **two separate networks**: reduce the R-only
network and the X-only network independently, then divide. It is never taken from the
complex Thevenin impedance (Das02 pp. 238, 246, 262). Zero-valued R or X elements are
not allowed in those networks (Das02 p. 262). This needs a diagnostic per element.

- Single line-to-ground faults: X/R = (X1+X2+X0)/(R1+R2+R0) (Das02 p. 246).

**Contributions.** The engine computes branch contributions from adjacent buses and
labels each source remote or local (Das02 p. 244). A generator is **remote** if it feeds
through two or more transformations, or if its external reactance is at least 1.5 times
its subtransient reactance (equivalently, it delivers under 40% of its own terminal
fault current). Otherwise it is **local** (Das02 pp. 241 to 242). Motors are neither:
their decay is already inside the multiplier (Das02 pp. 245 to 246).

## 5. Duty equations

Notation: f is the system frequency, C the contact parting time in cycles (60 Hz basis),
and X/R the fault-point ratio from section 4.

**First cycle, asymmetrical rms at half a cycle:**

    MF_rms = sqrt(1 + 2 exp(-2π / (X/R)))

This is the same decay form as the remote equation below with C = 1/2. It is consistent
with the asymmetrical rms factors in Das02 Table 5-1 (p. 165) and Example 7.1 (p. 256);
see the checks in section 7.

**First cycle, crest:**

    MF_peak = sqrt(2) (1 + sin φ · exp(-(φ + π/2) / (X/R))),  φ = atan(X/R)

This is Das02 eq. 7.5 (p. 248). The breaker is adequate when MF_peak × (E/Z)_first-cycle
is at most its close and latch capability in kA crest, eq. 7.6. The capability is:

- 2.7K times the rated short-circuit current in the older rating structure;
- 2.6 for newer 60 Hz breakers, 2.5 for 50 Hz (Das02 p. 164);
- the rms version is 1.6K.

**Interrupting, remote sources (dc decay only), Das02 eq. 7.1 (p. 241):**

    MF_remote = (1/S) · sqrt(1 + 2 exp(-4π C / (X/R)))

S is the breaker's asymmetrical capability ratio, which comes from the contact parting
time. Verified in Das02 p. 162:

| Contact parting time (cycles) | S |
| --- | --- |
| 1 | 1.4 |
| 1.5 | 1.3 |
| 2 | 1.2 |
| 3 | 1.1 |
| 4 or more | 1.0 |

Contact parting time is the half-cycle tripping delay plus the lesser of the actual
opening time and 1.0, 1.5, 2.5 or 3.5 cycles for 2, 3, 5 and 8 cycle breakers. That
gives default contact parting times of 1.5, 2, 3 and 4 cycles (Das02 p. 162).

The book's examples apply a floor of 1.0 (F1 below gives 0.996 and is reported as 1).

**Interrupting, local sources (ac and dc decay).** The local multiplying factors are
**not** given by a closed-form equation. They come from IEEE C37.010 curves of
multiplier against X/R per contact parting time, for three-phase and line-to-ground
faults (Das02 Figs 7-6 and 7-7, p. 242). Das02 pp. 242 to 243 explains how the curves
were built:

1. Start from the no-ac-decrement asymmetry.
2. Apply an empirical ac-decrement reduction factor, eq. 7.2.
3. Divide by S.

The empirical band data in Figs 7-9(a) to (c) is not reproducible from the text.
**Gap: needs IEEE C37.010 local-curve data (tabulated or digitised with the standard's
permission).** We must not digitise the book's reproduced figures into the repo.

**Weighting (NACD).** NACD = (sum of remote, no-ac-decay source currents) / (E/X of the
interrupting network), eq. 7.3 (Das02 p. 245). The text applies the remote multiplier to
the remote part and the local multiplier to the local part. My reading is that this is
a linear interpolation:

    MF_w = NACD · MF_remote + (1 - NACD) · MF_local

Das02 Fig. 7-11 and Das21 Fig. 5.3 tabulate interpolated values from W. C. Huening Jr.,
"Interpretation of new American standards for power circuit breaker applications", IEEE
Trans. IGA-5, pp. 121 to 143, 1969 (named in Das21 ch. 5 ref. 12). That paper is a
candidate source for the local curves and the weighting. This
reading is consistent with two book results (section 7), but the formula itself is
**my inference**, to confirm against C37.010 before coding.

**Interrupting adequacy, Das02 eq. 7.4 (p. 248):**

    MF_w · (E/X or E/Z)_interrupting  <  breaker symmetrical interrupting rating

The rating at the operating voltage is rated current × (rated max voltage / operating
voltage), capped at K times the rated current (Das02 eq. 5.4, p. 163). K = 1 for newer
breakers (Das02 p. 163). Line-to-ground capability is 1.15 times the polyphase value,
still capped at K times (Das02 p. 163).

**Shortcuts the engine may offer** (Das02 p. 238):

- If X/R ≤ 15, E/X can be compared with the symmetrical rating directly.
- If X/R > 15 and E/X ≤ 80% of the rating, the breaker passes with no X/R work.

Use these as screening flags only, never as the reported duty.

**Conflict on the threshold.** Das21 sec. 5.5.1 to 5.5.2 (printed pp. 136 to 137)
gives the same two shortcuts with X/R **17** instead of 15. For line-to-ground faults it
uses (2X1+X0)/(2R1+R0). Both books cite C37.010-1999. A 45 ms dc time constant at 60 Hz
corresponds to X/R about 17, which points to a newer rating basis, but that is my
reading. **Gap: confirm in the current C37.010 before coding. Until then, the threshold
is a parameter that cites its source.**

**Validity limit.** The E/X method with decrement adjustments is stated valid up to
X/R 45 at 60 Hz (dc time constant 120 ms). Above that, the engine must emit a diagnostic
advising the manufacturer check (Das02 p. 248).

**High asymmetry and generator breakers.** These apply when ac decays faster than dc
(near large generators). Current zeros may be missing at contact parting. The analytical
check is (Das02 pp. 249, 258 to 259):

- symmetrical current at contact parting from the generator decrement equations;
- dc at contact parting = sqrt(2) I'' e^(-t/Ta);
- asymmetry factor α = Idc / (sqrt(2) Isym);
- total rms = sqrt(Isym² + Idc²);
- S = sqrt(2α² + 1), eqs 7.7 and 7.8.

If α > 1 (asymmetry over 100%), flag "no current zero at contact parting". External
resistance shortens Ta, eq. 7.11. The book recommends dynamic simulation in that case.
This links to engine T1/T4 later.

**Generator breaker breaking duty.** The engine evaluates both fault sides of the breaker
(generator side and system side) and takes the worse. A feeder breaker is evaluated at
its load terminals without its own downstream motor contribution. Bus bracing uses all
contributions (Das02 p. 256). **This applies to every breaker: device duty uses the
current through the device, not the bus total (Das21 p. 152).**

## 6. LV devices (first-cycle)

LV breakers and fuses are tested at a fixed test X/R. When system X/R exceeds it, the
calculated current is multiplied up (Das21 pp. 232 to 234, 243).

**LV power circuit breakers.** The test X/R is 6.6 (15% power factor, IEEE C37.13).

- Unfused: MF = sqrt(2)(1 + exp(-π/(X/R))) / 2.29, eq. 7.3.
- Fused: MF = sqrt(1 + 2 exp(-2π/(X/R))) / 1.25, eq. 7.4.
- In both cases the floor is 1.0.

**General form for any test power factor** (Das21 eq. 7.5):

    MF = (1 + exp(-π/(X/R))) / (1 + exp(-π/(X/R)_test))

**MCCBs and ICCBs** (UL 489) have a test power factor that depends on the interrupting
rating band (verified in Das21 Table 7.8, p. 234). The correction applies only when the
system X/R exceeds the test X/R.

**Fuses** (Das21 p. 243). The rated asymmetrical capability of power fuses is 1.6 times
the symmetrical rating. The test X/R is 25 for expulsion and current-limiting fuses, and
1.5 to 15 for distribution cutouts.

The engine stores the device test X/R in the device library, never hard-coded per type
without a source.

## 7. Verification cases (computed here, against book results)

| Check | Inputs | Computed | Book | Status |
| --- | --- | --- | --- | --- |
| Remote MF | X/R 40, C 3, S 1.1 | 1.213 | 1.21 (Das02 p. 241) | ok |
| Remote MF, Ex. 7.1 F1 | X/R 16.28, C 2, S 1.2 | 0.996, floor 1.0 | 1.0 (p. 254) | ok |
| Remote MF, Ex. 7.1 F4 | X/R 26.0, C 3, S 1.1 | 1.102 | 1.102 (p. 260) | ok |
| Crest MF, Ex. 7.1 F2 | X/R 74.89 | 2.770 | 2.768 (p. 257) | ok |
| Crest MF, Ex. 7.1 F3 | X/R 15.94 | 2.578 | 2.575 (p. 257) | ok |
| Crest MF, generator | X/R 123 | 2.793 | 2.789 (p. 256) | ok |
| Half-cycle rms MF | X/R 74.89 / 15.94 / 123 | 1.685 / 1.532 / 1.703 | 1.685 / 1.532 / 1.70 | ok |
| Crest and rms MF, Ex. 7.1 F1 | X/R 16.27 | 2.582 and 1.536 | 2.514 and 1.487 (Table 7-5, p. 257) | **book inconsistency** |
| Das21 eq. 5.7 as printed (no 1/S) | X/R 40, C 3 | 1.334 | 1.21 (Das21 p. 138) | **printed equation omits 1/S; 1.21 needs S = 1.1 as in Das02 eq. 7.1** |
| S from α | α 1.3 | 2.093 | 2.09 (p. 249) | ok |
| LVPCB unfused / fused | X/R 20 | 1.145 / 1.255 | 1.14 / 1.26 (Das21 Table 7.7) | ok |
| LVPCB unfused / fused | X/R 9.95 | 1.068 / 1.149 | 1.07 / 1.15 | ok |
| NACD weighting, Ex. 7.1 F2 | NACD 0.487, X/R 75.26, remote 1.352 | implies local 1.196 | weighted 1.272 | plausible (local at X/R 80 is 1.21 per p. 243) |
| NACD weighting, Das21 Ex. 5.2 bus 2 | NACD 0.335, X/R 47.9, remote 1.257 | implies local 1.116 | weighted 1.163 (Das21 p. 152) | plausible |

**About the F1 row.** In the same table, the book's own asymmetrical rms current (31.56
kA at 20.55 kA symmetrical) equals 20.55 × 1.536, not 20.55 × 1.487. So the 1.487 is a
printing error. The crest value (2.514, 51.66 kA) does not match the book's equation for
an X/R almost equal to F3's. Use F2, F3 and the generator rows as references, not F1's
multiplier columns.

**Example 7.1, motor M3.** The 500 hp, 2-pole motors use 3.0 (interrupting) and 1.2
(first-cycle). For induction motors above 250 hp at 3600 rpm, Das21 Table 5.1 gives
1.5 and 1.0. The effect at F1 is negligible (the book itself shows motors change F1 by
0.13%), but the example is not a clean reference for the multiplier rule.

## 8. Engine inputs and outputs (sketch for the contract WP)

**Inputs:**

- network with R and X per element (no zeros);
- machine data: type, hp, rpm, X'', X', X2, Ta;
- source classification overrides;
- prefault voltage, defaulting to rated;
- calculation types requested;
- per breaker: interrupting time or contact parting time, rated maximum voltage, rated
  short-circuit current, K, close and latch rating, and rating basis (symmetrical or
  total);
- per LV device: test X/R and whether it is fused.

**Outputs per faulted bus:**

- complex Z, E/Z, X/R from separate networks;
- remote and local currents, NACD;
- MF_remote, MF_local, MF_w;
- first-cycle rms and crest;
- 30-cycle current.

**Outputs per device:** duty current through the device (worse side), and percent of
rating with a pass or fail flag.

**Diagnostics:**

- zero R or X;
- X/R above 45;
- asymmetry above 100%;
- local-curve data missing;
- a source classified local or remote by override.

**Worked trace (our differentiator, matrix G13):** show each multiplier with its equation
and source line.

## 9. Gaps and next sources

1. IEEE C37.010 local multiplier curves (three-phase and line-to-ground) and the NACD
   interpolation (Das02 Figs 7-6, 7-7, 7-11). We need the standard. Peter would have to
   buy IEEE C37.010 (it is a paid standard; it goes in QE-References only).
2. Typical X/R by rating curves (Das02 Figs 7-2 to 7-4). These are defaults only; they
   can come from the device library instead.
3. Das02 pdf p. 236 is blank in our copy. Das21 Table 5.1 covers it.
4. The analytical generator decrement (Das02 ch. 6, eqs 6.13 and 6.24) is to be read
   next for the analytical path and for IEC 61363 (matrix F4).
