# Why starting needs its own motor inputs

A motor's shaft rating is not its electrical input. For shaft power P in kW,
efficiency eta, rated line-to-line voltage U in kV and rated power factor pf:

    I_rated [kA] = (P / 1000) / (sqrt(3) U eta pf)
    I_locked [kA] = locked_rotor_current_ratio * I_rated
    |Z_locked| [ohm per phase] = U / (sqrt(3) I_locked)
    R = |Z_locked| * locked_rotor_power_factor
    X = |Z_locked| * sqrt(1 - locked_rotor_power_factor**2)

These follow the balanced three-phase power identity and Ohm's law. The starting
power factor sets the impedance angle; the rated power factor only establishes
rated current. Confusing them changes both the impedance and voltage dip.
A fixed impedance draws less current at a depressed voltage. It is not a fixed
locked-rotor current imposed regardless of terminal voltage.

The request introduces one motor that was disconnected in the pre-start state.
All other loads remain in the network. Do not also model the starting motor as a
pre-existing load. Later shared asset identity can automate this relationship.
The authored example values are educational choices, not typical equipment data,
manufacturer recommendations or values from a standard.

The report compares magnitudes before and during starting on each bus's own
nominal-voltage base. Relative dip is 100*(before-during)/before. Negative dip is
a rise. A computed dip above the selected limit is a successful calculation with
a failed engineering check. A failed voltage solve has unknown compliance,
represented by null plus diagnostics. No universal acceptable dip is assumed.

This contract supports a steady locked-rotor snapshot only. It cannot establish
acceleration time, motor torque margin, thermal withstand or successful run-up.
