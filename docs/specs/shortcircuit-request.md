# Three-phase short-circuit request

Schema: `../../contracts/power/shortcircuit-request.schema.json`

Version 0.2.0. Every input is explicit: balanced bolted three-phase faults at every bus, requested maximum/minimum cases, positive fault duration in seconds, frequency 50 or 60 Hz, and low-voltage tolerance 6 or 10 percent. The equivalent-voltage-source method is used; pre-fault load flow is not an input. Unknown equipment data must produce diagnostics, never defaults. Network paths follow project confinement rules.

```json
{
  "schema_version": "0.2.0",
  "request_id": "three-phase-fault",
  "network_file": "network.json",
  "fault_type": "3ph",
  "cases": [
    "max",
    "min"
  ],
  "fault_duration_s": 1,
  "frequency_hz": 50,
  "lv_tolerance_percent": 10
}
```
