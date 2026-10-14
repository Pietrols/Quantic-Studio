"""CC-5/CC-6 authored routing references, never engine-generated expectations."""

import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from qe_api.app import create_app
from qe_api.runner import Runner, WorkerError
from qe_cli.main import run_study
from qe_report import VoltageLimits

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(params=["pv", "plc"])
def project(request, tmp_path):
    suite = request.param
    folder = tmp_path / suite
    shutil.copytree(ROOT / f"apps/web/e2e/{suite}/fixture", folder)
    # Foreign data is opaque and must never be normalized or changed.
    manifest = json.loads((folder / "manifest.json").read_bytes())
    manifest["models"].append(
        {"model_id": "future", "model_type": "circuit.schematic", "file": "future.bin"}
    )
    (folder / "future.bin").write_bytes(b'{ "opaque": true }\n')
    (folder / "manifest.json").write_text(json.dumps(manifest))
    return folder, manifest


def client(folder, **options):
    return TestClient(create_app(folder.parent, **options), base_url="http://127.0.0.1")


def test_api_and_cli_unavailable_preserve_every_file(project, capsys):
    folder, manifest = project
    before = {p.name: p.read_bytes() for p in folder.iterdir()}
    study = manifest["studies"][0]
    c = client(folder)
    response = c.post(
        "/api/studies/run",
        json={"project_path": folder.name, "study_id": study["study_id"]},
    )
    assert response.status_code == 422
    assert response.json()["diagnostics"][0]["code"] == "ENGINE_UNAVAILABLE"
    assert run_study(folder, study["study_id"], "pandapower", VoltageLimits()) == 2
    assert "ENGINE_UNAVAILABLE" in capsys.readouterr().err
    assert before == {p.name: p.read_bytes() for p in folder.iterdir()}
    assert not (folder / "out").exists()


def test_atomic_save_versions_assets_and_etag(project):
    folder, manifest = project
    c = client(folder)
    mid = manifest["models"][0]["model_id"]
    opened = c.get(
        "/api/model", params={"project_path": folder.name, "model_id": mid}
    ).json()
    body = {
        "project_path": folder.name,
        "model_id": mid,
        "etag": opened["etag"],
        "data": copy.deepcopy(opened["data"]),
    }
    foreign = (folder / "future.bin").read_bytes()
    body["data"]["name"] = "Updated authored name"
    response = c.post("/api/model/save", json=body)
    assert response.status_code == 200, response.json()
    assert (folder / "future.bin").read_bytes() == foreign
    assert c.post("/api/model/save", json=body).status_code == 409
    body["etag"] = response.json()["etag"]
    body["data"]["schema_version"] = "99.0.0"
    assert c.post("/api/model/save", json=body).status_code == 422
    body["data"]["schema_version"] = "0.1.0"
    # The referenced element cannot be removed, even when the rest of the model remains valid.
    key = "arrays" if folder.name == "pv" else "devices"
    if key == "devices":
        body["data"]["devices"] = [body["data"]["devices"][0]]
    else:
        body["data"]["arrays"][0]["array_id"] = "renamed"
    assert c.post("/api/model/save", json=body).status_code == 422
    assert (
        json.loads((folder / manifest["models"][0]["file"]).read_bytes())["name"]
        == "Updated authored name"
    )


def test_non_json_series_is_bounded_before_load(project):
    folder, manifest = project
    request = folder / manifest["studies"][0]["request_file"]
    data = json.loads(request.read_bytes())
    data["execution"]["input_series_file"] = "large.dat"
    request.write_text(json.dumps(data))
    (folder / "large.dat").write_bytes(b" " * 1001)
    response = client(folder, max_data_bytes=1000).get(
        "/api/project", params={"project_path": folder.name}
    )
    assert response.status_code == 413
    assert response.json()["diagnostics"][0]["code"] == "INPUT_LIMIT"


@pytest.mark.parametrize("name", ["../outside.dat", "/tmp/outside.dat"])
def test_series_path_is_confined(project, name):
    folder, manifest = project
    path = folder / manifest["studies"][0]["request_file"]
    data = json.loads(path.read_bytes())
    data["execution"]["input_series_file"] = name
    path.write_text(json.dumps(data))
    response = client(folder).get("/api/project", params={"project_path": folder.name})
    assert response.status_code == 422
    assert response.json()["diagnostics"][0]["code"] == "PROJECT_PATH"


