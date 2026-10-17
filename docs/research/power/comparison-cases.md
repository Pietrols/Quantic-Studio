# Original power-software comparison cases

WP-2.15, ChatGPT, 2026-10-17. Original synthetic inputs for feature-by-feature
comparison, led by mining and industrial workflows. These are research fixtures,
not designs for a mine, manufacturer models, safety settings or copied vendor/book
cases. No reference product has been run for this document. Numerical observations
from any future product execution must be dated and kept distinct from the authored
analytical checks recorded below.

## Protocol and evidence

Use [R-001 to R-052](reconstruction-requirements.md) as the obligations being tested.
S means a cited primary source states the behavior, I means our inference and U means
not established. The fixtures and tolerance choices here are our proposals, class I.
Actual product output for every case is currently U. A documented module is S for
availability, not evidence that it accepts our exact model or produces a passing result.

Comparison uses ordinary supported inputs and outputs. Do not inspect, decompile,
trace or instrument proprietary product code. No REA binaries, decompilers or
reference-product implementation material are part of this work. A license holder
may operate within the applicable terms; evaluation/student access is not assumed
to authorize commercial use, automated benchmarking or publication of results.

| Case | Feature | Visible electrical buses | Principal R-IDs |
| --- | --- | ---: | --- |
| C-01 | Synthetic mill load, direct-on-line starting | 2 | R-007, R-009, R-015, R-017, R-020, R-047 |
| C-02 | Synthetic conveyor load, reactor start and bypass | 2 | R-009, R-015, R-019, R-020, R-021, R-026 |
| C-03 | 33/11 kV fault paths and coordination | 3 | R-006, R-023, R-024, R-025, R-026, R-027 |
| C-04 | Two-source 400 V arc bus and changing clearing paths | 1 | R-024, R-027, R-028, R-029, R-030, R-043 |
| C-05 | Synthetic VSD harmonic injections and capacitor resonance | 2 | R-014, R-031, R-034, R-044, R-048 |
| C-06 | Ground grid and surface potentials | 0 network buses | R-025, R-031, R-035, R-048, R-051 |
| C-07 | Islanded generator pickup and governor limit | 1 | R-010, R-017, R-018, R-019, R-020, R-022, R-044 |

Internal machine/source nodes, terminals and grid conductors may count differently
toward a product's entitlement. Confirm the installed limit; the counts above are
not a promise that a demo can execute every case. Node count alone does not establish
module, model, editing or export availability.

### Common input and result contract

All cases use SI units, 50 Hz, phase order a-b-c and RMS phasors with positive
rotation. The phase-a source reference is zero degrees. Positive branch current is
from the named source toward the load/fault. Consumed P and Q are positive;
capacitive shunt susceptance is positive in Y. Report both magnitude and angle where
a phasor is requested. A three-phase power base S and line-line voltage base V imply
phase voltage V/sqrt(3), current S/(sqrt(3)*V) and impedance V^2/S. Use radians in
equations and explicitly convert displayed degrees. Parameters are exact decimal
fixture choices; displayed calculations may be rounded.

Unlisted elements do not exist: no hidden loads, shunts, charging, mutual coupling,
tap regulation, saturation, temperature adjustment or automatic protection. Where
a case requests a custom mathematical element, enter its stated equations. A
closest built-in model is a separately named approximation, not the same-input case.
If an interface demands an additional physical parameter, record it as an unresolved
mapping and do not guess a default or declare the exact case executed.

For each run record product/build, licensed modules, OS/access route, case/revision,
input hash, field-by-field model mapping, requested/effective inputs, reference
frame, study method/edition, control settings, initialization policy, integrator,
internal maximum step, tolerances, event ordering, stored cadence, meter processing,
raw results and diagnostics. Unavailable fields are U, not assumed zero. If a default
cannot be disabled or inspected, the mapping is unresolved. Store unrounded values
where permitted; retain display precision when only a screen can be read.
Request a 1e-9 pu static residual tolerance and 100 maximum nonlinear iterations.
For adaptive dynamics request rtol=1e-8 and atol=1e-10 pu, alongside the stated step
limit; record products that expose different controls. Exact circuit cases need no
nonlinear iteration. A different numerical method may be compared after refinement,
but hidden/inequivalent physical equations cannot be normalized away.

Every product gets the same record: ETAP, PowerFactory, PowerWorld, EasyPower, SKM,
NEPLAN and PSS/E. An unavailable module or inequivalent model produces a documented
not-executed/approximation outcome, not a fabricated output. Compare ordinary
observable behavior only. No user accounts, demo activations or contacts were created
for this pass; no installed entitlement or licensed collaborator is confirmed.

