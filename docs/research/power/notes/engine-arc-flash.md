# Engine spec note: arc flash (IEEE 1584-2018) (WP-2.10)

This note covers matrix rows:

- A1: IEEE 1584-2018 incident energy with automatic clearing time;
- A2: labels and permits;
- A3: DC arc flash;
- A4: above 15 kV.

These rows also depend on F1/F3 (short circuit) and P1 (TCC data for clearing times).

Arc flash studies are a paid service line for Quantic in mining and industrial plants, so
this engine has commercial priority.

Paraphrased from the owned book. No coefficient tables, figures or worked examples are
reproduced.

## 1. Sources

| Key | Source | Where |
| --- | --- | --- |
| Das21 | J. C. Das, *Arc Flash Hazard Analysis and Mitigation*, 2nd ed., Wiley/IEEE, 2021 | ch. 3 (printed pp. 68 to 82), ch. 5 (pp. 133 to 177), ch. 6 sec. 6.9 (pp. 197 to 205), ch. 7 (pp. 232 to 243), ch. 15 (DC) |
| arcflash | L. Yip, `arcflash`, Python library, MIT licence (stated on the repository page) | https://github.com/LiaungYip/arcflash (read 2026-10-15) |

**Standard:** IEEE 1584-2018, *Guide for Performing Arc-Flash Hazard Calculations*. We do
not own it; it is paid. Das21 ch. 3 reproduces its model and coefficient tables (Tables
3.1 to 3.7), so we can **verify** against the book. Our rules forbid copying those tables
into this repository (AGENTS.md rule 6). See section 6 for the decision this needs.

## 2. Model scope (Das21 sec. 3.1, pp. 68 to 69)

IEEE 1584-2018 is an empirical, curve-fitted model. It applies to:

- three-phase AC systems, 208 V to 15 kV line-to-line, 50 or 60 Hz;
- bolted fault currents from 500 A to 106 kA (208 to 600 V) and from 200 A to 65 kA
  (601 V to 15 kV);
- electrode gaps from 6.35 to 76.2 mm (LV) and from 19.05 to 254 mm (MV);
- working distance of at least 305 mm;
- any clearing time.

Single-phase AC and DC are outside the model.

**Diagnostics:** the engine must emit a diagnostic naming the field for every input
outside these ranges. It must never extrapolate silently.

Since 2018, system grounding no longer changes the result. The 2002 edition did make a
grounded or ungrounded distinction (p. 69).

## 3. Algorithm (Das21 ch. 3; flow chart Fig. 3.4, p. 81)

**Inputs per location:**

- Voc (system line-to-line voltage);
- Ibf, the bolted three-phase fault current from the short-circuit engine;
- electrode configuration;
- gap G;
- working distance D;
- enclosure height, width and depth;
- the protective device that clears the arc, with its TCC.

**Electrode configurations** (sec. 3.2, p. 69):

- VCB: vertical conductors in a box;
- VCBB: vertical conductors in a box, terminated in an insulating barrier;
- HCB: horizontal conductors in a box;
- VOA: vertical conductors in open air;
- HOA: horizontal conductors in open air.

The choice must match the real equipment. The equipment library should carry a default
per equipment class (see Das21 Tables 1.5 and 1.6, referenced on p. 81).

**Steps:**

1. **Intermediate average arcing currents** at three test voltages, 600 V, 2700 V and
   14,300 V (eq. 3.1, p. 71). Each is a polynomial in Ibf times a log-linear term in Ibf
   and G. The coefficients depend on configuration and test voltage (Table 3.1).
2. **Final arcing current** (secs 3.11.1 and 3.12.1):
   - if Voc is above 600 V, interpolate between the intermediate currents (eqs 3.16 to
     3.18). There are two branches, one for Voc up to 2.7 kV and one above it;
   - if Voc is 600 V or less, use a separate expression (eq. 3.25).
3. **Arcing current variation factor** (eq. 3.2, Table 3.2, p. 73):
   - compute VarCf as a polynomial in Voc;
   - set Iarc_min = Iarc (1 − 0.5 VarCf).

   The 2002 edition used a flat 85% (p. 73).
4. **Clearing time.** Run the protective-device TCC at both Iarc and Iarc_min, using the
   device's share of the arcing current where the device is not in series with all
   sources. This gives T and T_min (p. 80 text).
5. **Enclosure size correction factor CF** (secs 3.8 to 3.10, pp. 76 to 77):
   - CF = 1 for VOA and HOA;
   - an enclosure is "shallow" if Voc is below 600 V, both height and width are under
     508 mm, and depth is under 203.2 mm; otherwise it is "typical";
   - equivalent height and width come from guideline ranges (Table 3.6) and eqs 3.11 to
     3.12, with constants that depend on the configuration;
   - EES = (height + width)/2, eq. 3.13;
   - CF comes from a quadratic in EES for typical enclosures (eq. 3.14) or a reciprocal
     form for shallow ones (eq. 3.15), with coefficients from Table 3.7.
6. **Intermediate incident energies** at 600, 2700 and 14,300 V (eqs 3.3 to 3.6), with
   an LV form for Voc of 600 V or less. Each energy is a log-linear expression in G, the
   intermediate Iarc, Ibf, D and T, divided by CF (coefficients in Tables 3.3 to 3.5).
