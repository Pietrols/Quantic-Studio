# Product model mappings for the original comparison cases

WP-2.17, ChatGPT, 2026-10-17. This research maps the equations in
[comparison-cases.md](comparison-cases.md) to documented candidate models. It does
not report commercial product execution. All 49 product/case executions remain U.
An available module is not evidence of an exact equation, parameter conversion,
initialisation, limiter or event match. An unresolved mapping is not a claim that
the product cannot perform the study.

## Evidence, conversions and comparison gates

S means a primary source states the named behavior. I means our derived mapping
or proposed experiment. U means not established. A row can have S availability and
U exact mapping. Original arithmetic below is an authored observation, not an
observation of a product. Product version, licence, effective settings, results and
permitted retained output remain unestablished until an actual recorded run.

Every row inherits the case's complete common input contract and N/D/E/F/M/R gates.
Three-phase bases give `Zb=Vll^2/S3`, `Ib=S3/(sqrt(3)*Vll)` and
`Vphase=Vll/sqrt(3)`. On a changed machine base, at unchanged voltage,
`Zpu,new=Zpu,old*Snew/Sold`, `Ppu,new=Ppu,old*Sold/Snew` and
`Hnew=Hold*Sold/Snew`. These are authored base conversions (I), not promises about
particular product fields. Verify whether each field expects ohms, pu, percent,
single-phase or three-phase quantities before entry. Unknown field units stay U.

For C-01/C-02 retain the source emf behind explicit Zs, background admittance,
motor-only starter and combined inertia. A load-flow slack at U would omit source
drop. For C-03 disable standard corrections or label a standardized run as a
separate variant. For C-04 no normative arcing-current/energy oracle has been
executed. For C-05 preserve complex phase, fundamental denominator and frequency
dependence. For C-06 retain exact geometry and field boundary. For C-07 no physical
external grid may supply the island's power deficit. Defaults that cannot be
inspected or disabled block exact comparison.

Existing E/P IDs resolve in the [ETAP index](notes/etap-sources.md) and
[PowerFactory index](notes/powerfactory-sources.md); W IDs in the
[PowerWorld dossier](powerworld.md); EP/SK/NP/PS IDs in
[other-products.md](other-products.md). M IDs below identify the more specific
primary sources read for this mapping. Documentary availability in a full product
does not imply demo entitlement: the [dated access ledger](../../sources/entries/power-comparison-access-2026-10-17.yaml)
still applies, including ETAP demo UDM/ground-grid exclusions.

## Coverage: every case and product pair

Each row explicitly states its conversion or the unresolved conversion. Detailed
subsections below are part of the referenced row, not a substitute for an execution
record. All named native models remain candidates until version-specific testing.

