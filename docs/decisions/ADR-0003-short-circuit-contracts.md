# ADR-0003: Versioned three-phase short-circuit contracts

Accepted under Peter's explicit CC-1 authorization, 2026-10-08.

Use version 0.2.0 for the extended network, manifest and new fault requests and
results. Keep original 0.1 schemas under `contracts/v0.1/` with unchanged IDs.
Core dispatch selects the schema by document version. Load-flow request/result
and common diagnostics/provenance remain 0.1.0. A 0.2 manifest may contain both
study types and load an old network; missing fault inputs are study diagnostics.
Version 0.1 documents cannot silently acquire new equipment fields.

Short circuit uses the balanced positive-sequence equivalent-voltage-source
method. Transformer vector group is unnecessary for this three-phase scope;
zero-sequence and earth faults are not supported. Transformer impedance remains
on its own rated MVA and LV kV bases, not the network base. Generator `xdss_pu`
uses its own `sn_mva` and `vn_kv`; `rdss_ohm` is on its own voltage side. External
grid strength is three-phase MVA and R/X is dimensionless. No equipment defaults
are provided. Generator voltage-control range and power-station association,
and transformer OLTC/unit flags, are represented so unsupported station modelling
can be diagnosed explicitly rather than silently treated as an ordinary transformer.

Each request supplies duration, frequency, cases and LV tolerance. Each result
records voltage factors, assumptions and provenance. Unavailable currents are
null with bus/field diagnostics. Structural constraints are JSON Schema;
relational result constraints are also enforced by core validation. See the
request and result specifications for precise status semantics.

Pandapower documents peak/thermal currents only for faults far from synchronous
generators. WP-1.3 must conservatively withhold these duties where that assumption
cannot be established. IEC 60909-0 has not been supplied: cite readable pandapower
pages and the pinned implementation, state limitations, and do not claim
independent standards certification.

Source review found a documentation discrepancy: the branch-elements page
prints 0.04/K for minimum-case line resistance, while pandapower 3.5.6
`build_branch._end_temperature_correction_factor` uses 0.004/K. This ADR does
not choose a normative value. WP-1.3 must document its implementation basis
or diagnose unsupported corrections rather than hide the difference.
