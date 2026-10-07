import copy
import hashlib
import json
import re
from pathlib import Path

import pytest
from qe_core import load_project, validate
from qe_core.project import validate_network
from qe_core.provenance import hash_files, hash_inputs, provenance
from qe_core.units import convert

ROOT = Path(__file__).resolve().parents[4]


def example(name):
    return json.loads(re.search(r"```json\s*\n(.*?)\n```", (ROOT / f"docs/specs/{name}.md").read_text(), re.S)[1])


@pytest.fixture
def project(tmp_path):
    for name in ("manifest", "network", "loadflow-request"):
        target = tmp_path / ("studies/loadflow-request.json" if name == "loadflow-request" else name + ".json")
        target.parent.mkdir(exist_ok=True)
        target.write_text(json.dumps(example(name)))
    return tmp_path


def test_load_typed_project(project):
    result = load_project(project)
    assert result.ok and result.value.network.base_mva == 10
    assert len(result.value.studies) == 1 and len(result.value.files) == 3


def test_bad_element_and_field(project):
    data = example("network")
    data["buses"][1]["vn_kv"] = -1
    (project / "network.json").write_text(json.dumps(data))
    result = load_project(project)
    assert not result.ok
    assert result.diagnostics[0].element_ref == {
        "element_type": "bus", "element_id": "bus-load", "field": "buses.1.vn_kv"}
    assert not validate(result.diagnostics[0].to_dict(), "common/diagnostic")


@pytest.mark.parametrize("change", ["missing", "malformed", "nonfinite", "escape", "symlink", "version"])
def test_invalid_input_diagnostic(project, change, tmp_path):
    path = project / "manifest.json"
    if change == "missing":
        path.unlink()
    elif change == "malformed":
        path.write_text("{")
    elif change == "nonfinite":
        p = project / "network.json"
        p.write_text(p.read_text().replace('10.0', 'NaN'))
    else:
        data = json.loads(path.read_text())
        if change == "escape":
            data["network_file"] = "../network.json"
        elif change == "symlink":
            (project / "outside.json").symlink_to(project.parent / "other.json")
            data["network_file"] = "outside.json"
        else:
            data["schema_version"] = "9.0.0"
        path.write_text(json.dumps(data))
    result = load_project(project)
    assert not result.ok and result.diagnostics and result.diagnostics[0].element_ref


def test_semantic_validation():
    data = example("network")
    data["buses"].append(copy.deepcopy(data["buses"][0]))
    data["loads"][0]["bus_id"] = "unknown"
    errors = validate_network(data)
    assert {e.code for e in errors} == {"DUPLICATE_ID", "UNKNOWN_BUS"}


def test_units():
    # SI prefix definitions: 1000 V = 1 kV, 1000 m = 1 km (BIPM SI Brochure, section 3).
    assert convert(1000, "volt", "vn_kv").value == 1
    assert convert(1000, "meter", "length_km").value == 1
    assert not convert(1, "meter", "vn_kv").ok
    assert not convert(float("inf"), "volt", "vn_kv").ok
    assert not convert(1, "volt", "missing").ok


def test_hashes(project):
    files = [project / "manifest.json", project / "network.json"]
    before = hash_files(files, project)
    assert before == hash_files(reversed(files), project)
    files[0].write_text(files[0].read_text() + "\n")
    assert before != hash_files(files, project)
    assert hash_inputs({"a": 1}) == hashlib.sha256(b'{"a":1}').hexdigest()
    assert not validate(provenance("test", "1", before), "common/provenance")
