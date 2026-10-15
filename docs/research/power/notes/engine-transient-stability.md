# Engine spec note: RMS transient stability (WP-2.10)

This note covers matrix rows:

- T1: RMS transient stability with machines, exciters, governors and PSS;
- T2: user-defined models;
- T3: small-signal analysis;
- T5: load shedding, fast bus transfer and generator start.

ETAP and PowerFactory both sell this as a module (dossiers).

Mining relevance:

- islanded mine power stations and diesel or gas gensets;
- large motor restarts after voltage dips;
- load shedding schemes on loss of a utility tie;
- fast bus transfer for critical drives.

Paraphrased from owned references.

## 1. Sources

| Key | Source | Where |
| --- | --- | --- |
| Kundur94 | P. Kundur, *Power System Stability and Control*, McGraw-Hill/EPRI, 1994 | ch. 13 (printed pp. 827 onward): sec. 13.2 integration methods (pp. 836 to 845), sec. 13.3 simulation structure (pp. 848 to 868), sec. 13.4 unbalanced faults in stability, sec. 13.5 relays during swings; ch. 3 to 5 machines, ch. 8 excitation, ch. 9 prime movers, ch. 12 small-signal |
| Sauer06 | P. W. Sauer, M. A. Pai, *Power System Dynamics and Stability*, 2006 | ch. 5 to 7: model hierarchy (two-axis, flux-decay, classical; pp. 99 to 104), multimachine models (ch. 6), DAE simulation, power-balance and current-balance forms, SI and PE solution methods, initial conditions (ch. 7, pp. 155 to 210) |
| foundations | `notes/open-source-foundations.md` | ANDES, Dynawo, OpenIPSL, PowerSimulationsDynamics.jl |

The standards are IEEE 1110 (generator model structures), IEEE 421.5 (excitation system
models) and the WECC generic renewable models (REGC, REEC, REPC). We do not own them.
ANDES and Dynawo implement many of these models, which is our practical reference.

## 2. Problem structure (Kundur94 sec. 13.3; Sauer06 sec. 7.1)

The system is a differential-algebraic initial value problem:

- **Differential:** generator rotor and flux states, exciters, governors and turbines,
  PSS, motor slips, dynamic loads, controllers (HVDC, SVC, inverter-based resources).
- **Algebraic:** the network current balance I = Y·V (sparse), plus the stator algebraic
  equations.
- **Reference frames:** each machine in its own d-q frame; the network in a common
  synchronously rotating R-I frame. The transformation uses the rotor angle δ (Kundur94
  eqs 13.31 to 13.34, pp. 852 to 853).
- **Network interface:** each generator appears as a Norton current source behind its
  subtransient admittance. With subtransient saliency, the interface impedance depends
  on δ; Kundur94 handles this with eq. 13.33 or iteration.
- **Discontinuities:** faults, switching and limiter hits. The network variables jump;
  the states do not.

## 3. Generator model hierarchy (Sauer06 ch. 5 to 6; Kundur94 ch. 3 to 5)

From most to least detailed:

1. **Full model with stator transients:** for EMT only (T4).
2. **Subtransient models** (Kundur94 Fig. 13.9: one d-axis and two q-axis amortisseurs).
   Stator transients and speed effects in the stator are neglected (Kundur94 eq. 13.28).
3. **Two-axis model:** E'd and E'q dynamics (Sauer06 sec. 5.4, p. 99).
4. **One-axis (flux-decay) model:** E'q only (sec. 5.5, p. 101).
5. **Classical model:** a constant voltage behind X'd (sec. 5.6, p. 103).

Saturation can be added to any of them (Sauer06 sec. 5.8 and 6.8; Kundur94 sec. 3.8).

The engine should support at least the classical, two-axis and one subtransient model
(GENROU/GENSAL-equivalent behaviour). It should also **read PSS/E .dyr parameter
files**, so customers' existing model data can be reused. ANDES and Dynawo both parse
.dyr; PowerFactory imports it (dossier).

**Swing equation** (Kundur94 eq. 13.22):

    p Δω = (Tm − Te − KD Δω) / 2H
    p δ = ω0 Δω

## 4. Controls

- **Excitation:** IEEE 421.5 types (DC, AC, ST families; for example SEXS, IEEEX1,
  ESST1A, AC8B). Kundur94 ch. 8 covers the theory. Parameter sets come from customer
  data.
