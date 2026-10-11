# Motor starting: current, impedance and voltage dip

This calculation is a balanced steady locked-rotor snapshot. It checks the
network voltage while one initially disconnected motor is connected at zero
speed. It does not calculate torque, acceleration time, thermal withstand,
starter transitions or whether the motor can reach running speed.

## Derive the motor impedance

The shaft rating is mechanical output. With P_shaft in kW, rated line-to-line
voltage U_r in kV, efficiency eta and rated power factor pf_r:

    P_electrical [MW] = P_shaft / (1000 eta)
    I_rated [kA] = P_electrical / (sqrt(3) U_r pf_r)
    I_locked = current_ratio * I_rated
    |Z_motor| [ohm per phase] = U_r / (sqrt(3) I_locked)
    Z_motor = |Z_motor| * (pf_locked + j sqrt(1 - pf_locked^2))

Both power factors are lagging. Rated power factor establishes full-load
current; locked-rotor power factor establishes the starting impedance angle.
No typical motor data or universal acceptable dip is assumed.

The adapter represents this impedance by nominal bus-voltage consumption:

    S_nominal [MVA] = U_bus_nominal^2 / conjugate(Z_motor)
    S_actual = S_nominal * |V_bus_pu|^2

A pandapower shunt has exactly this constant-admittance behavior (v3.5.6 shunt
documentation, Electric Model). This retains existing constant-power loads,
line charging, transformers, shunts and generator reactive limits through the
already verified load-flow adapter. The motor and bus voltage bases need not
be equal. Converting on the motor base alone would give incorrect loading
when connected to a bus with a different nominal voltage.

## Independent authored reference

The example uses a 400 V source at 1 pu and a 0.02+j0.03 ohm feeder. Motor inputs
are 30 kW shaft, eta=.9, rated pf=.85, current ratio=6, locked-rotor pf=.3.
These are original educational inputs, not data from a standard or datasheet.
Let Z_l be the feeder and Z_m the motor impedance derived above. With no other
loads, pre-start voltage is the source voltage. Complex voltage division gives:

    V_motor / V_source = Z_m / (Z_l + Z_m)
    dip_percent = 100 * (|V_pre| - |V_start|) / |V_pre|

The tests compute this expression independently, using SI watts and volts,
without calling conversion helpers or reading engine results as references.
They also vary system MVA, motor voltage, source voltage and starting power
factor. Another analytical case adds an existing shunt admittance Y_o:

    V_pre / V_source = 1 / (1 + Z_l Y_o)
    V_start / V_source = 1 / (1 + Z_l (Y_o + 1/Z_m))

This checks that an existing load is retained and that dip uses the pre-start
voltage, not nominal voltage. Numerical tolerances are fixed, not relaxed.

## Read the result

Every bus reports pre-start and locked-rotor voltage magnitude on its own
nominal-voltage base. Dip is signed; a voltage rise gives negative dip.
Equality to the user limit passes. A successful numerical calculation can
fail the selected limit. The CLI returns 1 for either an unavailable calculation
or a failed dip check, while preserving the different states in JSON/report.
Invalid input returns 2 without new outputs; an unavailable engine returns 3.

A failed second solve preserves verified pre-start values but reports unknown
dip and compliance, with bus/field diagnostics. No failed iterate is accepted
as a solution. Provenance hashes the network and full request.

External grids are ideal voltage references. Short-circuit MVA fields do not
become source impedance in this study. Model required upstream impedance as
explicit network branches. The starting motor must not also be counted as an
existing load; the pre-start network represents all other operating equipment.

References: original derivation in motorstart-authored-reference.yaml and
pandapower v3.5.6 shunt mapping in motorstart-pandapower-shunt.yaml.
