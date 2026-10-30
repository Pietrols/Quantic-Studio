# AGENTS.md: Rules for every AI model working in this repository

These rules apply to every model and every session, whichever tool you run in. `PLAN.md` is the source of truth for what to build. This file is the source of truth for how to work.

## 1. Non-negotiables

1. Work on **one work package (WP) at a time**, and only one Peter has approved in `PLAN.md`.
2. Change **only the WP's owned paths**, plus that WP's own `Status:` and `Change record:` lines in `PLAN.md`, plus the learning note named in that WP's `Learning note:` field and new files in `docs/log/` and `docs/sources/entries/`. Anything else needs a new WP or Peter's explicit authorization. Channel messages (section 7) are the exception: they go straight to `main`, never inside a WP branch.
3. **The implementer completes its own WP.** Mark Done after all tests and acceptance commands pass and CI is green. There is no per-WP cross-verification. A different model performs one cross-audit at each milestone, first M0 in WP-0.10.
4. **Never change `contracts/`** outside a Contract Change WP (PLAN.md section 4.5).
5. **Never guess engineering numbers** from standards, datasheets or tables. If a value comes from a source you cannot read, stop and ask Peter, and record the gap as a diagnostic or a TODO that names the source and clause. A plausible value without a source is treated as a defect.
6. **Never commit copyrighted textbooks, paid standards or client data to this repository.** They live only in Peter's private reference repository `Pietrols/QE-References` (local copy `~/QE-References/`). Cloud and local agents may clone and read it: search its page-tagged text first, and fetch a PDF (Git LFS) only to check a specific page, table or figure. Use it only to verify formulas, constants and results, never to copy text, figures, tables or worked examples into this repository or anywhere public. Never make it public, add collaborators, fork it or link it publicly. Cite the source (book, edition, volume, page or clause) in a code comment and in `docs/sources/entries/`.
7. **Never import a GPL-licensed library** into our packages. GPL programs may only run as separate processes.
8. **No em dashes** (U+2014) anywhere: code, comments, docs, commit messages. Use commas, colons, hyphens or new sentences.
9. **If you depart from a WP as written,** set the Changed design status before continuing:
   `Status: [!] Changed design | due to <reason>, while original was <original>, as it was better for <benefit> | <model> | <YYYY-MM-DD>`
   and copy the same sentence into the WP's `Change record:`.


### Commit authorship (Peter, 26 October 2026)

Every commit is authored and committed as the owner, whichever model or person writes it:

```bash
git config user.name "Peter Kabamba"
git config user.email "178684704+Pietrols@users.noreply.github.com"
```

- Run both lines in the clone before the first commit of a session.
- After committing, check with `git log -1 --format='%an <%ae> | %cn <%ce>'`. If either name or email is anything else, fix it before pushing: `git commit --amend --reset-author --no-edit`.
- An AI model may name itself in one `Co-Authored-By:` line at the end of the commit message. It is never the author or the committer.
- Why: GitHub only counts a commit on Peter's contribution graph when it is authored with an email on his account and reaches `main`. The address above is his private GitHub address, so it counts without publishing his personal email.

## 2. Session-start review (mandatory, every session)

Do this before claiming or continuing any work:

1. `git fetch && git checkout main && git pull`
2. Read this file, `PLAN.md` sections 0 to 5, `docs/agents/BOARD.md` and every message in `docs/agents/messages/` newer than your last one.
3. Find your own most recent file in `docs/log/` and note its commit, which is your last checkpoint.
4. Review everything since that checkpoint:
   - `git log --oneline <checkpoint>..HEAD`
   - `git diff <checkpoint>..HEAD -- PLAN.md contracts/ AGENTS.md`
   - every new file in `docs/log/` since then
5. For every WP that became Done since your checkpoint: check its acceptance and CI evidence, and that any Changed design entry has all three clauses. Historical verifier fields remain valid records; new Done entries do not need a verifier. If something is wrong, write a `dispute` log file and tell Peter.
6. Run `PYTHONPATH=tools uv run python -m check_plan --summary PLAN.md` (WP-0.3 is Done and CI runs the same checker).
7. Only then claim or continue a WP.

## 3. Doing a WP

One WP is one branch, one pull request and one log file. Do not make separate commits or logs to reserve, start or record a WP. Peter assigns WPs in chat, and lanes own disjoint paths, so no reservation commit is needed.

1. Confirm that every WP in `Depends on` is Done.
2. Create branch `wp-<id>-<short-name>` from the latest `main`.
3. Build in commits whose messages start with `[WP-<id>]`. Keep the count small: implementation commits, then one final status commit.
4. Write tests first, or alongside the code. Numerical code must be tested against a reference with recorded provenance.
5. Write the learning note named in the WP, for Peter: explain the concept and the why, with the equations, not just the code.
6. Run every test and acceptance command locally.
7. In one final commit, set your WP to Done (citing your last implementation commit) and add a single `completed` log with the evidence.
8. Open the PR, titled `[WP-<id>] <title>`, with the acceptance commands and their output in the description.
9. Wait for CI on the PR head. If it fails, fix it in the same PR. Done reaches `main` only through a merge with green CI, so Done on `main` always means CI passed.
10. Merge your PR (with `gh`, or the connected GitHub app if `gh` is not signed in), pull main, and continue to the next approved WP without waiting for Peter. Respect dependencies and explicit stop points. Do not bypass failed checks or repository merge protections.

Use the In progress status only when a WP must pause across sessions or is blocked; then push it on the WP branch, not as a separate PR. Extra logs are only for `changed-design`, `dispute` and `audit` events.

## 4. Milestone cross-audit

1. A different model from the relevant implementer audits each milestone, first M0 in WP-0.10. This replaces per-WP cross-verification.
2. Check out the milestone on a clean environment and rerun its acceptance commands and the constituent WPs' relevant tests. Do not trust pasted output.
3. Read the diffs, check owned paths and the Definition of Done in PLAN.md section 4.6, and review sources, assumptions and numerical references.
4. Record findings in an `audit` log. Failures require a `dispute` log with exact commands, expected and actual results; resolve them before closing the milestone.
5. Preserve the independence of WP-0.7: its model must not read WP-0.6 implementation code. A model that implemented WP-0.6 must not implement WP-0.7.

## 5. Log file format

Path: `docs/log/<YYYY-MM-DD>-<model>-WP-<id>-<event>.md`

```
wp: WP-<id>
model: <Claude | ChatGPT | Peter>
event: completed | changed-design | audit | dispute
commit: <short-sha or none>
date: <YYYY-MM-DD>
summary: <one or two sentences>
evidence: <commands run and results, or CI link>
```

Never edit or delete an existing log file. Corrections are new files. Older logs with the events `start`, `progress`, `ready-for-review` and `verified` remain valid history; new work does not create them.

## 6. Engineering conduct

- Every result carries provenance (solver and version, input hash) and diagnostics.
- Invalid input produces a diagnostic that names the element and field, never an unexplained crash.
- Do not loosen a test tolerance to make a test pass. Document the modelling difference and ask Peter.
- Prefer clear code with equations cited in comments over clever code.
- When unsure, stop and ask Peter rather than invent a requirement.

## 7. Coordination channel between the models

Claude (cloud, main agent) and ChatGPT (co-agent) talk to each other in `docs/agents/`, so Peter only has to say "continue". The protocol is in `docs/agents/README.md`; the current assignments are in `docs/agents/BOARD.md`. Peter's instructions in chat override anything in the channel.
