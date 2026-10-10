from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .validation import Outcome, diagnostic, validate


@dataclass(frozen=True)
class Network:
    data: dict[str, Any]

    @property
    def network_id(self) -> str:
        return self.data["network_id"]

    @property
    def base_mva(self) -> float:
        return self.data["base_mva"]


@dataclass(frozen=True)
class Study:
    study_id: str
    study_type: str
    request: dict[str, Any]


@dataclass(frozen=True)
class Project:
    name: str
    network: Network
    studies: tuple[Study, ...]
    files: tuple[Path, ...]


def read_json(path: Path) -> Outcome[dict]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return Outcome(value)
    except (OSError, ValueError, UnicodeError) as exc:
        return Outcome(diagnostics=[diagnostic("INPUT_READ", str(exc), "file", path.name, "content")])


def safe_path(root: Path, name: str) -> Path:
    path = (root / name).resolve()
    if Path(name).is_absolute() or "\\" in name or ":" in name or not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path must stay inside project: {name}")
    return path


def validate_network(data) -> list:
    errors = validate(data, "power/network")
    if errors:
        return errors
    ids = {}
    for kind in ("buses", "lines", "transformers", "loads", "generators", "external_grids", "shunts"):
        ids[kind] = set()
        for item in data[kind]:
            key = next(k for k in item if k.endswith("_id") and k != "bus_id") if kind != "buses" else "bus_id"
            identifier = item[key]
            if identifier in ids[kind]:
                errors.append(diagnostic("DUPLICATE_ID", "Identifier is not unique", kind, identifier, key))
            ids[kind].add(identifier)
    for kind in ("lines", "transformers", "loads", "generators", "external_grids", "shunts"):
        for item in data[kind]:
            key = next(k for k in item if k.endswith("_id") and k != "bus_id")
            for field in ("bus_id", "from_bus", "to_bus", "hv_bus", "lv_bus"):
                if field in item and item[field] not in ids["buses"]:
                    errors.append(diagnostic("UNKNOWN_BUS", f"Bus {item[field]} does not exist",
                                             kind, item[key], field))
    return errors


def load_project(folder: str | Path) -> Outcome[Project]:
    root = Path(folder).resolve()
    manifest_path = root / "manifest.json"
    parsed = read_json(manifest_path)
    if parsed.diagnostics:
        return Outcome(diagnostics=parsed.diagnostics)
    manifest = parsed.value
    errors = validate(manifest, "project/manifest")
    if errors:
        return Outcome(diagnostics=errors)
    files = [manifest_path]
    try:
        network_path = safe_path(root, manifest["network_file"])
    except ValueError as exc:
        return Outcome(diagnostics=[diagnostic("PROJECT_PATH", str(exc), "manifest", manifest["name"], "network_file")])
    parsed = read_json(network_path)
    if parsed.diagnostics:
        return Outcome(diagnostics=parsed.diagnostics)
    network = parsed.value
    errors.extend(validate_network(network))
    files.append(network_path)
    studies = []
    seen = set()
    for item in manifest["studies"]:
        sid = item["study_id"]
        if sid in seen:
            errors.append(diagnostic("DUPLICATE_ID", "Study ID is not unique", "study", sid, "study_id"))
        seen.add(sid)
        supported = {"0.1.0": ("loadflow",), "0.2.0": ("loadflow", "shortcircuit"),
                     "0.3.0": ("loadflow", "shortcircuit", "motorstart")}[manifest["schema_version"]]
        if item["study_type"] not in supported:
            errors.append(diagnostic("UNSUPPORTED_STUDY", "Study is unsupported by this manifest version", "study", sid, "study_type"))
            continue
        try:
            path = safe_path(root, item["request_file"])
        except ValueError as exc:
            errors.append(diagnostic("PROJECT_PATH", str(exc), "study", sid, "request_file"))
            continue
        request = read_json(path)
        errors.extend(request.diagnostics)
        if request.diagnostics:
            continue
        problems = validate(request.value, f"power/{item['study_type']}-request")
        errors.extend(problems)
        if problems:
            continue
        try:
            if safe_path(root, request.value["network_file"]) != network_path:
                errors.append(diagnostic("NETWORK_MISMATCH", "Request must name the project network", "study", sid, "network_file"))
        except ValueError as exc:
            errors.append(diagnostic("PROJECT_PATH", str(exc), "study", sid, "network_file"))
        if item["study_type"] == "motorstart" and not validate_network(network):
            motor = request.value["motor"]
            if motor["bus_id"] not in {bus["bus_id"] for bus in network["buses"]}:
                errors.append(diagnostic("UNKNOWN_BUS", "Motor bus does not exist", "motor",
                                         motor["motor_id"], "bus_id"))
        studies.append(Study(sid, item["study_type"], request.value))
        files.append(path)
    if errors:
        return Outcome(diagnostics=errors)
    return Outcome(Project(manifest["name"], Network(network), tuple(studies), tuple(files)))
