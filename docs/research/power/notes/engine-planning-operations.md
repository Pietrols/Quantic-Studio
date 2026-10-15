# Engine spec note: contingency, sensitivities, state estimation, dispatch, OPF, voltage stability, reliability (WP-2.10)

This note covers matrix rows S14 (OPF), S15 (contingency), S16 (PTDF and LODF), S17
(voltage stability), S18 (state estimation), S23 (reliability), S24 (network reduction)
and S26 (economic dispatch and unit commitment).

These are mostly utility and transmission-grade features. For Quantic's mining and
industrial clients, the important ones are contingency (N-1 on mine supply), voltage
stability (weak rural feeds), and reliability (downtime cost). State estimation and unit
commitment are lower priority. Their main value is parity with the "platform" tier of
ETAP and PowerFactory.

Paraphrased from owned references.

## 1. Sources

| Key | Source | Where |
| --- | --- | --- |
| Grainger94 | Grainger and Stevenson, *Power System Analysis*, 1994 (printed page = pdf page − 26 in this range) | ch. 13 economic dispatch and unit commitment (printed pp. 531 onward; UC sec. 13.7 p. 572); ch. 14 Zbus contingency analysis (sec. 14.1 p. 597, single and multiple contingencies, DC model sec. 14.5 p. 627, system reduction sec. 14.6 p. 635); ch. 15 state estimation (least squares sec. 15.1 p. 645, bad data sec. 15.3 p. 655, power system SE sec. 15.4 p. 665) |
| Das02 | J. C. Das, *Power System Analysis*, 2002 | ch. 15 optimisation techniques; ch. 16 OPF (decoupled, Newton, SQP, SLP, interior point, security-constrained) |
| Kundur94 | P. Kundur, *Power System Stability and Control*, 1994 | ch. 14 voltage stability (sec. 14.1 at printed p. 960; static analysis sec. 14.3.3 around p. 990; continuation power flow sec. 14.3.5 at p. 1012) |
| Glover17 | Glover et al., 2017 | economic dispatch and reliability basics (thin) |

## 2. Contingency analysis and sensitivities (S15, S16, S24; Grainger94 ch. 14)

- **Line outage distribution factor** (DC model, eq. 14.62, p. 627):
  - the change in flow on line ij per unit of pre-outage flow on outaged line mn;
  - built from Zbus (reactance) elements and the Thevenin reactance seen across mn;
  - multiple outages are handled by superposition with a small matrix solve (sec. 14.4).
- **Single-contingency AC screening with Zbus modifications** (sec. 14.1 to 14.3): add or
  remove lines without refactoring the whole matrix.
- **System reduction** (sec. 14.6): an external equivalent for the part of the system
  outside the study area. This is the textbook base for Ward and REI reduction (S24).
  ETAP 2026 lists network reduction and aggregation as new (E91).
- **Engine plan:**
  1. Fast DC screening (PTDF and LODF from pandapower `rundcpp` matrices, or computed
     directly).
  2. AC recheck of the worst cases with pandapower.
  3. Rank by overload percentage and voltage violation.
- **Outputs:** a violation table per contingency, ranked, with the worked LODF trace for
  the top cases.

## 3. State estimation (S18; Grainger94 ch. 15)

**Weighted least squares** (sec. 15.1 to 15.2):

    x̂ = (Hᵀ R⁻¹ H)⁻¹ Hᵀ R⁻¹ z

where R is the diagonal matrix of measurement variances. The estimates are unbiased if
there is no bad data (eq. 15.36, p. 655). For the non-linear AC case (sec. 15.4), iterate
with a Gauss-Newton gain matrix G = Hᵀ R⁻¹ H.

**Bad data** (sec. 15.3, after Dopazo, Klitin and Sasson 1973):

- the residual covariance is [I − H G⁻¹ Hᵀ R⁻¹] R, an idempotent projector (eqs 15.38 to
  15.40);
