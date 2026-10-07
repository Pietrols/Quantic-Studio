# Load-flow request

Schema: `../../contracts/power/loadflow-request.schema.json`

A request names the network file and makes solver stopping criteria explicit. `tolerance_mva` is the maximum accepted active or reactive power mismatch, and `max_iterations` is a caller-provided iteration limit. The contract does not choose default engineering tolerances. `initialization` is optional; `flat` starts from nominal voltage magnitudes and zero angles, while `previous_result` asks an implementation to use a compatible prior solution when available.

The example inputs are illustrative only and do not prescribe study settings.

```json
{
  "schema_version": "0.1.0",
  "request_id": "loadflow-base-case",
  "network_file": "network.json",
  "tolerance_mva": 0.0001,
  "max_iterations": 20,
  "initialization": "flat"
}
```
