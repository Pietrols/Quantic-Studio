from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Generic, TypeVar

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

T = TypeVar("T")


@dataclass(frozen=True)
class Diagnostic:
    code: str
    message: str
    element_ref: dict[str, str] | None = None
    severity: str = "error"

    def to_dict(self):
        return asdict(self)


@dataclass
class Outcome(Generic[T]):
    value: T | None = None
    diagnostics: list[Diagnostic] = field(default_factory=list)

    @property
    def ok(self):
        return self.value is not None and not any(d.severity == "error" for d in self.diagnostics)


def diagnostic(code, message, kind, identifier, field):
    return Diagnostic(code, message, {"element_type": kind,
                                      "element_id": str(identifier), "field": str(field)})


def contract_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "contracts" / "common" / "diagnostic.schema.json").is_file():
            return parent / "contracts"
    raise FileNotFoundError("Repository contracts directory is unavailable")


def _nonfinite(value, path=()):
    if isinstance(value, float) and not math.isfinite(value):
        yield path
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from _nonfinite(child, (*path, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _nonfinite(child, (*path, index))


def _reference(value, path, kind):
    node = value
    element_id = kind
    element_type = kind
    for part in path:
        if isinstance(node, dict):
            for key, identifier in node.items():
                if key.endswith("_id") and isinstance(identifier, str):
                    element_id = identifier
                    element_type = key.removesuffix("_id")
                    break
        try:
            node = node[part]
        except (KeyError, TypeError, IndexError):
            break
    if isinstance(node, dict):
        for key, identifier in node.items():
            if key.endswith("_id") and isinstance(identifier, str):
                element_id = identifier
                element_type = key.removesuffix("_id")
                break
    return {"element_type": element_type, "element_id": element_id,
            "field": ".".join(map(str, path)) or "$"}


def validate(value, name: str, root: Path | None = None) -> list[Diagnostic]:
    """Validate only local Draft 2020-12 schemas; never retrieve remote references."""
    try:
        root = root or contract_root()
        schemas = [json.loads(p.read_text()) for p in sorted(root.rglob("*.schema.json"))]
        resources = [(s["$id"], Resource.from_contents(s)) for s in schemas]
        version = value.get("schema_version") if isinstance(value, dict) else None
        supported = ("0.1.0", "0.2.0") if name in ("power/network", "project/manifest") else (
            ("0.2.0",) if name in ("power/shortcircuit-request", "power/shortcircuit-result") else ("0.1.0",))
        if version is not None and version not in supported:
            return [diagnostic("SCHEMA_VERSION", f"Supported versions: {', '.join(supported)}",
                               name, name, "schema_version")]
        legacy = version == "0.1.0" and name in ("power/network", "project/manifest")
        schema = json.loads((root / ("v0.1" if legacy else "") / f"{name}.schema.json").read_text())
        validator = Draft202012Validator(schema, registry=Registry().with_resources(resources),
                                        format_checker=FormatChecker())
        result = [Diagnostic("NONFINITE", "Numbers must be finite", _reference(value, p, name))
                  for p in _nonfinite(value)]
        for error in validator.iter_errors(value):
            path = list(error.absolute_path)
            if error.validator == "required":
                missing = next((k for k in error.validator_value if k not in error.instance), "$")
                path.append(missing)
            result.append(Diagnostic("SCHEMA_INVALID", error.message,
                                     _reference(value, path, name)))
        if not result and name == "power/shortcircuit-result":
            result.extend(_shortcircuit_semantics(value))
        return result
    except (OSError, ValueError, KeyError) as exc:
        return [diagnostic("CONTRACT_UNAVAILABLE", str(exc), "contract", name, "schema")]


def _shortcircuit_semantics(value):
    """Cross-row invariants not expressible as ordinary JSON Schema constraints."""
    errors = []
    seen = set()
    bus_sets = []
    statuses = []
    for case in value["case_results"]:
        label = case["case"]
        if label in seen:
            errors.append(diagnostic("DUPLICATE_CASE", "Case must occur once", "case", label, "case"))
        seen.add(label)
        rows = case["bus_results"]
        ids = [r["bus_id"] for r in rows]
        bus_sets.append(set(ids))
        if len(ids) != len(set(ids)):
            errors.append(diagnostic("DUPLICATE_ID", "Bus must occur once per case", "case", label, "bus_results"))
        available = [r[k] is not None for r in rows for k in ("ikss_ka", "ip_ka", "ith_ka")]
        expected = "success" if all(available) else "partial" if any(available) else "failed"
        statuses.append(expected)
        if case["status"] != expected:
            errors.append(diagnostic("RESULT_STATUS", f"Expected {expected}", "case", label, "status"))
        for row in rows:
            for result_field in ("voltage_factor", "ikss_ka", "ip_ka", "ith_ka"):
                if row[result_field] is None and not any(
                    (d.get("element_ref") or {}).get("element_id") == row["bus_id"] and
                    (d.get("element_ref") or {}).get("field") == result_field for d in case["diagnostics"]):
                    errors.append(diagnostic("MISSING_DIAGNOSTIC", "Unavailable value requires a bus/field diagnostic",
                                             "buses", row["bus_id"], result_field))
    if any(ids != bus_sets[0] for ids in bus_sets):
        errors.append(diagnostic("BUS_COVERAGE", "Cases must cover the same buses", "result", value["result_id"], "case_results"))
    expected = "success" if all(s == "success" for s in statuses) else (
        "failed" if all(s == "failed" for s in statuses) else "partial")
    if value["status"] != expected:
        errors.append(diagnostic("RESULT_STATUS", f"Expected {expected}", "result", value["result_id"], "status"))
    return errors