def test_opaque_future_version_cannot_run_or_save(project):
    folder, manifest = project
    if folder.name != "plc":
        return  # Only PLC supports the archived CC-3 placeholder version.
    model = folder / manifest["models"][0]["file"]
    data = json.loads(model.read_bytes())
    data["schema_version"] = "future"
    model.write_text(json.dumps(data))
    req = folder / manifest["studies"][0]["request_file"]
    data = json.loads(req.read_bytes())
    data["schema_version"] = "future"
    req.write_text(json.dumps(data))
    c = client(folder)
    response = c.post(
        "/api/studies/run",
        json={
            "project_path": folder.name,
            "study_id": manifest["studies"][0]["study_id"],
        },
    )
    assert response.status_code == 422
    assert response.json()["diagnostics"][0]["code"] == "UNSUPPORTED_STUDY"


def test_worker_timeout_kills_and_releases_slot():
    runner = Runner(
        timeout_s=0.05,
        max_workers=1,
        command=[sys.executable, "-c", "import time; time.sleep(5)"],
    )
    for _ in range(2):
        with pytest.raises(WorkerError) as caught:
            runner.run({"study_type": "plc.scan"})
        assert caught.value.code == "STUDY_TIMEOUT"
    runner.command = [
        sys.executable,
        "-c",
        'print(\'{"error": true, "diagnostics": []}\')',
    ]
    assert runner.run({})["error"]


def test_worker_busy_and_invalid_response_release():
    runner = Runner(max_workers=1, command=[sys.executable, "-c", 'print("invalid")'])
    runner.slots.acquire()
    with pytest.raises(WorkerError) as caught:
        runner.run({})
    assert caught.value.code == "STUDY_BUSY"
    runner.slots.release()
    for _ in range(2):
        with pytest.raises(WorkerError) as caught:
            runner.run({})
        assert caught.value.code == "WORKER_FAILURE"


@pytest.mark.parametrize("stream", ["stdout", "stderr"])
def test_worker_output_bound_and_release(stream):
    runner = Runner(
        max_workers=1,
        max_output_bytes=500,
        max_stderr_bytes=500,
        command=[sys.executable, "-c", f'import sys; sys.{stream}.write("x" * 1000)'],
    )
    for _ in range(2):
        with pytest.raises(WorkerError) as caught:
            runner.run({})
        assert caught.value.code == "RESULT_LIMIT"
    runner.command = [
        sys.executable,
        "-c",
        'print(\'{"error": true, "diagnostics": []}\')',
    ]
    assert runner.run({})["error"]


def test_worker_input_bound_and_release():
    runner = Runner(
        max_input_bytes=20,
        command=[sys.executable, "-c", 'print(\'{"error": true, "diagnostics": []}\')'],
    )
    with pytest.raises(WorkerError) as caught:
        runner.run({"oversized": "x" * 100})
    assert caught.value.code == "INPUT_LIMIT"
    assert runner.run({})["error"]


def test_suite_response_validates_result_hashes_and_exports_pdf(monkeypatch):
    from qe_api.responses import study_response
    from qe_report.registry import REPORTS

    site, request, result = json.loads(
        (ROOT / "packages/ts/contracts/tests/pv-fixture.json").read_bytes()
    )
    payload = {
        "study_type": "pv.yield",
        "model_type": "pv.site",
        "model_id": "solar",
        "project_name": "Authored fixture",
        "model": site,
        "request": request,
        "input_files": copy.deepcopy(result["execution"]["input_files"]),
        "report_format": "pdf",
    }
    monkeypatch.setitem(
        REPORTS, "pv.yield", lambda **inputs: "# Authored report trace\n"
    )
    response = study_response(payload, result)
    assert response["report_markdown"] == "# Authored report trace\n"
    import base64

    assert base64.b64decode(response["report_pdf_base64"]).startswith(b"%PDF-")
    payload["input_files"][0]["sha256"] = "f" * 64
    assert (
        study_response(payload, result)["diagnostics"][0]["code"] == "RESULT_PROVENANCE"
    )
    assert study_response(payload, {})["error"]


def test_input_context_hashes_the_actual_bound_files(project):
    from qe_api.inputs import context as api_context
    from qe_cli.inputs import context as cli_context
    from qe_core import load_project

    folder, _ = project
    loaded = load_project(folder).value
    study = loaded.studies[0]
    model = loaded.model(study.model_id)
    left = api_context(folder, loaded, model, study)
    right = cli_context(folder, loaded, model, study)
    assert left == right
    assert [item["role"] for item in left["input_files"]] == [
        "model",
        "request",
        "data",
    ]
    for record in left["input_files"]:
        assert (
            record["sha256"]
            == hashlib.sha256((folder / record["path"]).read_bytes()).hexdigest()
        )


def test_generated_large_result_is_not_reloaded_as_input(project):
    folder, _ = project
    (folder / "out").mkdir()
    (folder / "out/results.json").write_bytes(b" " * 2_000_001)
    response = client(folder).get("/api/project", params={"project_path": folder.name})
    assert response.status_code == 200
