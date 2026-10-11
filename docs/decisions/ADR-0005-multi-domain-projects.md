# ADR-0005: Multi-domain projects and physical asset identity

Status: Accepted under Peter's continuation authorization, CC-3 / WP-1.9.
Context: ADR-0003-four-suites and the Phase 1 prerequisite plan merged in PR 30.

## Decision

Manifest 1.0 contains a model collection, studies bound by model ID, and an
inline versioned asset registry. This is a major contract version because it
replaces the top-level single network_file. Previous manifest schemas remain
byte-for-byte under contracts/v0.1, v0.2 and v0.3. Existing power network,
request and result versions remain unchanged. Legacy projects become one-model
projects in memory, without rewriting their files.

Model IDs, study IDs and asset IDs have separate project-local namespaces.
Model IDs identify representations. Asset IDs identify physical items across
representations. An asset reference names a model, an element collection/type,
and an element ID. Each representation belongs to at most one physical asset.
Power references are validated against known network collections. This contract
does not yet bind study-local motor request equipment to an asset; use existing
network elements for known power references. A future contract can extend that
addressing explicitly rather than treating a request motor as a network load.

Core owns loading and binding checks and imports no engine. CLI selects the
study's model; it never selects the first model. The legacy Project.network
accessor requires exactly one power network, preventing silent routing errors.
Unknown domain model and study kinds can be stored as confined JSON-object files,
but receive deferred-validation diagnostics. CLI rejects unsupported execution.
This permits future-suite content to coexist with runnable power studies without
pretending to validate a domain whose contract does not yet exist.

Every model needs a distinct payload file; requests are separate from models and
the manifest. All paths are relative to the project root and resolved within it,
including symlink checks. A power request's network_file must resolve to the
bound model file. Supported power studies on foreign models are errors.
Duplicate IDs, dangling references and duplicate representation ownership fail
loading. Deferred foreign element references are retained and diagnosed.

Numerical provenance retains each study's existing policy: selected network and
request content for fault/motor studies, network bytes for legacy load flow.
Registry and unrelated foreign models do not change numerical inputs. A complete
project archive can use core hash_files for a broader provenance boundary.
Model binding is checked before execution; registry links are identity, not a
signal-coupling or simulation interface.

## Consequences

API and canvas can enumerate models and assets without importing foreign engines.
Future domain WPs must add real payload/request validation and execution support
before replacing deferred diagnostics. Time series and FMI-style co-simulation
remain separate contracts. Persisted generic canvas layout is not included here;
WP-1.6 must complete any required layout Contract Change before implementing it.

Rejected alternatives: first-power-model defaults create ambiguous study routing;
copying electrical models into control engines breaks the domain boundary; and
accepting arbitrary foreign JSON as verified engineering input hides validation
gaps. No engineering constants or numerical modelling changes are introduced.
