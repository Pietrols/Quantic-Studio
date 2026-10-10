# Authored motor-start feeder

Original educational 400 V, two-bus feeder with a 30 kW motor initially
disconnected. Nameplate inputs and the 15 percent dip limit are authored user
choices, not standard values or equipment recommendations. The pre-start
network has no loads; its source voltage is 1 pu. The line is 0.02+j0.03 ohm.

CC-2 defines and validates this project. WP-1.4 implements its solver, CLI and
report; until then `qe study run` does not support this study type.

For independent numerical verification in WP-1.4, derive motor impedance from
its nameplate, then use V_motor/V_source = Z_motor/(Z_line+Z_motor). This is an
original complex voltage-divider reference, not output copied from an engine.
The external grid is ideal at the source bus; source impedance must be modelled
explicitly as network branches when required.
