# Engines versus Peter's library: first map (WP-2.10 working note)

Method: each topic was searched (case-insensitive regular expression) through the
page-tagged text of every book in `Pietrols/QE-References`. Hit counts and the first
printed page found indicate coverage depth only. Exact chapters are to be confirmed when
each engine is built. Raw output, run 2026-10-15:

```
Newton-Raphson load flow: glover-2017-power-system-analysis-design (74 hits, first printed p. vii); pillage-1995-circuit-system-simulation (45 hits, first printed p. viii); vlach-1983-computer-methods-circuits (39 hits, first printed p. xxi); grainger-1994-power-system-analysis (33 hits, first printed p. xiii); kundur-1994-power-system-stability (15 hits, first printed p. ?)
Gauss-Seidel: glover-2017-power-system-analysis-design (70 hits, first printed p. vii); najm-2010-circuit-simulation (20 hits, first printed p. viii); grainger-1994-power-system-analysis (19 hits, first printed p. xiii); chen-2004-electrical-engineering-handbook (14 hits, first printed p. 766); kundur-1994-power-system-stability (8 hits, first printed p. ?)
Fast decoupled: chen-2004-electrical-engineering-handbook (12 hits, first printed p. 766); glover-2017-power-system-analysis-design (11 hits, first printed p. vii); kundur-1994-power-system-stability (7 hits, first printed p. ?); das-2002-power-system-analysis (7 hits, first printed p. ?)
Unbalanced/three-phase load flow: 
Continuation power flow / PV curve: sauer-2006-power-system-dynamics (6 hits, first printed p. 211)
Optimal power flow: das-2002-power-system-analysis (18 hits, first printed p. ?); glover-2017-power-system-analysis-design (13 hits, first printed p. vii)
Economic dispatch: glover-2017-power-system-analysis-design (66 hits, first printed p. vii); grainger-1994-power-system-analysis (42 hits, first printed p. xiv); chen-2004-electrical-engineering-handbook (9 hits, first printed p. ?); shaik-2020-power-systems-analysis-notes (6 hits, first printed p. 1); kundur-1994-power-system-stability (4 hits, first printed p. 616)
Unit commitment: grainger-1994-power-system-analysis (36 hits, first printed p. xiv); das-2002-power-system-analysis (4 hits, first printed p. ?)
State estimation: grainger-1994-power-system-analysis (46 hits, first printed p. ?); chen-2004-electrical-engineering-handbook (20 hits, first printed p. vii); arrillaga-2003-power-system-harmonics (17 hits, first printed p. x); franklin-1998-digital-control (5 hits, first printed p. 324); bose-2002-power-electronics-ac-drives (5 hits, first printed p. 396)
Contingency analysis: grainger-1994-power-system-analysis (33 hits, first printed p. ?); glover-2017-power-system-analysis-design (8 hits, first printed p. xii)
Distribution factors PTDF/LODF: grainger-1994-power-system-analysis (46 hits, first printed p. 592); theraja-2005-electrical-technology (7 hits, first printed p. 1413); alstom-2011-network-protection-automation-guide (6 hits, first printed p. 4-10); arrillaga-2003-power-system-harmonics (5 hits, first printed p. 68); blackburn-2006-protective-relaying (4 hits, first printed p. ?)
Symmetrical components: grainger-1994-power-system-analysis (94 hits, first printed p. xiv); glover-2017-power-system-analysis-design (72 hits, first printed p. viii); gonen-1988-transmission-engineering (68 hits, first printed p. X); das-2002-power-system-analysis (34 hits, first printed p. ?); theraja-2005-electrical-technology (31 hits, first printed p. ?)
IEC 60909: kasikci-2002-short-circuits (6 hits, first printed p. ?); das-2010-transients (6 hits, first printed p. 233); das-2002-power-system-analysis (4 hits, first printed p. ?); schneider-2022-mv-technical-guide (3 hits, first printed p. 66)
ANSI C37 short circuit: das-2002-power-system-analysis (7 hits, first printed p. ?); das-2021-arc-flash (6 hits, first printed p. ?); das-2010-transients (3 hits, first printed p. 233); blackburn-2006-protective-relaying (3 hits, first printed p. ?)
Transient stability: kundur-1994-power-system-stability (238 hits, first printed p. XIV); glover-2017-power-system-analysis-design (103 hits, first printed p. ix); das-2010-transients (39 hits, first printed p. vii); grainger-1994-power-system-analysis (21 hits, first printed p. ?); sauer-2006-power-system-dynamics (19 hits, first printed p. 153)
Swing equation: glover-2017-power-system-analysis-design (47 hits, first printed p. ix); grainger-1994-power-system-analysis (39 hits, first printed p. ?); kundur-1994-power-system-stability (18 hits, first printed p. ?); das-2010-transients (13 hits, first printed p. vii); sauer-2006-power-system-dynamics (8 hits, first printed p. 105)
Small signal / eigenvalue: kundur-1994-power-system-stability (454 hits, first printed p. ?); kreyszig-2011-advanced-engineering-mathematics (442 hits, first printed p. viii); sedra-2004-microelectronic-circuits (365 hits, first printed p. ?); astrom-2008-feedback-systems (196 hits, first printed p. xi); sauer-2006-power-system-dynamics (150 hits, first printed p. vii)
Excitation systems / AVR: kundur-1994-power-system-stability (331 hits, first printed p. ?); das-2010-transients (106 hits, first printed p. vii); das-2002-power-system-analysis (16 hits, first printed p. ?); sauer-2006-power-system-dynamics (12 hits, first printed p. 71); fitzgerald-2003-electric-machinery (12 hits, first printed p. 246)
Governor: kundur-1994-power-system-stability (227 hits, first printed p. ?); glover-2017-power-system-analysis-design (112 hits, first printed p. ix); sauer-2006-power-system-dynamics (27 hits, first printed p. vi); astrom-2008-feedback-systems (20 hits, first printed p. 2); grainger-1994-power-system-analysis (12 hits, first printed p. 562)
Power system stabilizer: kundur-1994-power-system-stability (41 hits, first printed p. ?); das-2010-transients (28 hits, first printed p. viii); sauer-2006-power-system-dynamics (25 hits, first printed p. vii)
Induction motor starting: alstom-2011-network-protection-automation-guide (24 hits, first printed p. 5-14); das-2021-arc-flash (15 hits, first printed p. 97); das-2010-transients (15 hits, first printed p. 143); morley-ic9258-mine-power-systems (14 hits, first printed p. ?); glover-2017-power-system-analysis-design (9 hits, first printed p. 672)
Harmonic analysis: arrillaga-2003-power-system-harmonics (71 hits, first printed p. ?); das-2002-power-system-analysis (19 hits, first printed p. ?); masters-2004-renewable-efficient-power (6 hits, first printed p. 87); das-2010-transients (4 hits, first printed p. 127); theraja-2005-electrical-technology (3 hits, first printed p. ?)
IEEE 519: arrillaga-2003-power-system-harmonics (6 hits, first printed p. 8); das-2010-transients (5 hits, first printed p. 130)
Harmonic filter: das-2010-transients (17 hits, first printed p. 131); bose-2002-power-electronics-ac-drives (11 hits, first printed p. ?); mohan-1995-power-electronics (8 hits, first printed p. 468); kundur-1994-power-system-stability (5 hits, first printed p. 468)
Electromagnetic transients: das-2010-transients (177 hits, first printed p. ?); mohan-1995-power-electronics (24 hits, first printed p. 67); arrillaga-2003-power-system-harmonics (24 hits, first printed p. x); sauer-2006-power-system-dynamics (20 hits, first printed p. v); das-2002-power-system-analysis (15 hits, first printed p. ?)
Travelling waves: das-2010-transients (42 hits, first printed p. 1); gonen-1988-transmission-engineering (31 hits, first printed p. ?); glover-2017-power-system-analysis-design (28 hits, first printed p. x); morley-ic9258-mine-power-systems (16 hits, first printed p. ?); das-2002-power-system-analysis (15 hits, first printed p. ?)
Insulation coordination: das-2010-transients (67 hits, first printed p. viii); gonen-1988-transmission-engineering (44 hits, first printed p. X); glover-2017-power-system-analysis-design (12 hits, first printed p. x)
Arc flash: das-2021-arc-flash (756 hits, first printed p. ?); inshaw-2004-arc-flash-paper (67 hits, first printed p. ?); das-2010-transients (3 hits, first printed p. 1)
IEEE 1584: das-2021-arc-flash (37 hits, first printed p. v); inshaw-2004-arc-flash-paper (10 hits, first printed p. ?)
Overcurrent relay coordination: kasikci-2002-short-circuits (21 hits, first printed p. VI); morley-ic9258-mine-power-systems (18 hits, first printed p. ?); glover-2017-power-system-analysis-design (17 hits, first printed p. 457); das-2021-arc-flash (14 hits, first printed p. ?); das-2002-power-system-analysis (9 hits, first printed p. ?)
Distance protection: alstom-2011-network-protection-automation-guide (229 hits, first printed p. iii); blackburn-2006-protective-relaying (91 hits, first printed p. ?); kundur-1994-power-system-stability (29 hits, first printed p. ?); chen-2004-electrical-engineering-handbook (24 hits, first printed p. ?); glover-2017-power-system-analysis-design (5 hits, first printed p. 639)
Differential protection: das-2021-arc-flash (138 hits, first printed p. xi); alstom-2011-network-protection-automation-guide (132 hits, first printed p. 2-6); blackburn-2006-protective-relaying (118 hits, first printed p. ?); glover-2017-power-system-analysis-design (53 hits, first printed p. ix); morley-ic9258-mine-power-systems (16 hits, first printed p. ?)
CT saturation: das-2021-arc-flash (34 hits, first printed p. xi); alstom-2011-network-protection-automation-guide (10 hits, first printed p. 10-6); blackburn-2006-protective-relaying (6 hits, first printed p. ?); glover-2017-power-system-analysis-design (4 hits, first printed p. 619); morley-ic9258-mine-power-systems (3 hits, first printed p. ?)
Cable ampacity / Neher-McGrath: anders-2005-cable-rating (223 hits, first printed p. vi); morley-ic9258-mine-power-systems (46 hits, first printed p. ?); das-2021-arc-flash (17 hits, first printed p. ?); gonen-1988-transmission-engineering (8 hits, first printed p. 139); masters-2004-renewable-efficient-power (5 hits, first printed p. 150)
IEC 60287: anders-2005-cable-rating (30 hits, first printed p. xiii)
Ground grid IEEE 80: das-2010-transients (55 hits, first printed p. 3); morley-ic9258-mine-power-systems (20 hits, first printed p. ?); das-2021-arc-flash (9 hits, first printed p. ?); neamen-2012-semiconductor-physics-devices (8 hits, first printed p. iv); das-2002-power-system-analysis (3 hits, first printed p. ?)
Reliability indices SAIFI: glover-2017-power-system-analysis-design (20 hits, first printed p. 907); worldbank-2022-mini-grids (14 hits, first printed p. xxiii)
Voltage stability: kundur-1994-power-system-stability (177 hits, first printed p. ?); das-2010-transients (21 hits, first printed p. vii); sauer-2006-power-system-dynamics (8 hits, first printed p. 207); das-2002-power-system-analysis (4 hits, first printed p. ?); glover-2017-power-system-analysis-design (3 hits, first printed p. 242)
Line parameters / Carson: arrillaga-2003-power-system-harmonics (14 hits, first printed p. 174); das-2010-transients (11 hits, first printed p. xi); das-2002-power-system-analysis (6 hits, first printed p. ?); glover-2017-power-system-analysis-design (4 hits, first printed p. 197); chen-2004-electrical-engineering-handbook (4 hits, first printed p. 387)
Transformer modelling taps: kundur-1994-power-system-stability (89 hits, first printed p. ?); glover-2017-power-system-analysis-design (24 hits, first printed p. 133); das-2002-power-system-analysis (22 hits, first printed p. ?); alstom-2011-network-protection-automation-guide (22 hits, first printed p. 10-6); grainger-1994-power-system-analysis (17 hits, first printed p. XI)
HVDC: kundur-1994-power-system-stability (207 hits, first printed p. ?); glover-2017-power-system-analysis-design (155 hits, first printed p. vii); das-2010-transients (111 hits, first printed p. x); mohan-1995-power-electronics (22 hits, first printed p. ?); gonen-1988-transmission-engineering (22 hits, first printed p. 6)
FACTS / SVC / STATCOM: das-2010-transients (32 hits, first printed p. viii); rashid-2014-power-electronics (22 hits, first printed p. 12); kundur-1994-power-system-stability (22 hits, first printed p. ?); bose-2002-power-electronics-ac-drives (18 hits, first printed p. ?); das-2002-power-system-analysis (9 hits, first printed p. ?)
Battery sizing IEEE 485: 
DC short circuit IEC 61660: 
Load models ZIP: sauer-2006-power-system-dynamics (31 hits, first printed p. 131); kundur-1994-power-system-stability (14 hits, first printed p. 37); das-2002-power-system-analysis (13 hits, first printed p. ?); gonen-1988-transmission-engineering (7 hits, first printed p. 48); das-2010-transients (5 hits, first printed p. 299)
```