| Case | Product | Documentary candidate, conversion and mismatch |
| --- | --- | --- |
| C-01 | ETAP | S: dynamic acceleration, single-cage and polynomial load families (M04/M05, E4). I: use the circuit and torque/inertia targets in section A. U: exact native circuit fields, H/WR2 convention and electrical-state reduction. Static acceleration times entered by the user do not execute our ODE. |
| C-01 | PowerFactory | S: asynchronous machine and explicit MDM/composite route (M06, P5/P19). I: section A's combined inertia and custom mechanical curve. U: exact native equivalent-circuit and state reduction; default implicit MDM power law cannot reproduce our intercept-plus-square curve (I). |
| C-01 | PowerWorld | S: initially offline CIM5/CIM6 start route (M01-M03). I: CIM6 polynomial and single-cage circuit candidate in section A. Native electrical states differ from our quasi-steady algebra; full trajectory equivalence U. |
| C-01 | EasyPower | S: Transient Motor Starting with torque/load/inertia inputs (EP12). U: exact circuit-to-native conversion, normalisation and removal of electrical states; no exact candidate equation established. Only the common base conversion is specified. |
| C-01 | SKM | S: TMS module (SK11). U: versioned motor equation, circuit and mechanical field units, H conversion and electrical-state equivalence. Module availability alone cannot turn an entered acceleration time into a solved result. |
| C-01 | NEPLAN | S: static/dynamic motor starting and fitting (NP12). U: exact cage circuit, load polynomial, inertia units and native states. Fitting a curve would be a distinct approximation, not this exact-input case. |
| C-01 | PSS/E | S: historical dynamic simulation brochure includes induction-motor events (PS4). U: suitable current starting model and circuit/torque/inertia mapping; RAW/DYR model names alone do not establish start-from-rest behavior. |
| C-02 | ETAP | S: motor/starter and polynomial-load families (M04, E4/E65). I: section A conveyor curve and explicit j0.10 motor-only branch bypassed at 2 s. U: equivalent native switching, shaft continuity and separate terminal-voltage monitor implementation. |
| C-02 | PowerFactory | S: starting-device examples and explicit MDM (P79, M06). I: use explicit reactor branch and scheduled bypass with custom affine torque. U: exact native motor reduction and synthetic monitor timing. An autotransformer or soft starter is not the same impedance. |
| C-02 | PowerWorld | S: CIM6 starting and torque form (M01/M02). I: section A conveyor mapping plus explicit branch/bypass topology. U: effective native electrical states, shaft hold and monitoring timer; neither mechanical mapping nor branch entry proves complete parity. |
| C-02 | EasyPower | S: timed starts and starting arrangements (EP12). U: exact reactor-only path, preserved shaft state and affine load/monitor conversions. Do not infer a specific starter equation from the feature name. |
| C-02 | SKM | S: TMS starting study (SK11). U: native branch bypass/event ordering, affine torque entry, measurement location and timer. Native field conversion beyond declared common bases remains unresolved. |
| C-02 | NEPLAN | S: motor starting and starter families (NP12). U: exact reactor bypass and custom monitor semantics, circuit/inertia fields and affine mechanical curve. Exact time-domain mapping remains blocked. |
| C-02 | PSS/E | S: motor disturbance/event family (PS4). U: reactor starting arrangement, offline shaft initialisation, custom curve and monitor timing in the current version. No exact-input industrial starter mapping established. |
| C-03 | ETAP | S: sequence/fault studies and Star protection (E3/E11/E15). I: apply common bases and section B transformer/relay targets. U: fully uncorrected linear fault option and exact toy accumulator, instantaneous reset, latching and breaker mapping. |
| C-03 | PowerFactory | S: multiple fault methods, detailed relays and short-circuit trace (P4/P11/P88). I: section B targets, explicitly inspect pre-fault voltages. U: exact toy curve/reset implementation and transformer-side phasor conventions; complete-method initialisation is not automatically our no-load sequence oracle. |
| C-03 | PowerWorld | S: sequence/fault analysis (W82) and TIOCR1 lookup/BreakerTime (M17). I: possible relay candidate and explicit HV/LV measurement mapping in section B. U: exact analytic curve representation and current base; five-point interpolation may differ substantially. |
| C-03 | EasyPower | S: faults and protection (EP6/EP7). I: use explicit sequence/base and transformer targets. U: standard correction bypass, exact toy curve, accumulator reset, latch and breakpoint handling; a TCC time is not a complete sequence. |
| C-03 | SKM | S: A_FAULT/IEC and CAPTOR (SK5/SK9/SK10). U: exact uncorrected sequence solve and custom toy accumulator/reset. I: separately report relay trip and breaker opening, as SK19 documents their distinction. |
| C-03 | NEPLAN | S: fault and overcurrent modules (NP8/NP10). I: specified sequence/base and side-reference targets. U: native analytic relay conversion and complete q/reset/failure sequence; an IEC label does not prove the toy law. |
| C-03 | PSS/E | S: faults and dynamic line/load relays (PS2/PS4). U: exact industrial coordination candidate, no-correction fault semantics, toy law and breaker sequence. Do not infer field-setting or TCC-suite breadth from dynamic relays. |
| C-04 | ETAP | S: arc studies and time-varying/decay claims (E13/E14/E106). I: section C source-current and enclosure targets. U: exact normative inputs/coefficients and event-by-event energy algorithm; availability is not evidence of the changing-source integration method. |
| C-04 | PowerFactory | S: IEEE 1584-2018 arc function and protection (P87/P11). I: section C target field entry after checking units. U: source-by-source opening, relay-memory retention and energy accumulation semantics for this case. |
| C-04 | PowerWorld | U: native IEEE 1584-2018 arc-energy and clearing mapping in sources read (W4/W82). Fault-current support cannot supply arcing current or energy. No native conversion candidate established. |
| C-04 | EasyPower | S: 2026 Integrated method, changing currents/device memory and breaker delays (EP20/EP21/EP22). I: closest documented sequence candidate in section C. U: exact step, curve/accumulator equivalence and normative coefficients; no numeric arc parity claimed. |
| C-04 | SKM | S: arc module, breaker delay, additional-source and decrement/reduced-current options (SK6/SK19/SK22/SK23). I: section C targets. U: complete interval algorithm and exact toy relay memory; generator decrement options are not proof of every opening sequence. |
| C-04 | NEPLAN | S: 2018 method, reduced-current branch and source contributions (NP9). I: section C input targets. U: exact enclosure/field units, toy relays and sequential energy integration. Do not adopt the source's anomalous 2013 edition label. |
| C-04 | PSS/E | U: native arc method, enclosure/working-distance schema and clearing integration in PS2/PS4. No exact or approximate arc-energy conversion established; a fault study alone is insufficient. |
| C-05 | ETAP | S: harmonic flow/frequency scan (E5/E110). I: common current/ohm/SI targets in section D. U: absolute source angle reference, source normalisation, spectrum shunt and frequency-dependent field entry for this exact phasor case. |
| C-05 | PowerFactory | S: ElmIac and phase-correct spectrum, IEC summation distinction and TypLne R/L characteristics (M07-M10). I: section D conversion, 100 A rated source gives 20/14/8/5 percent. U: effective absolute phases and full native scan/model match until measured. |
| C-05 | PowerWorld | S: specialised external GICHarm route for GIC harmonics (W70/W102). U: general VSD harmonic flow/scan candidate and exact native parameter conversion. The GIC route does not establish this study. |
| C-05 | EasyPower | S: harmonic spectra/filter study (EP11). I: section D absolute current and network targets. U: angle/percentage reference, frequency-dependent field mapping and scan resolution; no complex-cancellation parity yet. |
| C-05 | SKM | S: HI_WAVE (SK12). I: section D physical targets. U: exact spectrum percentage denominator, per-phase angle convention, impedance scaling and refinement settings. |
| C-05 | NEPLAN | S: phase/sequence harmonics and adaptive scan (NP16). I: section D physical targets. U: native source-phase normalisation, load damping and scan controls; an adaptive scan needs its actual frequency samples retained. |
| C-05 | PSS/E | S: optional harmonics module (PS3). U: exact source model, phase/percentage convention, frequency scan and network frequency mapping; package naming does not close these fields. |
| C-06 | ETAP | S: ground-grid module (E107). I: section E geometry/soil/current targets. U: native solver formulation, radius/segmentation/boundary conversion and precise finite-radius equivalence. Documented online demo excludes this module (CA3). |
| C-06 | PowerFactory | U: native conductor-earth field solver for this geometry in dossier/matrix C6. No exact parameter or boundary conversion established. Transformer neutral grounding is not a ground-grid field solution. |
| C-06 | PowerWorld | U: native ground-grid/surface-potential solver and geometry mapping in sources read. GIC return resistance and electrical ground symbols do not execute the specified field problem. |
| C-06 | EasyPower | S: separate XGSLab partner route, GSA/GSA_FD/XGSA families (EP23). I: section E target a static equipotential soil solution. U: exact finite-radius formulation and input mapping; native EasyPower and separate partner entitlement remain distinct. |
| C-06 | SKM | S: GroundMat (SK16). I: section E field targets. U: whether the selected method solves this radius-resolved infinite-earth boundary problem, and exact geometry/refinement/soil entry. IEEE 80 formula output is a different model if assumptions differ. |
| C-06 | NEPLAN | U: native field solver, conductor geometry, infinite-earth boundary and sample-potential conversion in sources read. An earth-fault network return impedance cannot establish these outputs. |
| C-06 | PSS/E | U: native ground-grid field solver and geometry/soil mapping in sources read. The documented GIC function is not this conductor-earth potential problem. |
| C-07 | ETAP | S: transient stability and custom governor/UDM families (E16/E39, M19). I: section F exact equations as a possible custom target. U: native classical-machine/governor state mapping and limiter; UDM is excluded from the documented online demo (CA3). |
| C-07 | PowerFactory | S: synchronous machines/RMS, explicit per-unit turbine conversion and external-grid dynamics (P5/P17, M11/M12). I: section F base conversion/custom governor target. U: exact native classical machine/limiter; external grid is not automatically an infinite source or a valid island reference. |
| C-07 | PowerWorld | S: GENCLS, TGOV1 and power-system options (M13-M16). I: section F governor reference conversion and equal lead/lag target. U: exact electrical torque/power, speed factor and state limiting. A matched block transfer does not prove a matched complete machine. |
| C-07 | EasyPower | S: Dynamic Stability machine/governor families (EP13). U: versioned classical-machine equations, damping units, governor base/reference, bounds and release semantics. No exact native parameter set established. |
| C-07 | SKM | S: I*SIM machine/control simulation (SK13). U: classical swing/Pe convention, custom first-order governor and hard-state limit mapping; use section F targets only after field definitions are read. |
| C-07 | NEPLAN | S: RMS dynamics and user-defined controls (NP13). I: potential custom equation target in section F. U: exact machine/base, initialisation and limit implementation; user-defined support does not prove the authored model has been entered. |
| C-07 | PSS/E | S: machine/governor models and graphical model builder (PS4/PS5). U: current named native model's exact equations, damping and bounded-governor mapping. Importing a shared model name from another engine is not parameter/limiter equivalence. |