### Tolerance rules

These are proposed numerical research gates, not standard-prescribed engineering
limits. Fix them before a comparison; investigate differences without loosening them
to obtain a pass. Normalize volts/amps/power to the declared case bases; use 1 rad
for angle and the named physical scale for other quantities. Apply
`abs(x_product-x_reference) <= a + r*max(abs(x_reference), scale)`.

| Rule | Gate and prerequisites |
| --- | --- |
| N: matched static algebra | a=1e-6 pu, r=1e-5, scale=1 pu; wrapped angle a=1e-5 rad. KCL and power-balance residuals must also meet the declared solver tolerance. |
| D: matched dynamics | At common times away from discontinuities, a=1e-4 pu, r=1e-3, scale=1 pu. Halve internal maximum step until the independent solution change is below one quarter of that gate. Require the same event ordering, limit state and qualitative outcome. |
| E: event timing | Scheduled events have exactly the authored time. State-triggered crossing error must be no more than 1 ms after refinement to a maximum step of 0.25 ms near the crossing. Compare left/right limits separately. |
| F: field solution | For grid resistance and defined sampled potentials, a=0, r=0.01, scale=the larger absolute reference value in that quantity's sample set. Mesh/domain refinement change must be below 0.25% first. This tests numerical agreement, not touch-voltage safety. |
| R: rounded observations | Record half the last displayed unit as observation uncertainty. If that exceeds the applicable gate, mark insufficient precision; do not widen the gate. |
| M: method/model mismatch | No numerical parity verdict until equations, method edition, corrections, controls and outputs match. Report the mismatch and compare invariant/qualitative checks separately. |

Use N for currents, circuit voltages, torque-speed algebra and harmonic phasors;
D/E for trajectories and operation times; F for C-06. C-04 normative arc outputs
use N only after the exact same method, inputs and coefficients are established;
otherwise M. Statistical or empirical model uncertainty is not solver roundoff.

## C-01: Mill starting, with explicit mechanical load

Input origin: I, authored here. Method evidence: requirements R-009/R-015 and
[Glover/Kundur/Das method ledger](../../sources/entries/power-reconstruction-book-methods-2026-10-17.yaml).
The word mill describes the workflow; this torque curve is not claimed to represent
a real mill. The primary comparison intentionally omits electromagnetic flux
transients so the electromechanical calculation has an independent circuit oracle.

| Input | Exact value or definition |
| --- | --- |
| Bases | S=2,000,000 VA three-phase; V=11,000 V line-line; 50 Hz; four poles |
| Network | At U, external source internal emf 1+j0 pu behind Zs=0.005+j0.03 pu; feeder U to M with Zf=0.005+j0.02 pu. U is the source connection bus, not an ideal fixed-voltage bus. Zs participates in the starting/load-flow circuit, not only in faults. |
| Background at M | Fixed admittance Ybg=0.10-j0.05 pu, connected throughout |
| Motor circuit | Per-phase equivalent: stator Rs=0.02, Xls=0.08; rotor referred to stator Rr=0.03, Xlr=0.08; magnetizing Xm=3.0; all pu on these bases. No core-loss resistance. |
| Mechanics | H=1.2 s for combined motor/load; synchronous mechanical speed ws=2*pi*50/2 rad/s; J=2*H*S/ws^2 kg m^2; torque base S/ws N m |
| Load | Tl(w)=0.35+0.25*w^2 pu, where w is mechanical speed/ws |
| State/events | Motor open initially, shaft held at w=0 while disconnected. At t=0.2 s release shaft and close motor. Run to 10 s. No relay or starter; no automatic speed reset. |
| Initialization/output | Solve the background-only network first. Store time points every 0.01 s plus event left/right states; maximum internal step initially 1 ms; refine for D/E. |

For `s=1-w`, define the rotor branch `Zr=Rr/s+j*Xlr`, magnetizing `Zm=j*Xm`,
parallel air-gap impedance `Zp=Zm*Zr/(Zm+Zr)`, and `Zmot=Rs+j*Xls+Zp`.
Then `Vm=1/(1+(Zs+Zf)*(Ybg+1/Zmot))`, `Im=Vm/Zmot`,
`Eg=Vm-Im*(Rs+j*Xls)`, `Ir=Eg/Zr`, and `Te=abs(Ir)^2*Rr/s` pu.
Use the continuous s-to-zero limit (Te=0, rotor current=0), not division by zero.
Mechanical evolution is `dw/dt=(Te-Tl)/(2*H)`. There is no additional damping or
mechanical efficiency factor. The disconnected shaft-hold is a test initialization
condition, not an implicit friction model. After connection a negative torque may
produce reversal; do not clamp speed silently.

