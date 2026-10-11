# Project asset-registry

Schema: `../../contracts/project/asset-registry.schema.json`

One stable asset ID represents a physical item across model-specific views. Representations use model ID, plural element collection/type and model-local element ID. Model references must exist. Known power element references must exist in their named collection. Foreign element references have explicit deferred-validation diagnostics until domain contracts exist. Each representation tuple belongs to exactly one asset; duplicate asset/model/study IDs and dangling references are loader errors. Registry identities do not alter electrical solver inputs or imply a co-simulation coupling. An asset can have multiple representations; elements without a physical asset link remain valid. The standalone schema validates structure; core project loading validates references and uniqueness.

```json
{
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
```
