"""Bounded local input snapshots. Limits are resource policy, not engineering values."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from qe_core.project import safe_path

MAX_DATA_BYTES = 4_000_000
MAX_FILES = 500
SUITES = {"pv.yield": "pv.site", "plc.scan": "automation.plc"}


class InputError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def read(root, name, limit):
    path = safe_path(root, name)
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise InputError(
            "INPUT_LIMIT", f"Input file exceeds configured byte limit: {name}"
        )
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise InputError("INPUT_OBJECT", f"Input must be a JSON object: {name}")
    json.dumps(value, allow_nan=False)
    return value, raw


def check_project(root: Path, max_file_bytes=2_000_000, max_data_bytes=MAX_DATA_BYTES):
    # Bound known external data before load_project opens it, including non-.json files.
    manifest, _ = read(root, "manifest.json", max_file_bytes)
    names = {"manifest.json": max_file_bytes}
    if isinstance(manifest.get("network_file"), str):
        names[manifest["network_file"]] = max_file_bytes
    for entry in manifest.get("models", []):
        if isinstance(entry, dict) and isinstance(entry.get("file"), str):
            names[entry["file"]] = max_file_bytes
    for entry in manifest.get("studies", []):
        if not isinstance(entry, dict) or not isinstance(
            entry.get("request_file"), str
        ):
            continue
        name = entry["request_file"]
        names[name] = max_file_bytes
        value, _ = read(root, name, max_file_bytes)
        if entry.get("study_type") in SUITES and value.get("schema_version") == "0.1.0":
            execution = value.get("execution")
            data = (
                execution.get("input_series_file")
                if isinstance(execution, dict)
                else None
            )
            if isinstance(data, str):
                names.setdefault(data, max_data_bytes)
    if len(names) > MAX_FILES:
        raise InputError("INPUT_LIMIT", "Too many project input files")
    # Preserve the previous JSON inventory bound, without materialising an unbounded list.
    count = 0
    for path in root.rglob("*.json"):
        name = path.relative_to(root).as_posix()
        # Generated study output is not an input unless the manifest explicitly binds it.
        if name == "out/results.json" and name not in names:
            continue
        count += 1
        if count > MAX_FILES:
            raise InputError("INPUT_LIMIT", "Too many project JSON files")
        confined = safe_path(root, name)
        if confined.is_file() and confined.stat().st_size > names.get(
            name, max_file_bytes
        ):
            raise InputError(
                "INPUT_LIMIT", f"Input file exceeds configured byte limit: {name}"
            )
    for name, limit in names.items():
        read(root, name, limit)


def context(
    root, project, model, study, max_file_bytes=2_000_000, max_data_bytes=MAX_DATA_BYTES
):
    manifest, _ = read(root, "manifest.json", max_file_bytes)
    entry = next(
        (
            entry
            for entry in manifest.get("studies", [])
            if isinstance(entry, dict) and entry.get("study_id") == study.study_id
        ),
        None,
    )
    bound = next(
        (
            entry
            for entry in manifest.get("models", [])
            if isinstance(entry, dict) and entry.get("model_id") == model.model_id
        ),
        None,
    )
    if (
        entry is None
        or bound is None
        or entry.get("model_id") != model.model_id
        or entry.get("study_type") != study.study_type
        or bound.get("file") != model.file
        or bound.get("model_type") != model.model_type
    ):
        raise InputError(
            "EDIT_CONFLICT", "Project binding changed while selecting the study; reload"
        )
    request_name = entry["request_file"]
    data_name = study.request["execution"]["input_series_file"]
    paths = [
        safe_path(root, name)
        for name in (model.file, request_name, data_name, "manifest.json")
    ]
    if len(set(paths)) != len(paths):
        raise InputError(
            "INPUT_FILE_ALIAS",
            "Model, request, series and manifest need distinct files",
        )
    values, records = [], []
    for name, role, limit in [
        (model.file, "model", max_file_bytes),
        (request_name, "request", max_file_bytes),
        (data_name, "data", max_data_bytes),
    ]:
        value, raw = read(root, name, limit)
        values.append(value)
        records.append(
            {"path": name, "role": role, "sha256": hashlib.sha256(raw).hexdigest()}
        )
    if values[0] != model.data or values[1] != study.request:
        raise InputError(
            "EDIT_CONFLICT", "Input changed while selecting the study; reload"
        )
    pin = values[1]["weather" if study.study_type == "pv.yield" else "events"]["sha256"]
    if records[2]["sha256"] != pin:
        raise InputError(
            "INPUT_HASH", "Series bytes differ from the request's pinned hash"
        )
    return {
        "model": values[0],
        "request": values[1],
        "series": values[2],
        "input_files": records,
    }
