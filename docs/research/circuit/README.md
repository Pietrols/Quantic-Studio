# Circuit and control reference-product research

WP-2.27, ChatGPT, 2026-10-18. Third-suite research: circuits, signal/control
models, power electronics, embedded co-simulation and multiphysics. Adapted from
[power](../power/README.md) and [PV](../pv/README.md) research rules.

Public primary documentation only. Paraphrase; do not reproduce vendor projects,
figures, interfaces, model libraries, firmware or paid reference contents. S means
documented, I an original inference/proposal, U unresolved and never absent.
Every claim names a source ID with URL, scope and retrieval date. Numerical
constants, limits, tolerances and defaults need readable model-specific evidence.
No software installed, simulated, benchmarked or purchased in this WP.

Do not equate causal signal blocks, conserving physical connections, SPICE nets
and firmware peripherals. Separate simulation, control design, embedded code
generation, real-time execution and communication. Preserve software/model/data
rights independently; GPL/AGPL engines are process-only candidates under the
repository policy and need exact release/component review before use.

The shared platform supplies projects, identity, units, results and reports.
Circuit/control time scales and solver needs must be specified independently
from PV yield and power load flow. Cross-suite coupling requires explicit units,
time/step/event semantics and contract work; this research changes no contracts.

## Dossier template

```
## 1. Identity: version, editions, licensing and platform boundaries
## 2. Sources: ID, title/type, URL, read scope and access date
## 3. Architecture and data model: signals, physical networks, devices, state
## 4. Element catalogue: parameters, units, meanings and model fidelity
## 5. Studies and modules: methods, inputs/outputs, applicability and diagnostics
## 6. Workflow and interface: edit, simulate, inspect, automate and exchange
## 7. User value and complaints: actual evidence versus our evaluation
## 8. Engines implied: original split, open licences and owned-book leads
## 9. Gaps: exact evidence or access needed to close them
```

## Deliverables

- [simulink.md](simulink.md): MATLAB/Simulink and Simscape Electrical, including
  the R2026a removal of legacy Specialized Power Systems.
- [other-products.md](other-products.md): Proteus, LTspice, PLECS, PSIM, ngspice,
  Xcos and OpenModelica; all nine sections with a shared comparison and licence audit.

Original fixture proposals are not copied vendor examples and are not test passes.
No language syntax, editor resemblance or matching annual/steady output establishes
behavioral parity, hardware fidelity, EMC compliance or real-time guarantees.