- **Governors and turbines:** steam, hydro and gas (Kundur94 ch. 9); GAST and diesel
  (for mine gensets: DEGOV-type models). **Gap:** diesel genset governor models are not
  in our books. ANDES and Dynawo libraries are the reference.
- **PSS:** PSS1A and PSS2B types (Kundur94 ch. 12).
- **Inverter-based resources:** WECC generic models (REGC_A/B, REEC_A, REPC_A). Needed
  for PV and BESS on mine sites, which links to Quantic's PV suite. **Gap:** not in our
  books. The model specification is public in WECC documents. To fetch.

## 4a. User-defined models (T2)

- **What the vendors offer:**
  - ETAP has a User-Defined Dynamic Model (UDM) block-diagram compiler (dossier);
  - PowerFactory has DSL plus Modelica and FMI (its FAQ tags include Modelica and FMI;
    `powerfactory-notes.md` P76).
- **Quantic route:** the **FMI 2.0/3.0 standard** (Functional Mock-up Units). Users bring
  models from any Modelica tool, Simulink or vendor exporters. We co-simulate or
  model-exchange them in our integrator.
- **Python libraries** (licences checked 2026-10-15 from PyPI and wheels):
  - **FMPy** 0.3.32: BSD-2-Clause (some bundled assets are CC BY 4.0 or MIT). Suitable.
  - PyFMI 2.5: LGPL. Usable only as a separately linked library; prefer FMPy.
  - OMPython 4.1.0: OpenModelica's OSMC licence. Separate process only.
- **Block diagrams in the workbench** compile to the same internal representation as
  the PLC suite's function blocks: a cross-domain reuse opportunity.

## 5. Numerical solution (Kundur94 sec. 13.2 and 13.3.6; Sauer06 sec. 7.7 and 7.8)

**(a) Partitioned, explicit** (RK4 or modified Euler):

- Alternate the network solve and the state update at each stage.
- Simple and flexible per device. This is the classic production approach.
- **Weakness:** numerical stability on stiff systems. The time step is set by the
  smallest time constant (pp. 861 to 862).

**(b) Simultaneous, implicit trapezoidal** (pp. 862 to 864):

- Newton on [states; network voltages] each step.
- Jacobian blocks Ad, Bd, Cd, Yd per device, with the reduction
  (YN + Yd − Cd·Ad⁻¹·Bd)·ΔV = −G + Cd·Ad⁻¹·F (eq. 13.67).
- Stable for stiff systems.
- Discontinuities need special handling.

**Initialisation** from a converged load flow (Sauer06 sec. 7.6 and 7.10). This is the
step most commercial users fight with. The engine must report every device whose
initial state violates a limit, naming the element and field (AGENTS.md conduct rule).

**Quantic recommendation:** implicit trapezoidal with a sparse Newton solve, a
variable step after events, and event location for switching and limits. That is the
same family as Dynawo (variable-step implicit) and PowerFactory RMS (dossier).

## 6. Events and studies (T5)

- **Events:** three-phase and unbalanced faults (Kundur94 sec. 13.4 shows how to insert
  an unbalanced fault into a positive-sequence simulation as a fault shunt, from
  negative- and zero-sequence Thevenin impedances), breaker opening, load steps, motor
  starts, generator trips, tap changes.
- **Protection during swings:** distance relay apparent impedance, out-of-step and
  loss-of-excitation logic (Kundur94 sec. 13.5).
- **Mining studies:**
  - load shedding on islanding (underfrequency relay models);
  - motor restart and re-acceleration after a dip (links to M2);
  - fast bus transfer (residual voltage and phase angle at transfer);
  - genset start and block loading;
  - critical clearing time search by bisection on fault duration.

## 7. Small-signal (T3), outline

Linearise the same DAE at the operating point, then compute eigenvalues,
participation factors and mode shapes (Kundur94 ch. 12). Reusing the transient model
Jacobian (sec. 5b) gives T3 almost free once T1 exists.

## 7a. Verification cases with complete data (checked on the page images, 2026-10-15)

