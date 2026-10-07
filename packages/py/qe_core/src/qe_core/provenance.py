"""SHA-256 with explicit framing, deterministic across machines and input ordering."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def hash_files(files, root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(set(Path(p).resolve() for p in files), key=lambda p: p.relative_to(root.resolve()).as_posix()):
        name = path.relative_to(root.resolve()).as_posix().encode()
        data = path.read_bytes()
        for part in (name, data):
            digest.update(len(part).to_bytes(8, "big"))
            digest.update(part)
    return digest.hexdigest()


def hash_inputs(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def provenance(solver: str, version: str, input_hash: str) -> dict:
    return {"solver_name": solver, "solver_version": version,
            "input_hash_sha256": input_hash,
            "timestamp": datetime.now(timezone.utc).isoformat()}