Variants: C-01A as above; C-01B replace only Tl by `1.20+0.25*w^2`, keeping all
else identical. Terminate B when speed first crosses zero downward after release,
if it occurs, and label failed acceleration; do not assert stall from a static dip.
An implementation that cannot resolve the initial negative acceleration must report
that limitation. Use the same right-side torque to determine the initial outcome.

Record: prestart and initial post-close voltage, source/motor current and P/Q;
w, slip, Te, Tl, accelerating torque and electrical losses versus time; first
crossings of w=0.8 and w=0.95 if reached; minimum terminal voltage with its time;
final mechanical state, initialization residuals and diagnostics. These crossing
levels are fixture reporting thresholds, not equipment acceptance limits.

Independent check: evaluate the circuit directly for fixed w, integrate acceleration
independently (or quadrature `dt=2H*dw/(Te-Tl)` only on intervals with nonzero positive
accelerating torque), and verify `d(H*w^2)/dt=w*(Te-Tl)` in pu power/seconds.
Crossing time, N/D/E and the same success/failure classification are required.

Product capture: enter this circuit/load equation if supported; record whether the
product instead retains rotor/stator flux states, fits parameters, adds friction
or assumes another mechanical curve. Built-in dynamic motor results with different
equations are comparison variants under M. A static starting-dip solve can execute
only the w=0 slice and must not supply invented acceleration time.
If the grid element uses its impedance only for faults, create an explicit internal
ideal-source node and Zs branch for this case. Count that extra node against the
actual entitlement; do not replace U by a fixed 1 pu slack and omit the voltage drop.

## C-02: Conveyor reactor start and bypass

Input origin: I, authored here. R-009/R-015/R-019/R-020/R-021/R-026.
Use all C-01 inputs/equations except the exact overrides below.

| Override | Value |
| --- | --- |
| Mechanical load | Tl(w)=0.20+0.30*w pu; combined H remains 1.2 s |
| Starting reactor | Zstart=j0.10 pu in series with the motor only, not with Ybg |
| Events | Close motor and release shaft at 0.2 s; bypass reactor at exactly 2.0 s, retaining shaft speed. End 10 s. |
| Algebra while reactor inserted | Ymotor=1/(Zstart+Zmot); bus voltage uses Ymotor; Im=Vm/(Zstart+Zmot); actual motor terminal Vmot=Vm-Im*Zstart. Use Vmot for the stator/rotor circuit. |

C-02A uses scheduled bypass; C-02B leaves the reactor inserted for the whole run.
No relay acts in either primary run. Add a separately labelled monitoring test:
record whether `abs(Vmot)<0.65 pu` continuously for 0.30 s after connection. Its
timer resets immediately when voltage recovers, includes equality as recovered,
and its flag does not trip anything. At an event, evaluate the post-event algebra
before updating that timer. These are authored logic values, not a real contactor specification.

Record all C-01 outputs plus bus versus actual motor-terminal voltage, reactor
current/drop, speed immediately before/after bypass, transient algebraic current
step, monitor pickup/reset/flag times and the unreached-threshold outcome where
applicable. Verify speed continuity across the ideal bypass, torque/current changes
and mechanical energy balance on either side. Use N/D/E. Compare the declared timer
to an independent piecewise signal evaluator; no TCC thermal safety claim follows.
Product capture includes actual starter connection, transition rule, shaft state
and whether the measurement uses the bus or motor terminal.

## C-03: 33/11 kV faults and coordination

Input origin: I, authored here. R-006/R-023 to R-027. This first run is a defined
linear sequence-network calculation, not an unqualified IEC 60909 result.

| Input | Value |
| --- | --- |
| Bases and buses | S=10 MVA; B33=33 kV; B11 and F11=11 kV, line-line; nominal transformer ratio matches bases |
| Source at B33 | Positive E1=1+j0 pu; negative/zero sources zero. Z1=Z2=0.02+j0.15 pu; Z0=0.04+j0.25 pu. All sequence impedances on these local bases. |
| Transformer B33 to B11 | Ideal delta HV, grounded-wye LV, in series with Z1=Z2=0.01+j0.08 pu. Zero-sequence LV-to-earth Z0=0.01+j0.08 pu; no transfer of zero-sequence line current to HV; neutral impedance zero. |
| Phase convention | Positive-sequence no-load LV phase voltage leads the corresponding reconstructed HV phase reference by 30 degrees; negative sequence shifts by -30 degrees. This mathematical convention is authoritative if a product's vector-group label differs. |
| Feeder B11 to F11 | Z1=Z2=0.015+j0.04 pu; Z0=0.045+j0.12 pu; no mutual coupling/shunts |
| Other equipment | No motors, generators, loads or correction factors. Prefault voltage is the no-load solution. All source/line data fixed at authored values; no temperature corrections. |
| Fault sweep | At B33 and F11 independently: 3-phase-to-earth, a-earth, b-c, b-c-earth. Each has Zf=0, then Zf=0.05+j0.02 pu on the fault-bus base. Restore base between all 16 solves. |
| Fault definition | 3-phase: each phase to earth through Zf; a-earth: a through Zf; b-c: phases joined through Zf; b-c-earth: b and c directly joined, common point through Zf to earth. |