## A. Motor and starter mapping detail, C-01/C-02

The case uses algebraic single-cage circuit torque at each speed. PowerWorld's
CIM5/CIM6 circuit documentation retains electrical states (S, M01/M03), so its
time trajectory is a model variant even if steady-state circuit quantities match.
Our CIM6 candidate is I: `Ra=.02, Xa=.08, Xm=3, R1=.03, X1=.08`,
`R2=X2=0` as the documented single-cage sentinel, not a zero-ohm second physical
rotor branch. Set explicit `Mbase=2 MVA` and `H=1.2 s`; confirm actual load allocation
and any native validation changes before accepting even the fixed-speed slice.

| Authored load | CIM6 mechanical candidate (I from M01) |
| --- | --- |
| C-01A, .35+.25*w^2 | Tnom=.6, A=5/12, C0=7/12, B=D=0, E=1 |
| C-01B, 1.20+.25*w^2 | Tnom=1.45, A=5/29, C0=24/29, B=D=0, E=1 |
| C-02, .20+.30*w | Tnom=.5, B=.6, C0=.4, A=D=0, E=1 |

S, M01: initially online CIM6 recalculates Tnom/C0. An initially offline start is
therefore essential to this candidate; inspect effective values and disable or
account for native undervoltage trip and restart logic. S, M02: validation can
change cage parameters relative to timestep. Do not claim original inputs survived
unless the effective model is captured. The historical M01 timestep behavior must
be checked against the installed release, not assumed a current default.

