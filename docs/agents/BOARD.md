# Board

Edited only by Claude. Updated: 2026-10-15.

Order from `PLAN.md` section 9 (revised 2026-10-14). Each row starts when its
dependencies are Done on main. Paths in the two lanes never overlap.

| Step | Lane A: Claude | Lane B: ChatGPT | Notes |
| --- | --- | --- | --- |
| 1 | WP-2.2 CC-6 PLC contracts: **Done** (PR #48) | WP-2.3 time runner and `qe_pv` seed: **Done** (PR #50) | Disjoint paths. 2.3 consumes CC-4 only. |
| 2 | WP-2.9 PLC process engine on CC-6: **Done** (PR #49); waiting for 2.4 | WP-2.4 routing, report registry, workspace scaffolding: **merged (PR #51), finishing guard and lock in a follow-up PR** | 2.4 needs 2.2 and 2.3 Done. 2.9 touches `qe_plc` and `tests/fixtures/plc` only. |
| 3 | WP-2.6 PLC end-to-end slice | WP-2.5 PV end-to-end slice | Both need 2.4 Done. |
| 4 | WP-2.7 audit of the PV slice | WP-2.7 audit of the PLC slice | Then STOP for Peter. |

Reviews: after each merge the other model reviews it (README rule 4).

Done so far in Phase 2: WP-2.0 (ChatGPT), WP-2.1 (ChatGPT), WP-2.8 (Claude), WP-2.2 (Claude), WP-2.9 (Claude), WP-2.3 (ChatGPT).

Follow-ups after WP-2.7 (each needs its own WP):
- CC-4 fix: a failed initialisation before a nonzero start cannot be serialized
  (raised by ChatGPT, 2026-10-14). Not needed by either Phase 2 slice.
- Workbench redesign (Peter's feedback, 2026-10-15): after the engines. Until then, suite
  web work stays inside each suite's workspace folder.
