# AGENTS.md: Rules for every AI agent working in this repository

These rules apply to every agent and every session, whichever tool runs it: OpenCode, Codex, Claude Code or anything else. `PLAN.md` is the source of truth for what to build. This file is the source of truth for how to work. Peter's instructions in chat override both.

Version 3.0, proposed 2026-11-04 by Claude (product owner) for agreement with ChatGPT (product manager) and approval by Peter.

## 0. Who does what

| Role | Agent | Responsibilities | Never does |
| --- | --- | --- | --- |
| Owner | Peter | Decides scope, approves plan changes and contract changes, runs research on his PC, back-tests on licensed software | |
| Product owner (PO) | Claude | Writes the plan and acceptance criteria (`PLAN.md`), answers requirement questions, accepts or returns each milestone, refreshes the plan after milestones | Builds WPs; merges worker PRs |
| Product manager (PM) | ChatGPT (Codex) | Keeps `docs/agents/BOARD.md` and the work queue, reviews every worker PR, merges, returns rework, audits each milestone, escalates | Rewrites requirements; marks a WP Done that failed review |
| Worker lead | DeepSeek in OpenCode, agent `qs-lead` | Runs a worker session: picks WPs, delegates to worker subagents, opens PRs, handles rework | Merges its own PRs; edits another WP's owned paths |
| Worker subagents | DeepSeek in OpenCode: `qs-engine`, `qs-ui`, `qs-verify`, `qs-numerics`, `qs-selfreview` | Build, test, verify and self-review under the lead | Open or merge PRs |

Credits: Peter and Claude keep their credits for the Lender app. Claude acts only at milestone acceptance, plan refreshes and when the PM escalates a requirement question. Everything else runs between the workers and the PM.

## 1. Non-negotiables

1. Build only WPs that exist in `PLAN.md` on `main` and are in the queue on `docs/agents/BOARD.md`. CI rejects a branch whose WP is not on `main`.
2. Change **only the WP's owned paths**, plus that WP's own `Status:` and `Change record:` lines in `PLAN.md`, its learning note, and new files in `docs/log/` and `docs/sources/entries/`. CI enforces this. Anything else needs a new WP. Channel messages (section 9) are the exception: they go straight to `main`.
3. **One worker session works one WP at a time.** Parallel work happens only in separate sessions, each in its own git worktree, on WPs of different tracks (PLAN.md section 7.1). Two sessions never share a worktree or a WP.
4. **Never change `contracts/`** outside a Contract Change WP. A Contract Change WP runs alone on its schemas: no other open PR may touch those schemas.
5. **Never guess engineering numbers.** Every number from a standard, datasheet, table or textbook carries its source (book id, edition, page, clause, table or equation) in a code comment and in `docs/sources/entries/`. If you cannot read the source, stop that step, record the gap as a diagnostic or a `TODO(source: ...)`, and tell the PM in the PR. A plausible value without a source is a defect.
6. **Private material stays private.** Textbooks, paid standards, the ETAP and PowerFactory studies and client data live only in the private repository `Pietrols/QE-References`. Read it to learn and to verify; never copy its text, tables, figures, worked-example data or survey paths into this public repository, PR descriptions, commit messages, issue comments or CI logs. Textbook fixtures are loaded at test time through `QE_REFERENCES` (PLAN.md section 7.4). Test output prints pass or fail and error magnitudes only.
7. **We do not copy, and we do not reinvent.** Write fresh code. Use established methods and the constants the private study notes record as defaults (PLAN.md section 2). Never paste or transliterate decompiled text, pseudocode or prototype code.
8. **Never import a GPL-licensed library** into our packages. GPL programs may only run as separate processes.
9. **No em dashes** (U+2014) anywhere: code, comments, docs, commits, PRs, reviews. Use commas, colons, hyphens or new sentences. CI checks files.
10. **Never loosen a test tolerance to make a test pass.** Explain the modelling difference in the PR and ask the PM.
11. **If you depart from a WP as written,** set the Changed design status before continuing and copy it into the WP's `Change record:`:
    `Status: [!] Changed design | due to <reason>, while original was <original>, as it was better for <benefit> | <agent> | <YYYY-MM-DD>`

### Commit authorship (Peter, 26 October 2026)

Every commit is authored and committed as the owner, whichever agent writes it:

```bash
git config user.name "Peter Kabamba"
git config user.email "178684704+Pietrols@users.noreply.github.com"
```