Use `a=exp(j*2*pi/3)` and
`[Va,Vb,Vc]=[V0+V1+V2,V0+a^2*V1+a*V2,V0+a*V1+a^2*V2]`.
Current transformation is identical. Record source reference and per-side angles,
not just magnitudes. For this network each fault-point sequence driving impedance
is obtainable by direct series reduction; verify with an independent phase circuit.

Coordination extension C-03P: only the bolted 3-phase fault at F11. Place relay L at
the B11 feeder entrance and relay H on the transformer's B33 terminal. CT ratios
are 600:1 A and 300:1 A respectively, polarity toward the transformer/feeder load.
Primary pickups are 400 A (L) and 180 A (H). The authored relay has accumulator q=0:
`dq/dt=((I/Ip)^2-1)/K` if `I>Ip`; otherwise reset q=0 immediately.
Trip when q reaches 1; K_L=0.6 s and K_H=1.8 s. Breaker opening delays are 0.06 s
and 0.08 s. There is no intentional minimum time, reclosing or directional logic.
At trip, hold q=1 and latch the trip command through the case; subsequent current
loss does not cancel an already issued opening command. Reset applies only before trip.
These are toy curves, not IEC/IEEE/manufacturer curves. I is the RMS magnitude of
phase-a current through that relay; all phases are balanced in this extension.

Apply the fault at 0.1 s after a no-load prefault period, run to 2.0 s, integrate
both relay states and re-solve after the first breaker opens. Reset a relay when
its current disappears before tripping. C-03P-fail prevents L's breaker opening
after its trip, allowing H backup; keep the failed L trip indication. Record
pickup, q(t), trip, breaker command/open time, current at each device, clearing
element and final fault-energized state. Exact constant-current relay timing before
any opening is `K/((I/Ip)^2-1)`, plus breaker delay for interruption.

Record for all faults: phase/sequence currents at the fault and each source/branch,
bus phase/sequence voltages, contribution sums, transformer side angles, units and
diagnostics. N applies; relay/event extension uses E and exact piecewise accumulation.
The 33 kV earth fault must not be fed by an invented path through the delta HV winding.

Product capture: ordinary prefault/superposition settings if the declared network
can be represented. A second, explicitly separate IEC study may request the named
edition and record every effective c/K factor and machine treatment, but cannot
be compared to the uncorrected oracle as the same method. If a demo cannot define
the toy relay, fault values remain comparable and coordination is not executed.

## C-04: Two-source arc bus

Input origin: I, authored here. R-024/R-027 to R-030/R-043. The bus, enclosure and
relay values are synthetic. No incident-energy or PPE answer is asserted here.

| Input | Value |
| --- | --- |
| Bus/source | One 400 V line-line bus A; 50 Hz; two grounded-wye ideal sources at phase-a 400/sqrt(3) V angle zero |
| Source impedances | Per-phase source-to-bus Z1=0.001+j0.004 ohm, Z2=0.002+j0.006 ohm; identical for positive/negative/zero sequences; neutral/earth ideal. Source currents separately measured. |
| Load/fault | No prefault load. Three-phase bolted fault baseline at A; arc exposure at A on the load side of both source breakers. No current-limiting device. |
| Requested empirical method | IEEE 1584-2018, three-phase AC, VCB configuration; enclosure H=600 mm, W=600 mm, D=400 mm; gap=32 mm; working distance=600 mm. Report whether the implementation accepts this domain and its corrections. |
| C-04A timing | Fault/arc begins at t=0.1 s. Source 1 opens at elapsed 0.08 s, source 2 at elapsed 0.20 s. These are total interruption times, with no additional opening delay. |
| C-04B protection | Replace scheduled opening with the C-03P accumulator rule. Source 1: Ip=4,000 A, K=1.0 s; source 2: Ip=2,500 A, K=0.8 s. Breaker delays 0.06/0.08 s; integrate their own branch arcing-current magnitudes, not bolted-current bus total. |
| C-04C backup failure | Same as B but source 1 breaker fails to open. Stop at elapsed 1.0 s and report the still-energized arc and the administrative cap separately. |

