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


def test_shunt_is_a_constant_admittance() -> None:
    # docs/specs/network.md defines shunt power at nominal voltage, so the solved
    # shunt reactive power must scale with |V|^2 rather than stay at q_mvar.
    network_path, network = load_network("three_bus_shunt")
    result = run_loadflow_file(network_path, request_for("network.json", "three-bus-shunt"))
    assert result["convergence"]["converged"] is True
    assert validate(result, "power/loadflow-result") == []
    assert verify_loadflow_result(network, result).max_bus_mismatch_pu < 1e-8

    shunt = network["shunts"][0]
    voltages = {
        item["bus_id"]: item["vm_pu"] * complex(
            math.cos(math.radians(item["va_degree"])), math.sin(math.radians(item["va_degree"]))
        )
        for item in result["bus_results"]
    }
    # Kirchhoff's current law at the shunt bus: load and shunt consumption must
    # equal the sum of power leaving the bus into its branches, negated.
    bus_id = shunt["bus_id"]
    branch_injection_mva = 0j
    for line, branch in zip(network["lines"], result["branch_results"], strict=False):
        assert line["line_id"] == branch["branch_id"]
        if line["from_bus"] == bus_id:
            branch_injection_mva += complex(branch["p_from_mw"], branch["q_from_mvar"])
        elif line["to_bus"] == bus_id:
            branch_injection_mva += complex(branch["p_to_mw"], branch["q_to_mvar"])
    load = next(item for item in network["loads"] if item["bus_id"] == bus_id)
    vm_squared = abs(voltages[bus_id]) ** 2
    shunt_consumption_mva = -branch_injection_mva - complex(load["p_mw"], load["q_mvar"])
    assert math.isclose(shunt_consumption_mva.real, shunt["p_mw"] * vm_squared, abs_tol=1e-8)
    assert math.isclose(shunt_consumption_mva.imag, shunt["q_mvar"] * vm_squared, abs_tol=1e-8)
    assert not math.isclose(vm_squared, 1.0, abs_tol=1e-6)


def test_shunt_case_matches_pandapower() -> None:
    # Black-box comparison through the public adapter API only.
    from qe_power.adapters.pandapower import run_loadflow_file as run_pandapower_file

    network_path, _ = load_network("three_bus_shunt")
    request = request_for("network.json", "three-bus-shunt-compare")
    ours = run_loadflow_file(network_path, request)
    theirs = run_pandapower_file(network_path, request)
    assert ours["convergence"]["converged"] and theirs["convergence"]["converged"]
    for got, want in zip(ours["bus_results"], theirs["bus_results"], strict=True):
        assert got["bus_id"] == want["bus_id"]
        assert math.isclose(got["vm_pu"], want["vm_pu"], abs_tol=1e-9)
        assert math.isclose(got["va_degree"], want["va_degree"], abs_tol=1e-7)


@pytest.mark.parametrize("setpoints", [(1.01, 1.005), (0.9998, 0.9693)])
def test_fourteen_bus_loading_from_solved_terminal_values(tmp_path: Path, setpoints: tuple) -> None:
    # Peter's three-phase current formula, docs/specs/loadflow-result.md.
    # This original synthetic network provides terminal powers and voltages;
    # the expected loading is calculated independently from those public results.
    _, network = load_network("fourteen_bus_original")
    for generator, vm_pu in zip(network["generators"], setpoints, strict=True):
        generator["vm_setpoint_pu"] = vm_pu
    # Exercise the contract's null loading when no line rating is supplied.
    network["lines"][0].pop("max_current_ka", None)
    path = tmp_path / "network.json"
    path.write_text(json.dumps(network), encoding="utf-8")
    result = run_loadflow_file(path, request_for("network.json", "terminal-loading"))
    assert result["convergence"]["converged"]
    assert validate(result, "power/loadflow-result") == []
    nominal = {bus["bus_id"]: bus["vn_kv"] for bus in network["buses"]}
    voltage_kv = {
        bus["bus_id"]: bus["vm_pu"] * nominal[bus["bus_id"]]
        for bus in result["bus_results"]
    }
    branches = {branch["branch_id"]: branch for branch in result["branch_results"]}
    for transformer in network["transformers"]:
        branch = branches[transformer["transformer_id"]]
        hv_current = math.hypot(branch["p_from_mw"], branch["q_from_mvar"]) / (
            math.sqrt(3) * voltage_kv[transformer["hv_bus"]]
        )
        lv_current = math.hypot(branch["p_to_mw"], branch["q_to_mvar"]) / (
            math.sqrt(3) * voltage_kv[transformer["lv_bus"]]
        )
        hv_rated = transformer["sn_mva"] / (math.sqrt(3) * transformer["vn_hv_kv"])
        lv_rated = transformer["sn_mva"] / (math.sqrt(3) * transformer["vn_lv_kv"])
        expected = 100 * max(hv_current / hv_rated, lv_current / lv_rated)
        assert branch["loading_pct"] == pytest.approx(expected, rel=0, abs=1e-9)
    for line in network["lines"]:
        branch = branches[line["line_id"]]
        if "max_current_ka" not in line:
            assert branch["loading_pct"] is None
            continue
        from_current = math.hypot(branch["p_from_mw"], branch["q_from_mvar"]) / (
            math.sqrt(3) * voltage_kv[line["from_bus"]]
        )
        to_current = math.hypot(branch["p_to_mw"], branch["q_to_mvar"]) / (
            math.sqrt(3) * voltage_kv[line["to_bus"]]
        )
        expected = 100 * max(from_current, to_current) / line["max_current_ka"]
        assert branch["loading_pct"] == pytest.approx(expected, rel=0, abs=1e-9)
