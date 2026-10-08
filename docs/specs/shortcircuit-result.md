# Three-phase short-circuit result

Schema: `../../contracts/power/shortcircuit-result.schema.json`

Version 0.2.0. Ik'' (`ikss_ka`) is initial symmetrical RMS current; `ip_ka`
is instantaneous peak current; `ith_ka` is equivalent RMS thermal current for
`fault_duration_s`. All are magnitudes in kA. Each requested case has exactly
one row per input bus, including disconnected or unavailable buses. Both cases
must cover the same bus IDs. Each row records the applied voltage factor.

`success` means every requested current is available. `partial` means at least
one current is available and at least one is unavailable. `failed` means no
current is available. The overall status aggregates all cases by the same rule.
Null is unavailable, never zero. If Ik'' is null, peak and thermal currents must
also be null. Every null field requires a case diagnostic identifying that bus
and exact field. Core validation enforces duplicate IDs, coverage, status and
null-diagnostic consistency; adapters must also check coverage against input.

Invalid schema inputs return diagnostics without a result. Schema-valid inputs
that cannot be calculated return a failed result with all requested buses,
null currents and diagnostics. A supported case may succeed when another fails.
Near-generator peak/thermal duties are unavailable unless the solver can justify
the far-from-generator assumptions; no numeric placeholder is permitted.

Assumptions, request settings and solver/version/input-hash provenance are
required. The hash covers network and request, since duration and case affect
results. This contract does not certify compliance with a paid standard.
