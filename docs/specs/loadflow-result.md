# Load-flow result

Schema: `../../contracts/power/loadflow-result.schema.json`

The result reports bus voltage magnitude in per unit and voltage angle in degrees. Each line or transformer has active and reactive power at both ends, losses, and loading. `loading_pct` is null only when no applicable thermal rating was supplied; implementations should emit a diagnostic explaining why loading is unavailable. A non-converged result still carries the best available state, convergence details, diagnostics, and provenance.

## Loading convention

For a line, `loading_pct` is 100 times the largest terminal current divided by its
`max_current_ka` rating. For a two-winding transformer, `loading_pct` is based on
current at both windings, using each winding's declared nominal voltage and the
transformer's `sn_mva` rating:

```text
I_rated_hv_ka = sn_mva / (sqrt(3) * vn_hv_kv)
I_rated_lv_ka = sn_mva / (sqrt(3) * vn_lv_kv)
loading_pct = 100 * max(abs(I_hv_ka) / I_rated_hv_ka,
                        abs(I_lv_ka) / I_rated_lv_ka)
```

For balanced three-phase terminal power, the current magnitude can be recovered as
`abs(I_ka) = hypot(p_mw, q_mvar) / (sqrt(3) * V_terminal_kv)`, where
`V_terminal_kv = vm_pu * bus.vn_kv` uses the **solved** terminal voltage. The rating
uses the transformer's `vn_hv_kv` or `vn_lv_kv`, which need not equal the corresponding
bus base. Thus, on either winding, the current ratio can equivalently be calculated
as `hypot(p_mw, q_mvar) / sn_mva * vn_winding_kv / V_terminal_kv`.

Do not substitute `100 * max(abs(S_hv), abs(S_lv)) / sn_mva`: that is apparent-power
loading and can understate winding current at low voltage. This current convention
was explicitly selected by Peter for M0 because winding heating depends on current.
It defines the reported loading ratio, not a detailed thermal or ageing model.

This example is synthetic and demonstrates the result structure only.

```json
{
  "schema_version": "0.1.0",
  "result_id": "result-1",
  "network_id": "example-two-bus",
  "bus_results": [
    { "bus_id": "bus-grid", "vm_pu": 1.0, "va_degree": 0.0 },
    { "bus_id": "bus-load", "vm_pu": 0.99, "va_degree": -0.5 }
  ],
  "branch_results": [
    {
      "branch_id": "line-1",
      "branch_type": "line",
      "p_from_mw": 1.01,
      "q_from_mvar": 0.22,
      "p_to_mw": -1.0,
      "q_to_mvar": -0.2,
      "p_loss_mw": 0.01,
      "q_loss_mvar": 0.02,
      "loading_pct": 30.0
    }
  ],
  "convergence": {
    "converged": true,
    "iterations": 3,
    "largest_mismatch_mva": 0.00001
  },
  "diagnostics": [],
  "provenance": {
    "solver_name": "example-solver",
    "solver_version": "1.0.0",
    "input_hash_sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    "timestamp": "2026-10-08T12:00:00Z"
  }
}
```