For ETAP, single-cage without deep bar and polynomial/equation load families are
documented (S, M04); exact coefficient fields and circuit-state reduction are U.
M05 is a 2009 tutorial: its static analysis uses entered acceleration times, while
dynamic analysis needs mechanical/model data. Its synchronous example's H/WR2
entry does not prove every induction model's units. Our combined inertia is
`J=2*1.2*2000000/(2*pi*50/2)^2=194.5366725933 kg m^2` (I); never convert that to
an unverified native WR2/GD2 convention or split combined inertia twice.

PowerFactory's implicit MDM uses a power law (S, M06). No one fixed exponent and
coefficient can reproduce either positive-intercept varying curve across w=0 to 1
(I): a positive exponent gives zero at rest, a zero exponent is constant and a
negative exponent is singular there. Use a documented explicit MDM/composite route
as a candidate; exact native mechanical field entry remains U.

The reactor is j0.10 pu, or 6.05 ohm at the 60.5 ohm motor-network base (I). It
belongs only to the motor path, with an ideal bypass at 2 s. An extra motor-terminal
bus may be needed. Preserve shaft speed across the event, solve post-event algebra
before the monitoring timer, and compare terminal rather than upstream bus voltage.
Native flux transients and contactor logic require separately labelled variants.

## B. Fault and relay mapping detail, C-03

