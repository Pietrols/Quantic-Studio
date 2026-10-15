# Open-source engines we can build on (WP-2.10 working note)

Peter's ruling (2026-10-15): we recreate the commercial tools by building on existing
work, not by reinventing every engine. This note lists open engines that already cover
part of what ETAP and PowerFactory do, with their licences as stated by their own pages
(accessed 2026-10-15). Licences must be rechecked against the exact version before any
dependency is added (AGENTS.md rule 7: no GPL imports; GPL tools only as separate
processes).

| Project | Licence (as stated) | What it covers | How we could use it | Source |
|---|---|---|---|---|
| pandapower | BSD-3 (already our dependency) | Balanced AC NR load flow, IEC 60909 short circuit, OPF, estimation, time series, 3-phase load flow | Current power engine; extend | already in uv.lock |
| VeraGrid (formerly GridCal) | MPL-2.0 | NR, Levenberg-Marquardt, Iwamoto, fast decoupled, Gauss-Seidel, holomorphic embedding and linear load flow; AC/DC multi-grid; 3-phase unbalanced flow; continuation power flow; balanced and unbalanced short circuit; linear OPF and NTC optimisation; contingency with LODF; time series; RMS (positive sequence) and EMT (ABC) simulation; state estimation; GUI | Candidate second engine or reference for CPF, unbalanced flow, NTC; MPL permits use with file-level copyleft on modified MPL files | https://github.com/SanPen/GridCal |
| OpenDSS (EPRI) with DSS-Python | DSS-Python BSD-3; OpenDSS own licence (to read); KLUSolve and SuiteSparse LGPL-2.1 | Unbalanced distribution power flow, faults, harmonics, dynamics, load parameter variation, GIC, time series | Engine for unbalanced feeders and harmonics; separate process if licence requires | https://opendss.epri.com/AboutOpenDSSCapabilities.html, https://pypi.org/project/dss-python/ |
| PYPOWER (MATPOWER port) | BSD-3 (case files excluded) | DC and AC power flow (NR, fast decoupled), DC and AC OPF | Reference cases and OPF cross-check | https://pypi.org/project/PYPOWER/ |
| ANDES (CURENT) | GPL-3.0-or-later | NR power flow, implicit trapezoidal transient stability, eigenvalues, continuation power flow, estimation; 100+ dynamic models (GENROU, TGOV1, IEEEG1, HYGOV, REGCA1, REECA1, REPCA1, PVD1, ZIP loads) | Only as a separate process for cross-checking stability; never imported | https://pypi.org/project/andes |
| Dynawo (RTE) | MPL-2.0 | Hybrid C++ and Modelica dynamics for large grids with power electronics; models separate from solvers | Candidate RMS dynamics engine; Modelica models | https://opensource.rte-france.com/projects/dynawo |
| OpenIPSL | BSD-3 | Modelica library of phasor-domain power system models built to reproduce PSAT and PSS/E results; no solver | Model library for a Modelica-based dynamics engine | https://github.com/openipsl/openipsl |
| PyPSA | not yet confirmed (fetch blocked) | Energy system and network optimisation | Planning and unit commitment | to fetch |

Gaps without an obvious open engine (we will write our own, verified against the owned
books): ANSI C37 multiplying-factor duty, IEEE 1584 arc flash with clearing time
iteration, TCC protection coordination and sequence of operation, cable sizing and
Neher-McGrath/IEC 60287 ampacity (Anders 2005), IEEE 80 ground grid, IEEE 485 battery
sizing, motor starting with starters.
