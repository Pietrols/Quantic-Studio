# qe_core

Contracts are validated at load time with jsonschema Draft 2020-12 and a local
referencing registry. We do not generate a second schema definition. Successful
loads return typed Project, Network and Study dataclasses containing validated
contract dictionaries; failures return Outcome diagnostics rather than partial models.

Use `load_project(folder)` with a manifest.json, its network, and request files.
File references resolve relative to the project root. Symlinks outside that root,
unsupported schema versions, malformed JSON, nonfinite values, duplicate identifiers
and unknown buses produce diagnostics. Each diagnostic names a field and element.
No remote schema retrieval is configured.

This Phase 0 package runs from the editable workspace. It finds the repository's
contracts beside the workspace rather than copying frozen schemas into the wheel.
A standalone distribution will need an explicitly versioned contract resource package.

`units.convert(value, from_unit, contract_field)` uses Pint and the contract unit map.
Dimensional conversion does not turn MW into a physical reactive or apparent power;
Mvar/MVA aliases only express the common SI dimension. Per-unit conversion requires
an external base and is not inferred by this helper.

`hash_files` sorts relative filenames and hashes length-prefixed names and byte
contents. `hash_inputs` hashes canonical JSON for in-memory solver inputs. These are
separate, documented hash domains. `provenance` adds solver, version and UTC time.

Run `uv run pytest packages/py/qe_core` from the repository root.