**Kundur94 Example 13.1** (printed pp. 843 to 848, pdf pp. 865 to 870): one equivalent
classical generator (4 × 555 MVA, X'd = 0.3, H = 3.5, KD = 0) feeding an infinite bus
through a transformer (j0.15) and two circuits (j0.5 and j0.93), all on 2220 MVA.
Initial condition P = 0.9, Q = 0.436, Et = 1.0∠28.34°, EB = 0.90081∠0. A solid
three-phase fault on circuit 2 is cleared by tripping that circuit.

- Book results: E' = 1.1626∠41.77°; critical clearing time 0.0865 ± 0.0005 s; critical
  clearing angle 52.17° ± 0.13° by integration and 52.29° by equal area; maximum swing
  125.27°.
- **Our independent recomputation** (equal area, P_e = 0 during the fault, so
  δ(t) = δ0 + ω0·P·t²/(4H)): δ0 = 41.77°, δmax = 125.27°, δc = 52.24°, t_cc = 0.0868 s.
  This agrees with the book to rounding (the 0.05° difference in δc comes from rounded
  intermediate values).
- Use: the first unit test of the integrator. A bisection on clearing time must return
  0.086 to 0.087 s.

**Kundur94 Example 13.2** (pp. 864 onward): the same system with rotor-circuit dynamics
and excitation control (to read before the subtransient model WP). **Example 13.6**
(p. 926): apparent impedance seen by a distance relay during the unstable case of
Example 13.2. That is a test for the protection-during-swings feature.

**Kundur94 Example 12.6, the two-area system** (printed pp. 813 to 816, pdf pp. 835 to
838). The data is complete:

- four 900 MVA, 20 kV units with full subtransient parameters and saturation
  (A_sat = 0.015, B_sat = 9.6, ψ_T1 = 0.9); H = 6.5 for G1 and G2, 6.175 for G3 and G4;
- step-up transformers j0.15 on 900 MVA;
- 230 kV lines with r = 0.0001, x = 0.001 and b = 0.00175 pu/km on 100 MVA, and the
  line lengths in Figure E12.8 (25, 10, 110, 110, 10, 25 km);
- the generator dispatch and terminal voltages;
- loads and shunt capacitors at buses 7 and 9, with load models stated (constant
  current P, constant impedance Q);
- four excitation variants: a self-excited DC exciter, a high-gain thyristor exciter,
  a thyristor exciter with TGR, and a thyristor exciter with PSS (Figure E12.9).

Published results: Table E12.3 (all 24 eigenvalues, manual excitation) and Table E12.4
(rotor modes for each exciter variant). With manual excitation, the interarea mode is
−0.111 ± j3.43 (0.545 Hz, ζ = 0.032) and the local modes are −0.492 ± j6.82
(1.087 Hz) and −0.506 ± j7.02 (1.117 Hz), both ζ = 0.072. We recomputed f = ω/2π and
ζ = −σ/|λ| from the printed eigenvalues and they agree. The high-gain thyristor case
makes the interarea mode unstable (+0.031 ± j3.84); adding the PSS gives
−0.501 ± j3.77 (ζ = 0.13).

This is the standard benchmark in the literature, and the same network is reused in
Kundur94 ch. 17 (Figures 17.15 and 17.22, including a parallel HVDC tie). It is
the acceptance test for T3 (small-signal) and the time-domain cross-check for T1. It
is also how PowerFactory and PSS/E users judge a new tool, so a published Quantic
reproduction has sales value.

## 8. Open-source route

See `open-source-foundations.md`:

- **ANDES:** GPL-3, so separate process only, never imported (AGENTS.md rule 7). It has
  a broad model library and PSS/E .dyr support. Use it as a **reference to verify**
  against, run as an external process.
- **Dynawo:** MPL-2.0, C++ and Modelica, variable-step implicit. A candidate engine.
  MPL is file-level copyleft, compatible with linking.
- **OpenIPSL:** BSD-3, a Modelica library of PSS/E-equivalent models. Needs a Modelica
  compiler (OpenModelica, OSMC-PL/GPL; run as a separate process).
- **PowerSimulationsDynamics.jl:** Julia. Licence to confirm.

**Likely route:**

1. Build a small Python implicit-trapezoidal core for the classical, two-axis and
   GENROU-equivalent models, SEXS and IEEEX1, and a simple governor, for mine-scale
   systems.
2. Verify against ANDES (external) and Kundur94 or Sauer06 examples.
3. Evaluate Dynawo for large systems later.

## 9. Gaps

1. IEEE 421.5 block diagrams and parameters: we need the standard or the ANDES and
   Dynawo documentation (public).
2. WECC renewable model specifications (public, to fetch).
3. Diesel genset governor and AVR models for mine gensets.
4. ~~Kundur94 example systems for verification~~: resolved in sec. 7a (Examples 13.1,
   13.2, 13.6 and 12.6 have complete data).
