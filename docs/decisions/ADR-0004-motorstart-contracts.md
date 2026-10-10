# ADR-0004: Study-local locked-rotor motor contract

Status: Accepted under Peter's 2026-10-10 continuation authorization, CC-2 / WP-1.8.

One motor starts from disconnected. Its nameplate and connection belong to the
request because the existing network describes the pre-start operating point.
This additive study requires manifest v0.3, with exact v0.2 preservation under
contracts/v0.2. The network remains v0.2; v0.1 load-flow projects remain readable.
No solver, CLI or report implementation is claimed here: WP-1.4 follows serially.

All motor data are explicit user inputs. Rated voltage is line-to-line kV,
shaft rating is mechanical kW, efficiency and power factors are fractions.
Starting current ratio uses full-load rated current at rated motor voltage.
Rated and locked-rotor power factors are independent, both lagging.
The connected motor is constant impedance during the starting snapshot.

Results report both voltage magnitudes on each bus nominal voltage base.
Dip is signed relative to pre-start voltage. A rise is negative; equality to
the user-specified limit passes. Calculation status is independent of engineering
compliance. Missing results are null, with bus/field diagnostics. A failed study
has unknown overall compliance; it must never claim a pass from only a subset.

A study-local motor ID is not the shared asset identity required by the four-suite
architecture. The separate multi-domain project/asset Contract Change must still
land before WP-1.5 and WP-1.6. Domain engines remain independent.

Rejected alternatives: embedding starting data in ordinary constant-power loads
would obscure the pre-start operating point and risk double counting. Changing
the network format for a study-local motor would create unnecessary migration.
