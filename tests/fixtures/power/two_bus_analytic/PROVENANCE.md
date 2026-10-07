# Two-bus analytic fixture provenance

Original work, Quantic Studio, created 2026-10-08.

## Purpose

A two-bus constant-power case with a closed-form high-voltage solution. It is the independent reference for the solver tests. The values are original illustrative data, not taken from an external network or equipment schedule.

## Assumptions

- Balanced, positive-sequence, steady-state, three-phase system.
- System base is 10 MVA. Both bus voltage bases are 11 kV line-to-line RMS.
- Slack voltage is 1.0 pu at 0 degrees.
- The line has a total series impedance of 0.363+j0.726 ohm over 1 km. On this base, its impedance is 0.03+j0.06 pu because Zbase=(11 kV)^2/(10 MVA)=12.1 ohm.
- The receiving bus is a constant PQ load of 2 MW+j1 Mvar, or 0.2+j0.1 pu.
- Line charging, shunts, transformer, and generator are absent.
- Positive P and Q values on a load denote consumption. Positive branch flow is from `from_bus` toward `to_bus`.
- The high-voltage root is used. The second root is the low-voltage branch of the same algebraic equation and is not the normal operating solution.

## Closed-form receiving-end voltage

Set the slack phasor to E=1 pu, the line impedance to Z=R+jX, the receiving voltage to V, and the consuming load to S=P+jQ. The load current is I=conj(S/V)=(P-jQ)/conj(V). The series-line equation is:

```text
E = V + Z(P-jQ)/conj(V)
```

Multiply by conj(V), and define A=RP+XQ and B=XP-RQ:

```text
E*conj(V) = |V|^2 + Z(P-jQ)
E*Vr = u + A
-E*Vi = B
u = Vr^2 + Vi^2
```

Eliminating Vr and Vi gives the quadratic:

```text
u^2 + (2A-E^2)u + (A^2+B^2) = 0
```

The high-voltage solution is:

```text
u = (E^2 - 2A + sqrt((E^2 - 2A)^2 - 4(A^2+B^2))) / 2
Vr = (u + A) / E
Vi = -B / E
V = Vr + jVi
```

For the declared inputs, A=0.012 pu, B=0.009 pu, and the discriminant is 0.951676 pu squared. The resulting reference is `vm_pu=0.987810413356306` and `va_degree=-0.522032510710008`. These values are calculated from the equations above, not copied from a source.
