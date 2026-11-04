# DeepSeek/OpenCode operating model

## Accountability

| Role | Owns | Cannot self-approve |
| --- | --- | --- |
| Peter | Scope, budget, disputed engineering assumptions, release | Not delegated by an agent prompt |
| Claude, product owner | User outcomes, acceptance, BOARD, priority decisions within agreed scope | Numerical correctness without evidence |
| ChatGPT, product manager/reviewer | Delivery dependencies, architecture review, acceptance evidence and rework | Its own fixes without renewed independent checks |
| power-manager | Task contracts, worker coordination, integration, checkpoint, PR handoff | Final acceptance of its own campaign |
| engine-worker | Numerical/domain implementation in assigned paths | Reference expectations and engineering review |
| ui-worker | Workbench implementation and component tests | Independent user-journey acceptance |
| validation-worker | Independent fixtures, benchmark harness, reproduction | Vendor-equivalence claims from reconstructions |
| docs-worker | Requirement/source mapping, learning notes, release evidence | Unread source assertions |
| code-quality-reviewer | Correctness, boundaries, security, maintainability, regression risks | Edits to the implementation under review |
| engineering-reviewer | Units/bases, methods, controls, provenance and independent oracles | Reuse of implementation output as expected values |
| implementation-quality-reviewer | Actual acceptance journey, incomplete features, UI/report behavior | Passing a checklist from prose alone |

Use separate sessions for implementer and reviewer. DeepSeek reviewers provide role separation but not model diversity; Codex/ChatGPT and Claude provide external review. Do not describe different DeepSeek instances as independent models.

## Task contract

Manager supplies: task and WP ID; baseline commit; dependency PRs; goal; exact owned paths; interface/schema versions; sources and permitted evidence; acceptance commands; expected artifacts; forbidden scope; reviewer roles; stop conditions. Each worker returns changed paths, commit, tests actually executed, results, uncertainties and handoff notes. A worker may not expand its own scope or edit PLAN acceptance to fit its implementation.

For parallel edits use isolated git worktrees and branches, not multiple agents mutating the same checkout/index. OpenCode subagents may share the manager's directory: if isolated worktrees cannot be provided to those sessions, run editing tasks sequentially. Read-only analysis may run concurrently. The manager alone integrates and pushes. Generated code and contracts have one designated owner at a time.

## Session loop

1. Read current main, PLAN, AGENTS, BOARD and newer messages; check local changes before switching branches.
2. Verify dependencies, source access and exact approved paths. Freeze the task contract.
3. Select the configured DeepSeek model in OpenCode. Record actual provider/model and CLI version in the run manifest. Do not substitute an unverified model name or assume the Go subscription covers arbitrary API calls.
4. Build in logical commits with tests alongside. Checkpoint at task completion and before compaction: branch, SHA, commands, failures, next task. Long runs are bounded by accepted task scope, not a promise of endless background execution.
5. Integrate in the WP branch; rerun integration acceptance. Read-only reviewers inspect the final diff and independently reproduce relevant checks in a disposable environment.
6. Resolve findings; write the evidence manifest and PR. Request external review according to the runbook.
7. Continue only independent approved work while review is pending. On review arrival, triage and repair before extending affected dependencies.
8. Merge only with current-head checks and independent acceptance; record a completed log and update the board through Claude. Never force-push shared history to conceal findings.

## Finding protocol

Return `severity`, `requirement`, `path/line`, `reproduction`, `expected`, `actual`, `impact`, `requested_fix`, `verification`. Distinguish blocker, major and note. Missing method provenance, incorrect units and false success are blockers. Cosmetic preferences are notes unless they violate explicit UI acceptance. Report inspected scope and unexecuted checks even when no findings occur.

Small fixes may be made by ChatGPT in the same PR under Peter's mandate; the manager pauses conflicting edits. Nontrivial fixes return to the owning worker with a regression test. Every code push invalidates affected review evidence; re-review the changed behavior against the new SHA. A reviewer who fixes a defect becomes an implementer for that change.

## OpenCode files and activation

`AGENTS.md` is the shared repository instruction file. `.opencode/agents/*.md` defines selectable roles; a single `agent.md` would not configure multiple OpenCode agents. These files use documented Markdown frontmatter and intentionally omit a guessed provider/model identifier. Configure the actual available DeepSeek model on the host and verify each role's resolved model before paid work.

On Peter's host, run `opencode --version`, `opencode models`, and `opencode agent list`. Confirm all eight roles load, then perform one disposable read-only task and one worker task, checking permissions and model identity. No live OpenCode execution was performed in the planning environment. Current documentation: https://opencode.ai/docs/agents/ (checked 2026-11-04). Host v2.2.5 compatibility must be smoke-tested rather than assumed from newer documentation.

Review agents deny edit and shell tools to prevent accidental mutation. They can inspect sources and return commands for an independent validation session. The validation worker executes tests in a disposable worktree; reported shell execution must come from that session, never be attributed to a read-only reviewer. Permission patterns are convenience restrictions, not a security sandbox; isolate credentials and the filesystem at the runner level.

Worker prompts forbid merges, pushes and channel edits. Manager integration uses its existing host permissions; prompts do not confer GitHub authorization or install credentials. Do not put API keys in agent files. Private research remains outside the public checkout and cannot be uploaded in PR artifacts.
