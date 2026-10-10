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

The printed voltage table gives maximum `cLV=1.05` at 6% LV tolerance and
`cHV=1.10` above 1 kV. The reference is a hand-derived complex circuit, not
output copied from pandapower. Increasing finite grid strength from `1e4` to
`1e12` MVA makes its impedance approach zero. Tests prove convergence to
the separately derived infinite-source expression, without changing tolerances.

For both maximum and minimum supported feeder duties, the authored example
uses two 20-kV buses and a 2-km line with `.2+j.4 ohm/km`. Its explicit final
conductor temperature is 20 C. Both disputed temperature formulas then give
unit correction, so neither coefficient needs to be chosen. Each case has
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

The machine reference uses `Xd''=xdss Un_machine^2/Sn_machine` and the
documented generator correction at equal machine and bus ratings with explicit
zero voltage-control range. Ik'' can be calculated. A connected synchronous
machine makes the far-from-generator assumption uncertain, so peak and thermal
values are null for every bus in that connected component.

## What is deliberately unavailable

The source review found disagreements or incomplete definitions. The approved
approach preserves supported values and states what cannot be verified:

| Condition | Handling |
| --- | --- |
| LV minimum at 10% tolerance | Printed c=.95, engine c=.90; affected component unavailable |
| Minimum line temperature other than explicit 20 C | Printed .04/K versus engine .004/K; component unavailable |
| Minimum transformer fault | Page omits case restriction, engine uses KT only for maximum; component unavailable |
| Thermal duty at 60 Hz | Engine hardcodes 50 Hz; Ik'' and supported ip remain, Ith unavailable |
| Thermal kappa greater than 1.99 | Engine sets m=0 without the printed equation's basis; Ith unavailable |
| Generator voltage mismatch or nonzero voltage range | Correction definitions disagree or are incomplete; component unavailable |
| Power-station/OLTC correction, duplicate generator bus | Not independently verified; component unavailable |
| Meshed or multiple-source component | Ik'' available; peak/thermal duties await their own reference |
| Exactly 1 kV | Printed table omits equality; affected component unavailable |
| Missing fault nameplate data or source-free island | Null results and named input/bus diagnostics |

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

The first returns maximum/minimum feeder duties. The second is maximum only.
Adding a minimum case to the transformer request demonstrates explicit
unavailability. Changing the feeder request to 60 Hz demonstrates partial
results. Outputs are `out/results.json` and `out/report.md` in the project.

Provenance records pandapower's version, UTC run time and SHA-256 of canonical
network plus request content. Changing duration, frequency, tolerance or case
changes that hash. JSON whitespace or object-key order does not. Requests and
network files are never edited by a study run.

Read the [source register](../sources/entries/pandapower-three-phase-reference.yaml)
for exact pages, installed-source functions and original test inputs. IEC
60909-0 is unavailable; this is a traceable implementation with explicit limits,
not independent standards certification. Resolving the gaps requires verified
source material and numerical tests, not plausible remembered constants.
