# Three-phase fault currents and the limits of a result

A load flow finds an operating point. A fault study replaces normal operation
with a fault and asks how much current the sources can drive through network
impedance. Its grid strength and machine reactance are separate inputs. A
voltage setpoint or a scheduled MW output is not enough.

WP-1.3 uses the balanced, bolted three-phase fault and the positive-sequence
network. This excludes earth faults, fault resistance and unbalanced networks.
Each bus is faulted separately, not simultaneously. Pandapower implements the
equivalent-voltage-source method: the driving voltage at the fault is
`c Un / sqrt(3)`, where Un is line-to-line nominal kV. Normal operating loads
and shunts do not contribute. A motor represented as an ordinary load therefore
has no fault contribution in this model; it needs a separate machine model.

## An independent circuit calculation

For a driving-point Thevenin impedance Z in ohms:

```
Ik'' = c Un / (sqrt(3) |Z|)                       [kA RMS]
|Zgrid| = c_grid Un_grid^2 / Sgrid                [ohms]
Xgrid = |Zgrid| / sqrt(1 + (R/X)^2)
Rgrid = (R/X) Xgrid
```

Maximum and minimum grid MVA and R/X are distinct user inputs. When an upstream
impedance is referred through a nominal transformer, multiply it by the square
of the receiving/sending voltage ratio. Add complex impedances, not magnitudes.

Our authored transformer has a 1-MVA rating and 20/0.4-kV nominal voltages,
with `r=.01` and `x=.05` pu. These are synthetic numbers, not a real nameplate.
Its own LV base is `0.4^2/1=.16 ohm`. For the supported maximum case:

```
KT = .95 cmax_LV / (1 + .6 xT)
ZT = KT (r + jx) Un_LV^2 / Sn_transformer
Zseen_LV = ZT + Zgrid_HV (Un_LV/Un_HV)^2
Ik''_LV = cLV Un_LV / (sqrt(3) |Zseen_LV|)
```

Kasikci Table 1.1 (p. 8) gives maximum `cLV=1.05` at 6% LV tolerance and
`cHV=1.10` above 1 kV. The reference is a hand-derived complex circuit, not
output copied from pandapower. Increasing finite grid strength from `1e4` to
`1e12` MVA makes its impedance approach zero. Tests prove convergence to
the separately derived infinite-source expression, without changing tolerances.

For both maximum and minimum feeder duties, the authored example uses two
20-kV buses and a 2-km line with `.2+j.4 ohm/km`. Its explicit final conductor
temperature is 20 C, so the minimum-case resistance factor is 1. Each case has
its own source impedance and voltage factor, 1.10 maximum and 1.00 minimum.

## Peak force and thermal heating are different duties

Initial symmetrical current is RMS. Peak current is instantaneous and is used
when considering electromagnetic forces. For the independently verified radial,
single-source, far-from-synchronous-generator case:

```
kappa = 1.02 + .98 exp(-3 R/X)
ip = sqrt(2) kappa Ik''                           [kA peak]
a = ln(kappa - 1)
m = expm1(4 f T a) / (2 f T a)
n = 1
Ith = Ik'' sqrt(m+n)                              [kA RMS]
```

Here R/X is the driving-point impedance ratio, f is Hz and T is the requested
fault duration in seconds. Ith gives an equivalent heating duty for that
duration; `Ith^2 T` describes its squared-current integral. The program does not
infer a breaker clearing time or claim that equipment passes a rating check.

The machine reference uses `Xd''=xdss Un_machine^2/Sn_machine` and
`K_G = (Un/UrG) cmax / (1 + xd'' sin phi)` (Kasikci eq. 9.3 p. 76) with explicit
zero voltage-control range. Ik'' can be calculated. A connected synchronous
machine makes the far-from-generator assumption uncertain, so peak and thermal
values are null for every bus in that connected component.

## How the earlier gaps were settled (WP-1.12)

When Phase 1 was built, several values were withheld because pandapower's
documentation and code disagreed and no owned book was available. Peter's
reference library now includes Kasikci, *Short Circuits in Power Systems*,
1st ed (Wiley-VCH, 2002), and Das, *Power System Analysis* (2002). Each gap
was settled from those books or by an explicit engineering decision:

