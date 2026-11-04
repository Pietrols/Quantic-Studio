# Board

Edited only by the product manager (ChatGPT). This version is Claude's handover for plan v3. Updated: 2026-11-04.

**Status:** plan v3.0 is proposed in the PR "Plan v3: power suite game plan and agentic workflow". Until Peter merges it, no worker starts. After merge, the first item is WP-3.0 (workflow dry run), then the tracks below run in parallel.

Roles: Claude product owner, ChatGPT product manager, DeepSeek workers in OpenCode (`AGENTS.md` section 0).

## First worker batch: M3.0, M3.1, M3.U

Take the first WP in your track whose dependencies are merged (stacking rule: `AGENTS.md` section 3.1).

| Order | Track E (engines) | Track D (data, API) | Track U (workbench) | Track V (verification) |
| --- | --- | --- | --- | --- |
| 0 | | | | WP-3.0 dry run (all wait for it) |
| 1 | WP-3.1 core, Ybus | WP-3.4 CC-10 network v1 | WP-3.50 shell (after 3.5) | WP-3.3 family map |
| 2 | WP-3.13 topology, islands | WP-3.5 CC-11 diagram, study case | WP-3.51 diagram editor | WP-3.2 benchmarks (after 3.6) |
| 3 | WP-3.17 DC load flow | WP-3.6 migration | WP-3.52 dialogs | WP-3.19 worked examples |
| 4 | WP-3.10 Newton-Raphson | WP-3.7 result store | WP-3.53 Data Manager | WP-3.58 recorded demos |
| 5 | WP-3.11 GS and FD | WP-3.49 API v1 | WP-3.55 study case dialogs | |
| 6 | WP-3.12 controls | WP-3.14 CC-8 contingency contracts | WP-3.56 output window | |
| 7 | WP-3.18 report, registration | | WP-3.54 libraries | |
| 8 | WP-3.15 contingency | | WP-3.57 results on diagram | |

Audits by the PM, then acceptance by Claude: WP-3.16 (M3.1) and WP-3.59 (M3.U, also retires the old workbench).

Then: WP-3.60 (Claude) expands M3.2 onward after a research refresh.

## Parked

WP-2.5 PV slice (branch `wp-2.5-pv-yield`), WP-2.6 PLC slice, WP-2.30 research refresh (superseded by the research in the private library).

## Follow-ups carried from Phase 2 (each needs its own WP)

- CC-4 fix: a failed initialisation before a nonzero start cannot be serialized.
- Shared harness: inject unavailable handlers in tests/integration/test_phase2_routing.py.
- Validation speed: cache the schema registry in qe_core.validation.
