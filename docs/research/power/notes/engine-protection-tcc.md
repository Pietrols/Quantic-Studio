# Engine spec note: overcurrent protection, TCC and coordination (WP-2.10)

This note covers matrix rows:

- P1: TCC plotting with device libraries;
- P2: damage curves;
- P3: automatic coordination checks;
- P4: sequence of operation;
- P5: setting calculation.

Distance protection (P6), differential protection (P7) and CT models (P8) are outlined
only. Arc flash (A1) depends on this engine for its clearing times.

Paraphrased from the owned references. No tables, figures or worked examples are
reproduced.

## 1. Sources

| Key | Source | Where |
| --- | --- | --- |
| NPAG | Alstom Grid, *Network Protection and Automation Guide*, 2011 edition | ch. 9, printed pp. 9-3 to 9-12 |
| Das21 | J. C. Das, *Arc Flash Hazard Analysis and Mitigation*, 2nd ed., 2021 | ch. 7 (printed pp. 212 to 257), ch. 10, ch. 11 (pp. 360 to 380) |
| Blackburn06 | J. L. Blackburn, T. J. Domin, *Protective Relaying: Principles and Applications*, 3rd ed., 2006 | to read for distance and differential |

The relevant standards are:

- IEC 60255-151 (IDMT curves, accuracy);
- IEEE C37.112 (inverse-time equations, reset);
- IEEE C57.109 (transformer through-fault withstand);
- the NEC tables for transformer protection limits.

We own none of them. The books quote them.

## 2. What the engine must do

1. **Device library.** It holds relays (curve family and settings ranges), LV trip units
   (long time, short time, instantaneous, ground, I²t ramps), fuses (minimum melt and
   total clear) and reclosers. Equation-defined curves are stored as parameters.
   Manufacturer curves are stored as digitised points with **tolerance bands**. Das21
   (p. 376) shows a 500 to 900 A spread at 2 s across four makers' 100E fuses, so a
   single generic curve per rating is not acceptable.
2. **Curve evaluation.** Evaluate operating time t(I) for a device at any current, using
   the CT ratio and the voltage base (TCC currents referred to one voltage). Use the
   device's own share of the fault current, not the bus total.
3. **TCC plot.** Log-log time and current, multiple devices, damage curves, and fault
   current markers (maximum and minimum, three-phase and ground).
4. **Coordination check.** For each pair of upstream and downstream devices, at every
   current from pickup up to the maximum fault current through both, check that the time
   gap is at least the required margin (section 4). Report violations by current range,
   not just at maximum fault.
5. **Sequence of operation.** For a fault at a chosen location, list devices in trip
   order with times. Each later device's current changes when an earlier one opens, so
   re-solve the short circuit after each opening. This links to the ETAP Star sequence
   viewer and the PowerFactory short-circuit trace (`etap.md` and `powerfactory.md`).
6. **Clearing time to arc flash** at Iarc and Iarc_min (`engine-arc-flash.md` step 4).

## 3. Curve families (equation-defined)

**IEC 60255 IDMT** (NPAG Table 9.1, p. 9-4). With Ir = I / Is (multiple of setting) and
TMS the time multiplier:

| Curve | Operating time t |
| --- | --- |
| Standard inverse | TMS · 0.14 / (Ir^0.02 − 1) |
| Very inverse | TMS · 13.5 / (Ir − 1) |
| Extremely inverse | TMS · 80 / (Ir² − 1) |
| Long-time standby earth fault | TMS · 120 / (Ir − 1) |

These four equations are the published IEC constants, quoted as equations, which is the
standard's own form.

**IEEE / US curves** (NPAG Table 9.1, same page). NPAG writes them in the form
t = (TD/7) · (A / (Ir^p − 1) + B) with constants for:

- IEEE moderately, very and extremely inverse;
- US CO8 inverse;
- US CO2 short-time inverse.

Store the constants as library data with this page cited.

**The TD/7 scaling is NPAG's convention.** Other references, and IEEE C37.112 itself as
commonly quoted, scale by TD directly. **Gap: confirm the C37.112 form before coding.
Until then, the library entry records which scaling it uses and its source.**

**GE-style "ANSI" polynomial curves** (Das21 eq. 7.1, p. 214, constants in Table 7.1,
p. 215):

    T = M · [A + B/(m − C) + D/(m − C)² + E/(m − C)³],   m = I / Ipickup

m is clamped to the range 1.03 to 20: below 1.03 the curve is evaluated at 1.03, and
above 20 at 20. Das21 eq. 7.2 (p. 217) applies the same clamping to the IEC form.

The clamping is a relay-vendor implementation detail and must be a per-device flag.
Das21 prints "1/I_PKP" in the middle line of eq. 7.1, which must be I/I_PKP; it is a
typesetting slip.

**Thermal and motor models.** IEEE C37.112 integrates the reciprocal of the hot thermal
limit curve (Das21 eqs 7.13 to 7.15, pp. 254 to 255). This gives relays with thermal
memory, needed for motor protection (M-series rows).

**Definite time and instantaneous elements:** a fixed time above the pickup.

## 4. Grading margin (NPAG secs 9.11 to 9.12, pp. 9-9 to 9-11)

