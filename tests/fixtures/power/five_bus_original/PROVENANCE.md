# Five-bus original fixture provenance

Original work, Quantic Studio, created 2026-10-08.

## Purpose

A compact 33 kV and 11 kV network with two PV buses, PQ loads, a meshed 33 kV section, line charging, and an off-nominal 33/11 kV transformer. It is a cross-check case and has no stored solution.

## Assumptions

- Balanced, positive-sequence, steady-state, three-phase model.
- System base is 10 MVA. Bus bases are line-to-line RMS and are declared as 33 kV or 11 kV.
- The external grid at bus-1 is the slack at 1.0 pu and 0 degrees. Generators at buses 2 and 4 are PV buses with the active powers and voltage setpoints in `network.json`.
- Two-winding transformer impedance is specified in per unit on its 10 MVA, 33/11 kV rating bases. Its high-side tap ratio is 1.025 and phase shift is zero.
- Each line uses a nominal pi model. `b_us_per_km` is total shunt susceptance per kilometre, split equally between the two terminals by a solver.
- Loads are constant P and Q. Positive load values denote consumption. No line thermal ratings are specified, so loading is unavailable unless an engine supplies a separate rating.
- All topology and numerical values are original, illustrative, and not equipment recommendations. No solved voltages or angles are asserted for this cross-check case.
