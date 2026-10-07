"""Unit labels come from contracts/common/units.schema.json, not inferred suffixes."""
import json
import math

import pint

from .validation import Outcome, contract_root, diagnostic

_REGISTRY = pint.UnitRegistry()
# Apparent/reactive power have the same SI dimensions as real power, but remain
# semantically distinct contract fields. Per-unit values require an explicit base.
_ALIASES = {"MVA": "megawatt", "Mvar": "megawatt", "pu": "dimensionless"}


def convert(value: float, from_unit: str, field: str) -> Outcome[float]:
    try:
        units = json.loads((contract_root() / "common/units.schema.json").read_text())
        label = units["properties"]["field_units"]["properties"][field]["const"]
        result = _REGISTRY.Quantity(value, _ALIASES.get(from_unit, from_unit)).to(
            _ALIASES.get(label, label)).magnitude
        if not math.isfinite(result):
            raise ValueError("Converted value must be finite")
        return Outcome(float(result))
    except (OSError, KeyError, ValueError, TypeError, pint.errors.PintError) as exc:
        return Outcome(diagnostics=[diagnostic("UNIT_CONVERSION", str(exc), "quantity", field, field)])
