# AGENTS.md: Rules for every AI model working in this repository

These rules apply to every model and every session, whichever tool you run in. `PLAN.md` is the source of truth for what to build. This file is the source of truth for how to work.

## 1. Non-negotiables

1. Work on **one work package (WP) at a time**, and only one Peter has approved in `PLAN.md`.
2. Change **only the WP's owned paths**, plus that WP's own `Status:` and `Change record:` lines in `PLAN.md`, plus new files in `docs/log/` and `docs/sources/entries/`. Anything else needs a new WP.
3. **Never verify your own work.** Done requires a verifier from another lane, or Peter.
4. **Never change `contracts/`** outside a Contract Change WP (PLAN.md section 4.5).
5. **Never guess engineering numbers** from standards, datasheets or tables. If a value comes from a source you cannot read, stop and ask Peter, and record the gap as a diagnostic or a TODO that names the source and clause. A plausible value without a source is treated as a defect.
6. **Never commit copyrighted textbooks, paid standards or client data.** Peter keeps them in a reference library outside the repo (`~/QE-References/`). Use it only to verify formulas, constants and results, never to copy text, figures, tables or worked examples. Cite the source (book, edition, volume, page or clause) in a code comment and in `docs/sources/entries/`.
7. **Never import a GPL-licensed library** into our packages. GPL programs may only run as separate processes.
8. **No em dashes** (U+2014) anywhere: code, comments, docs, commit messages. Use commas, colons, hyphens or new sentences.
9. **If you depart from a WP as written,** set the Changed design status before continuing:
   `Status: [!] Changed design | due to <reason>, while original was <original>, as it was better for <benefit> | <model> | <YYYY-MM-DD>`
   and copy the same sentence into the WP's `Change record:`.

## 2. Session-start review (mandatory, every session)

Do this before claiming or continuing any work:

1. `git fetch && git checkout main && git pull`
2. Read this file and `PLAN.md` sections 0 to 5.
3. Find your own most recent file in `docs/log/` and note its commit, which is your last checkpoint.
4. Review everything since that checkpoint:
   - `git log --oneline <checkpoint>..HEAD`
   - `git diff <checkpoint>..HEAD -- PLAN.md contracts/ AGENTS.md`
   - every new file in `docs/log/` since then
5. For every WP that became Done since your checkpoint: check that the verifier differs from the implementer, and that any Changed design entry has all three clauses. If something is wrong, write a `dispute` log file and tell Peter.
6. Run `uv run python -m check_plan --summary PLAN.md` once it exists (WP-0.3) and confirm it passes.
7. Only then claim or continue a WP.

## 3. Doing a WP

1. Confirm that every WP in `Depends on` is Done.
2. Create branch `wp-<id>-<short-name>` from the latest `main`.
3. Set your WP to In progress and add a `start` log file. Commit this first.
4. Build in small commits whose messages start with `[WP-<id>]`.
5. Write tests first, or alongside the code. Numerical code must be tested against a reference with recorded provenance.
6. Write the learning note named in the WP, for Peter: explain the concept and the why, with the equations, not just the code.
7. Run every acceptance command and paste the output into the pull request.
8. Add a `ready-for-review` log file and open the PR, titled `[WP-<id>] <title>`.

## 4. Verifying a WP

1. Check out the PR branch on a clean environment.
2. Re-run every acceptance command yourself. Do not trust pasted output.
3. Read the full diff. Confirm that only owned paths changed (`tools/check_plan` automates this from WP-0.3).
4. Check the Definition of Done in `PLAN.md` section 4.6.
5. If everything passes: set the status to Done with your name as verifier, add a `verified` log file and approve the PR.
6. If anything fails: add a `dispute` log file stating the exact command, the expected result and the actual result. Leave the status unchanged.

## 5. Log file format

Path: `docs/log/<YYYY-MM-DD>-<model>-WP-<id>-<event>.md`

```
wp: WP-<id>
model: <Claude | ChatGPT | Peter>
event: start | progress | changed-design | ready-for-review | verified | dispute
commit: <short-sha or none>
date: <YYYY-MM-DD>
summary: <one or two sentences>
evidence: <commands run and results, or CI link>
```

Never edit or delete an existing log file. Corrections are new files.

## 6. Engineering conduct

- Every result carries provenance (solver and version, input hash) and diagnostics.
- Invalid input produces a diagnostic that names the element and field, never an unexplained crash.
- Do not loosen a test tolerance to make a test pass. Document the modelling difference and ask Peter.
- Prefer clear code with equations cited in comments over clever code.
- When unsure, stop and ask Peter rather than invent a requirement.
