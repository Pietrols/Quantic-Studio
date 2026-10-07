from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "contracts"
SPECS_ROOT = ROOT / "docs" / "specs"
SCHEMA_REFERENCE = re.compile(r"^Schema: `([^`]+)`$", re.MULTILINE)
JSON_EXAMPLE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


def main() -> int:
    schemas: dict[Path, dict[str, object]] = {}
    resources: list[tuple[str, Resource[object]]] = []

    for schema_path in sorted(SCHEMA_ROOT.rglob("*.schema.json")):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str):
            raise TypeError(f"Schema is missing a string $id: {schema_path}")
        schemas[schema_path.resolve()] = schema
        resources.append((schema_id, Resource.from_contents(schema)))

    registry = Registry().with_resources(resources)
    checked = 0

    for spec_path in sorted(SPECS_ROOT.rglob("*.md")):
        text = spec_path.read_text(encoding="utf-8")
        schema_match = SCHEMA_REFERENCE.search(text)
        examples = JSON_EXAMPLE.findall(text)
        if not examples:
            continue
        if schema_match is None:
            raise ValueError(f"JSON examples have no Schema declaration: {spec_path}")

        schema_path = (spec_path.parent / schema_match.group(1)).resolve()
        schema = schemas.get(schema_path)
        if schema is None:
            raise ValueError(f"Schema not found or not indexed: {schema_path}")
        validator = Draft202012Validator(
            schema, registry=registry, format_checker=FormatChecker()
        )

        for example_number, example_text in enumerate(examples, start=1):
            instance = json.loads(example_text)
            errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
            if errors:
                details = "; ".join(
                    f"{list(error.absolute_path)}: {error.message}" for error in errors
                )
                raise ValueError(f"Invalid example {example_number} in {spec_path}: {details}")
            checked += 1

    if checked == 0:
        raise ValueError(f"No JSON examples found under {SPECS_ROOT}")

    print(f"Validated {checked} JSON examples against Draft 2020-12 schemas.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
