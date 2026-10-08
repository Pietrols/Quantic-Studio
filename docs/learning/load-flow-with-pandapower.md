# Load flow with pandapower

This note explains how Quantic Studio runs a balanced AC load flow through pandapower, and why the adapter is built the way it is. It is written for an electrical engineer reading `packages/py/qe_power/src/qe_power/adapters/pandapower/solver.py`. The Newton-Raphson method itself is derived in `newton-raphson-load-flow.md`; here the focus is on translating between two descriptions of the same network without losing or bending anything.

## 1. Why an adapter at all

Our network contract (`contracts/power/network.schema.json`, explained in `docs/specs/network.md`) is engine neutral. It speaks the language of a one-line diagram: buses with nominal voltages, lines with ohms per kilometre, transformers with per-unit impedance on their own rating, loads, generators, external grids and shunts.

pandapower speaks its own dialect: line capacitance in nanofarads, transformer short-circuit voltage in percent, tap position and tap step instead of a ratio. The adapter is a dictionary between the two. Its rules are:

1. Every conversion is derived from the definition on the relevant pandapower documentation page (version 3.5.6), and the page is cited next to the code.
2. Anything in the contract that pandapower cannot represent, or that the study does not apply, produces a diagnostic. Nothing is silently dropped.
3. The result is a contract `loadflow-result`, with the same shape as the independent textbook solver, so the two can be compared number by number.

## 2. The per-unit system pandapower uses

pandapower takes one system apparent-power base $S_N$ (`net.sn_mva`, set from our `base_mva`) and uses each bus nominal voltage `vn_kv` as its voltage base. For each voltage level:

$$
Z_N = \frac{V_N^2}{S_N}
$$

This is the same choice as our contract, so bus voltages in per unit and angles in degrees come back unchanged. Only the element parameters need conversion.

## 3. Lines: from susceptance to capacitance

pandapower models a line as a $\pi$ circuit (`elements/line.html`, Electric Model):

$$
\underline{Z} = (r' + jx')\,\ell, \qquad
\underline{Y} = (g' \cdot 10^{-6} + j\,2\pi f\,c' \cdot 10^{-9})\,\ell
$$

where $r'$, $x'$ are in ohm/km, $c'$ in nF/km, $g'$ in $\mu$S/km and $\ell$ in km. The total shunt admittance $\underline{Y}$ is split equally, $\underline{Y}/2$ at each end.

Our contract gives the charging susceptance directly, $b'$ in $\mu$S/km, already evaluated at the study frequency. Setting the two susceptances equal:

$$
b' \cdot 10^{-6} = 2\pi f\,c' \cdot 10^{-9}
\quad\Rightarrow\quad
c' = \frac{b' \cdot 10^{3}}{2\pi f}
$$

pandapower multiplies by $2\pi f$ again internally, so whatever $f$ the network uses cancels out exactly. The conductance $g'$ is set to zero because the contract has no line conductance.

Line loading is $i / i_{max} \cdot 100$ (`elements/line.html`, Result Parameters). If the contract line has no `max_current_ka`, pandapower reports NaN and the adapter returns `loading_pct: null`, which the contract allows.

## 4. Transformers: from per unit to percent

The contract gives $r$ and $x$ in per unit on the transformer rating `sn_mva` and its rated voltages. pandapower wants the short-circuit voltage $v_k$ and its resistive part $v_{kr}$ in percent, on the same rating (`elements/trafo.html`, Impedance Values):

$$
z_k = \frac{v_k\%}{100}, \qquad r_k = \frac{v_{kr}\%}{100}, \qquad x_k = \sqrt{z_k^2 - r_k^2}
$$

A short-circuit test measures exactly this: the voltage, as a fraction of rated, that drives rated current through the shorted transformer is $|z|$. So:

$$
v_{kr}\% = 100\,r, \qquad v_k\% = 100\,\sqrt{r^2 + x^2}
$$

Because pandapower recovers $x_k$ with a square root, it can only represent a positive reactance. The adapter therefore rejects $x \le 0$ with a diagnostic on the `x_pu` field instead of letting a negative reactance flip sign silently.

