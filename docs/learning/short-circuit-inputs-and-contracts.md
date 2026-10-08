# Inputs that define a fault study

A load flow asks which voltage and current satisfy specified generation and
loads. A fault calculation asks how the network's internal impedances limit a
fault. A grid's load-flow voltage setpoint does not tell us its fault strength.

For a three-phase source with rated line-to-line voltage Un, short-circuit level
Sk and voltage factor c, the equivalent impedance magnitude is

```
|Zq| = c Un^2 / Sk
Xq = |Zq| / sqrt(1 + (R/X)^2)
Rq = (R/X) Xq
```

Use kV and MVA to obtain ohms. These relations follow from
`Sk = sqrt(3) Un Ik` and `Ik = c Un / (sqrt(3) |Zq|)`.
See pandapower's [voltage-source model](https://pandapower.readthedocs.io/en/stable/shortcircuit/voltage_source.html).
Maximum and minimum grid strengths and their R/X ratios are separate input
conditions. Neither can safely be inferred from the load-flow dispatch.

A machine's subtransient reactance is a per-unit number on the machine's own
rating: `Xd''[ohm] = xdss_pu * Un_generator^2 / Sn_generator`. Changing bases
requires `x_new = x_old * S_new/S_old * (U_old/U_new)^2`. Rated power factor
and voltage range support documented correction factors; missing nameplate
values remain missing. A power-station transformer needs explicit association.

Transformer R and X already use the transformer's own rating. Balanced
three-phase faults use positive sequence; vector group and zero-sequence data
are needed for other fault types, which this contract does not accept.

Fault duration determines thermal duty. Peak current describes an instantaneous
force-producing maximum, while Ik'' and Ith are RMS quantities. A null duty
means unavailable and carries a diagnostic. It does not mean a safe zero-duty
bus. A result can have usable Ik'' while peak and thermal duties remain unknown.
The result status makes this distinction visible to reports and callers.

The versioned contract keeps load-flow projects readable and makes fault inputs
optional on networks. The study then checks whether its particular inputs are
complete. Load flow reports fault-only fields as informational, without using
them as operating controls. Numerical reference calculations belong to WP-1.3;
CC-1's example values are original synthetic equipment inputs, not measured
ratings or copied standard tables.
