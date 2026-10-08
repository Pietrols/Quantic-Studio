# Unit conventions

Schema: `../../contracts/common/units.schema.json`

Contract field names carry their unit as a suffix. Values are expressed in the named unit directly, with no hidden conversion or implicit unit-bearing object. The registry below fixes the spelling used by the contracts. Dimensionless ratios and per-unit values are identified as such.

Synthetic registry example:

```json
{
  "field_units": {
    "base_mva": "MVA",
    "vn_kv": "kV",
    "vm_pu": "pu",
    "vm_setpoint_pu": "pu",
    "va_degree": "degree",
    "va_setpoint_degree": "degree",
    "length_km": "km",
    "r_ohm_per_km": "ohm/km",
    "x_ohm_per_km": "ohm/km",
    "b_us_per_km": "uS/km",
    "max_current_ka": "kA",
    "sn_mva": "MVA",
    "vn_hv_kv": "kV",
    "vn_lv_kv": "kV",
    "r_pu": "pu",
    "x_pu": "pu",
    "tap_ratio": "dimensionless",
    "phase_shift_degree": "degree",
    "p_mw": "MW",
    "q_mvar": "Mvar",
    "p_min_mw": "MW",
    "p_max_mw": "MW",
    "q_min_mvar": "Mvar",
    "q_max_mvar": "Mvar",
    "tolerance_mva": "MVA",
    "largest_mismatch_mva": "MVA",
    "p_from_mw": "MW",
    "q_from_mvar": "Mvar",
    "p_to_mw": "MW",
    "q_to_mvar": "Mvar",
    "p_loss_mw": "MW",
    "q_loss_mvar": "Mvar",
    "loading_pct": "%"
  }
}
```

CC-1 extends the unit registry to version 0.2 with fault MVA, R/X and power
factor (dimensionless), subtransient pu/ohms, generator voltage range and LV
tolerance (%), line end temperature (degC), fault duration (s), frequency (Hz),
voltage factor (dimensionless) and Ik''/ip/Ith (kA). Existing labels are unchanged.