pandapower refers this impedance to the LV side, $Z_{ref} = V_{n,LV}^2 / S_{rated}$, and rescales it to the system base, $\underline{z} = \underline{z}_k \cdot Z_{ref}/Z_N$. This is the textbook change of base, and it is why we pass the impedance on the transformer rating rather than converting it to `base_mva` ourselves.

### Taps and phase shift

The contract `tap_ratio` multiplies the nominal turns ratio. pandapower describes a ratio tap changer by a position and a step (`elements/trafo.html`, Tap Changer):

$$
n_{tap} = 1 + (\text{tap\_pos} - \text{tap\_neutral}) \cdot \frac{\text{tap\_step\_percent}}{100}
$$

and, with `tap_side="hv"`, multiplies the HV reference voltage by $n_{tap}$. Choosing `tap_neutral = 0`, `tap_pos = 1` and `tap_step_percent = 100(\text{tap\_ratio} - 1)` gives $n_{tap} = \text{tap\_ratio}$ exactly. The tap sits on the HV side and the impedance stays on the LV side, which is the standard branch model with an off-nominal ratio at the from end:

$$
Y_{hh} = \frac{y}{|t|^2}, \quad Y_{hl} = -\frac{y}{t^*}, \quad Y_{lh} = -\frac{y}{t}, \quad Y_{ll} = y
$$

The phase shift enters as a complex ratio, $\underline{t} = t\,e^{j\theta}$ with $\theta$ = `shift_degree` (`elements/trafo.html`, Transformer Ratio). At no load the LV voltage is $V_{HV}/\underline{t}$: magnitude divided by the ratio, angle lagging by $\theta$. The adapter test `test_no_load_transformer_ratio_phase` checks both: with ratio 1.1 and 10 degrees, the LV bus sits at $1/1.1$ pu and $-10$ degrees.

The contract has no magnetizing branch, so `pfe_kw = 0` and `i0_percent = 0`. With no shunt branch the `t` and `pi` equivalent circuits are identical. Each transformer gets an info diagnostic `TRANSFORMER_MODEL` that says so.

## 5. Loads, generators, external grids and shunts

- **Loads.** pandapower uses the consumer system: positive $P$ and $Q$ are consumed (`elements/load.html`). This matches the contract, so values pass straight through. Voltage-dependent load models are switched off, so every load is constant power.
- **Generators** become PV buses: fixed $P$ and a voltage magnitude setpoint (`elements/gen.html`).
- **External grids** are the slack: fixed voltage magnitude and angle (`elements/ext_grid.html`).
- **Shunts.** pandapower gives the shunt power at $v = 1$ pu and treats it as a constant admittance (`elements/shunt.html`):

$$
\underline{y}_{shunt} = \frac{P + jQ}{S_N}, \qquad S_{shunt}(V) = \underline{y}^*_{shunt}\,V^2
$$

This matches the contract wording, "power at nominal bus voltage". A capacitor bank rated at 1 Mvar delivers only 0.81 Mvar at 0.9 pu. Each shunt gets an info diagnostic `SHUNT_MODEL`, so a reader of the result knows which model was used. Note that the WP-0.7 textbook solver injects shunt power as a constant power, so the two solvers differ when a shunt bus is away from 1 pu. None of the current fixtures has a shunt.

## 6. What is reported but not applied

The contract allows some fields that an unconstrained load flow does not use. Each one produces a diagnostic naming the element and field:

| Field | Diagnostic | Why |
| --- | --- | --- |
| bus `vm_pu`, `va_degree` | `REFERENCE_NOT_INITIALIZATION` (info) | Stored values are reference data; the solve uses a flat start |
| generator `p_min_mw`, `p_max_mw`, `q_min_mvar`, `q_max_mvar` | `LIMIT_NOT_ENFORCED` (warning) | Q limits are off (`enforce_q_lims=False`); a generator may need more reactive power than it can give |
| transformer magnetizing branch | `TRANSFORMER_MODEL` (info) | Not in the contract |
| shunt | `SHUNT_MODEL` (info) | States the constant admittance model |

