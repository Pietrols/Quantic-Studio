# Fourteen-bus original example

An original Quantic Studio network (11 kV and 33 kV, with an off-nominal transformer tap, line charging and a mix of PV and PQ buses). It has no published solution; it is a cross-check case for the two load-flow solvers.

Run it:

```
uv run qe study run examples/fourteen_bus --study loadflow --solver textbook
uv run qe study run examples/fourteen_bus --study loadflow --solver pandapower
```

Each run writes `out/results.json` and `out/report.md` in this folder (`out/` is git-ignored).

`network.json` is a copy of `tests/fixtures/power/fourteen_bus_original/network.json`. A test in `packages/py/qe_cli/tests` fails if the two ever differ, so the fixture stays the single source of truth.

The request settings (0.0001 MVA tolerance, 20 iterations, flat start) are study choices for this example, not values from a standard.
