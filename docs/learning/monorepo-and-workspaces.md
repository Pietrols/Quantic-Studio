# Monorepos and Python workspaces

## What is a monorepo?

A monorepo is one version-controlled repository containing several related packages and the project material around them. Quantic Studio uses one repository for shared data contracts, Python engineering packages, examples, tests, and documentation. A monorepo is not the same as one giant package: each package can have a focused purpose and clear rules about what it may depend on.

Keeping related work together makes a change to a shared contract, the packages that use it, and its tests visible in one review. It also gives contributors one issue tracker, one CI setup, and one plan. The trade-off is that boundaries must be made explicit, or unrelated packages can become tightly coupled.

## How uv workspaces work

The root `pyproject.toml` defines a uv workspace. The root project is a workspace manager rather than an installable package, and `packages/py/*` identifies the Python packages that belong to the workspace. Each member package has its own `pyproject.toml` describing its name, dependencies, and build details.

The workspace gives its members a shared dependency resolution and lock file. Running `uv sync` at the root resolves the workspace dependencies and installs the development environment. As package manifests are added, the member pattern lets uv discover them without turning the repository root into a Python library.

For example, `qe_power` can be developed alongside `qe_core` in the same checkout. A contributor can update both packages together and run tests using the same environment and lock file.

## Why package boundaries matter

Boundaries make the direction of dependencies predictable. In this project, `qe_core` owns shared loading, validation, units, and provenance and does not depend on domain packages. A domain package such as `qe_power` can depend on the core, but domain packages do not import each other. The CLI and report packages sit at the edges and can coordinate domain functionality.

This structure prevents a change in one engineering workbench from unexpectedly breaking another. It also makes replacement easier: engine-specific code stays in its adapter area, and a package can be tested without importing every other workbench. Boundaries are useful only when followed, so owned paths, review, and automated dependency checks will enforce them as the repository grows.