The 10 MVA bases give `Ib,11=524.8638811 A`, `Ib,33=174.9546270 A`,
`Zb,11=12.1 ohm`, `Zb,33=108.9 ohm` (I). Map zero-sequence grounding and
delta blocking explicitly, plus +30 degree positive and -30 degree negative
LV phase lead. Verify phasor reference at both sides, not just current magnitude.
An IEC voltage factor, transformer correction or pre-fault load flow is a
different specified method unless its effective equations reduce to this circuit.

Toy relay target: `M=abs(I)/Ip`, `qdot=(M^2-1)/K` above pickup, q reset
instantaneously to zero at/below pickup before trip, q=1 latched after trip.
L uses 400 A/K=.6/breaker .06 s; H uses HV 180 A/K=1.8/breaker .08 s.
These are authored test settings, not an IEC or manufacturer curve. Fault inception
is .1 s, so distinguish absolute event time from elapsed fault duration.

S, M17: TIOCR1 has five current-multiple/time points, breaker delay and ResetTime.
Its documented TimeDelay power-flow contingency description is not enough to
establish transient relay memory. A historical 2017 block-diagram source (M18)
describes piecewise interpolation and reset behavior, but that is not current-version
execution evidence. I: a lookup approximation must be checked between knots.
The table counterexample below shows why exact agreement at knots is insufficient.
Current bases, monitored branch end and trip connection remain U for this candidate.
Separate q, trip command and physical open event; downstream opening resets the
upstream untripped relay, whereas a commanded failed breaker retains fault current.

## C. Arc mapping detail, C-04

The targets are a 400 V line-line two-source grounded-wye bus, source impedances in
ohms, and the declared VCB enclosure/spacing/working distance. Convert mm/metres
only after each product's input units and interpretation are read. The independent
bolted source contributions are complex, not scalar current shares. Partition an
arcing-current estimate using the selected method's declared convention, recompute
after each source opens, and retain normal/reduced-current branch identity.

IEEE 1584-2018 coefficients, full validity bounds and exact product field mapping
are U here. No energy result is available. EasyPower's Integrated method (S,
EP21) is the most explicit inspected device-sequence candidate; its staged ANSI
current approximation, step boundaries and native device memory need comparison
against the authored case. ETAP decay/time-varying wording, SKM decrement options
and NEPLAN contribution reporting do not establish the same integration algorithm.
Fixed clearing variant A tests declared openings only; it cannot validate variant B
toy relay behavior or failed-source variant C. A 1 s cap is not an opening event.

## D. Harmonic mapping detail, C-05

I: retain `Zs(h)=.10+j*.50*h ohm`, `Zf(h)=.15+j*.30*h ohm`,
`Rphase=63.5085296109 ohm` and `Cphase=15.7839612984 microfarad`.
They are phase impedance/admittance values, not three-phase equivalent resistance
or total phase capacitance. A simple constant-inductance mapping gives
`Ls=.50/(2*pi*50)=1.591549431 mH`, `Lf=.30/(2*pi*50)=.954929659 mH`.
Do not multiply an already frequency-scaled reactance by harmonic order twice.

S, M07: ElmIac can represent a harmonic current source with zero fundamental
setpoint and zero sequence shunt conductances/susceptances. Its harmonics are
percent of rated current. I: select 100 A rated current, giving 20,14,8,5 percent
for the authored h=5,7,11,13 currents. This rating is a normalisation choice, not
a fundamental load. Output absolute phase angles must be verified before a run
is accepted: native spectrum angles may be relative to a fundamental reference.