For A/B/C run each method-prescribed normal and reduced arcing-current alternative
separately; the method defines its reduction, not an assumed 85% factor. Record the
effective current multiplier/equation and edition. On a clearing action, recalculate
the remaining source network and method-dependent arc current using the same
declared policy. For this fixture, partition the bus arcing-current magnitude by
the complex bolted-current shares: `Iarc_k=Ibolted_k*Iarc_bus/abs(Ibolted_bus)`.
Recompute shares after an opening. Assume the arc persists while a source remains;
there is no extra extinction/reignition rule. Compute each interval's method energy
for its actual duration, then add the interval energies. Record a product that
cannot express this partition/accumulation policy as a different model under M.
A tool that computes one fixed-current exposure rather than
re-solving must be recorded as a different variant. In B use post-action currents
for further relay accumulation; q carries across current changes until reset/trip.

Record bolted currents per source/bus; normal/reduced arcing currents per source
and interval; source/device search and location; relay q, trip and opening times;
energy increments, cumulative incident energy (J/cm^2 and cal/cm^2 with stated
conversion), duration/cap and limiting branch; enclosure corrections and validity
messages. Request an unformatted intermediate report if available; unavailable
intermediates remain U. Labels alone cannot validate interval integration.

Independent check: bolted phase currents follow the two stated impedances; timed
clearing and toy relay timing have independent circuit/event checks. Normative arc
current/energy comparison requires the same readable method/coefficient revision,
not coefficients recalled from memory or the flagged Das table. Record method
outputs as observations until that oracle exists. Use N/E on matched quantities and
M elsewhere. Do not claim that reduced current must give lower energy; test it.
If normative accumulation cannot be inspected, state U for the mechanism even when
a final energy number is visible. No automatic PPE recommendation is requested.

## C-05: VSD harmonics and resonance

Input origin: I, authored here. R-014/R-031/R-034/R-044/R-048. This is a linear
emission-source test, not a switching-level VSD or a manufacturer spectrum.

| Input | Value |
| --- | --- |
| Network | Two buses U and H at 11 kV line-line; ideal source U, 50 Hz fundamental voltage, zero source harmonic voltages |
| Grid/feeder per phase | Source impedance Zs(h)=0.10+j*0.50*h ohm; feeder U to H Zf(h)=0.15+j*0.30*h ohm. No mutual coupling or shunts. Z at noninteger h uses the same formula. |
| Background | At H, three equal phase-earth resistors R=11,000/(sqrt(3)*100) ohm, present at every frequency |
| Capacitor | Grounded-wye, each phase C=600,000/(2*pi*50*11,000^2) F; no series reactor, no losses in capacitor |
| Harmonic injection into H, phase a | I5=20 A at 0 degrees; I7=14 A at 20 degrees; I11=8 A at -15 degrees; I13=5 A at 30 degrees; all other nonfundamental source currents zero |
| Phase definition | For each order h, Ib=Ia*exp(-j*h*2*pi/3), Ic=Ia*exp(j*h*2*pi/3); phasor magnitudes RMS |
| Fundamental | No imposed fundamental drive-current source; only the resistors and capacitor load the fundamental. Calculate the actual fundamental currents for distortion denominators. |
| Scan | 100 to 1,250 Hz inclusive, 5 Hz initial spacing. Refine around each detected peak/minimum to 0.5 Hz, then 0.05 Hz, until N/frequency stability is established. |

C-05A capacitor connected; C-05B capacitor open; C-05C uses A plus a second
co-located source exactly opposite to the first at every specified harmonic.
For scans remove all emission sources, inject 1 A phase-a harmonic current at H
with b/c injection zero, and calculate driving/transfer impedances. This scan is
separate from the balanced three-phase emission solves; identical uncoupled phase
circuits make the single-phase driving-point check unambiguous.

Record fundamental operating point; each phase/harmonic voltage and branch current
with angle; order-specific individual distortion and voltage THD with the actual
fundamental denominator; RMS summed current with the included-order list; impedance
magnitude/phase and refined resonance frequencies. Do not report TDD against an
invented maximum-demand current or an IEEE 519 compliance verdict without a sourced
assessment point and limits. Fixed-R and linear-X frequency models are intentional.

