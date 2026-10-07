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
        schema = json.loads((root / f"{name}.schema.json").read_text())
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
        if isinstance(value, dict) and "schema_version" in value and value["schema_version"] != "0.1.0":
            result.append(diagnostic("SCHEMA_VERSION", "Only schema version 0.1.0 is supported",
                                     name, name, "schema_version"))
        return result
    except (OSError, ValueError, KeyError) as exc:
        return [diagnostic("CONTRACT_UNAVAILABLE", str(exc), "contract", name, "schema")]
