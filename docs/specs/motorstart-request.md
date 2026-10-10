# motorstart-request

Schema: `../../contracts/power/motorstart-request.schema.json`

One balanced three-phase motor starts from disconnected. The network contains all other pre-existing loads; do not also include this motor as a load. Motor voltage is line-to-line kV, shaft rating is mechanical kW, efficiency and both power factors are fractions in (0,1]. Starting current ratio is locked-rotor current divided by full-load rated current at the motor rated voltage. Both power factors are lagging. All values and the dip limit are user inputs, with no equipment defaults. Solver tolerance is MVA. The bus must exist. Study-local motor_id is not yet a cross-suite asset registry.

```json
{
  "schema_version": "0.3.0",
  "request_id": "motor-start",
  "network_file": "network.json",
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
  "tolerance_mva": 1e-10,
  "max_iterations": 100
}
```
