# Project manifest

Schema: `../../contracts/project/manifest.schema.json`

The project manifest is the entry point for a study. `schema_version` identifies the contract version used by the project. `network_file` and each `request_file` are relative paths within the project folder, not absolute paths. Each study has a project-unique identifier and a study type string so new study kinds can be added without coupling the manifest to a particular solver.

```json
{
  "schema_version": "0.1.0",
  "name": "Example distribution study",
  "network_file": "network.json",
  "studies": [
    {
      "study_id": "loadflow-base-case",
      "study_type": "loadflow",
      "request_file": "studies/loadflow-request.json"
    }
  ]
}
```
