# Engine spec note: electromagnetic transients (EMT) (WP-2.10)

This note covers matrix row T4 (EMT simulation) and the transient studies built on it:

- capacitor switching;
- transformer inrush;
- TRV;
- lightning and insulation coordination;
- ferroresonance;
- VFD and drive interaction.

ETAP licenses a third-party engine (PSCAD) for EMT; PowerFactory has its own EMT
(dossiers).

Mining relevance:

- capacitor bank switching near VFDs (nuisance drive trips are common in mines);
- transformer energisation and sympathetic inrush on weak mine supplies;
- switching surges on long trailing cables;
- lightning on overhead mine feeders.

Paraphrased from owned references.

## 1. Sources

| Key | Source | Where |
| --- | --- | --- |
| Das10 | J. C. Das, *Transients in Electrical Systems: Analysis, Recognition, and Mitigation*, McGraw-Hill, 2010 | ch. 1 (EMTP history, Dommel 1969), ch. 4 (line and cable models, sec. 4-16), ch. 6 (shunt capacitor transients, printed pp. 123 to 153), ch. 7 (switching transients, TOV, ferroresonance, statistical studies, pp. 155 to 180), ch. 8 (TRV, pp. 181 to 206), ch. 11 (motor starting transients), ch. 14 (transformer models, inrush, sympathetic inrush, pp. 365 to 396), ch. 15 (power electronics, FACTS), ch. 16 (bus transfer, torsional dynamics), ch. 17 (insulation coordination), ch. 20 to 21 (arresters, grounding transients), App. C (difference equations), App. D (line constants, Carson), App. G (numerical techniques: network equations, compensation method, non-linear and piecewise-linear inductance, trapezoidal rule, pp. 703 to 709) |
| Najm10 | F. N. Najm, *Circuit Simulation*, Wiley/IEEE, 2010 | MNA and companion models (ch. 4), integration methods and stability (ch. 5), **trapezoidal ringing** (sec. 5.5, printed p. 257) with smoothing and extrapolation remedies (sec. 5.5.1 to 5.5.2), variable time-step (sec. 5.6), DAE discretisation (sec. 5.7) |
| Pillage95 | L. Pillage, R. Rohrer, C. Visweswariah, *Electronic Circuit and System Simulation Methods*, 1995 | MNA, sparse solution, time-step control: to cite where needed |
| Vlach83 | J. Vlach, K. Singhal, *Computer Methods for Circuit Analysis and Design*, 1983 | classical formulations |

## 2. Method (Dommel's EMTP approach; Das10 ch. 1 and App. G; Najm10 ch. 4 to 5)

1. **Companion models:** each L and C is discretised with the trapezoidal rule into a
   conductance in parallel with a history current source. Lines use travelling-wave
   models (Bergeron; frequency-dependent models; Das10 sec. 4-16).
2. **Nodal network:** solve G·v(t) = i_hist + i_src at each step with a sparse LU
   factorisation. Refactor only when switches change state.
3. **Non-linear elements:** saturation, arresters and arcs, by the compensation method
   or piecewise-linear segments (Das10 App. G-2 to G-4), or Newton iteration.
4. **Switch events:** time-controlled, current-zero interruption, and statistical
   (random closing times for switching overvoltage distributions; Das10 sec. 7-15).
5. **Numerical trap:** the trapezoidal rule's amplification factor (1 + hλ/2)/(1 − hλ/2)
   tends to −1 for stiff modes. This gives **trapezoidal ringing**: sustained
   oscillations after discontinuities such as inductor current interruption (Najm10
   sec. 5.5, eqs 5.247 to 5.251). Remedies are a few backward-Euler steps (damping) at
   discontinuities, interpolation to the event time, or smoothing and extrapolation
   (Najm10 sec. 5.5.1 to 5.5.2). The EMTP literature addresses the same issue (Das10
   ch. 7 references, "suppression of numerical oscillation"). **This is required, not
   optional.**
6. **Initialisation** from a load-flow (phasor) steady state.

## 3. Studies that sit on the engine (Das10)

- **Capacitor bank energisation and back-to-back switching:**
  - inrush current and frequency;
  - inrush-limiting reactors;
  - secondary resonance;
  - impact on drives;
  - switching with motors.
  - **High mining value.**
- **Transformer inrush:**
  - saturation with residual flux;
  - sympathetic inrush between parallel transformers;
  - ferroresonance.
  - Matches ETAP's inrush module (E84).
- **TRV:**
  - terminal fault (single and double frequency);
  - short-line fault;
  - checks against ANSI/IEEE and IEC TRV envelopes.
  - Links to breaker duty (F3, F7).
- **Lightning:** shielding, backflashover, arrester placement and insulation
  coordination (BIL and BSL margins, risk of failure).
- **Power electronics:** six-pulse bridge and VSC models, notching, and harmonic
  interaction (also H1 time-domain).
- **Bus transfer, motor reacceleration and torsional dynamics** (Das10 ch. 16).

## 4. Open-source route

- No mature, permissive power-system EMT engine was confirmed in this pass.
  - VeraGrid lists "EMT (ABC) simulation" (see `open-source-foundations.md`); its depth
    is to evaluate.
  - ATP-EMTP is free-of-charge under its own licence terms, not open source; avoid it as
    a dependency.
  - OpenModelica can model EMT with Modelica libraries (OSMC-PL/GPL; separate process).
- **Proposed path:**
  1. Write a compact EMT core in Python/NumPy with SciPy sparse LU:
     - R, L and C companion models;
     - an ideal switch with current-zero logic;
     - a Bergeron line;
     - a piecewise-linear saturable inductor;
     - a backward-Euler damping step at discontinuities.
  2. Verify it against closed-form RLC switching results (Das10 ch. 6 capacitor
     energisation examples) and Najm10's ringing example.
  3. Scale later, or evaluate VeraGrid EMT.
- **Quantic's circuit suite (qe_circuit)** already plans MNA for electronics; **the EMT
  core and the circuit simulator should share one MNA and companion-model kernel.**
  That is a design opportunity for the cross-domain platform (Peter's DaVinci-style
  "one tool").

## 5. Gaps

1. Frequency-dependent line and cable models (J. Marti, Universal Line Model): Das10
   ch. 4 gives the concepts. Implementation papers to locate.
2. IEEE and IEC TRV envelope parameters: the standards are paid; Das10 ch. 8 quotes
   profiles (verify only).
3. Arrester V-I data: manufacturer data.
4. Evaluate VeraGrid's EMT capability against a capacitor switching case.
