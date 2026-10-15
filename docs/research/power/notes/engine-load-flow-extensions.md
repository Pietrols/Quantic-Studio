# Engine spec note: load flow extensions, unbalanced and distribution load flow (WP-2.10)

This note covers matrix rows:

- S2: Gauss-Seidel and fast decoupled;
- S4: LTC and regulator control;
- S5: phase shifters;
- S7: load models (see `engine-motors.md`);
- S9: islands;
- S10: unbalanced three-phase load flow;
- S12: DC load flow;
- S20: capacitor placement.

Quantic today has balanced Newton-Raphson with Q limits through pandapower (S1, S3).

Paraphrased from owned references.

## 1. Sources

| Key | Source | Where |
| --- | --- | --- |
| Das02 | J. C. Das, *Power System Analysis*, 2002 | ch. 11 (two-winding transformer model with taps, bus types, Gauss-Seidel), ch. 12 (NR rectangular and polar, decoupled, fast decoupled, phase-shifting transformer sec. 12.8, DC models 12.9, load models 12.10, practical studies 12.12), ch. 13 (reactive power control, FACTS), ch. 14 (three-phase and distribution load flow, pdf pp. 493 to 515) |
| Glover17 | Glover, Overbye, Sarma, 6th ed., 2017 | ch. 6 power flows (Gauss-Seidel, NR, fast decoupled, control of power flow) |
| pp3ph | pandapower docs, "Asymmetric / Three Phase Power Flow" | https://pandapower.readthedocs.io/en/latest/powerflow/ac_3ph.html (read 2026-10-15) |
| Kersting | W. H. Kersting, *Distribution System Modeling and Analysis*: **not owned**. It is the reference for four-wire line models, regulators and distribution transformer connections. Still a gap |

## 2. Balanced extensions (Das02 ch. 11 to 13)

- **Solvers:** Gauss-Seidel (Y and Z matrix forms), NR (rectangular and polar), decoupled
  and fast decoupled. pandapower `runpp` provides nr, iwamoto_nr, bfsw (backward-forward sweep), gs, fdbx and fdxb (algorithm names as used in the pandapower runpp API; to confirm against the current docs). Quantic
  exposes the choice and reports iterations and mismatch history in the trace.
- **Transformer tap model** (Das02 ch. 11): an off-nominal ratio π-equivalent.
- **LTC control** (S4): a voltage band, local or remote regulated bus, step size and tap
  limits, and an outer loop around the load flow. pandapower has controller classes
  (DiscreteTapControl, ContinuousTapControl). Use them, and add band, deadband and time
  delay for quasi-dynamic studies.
- **Phase-shifting transformers** (S5; Das02 sec. 12.8): a complex ratio, with active
  power control by angle as an outer loop.
- **Islands** (S9): detect islands from topology, require a slack (or distributed slack)
  per energised island, and report de-energised buses. pandapower handles multiple
  ext_grids and islands; verify that its behaviour with no slack in an island is a
  diagnostic, not a silent drop.
- **Reactive compensation** (Das02 ch. 13): switched shunts, SVC and STATCOM as voltage
  controllers with limits.

## 3. Unbalanced three-phase load flow (S10)

**Phase-coordinate method** (Das02 sec. 14.1, pdf pp. 494 to 496):

- Each bus has three nodes; each branch has a 3×3 (or 4×4 with neutral) admittance block.
- Solve Y·V = I with Gauss or NR.
- This keeps untransposed lines, single-phase laterals and mutual coupling exact,
  which the sequence method cannot when the system is coupled after transformation.
- The same Y supports series faults (open conductor by Y modification) and multiple
  simultaneous faults by superposition.
- **This closes matrix F8 (open conductor, simultaneous faults) for the phase-frame
  engine.**

**Distribution load flow** (Das02 sec. 14.3, pdf pp. 506 to 511):

- Distribution systems are inherently unbalanced, with low X/R, so NR cannot be
  decoupled. A Gauss method with a factored Y and a single swing bus converges
  comparably (p. 508).
- **Ladder or backward-forward sweep for radial feeders** (eqs 14.46 to 14.49):
  - load currents from S/V;
  - sweep voltages from the end node up to the source;
  - rescale and repeat;
  - laterals handled as sub-ladders with a voltage-mismatch correction at the junction
    (p. 511).
- **Short circuit uses load-flow prefault voltages and currents**, because load currents
  are not negligible in distribution (p. 507). That is the "complete method" (F6).

**Open-source options:**

- **pandapower `runpp_3ph`** (docs read 2026-10-15):
  - sequence frame, with NR on the positive sequence and current injection for zero and
    negative sequence;
  - successful only with earthed transformers (Dyn, Yyn, YNyn, Yzn);
  - T-model only;
  - many options marked "not tested";
  - no quantitative validation published.

  So it is suitable for simple LV unbalance, **not** as the main S10 engine.
- **OpenDSS** (BSD-3 through DSS-Python): a true multiphase phase-coordinate engine with
  regulators, any transformer connection, single-phase laterals, and time series. It is
  the natural S10 base, as already noted for harmonics (`engine-harmonics.md`).

**Verification:** the IEEE distribution test feeders (13, 34, 37 and 123 node) are public
with published results. They are the standard check for S10, and the reason Kersting's
book matters.

## 4. DC load flow (S12)

There are two meanings, and both are needed:

1. **DC approximation of AC flow** (Das02 sec. 12.9): linear P-θ, used for contingency
   screening and PTDFs (S15, S16). pandapower has `rundcpp`.
2. **DC networks** (battery, charger, DC loads, traction): resistive network solve with
   constant-power loads (Newton on V). It shares its network model with the DC
   short-circuit engine (`engine-dc-short-circuit.md`). No library is chosen yet; it is a
   simple engine to build.

## 5. Optimal capacitor placement (S20; Das02 sec. 14.3.3)

The objective weighs peak and energy loss reduction against capacitor cost:

- the loss reduction per segment is 3·Rk·(2·ILk·ICk − ICk²) (eq. 14.50);
- the average-load form uses the load factor LF (eq. 14.51);
- the objective sums these with monetary conversion factors (eq. 14.52), solved by
  dynamic programming in the book.

A modern approach is mixed-integer optimisation over standard bank sizes. This feature
is valuable for mine distribution systems with poor power factor (penalty tariffs).

## 6. Gaps

1. Kersting's *Distribution System Modeling and Analysis* (four-wire lines, Carson's
   equations with neutral, regulator models, open-delta and open-wye transformers).
   Grainger94 ch. 4 to 6 and Das02 App. B cover line constants (Carson) partly. Suggest
   buying Kersting.
2. IEEE test feeder data: public, to download from the IEEE PES site (not into this
   repo if the licence forbids redistribution; check).
3. OpenDSS licence details and the DSS-Python API: in `open-source-foundations.md`;
   confirm the KLUSolve LGPL handling (separate shared library).