Independent check per phase/frequency:
`Y=1/(Zs+Zf)+1/R+j*2*pi*f*C`, capacitor term zero in B;
`Vh=Ih/Y` and driving impedance `1/Y`. Fundamental voltage follows the corresponding
voltage-divider circuit. C cancels all imposed harmonic injections exactly; any
residual must fit numerical precision, not a changed spectrum convention. Use N;
resonance locations must stabilize within 0.05 Hz after the last refinement.
Record whether a product changes source angle with fundamental terminal angle,
uses fundamental-frequency impedance at all orders or adds default harmonic damping.

## C-06: Ground grid and surface potential

Input origin: I, authored here. R-025/R-031/R-035/R-048/R-051. This fully specifies a
static conduction field problem. It does not specify a human shock-safety method;
that would be a separate standards-backed study with additional physiological and
surface-layer inputs. Do not substitute such a safety verdict for field verification.

| Input | Value |
| --- | --- |
| Coordinates | Cartesian metres; soil z<0, air z>0, ground surface z=0 |
| Horizontal conductors | Four perimeter segments joining (-5,-5,-0.5), (5,-5,-0.5), (5,5,-0.5), (-5,5,-0.5), then close; plus cross segments (-5,0,-0.5) to (5,0,-0.5) and (0,-5,-0.5) to (0,5,-0.5) |
| Rods | At each perimeter corner, vertical segment z=-0.5 to -3.5; radius 0.008 m |
| Metal model | Horizontal radius 0.01 m; all metal perfectly conducting, all intersections/end contacts bonded; all connected surfaces at the same solved grid potential |
| Soil | Uniform isotropic resistivity rho=100 ohm m; linear DC conduction, no frequency dependence or ionization; no surface layer |
| Injection and return | Net 1,000 A injected into grid; infinity at zero potential; no parallel metallic return or current split to another electrode |
| Boundary problem | Outside conductors, div(sigma*grad(V))=0, sigma=1/rho; zero normal current at air/soil interface; integrated outward grid current=1,000 A into soil; V tends to zero at infinity |

Use infinite-earth/BEM formulation if available. For a finite-domain implementation,
use a hemispherical soil domain centered at (0,0,0), radii 100, 200, 400 m in turn,
zero potential on curved outer boundary and insulation on its planar surface.
Refine radius and conductor/soil discretization independently until the F gate's
0.25% change criterion is met; extend beyond 400 m if needed. Record the effective
conductor-surface/centerline approximation. A thin-wire formula is a named alternate,
not assumed equivalent to the finite-radius field model.

Record grid potential Vg, Rg=Vg/1,000 A, current per segment/rod, net current
balance and surface potentials at (x,0,0) for x=-10,-6,-5,0,5,6,10 m and at
(-6,-5,0), (6,5,0). Also record the authored step difference
`V(6,0,0)-V(7,0,0)` and touch-like difference `Vg-V(6,0,0)`.
The latter labels describe mathematical potential differences only, not a sourced
IEEE touch criterion. Request V(7,0,0) explicitly in addition to the sample list.

C-06A as above; C-06B changes injection to 500 A; C-06C changes rho to 200 ohm m
and restores injection to 1,000 A. Geometry is unchanged. Linearity demands that B
halves potentials with unchanged Rg, while C doubles potentials and Rg, within
solver error. Independent verification requires a separately implemented field
solution or a geometry-matched analytical reduction with declared approximation,
plus F and current balance. Scaling alone does not validate spatial accuracy.

Product capture: exact soil/electrode model, segmentation, boundary treatment and
current split; whether the product is a grid solver, an analytic IEEE formula or a
partner product. ETAP demo documentation excludes its ground-grid module. EasyPower's
XGSLab route needs its own legitimate access; it is not a confirmed native module.

## C-07: Islanded genset pickup

Input origin: I, authored here. R-010/R-017 to R-022/R-044. This is an explicit
classical source and first-order governor test, not a complete diesel engine,
exciter, black-start or frequency-dependent motor model.

