# Engine spec note: motor starting, acceleration and load models (WP-2.10)

This note covers matrix rows:

- M1: static motor start (Quantic partial);
- M2: dynamic acceleration;
- M3: starters;
- M4: parameter estimation;
- S7: voltage-dependent loads.

Mining relevance is very high: conveyors (constant torque), SAG and ball mills (high
inertia, long starts), crushers, and pumps and fans (quadratic torque). Large motors on
weak mine supplies cause voltage-dip and stall problems.

Paraphrased from owned references.

## 1. Sources

| Key | Source | Where |
| --- | --- | --- |
| Das02 | J. C. Das, *Power System Analysis*, 2002 | sec. 12.10 (load models, pdf pp. 430 to 437), sec. 12.11 (impact loads, motor starting, pdf pp. 437 to 440) |
| Fitz03 | A. E. Fitzgerald, C. Kingsley, S. D. Umans, *Electric Machinery*, 6th ed., 2003 | ch. 6: equivalent circuit (sec. 6.3), Thevenin torque (6.5), no-load and blocked-rotor tests (6.6, printed pp. 330 to 336), deep-bar and double-cage rotors (6.7, p. 343 onward) |
| Krause23 | P. C. Krause, T. C. Krause, *Introduction to Modern Analysis of Electric Machines and Drives*, 1st ed., 2023 | free acceleration, reference frames (pdf p. 101 onward); steady-state torque-speed (ch. 3) |
| Bose02 | B. K. Bose, *Modern Power Electronics and AC Drives*, 2002 | soft starters, VFDs: to read |

The standards are NEMA MG-1 (design letters, locked-rotor kVA codes) and IEEE 112
(test procedures). We do not own them.

## 2. Load models for load flow (S7; Das02 sec. 12.10)

**Exponential model:** P = P0·(V/V0)^np and Q = Q0·(V/V0)^nq, with frequency terms for
dynamics (eqs 12.89 to 12.90). The exponent has a physical meaning:

- n = 0 for constant power;
- n = 1 for constant current;
- n = 2 for constant impedance.

For a composite load, n = 1 + (dI/dV) at rated values (eqs 12.91 to 12.94, p. 433).

**Polynomial (ZIP) fits:** Das02 quotes quadratic fits for air conditioning, fluorescent
lighting and induction-motor loads from its ref. 5 (eqs 12.95 to 12.100). These are
library defaults with a citation, which the user can edit. **Check them against the
original (EPRI) before shipping.**

**Synchronous motors and drives** (p. 437):

- A synchronous motor is a generator with negative P.
- Drives are constant P with Q varying with voltage.

**Unbalance** (pp. 436 to 437):

- The negative-sequence impedance of an induction motor is about Z1/(Is/If). A 5%
  negative-sequence voltage then drives about 30% negative-sequence current.
- Zero-sequence impedance is infinite (ungrounded windings).
- **Feature: derating for unbalance.** Das02 quotes NEMA's unbalance definition.

## 3. Static motor-start voltage dip (M1, existing in Quantic)

The motor is modelled as its locked-rotor impedance, Z_lr from the starting current
(Das02 eq. 12.106). A load flow then gives the dip.

**Stall check** (Das02 p. 435): electromagnetic torque scales roughly with V². With
breakdown torque Tbd at rated voltage and load torque TL, the largest dip before stall is
1 − sqrt(TL/Tbd).

**Check:** for breakdown torque at 200% and full-load torque, 1 − sqrt(0.5) = 0.293,
which matches the book's 29.3%.

## 4. Dynamic acceleration (M2)

Solve the mechanical equation together with a load flow at each time step (or a
dynamic-phasor network):

    J dω/dt = Te(s, V) − TL(ω)

- **Te from the steady-state equivalent circuit** (Das02 eq. 12.102; Fitz03 secs 6.4 to
  6.5, Thevenin form):

      Te = (1/ωs) · V1² (r2/s) / ((R1 + r2/s)² + (X1 + x2)²)

  The terminal voltage V1 comes from the network at that instant, so the motor and the
  network are solved together.
