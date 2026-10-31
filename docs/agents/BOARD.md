# Board

Edited only by Claude. Updated: 2026-10-31.

**Phase 3, power suite build (Peter, 2026-10-31).** The research phase is closed. The live plan is `PLAN.md` v2.0; the old plan is archived in `docs/plan/PLAN-v1.md`. Method: learn from the private reference library (books, standards, and the ETAP static survey in `QE-References/etap-survey/`), write our own Python, use established and survey-observed constants as defaults, benchmark everything (PLAN.md section 2).

| Item | Lane A: Claude | Lane B: ChatGPT |
| --- | --- | --- |
| Now | Groundwork WP-3.1 native core, WP-3.2 benchmark harness and baseline, WP-3.3 family map | Continue the survey on Peter's PC (Peter's instruction). WP-2.30 optional |
| Next | Batch A: WP-3.10 to WP-3.15 (load flow, GS/FD, controls, topology, contingency) | Batch B: WP-3.20 to WP-3.25 (faults, IEC 60909, motor starting, harmonics, protection, arc flash), starts when WP-3.1 is Done |
| Then | Batch C: WP-3.30 to WP-3.34 (unbalanced, transient stability, OPF, voltage stability, planning) | Batch D: WP-3.40 to WP-3.43 (workbench, import, libraries, reports) |
| Audits | Claude audits batches B and D (WP-3.26, WP-3.44) | ChatGPT audits batches A and C (WP-3.16, WP-3.35) |
| Parked | WP-2.6 PLC slice | WP-2.5 PV slice (branch `wp-2.5-pv-yield`) |

Each model works through its batch without waiting, one WP per PR, and the other model audits the whole batch at the end.

Survey snapshot in QE-References: `etap-survey/` (journal, reports, pseudocode, prototype), with `etap-survey/WP-MAP.md` mapping each Phase 3 WP to the survey reports to read. Public files in this repository cite it only as "private study notes".

Follow-ups carried from Phase 2 (each needs its own WP):
- CC-4 fix: a failed initialisation before a nonzero start cannot be serialized.
- Shared harness: inject unavailable handlers in tests/integration/test_phase2_routing.py.
- Validation speed: cache the schema registry in qe_core.validation.
