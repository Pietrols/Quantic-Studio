# Projects, models and physical assets

A project is a container. A model is a particular engineering representation.
A study asks an engine to calculate something on one model. A physical asset
may have representations in several models without being several physical items.

For example, a motor can be an operating load in a power network, a controlled
device in a PLC model and a dynamic machine in another workspace. One asset ID
links those representations. It does not make the engines interchangeable or
force them to share implementation objects. Each engine still owns its equations.
The current registry validates power network element references and model bindings.
Foreign element references await their domain contracts. Study-local motor-start
nameplates are not network elements; linking those requests requires an explicit
future addressing extension, not automatic conversion into existing loads.

## Study routing

A multi-domain project may contain several power networks, perhaps a plant and
a feeder model, alongside a PLC program. The manifest gives each a model ID and
file. Every study explicitly names its model. A fault request's network_file must
match that model file. Selecting an arbitrary first network would produce a valid
calculation for the wrong system, a serious error that schema-valid results alone
cannot catch.

Core exposes Project.models and Study.model_id. CLI follows this binding. The
old Project.network accessor still works for one-power-network projects, and
raises an error for multiple or zero power networks. The API/editor must use
explicit study/model selection.

## Compatibility and migration

Old manifests 0.1, 0.2 and 0.3 remain readable through exact archived schemas.
They are normalized in memory to a single power model, whose model ID derives
from network_id. Their files and study schemas stay unchanged. Manifest 1.0 is a
major version because its structure replaces network_file with models and adds
model bindings to studies. It does not require upgrading power payloads.

A deliberate migration writes a new manifest with a model entry for each old
network, assigns study model IDs, and supplies an empty or populated asset
registry. Loading does not perform this rewrite automatically. That preserves
old workflows and lets an engineer review migration separately.

## Storing is different from validating or executing

Future-suite files can be retained now as JSON objects. Core verifies file paths,
finite JSON numbers and identity/binding structure, but emits explicit deferred
validation diagnostics for payload/request kinds with no implemented schema.
CLI refuses to execute those studies. Other supported power studies still run.
The example's PLC content is an authored placeholder, not a validated IEC program.

Known power references must name a real element in their declared collection.
An unknown foreign element reference is not silently accepted as validated;
its diagnostic records the missing domain check. Duplicate IDs, missing models,
invalid known power references and representations shared by two assets are errors.

## Safety and provenance boundaries

Project paths are confined after resolution, so a symlink cannot redirect a model
outside the project. Requests must remain separate from model/manifest files.
Models must have distinct files. Core never rewrites loaded model or asset data.

Electrical results hash the inputs their solver actually uses under the existing
study provenance policy. Changing an unrelated PLC label does not change motor
impedance. A whole-project archive may additionally hash every file, including
registry and foreign representations. Identity links alone do not exchange signals
or imply a co-simulation; shared time-series and coupling contracts come later.
