from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from qe_cli.main import main, run_study
from qe_core import validate
from qe_report import VoltageLimits

REPO = Path(__file__).resolve().parents[4]
FIXTURES = REPO / "tests" / "fixtures" / "power"
EXAMPLE = REPO / "examples" / "fourteen_bus"


def make_project(tmp_path: Path, fixture: str, max_iterations: int = 20,
                 tolerance_mva: float = 0.0001) -> Path:
    folder = tmp_path / fixture
    folder.mkdir()
    shutil.copy(FIXTURES / fixture / "network.json", folder / "network.json")
    (folder / "manifest.json").write_text(json.dumps({
        "schema_version": "0.1.0", "name": fixture, "network_file": "network.json",
        "studies": [{"study_id": "lf", "study_type": "loadflow",
                     "request_file": "request.json"}],
    }), encoding="utf-8")
    (folder / "request.json").write_text(json.dumps({
        "schema_version": "0.1.0", "request_id": f"{fixture}-lf",
        "network_file": "network.json", "tolerance_mva": tolerance_mva,
        "max_iterations": max_iterations, "initialization": "flat",
    }), encoding="utf-8")
    return folder


def test_example_network_is_an_exact_copy_of_the_fixture():
    assert (EXAMPLE / "network.json").read_bytes() == (
        FIXTURES / "fourteen_bus_original" / "network.json").read_bytes()


@pytest.mark.parametrize("fixture", ["two_bus_analytic", "three_bus_original",
                                     "five_bus_original", "fourteen_bus_original"])
def test_textbook_run_writes_valid_results_and_report(tmp_path, fixture):
    folder = make_project(tmp_path, fixture)
    code = main(["study", "run", str(folder), "--study", "loadflow", "--solver", "textbook"])
    assert code == 0
    result = json.loads((folder / "out" / "results.json").read_text(encoding="utf-8"))
    assert validate(result, "power/loadflow-result") == []
    report = (folder / "out" / "report.md").read_text(encoding="utf-8")
    assert report.startswith(f"# Load-flow study: {fixture}")
    assert "CONVERGED" in report


def test_two_bus_cli_result_matches_closed_form(tmp_path):
    folder = make_project(tmp_path, "two_bus_analytic", tolerance_mva=1e-9)
    assert main(["study", "run", str(folder), "--study", "lf", "--solver", "textbook"]) == 0
    result = json.loads((folder / "out" / "results.json").read_text(encoding="utf-8"))
    reference = json.loads((FIXTURES / "two_bus_analytic" / "reference.json").read_text())
    got = {b["bus_id"]: b for b in result["bus_results"]}
    for bus in reference["bus_results"]:
        assert got[bus["bus_id"]]["vm_pu"] == pytest.approx(bus["vm_pu"], abs=1e-9)
        assert got[bus["bus_id"]]["va_degree"] == pytest.approx(bus["va_degree"], abs=1e-7)


def test_non_convergence_exits_1_but_still_reports(tmp_path):
    folder = make_project(tmp_path, "fourteen_bus_original", max_iterations=1,
                          tolerance_mva=1e-12)
    code = main(["study", "run", str(folder), "--study", "loadflow", "--solver", "textbook"])
    assert code == 1
    report = (folder / "out" / "report.md").read_text(encoding="utf-8")
    assert "NOT CONVERGED" in report


def test_invalid_project_exits_2_and_writes_nothing(tmp_path, capsys):
    folder = make_project(tmp_path, "two_bus_analytic")
    network = json.loads((folder / "network.json").read_text())
    network["lines"][0]["to_bus"] = "nowhere"
    (folder / "network.json").write_text(json.dumps(network))
    assert main(["study", "run", str(folder), "--study", "loadflow", "--solver", "textbook"]) == 2
    assert "UNKNOWN_BUS" in capsys.readouterr().err
    assert not (folder / "out").exists()


def test_unknown_study_exits_2(tmp_path, capsys):
    folder = make_project(tmp_path, "two_bus_analytic")
    assert main(["study", "run", str(folder), "--study", "shortcircuit",
                 "--solver", "textbook"]) == 2
    assert "STUDY_SELECTION" in capsys.readouterr().err


def test_missing_solver_exits_3(tmp_path, capsys):
    folder = make_project(tmp_path, "two_bus_analytic")

    def unavailable(name):
        raise ImportError(f"No module for {name}")

    assert run_study(folder, "loadflow", "pandapower", VoltageLimits(), unavailable) == 3
    assert "SOLVER_UNAVAILABLE" in capsys.readouterr().err


def test_bad_voltage_band_exits_2(tmp_path):
    folder = make_project(tmp_path, "two_bus_analytic")
    assert main(["study", "run", str(folder), "--study", "loadflow", "--solver", "textbook",
                 "--vmin", "1.1", "--vmax", "1.0"]) == 2


@pytest.mark.parametrize("solver", ["textbook", "pandapower"])
def test_solver_input_error_exits_2_without_traceback(tmp_path, capsys, solver):
    # Zero series impedance passes the schema but no solver can model it.
    folder = make_project(tmp_path, "two_bus_analytic")
    network = json.loads((folder / "network.json").read_text())
    network["lines"][0]["r_ohm_per_km"] = 0.0
    network["lines"][0]["x_ohm_per_km"] = 0.0
    (folder / "network.json").write_text(json.dumps(network))
    assert main(["study", "run", str(folder), "--study", "loadflow", "--solver", solver]) == 2
    err = capsys.readouterr().err
    assert "ERROR" in err and "Traceback" not in err
    assert not (folder / "out").exists()


@pytest.mark.parametrize("fixture", ["two_bus_analytic", "three_bus_original",
                                     "five_bus_original", "fourteen_bus_original"])
def test_both_solvers_agree_through_the_cli(tmp_path, fixture):
    results = {}
    for solver in ("textbook", "pandapower"):
        base = tmp_path / solver
        base.mkdir()
        folder = make_project(base, fixture, tolerance_mva=1e-9)
        assert main(["study", "run", str(folder), "--study", "loadflow",
                     "--solver", solver]) == 0
        data = json.loads((folder / "out" / "results.json").read_text(encoding="utf-8"))
        results[solver] = {b["bus_id"]: b for b in data["bus_results"]}
    for bus_id, bus in results["textbook"].items():
        other = results["pandapower"][bus_id]
        assert bus["vm_pu"] == pytest.approx(other["vm_pu"], abs=1e-8)
        assert bus["va_degree"] == pytest.approx(other["va_degree"], abs=1e-6)
