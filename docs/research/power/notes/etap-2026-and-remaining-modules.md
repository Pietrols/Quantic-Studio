# ETAP: remaining modules and the 2026 release (WP-2.10 working note)

Sources E84 to E91 (in `etap-sources.md`). These sources close most of the "still unread"
list in `etap.md` sec. 10, item 3. Everything below is paraphrased from public vendor pages.

## Modules read in this pass

**Transformer inrush [E84]**
- Approach: a phasor-based transient stability model, with inrush from magnetisation
  curve points and remnant flux.
- Cases covered: energisation, sympathetic inrush (single and multiple transformers),
  inrush on fault clearance, and out-of-phase synchronising.
- Also sizes pre-magnetising transformers.
- Outputs are plots. Purpose: voltage dip and relay misoperation.
- No standard is named.
- Quantic implication: a T1 add-on, a saturable transformer model in RMS (approximate)
  or EMT (T4).

**Control system diagram (CSD) [E85]**
- Simulates the AC and DC control circuit sequence of operation:
  - relays, coils, solenoids, contacts, macro contacts, fuses, wires;
  - pickup and dropout voltage checks, inrush and burden modes;
  - temperature-adjusted coil resistance;
  - battery discharge through the sequence.
- Outputs: an action log, voltage drops, and alerts for pickup or dropout violations.
- Quantic implication: this overlaps with the PLC suite. A control circuit is a small DC
  network plus discrete logic. It is a natural bridge between Quantic's PLC engine (CC-6)
  and the DC network solver (`engine-dc-short-circuit.md`). It is a differentiator if
  joined with real ladder logic.

**Optimal capacitor placement [E86]**
- Objectives: voltage support, power factor, or both.
- Costs: installation and operation, plus savings over a planning period at an interest
  rate.
- Locations: global or per-location constraints, with user-chosen candidate locations.
- Loading: minimum, maximum and average loading categories.
- Networks: radial or meshed, balanced.
- The algorithm is not described, though the page claims a "global optimal" result.
- Compare with Das02 sec. 14.3.3 (`engine-load-flow-extensions.md` sec. 5).

**Motor parameter estimation [E87, ETAP 5.5 era]**
- Inputs: LRC, LR power factor, LRT, maximum torque, full-load slip, PF and efficiency,
  plus nameplate data.
- Model: a single-cage circuit.
- Solver settings: precision (default 2%) and acceleration factor (default 0.25). This
  implies an iterative fixed-point or Gauss-type solver.
- Estimation may fail on inconsistent data.
- The 2026 release adds "MotorPro", graphical parameter estimation and starting [E91].
- Quantic implication: matches `engine-motors.md` sec. 6. Least squares with a residual
  report per datasheet point is a strict improvement over "may fail".

**Distribution network optimisation [E88]**
- Modules: OPF, switching optimisation (tie points, multi-objective), capacitor placement,
  and Volt/VAR optimisation (taps, regulators, capacitors, inverters).
- Methods are not stated.

**Wind turbine generators [E89]**
- Types 1 to 4.
- Generic models: IEC 61400-27-1 4A and 4B, and WECC types 1 to 4; vendor models via UDM.
- Short circuit per IEC 60909-2016, with crowbar and current-limit models.
- LVRT auto-trip; wind ramp, gust and noise profiles; collector protection; grid
  compliance.
- Quantic implication: the IBR gap in `engine-transient-stability.md` sec. 9 now has
  names: IEC 61400-27-1 and the WECC generic models.

**eTraX traction [E90]**
- Modules: train performance calculator, traction unified power flow (time-varying train
  demand on AC and DC, single- and three-phase), unbalanced short circuit including
  simultaneous faults, protection, ground grid, harmonics, energy efficiency.
- Touch voltage and stray current are not mentioned on the page.
- Mining relevance: trolley-assist haul trucks and underground rail haulage are traction
  systems, so a smaller "mine traction" scope could be a Quantic niche.

## ETAP 2026 release series [E91]

Releases: 2026 Beta (2025-12-09), 2026 Commercial (2026-05-07), and 2026.0.1
(2026-10-08). The page does not map features to versions.

| Area | New or notable items |
| --- | --- |
| Studies | StarZ stepped-event analysis (multi-stage short circuit and coordination in meshed systems); capacitor energy discharge (NFPA 70E); unbalanced transient stability; unbalanced short circuit with generator breaker duty to IEC/IEEE 62271-37-013-2021; time-series load flow analyzer (statistics, violations); MotorPro; transformer load capability (IEEE C57.91); network reduction and aggregation; frequency response estimation (Bode plots from time-domain runs); underground raceway FEM ampacity, including subsea |
| Hosting capacity | New constraints: branch current THD, bus voltage THD, harmonic library and PV array rules, bus bracing, device interrupting rating |
| Microgrid controller | Rule-based and optimal dispatch, grid-connected and islanded control, automatic and user-defined black start, soft energisation of BESS |
| Digital twin elements | Mixed one- and three-phase loads, high-leg and corner-grounded delta, control power transformers, PV MPPT control, per-phase lumped loads; 5,000+ new PV array models |
| Grid code | Voltage and frequency ride-through at POI and IBR terminals, with EMT co-simulation (eMTCoSim) |
| Protection | StarZ distance for all unbalanced fault types; vendor-specific differential relays; CT saturation plots and Excel export; generator breaker category; LV breaker slash and individual-pole ratings; ZSI; AFAS fault classification and relay setting assistance via Python |
| Cables | BS 7671, IEC 60364 and NF C15-100 neutral and PE sizing; K²S² energy check per conductor against device let-through |
| Automation | etapPy (remote and parallel runs, automation of switching optimisation, unbalanced short circuit, contingency); etapAPI (REST over HTTPS to DataHub, Python client) |
| Interface | Network Manager tabular editing (editing still limited in 2026); Data Manager across revisions; Report Manager with comparison and Excel; sequence-of-operation slider; TCC improvements; iSLD result animation; high-DPI support |

## What this means for Quantic

1. **ETAP is moving to REST and Python automation (etapAPI, etapPy).** Quantic already
   has a CLI and REST API with JSON contracts (matrix D14), so this is parity, not an
   advantage. Our advantage must be openness (documented contracts, no licence server)
   and the worked trace (G13).
2. **Tabular editing arrived only in 2026, and with limits.** Peter's "forms plus JSON"
   customisability goal matches a direction ETAP itself is still finishing.
3. **Unbalanced transient stability and stepped-event short circuit are new in 2026.**
   Our phase-coordinate plan (`engine-load-flow-extensions.md` sec. 3) should be designed
   so these come naturally.
4. **Capacitor discharge (NFPA 70E) and transformer load capability (C57.91)** are small,
   well-defined calculators. They are cheap wins for a mining services company.
5. **Arc flash with decaying sources** is already in ETAP (dossier E13 and E14), so Das21's
   2021 "no commercial software" claim is out of date. `engine-arc-flash.md` sec. 4 is
   corrected.