| h | Target absolute angles, a/b/c in degrees (I) |
| --- | --- |
| 5 | 0 / 120 / -120 |
| 7 | 20 / -100 / 140 |
| 11 | -15 / 105 / -135 |
| 13 | 30 / -90 / 150 |

S, M08/M09: IEC harmonic sources use special magnitude summation rather than our
phase-coherent complex addition, including their own sequence assumptions.
Consequently that source family cannot validate the opposite-source cancellation
oracle (I). Add 180 degrees to each target phase for the second source, calibrate
actual output phasors, and retain complex cancellation residuals.
S, M10: TypLne frequency characteristics apply to R and L; constant L already
produces X proportional to frequency. Actual units/mode and damping behavior
must still be captured. Do not substitute a source calibrated against one network
impedance and assume universal equivalence after the capacitor or topology changes.

## E. Ground-grid mapping detail, C-06

The candidate must accept the original bonded 10 m square grid and corner rods,
burial/length/radius data, uniform 100 ohm m soil, 1000 A net injection and insulated
ground surface/infinite return. No voltage-network base conversion is needed.
Record radius versus diameter, centreline versus surface representation, segment
connectivity and the infinity approximation. A perfectly conducting equipotential
electrode differs from a resistive metal network unless that resistance is disabled.

ETAP Ground Grid, SKM GroundMat and the separate XGSLab route are documentary
candidates, not established equivalent field solvers. A selected IEEE analytical
formula or thin-wire model is a named approximation unless its geometric/physics
equivalence is independently established. The required sample includes V(7,0,0).
Linearity scaling tests do not establish spatial accuracy or touch-voltage safety.
No native field mapping or numerical ground-grid solution has been executed.

## F. Islanded genset mapping detail, C-07

Targets: S=2 MVA, H=2 s, D=1, R=.05, Tg=.4 s, nominal 50 Hz and the authored
fixed-admittance load steps. Initial `Pref=Pm=Pe0=.2859740161357524 pu` includes
stator loss in internal electrical power. A terminal P meter would omit that loss.
The state is speed w with synchronous value 1, while many native models store
deviation `dw=w-1`. Use `f=50*w` before any bus-frequency filtering. No added AVR,
frequency-sensitive load or external physical slack is part of the exact case.

S, M13: TGOV1 sums its reference and auxiliary input with negative speed deviation
before division by R, unlike the case's Pref convention. I, for equal machine and
turbine bases and zero auxiliary input, candidate native reference is
`R*Pref=.01429870080678762`, not Pref. `T1=.4`, positive `T2=T3=1 s`
and `Dt=0` reduce the lead-lag transfer algebra to the authored first-order governor
when all internal states are consistently initialised. Equal 1 s constants are an
authored cancellation choice, not a vendor default or engineering turbine value.
Record validation and Fixed/DownOnly response effects (S, M14).

The above is transfer algebra only. C-07B limits the Pm state itself with outward
hold and immediate inward release. Native valve limits, turbine states, clipping
and anti-windup need separate proof; VMIN/VMAX field names alone do not establish
that equivalence. Even C-07A requires proving no active native limit changed it.

S, M15/M16: GENCLS help links a GENCLS_PLAYBACK diagram with speed-dependent
mechanical conversion and the option to ignore speed effects. Native speed
deviation, the `(1+dw)` conversion, electrical torque versus power and D convention
must be resolved before asserting the authored swing equation. The option is a
candidate control, not proof of a complete equivalent model. Check default system
frequency, small-island retention and initial-limit repair options; none is assumed.

S, M11: PowerFactory's RMS external grid includes internal impedance and mechanical
frequency response, so it is not automatically a stiff infinite source. It must
not supply this generator island. S, M12: turbine output conversion follows the
turbine/generator power bases, `pt=pt_t*Pnt/Png`. I: use equal declared bases to
avoid scaling in a custom target; exact native governor/limiter entry remains U.
ETAP's custom dynamic compiler supports governor/load/relay families (S, M19),
but custom equation entry, compiled state semantics and usable entitlement remain U.

## Authored observations, separate from all product execution

