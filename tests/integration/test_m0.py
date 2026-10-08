"""Milestone M0: two independent load-flow solvers agree, and both are right.

The pandapower adapter (WP-0.6) and the textbook Newton-Raphson solver (WP-0.7)
share no solver code. For every fixture they must agree with each other, pass
the independent power-balance verifier, and match the closed-form reference.
Tolerances come from PLAN.md WP-0.10 and must not be loosened.
"""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

import pytest
from qe_cli.main import main
from qe_core import validate
from qe_power import textbook
from qe_power.adapters import pandapower
from qe_report.loadflow import source_outputs

REPO = Path(__file__).resolve().parents[2]
FIXTURES = REPO / "tests" / "fixtures" / "power"
NETWORKS = sorted(FIXTURES.glob("*/network.json"))
EXAMPLE = REPO / "examples" / "fourteen_bus"

SOLVERS = {"pandapower": pandapower.run_loadflow_file, "textbook": textbook.run_loadflow_file}
VM_TOLERANCE_PU = 1e-6
VA_TOLERANCE_DEGREE = 1e-4
# verify.py checks bus mismatch and energy balance against this bound.
MISMATCH_TOLERANCE_PU = 1e-8


def _load_verifier():
    spec = importlib.util.spec_from_file_location("m0_fixture_verify", FIXTURES / "verify.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.verify_loadflow_result


verify_loadflow_result = _load_verifier()


def request(name: str) -> dict:
    # A tight tolerance so the solver's own error sits far below the cross-check bounds.
    return {"schema_version": "0.1.0", "request_id": f"m0-{name}", "network_file": "network.json",
            "tolerance_mva": 1e-10, "max_iterations": 30, "initialization": "flat"}


@pytest.fixture(scope="module")
def results(tmp_path_factory):
    temporary = tmp_path_factory.mktemp("unconstrained-comparison")
    results = {}
    for path in NETWORKS:
        network = json.loads(path.read_text())
        has_bounds = any("q_min_mvar" in g or "q_max_mvar" in g for g in network["generators"])
        for generator in network["generators"]:
            generator.pop("q_min_mvar", None)
            generator.pop("q_max_mvar", None)
        comparison = temporary / (path.parent.name + ".json")
        # Retain exact reference bytes when no bounds need removing.
        comparison.write_bytes(json.dumps(network).encode() if has_bounds else path.read_bytes())
        results[path.parent.name] = {
            solver: run(comparison, request(path.parent.name)) for solver, run in SOLVERS.items()}
    return results


def test_required_fixtures_are_covered():
    # New fixtures join the cross-check automatically; these must never drop out.
    assert {path.parent.name for path in NETWORKS} >= {
        "two_bus_analytic", "three_bus_original", "three_bus_shunt", "five_bus_original",
        "fourteen_bus_original"}


@pytest.mark.parametrize("path", NETWORKS, ids=lambda p: p.parent.name)
def test_solvers_agree(results, path):
    pair = results[path.parent.name]
    for solver, result in pair.items():
        assert result["convergence"]["converged"], solver
        assert not validate(result, "power/loadflow-result"), solver
    ours, theirs = pair["pandapower"]["bus_results"], pair["textbook"]["bus_results"]
    for a, b in zip(ours, theirs, strict=True):
        assert a["bus_id"] == b["bus_id"]
        assert abs(a["vm_pu"] - b["vm_pu"]) < VM_TOLERANCE_PU, a["bus_id"]
        assert abs(a["va_degree"] - b["va_degree"]) < VA_TOLERANCE_DEGREE, a["bus_id"]


@pytest.mark.parametrize("solver", SOLVERS)
@pytest.mark.parametrize("path", NETWORKS, ids=lambda p: p.parent.name)
def test_solver_passes_verifier(results, path, solver):
    network = json.loads(path.read_text(encoding="utf-8"))
    summary = verify_loadflow_result(network, results[path.parent.name][solver], MISMATCH_TOLERANCE_PU)
    assert summary.max_bus_mismatch_pu < MISMATCH_TOLERANCE_PU
    assert abs(summary.energy_balance_error_mw) < MISMATCH_TOLERANCE_PU * network["base_mva"]


@pytest.mark.parametrize("solver", SOLVERS)
def test_solver_matches_closed_form_reference(results, solver):
    reference = json.loads((FIXTURES / "two_bus_analytic" / "reference.json").read_text(encoding="utf-8"))
    result = results["two_bus_analytic"][solver]
    for got, want in zip(result["bus_results"], reference["bus_results"], strict=True):
        assert got["bus_id"] == want["bus_id"]
        assert abs(got["vm_pu"] - want["vm_pu"]) < VM_TOLERANCE_PU
        assert abs(got["va_degree"] - want["va_degree"]) < VA_TOLERANCE_DEGREE
    base_mva = json.loads((FIXTURES / "two_bus_analytic" / "network.json").read_text())["base_mva"]
    for got, want in zip(result["branch_results"], reference["branch_results"], strict=True):
        assert got["branch_id"] == want["branch_id"]
        for field in ("p_from_mw", "q_from_mvar", "p_to_mw", "q_to_mvar", "p_loss_mw", "q_loss_mvar"):
            # Power flows checked to the same per-unit bound as the voltages.
            assert abs(got[field] - want[field]) < VM_TOLERANCE_PU * base_mva, field
    assert result["provenance"]["input_hash_sha256"] == reference["provenance"]["input_hash_sha256"]


# Report lines that legitimately differ between solvers: solver identity,
# timestamp and result ID. Section 8 lists each solver's own diagnostics and is
# compared separately.
_SOLVER_SPECIFIC = re.compile(r"^\| (Solver|Solver version|Run time \(UTC\)|Result) \|")


def _comparable_report(text: str) -> list[str]:
    before, _, rest = text.partition("## 8. Diagnostics")
    _, _, provenance = rest.partition("## 9. Provenance")
    assert provenance, "report layout changed: section 9 not found"
    return [line for line in (before + provenance).splitlines() if not _SOLVER_SPECIFIC.match(line)]


def test_cli_reports_match_for_both_solvers(tmp_path):
    reports = {}
    for solver in SOLVERS:
        project = tmp_path / solver
        shutil.copytree(EXAMPLE, project, ignore=shutil.ignore_patterns("out"))
        assert main(["study", "run", str(project), "--study", "loadflow", "--solver", solver]) == 0
        reports[solver] = (project / "out" / "report.md").read_text(encoding="utf-8")
    pandapower_report = _comparable_report(reports["pandapower"])
    textbook_report = _comparable_report(reports["textbook"])
    assert any(line.startswith("| bus-14 |") for line in pandapower_report)
    assert any(line.startswith("| Input SHA-256 |") for line in pandapower_report)
    assert pandapower_report == textbook_report
    # Neither solver reports an error-severity diagnostic on the example.
    for report in reports.values():
        diagnostics = report.partition("## 8. Diagnostics")[2].partition("## 9.")[0]
        assert "| error |" not in diagnostics


@pytest.mark.parametrize("solver", SOLVERS)
@pytest.mark.parametrize("tolerance_mva", [1e-10, 1e-4])
def test_fourteen_bus_generator_setpoints_are_feasible(solver, tolerance_mva):
    """M0 section 6: authored setpoints must satisfy the existing Q limits.

    Check both the strict integration and shipped CLI request tolerances.
    Reactive output is recovered independently from solved branch power balance.
    These feasible targets need no PV to PQ switching in the constrained adapter.
    """
    path = FIXTURES / "fourteen_bus_original" / "network.json"
    assert path.read_bytes() == (EXAMPLE / "network.json").read_bytes()
    network = json.loads(path.read_text(encoding="utf-8"))
    study = request("fourteen-bus-feasibility")
    study["tolerance_mva"] = tolerance_mva
    result = SOLVERS[solver](path, study)
    assert result["convergence"]["converged"]
    sources = {s["source_id"]: s for s in source_outputs(network, result)}
    for generator in network["generators"]:
        output = sources[generator["generator_id"]]
        assert not output["shared_bus"]
        assert generator["q_min_mvar"] <= output["q_mvar"] <= generator["q_max_mvar"]
        assert output["q_check"] == "ok"
    # Existing report defaults, not new engineering limits (PLAN.md WP-0.9).
    assert all(0.95 <= bus["vm_pu"] <= 1.05 for bus in result["bus_results"])
