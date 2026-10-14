# Auditable calculation traces: showing the working

A study result that only gives final answers asks the reader to trust the
software. An engineering deliverable has to do better: a checking engineer must
be able to take the report, a calculator and the cited book, and arrive at the
same numbers. That is why every Quantic Studio report now shows its working
(decision D11).

## What "showing the working" means

For each result, the report gives three things:

1. **The governing equation**, in symbols, with the book, edition and page it
   comes from. Example: Ik'' = c Un / (sqrt(3) |Z_k|) (Kasikci 2002, section
   11.2, p. 92).
2. **The substitution**: the same equation with the actual input values in it,
   with units. Example: Ik'' = 1.1 * 20 kV / (sqrt(3) * 1.31496 ohm).
3. **The result**: = 9.65935 kA.

If any of the three is missing, the line cannot be checked.

## How the short-circuit trace is built

The IEC 60909 method replaces the network by one voltage source c Un / sqrt(3)
at the fault and the internal impedances of everything else. For a radial
network with one source, the impedance seen from the fault is simply the sum of
the series elements between source and fault:

    Z_k = Z_Q + Z_L + Z_T + ...

Each element has its own formula:

- External grid: Z_Q = c U_nQ^2 / S''_kQ, split into R and X with the given
  R/X ratio: R_Q = Z_Q (R/X) / sqrt(1 + (R/X)^2), X_Q = Z_Q / sqrt(1 + (R/X)^2).
- Line: Z_L = (r' + j x') l.
- Transformer, on its LV side: Z_T = K_T (r + j x) U_rLV^2 / S_rT, where
  K_T = 0.95 c_max / (1 + 0.6 x_T) corrects for the method ignoring the
  pre-fault load and tap position.
- Generator: Z_GK = K_G (R_G + j X''_d) with
  K_G = (U_n / U_rG) c_max / (1 + x''_d sin phi_rG).

An impedance on one side of a transformer appears on the other side scaled by
the square of the rated voltage ratio: Z_B = Z_A (U_rB / U_rA)^2. That is why
the trace has a "referral factor" column. A 20 kV grid impedance seen from a
0.4 kV bus is multiplied by (0.4/20)^2 = 0.0004.

## Why the trace is evidence, not decoration

The adapter does this sum itself, from the input data, and compares it with
pandapower's own network reduction. Only if both agree to one part in a
billion is the current reported. Two independent routes to the same number is
the same idea as a checker redoing a hand calculation. If someone later changes
the engine or the inputs in a way that breaks the agreement, the report shows
"n/a" with a TRACE_MISMATCH diagnostic instead of a wrong number.

## Checking a trace by hand: worked example

From the feeder example, maximum case, bus lv:

- Z_Q = 1.1 * 20^2 / 1000 = 0.44 ohm, R/X = 0.1, so R_Q = 0.04378 ohm, X_Q = 0.43782 ohm.
- Z_L = (0.2 + j0.4) * 2 = 0.4 + j0.8 ohm.
- Z_k = 0.44378 + j1.23782 ohm, |Z_k| = sqrt(0.44378^2 + 1.23782^2) = 1.31496 ohm.
- Ik'' = 1.1 * 20 / (sqrt(3) * 1.31496) = 9.6594 kA.
- R/X = 0.35852, kappa = 1.02 + 0.98 exp(-3 * 0.35852) = 1.35428.
- ip = 1.35428 * sqrt(2) * 9.6594 = 18.500 kA.
- m = [exp(4 * 50 * 1 * ln(0.35428)) - 1] / (2 * 50 * 1 * ln(0.35428)). The
  exponential is about exp(-207.5), effectively zero, so m = 1 / 103.765 = 0.00964.
- Ith = 9.6594 * sqrt(1 + 0.00964) = 9.7058 kA.

Try it with a calculator: every value matches the report.

## Motor start and load flow

The motor-start trace shows the nameplate-to-impedance chain: rated current,
locked-rotor current, |Z_LR| and its angle, R and X, and the equivalent shunt
power S = U^2 / conj(Z). The load-flow report states the Newton-Raphson
equations and adds a power-balance table: at every bus without a source, the
power leaving through branches plus the load must be zero. That closes the
loop from the reported flows back to Kirchhoff's current law.
