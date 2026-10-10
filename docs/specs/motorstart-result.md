# motorstart-result

Schema: `../../contracts/power/motorstart-result.schema.json`

Voltages are magnitudes on each network bus nominal line-to-line voltage base. Signed dip is 100*(pre-start minus locked-rotor)/pre-start; a voltage rise has negative dip. Equality to the user limit passes. All network buses appear exactly once. success means all values are available, independently of passes_limit. If any row is unavailable, status is failed and the overall limit outcome is null, even if another row exceeds the limit. Each unavailable row field needs a bus/field diagnostic. A row may preserve pre-start voltage when the second solve fails; its dip and compliance must then be null. Never substitute zero for a failed voltage solve. Core validation enforces numerical/status/limit consistency. The solver must enforce request/network coverage. Provenance hashes both network and complete request. This is a steady locked-rotor snapshot, not acceleration, protection or starting-time prediction.

```json
{
  "schema_version": "0.3.0",
  "result_id": "schema-example",
  "network_id": "authored-motor-feeder",
  "motor": {
    "motor_id": "motor-1",
    "bus_id": "motor_bus",
    "shaft_rated_kw": 30,
    "efficiency": 0.9,
    "rated_power_factor": 0.85,
    "rated_voltage_kv": 0.4,
    "locked_rotor_current_ratio": 6,
    "locked_rotor_power_factor": 0.3
  },
  "dip_limit_percent": 15,
  "dip_definition": "100*(prestart_vm_pu-locked_rotor_vm_pu)/prestart_vm_pu",
  "status": "success",
  "passes_limit": true,
  "bus_results": [
    {
      "bus_id": "source",
      "prestart_vm_pu": 1,
      "locked_rotor_vm_pu": 1,
      "dip_percent": 0,
      "passes_limit": true
    },
    {
      "bus_id": "motor_bus",
      "prestart_vm_pu": 1,
      "locked_rotor_vm_pu": 0.9,
      "dip_percent": 10,
      "passes_limit": true
    }
  ],
  "assumptions": [
    "Synthetic schema illustration, not a numerical reference."
  ],
  "diagnostics": [],
  "provenance": {
    "solver_name": "schema-example",
    "solver_version": "1",
    "input_hash_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "timestamp": "2026-10-10T00:00:00Z"
  }
}
```
