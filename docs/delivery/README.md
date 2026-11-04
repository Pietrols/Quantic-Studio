# Power systems delivery, 4 November 2026

Peter is sponsor and final scope/release authority. Claude is product owner. ChatGPT is product manager and external reviewer. DeepSeek through OpenCode implements through a manager and specialist agents.

This package turns the existing research and PLAN into executable delivery instructions. It is not a claim that Phase 3 engines exist. Read in order:

1. `AGENTS.md`, live `PLAN.md`, `docs/agents/BOARD.md` and newer channel messages.
2. [Baseline and architecture](architecture.md).
3. [Delivery batches](batches.md).
4. [Integration work-package proposals](integration-packages.md).
5. [Workbench specification](workbench.md).
6. [Agent operations](agents.md).
7. [Review automation](review-automation.md).

## State at this checkpoint

Main inspected at d3454be, then coordination and WP-3.0 authorization added. All 28 Phase 3 WPs were Not started; 3 parked Phase 2 WPs remain. Existing code includes the pandapower adapter, dense teaching NR solver, project/API/report layers and React workbench. Native engine capacity is unmeasured.

The November 1 language consensus is retained. The November 3 private research captures for ETAP 16 and PowerFactory 15.1 were consulted. This is a design audit, not a re-execution of the private experiments. Exact private source paths and raw artifacts remain private. Public engineering requirements are original specifications linked to existing public R-IDs.

## Activation and first handoff

Merge WP-3.0 only after its checks and reciprocal review. Claude reconciles BOARD and approves task-level product acceptance within Peter's mandate. The first implementation campaign is B0: sparse core, independent harness and capability map. Each worker receives a bounded task contract. UI preparation can proceed independently; integration waits for approved contracts.

Keep one existing WP per PR while the current ownership checker applies. A large batch means uninterrupted execution of several coherent WPs with a checkpoint after each and a batch audit. Combining WPs into one PR requires an approved umbrella WP already present on main with the precise union of owned paths; do not disable CI to make a mega-PR pass.

OpenCode provider identity, installed CLI compatibility, Codex review settings and branch protection are activation checks, not verified capabilities of this commit. The supplied agent definitions do not start a daemon or wake this chat. Review requests are delegated GitHub tasks; see the runbook.

## Release meaning

Internal milestones are demonstration and validation gates within one product, not separate student editions or promises of partial commercial releases. Production deployment is a later explicit release decision, after engineering validation, install/restore tests and licence/source gates. No cloud hosting or desktop wrapper is selected by this planning change.
