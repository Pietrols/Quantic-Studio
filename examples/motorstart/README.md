# Authored motor-start feeder

Original educational 400 V, two-bus feeder with a 30 kW motor initially
disconnected. Nameplate inputs and the 15 percent dip limit are authored user
choices, not standard values or equipment recommendations. The pre-start
network has no loads; its source voltage is 1 pu. The line is 0.02+j0.03 ohm.

Run `uv run qe study run examples/motorstart --study motorstart`.
The command writes `out/results.json` and `out/report.md`, reporting both
voltages and the 15 percent dip limit for every bus. Exit 0 means calculated
and passed; exit 1 means a failed dip limit or unavailable calculation.
The JSON/report distinguish these conditions. Only pandapower supports this study.

For independent numerical verification in WP-1.4, derive motor impedance from
its nameplate, then use V_motor/V_source = Z_motor/(Z_line+Z_motor). This is an
original complex voltage-divider reference, not output copied from an engine.
The external grid is ideal at the source bus; source impedance must be modelled
explicitly as network branches when required.