| Input | Value |
| --- | --- |
| Bases | S=2 MVA, V=11 kV line-line, f=50 Hz |
| Electrical island | One generator internal source E=1 pu behind Zg=0.02+j0.20 pu supplying bus G; voltage phase is delta, no external grid or slack supplying power |
| Background load | Fixed admittance Y0=0.30-j0.10 pu |
| Pickup | At t=1.0 s connect Ystep=0.20-j0.05 pu in parallel; at t=5.0 s disconnect only Ystep; run 12 s |
| Machine | H=2 s; D=1 pu power per pu speed deviation; no saturation/flux states. `2H*dw/dt=Pm-Pe-D*(w-1)` and `d(delta)/dt=2*pi*50*(w-1)`. |
| Governor | R=0.05 pu speed/pu power; Tg=0.4 s; `dPm/dt=(Pref-(w-1)/R-Pm)/Tg` |
| Algebra | `Vg=E*exp(j*delta)/(1+Zg*Y)`; `Ig=Y*Vg`; `Pe=real(E*exp(j*delta)*conj(Ig))`. Impedance/admittance stay at nominal-frequency values intentionally. |
| Initialization | w=1, delta=0; compute pre-event Pe0 using Y0; Pm=Pref=Pe0. No separate load or generator injection beyond the equations above. |
| Limits/output | A has no active governor limits. B has Pm in [0,0.35] pu, outward derivative held zero at a bound and inward derivative released immediately; initial Pm unchanged. Store every 0.01 s and event sides; initial maximum step 1 ms, refine for D/E. |

For A the electrical Pe is constant between switching events and independent of
absolute delta. The two states (w-1, Pm-Pe0) obey an affine linear system, providing
an independent matrix-exponential reference. At a constant final load,
`w_eq=1-(Pe-Pref)/(D+1/R)` and `Pm_eq=Pref-(w_eq-1)/R` when no bound is active.
Check this equilibrium analytically rather than equating a finite-duration sample
to it. B exercises state limiting and a power deficit; do not let an implicit
slack source hide the missing mechanical power. Damping is the explicit D term,
not an integrator stabilization option. The global angle is a reference freedom.

Record initialization residuals and no-event drift, terminal voltage/current/P/Q,
Pe/Pm, speed/frequency (f=50*w), delta/reference, governor demand and bound state;
event current steps, frequency minimum, recovery trajectory and final mismatch.
Apply N/D/E. Compare raw w-derived frequency before any vendor meter filter.
Product capture must identify extra governor/AVR/turbine states or frequency-aware
load behavior; those are separate model variants under M. A valid load flow with a
slack is not execution of this dynamic island case.

## Legitimate access routes, observed 2026-10-17

The source ledger is
[power-comparison-access-2026-10-17.yaml](../../sources/entries/power-comparison-access-2026-10-17.yaml).
Access offers below are S documented; successful enrollment, current entitlement,
case entry, output capture and permitted publication for our project remain U.
No named licensed collaborator has been confirmed. Do not reuse a student's or
client's seat for company work without the applicable authorization and terms.

| Product | Documented route and limits | Platform and practical comparison constraint |
| --- | --- | --- |
| PowerWorld | CA1: V24 evaluation/education demo, up to 13 buses; TS, GIC, ATC, OPF/SCOPF/reserves and PV/QV listed. Commercial development/comparison permission must be checked against accepted terms. | Windows 64-bit; page lists Windows 7/Server 2008R2 or newer, not an OS security recommendation. Model/automation/export support for our exact cases U. Viewer is not a replacement solver. |
| ETAP | CA2/CA3: corporate-account 30-day browser or downloadable demo. Online limit 12 AC/10 DC buses and five TCC presentations; saved-project opening/saving and data exchange disabled, report printing restricted to supplied examples. | Browser route avoids local installation; desktop is Windows per dossier. C-01 to C-05/C-07 have relevant advertised demo study modules, but exact custom equations and capture U. CA3 excludes ground grids, motor estimation and UDM. Demo is evaluation/training, not commercial project delivery. |
| PowerFactory | CA4: 28-day evaluation demo, browser streaming offered; excludes DGS/exports and API. Student 50-node/12-month and institutional education/research routes have eligibility/noncommercial restrictions. Demo node count not stated in the inspected text. | Desktop Windows per dossier; streaming browser available. Relevant advanced functions listed, exact model entry and durable output capture U. No assumption that Python scripting means API entitlement in the demo. |
| EasyPower | CA7/CA8: free trial request and personal demonstration; instant online page currently reports all slots occupied. Duration, editable bus count and exact modules for our offered trial U. | Windows desktop per EP2; browser availability is contingent. C-06 requires separate XGSLab access, U. A 30-day purchase refund guarantee is not a 30-day free-trial entitlement. |
| SKM | CA9/CA10: vendor contact route and My SKM licensed downloads. Free/student entitlement, current demo capacity/duration and included modules U from these pages. | PowerTools for Windows; current release requirements must be checked against its installer, not only the old download-page OS list. Existing licensed-contact route possible but none confirmed. |
| NEPLAN | CA5: 15-node NEPLAN 360 Free Student Version; CA6: separate demo/student page advertises 50 nodes for six months, noncommercial cloud use, selected core studies. Confirm the offered route and eligibility instead of conflating them. | CA6 requires an installed NEPLAN App for cloud access; supported client OS not established here. Arc/ground-grid demo entitlement U; no inference from full-product capabilities. |
| PSS/E | CA11: commercial module/package route documented in other-products PS1-PS3. A free/student edition usable for our cases and a current demo limit are U in the sources inspected. | Product is Windows-oriented; exact current install requirements U. Monthly physical-PC/VM restrictions in PS3 apply to that offer, not every license. Industrial protection/arc/grounding case support U. |

