# Authored three-phase fault examples

These synthetic inputs are independent test networks, not real equipment data.

```
uv run qe study run examples/shortcircuit --study shortcircuit
uv run qe study run examples/shortcircuit/transformer --study shortcircuit
```

The default is a 20-kV source and 2-km feeder, with explicit final conductor
temperature 20 C. It returns maximum and minimum Ik'', ip and Ith at both buses.
The transformer subproject is the original 20/0.4-kV, 1-MVA reference and requests
maximum faults only. Both use 50 Hz and 6% LV tolerance.

The original transformer request included minimum faults. Independent tests
found that the public correction page omits a case distinction present in the
pinned implementation, which applies KT only for maximum. Minimum transformer
duties are now explicitly unavailable rather than silently picking a basis.
Changing the transformer request to include minimum will produce a partial
report and exit 1. See the learning note and source register for all limitations.

Successful studies exit 0. Partial or failed but schema-valid studies exit 1,
with results and report written. Invalid documents exit 2 without new outputs.
Generated out/ folders are ignored by git.

Reference equations and provenance: [three-phase fault learning note](../../docs/learning/three-phase-short-circuit.md).