| Condition | Now | Source |
| --- | --- | --- |
| LV minimum voltage factor at +10% tolerance | c_min = 0.95 for both LV classes | Kasikci Table 1.1 p. 8; Peter's decision D10 |
| Minimum transformer fault | Available with K_T = 1 | Kasikci ch. 9 p. 75 (corrections serve the greatest current); pandapower cites IEC 60909-0:2016 cl. 6.3.3 |
| Line end temperature other than 20 C | R = R_20 (1 + 0.004 (theta_e - 20)) | Kasikci p. 12 (factor 1.24 for 20 to 80 C) |
| Thermal duty at 60 Hz | m evaluated at the requested f | Kasikci eq. 13.2 p. 117 |
| Thermal duty for kappa above 1.99 | m from the equation, limit m = 2 at kappa = 2 | Kasikci eq. 13.2 p. 117 and Fig. 13.3a p. 118 |
| Generator with machine kV different from bus kV | K_G = (U_n/U_rG) c_max / (1 + x''_d sin phi_rG) | Kasikci eq. 9.3 p. 76; Das eq. 8.11 |
| Peak and thermal duty in meshed or multi-grid networks, with or without transformers | Method C, checked by our own nodal solve (WP-1.14) | Kasikci p. 99 |
| Exactly 1 kV | LV factors (WP-1.14) | Decision D12: LV up to and including 1 kV, MV to 33 kV, HV above; the adapter supplies the factors to the engine |
| Nonzero generator voltage range, power-station/OLTC units, near-generator duties | Still unavailable | No owned source verifies them yet |

Three of these deserve a closer look.

**Why c_min is a decision, not a lookup.** The c factor scales the pre-fault
voltage. c_min gives the smallest fault current, which is what protection must
still detect. Kasikci follows the 1997 draft of the 2001 standard and uses 0.95
for all LV networks. The 2016 standard (as reported by its software vendors)
uses 0.90 for the +10% class. Peter chose 0.95 (D10). For a +10% network this
gives a minimum current about 5.6% higher than 0.90 would, so it should be
revisited when the 2016 or 2026 text is owned.

**Why m tends to 2, not 0.** The DC offset of a fault current decays with the
time constant L/R. The factor m is the extra heating it adds over the fault
duration Tk:

```
a = ln(kappa - 1)
m = [exp(4 f Tk a) - 1] / (2 f Tk a)
```

As R/X falls to zero, kappa rises to 2 and a falls to 0. The fraction becomes
0/0. Using exp(x) - 1 = x for small x, it approaches 4 f Tk a / (2 f Tk a) = 2.
Physically, a DC offset that never decays adds heat for the whole fault.
pandapower's shortcut sets m = 0 above kappa 1.99, which under-states Ith by up
to about 42% in the limit. The adapter now evaluates the equation itself.

**Method C for meshed networks.** In a mesh, parallel paths have different R/X,
so the fault impedance's own R/X does not describe the decay of the DC offset.
Method C reduces the network again with all reactances scaled to an equivalent
frequency fc (20 Hz in a 50 Hz system), then uses R/X = (R_c / X_c)(fc / f).
The adapter performs that reduction itself, Z_bus = Y_bus^-1 at f and at fc,
and only reports ip and Ith when its answer agrees with the engine.

A transformer enters that nodal solve as an ideal transformer with its series
impedance on the LV side. In per unit on each bus's nominal voltage, its
off-nominal ratio is t = (U_rHV / U_rLV)(U_nLV / U_nHV), and it adds y / t^2 at the
HV bus, y at the LV bus and -y / t between them. For a single path this gives
exactly the referral by the squared rated ratio used in the radial sum, so the
two methods agree where both apply.

**Voltage levels.** Peter's decision D12: LV up to and including 1 kV, MV above
1 kV up to 33 kV, HV above 33 kV. pandapower's own table stops LV just below
1 kV and uses c_min 0.90 for +10% networks, so the adapter hands the engine our
factor table (one function, build_bus._add_c_to_ppc) and still checks the
applied factor at every bus.

Every unavailable result identifies its bus and exact field. Each requested case
includes every input bus, preserving input order. Healthy separate components
continue even if another cannot be solved. A failure is never converted to a
zero fault current or hidden behind a successful operating-point calculation.

`success` means every duty is available, `partial` means some are available,
and `failed` means none are available. The CLI writes reports for all three,
returning 0 only for success and 1 for partial/failed. Malformed inputs return
2 and produce no new output. An unavailable solver returns 3.

## Run and inspect

```
uv run qe study run examples/shortcircuit --study shortcircuit
uv run qe study run examples/shortcircuit/transformer --study shortcircuit
```

The first returns maximum and minimum feeder duties. The second is maximum
only; adding "min" to its cases shows the K_T = 1 minimum. Adding a
synchronous generator demonstrates partial results (near-generator duties are
withheld). Outputs are `out/results.json` and `out/report.md`, and each report
shows a worked calculation for every bus (WP-1.11).

Provenance records pandapower's version, UTC run time and SHA-256 of canonical
network plus request content. Changing duration, frequency, tolerance or case
changes that hash. JSON whitespace or object-key order does not. Requests and
network files are never edited by a study run.

Read the [source register](../sources/entries/pandapower-three-phase-reference.yaml)
and [Kasikci entry](../sources/entries/kasikci-2002-short-circuits.yaml) for
exact pages, installed-source functions and original test inputs. IEC 60909-0
itself is not owned; this is a traceable implementation with explicit limits,
not independent standards certification. Remaining gaps need verified source
material and numerical tests, not plausible remembered constants.
