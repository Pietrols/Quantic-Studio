from __future__ import annotations

import json
import math
from pathlib import Path

import pytest
from qe_core import validate
from qe_power.textbook import run_loadflow_file
from verify import verify_loadflow_result

REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
FIXTURE_ROOT = REPOSITORY_ROOT / "tests" / "fixtures" / "power"


def request_for(network_file: str, request_id: str) -> dict:
    return {
        "schema_version": "0.1.0",
        "request_id": request_id,
        "network_file": network_file,
        "tolerance_mva": 1e-8,
        "max_iterations": 30,
        "initialization": "flat",
    }


def load_network(fixture_name: str) -> tuple[Path, dict]:
    network_path = FIXTURE_ROOT / fixture_name / "network.json"
    return network_path, json.loads(network_path.read_text(encoding="utf-8"))


def diagnostic_history(result: dict) -> list[float]:
    history_diagnostics = [
        item for item in result["diagnostics"]
        if item["code"] == "ITERATION_MISMATCH_HISTORY"
    ]
    assert len(history_diagnostics) == 1
    message = history_diagnostics[0]["message"]
    return json.loads(message.removeprefix("mismatch_history_pu="))


def test_two_bus_solution_matches_closed_form_reference() -> None:
    fixture_path = FIXTURE_ROOT / "two_bus_analytic"
    network_path = fixture_path / "network.json"
    network = json.loads(network_path.read_text(encoding="utf-8"))
    reference = json.loads((fixture_path / "reference.json").read_text(encoding="utf-8"))
    result = run_loadflow_file(
        network_path,
        request_for("network.json", "two-bus-textbook"),
    )
    assert result["convergence"]["converged"] is True
    assert validate(result, "power/loadflow-result") == []
    assert verify_loadflow_result(network, result).max_bus_mismatch_pu < 1e-8
    expected_by_bus = {item["bus_id"]: item for item in reference["bus_results"]}
    for bus_result in result["bus_results"]:
        expected = expected_by_bus[bus_result["bus_id"]]
        assert math.isclose(bus_result["vm_pu"], expected["vm_pu"], abs_tol=1e-12)
        assert math.isclose(bus_result["va_degree"], expected["va_degree"], abs_tol=1e-12)
    assert result["provenance"]["input_hash_sha256"] == reference["provenance"]["input_hash_sha256"]


def test_three_bus_converges_and_records_each_iteration() -> None:
    network_path, network = load_network("three_bus_original")
    result = run_loadflow_file(
        network_path,
        request_for("network.json", "three-bus-iteration-test"),
    )
    assert result["convergence"]["converged"] is True
    assert validate(result, "power/loadflow-result") == []
    assert verify_loadflow_result(network, result).max_bus_mismatch_pu < 1e-8
    history = diagnostic_history(result)
    assert len(history) == result["convergence"]["iterations"] + 1
    assert history[0] > history[-1]
    assert history[-1] < 1e-8 / network["base_mva"]


@pytest.mark.parametrize("fixture_name", ["five_bus_original", "fourteen_bus_original"])
def test_cross_check_network_converges_and_returns_contract(fixture_name: str) -> None:
    network_path, network = load_network(fixture_name)
    result = run_loadflow_file(
        network_path,
        request_for("network.json", f"{fixture_name}-cross-check"),
    )
    assert result["convergence"]["converged"] is True
    assert validate(result, "power/loadflow-result") == []
    assert verify_loadflow_result(network, result).max_bus_mismatch_pu < 1e-8
    assert len(result["bus_results"]) == len(network["buses"])
    assert len(result["branch_results"]) == len(network["lines"]) + len(network["transformers"])
