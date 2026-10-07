# Diagnostic

Schema: `../../contracts/common/diagnostic.schema.json`

A diagnostic explains a condition in a stable, machine-readable form. The code is a stable identifier, severity is `info`, `warning`, or `error`, and the message is written for a person. `element_ref` is null for a general condition. Otherwise it identifies the element and may identify the field that needs attention.

```json
{
  "code": "MISSING_FIELD",
  "severity": "error",
  "message": "Bus voltage rating is required.",
  "element_ref": {
    "element_type": "bus",
    "element_id": "bus-1",
    "field": "vn_kv"
  }
}
```
