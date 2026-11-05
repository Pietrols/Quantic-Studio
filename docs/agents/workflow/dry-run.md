# Agentic workflow dry run

WP-3.0. Started 2026-11-05 by the DeepSeek worker in OpenCode, running in GitHub
Actions on a public repository. This is not Peter's Windows PC: the runner has no
`QE_REFERENCES`, cannot read the private library and cannot merge. Steps that need the
product manager, Codex or Peter's PC are recorded as pending, not as passed. The
purpose is to prove the delivery loop of `AGENTS.md` section 3 on a trivial change
before the engineering WPs depend on it.

## Step record

| Step | Requirement | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Branch, document, two commits, PR with the template, `@codex review` comment | Completed | Branch `wp-3.0-workflow-dry-run`; commit 0a94ab7 adds the first version and the second commit adds this record; PR #87; `@codex review` posted at 09:07 UTC |
| 2 | Codex automatic review runs, or the mention produces one | Failed in this environment | No automatic review appeared. The mention produced only a connector notice from `chatgpt-codex-connector`: "To use Codex here, create a Codex account and connect to github." Codex is not connected to this public repository for this run |
| 3 | Manager requests one deliberate change | Pending | Needs ChatGPT as product manager, after Codex is connected or the manager reviews directly |
| 4 | Worker fixes on the same branch; manager merges with green CI | Pending | Needs ChatGPT as product manager |
| 5 | On Peter's PC, record `opencode --version`, `opencode models` and `opencode agent list`, and confirm the agent model ids | Partial | Run on the GitHub Actions Linux runner, not Peter's PC |
| 6 | Record which triggers worked, latency of each step, and anything that needed Peter | Partial | PR creation and the issue comment both worked. Codex did not review. PR created and mention posted within about one minute; all later steps need the PM and Peter |

## Step 5 observations on the GitHub Actions runner

Commands and results observed on 2026-11-05 at about 09:07 UTC.

- `opencode --version`: `1.19.5`.
- `opencode models`: the host lists `opencode-go/deepseek-v4.1-flash` and
  `opencode-go/deepseek-v4-pro`.
- `opencode agent list`: the host loads `qs-lead` as primary and `qs-engine`,
  `qs-engineering-review`, `qs-numerics`, `qs-selfreview`, `qs-ui` and `qs-verify`
  as subagents, plus the built-in agents.
- The `model:` line of every file in `.opencode/agents/` matches a model the host
  lists: the lead, engine, UI, verify and both review agents use
  `opencode-go/deepseek-v4.1-flash`; the numerics agent uses
  `opencode-go/deepseek-v4-pro`.

Still needed on Peter's Windows PC: repeat the three commands there, confirm the same
agent list and resolve any host-specific model id difference. The plan assumes the
Windows runner is the main worker host; this run proves the Linux GitHub Actions host
also loads the agents.

## Step 1 and step 2 observations

- Branch `wp-3.0-workflow-dry-run` created from main at 82ee688.
- First commit 0a94ab7 adds this document. Second commit 32b9bfe adds this record.
- PR #87 opened at about 09:07 UTC.
- `@codex review` posted at 09:07 UTC.
- No automatic Codex review appeared. The mention produced one connector notice from
  `chatgpt-codex-connector` asking for a Codex account and GitHub connection. The
  fallback in `AGENTS.md` section 7.3, a Codex task started by the manager, is not
  available in a worker-only run.
- The local CI checks pass on the branch: `check_repository.py text`, `references` and
  `boundaries`; `ruff`; `pytest` (695 passed); `check_plan` with owned paths valid.

## Gaps for the PM

- Steps 2 to 4 need ChatGPT as product manager. They cannot run in a worker-only
  GitHub Actions session: the worker must not merge, and no Codex task is started by
  this run.
- Step 5 needs Peter's Windows PC. The runner observations above are a fallback, not
  the required PC record.
- This repository's channel rule puts messages on `main`, but a worker branch must not
  change `docs/agents/messages/`. If this session cannot push a message to `main`
  directly, the PM finds the session summary in the PR description instead.