7. **Final incident energy** (eqs 3.19 to 3.21 for Voc above 600 V, eq. 3.6 at 600 V or
   less): use the same interpolation scheme as for the current.
8. **Arc flash boundary**: the same structure for the distance at which E equals
   1.2 cal/cm² (5.0 J/cm²; threshold per Das21 printed p. 4, pdf p. 27) (eqs 3.7 to 3.10 and 3.22 to 3.24).
9. **Repeat steps 6 to 8 with Iarc_min and T_min.** Report the larger E and AFB
   (p. 79).

**Outputs per location:**

- Iarc and Iarc_min;
- T and T_min, with the clearing device;
- E in J/cm² and cal/cm²;
- AFB;
- the PPE category or label data under NFPA 70E. **Gap:** read Das21 ch. 1 and 2 for
  the category rules;
- every intermediate value in the worked trace (our G13 differentiator).

## 4. Short-circuit current to use (Das21 ch. 5 and 6)

- Arc flash needs symmetrical rms currents with no post-multiplying factors. Still, two
  networks are needed (first-cycle and interrupting) because their machine multipliers
  differ (Das21 p. 139).
- **Decaying sources** (sec. 6.9, pp. 197 to 205). Commercial tools offer one of two
  options:
  - a single current, either first-cycle or interrupting, applied for the whole
    duration;
  - stepped removal of motors and generators after user-chosen delays.

  The first overstates energy; the second depends on guessed step times. Das proposes
  integrating energy over time:
  1. Build each source's actual decrement curve. The utility is non-decaying; generators
     follow their subtransient and transient decrement; motors decay within a few cycles.
  2. Sum the curves.
  3. Split the arc duration into intervals.
  4. Accumulate incident energy interval by interval, with each source tripping at its
     own device time.

  Das21 (p. 199) states that **no commercial software** did this when the book was
  written (2021). This is a candidate Quantic differentiator. To verify against current
  ETAP and PowerFactory features before claiming it.

  It needs:
  - the machine decrement equations: Das21 ch. 6, and Das02 ch. 6, already noted in
    `engine-ansi-short-circuit.md`;
  - the 1584 model applied piecewise in time. **Validity of piecewise application must
    be checked: the 1584 model was fitted on constant currents.** Das21 pp. 201 to 205
    shows a worked approach to read before design.

## 5. Related LV device behaviour

- Current-limiting fuses and breakers. Below the current-limiting threshold, the TCC
  gives the time. Above it, the clearing time is about half a cycle or less, and the
  let-through matters (Das21 ch. 7). The device library must carry this.
- LV device duty multipliers are in `engine-ansi-short-circuit.md` sec. 6.

## 6. Decision for Peter: how to get the 1584-2018 coefficients into Quantic

The engine needs about 300 published coefficients (Das21 Tables 3.1 to 3.7, which
reproduce IEEE 1584-2018). Options:

1. **Depend on `arcflash` (MIT)** as a library, the same way we depend on pandapower.
   The repository page says it reproduces the standard's Annex D examples and agrees
   with 144,000 cases from the official IEEE calculator spreadsheets to within 0.1%. We
   would verify it against Das21 Tables 3.1 to 3.7 and Das21's examples (Tables 3.8 and
   3.9), not trust it blindly.
   - Pros: it is not copied into our repo, and it is fast.
   - Con: it is a third-party library with the usual maintenance risk, and the page
     does not discuss IEEE permission for the coefficients.
2. **Buy IEEE 1584-2018** and have Quantic load the coefficients from a user-supplied
   data file kept outside the repo (as with QE-References). This is the cleanest
   licence position. Users would need their own copy, as some tools require.
3. **Enter the coefficients ourselves from Das21** into a data file in the repo. This
   breaks AGENTS.md rule 6 and is not recommended.

My recommendation is option 1 for the engine, with option 2 as the long-term clean path.
This is Peter's call (licence and source question, README rule 7).

## 7. Above 15 kV and DC (A3, A4)

- **Above 15 kV:** IEEE 1584 does not apply. `arcflash` lists the Lee method as planned,
  not done. Das21 discusses HV methods. **Gap:** read Das21 sections on the Lee method
  and on arc-resistant equipment (ch. 13).
- **DC:** Das21 ch. 15 covers DC short-circuit currents (IEC 61660 procedures, battery
  short circuit) and DC arc flash. `arcflash` lists Doan and Ammerman as planned. **To
  read next.** This also closes part of gap F5 (DC faults).

## 8. Gaps

1. NFPA 70E PPE category and label rules: Das21 ch. 1 and 2.
2. Equipment default gaps, distances and configurations by class: Das21 Tables 1.5 and
   1.6.
3. Validity of piecewise-time application of the 1584 model (sec. 4).
4. Above 15 kV (Lee) and DC methods: Das21 ch. 13 and 15.
5. Current ETAP and PowerFactory arc flash features (decay handling, 2018 model,
   labels): compare with `etap.md` and `powerfactory.md` rows A1 to A4.