Recomputed 2026-10-17 using CPython 3.12.14, NumPy 2.4.6 and SciPy 1.18.1.
Inputs are the original case equations and synthetic signals below. No vendor
library, project, binary, fitted parameters or solver was used. These observations
check our own mappings and oracles; they are not claims of product correctness.

| Original check and inputs | Tool/method and observed result | Boundary |
| --- | --- | --- |
| C-01A/C-02 torque mappings above; 101 equally spaced w from 0 to 1 | NumPy evaluation, maximum absolute difference below 1e-15 pu for both polynomial identities | Mechanical curves only; C-01B mapping is algebraic, not included in this sampled check |
| TGOV1 reference conversion with speed deviations -.01,0,.01 | NumPy algebra, difference below 1e-15 pu; candidate native reference .01429870080678762 | No native governor, initialisation or limiter tested |
| Toy K=.6 relay, M=2 on [0,.1], .5 on [.1,.3], 3 on [.3,.5]; instantaneous reset; breaker .06 | Independent piecewise accumulation and solve_ivp crossing: trip .3750000000 s, open .4350000000 s | New synthetic signal, not the C-03 fault network or a vendor run |
| Same synthetic signal, explicitly changed timed-reset law qdot=-(1-M^2)/1 below pickup, floored at zero | Piecewise arithmetic gives trip .3487500000 s | A deliberate model variant shows reset semantics matter |
| Toy t(M)=.6/(M^2-1); knots M=2 and 3; midpoint M=2.5 | Exact .1142857142857143 s; linear knot interpolation .1375 s, 20.3125 percent larger | Hypothetical table approximation, not a measured product error |
| C-07B exact input equations, step at 1 s, shed at 5 s, end 12 s, upper Pm=.35 | Matrix exponential/free state, scalar exponential/bounded state and event ODE: hit 1.283004509420 s; release 7.839450499088 s | Exact authored state-limiter model only |
| Same C-07B, w at load shed and final (w,Pm) | w(5)=.927305061141; w(12)=1.000009904871; Pm(12)=.286098543571 pu; matrix/ODE final difference 8.2e-18 pu | No claim about native limiter or filtered bus frequency |

For reproducibility, let x=w-1, p=Pm and L=Pe. Between load events the free
state z=[x,p] has
`A=[[-D/(2H),1/(2H)],[-1/(R*Tg),-1/Tg]]`,
`b=[-L/(2H),Pref/Tg]`, `zeq=-solve(A,b)` and
`z(t)=zeq+expm(A*t)*(z(0)-zeq)`. Compute L directly as
`real(conj(Y/(1+(.02+.20j)*Y)))` for Y=.30-.10j or .50-.15j.
Find the first p=.35 crossing with scalar root finding. While bounded,
`x(t)=xeq+(x0-xeq)*exp(-D*t/(2H))`, `xeq=(.35-L)/D`.
Release when `x=R*(Pref-.35)` after shedding; then use the free solution again.
The independent ODE used rtol=1e-11, atol=1e-13, max_step=.001 s and event
localisation with consistent projection to the bound. Hit/release agreement was
below 1e-10 s. Numerical self-agreement does not validate generator physics.

