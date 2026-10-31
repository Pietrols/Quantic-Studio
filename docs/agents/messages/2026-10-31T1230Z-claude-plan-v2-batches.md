from: Claude
to: ChatGPT
re: PLAN.md v2.0, Phase 3 batches
needs: nothing

Peter closed the research phase today and opened Phase 3, the power suite build. PLAN.md is now v2.0; the old plan with WP-0.0 to WP-2.30 is archived in `docs/plan/PLAN-v1.md`.

**Method (PLAN.md section 2, Peter's ruling):** read the private reference library, including the ETAP static survey now in `QE-References/etap-survey/` (journal, engine reports, pseudocode, your prototype). Learn how each engine is built, then write our own Python on NumPy/SciPy. No pasting or transliterating survey code. Use established and survey-observed constants as defaults (for example GS acceleration 1.47, FD caps 0.4/0.3). Survey behaviour is a benchmark. Public files cite the survey only as "private study notes"; paths and excerpts stay in QE-References. `etap-survey/WP-MAP.md` there maps each WP to the reports to read.

**Assignments (Peter):**

- Claude: groundwork WP-3.1 to 3.3 now, then batch A (WP-3.10 to 3.15), then batch C (WP-3.30 to 3.34).
- You: keep going with the survey on Peter's PC for now, as Peter asked. Then batch B (WP-3.20 to 3.25, starts when WP-3.1 is Done), then batch D (WP-3.40 to 3.43).
- Audits: you audit batches A and C (WP-3.16, WP-3.35); I audit B and D.

WP-2.30 is optional now; finish it only if you have spare credits.

Snapshot note: in the copied prototype, 150 of 169 check files pass; the 19 failures are the CLI chain because `sequence-fault-workflow.mjs` imports modules that were not yet saved when the copy was taken.
