# Continuous integration: keeping each change checkable

Continuous integration (CI) runs the same checks on a fresh machine whenever someone
opens or updates a pull request, and when code reaches main. A passing run means those
checks passed for that commit. It does not mean every engineering result is correct,
and it does not replace the independent verifier required by this project.

## A reproducible starting point

A developer's computer can hide missing files or dependencies. GitHub Actions checks
out the repository and installs Python 3.12 with uv. `uv sync --all-packages --locked`
uses the committed dependency lock and fails if that lock needs updating. The
all-packages option includes workspace members once their manifests are enabled.

The workflow then runs repository guards, Ruff and pytest. Ruff catches common Python
mistakes without running the program. Pytest executes examples of expected behaviour.
Neither is a numerical reference: a solver will still need independently sourced cases,
units, tolerances and provenance in its own WP.

Think of the result as a conjunction of requirements:

    CI passes = dependencies resolve AND style checks pass AND tests pass
                AND repository guards pass AND available plan checks pass

One false condition makes the run fail. We keep the remaining diagnostic steps running
after a failure, so one bad punctuation mark does not hide an import-boundary defect.
We do not convert failed tests, or an empty test suite, into a passing run.

## Why check only tracked files?

Git's tracked-file list describes the material a commit can deliver. Local scratch files,
virtual environments and downloaded packages should not determine whether our source
meets the repository rules. This distinction fixes the problem seen in WP-0.1, where
a recursive punctuation scan accidentally inspected installed dependencies.

The text guard reports a filename and line for U+2014. It reads UTF-8 bytes and treats
NUL-containing data as binary. The reference guard rejects tracked PDF, EPUB and DJVU
files outside `docs/assets/`, even if someone force-adds an ignored file. This catches
an accidental commit of a private book; the allowlist still does not grant permission
to publish someone else's material.

## Dependency rules are a directed graph

Treat each package as a vertex. An import from package A to package B creates the
edge A -> B. Core must have no outgoing edges to other internal packages. A domain
may have an edge to core, but not to another domain. The CLI and report packages may
coordinate domains. For example:

    qe_cli -> qe_power -> qe_core
    qe_report -> qe_power

The forbidden edge `qe_core -> qe_power` reverses the intended direction and makes
shared infrastructure depend on one study type. If domains import each other, changing
one study can unexpectedly affect another. Engine imports belong in adapters so an
engine can be replaced without rewriting the rest of the package.

The Python guard parses import syntax using the standard library AST, without importing
or running the inspected module. It also checks literal dynamic imports. Computed
module names, aliases for dynamic loaders and unusual TypeScript syntax remain review
concerns; static inspection is not a security sandbox. The current engine list covers
pandapower, selected for Phase 0, and must grow when adapters are added.

## Proving a guard rejects mistakes

A test that only sees correct input cannot show that a guard catches its target defect.
Our unit tests build temporary Git repositories, stage both valid and invalid files,
and check the exit status and diagnostic path. The WP's acceptance test also uses a
disposable PR with three synthetic defects: forbidden punctuation, a core import of
a domain, and a root-level file named `book.pdf`. That file is plain synthetic text,
not a real book. Each intended CI step must fail, then pass after the fixtures are
removed. The test PR is closed without merging.

The implementation PR remains available for Lane A to inspect and rerun. Codex can run
its implementation tests but cannot independently verify its own WP or mark it Done.

## What happens when the plan checker arrives?

The workflow currently reports that the checker is not implemented. Once WP-0.3 adds
its Python module entry point, the same step runs it against PLAN.md. The checker's
nonzero exit status will fail CI. A .gitkeep placeholder does not count as an executable
checker.

To reproduce the checks locally, see [the CI command guide](../../tools/ci/README.md).
Workflow setup follows the [uv GitHub Actions guide](https://docs.astral.sh/uv/guides/integration/github/).
