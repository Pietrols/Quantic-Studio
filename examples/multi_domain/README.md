# Authored multi-domain project

This project contains two separate power networks and a future PLC model.
The manifest binds every study to its intended model; no first-model default.

Run from the repository root:

```sh
uv run qe study run examples/multi_domain --study plant-flow
uv run qe study run examples/multi_domain --study plant-fault
uv run qe study run examples/multi_domain --study motor-start
uv run qe study run examples/multi_domain --study control-scan
```

The first three exit 0 and write the existing contract-shaped results/report
under out. The last exits 2 with UNSUPPORTED_STUDY and writes no new results.
An earlier result in out is retained, as with other rejected CLI inputs.
Select a study ID explicitly when several studies share a type.

The power inputs are copies of the original authored feeder examples with
new network IDs and paths. The control payload/request are original placeholders,
not IEC 61131-3 programs or executable controller models. Core reports deferred
validation explicitly. Loader and CLI do not rewrite foreign files.

The feeder asset links a power line to a placeholder monitoring-device view.
The power reference is validated; the PLC element reference awaits its domain
contract. This is identity, not electrical equivalence or live coupling.