- **Deep-bar and double-cage rotors:** r2 and x2 vary with slip (Fitz03 sec. 6.7).
  Single-cage parameters fitted at full load misrepresent starting torque and current.
  The engine needs either a double-cage model or slip-dependent parameters.
- **Full electromagnetic transient model** (Krause23, free acceleration in machine
  variables and reference frames): needed for transient torques at energisation and for
  restarts with residual voltage. It is optional and tied to T1/T4.
- **Load torque models:**
  - constant torque (conveyor, crusher);
  - quadratic (fan, pump);
  - linear;
  - user-supplied point curves.

  Breakaway friction needs a separate starting value.
- **Inertia:** the motor's J plus the load's J referred through the gearbox (J·(n_load/
  n_motor)²).
- **Outputs:**
  - speed, current, torque, terminal voltage and slip against time;
  - acceleration time;
  - minimum voltage at each bus;
  - a check of thermal stall time against motor limits (links to the P2 damage curves);
  - which other motors stall or contactors drop out (Das21: contactors drop at 30 to 70%
    voltage).

## 5. Starters (M3)

**Methods:**

- direct on line;
- autotransformer (taps);
- star-delta (1/3 current and torque);
- primary reactor or resistor;
- capacitor-assisted;
- soft starter (voltage ramp or current limit);
- VFD (current-limited, rated torque from zero speed).

Each starter changes V1 seen by the motor and the current drawn from the network. The
model needs:

- the transition events (star-delta changeover, autotransformer transition);
- a soft starter as a voltage-ramp or current-limit controller;
- a VFD as a current-limited source with a power-factor model.

**Gap:** read Bose02 for soft-starter and VFD control models, and Das21 or Das02 for
transient torques at star-delta transition.

## 6. Parameter estimation (M4)

**From tests** (Fitz03 sec. 6.6, printed pp. 330 to 336):

- **No-load test:**
  - Prot = Pnl − nph·I²nl·R1 (eq. 6.37);
  - the speed-decay method separates rotational and core losses (eqs 6.38 to 6.40);
  - X1 + Xm ≈ Xnl = Qnl / (nph·I²nl) (eqs 6.42 to 6.46).
- **Blocked-rotor test:** at reduced frequency for normal-frequency equivalence. It gives
  R1 + R2 and X1 + X2, with the split per NEMA design class.
- **DC resistance:** R1.

**From datasheet values:** full-load current, power factor, efficiency, locked-rotor
current and power factor, locked-rotor torque, breakdown torque, full-load slip. This is
what users have.

- Fit single- or double-cage parameters by non-linear least squares so that the circuit
  reproduces those points. ETAP and PowerFactory both offer this (dossier rows M4).
- **Gap: no owned source gives a fitting procedure.** Candidates: IEEE papers on
  induction-motor parameter estimation from manufacturer data. To search (public
  abstracts).
- The Quantic approach is ordinary constrained least squares with SciPy, reporting fit
  residuals per datasheet point in the worked trace.

## 7. Open-source foundations

- **pandapower:** has motor elements for load flow and short circuit (static), but no
  acceleration study as far as its docs show. **To verify.**
- **OpenDSS:** has an induction machine model for dynamics mode. **To verify.**
- **ANDES** (GPL-3, separate process only) and **Dynawo** (MPL-2.0): motor dynamic
  models for stability. See the T1 note when written.

Likely route: our own acceleration integrator (SciPy ODE) coupled to pandapower load
flow per step. This is a small, well-defined engine and a good first dynamic study.

## 8. Gaps

1. A datasheet-to-circuit fitting method from a published source.
2. NEMA MG-1 data (design letters, code letters): paid.
3. Soft starter and VFD models (Bose02).
4. Check the EPRI load polynomial coefficients quoted in Das02.
