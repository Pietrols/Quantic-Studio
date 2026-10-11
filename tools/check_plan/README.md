# Plan checker and owned-path guard

The checker follows PLAN.md sections 0 and 4 and AGENTS.md. The current implementer
completes its own WP; a different model audits milestones. Historical `verified by`
fields remain readable and are not required on new Done records. This precedence
also applies to the older WP-0.3 wording and PR template.

From the repository root, set the same import path that the existing CI hook uses:

```sh
export PYTHONPATH="tools${PYTHONPATH:+:$PYTHONPATH}"
uv run python -m check_plan PLAN.md
uv run python -m check_plan --summary PLAN.md
uv run pytest tools/check_plan -q
```

No dependency, root package configuration or workflow changes are required. Python
needs `tools` on its import path because that is the WP's owned location. The module
command without this environment setup is not an installed workspace command.

The first command validates all WPs, and on a `wp-<id>-<name>` branch it also checks
the committed diff from the merge base with `origin/main`. Commit your changes and
fetch main before the final check. Uncommitted, staged-only and untracked files are
not included in the ownership result. The summary validates the plan and prints a
table without requiring Git or checking ownership. Exit 0 means the requested
checks passed; exit 1 reports the WP, field or path that failed.

For a detached checkout or an explicit comparison:

```sh
uv run python -m check_plan --check-paths --branch wp-0.3-plan-guard --base origin/main --head HEAD PLAN.md
```

In GitHub pull-request CI, the existing hook invokes this module. It uses
`GITHUB_HEAD_REF` for the branch and the PR event's head SHA for ownership, so GitHub's
temporary merge commit cannot charge this WP for another agent's changes. The
checked-out merged plan is still validated. Main pushes validate the plan without
pretending that main belongs to one WP. A PR with an unrecognised branch name fails
ownership rather than silently skipping it. Local non-WP branches and detached
checkouts print that ownership was not checked unless `--check-paths` is requested.

## What the rules mean

- Live `### WP-<number>.<number> <title>` sections are parsed; fenced examples are
  ignored. Every WP needs exactly one of the six required fields and a supported
  status. Dates must exist, and an In progress branch must name its WP.
- Changed design needs all three explanation clauses and the same explanation in
  the permanent Change record. Existing free-form historical records remain intact.
- Ownership comes from PLAN.md at the merge base, not from the branch's edited
  plan. A new WP must be approved in the base plan first. Changing its ownership on
  the working branch does not grant permission. Missing refs/plans fail closed.
- Paths in backticks are repository-root anchored. `*` spans one path component;
  `**` spans zero or more. `/*` means root files, not every file in the repository.
- The WP's named learning note is allowed. New `docs/log/` and
  `docs/sources/entries/` files are allowed. Existing records cannot be changed,
  deleted or renamed, even if a wider owned glob would match them.
- PLAN.md is compared in full, with only this WP's Status and Change record masked.
  Other statuses, titles, steps, permissions and whitespace outside those fields
  must remain unchanged. Existing Change record text is append-only. Explicit
  `PLAN.md` ownership permits wider edits; `(section N only)` limits that extra
  grant to the named level-two section while retaining the own-field allowance.
- Renames check both the old and new path. NUL-delimited Git output preserves names
  with spaces or newlines. Changed symlinks and submodules require manual review.

## Deliberate limits

This is a static workflow check, not an approval service or security sandbox. It
does not prove CI evidence, engineering correctness, completed dependencies, or a
person's authority. Milestone audits and branch protections remain necessary. It
does not infer exceptional permissions from prose, chat messages or logs. Unusual
ownership descriptions, including the historical skeleton's empty-directory prose,
need review and an approved planning change before reuse. Only explicit backtick
paths and the documented PLAN section restriction are interpreted as grants.

Tests use good/bad plans and real disposable Git histories. They cover status
syntax, permanent records, section grants, self-granted scope, cross-boundary moves,
missing refs, unusual filenames, detached heads, PR event metadata and unrelated
main-branch changes.
