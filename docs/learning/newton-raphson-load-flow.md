# Newton-Raphson load flow in polar form

This note derives the balanced steady-state load-flow equations used by the textbook solver. It is written for an electrical engineer reading the implementation in `packages/py/qe_power/src/qe_power/textbook/solver.py`. The derivations start from complex voltage, current, and power relationships. No solver-specific adapter defines the equations.

## 1. Choose consistent per-unit bases

For a three-phase system, choose a three-phase apparent-power base $S_{base}$ and line-to-line RMS voltage base $V_{LL,base}$. The current and impedance bases are:

$$
I_{base} = \frac{S_{base}}{\sqrt{3}V_{LL,base}}, \qquad
Z_{base} = \frac{V_{LL,base}^2}{S_{base}}
$$

The voltage and impedance conversions are:

$$
V_{pu} = \frac{V_{LL}}{V_{LL,base}}, \qquad
Z_{pu} = \frac{Z_{ohm}}{Z_{base}}
$$

With MVA and kV units, these equations produce current in kA and impedance in ohms. The network declares one system `base_mva`; each bus supplies its line-to-line `vn_kv` voltage base.

## 2. Build the bus admittance matrix

For a series branch with impedance $z=r+jx$, its series admittance is:

$$
y = \frac{1}{z}
$$

A line with per-kilometre impedance and length $\ell$ first forms:

$$
z_{pu} = \frac{(r_{ohm/km}+jx_{ohm/km})\ell}{Z_{base}}
$$

For total line charging susceptance $b$, the nominal-pi model puts half at each terminal. Its Y-bus contributions are:

$$
Y_{ff} \mathrel{+}= y + j\frac{b_{pu}}{2}, \quad
Y_{tt} \mathrel{+}= y + j\frac{b_{pu}}{2}, \quad
Y_{ft} \mathrel{-}= y, \quad
Y_{tf} \mathrel{-}= y
$$

For a two-winding transformer whose complex tap $a=\tau e^{j\phi}$ is on the high-voltage side, the series-branch stamp is:

$$
Y_{ff} \mathrel{+}= \frac{y}{|a|^2}, \quad
Y_{ft} \mathrel{-}= \frac{y}{a^*}, \quad
Y_{tf} \mathrel{-}= \frac{y}{a}, \quad
Y_{tt} \mathrel{+}= y
$$

Transformer per-unit impedance must be converted to the system MVA base. When the bus voltage bases equal the transformer nominal voltages, only the MVA base changes:

$$
z_{pu,system} = z_{pu,rated}\frac{S_{base,system}}{S_{rated}}
$$

## 3. Calculate bus power from voltage

Write bus voltage in polar form as $V_i=|V_i|e^{j\theta_i}$. Complex current and injected complex power are:

$$
I_i = \sum_k Y_{ik}V_k, \qquad S_i=P_i+jQ_i=V_i I_i^*
$$

Expanding the product gives:

$$
P_i = \sum_k |V_i||V_k|\left(G_{ik}\cos\theta_{ik}+B_{ik}\sin\theta_{ik}\right)
$$

$$
Q_i = \sum_k |V_i||V_k|\left(G_{ik}\sin\theta_{ik}-B_{ik}\cos\theta_{ik}\right)
$$

where $\theta_{ik}=\theta_i-\theta_k$ and $Y_{ik}=G_{ik}+jB_{ik}$. The implementation evaluates these equations through complex matrix multiplication, then separates the real and imaginary parts.

## 4. Form the mismatch vector

For a bus with specified active and reactive injection, define mismatch as specified minus calculated power:

$$
\Delta P_i=P_{i,spec}-P_{i,calc}, \qquad
\Delta Q_i=Q_{i,spec}-Q_{i,calc}
$$

The slack bus has fixed magnitude and angle, so neither mismatch is an equation in the Newton system. A PV bus has fixed active power and voltage magnitude, so only $\Delta P_i$ is included. A PQ bus has fixed active and reactive power, so both $\Delta P_i$ and $\Delta Q_i$ are included.

The unknown state is ordered as all non-slack voltage angles followed by PQ voltage magnitudes:

$$
x=[\theta_{non-slack}, |V|_{PQ}]^T
$$

## 5. Construct the explicit Jacobian

The Newton Jacobian is partitioned by mismatch and state type:

$$
J=\begin{bmatrix}
H & N \\
M & L
\end{bmatrix}
=\begin{bmatrix}
\partial P/\partial\theta & \partial P/\partial|V| \\
\partial Q/\partial\theta & \partial Q/\partial|V|
\end{bmatrix}
$$

For $i\ne k$, the off-diagonal entries are:

$$
H_{ik}=|V_i||V_k|(G_{ik}\sin\theta_{ik}-B_{ik}\cos\theta_{ik})
$$

$$
N_{ik}=|V_i|(G_{ik}\cos\theta_{ik}+B_{ik}\sin\theta_{ik})
$$

$$
M_{ik}=-|V_i||V_k|(G_{ik}\cos\theta_{ik}+B_{ik}\sin\theta_{ik})
$$

$$
L_{ik}=|V_i|(G_{ik}\sin\theta_{ik}-B_{ik}\cos\theta_{ik})
$$

The diagonal entries are:

$$
H_{ii}=-Q_i-B_{ii}|V_i|^2, \quad
N_{ii}=\frac{P_i}{|V_i|}+G_{ii}|V_i|
$$

$$
M_{ii}=P_i-G_{ii}|V_i|^2, \quad
L_{ii}=\frac{Q_i}{|V_i|}-B_{ii}|V_i|
$$

Rows and columns are selected according to the bus types: P rows for PV and PQ buses, Q rows for PQ buses, angle columns for non-slack buses, and voltage-magnitude columns for PQ buses.

## 6. Update the state and test convergence

At iteration $k$, solve the linearized mismatch equation:

$$
J(x_k)\Delta x_k=\begin{bmatrix}\Delta P\\\Delta Q\end{bmatrix}
$$

Then apply the angle and magnitude corrections:

$$
\theta_{k+1}=\theta_k+\Delta\theta_k, \qquad
|V|_{k+1}=|V|_k+\Delta|V|_k
$$

The slack voltage remains fixed, PV magnitudes remain at their setpoints, and only PQ magnitudes are updated. Convergence is declared when the largest absolute component of the constrained P and Q mismatch is below the caller-supplied tolerance converted from MVA to pu. The result diagnostic stores the mismatch magnitude from the initial state and after every update, so a reader can see the convergence path instead of only its final value.

## 7. Calculate branch flows and losses

For a line, the terminal current includes series current and half of line charging at that end:

$$
I_f=y(V_f-V_t)+j\frac{b_{pu}}{2}V_f, \qquad
I_t=y(V_t-V_f)+j\frac{b_{pu}}{2}V_t
$$

For a transformer, terminal currents use the same off-nominal tap stamp used in Y-bus. At either terminal, complex power flowing into the branch is:

$$
S_{terminal}=V_{terminal}I_{terminal}^*S_{base}
$$

The branch active and reactive losses are the sums of the two terminal powers. A line loading is reported only when a current rating exists. Transformer loading uses its declared MVA rating.

## 8. How the tests use the original fixtures

`two_bus_analytic` is checked against the independent quadratic derivation in its fixture provenance and provides a voltage magnitude and angle reference. `three_bus_original` checks the complete per-iteration mismatch history on a meshed PV/PQ network. `five_bus_original` and `fourteen_bus_original` have no expected-answer files; they exercise line charging and off-nominal transformer taps as cross-check cases. The shared fixture verifier independently recomputes Y-bus bus mismatch and active losses from the returned voltages.