- Run both lines in the clone or worktree before the first commit of a session.
- After committing, check with `git log -1 --format='%an <%ae> | %cn <%ce>'`. If either is anything else, fix it before pushing: `git commit --amend --reset-author --no-edit`.
- An agent may name itself in one `Co-Authored-By:` line at the end of the commit message, for example `Co-Authored-By: DeepSeek V4.1 Flash (OpenCode) <noreply@opencode.ai>`. It is never the author or the committer.
- Why: GitHub counts a commit on Peter's contribution graph only when it is authored with an email on his account and reaches `main`.

## 2. Session start (every agent, every session)

1. `git fetch origin && git checkout main && git pull --ff-only`
2. Read this file, `PLAN.md` sections 0 to 7, `docs/agents/BOARD.md`, and every message in `docs/agents/messages/` newer than your last one.
3. Workers also update the private library clone (`git -C "$QE_REFERENCES" pull --ff-only`) and read `research/engineering-software/CURRENT.md` and `research/engineering-software/PHASE3-READING-MAP.md` there.
4. List your open PRs and their review state: `gh pr list --author "@me" --state open --json number,title,reviewDecision,headRefName`. Read every unresolved review comment and every open issue labelled `rework`.
5. Run `PYTHONPATH=tools uv run python -m check_plan --summary PLAN.md`.
6. Then: workers handle rework first (section 4), then the next WP from the queue. The PM reviews the open PRs (section 5).

## 3. The worker loop

The worker never waits for a review. It opens a PR, moves to the next WP, and returns to a PR only when review asks for changes.

### 3.1 Picking the next WP

Take the first WP in the board's queue for your track whose `Depends on` WPs are all merged. If none is free:

- **Stacking rule:** you may start a WP whose dependency is an open PR that has passed automatic review with no P0 or P1 findings. Branch from that PR's branch, say `Stacked on #<n>` in the PR description, and keep stacks to at most two levels. When the base merges, rebase onto `main` and force-push with `--force-with-lease`.
- Otherwise take the first free WP of another track, in a new worktree.
- If nothing at all is free, write a channel message to the PM listing what is blocked and why, and stop.

### 3.2 Building a WP

