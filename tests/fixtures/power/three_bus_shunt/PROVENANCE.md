# Three-bus shunt fixture provenance

Original work, Quantic Studio, created 2026-10-08.

## Purpose

The `three_bus_original` network plus one capacitor shunt at the PQ load bus. It exists so that the textbook Newton-Raphson solver and the pandapower adapter are compared on a case where the shunt model matters.

## Assumptions

- Identical to `three_bus_original` in every bus, line, load, generator and external grid value. Only `network_id` and `shunts` differ.
- Shunt `capacitor-3` at `bus-3` has `p_mw` 0.0 and `q_mvar` -0.4. Per `docs/specs/network.md`, shunt values are power at nominal bus voltage with positive values denoting consumption, so this is a capacitor that supplies 0.4 Mvar at 1.0 pu and `0.4 * |V|^2` Mvar in general (a constant admittance).
- Balanced, positive-sequence, steady-state, three-phase model.
- The shunt value is invented for this test fixture and is not an equipment recommendation.
