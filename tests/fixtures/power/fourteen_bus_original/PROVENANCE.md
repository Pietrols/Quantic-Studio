# Fourteen-bus original fixture provenance

Original work, Quantic Studio, created 2026-10-08.

## Purpose

A fully authored, 14-bus cross-check network with 33 kV and 11 kV sections, two PV buses, PQ loads, line charging, a meshed topology, and an off-nominal transformer. It has no stored solution and is intended for solver-to-solver comparison.

## Assumptions

- Balanced, positive-sequence, steady-state, three-phase model.
- System base is 10 MVA. Bus voltage bases are line-to-line RMS and are explicitly 33 kV or 11 kV.
- Bus-01 is the slack at 1.0 pu and 0 degrees. Bus-02 and bus-08 are PV generator buses with the active powers and voltage setpoints in `network.json`. All other buses are PQ.
- All line impedances, charging susceptances, loads, generator outputs, and transformer parameters were authored for this fixture. They are synthetic and are not copied from an operating network, standard, or publication.
- Lines use nominal pi charging, with the declared total susceptance split equally between their ends by a solver.
- The 33/11 kV transformer is represented with per-unit impedance on its declared 10 MVA rating base, a 1.025 high-side tap ratio, and zero phase shift.
- Loads are constant P and Q. Positive values denote consumption. Shunts are absent. No line thermal ratings are supplied.
- Cross-check solvers should compute their own results. No solved bus values, flows, or losses are stored as reference answers.
