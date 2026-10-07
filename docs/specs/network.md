# Power network

Schema: `../../contracts/power/network.schema.json`

The network contract describes buses, lines, two-winding transformers, loads, generators, external grids, and shunts without naming any simulation engine. All component IDs are strings. Every bus reference must resolve to a bus ID in the same network, and IDs must be unique within their component type; JSON Schema checks each object's shape, while a project loader checks these cross-element relationships.

Line resistance and reactance are per unit length, so the line's total series impedance is derived using `length_km`. Line charging susceptance is also per unit length. Transformer resistance and reactance are per unit on the transformer's `sn_mva` and nominal voltage bases. `tap_ratio`, when present, multiplies the nominal turns ratio, and `phase_shift_degree` is the phase displacement. A load's positive `p_mw` denotes consumption; sign conventions for reactive power are preserved by its signed `q_mvar`. Shunt values are specified as power at nominal bus voltage, with positive values denoting consumption.

The example values are synthetic and demonstrate contract shape only. They are not equipment ratings or a reference test case.

```json
{
  "schema_version": "0.1.0",
  "network_id": "example-two-bus",
  "base_mva": 10.0,
  "buses": [
    { "bus_id": "bus-grid", "vn_kv": 11.0, "bus_type": "slack" },
    { "bus_id": "bus-load", "vn_kv": 11.0, "bus_type": "pq" }
  ],
  "lines": [
    {
      "line_id": "line-1",
      "from_bus": "bus-grid",
      "to_bus": "bus-load",
      "length_km": 1.0,
      "r_ohm_per_km": 0.1,
      "x_ohm_per_km": 0.2,
      "b_us_per_km": 1.0,
      "max_current_ka": 0.2
    }
  ],
  "transformers": [],
  "loads": [
    { "load_id": "load-1", "bus_id": "bus-load", "p_mw": 1.0, "q_mvar": 0.2 }
  ],
  "generators": [],
  "external_grids": [
    {
      "external_grid_id": "grid-1",
      "bus_id": "bus-grid",
      "vm_setpoint_pu": 1.0,
      "va_setpoint_degree": 0.0
    }
  ],
  "shunts": []
}
```
