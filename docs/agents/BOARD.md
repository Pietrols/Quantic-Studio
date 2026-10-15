# Board

Edited only by Claude. Updated: 2026-10-15.

Order from `PLAN.md` section 9 (revised 2026-10-14). Each row starts when its
dependencies are Done on main. Paths in the two lanes never overlap.

**Research phase (Peter, 2026-10-15): building paused.**

| Item | Lane A: Claude | Lane B: ChatGPT |
| --- | --- | --- |
| Done | | WP-2.11 PowerWorld research (PR #53, merged 9eed253; reviewed by Claude, accepted) |
| Now | WP-2.10 ETAP and PowerFactory research: **in progress** | Cross-review WP-2.10 branch, then WP-2.11 deepening pass (Peter authorized in chat 2026-10-15; see message 2026-10-15T1537Z) |
| Next | WP-2.12 parity matrix and engine inventory | Review WP-2.12 |
| Parked | WP-2.6 PLC slice (not started) | WP-2.5 PV slice (branch `wp-2.5-pv-yield`) |

Engine order after research is decided from the parity matrix.

Reviews: after each merge the other model reviews it (README rule 4).

Done so far in Phase 2: WP-2.0, 2.1, 2.3, 2.4 (ChatGPT); WP-2.8, 2.2, 2.9 (Claude).

Follow-ups after WP-2.7 (each needs its own WP):
- CC-4 fix: a failed initialisation before a nonzero start cannot be serialized
  (raised by ChatGPT, 2026-10-14). Not needed by either Phase 2 slice.
- Shared harness: inject unavailable handlers in tests/integration/test_phase2_routing.py
  instead of assuming both suites are unavailable (ChatGPT, 2026-10-15).
- Validation speed: cache the schema registry in qe_core.validation; keep every check
  (ChatGPT, 2026-10-15).
- Workbench redesign (Peter's feedback, 2026-10-15): white background, grey panels, nothing blue; blend of ETAP and PowerFactory usage. After the research. Until then, suite
  web work stays inside each suite's workspace folder.