All bus counts here are dated page observations, not installed entitlements. None
of these routes establishes that exports are available. Manual screen observations
may be limited by R precision and accepted terms; do not bypass export restrictions.

## Product-output capture checklist

The case-specific output lists apply to every product. Each product/case record
must name one of: not accessed, model mapping blocked, module unavailable, executed
exact model, executed approximation, insufficient output precision or fully compared.
No blank cell means pass. Preserve the distinction between S documented availability
and S observed execution, including timestamp/build and permitted retained evidence.

| Case | Primary requested studies | Minimum output needed for an exact comparison |
| --- | --- | --- |
| C-01/C-02 | Static start slice, dynamic acceleration, event trace | Terminal phasors plus raw speed/torque/current/time, model mapping and step/event metadata |
| C-03 | Linear phase/sequence fault and custom coordination | Complex contributions, side/reference conventions, q/trip/open timeline; standardized method results separated |
| C-04 | Bolted fault, arc method, source-by-source clearing | Effective normative method/inputs, normal/reduced currents and energy increments; otherwise mechanism U |
| C-05 | Harmonic flow and unit-injection frequency scan | Complex phasors, spectrum reference, actual denominator and impedance curve with refinement |
| C-06 | Conduction/grid analysis | Geometry/soil representation, Vg/Rg, defined surface samples, conductor currents and mesh/domain convergence |
| C-07 | RMS dynamic island and explicit governor | Initial states/residuals, raw frequency, Pm/Pe, bound/event trace and matched equations |

## Authored checks and execution status

The source entry records any independent scratch arithmetic performed while
authoring. Those checks validate internal fixture consistency only. Vendor results
for C-01 through C-07 remain U; none has a vendor parity verdict. Before calling
an engine equivalent, complete the exact-model mapping, rights/access and output
precision checks, independent oracle and applicable numerical gate. A source gap,
unsupported model or inaccessible product is an honest unresolved result.

| Authored arithmetic observation | Result and limit |
| --- | --- |
| C-01A direct circuit/acceleration | Initial motor voltage 0.7629974302 pu; torque 0.6052133046 pu; first w=0.8 at 3.9285907030 s by positive-torque quadrature and ODE comparison. At 10 s w=0.9794802674. No product run. |
| C-01B failed-start branch | Initial acceleration -0.2478277897 pu/s with the high-torque load. The case terminates at its initial downward zero-speed boundary; it is not a successful start with a longer time. |
| C-02A authored reactor/bypass | Initial motor voltage 0.5258978875 pu, torque 0.2875180861 pu; final w=0.9829906028 at 10 s. Not a validated starter equipment model. |
| C-03P direct series/relay algebra | F11 bolted three-phase current 1,917.4909005 A. L trip/open at 0.0272977656/0.0872977656 s after fault; H would trip at 0.1550527123 s if still energized and open at 0.2350527123 s. Normally L interrupts before H trips. |
| C-03 fault-boundary sweep | All 16 authored phase-circuit fault solves satisfy their boundary equations within 3.9e-16 pu; SLG also agrees with an independent sequence expression. This is not standardized-fault or transformer-side output validation. |
| C-04 bolted circuit only | Source magnitudes 56,011.2033611 and 36,514.8371670 A; phasor-summed bus magnitude 92,460.9085389 A. Magnitudes do not add arithmetically. No arcing-current/energy result computed. |
| C-05 complex admittance | C=1.57839612984e-5 F/phase; R=63.5085296109 ohm/phase. Independent scalar peak search gives 795.4138974 Hz and 57.8296514 ohm. This is not a completed vendor scan or its grid-refinement check. |
| C-06 field solution | Not performed. Scaling identities are future checks; no ground resistance or safety result asserted. |
| C-07 affine system | Pe0=0.2859740161 pu; pickup Pe=0.4632867373 pu; unconstrained pickup equilibrium f=49.5778268543 Hz. Matrix exponential versus high-accuracy ODE agrees within 1.2e-16 pu in the inspected two-state sample. Limit-case trajectory not independently verified here. |
