# Generator reactive limits in a load flow

A voltage-regulating generator specifies active power P and voltage magnitude
|V|. The load flow solves its angle and the reactive injection Q required to
hold that voltage. This is a PV bus. A converged calculation can demand more Q
than the machine can supply or absorb.

At a reactive limit, Q becomes fixed at Qmin or Qmax. The bus becomes PQ: P and
Q are specified, while voltage magnitude and angle are solved. The setpoint is
now a target that cannot necessarily be met. Increasing a voltage target does
not increase the machine's reactive capability.

For each bus, the governing complex-power equation is

```
S_i = P_i + j Q_i = V_i conjugate(sum_j Y_ij V_j).
```

The adapter passes declared limits to pandapower and enables `enforce_q_lims`
with Newton-Raphson. Pandapower resolves the load flow when it finds a binding
limit. This behavior is documented under
[`enforce_q_lims`](https://pandapower.readthedocs.io/en/stable/powerflow/ac.html).
The result includes a `GENERATOR_Q_LIMIT` warning for each generator at a bound,
with its identifier, bound, actual Q and voltage. Active-power limits remain
unenforced and produce a warning; this WP is not an optimal power flow.
An omitted Q bound uses pandapower's unspecified-bound convention, not a made-up
machine rating. Its internal numerical sentinel is not a certified equipment
capability. Reversed declared bounds are input errors. Equal bounds fix Q.

## An independent two-bus derivation

Use an authored 1 MVA base, 1 kV line-to-line base and a source E=1 pu behind
jX=j0.1 pu. There is no real power or load. The generator-terminal phasor V is
real on the high-voltage solution branch. Current injected toward the source is

```
I = (V - E)/(jX)
S = V conjugate(I) = j V(V - E)/X
Q = V(V - 1)/X
V = [1 + sqrt(1 + 4 X Q)]/2.
```

At a 1.1 pu PV target the required Q is 1.1 Mvar. With Qmax=0.2 Mvar the
PQ solution is 1.0196152423 pu. At a 0.9 pu target the required Q is -0.9 Mvar;
with Qmin=-0.2 Mvar the solution is 0.9795831523 pu. Tests compute these roots
from the equations, not from saved solver outputs. They also check terminal
reactive flow, zero angle and residual. These are original synthetic inputs,
not numbers taken from a standard or manufacturer's data.

## Reading the fourteen-bus result

The committed example retains its feasible 0.9998/0.9693 pu targets. A regression
restores the former 1.010/1.005 pu targets in a temporary file. Both generators
then reach their authored upper bounds, 1.0 and 0.5 Mvar, and both bus voltages
fall below the requested setpoints. Branch power balance independently recovers
each generator's reactive injection. The original example bytes remain intact.

The textbook solver still solves the unconstrained PV equations. Equality
between solvers is meaningful only when neither is constrained, or when Q
bounds are omitted from both comparison inputs. A changed voltage under a
binding limit is a different operating condition, not a numerical tolerance
problem. The reported iteration count describes pandapower's last NR solve,
not the total of the preliminary PV and subsequent constrained solves.
