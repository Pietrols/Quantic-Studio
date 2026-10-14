# PV inputs, power and energy

Peter, a PV calculation is a chain of questions: where is the sun, how much
irradiance reaches the tilted surface, how hot are the cells, what DC power do
they produce, and how much AC leaves the inverter after losses? A contract must
keep those questions and their units visible before we add an engine.

A fixed-tilt array has tilt from horizontal and azimuth clockwise from north.
A module specification has reference DC watts and a temperature coefficient;
the inverter has its own input scaling limit and AC rating. Adding module
nameplates does not set the inverter limit. Our authored five-module example
is 5 x 300 = 1500 W reference DC, while its hypothetical inverter is rated
900 W AC with 1000 W DC input scaling and efficiency 0.9. The distinction
explains why clipping can occur without an invalid module rating.

Gilman, NREL/TP-6A20-64102 (2015), pp. 18-19 explains surface angles;
p. 51 Eq. 11.2 gives `P_DC0 = P_AC0 / eta_nom`. Every equipment value is
explicit input. None of these hypothetical numbers recommends real equipment.

The PVWatts DC relation is

`P_DC = (G_effective / 1000 W/m^2) * P_reference * (1 + gamma * (T_cell - T_reference))`.

The irradiance ratio and temperature correction are dimensionless, leaving
watts. This equation and reference irradiance are from pvlib 0.16.1
`pvsystem.pvwatts_dc`, citing Dobos, NREL/TP-6A20-62641 (2014).
The model's reference temperature is supplied explicitly, not inferred.
Ross cell temperature needs explicit NOCT and ambient temperature, or we can
supply cell temperature directly. Its fixed-wind/steady-irradiance assumptions
are limits of the approximation, not measured weather information.

Named loss fractions have a location in the chain. For two sequential losses,
`X_out = X_in * (1-f_1) * (1-f_2)`. Adding fractions loses the cross term and
usually overstates the loss. A 0.1 fraction means ten percent; it is never
silently interpreted as 0.1 percent. Record each removed amount with its unit.
Irradiance-stage loss is W/m^2, while DC and AC losses are W.

Power answers "how fast"; energy answers "how much over time". For interval
mean power, our dimensional equation is

`E_Wh = sum(P_W * duration_s / 3600)`.

The 3600 is seconds per hour, a unit conversion, not an engineering assumption.
An original hand calculation is 100 W for two hours: `100 * 7200 / 3600 = 200 Wh`.
Gilman's pp. 55-56 connect net AC output and delivered hourly energy. These
contract tests check the unit calculation independently of any PV engine.

Coverage is as important as the sum. Half-open intervals have an unambiguous
start and end. An unavailable weather interval is not zero sunlight. The result
may report the energy from its valid intervals, but must mark incomplete
coverage. Monthly totals split a boundary-crossing mean-power interval by time.
A UTC calendar year includes every interval through the next January 1.
Leap 2024 has 366 days, so constant 100 W gives 878400 Wh, and February gives
29 x 24 x 100 = 69600 Wh. These are original calendar test cases, not yield
predictions. Two hours cannot become an annual result by multiplying a factor.

The step trace declares weather channels as named inputs with units, records
their exchange and preserves their values alongside the outputs.
The input weather hash ties the result to exact local file bytes. A citation,
licence and synthetic/observed label explain where those bytes came from.
The trace then records each step and, under D11, equations with sources,
substitutions and answers that a report reviewer can recalculate. Recording a
trace is not enough: WP-2.5's report adapter must independently check it.

The contract uses readable model references, not unavailable IEC 61724-1.
It cannot claim monitoring-standard conformance, qualified equipment or safety
certification. Keeping those limits explicit makes the first working slice
reviewable without inventing missing data.