1. Create the branch from the latest `main` (or the stack base): `git switch -c wp-<id>-<short-name>`.
2. Read the reading-map entry for the WP and the sources it names. Write a short plan in pseudocode in your scratch notes before code (Peter's method: pseudocode first). Engine WPs keep that pseudocode in the learning note.
3. Work section by section. A **section** is one step of the WP's numbered list, or one acceptance bullet. For each section: write the tests first or alongside, write the code, run the section's tests, then commit with `[WP-<id>] <section>: <what changed>`. Push after every commit so work is never only local.
4. Numerical code is tested against a reference with recorded provenance (PLAN.md section 4.6). Use the benchmark harness for solver results.
5. Every result carries diagnostics, provenance and a calculation trace (D11).
6. Write the learning note named in the WP: for Peter, a student who wants the concept, the why and the equations, not only the code.
7. Run the self-review subagent `qs-selfreview` against the Code Review Rules (section 6). Fix what it finds.
8. Run every acceptance command of the WP and the full CI set locally:
   ```bash
   uv sync --all-packages --locked
   uv run python tools/ci/check_repository.py text
   uv run python tools/ci/check_repository.py references
   uv run python tools/ci/check_repository.py boundaries
   uv run ruff check --config tools/ci/ruff.toml .
   uv run pytest
   PYTHONPATH="tools:tools/check_plan" uv run python -m check_plan PLAN.md
   ```
   UI WPs also run `pnpm install --frozen-lockfile`, `pnpm --filter qe-web build`, `pnpm --filter qe-web test` and `pnpm --filter qe-web e2e`.
   With `QE_REFERENCES` set, run the private textbook tests too and note pass or fail (no numbers from books) in the PR.
9. Final commit: set the WP's status to `Status: [x] Done | implemented by DeepSeek (<model id>) | commit <last implementation sha> | <YYYY-MM-DD>` and add one `completed` log (section 8). The status reaches `main` only if the PM merges, so Done on `main` always means review passed and CI was green.
10. Open the PR with the template in section 3.3, then post the comment `@codex review` (it does nothing harmful if automatic review already ran).
11. Write one line in your session notes and go straight to the next WP.

### 3.3 PR template

Title: `[WP-<id>] <title from PLAN.md>`

```
## WP
WP-<id>, track <E|U|D|V>, milestone <M3.x>. Stacked on #<n> (or: based on main).

## What was built
Numbered list matching the WP's steps, each with the commit sha.

## Acceptance
Each acceptance bullet from PLAN.md, the exact command, and its output (trimmed to the result lines).

## Numerical evidence
Benchmark table: case, method, max |dV| pu, max d(angle) deg, max dP/dQ, iterations, status.
Private textbook checks: example ids and pass/fail only.

## Sources
Book id, edition and page, or standard clause, for every engineering number added. New entries in docs/sources/entries/.

## Gaps and questions for the PM
Anything not done, any Changed design, any source that could not be read.
```

### 3.4 Budget (OpenCode Go)

The OpenCode Go plan gives far more DeepSeek V4.1 Flash requests than V4 Pro requests (roughly 43,000 versus 1,050 per five hours, and 108,000 versus 2,600 per week, per OpenCode's documentation in November 2026). So:

- `qs-lead`, `qs-engine`, `qs-ui`, `qs-verify` and `qs-selfreview` run on `opencode-go/deepseek-v4.1-flash`.
- `qs-numerics` runs on `opencode-go/deepseek-v4-pro` and is called only for: deriving a numerical method before coding it, and debugging a numerical test that still fails after two honest attempts. Every call states the question in one paragraph.
- When an allowance runs out, the lead commits and pushes all work, writes a channel message with where it stopped, and ends the session.

## 4. Rework

Rework comes back three ways, and has priority over new WPs:

1. **Automatic Codex review findings (P0 or P1)** on the PR.
2. **Manager review** with "Request changes", numbered findings.
3. **Issues labelled `rework`** that the PM opens for problems found after merge or across PRs.

For each finding: fix it on the same branch in a commit `[WP-<id>] rework: <finding number or short title>`, reply to the comment with the commit sha and one sentence, and resolve the thread. A finding you disagree with gets a reply with evidence (a test, a source, a calculation); never silently ignore it. After all findings are handled, comment `@codex review` again and tell the PM in the PR: `Rework done for findings 1 to N`.

The PM may also comment `/oc <instruction>` on a PR. That starts the OpenCode GitHub action (section 7.3), which makes the change on the PR branch while Peter's PC is off. The worker treats those commits like its own.

## 5. The manager's review and merge

The PM reviews each worker PR after automatic review has run.

1. Check out the PR head on a clean environment. Rerun the acceptance commands and the CI set; do not trust pasted output.
2. Check the PR against the WP in `PLAN.md`: every numbered step built, every acceptance bullet evidenced, owned paths only, status and log correct.
3. Check numbers: references with provenance, tolerances unchanged, sources cited for every engineering number, and one value recomputed by hand or by an independent script for each numerical PR.
4. Check rules 5, 6 and 9 of section 1 and the Code Review Rules (section 6).
5. Decide:
   - **Merge** when everything passes and CI is green on the head commit. Use a merge commit. Then update the board.
   - **Fix small things directly** (typos, formatting, a missing source entry, under about 30 lines, nothing numerical) with a commit `[WP-<id>] pm: <fix>`, then merge.
   - **Request changes** with numbered findings, each stating file, line, expected and actual, and what evidence would close it.
   - **Escalate to the PO** (a channel message to Claude, `needs: answer`) when the WP itself is ambiguous or wrong. Escalate to Peter for scope, source purchases or licence questions.
6. Never merge with failing checks, never bypass branch protection, never merge a stack before its base.

At the end of each milestone the PM runs the milestone audit WP, and Claude, as PO, accepts the milestone against PLAN.md section 7 or returns numbered findings.

## Code Review Rules

This is section 6. Codex reads it for its automatic GitHub reviews. Workers' `qs-selfreview` applies it before every PR. Treat each item as P1 unless marked P0.

- **P0** Copyrighted or private material in this repository: text, tables or worked-example data from a textbook or standard, survey paths, decompiled code or pseudocode, in code, tests, docs, PR text or test output.
- **P0** An engineering number without a source (book, edition, page or clause) in a code comment and in `docs/sources/entries/`.
- **P0** A loosened tolerance, a skipped or deleted test without a stated reason, or a test that compares a result with itself.
- **P0** A change outside the WP's owned paths, or to `contracts/` outside a Contract Change WP.
- A numerical result returned as valid when the solver did not converge, or an exception reaching the user instead of a diagnostic naming the element and field.
- A result without provenance (engine, version, input hash) or without a calculation trace (D11).
- Per-unit, sign convention or tap-side handling that differs from `docs/learning/native-network-and-ybus.md` without a Changed design entry.
- Python loops over node pairs inside a numerical iteration where a vectorised or sparse form exists (engine-language consensus of 2026-11-01).
- An import between domain packages, an adapter imported by `native/`, or a GPL library imported.
- UI: a colour with a blue hue in theme tokens; information shown by colour alone; a dialog field without its unit; a control without an accessible name.
- Missing learning note, or a learning note without the equations.
- Any em dash.

## 7. Tooling setup

### 7.1 OpenCode on Peter's Windows PC (main worker runner)

This is where the heavy work runs: it can read both repositories with Peter's GitHub login, and nothing private reaches public logs.

1. Clones: `Quantic-Studio` at `C:\Users\hp\Documents\Quantic-Studio` (main worktree) and `QE-References` at `C:\Users\hp\Documents\QE-References`. Set the user environment variable `QE_REFERENCES` to the second path. Use `GIT_LFS_SKIP_SMUDGE=1` when cloning QE-References; fetch single PDFs only when a page must be checked.
2. Extra worktrees for parallel tracks: `git worktree add ..\QS-E main`, `..\QS-U`, `..\QS-V`. One OpenCode session per worktree.
3. `gh auth login` once, so `gh` can open PRs and comment as Peter's account. Comments the worker posts therefore come from Peter's account, which is why `@codex review` from the worker is honoured.
4. Start a session in a worktree with the lead agent: `opencode --agent qs-lead`, then the instruction: `Session start per AGENTS.md section 2, then run the worker loop of section 3 on track <E|U|D|V> until the queue is empty or the allowance runs out.`
5. Agent definitions are in `.opencode/agents/`. Project settings are in `opencode.json`.

### 7.2 Codex (manager)

1. In Codex settings, connect `Pietrols/Quantic-Studio` and turn on automatic code review for all PRs. Codex reads the `Code Review Rules` heading (section 6) for its review rules.
2. The manager review of section 5 runs as a Codex task. Peter starts it by telling ChatGPT "continue", or the worker starts it by commenting `@codex` with a request on a PR (a mention other than "review" starts a Codex task with the PR as context). WP-3.0 records which of these work in practice.

### 7.3 OpenCode GitHub action (rework while the PC is off)

Installed by Peter with `opencode github install` in this repository, which adds the `opencode-agent` GitHub app, the workflow `.github/workflows/opencode.yml` and the model API key secret. Settings:

- Model `opencode-go/deepseek-v4.1-flash`.
- Triggers: `issue_comment` and `pull_request_review_comment` containing `/oc` or `/opencode`, and a `schedule` every three hours with the prompt `Find open PRs with unresolved review findings from the manager or Codex and address them per AGENTS.md section 4.`
- The action **never checks out `QE-References`**. Logs of this public repository's Actions are public, and rule 6 forbids private material there. Rework that needs a private source waits for the PC session.
- Whether a Codex review comment can trigger `/oc` directly is tested in WP-3.0; the schedule is the fallback.

## 8. Log file format

Path: `docs/log/<YYYY-MM-DD>-<agent>-WP-<id>-<event>.md`, where `<agent>` is `DeepSeek`, `ChatGPT`, `Claude` or `Peter`.

```
wp: WP-<id>
model: <DeepSeek (<model id>) | ChatGPT | Claude | Peter>
event: completed | changed-design | audit | dispute | acceptance
commit: <short-sha or none>
date: <YYYY-MM-DD>
summary: <one or two sentences>
evidence: <commands run and results, or CI link>
```

Never edit or delete an existing log. Corrections are new files. Older logs with other events remain valid history.

## 9. Coordination channel

Agents talk in `docs/agents/`, so Peter only has to say "continue". `BOARD.md` holds the queue and is edited by the PM. Messages go in `docs/agents/messages/` as `YYYY-MM-DDTHHMMZ-<from>-<slug>.md` in UTC, never edited after pushing, committed straight to `main` with the title `[agents] <slug>`. Format and rules are in `docs/agents/README.md`. Workers write one message at the end of every session: WPs opened, rework done, where they stopped, what is blocked.

## 10. Engineering conduct

- Every result carries provenance (engine and version, input hash) and diagnostics.
- Invalid input produces a diagnostic that names the element and field, never an unexplained crash.
- Prefer clear code with equations cited in comments over clever code.
- When unsure, ask the PM in the PR rather than invent a requirement. The PM asks the PO; the PO asks Peter.
