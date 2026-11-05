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
| 1 | Branch, document, two commits, PR with the template, `@codex review` comment | In progress | Branch `wp-3.0-workflow-dry-run`; first commit adds this file; a second commit records the PR and the trigger result |
| 2 | Codex automatic review runs, or the mention produces one | Pending | Recorded after the PR and mention exist |
| 3 | Manager requests one deliberate change | Pending | Needs ChatGPT as product manager |
| 4 | Worker fixes on the same branch; manager merges with green CI | Pending | Needs ChatGPT as product manager |
| 5 | On Peter's PC, record `opencode --version`, `opencode models` and `opencode agent list`, and confirm the agent model ids | Partial | Run on the GitHub Actions Linux runner, not Peter's PC |
| 6 | Record which triggers worked, latency of each step, and anything that needed Peter | Pending | Filled in as the loop runs |

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

## Step 1 observations

Filled in the second commit: branch, first and second commit shas, PR number, and the
time the `@codex review` comment was posted.

## Gaps for the PM

- Steps 2 to 4 need ChatGPT as product manager. They cannot run in a worker-only
  GitHub Actions session: the worker must not merge, and no Codex task is started by
  this run.
- Step 5 needs Peter's Windows PC. The runner observations above are a fallback, not
  the required PC record.
- This repository's channel rule puts messages on `main`, but a worker branch must not
  change `docs/agents/messages/`. If this session cannot push a message to `main`
  directly, the PM finds the session summary in the PR description instead.
