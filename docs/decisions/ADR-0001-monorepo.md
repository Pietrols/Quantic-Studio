# ADR-0001: Monorepo with strict package boundaries

Status: Accepted

## Context

The platform combines engineering workbenches that share schemas, adapters, tests, documentation, and project data. Early development will often change several of these together.

## Decision

Keep the platform in one monorepo and enforce strict boundaries between its packages. The repository may be split later if those boundaries and project needs justify it.

## Reasons

- Early work can change schemas, adapters, tests, and docs atomically in one repository.
- One repository provides one CI system, issue tracker, and work plan for all contributors.
- Owned paths, dependency rules, and CI checks enforce package boundaries and leave the option to split packages into separate repositories later.
- Large external engines such as pandapower, ngspice, and containerlab remain external dependencies and are never copied into the repository.

## Consequences

- Related changes can be reviewed and released together.
- Contributors must respect package ownership and dependency boundaries even though the code is in one repository.
- Dependency rules need automated enforcement as the package set grows.
- Packages can move to separate repositories later without requiring that split now.
