# Repository checks

Run from the repository root after `uv sync --all-packages --locked`:

```sh
uv run python tools/ci/check_repository.py text
uv run python tools/ci/check_repository.py references
uv run python tools/ci/check_repository.py boundaries
uv run ruff check --config tools/ci/ruff.toml .
uv run pytest
```

The guards inspect `git ls-files`, including newly staged files. Untracked local scratch
files and installed dependencies do not affect the result. Failure messages identify
the path, and where applicable the line and violated dependency.

The text guard searches UTF-8 bytes and treats NUL-containing files as binary. The
reference guard checks extensions without case sensitivity and permits them only below
`docs/assets/`. An allowed path is not permission to publish copyrighted material.

The boundary guard parses Python imports without importing any application code.
`qe_core` cannot import another internal package. Domain packages can import themselves
and `qe_core`; they cannot import other domains or the CLI/report layers. CLI and report
packages can coordinate domains. `pandapower`, the engine selected for Phase 0, can only
be imported below `qe_power/src/qe_power/adapters/pandapower/`. Add engine module names
when new adapters are introduced. TypeScript import sources must not reference Python
modules or package paths.

This is a static dependency check, not a security sandbox. It checks Python import
statements and literal calls to `__import__` and `importlib.import_module`; computed
module names and aliases for dynamic loaders need review. TypeScript checking is a
conservative import-source scan rather than a complete TypeScript parser.

The workflow runs all workspace tests and does not suppress pytest's no-tests or
failure exits. The CI guard tests themselves give this skeleton a meaningful suite.
The plan-check step is skipped only while its Python entry point is absent. It supports
either `tools/check_plan/__main__.py` or `tools/check_plan/check_plan/__main__.py` so
WP-0.3 can supply the command without an unrelated workflow change.

For acceptance, use a disposable test PR containing synthetic fixtures, never a real
book: a tracked text file with U+2014, a core module importing `qe_power`, and `book.pdf`.
The corresponding steps must fail. Remove the fixtures and confirm all steps pass.

Workflow setup follows the [uv GitHub Actions guide](https://docs.astral.sh/uv/guides/integration/github/).
The workflow uses `pull_request` and read-only repository permissions.
