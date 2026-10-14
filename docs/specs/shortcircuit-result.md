# Three-phase short-circuit result

Schema: `../../contracts/power/shortcircuit-result.schema.json`

Version 0.3.0. Ik'' (`ikss_ka`) is initial symmetrical RMS current; `ip_ka`
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

## Calculation trace (version 0.3.0, CC-7)

Each bus row may carry a `trace`, the worked calculation behind its currents
(decision D11). It is null whenever Ik'' is null. Fields: nominal voltage
`un_kv`, voltage factor, source voltage c Un / sqrt(3) in kV, the Thevenin
impedance at the fault bus `zk_r_ohm`, `zk_x_ohm`, `zk_ohm` in ohms, its R/X,
and, when the duties are available, `kappa` with its method, `m` and `n`.

`impedance_basis` is `radial-sum` when the adapter summed the element
impedances itself (single-source radial components) and `engine-thevenin`
otherwise. For `radial-sum`, `elements` lists each series element between the
source and the bus with its numeric inputs, its own-side R and X in ohms, the
referral factor (product of squared rated transformer ratios crossed) and the
referred R and X. The adapter reports a current only if this sum agrees with
the engine's reduction, and c Un / (sqrt(3) |Z_k|) reproduces the engine's Ik'',
to a relative 1e-9; otherwise the values are unavailable with TRACE_MISMATCH.

Version 0.2.0 results remain valid against
`contracts/v0.2/power/shortcircuit-result.schema.json`.
