"""Exercise contracts, project IO, CLI, solver and report together."""
import json
import shutil
from pathlib import Path

import pytest
from qe_cli.main import main
from qe_core import validate

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples" / "shortcircuit"


def project(tmp_path, *, transformer=False):
    folder = tmp_path / "project"
    folder.mkdir()
    source = EXAMPLE / "transformer" if transformer else EXAMPLE
    for name in ("network.json", "manifest.json", "shortcircuit-request.json"):
        shutil.copy(source / name, folder / name)
    return folder


@pytest.mark.parametrize("transformer", [False, True])
def test_cli_success_writes_contract_result_and_full_report(tmp_path, transformer):
    folder = project(tmp_path, transformer=transformer)
    original = {p.name: p.read_bytes() for p in folder.iterdir()}
    assert main(["study", "run", str(folder), "--study", "shortcircuit"]) == 0
    result = json.loads((folder / "out/results.json").read_text())
    assert validate(result, "power/shortcircuit-result") == []
    assert [c["case"] for c in result["case_results"]] == (["max"] if transformer else ["max", "min"])
    assert all({b["bus_id"] for b in c["bus_results"]} == {"hv", "lv"} for c in result["case_results"])
    report = (folder / "out/report.md").read_text()
    for expected in ("SUCCESS", "Maximum case", "Ik''", "kA RMS", "Fault duration (s)",
                     "Frequency (Hz)", "LV tolerance (%)", "Equipment inputs", "Provenance", "input_hash_sha256"):
        assert expected in report
    assert transformer or "Minimum case" in report
    assert all((folder / name).read_bytes() == data for name, data in original.items())


def test_partial_duties_exit_1_write_nulls_and_visible_diagnostics(tmp_path, capsys):
    folder = project(tmp_path)
    path = folder / "shortcircuit-request.json"
    request = json.loads(path.read_text())
    request["frequency_hz"] = 60
    path.write_text(json.dumps(request))
    assert main(["study", "run", str(folder), "--study", "shortcircuit"]) == 1
    result = json.loads((folder / "out/results.json").read_text())
    assert validate(result, "power/shortcircuit-result") == []
    assert result["status"] == "partial"
    assert "THERMAL_FREQUENCY_UNAVAILABLE" in capsys.readouterr().err
    report = (folder / "out/report.md").read_text()
    assert "PARTIAL" in report and "n/a" in report and "THERMAL_FREQUENCY_UNAVAILABLE" in report
    assert "buses:hv.ith_ka" in report


def test_valid_but_missing_fault_inputs_exit_1_with_failed_report(tmp_path):
    folder = project(tmp_path)
    path = folder / "network.json"
    network = json.loads(path.read_text())
    del network["external_grids"][0]["s_sc_max_mva"]
    del network["external_grids"][0]["s_sc_min_mva"]
    path.write_text(json.dumps(network))
    assert main(["study", "run", str(folder), "--study", "shortcircuit"]) == 1
    result = json.loads((folder / "out/results.json").read_text())
    assert result["status"] == "failed"
    assert validate(result, "power/shortcircuit-result") == []
    assert "FAILED" in (folder / "out/report.md").read_text()


def test_textbook_fault_solver_is_explicitly_unsupported(tmp_path, capsys):
    folder = project(tmp_path)
    assert main(["study", "run", str(folder), "--study", "shortcircuit", "--solver", "textbook"]) == 2
    assert "UNSUPPORTED_SOLVER" in capsys.readouterr().err
    assert not (folder / "out").exists()


def test_bad_schema_exits_2_without_outputs(tmp_path, capsys):
    folder = project(tmp_path)
    path = folder / "shortcircuit-request.json"
    request = json.loads(path.read_text())
    request["frequency_hz"] = 45
    path.write_text(json.dumps(request))
    assert main(["study", "run", str(folder), "--study", "shortcircuit"]) == 2
    assert "SCHEMA_INVALID" in capsys.readouterr().err
    assert not (folder / "out").exists()


def test_unavailable_fault_solver_exits_3(tmp_path, monkeypatch, capsys):
    from qe_cli import main as cli_module

    folder = project(tmp_path)

    def missing(*args):
        raise ImportError("synthetic missing engine")

    monkeypatch.setattr(cli_module.importlib, "import_module", missing)
    assert main(["study", "run", str(folder), "--study", "shortcircuit"]) == 3
    assert "SOLVER_UNAVAILABLE" in capsys.readouterr().err
    assert not (folder / "out").exists()


def test_contract_valid_but_wrong_bus_coverage_is_rejected(tmp_path, monkeypatch, capsys):
    from qe_power.adapters import pandapower as solver_module

    folder = project(tmp_path)
    original = solver_module.run_shortcircuit_file

    def wrong_coverage(path, request):
        result = original(path, request)
        for case in result["case_results"]:
            case["bus_results"][0]["bus_id"] = "unrequested-bus"
        assert validate(result, "power/shortcircuit-result") == []
        return result

    monkeypatch.setattr(solver_module, "run_shortcircuit_file", wrong_coverage)
    assert main(["study", "run", str(folder), "--study", "shortcircuit"]) == 2
    assert "RESULT_COVERAGE" in capsys.readouterr().err
    assert not (folder / "out").exists()
