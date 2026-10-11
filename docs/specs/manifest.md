# Project manifest

Schema: `../../contracts/project/manifest.schema.json`

Manifest 1.0 binds studies to model IDs rather than one top-level network. Model, study and physical asset IDs each have project-local namespaces. Each model owns a distinct confined JSON-object file; a request is separate from model/manifest files. A supported power request must name the bound model file, relative to the project root. Unknown model/study kinds may be stored as JSON objects with explicit deferred-validation diagnostics, never treated as validated engineering data or executable support. All IDs are non-empty, case-sensitive opaque strings. No domain engine imports another. Files are read without rewriting.

```json
{
  "schema_version": "1.0.0",
  "name": "Authored mixed-domain project",
  "models": [
    {
      "model_id": "plant",
      "model_type": "power.network",
      "file": "plant.json"
    },
    {
      "model_id": "motor-feeder",
      "model_type": "power.network",
      "file": "motor-feeder.json"
    },
    {
      "model_id": "control",
      "model_type": "automation.plc",
      "file": "control.json"
    }
  ],
  "studies": [
    {
      "study_id": "plant-flow",
      "study_type": "loadflow",
      "model_id": "plant",
      "request_file": "plant-flow.json"
    },
    {
      "study_id": "plant-fault",
      "study_type": "shortcircuit",
      "model_id": "plant",
      "request_file": "plant-fault.json"
    },
    {
      "study_id": "motor-start",
      "study_type": "motorstart",
      "model_id": "motor-feeder",
      "request_file": "motor-start.json"
    },
    {
      "study_id": "control-scan",
      "study_type": "plc.scan",
      "model_id": "control",
      "request_file": "scan.json"
    }
  ],
  "asset_registry": {
    "schema_version": "1.0.0",
    "assets": [
      {
        "asset_id": "feeder-asset",
        "name": "Feeder monitored by control model",
        "representations": [
          {
            "model_id": "motor-feeder",
            "element_type": "lines",
            "element_id": "feeder"
          },
          {
            "model_id": "control",
            "element_type": "devices",
            "element_id": "feeder-sensor"
          }
        ]
      }
    ]
  }
}
```

Legacy manifests 0.1, 0.2 and 0.3 remain readable through exact archived schemas.
They become one power.network model in memory, with its model ID derived from
network_id. Their study types and original requests are unchanged. No automatic
file rewrite occurs. Manifest 1.0 is a major version because models/study bindings
replace network_file. Power network and study request/result versions do not change.

Core exposes Project.models, Project.assets and Study.model_id. Project.model(id)
selects a model; Model.network requires power.network. Project.network is a
compatibility accessor only when exactly one power model exists. Future API/editor
code must bind to the selected study model. Numerical provenance continues to hash
selected network and request under each study's existing policy, not unrelated
foreign models or identity-only registry entries. The manifest/model binding is
validated before execution; a project archive may separately hash all project files.