The margin has five parts:

1. breaker interrupting time;
2. relay timing error;
3. relay overshoot;
4. CT error;
5. a final safety margin.

**Fixed margins.** About 0.4 s is reasonable with modern breakers and relays; the older
convention was 0.5 s. Fixed margins are valid only at high fault levels. At low currents,
the IEC permitted error (7.5% of operating time) can exceed a fixed margin.

**Calculated margin** (NPAG eq. 9.2):

    t' = ((2 E_R + E_CT) / 100) · t + t_CB + t_O + t_S

where:

- E_R is the relay timing error in %;
- E_CT is the CT error allowance in %;
- t is the downstream relay's operating time;
- t_CB is the breaker interrupting time;
- t_O is the relay overshoot time;
- t_S is the safety margin.

For definite-time relays, drop E_CT (eq. 9.3).

Typical values of each term by relay technology are in NPAG Table 9.3 (p. 9-10). These
are typical values, not standards, so the engine stores them as editable defaults with
that citation.

**Pickup setting** (sec. 9.10, p. 9-9): modern relays have a drop-off-to-pickup ratio of
about 0.95. The pickup should therefore be at least about 1.05 times the circuit's
short-time rated current, so the relay resets at full load.

**Engine behaviour:**

- Compute t' per device pair at each current point.
- Flag any point where the actual gap is less than t'.
- Show the margin used and its components in the worked trace.

## 5. Damage and withstand curves (P2)

- **Transformers, IEEE C57.109 through-fault curves** (Das21 secs 11.4 to 11.5,
  pp. 369 to 374):
  - Categories I to IV by kVA rating.
  - The curve has a thermal I²t part fixed by tabulated points (time against multiple of
    rated current, Table 11.3) and, for frequent faults, a mechanical part. That part is
    an I²t = K line from 100% of the through-fault current at 2 s down to 70% of it.
  - For category II transformers the source impedance is ignored when computing the
    through-fault current (Das21 p. 374).
  - The 70% point time follows from (1.0)² × 2 = (0.7)² × t₁, so t₁ ≈ 4.08 s. That is
    independent of the transformer. The book's 4.09 s comes from rounded kA values.
- **Cables, conductor short-circuit withstand I²t:** read Anders 2005 (IEC 60949 and
  adiabatic formulas) next. This also feeds C1 cable sizing.
- **Motors:** hot and cold thermal limit curves and starting curve. These are datasheet
  inputs; link to the M2 acceleration study.
- **NEC transformer protection limits** (Das21 sec. 11.1, Table 11.1): these are rule
  checks, P3.

## 6. Data model sketch (for the contract WP)

`protective_device`:

- `id`, `kind` (relay | lv_trip_unit | fuse | recloser);
- `ct_ratio`, `voltage_base_kv`;
- `elements[]`, each one of:
  - an `idmt` element with `family` (iec | ieee | ansi_poly | user_points), `constants`,
    `scaling` (td | td_over_7), `pickup`, `time_dial`, and `clamp` (min_multiple,
    max_multiple);
  - a `definite_time` element;
  - an `instantaneous` element;
  - an `lv` element with `ltpu`, `ltd`, `stpu`, `std`, `i2t_on`, `inst`, `gf`;
  - a fuse element with `points_min_melt[]`, `points_total_clear[]`, `tolerance`;
- `source` (catalogue reference, page).

The coordination request lists device pairs or the path to the source, the margin
method (fixed | calculated) with its parameters, and the fault cases.

## 7. Outline only (later dossiers)

- **P6, distance protection:** zones, R-X characteristics (mho, quadrilateral), infeed.
  Sources: NPAG ch. 11, Blackburn06 ch. 12.
- **P7, differential protection:** percent bias, harmonic restraint, CT phase
  compensation. Sources: NPAG ch. 10 and 16, Das21 ch. 8.
- **P8, CT saturation:** C-class and knee-point checks, transient saturation. Source:
  Das21 ch. 12 (secs 12.3, 12.9), NPAG ch. 6.

## 8. Gaps

1. The exact IEEE C37.112 equation form and reset equations; we need the standard.
2. Manufacturer curve data (fuses, trip units): this needs a data acquisition plan, as
   for the ETAP library. It is a business task: request catalogues from suppliers in
   Zambia and South Africa first.
3. IEEE C57.109 tables. The values are quoted in Das21 Table 11.3; we must not copy the
   table, so we need the standard or user entry.
4. Open-source reuse. pandapower has a protection package (docs read 2026-10-15):
   - an `OCRelay` class with DTOC, IDMT and IDTOC elements;
   - a `Fuse` class with a standard library from 16 to 1000 A (example "Siemens
     NH-1-100") and PCHIP-interpolated melting curves (minimum and total);
   - `calculate_protection_times(net, scenario='sc'|'pp')`.

   The docs do not state the curve families, the grading logic or the fault types, so
   read the tutorials and source before relying on it. It is a candidate base for P1 and
   P4, with our curve families, margins and trace on top.
   Docs: https://pandapower.readthedocs.io/en/latest/protection/oc_relay.html and
   .../protection/fuse.html.