- detect with a chi-square test on the weighted sum of squared residuals;
- identify with the largest normalised residual;
- remove and re-estimate.

**Gaps:**

- observability analysis;
- PMU measurements;
- robust estimators.

Abur and Expósito's book is still the missing reference. pandapower has a state
estimation module (WLS and robust variants). Verify its feature list before use.

**Mining relevance:** low. Possible later as a "digital twin from SCADA" feature (links
to the SCADA and PLC suites).

## 4. Economic dispatch and unit commitment (S26; Grainger94 ch. 13)

- Equal incremental cost within a plant and between plants (sec. 13.1 to 13.2).
- Loss formula (B-coefficients, sec. 13.3) and dispatch with losses (sec. 13.5).
- AGC (sec. 13.6).
- Unit commitment (sec. 13.7 to 13.8: priority list and dynamic programming).

Modern practice is MILP. **Mining relevance:** dispatch of an on-site genset, PV and BESS
fleet (microgrid). Quantic's PV and storage work (WP-2.5 suite) makes a small
microgrid dispatch optimiser plausible. ETAP's microgrid controller (E91) is the
commercial comparison.

## 5. Optimal power flow (S14; Das02 ch. 15 to 16)

Das02 covers:

- the Lagrangian and Kuhn-Tucker theory;
- gradient, Newton, SQP and SLP methods;
- interior point methods (sec. 16.9);
- security and environmental constraints (sec. 16.10).

**Engine plan:** use pandapower's OPF (PYPOWER interior point, or PowerModels.jl
through its interface) and VeraGrid or GridCal for alternatives. Do not write an OPF
solver from scratch. Quantic's value is setting up the problem, constraint reporting
(binding constraints and shadow prices) and the trace.

## 6. Voltage stability (S17; Kundur94 ch. 14)

- **Concepts:** transmission, generator, load and compensator characteristics, and
  collapse scenarios (sec. 14.1 to 14.2).
- **Static analysis** (sec. 14.3.3 to 14.3.4): P-V and Q-V curves, the distance to
  instability, and modal analysis of the reduced Jacobian (smallest eigenvalues and
  participation factors).
- **Continuation power flow** (sec. 14.3.5, p. 1012): predictor-corrector with
  parameterisation by the load factor or a state variable. It traces the curve through
  the nose, where ordinary NR diverges. Ajjarapu's original paper (1992) is the standard
  reference; Ajjarapu's book is still a gap. pandapower does not ship a CPF, as far as
  its docs show; VeraGrid or GridCal has one (**to verify**).
- **Dynamic analysis** (sec. 14.3.2): long-term simulation with OLTCs, overexcitation
  limiters and load recovery. This is the T1 engine with slow controls.
- **Mining relevance:** high where mines hang off long weak feeders. The Q-V margin at
  the mine substation and motor-start voltage collapse are real problems.

## 7. Reliability (S23)

- **Owned coverage is thin** (Glover17 basics). Billinton and Allan, *Reliability
  Evaluation of Power Systems*, is the missing reference.
- **What the engine needs:**
  - component failure rate and repair time data;
  - network topology with protection and switching for restoration;
  - state enumeration or Monte Carlo;
  - indices SAIFI, SAIDI, CAIDI, ENS and EENS;
  - customer and load-point indices;
  - cost of interruption.
- **Mining framing:** expected lost production per year from electrical outages. This is
  a strong selling point (the monetary value of a redundant feeder).
- **Data sources:** IEEE 493 (Gold Book) failure rates. Paid, a gap.

## 8. Gaps

1. Abur and Expósito (state estimation), Billinton and Allan (reliability), and Ajjarapu
   (continuation power flow). Suggested purchases in that order of value: Billinton
   first.
2. IEEE 493 failure-rate data.
3. Verify pandapower's state estimation and OPF capabilities, and VeraGrid's CPF, against
   their current docs.