The warning on generator limits matters in practice: if a result shows a PV bus holding its voltage with a reactive output above `q_max_mvar`, the real machine would hit its limit and the bus would become PQ. That study belongs to a later work package.

## 7. Running the solve

The adapter calls `pandapower.runpp` (`powerflow/ac.html`) with:

- `algorithm="nr"`: polar Newton-Raphson, the same method as the textbook solver.
- `init="flat"`: every voltage starts at 1 pu, 0 degrees, apart from slack and PV setpoints.
- `calculate_voltage_angles=True`: so transformer phase shifts are applied.
- `tolerance_mva` and `max_iteration` from the request.
- `check_connectivity=False`: the adapter checks itself, before the solve, that each connected island has exactly one external grid, and reports the network and field when not.

## 8. Convergence and the mismatch

Newton-Raphson drives the power mismatch to zero. At bus $i$:

$$
\Delta S_i = V_i \left(\sum_k Y_{ik} V_k\right)^* - S_i^{spec}
$$

The equations solved are $\Delta P$ at PV and PQ buses and $\Delta Q$ at PQ buses. The adapter recomputes the largest of these from pandapower's final voltages and admittance matrix and reports it, in MVA, as `largest_mismatch_mva`. It does this for converged and non-converged runs alike.

As an independent check, every fixture result goes through `tests/fixtures/power/verify.py`, which rebuilds its own Y-bus from the contract, so it shares no code with pandapower. The mismatch must be below $10^{-8}$ pu, and generation must equal load plus losses. Current fixtures pass at about $10^{-13}$ pu, and agree with the textbook solver to about $10^{-14}$ in voltage.

### A closed-form check

Take one purely resistive line, $r = 0.1$ pu, from a 1 pu slack to a load $P$ at unity power factor. With the receiving voltage $V$ in phase with the source, the current is $(1 - V)/r$ and the load power is

$$
P = V\,\frac{1 - V}{r}
\quad\Rightarrow\quad
V^2 - V + rP = 0
\quad\Rightarrow\quad
V = \frac{1 + \sqrt{1 - 4rP}}{2}
$$

For $P = 0.9$ pu: $V = (1 + 0.8)/2 = 0.9$ pu, the current is 1 pu and the loss is $I^2 r = 0.1$ pu. The test `test_analytical_two_bus` checks exactly these numbers. The repository fixture `two_bus_analytic` does the same with an R+jX line, against `reference.json`.

### When it does not converge

The square root above also shows when there is no solution: when $1 - 4rP < 0$, so $P > 1/(4r) = 2.5$ pu. Beyond that point no voltage can deliver the power, which is the simplest form of voltage collapse, the nose of the P-V curve. Newton-Raphson then wanders or diverges.

pandapower signals this by raising `LoadflowNotConverged`. The adapter catches it and still returns a contract result: `converged: false`, the iteration count, the last mismatch, empty bus and branch tables (a non-converged iterate is not an operating point), and a `NON_CONVERGENCE` error diagnostic that lists the likely causes:

- load beyond the network's transfer limit (voltage collapse);
- slack or generator setpoints that cannot be met together;
- extreme tap ratios;
- very high R/X, or near-zero impedance branches, which make the Jacobian ill conditioned;
- too few iterations for a heavily loaded case.

The code `NON_CONVERGENCE` is the same one the textbook solver uses, so the command line can treat both solvers the same way.

## 9. Using it

```python
from qe_power.adapters.pandapower import run_loadflow_file

request = {"schema_version": "0.1.0", "request_id": "lf", "network_file": "network.json",
           "tolerance_mva": 1e-8, "max_iterations": 20}
result = run_loadflow_file("tests/fixtures/power/five_bus_original/network.json", request)
```

The signature matches `qe_power.textbook.run_loadflow_file`. Provenance records `pandapower`, its version, and the SHA-256 of the exact network file bytes, so two results from the same file can be traced to the same input. If the input cannot be solved at all (unreadable file, schema error, no slack on an island), the function raises `LoadflowInputError`, a `ValueError` that carries the diagnostics, each naming the element and field.
