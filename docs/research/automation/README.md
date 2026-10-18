# Industrial automation reference-product research

WP-2.28, ChatGPT, 2026-10-18. Fourth-suite research, adapted from the
[power dossier rules](../power/README.md). Research only; builds remain parked.

Use public primary documentation and independently authored explanations. S means
documented for the named version/component, I an original inference or proposal,
U unresolved. U never means absent. Every product assertion cites a source ID
in [plc-products.md](plc-products.md), with URL, read scope and access date.
Separate engineering IDE, emulator, deployable runtime, HMI, SCADA and DCS.
Separate product support for an IEC language from conformance to a particular
IEC edition, vendor instruction semantics and actual target timing.

Do not reproduce vendor programs, protected routines, firmware, screenshots,
libraries, client configurations or paid standards. Numerical limits and timer
corner cases need readable, version-specific evidence. No engineering number
may be supplied from memory. No application or plant controller was operated.
Repository facts cite the inspected local files; inferred differences and
proposed experiments are not vendor benchmark results.

## Dossier template

```
## 1. Identity: versions, editions, IDE/runtime/emulator and licensing
## 2. Sources: ID, title/type, URL, read scope and retrieval date
## 3. Architecture: project, resource, task, program, variable and I/O model
## 4. Elements: languages, types, timers, counters, scan and state semantics
## 5. Studies: simulation, debugging, plant coupling and HMI/SCADA boundaries
## 6. Workflow: edit, build, transfer, execute, monitor, automate and exchange
## 7. User value: sourced evidence versus our assessment; plant adoption
## 8. Engines implied: original architecture, licences and current qe_plc gaps
## 9. Gaps: precise missing evidence and original unrun fixture proposals
```

GPL components are process-only candidates under AGENTS.md, never imports into
our packages. LGPL and permissive components still need release, dependency,
generated-code and redistribution review. An API or separate process does not
by itself establish licence compliance. No engine is selected by this research.

Copperbelt relevance needs a dated, named plant and subsystem source. A Zambia
marketing example, a supplier's global mining customer, a training syllabus or
a drive installation cannot establish a current PLC/SCADA installed base.
Where that evidence is unavailable, retain U and request an authorized asset
inventory rather than inventing a market-share claim.
