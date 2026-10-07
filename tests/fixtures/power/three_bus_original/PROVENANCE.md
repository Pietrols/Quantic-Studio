# Three-bus original fixture provenance

Original work, Quantic Studio, created 2026-10-08.

## Purpose

A small meshed network with a slack bus, one PV generator bus, and one PQ load bus. WP-0.7 uses it to exercise the Newton-Raphson mismatch and state update at every iteration.

## Assumptions

- Balanced, positive-sequence, steady-state, three-phase model.
- System and bus voltage bases are 10 MVA and 11 kV line-to-line RMS.
- The slack setpoint is 1.0 pu at 0 degrees. The PV setpoint is 1.01 pu with fixed active generation of 0.8 MW. The PQ load consumes 1.4 MW+j0.6 Mvar.
- The three lines form a closed triangle. Their series impedances are defined by the original per-kilometre values and lengths in `network.json`.
- Line charging, shunts, and transformers are absent to keep iteration diagnostics focused on the nonlinear power balance.
- All impedances, dispatch values, and setpoints are invented for this test fixture and are not equipment recommendations.