## Reading of the map

| Engine area (from ETAP and PowerFactory) | Strongest owned books | Coverage |
|---|---|---|
| Balanced load flow (NR, GS, fast decoupled) | Glover 2017, Grainger 1994, Das 2002, Chen 2004 | strong |
| Unbalanced phase-frame load flow, line constants (Carson) | Arrillaga 2003 and Das 2010 touch Carson; no dedicated distribution text | **gap** |
| Continuation power flow, P-V and Q-V | Kundur 1994 (voltage stability), Sauer 2006 | partial |
| OPF, economic dispatch, unit commitment | Glover 2017, Grainger 1994, Das 2002 | moderate |
| State estimation, contingency analysis, distribution factors | Grainger 1994 | moderate |
| Symmetrical components, unbalanced faults | Grainger 1994, Glover 2017, Gonen 1988, Das 2002 | strong |
| IEC 60909 and ANSI C37 short circuit | Kasikci 2002, Das 2002, Das 2010, Schneider guide | strong (old IEC edition) |
| DC short circuit (IEC 61660, IEEE 946) | none found | **gap** |
| Transient stability, machines, exciters, governors, PSS | Kundur 1994, Sauer 2006, Glover 2017, Das 2010 | strong |
| Small signal, eigenvalues | Kundur 1994, Sauer 2006, Kreyszig 2011 | strong |
| Motor starting | Das 2002 and 2010, Morley, Alstom guide, Fitzgerald 2003, Krause 2023 | strong |
| Harmonics, IEEE 519, filters | Arrillaga 2003, Das 2002 and 2010, Mohan 1995 | strong |
| EMT, travelling waves, insulation coordination | Das 2010, Gonen 1988 | strong |
| Arc flash, IEEE 1584 | Das 2021, Inshaw 2004 paper | strong |
| Overcurrent coordination, distance, differential, CT saturation | Alstom 2011 NPAG, Blackburn 2006, Das 2021, Morley | strong |
| Cable ampacity, Neher-McGrath, IEC 60287 | Anders 2005 | strong |
| Grounding grids (IEEE 80 style step and touch) | Das 2010, Morley | partial |
| Reliability indices (SAIFI and others) | Glover 2017 chapter, World Bank mini-grids | **thin** |
| HVDC and FACTS | Kundur 1994, Glover 2017, Das 2010, Mohan, Rashid, Bose | strong |
| Battery sizing (IEEE 485) | none found | **gap** |
| Load models (ZIP, exponential) | Sauer 2006, Kundur 1994, Das 2002 | strong |

## Books that would close the gaps

These are suggestions for Peter. None is bought or committed.

- **W. H. Kersting, Distribution System Modeling and Analysis.** Unbalanced
  three-phase load flow, line constants, transformer connections, the IEEE test
  feeders.
- **R. Billinton and R. N. Allan, Reliability Evaluation of Power Systems.** Network
  reliability indices and state enumeration.
- **A. Abur and A. Gomez Exposito, Power System State Estimation.**
- **V. Ajjarapu, Computational Techniques for Voltage Stability Assessment and
  Control.** Continuation power flow.
- Standards needed for **DC short circuit and batteries** (IEC 61660-1, IEEE 946,
  IEEE 485). These are paid standards. Alternatively, find a textbook treatment, to be
  found.
