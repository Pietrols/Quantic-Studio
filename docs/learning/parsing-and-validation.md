# Parsing a plan and enforcing work boundaries

A shared repository needs an equivalent of a work permit. A work package says what
an agent may change, and its status says where that work stands. When several agents
work at once, checking those statements automatically catches mistakes before they
reach main.

## Parsing and validation are different jobs

A parser turns text into structure. Here it finds each WP heading and collects its
Status, Lane, Depends on, Owned paths, Learning note and Change record. It ignores
fenced code examples so a sample status is not mistaken for a second real status.

Validation asks whether that structure follows the rules. A WP must have exactly
one of every required field. Its status must be Not started, In progress, Done or
Changed design. An In progress branch must identify that WP, and a date such as
30 February is rejected even though it looks like a date.

The distinction matters: finding a line beginning `Status:` is easy, but accepting
two contradictory status lines would make the summary unreliable. Diagnostics name
the WP and field so an agent can correct the actual problem.

The current rules let an implementer complete its WP after acceptance and green CI.
A different model audits milestones. Older Done records contain verifier names;
they remain valid history, but the checker does not force new work back into the
superseded per-WP verification process.

## Ownership as a set check

Let D be the set of paths changed by a branch, O its approved owned paths, and E the
standing exceptions: the named learning note and new log/source entries. For ordinary
files, the requirement is:

```text
D is a subset of (O union E)
```

PLAN.md needs a more precise check. Permission to update one status cannot imply
permission to rewrite another agent's task. The checker masks only the current WP's
Status and Change record, then compares the rest of the old and new documents. The
remaining text must be identical unless the WP explicitly owns a larger part of the
plan. Existing Change record text must also remain as a prefix of the new record.

A planning WP can own a named section. That adds permission for that section while
retaining the usual right to update its own status and permanent change record.

## Why permissions come from the base

Suppose a branch owns `tools/check_plan/**` but edits the power solver. If it can
change its own Owned paths line to include that solver and then validate against the
edited plan, the guard has no value. We therefore read permissions from the common
ancestor of the branch and main: the merge base.

The comparison is the same set of committed changes represented by:

```sh
git diff --name-only origin/main...HEAD
```

The three dots matter. If another agent adds a report to main after this branch
starts, a direct comparison of the two tips can wrongly treat that report as our
deletion. Comparing from their common ancestor isolates this branch's work.

An approved new WP must reach the base plan before an implementation branch can use
its permissions. A chat approval does not automatically rewrite what the checker
knows. Exceptions belong in an explicitly approved planning change, not a hidden
bypass switch.

## Boundaries must include moves and history

A rename has two sides. Moving an unowned file into an owned folder still changes
the unowned original. The checker treats a move as deletion plus addition and checks
both paths. Logs and source entries are stricter: only new files are allowed, so
history cannot quietly be rewritten.

Path matching is anchored at the repository root. A single `*` cannot cross a slash;
`**` can. Thus `/*` means root files and `tools/check_plan/**` cannot accidentally
include `tools/check_plan_extra/`.

## What a passing check does and does not prove

A passing plan check proves the document follows the supported format. A passing
ownership check proves the committed branch diff stays within the interpreted
permissions. It does not prove the numerical results, verify a claimed CI run, or
replace a milestone audit. Uncommitted edits are not in the ownership diff.

The tests deliberately try to break the rules in temporary Git repositories. This
checks behaviour that simple string tests miss: deleted logs, renamed files, changed
permissions, detached PR checkouts and concurrent main changes.

## Running it

From the repository root, after the normal workspace sync:

```sh
export PYTHONPATH="tools${PYTHONPATH:+:$PYTHONPATH}"
uv run python -m check_plan PLAN.md
uv run python -m check_plan --summary PLAN.md
```

The import path makes the WP-owned module discoverable without changing the root
workspace. CI already provides that path. Commit the proposed work before the final
ownership check, and use the summary at session start to see every WP's current state.
