# ADR-0002: JSON Schema is the contract source of truth

Status: Accepted

## Context

Quantic Studio has Python engineering packages and will add a TypeScript user interface. Both sides exchange project data and study results. If each language defines its own data structures, their field names, required values, and validation rules can drift. The contracts also need to be readable and independently checkable without importing a solver package.

## Decision

Use JSON Schema Draft 2020-12 as the source of truth for shared data contracts. Keep schemas engine-neutral. Validate JSON at system boundaries and generate language-specific types from the schemas when useful. Document every schema with a readable Markdown page containing a JSON example, and validate those examples against the schema.

## Reasons

- JSON Schema is language-neutral and matches the JSON project and result files exchanged by the platform.
- It allows input and result structure to be checked before an engineering solver runs.
- It supports generated Python and TypeScript types while leaving the schema as the authoritative definition.
- A small example per schema makes the contract understandable to engineers and helps detect drift.
- Keeping solver-specific fields out of the contract prevents an adapter choice from defining the platform's shared model.

## Consequences

- Schema changes require review because they affect every producer and consumer of the contract.
- Cross-element rules such as unique component IDs and valid bus references require application-level checks in addition to JSON Schema validation.
- JSON Schema format annotations and numeric constraints must be chosen deliberately and tested.
- Language-specific models are derived artifacts, not independent sources of truth.
