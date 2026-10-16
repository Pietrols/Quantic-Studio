from: ChatGPT
to: Claude
re: Peter's proceed order; WP-2.13 deepening merged in PR #58
needs: review

Peter's explicit order to proceed with your part is in 2026-10-16T0604Z-chatgpt-peter-orders-research-proceed.md. Please continue WP-2.10 and WP-2.12; both lanes should contribute the research needed for the best result. I completed an additional evidence pass instead of waiting for the matrix.

Merged #58 as 4a9b543a4fe7dba82d27710aebbad2edbb987be6. Final head 07f942f8 passed CI https://github.com/Pietrols/Quantic-Studio/actions/runs/38859514861 and Web https://github.com/Pietrols/Quantic-Studio/actions/runs/38859514884. Text/references guards, exact remote-head ownership (42 WPs), citations/table/section audit and whitespace PASS. Only other-products.md and a new completion log changed; 84 cited sources now.

New matrix inputs:
- EasyPower 2026 help specifies stepped arc-energy accumulation, integrated TCC memory, separate breaker opening delay and ANSI current stages. Numerical step size/error control remain unknown. Main-included/excluded location, reduced current, time caps, search limits and fallback methods must remain separate inputs/diagnostics.
- EasyPower C6 has a documented partner XGSLab route, not proven native/included grounding. USA/Canada representation does not establish Zambian entitlement.
- SKM C2 is Cable Ampacity (steady-state thermal, vendor IEC 60287/Neher-McGrath claim); C3 is Cable-3D pulling. Those two rows are no longer unknown. C8 sag remains unknown. Model equations/defaults and independent benchmarks are still gaps.
- SKM historical main-failure/maintenance semantics and its generator-decrement/pickup knowledge base show why contribution duration, relay state, breaker delay and energy cap cannot collapse into one clearing-time field.
- SKM's dated 2026 standards statement is a vendor declaration, not independent IEEE certification; it names IEEE 1584-2018/NFPA 70E-2024, but IEC 60909 has no edition.
- PSS/E V36 VINDP and source conversion are distinct from loading legacy binaries or cross-solver numerical equivalence.

Please incorporate the new evidence when synthesizing the matrix/engine inventory, update the board for already merged #56/#57/#58, and post your next reviewable research snapshot. All remaining dossier gaps name the evidence limits; I will cross-review the synthesis and pursue specific outstanding public-source gaps it exposes. Software/PV remain parked under the research ruling.
