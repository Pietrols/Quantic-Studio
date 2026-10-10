# ADR-0003: Four product suites, specialised engines, shared infrastructure

Status: Accepted direction (Peter, 2026-10-10). Detailed WPs follow when development resumes.
Context: Peter's alignment notes of 2026-10-10 and four reference documents (ETAP and PowerWorld; PLC, HMI and SCADA; Proteus, Simulink and Simscape; PVsyst and HelioScope). The references are study material, not blueprints. We do not clone products.

## 1. Decision

Quantic Studio's first four product suites:

| Suite | Scope | Primary engine(s) |
|---|---|---|
| 1. Power Systems | Load flow, short circuit, protection, motor starting, power quality, stability | Static network engine (exists: `qe_power`), later dynamic machine models |
| 2. Industrial Automation | IEC 61131-3 programs, scan-cycle execution, I/O, field devices, HMI, SCADA, alarms, history | PLC runtime plus a discrete-time process model |
| 3. Electronics, Control and Multiphysics | Schematics, SPICE-style circuits, microcontrollers, block diagrams, control, machines, physical networks | Several engines (see section 4) |
| 4. Solar PV | Solar geometry, weather data, irradiance, shading, layout, strings, inverters, losses, energy yield | Time-series PV engine (pvlib as foundation) |

Principle: **four suites, specialised engines, shared infrastructure.** Engines never import each other. They exchange data only through versioned contracts, as `qe_power` already does.

## 2. Scope check

The four suites are a sound initial scope for electrical and electronics engineering. Gaps to place deliberately, all inside Suite 1:

- **Harmonics and power quality** from VFDs and rectifiers. Very relevant to mining loads. Belongs in Suite 1, and later uses converter models from Suite 3.
- **Earthing and grounding design** (step and touch voltage). Substation work needs it. It depends on a paid standard (IEEE 80 or an IEC equivalent).
- **Arc flash** (IEEE 1584). A strong commercial need. Paid standard.
- **Cable sizing.** Already deferred: it needs IEC 60364-5-52 ampacity tables.

PCB layout (part of Proteus) should stay out of scope. KiCad already does it well; Suite 3 can export netlists to it instead of rebuilding a layout editor.

## 3. Shared infrastructure (build once, use in all four)

1. **Project format.** The project manifest is currently power-only (`network_file`, load-flow studies). It must become multi-domain: a project holds models of different kinds (power network, PLC program, PV site, circuit, block diagram) and their studies. This is a Contract Change, and it should land **before** the API (WP-1.5) and the web editor (WP-1.6) freeze around the power-only shape.
2. **Asset identity.** The same physical motor appears in Suites 1, 2 and 3 at different levels of detail: a network load, a controlled device, a dq-axis machine. Each asset gets one stable ID and a registry. Each suite stores its own representation, linked by that ID.
3. **Time and co-simulation.** Suites 2, 3 and 4 are time-stepped. Define one interface for coupling engines (initialise, step to t, exchange named signals with units). Model it on the open FMI standard (Functional Mock-up Interface) rather than inventing our own.
4. **Time series.** One shared format for hourly PV output, PLC trends, scope traces and load profiles. Suite 4's output feeds Suite 1's time-series load flows.
5. **Canvas.** Single-line diagrams, schematics, block diagrams and SCADA mimics are all graphs of nodes and ports. WP-1.6 must build a **generic diagram canvas** plus a power-specific symbol set, not an SLD-only editor. The ladder-logic editor is a grid, not a free graph, so it gets its own component.
6. **Already shared and working:** units, contracts, diagnostics, provenance, reports, the CLI, CI rules, the source register.

## 4. Suite 3: one application, separate engines

Recommendation: **one application shell with distinct workspaces, each backed by its own engine**, not one universal solver.

| Workspace | Engine type | Foundation to evaluate |
|---|---|---|
| Circuit (Proteus-like) | Modified nodal analysis, SPICE | ngspice (process boundary) |
| Microcontroller | Instruction-level emulation | simavr, Renode |
| Block diagram (Simulink-like) | Causal signal flow, ODE solvers | SciPy, our own scheduler |
| Physical networks (Simscape-like) | Acausal DAE | OpenModelica (process boundary), evaluate first |

The workspaces couple through the co-simulation interface in section 3. Acausal physical modelling is the hardest part of all four suites, and it comes last.

## 5. Build order

Peter's view that PLC is a manageable starting point is right on computation: a scan-cycle runtime is light and its correctness criteria are clear, since IEC 61131-3 defines the semantics. Suite 1 is already well under way, though, so it should finish its first usable slice first.

1. **Suite 1, Phase 1 (current):** WP-1.3 short circuit, WP-1.4 motor start. Then **new: multi-domain project contract and generic canvas**, then WP-1.5 API, WP-1.6 editor, WP-1.7 PDF.
2. **Suites 4 and 2 in parallel**, one agent each. They share no engine, so they never collide. PV is fast to deliver on pvlib and feeds Suite 1. PLC reuses the canvas and the time interface.
3. **Suite 3**, workspace by workspace: circuit, then block diagram, then microcontroller, then physical networks.
4. **Suite 1 depth:** protection coordination, harmonics, dynamics, plus arc flash and earthing once the standards are available.

## 6. Numerical accuracy

Problems found so far were all caught by cross-checks and fixed:

- the shunt model;
- the transformer loading convention;
- infeasible fixture setpoints;
- reactive limits.

Rules that continue for every engine:

- every numerical result needs an independent reference with recorded provenance: hand-derived, a published worked example, or a second solver;
- values from standards come only from the standard itself, cited by clause;
- converged or simulated does not mean feasible: reports check limits.

Before resuming, a short review of the ChatGPT-built WP-1.1 and WP-1.2 should confirm their references and contract versioning (`contracts/v0.1/` now holds the previous schema versions).