The earlier [authored observations](comparison-cases.md#authored-checks-and-execution-status)
remain separate: C-04 has only bolted-current arithmetic; C-06 has no field result.
No additional arcing, soil or commercial model output is inferred here.

## Specific primary mapping sources

Accessed/read 2026-10-17. Historical dates are retained. Attachments were not used
as case inputs. PDF inspection listed below covers selected public model diagrams,
not a licensed product execution or an exhaustive model manual review.

| ID | Primary source and inspected scope |
| --- | --- |
| M01 | [PowerWorld motor starting](https://www.powerworld.com/knowledge-base/motor-load-starting-using-transient-stability), 2013 article: CIM5/CIM6 torque and online/offline initialisation; example not imported |
| M02 | [CIM6 help](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Load%20Characteristic%20CIM6.htm), parameter bases and validation changes |
| M03 | [CIM5 public model PDF](https://www.powerworld.com/WebHelp/Content/TransientModels_PDF/Load/Load_Characteristic/Load%20Characteristic%20CIM5.pdf), text: cage sentinel and electrical states |
| M04 | [ETAP motor modelling](https://etap.com/motor-starting/libraries-modeling), circuit and mechanical-load families |
| M05 | [ETAP motor tutorial](https://etap.com/docs/default-source/faqs-tutorials/motor-acceleration-analysis.pdf), 2009, four pages' text: static entered time versus dynamic model and inertia |
| M06 | [PowerFactory implicit MDM](https://www.digsilent.de/index.php/en/faq-reader-powerfactory/how-is-the-mdm-motor-driven-machine-torque-calculated-when-no-machine-is-explicitly-modelled-for-an-asynchronous-machine.html), default power law and explicit driven-machine route |
| M07 | [PowerFactory harmonic current source](https://www.digsilent.de/en/faq-reader-powerfactory/how-can-a-harmonic-voltage-spectrum-be-converted-to-a-harmonic-current-injection.html), ElmIac normalisation and source shunts |
| M08 | [PowerFactory IEC harmonic summation](https://www.digsilent.de/en/faq-reader-powerfactory/how-are-IEC-61000-sources-taken-into-account-in-the-harmonic-load-flow.html), magnitude law versus phasor sums |
| M09 | [PowerFactory unbalanced IEC source](https://www.digsilent.de/en/faq-reader-powerfactory/how-do-you-model-a-harmonic-current-injection-based-on-iec-as-an-unbalanced-source.html), sequence and summation qualification |
| M10 | [PowerFactory TypLne frequency data](https://faq.digsilent.de/en/faq-reader-powerfactory/how-do-you-model-frequency-dependent-line-parameters-for-cables-and-overhead-lines-for-harmonic-analysis-using-typlne.html), R and inductance rather than direct X multiplier |
| M11 | [PowerFactory external grid in RMS](https://www.digsilent.de/en/faq-reader-powerfactory/how-is-the-external-grid-modeled-for-rms-simulation.html), electrical and mechanical/frequency behavior |
| M12 | [PowerFactory turbine/generator bases](https://www.digsilent.de/en/faq-reader-powerfactory/how-does-powerfactory-interpret-p-u-values-for-turbine-and-generator-models.html), power-base conversion |
| M13 | [TGOV1 public diagram](https://www.powerworld.com/WebHelp/Content/TransientModels_PDF/Generator/Governor/Governor%20TGOV1.pdf), one page visually inspected: summing/gain placement, lead-lag, limits and bases |
| M14 | [TGOV1/TGOV1D help](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Governor%20TGOV1%20and%20TGOV1D.htm), validation/initial-limit controls |
| M15 | [GENCLS help](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Machine%20Model%20GENCLS.htm) and [linked GENCLS_PLAYBACK PDF](https://www.powerworld.com/WebHelp/Content/TransientModels_PDF/Generator/Machine/Machine%20Model%20GENCLS_PLAYBACK.pdf), one-page diagram visually inspected; linked-model identity retained |
| M16 | [PowerWorld system-model options](https://www.powerworld.com/WebHelp/Content/MainDocumentation_HTML/Transient_Stability_Dialog_Options_Power_System_Model.htm), speed effects, islands and system frequency |
| M17 | [TIOCR1 help](https://www.powerworld.com/WebHelp/Content/TransientModels_HTML/Line%20Relays%20TIOCR1.htm), lookup points, reset and breaker fields |
| M18 | [PowerWorld 2017 block diagrams](https://www.powerworld.com/files/Block-Diagrams-17.pdf), indexed TIOCR1 description; full PDF not newly rendered, historical semantics require current-version confirmation |
| M19 | [ETAP dynamic model compiler](https://etap.com/user-defined-dynamic-models/dynamic-model-compilers), custom model families; no custom model compiled |

No exact-model vendor parity verdict is currently possible. Next evidence must
resolve the U fields through versioned primary definitions and legitimate ordinary
input/output runs, with approximations recorded separately. Research remains
distinct from build approval and from reconstructing any proprietary source code.
