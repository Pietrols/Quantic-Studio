import importlib.util
import json
import sys
from pathlib import Path

import pytest
from qe_core import validate
from qe_power import textbook
from qe_power.adapters.pandapower import LoadflowInputError, run_loadflow_file

FIXTURES = Path(__file__).resolve().parents[5] / "tests" / "fixtures" / "power"
NETWORKS = sorted(FIXTURES.glob("*/network.json"))


def _verifier():
    # Load the shared fixture verifier by path, so this test needs no sys.path changes.
    spec = importlib.util.spec_from_file_location("power_fixture_verify", FIXTURES / "verify.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.verify_loadflow_result


verify_loadflow_result = _verifier()


def request(**updates):
    return {"schema_version": "0.1.0", "request_id": "lf", "network_file": "network.json",
            "tolerance_mva": 1e-10, "max_iterations": 30, **updates}


def test_fixtures_exist():
    assert {p.parent.name for p in NETWORKS} >= {
        "two_bus_analytic", "three_bus_original", "five_bus_original", "fourteen_bus_original"}


@pytest.mark.parametrize("path", NETWORKS, ids=lambda p: p.parent.name)
def test_fixture_converges_and_verifies(path):
    result = run_loadflow_file(path, request())
    assert result["convergence"]["converged"]
    assert not validate(result, "power/loadflow-result")
    network = json.loads(path.read_text())
    summary = verify_loadflow_result(network, result, mismatch_tolerance_pu=1e-8)
    assert summary.max_bus_mismatch_pu < 1e-8
    assert abs(summary.energy_balance_error_mw) < 1e-8 * network["base_mva"]
    assert not any(d["severity"] == "error" for d in result["diagnostics"])


def test_two_bus_matches_closed_form_reference():
    path = FIXTURES / "two_bus_analytic" / "network.json"
    reference = json.loads((path.parent / "reference.json").read_text())
    result = run_loadflow_file(path, request())
    for got, want in zip(result["bus_results"], reference["bus_results"], strict=True):
        assert got["bus_id"] == want["bus_id"]
        assert got["vm_pu"] == pytest.approx(want["vm_pu"], abs=1e-10)
        assert got["va_degree"] == pytest.approx(want["va_degree"], abs=1e-8)
    for got, want in zip(result["branch_results"], reference["branch_results"], strict=True):
        assert got["branch_id"] == want["branch_id"] and got["branch_type"] == want["branch_type"]
        for field in ("p_from_mw", "q_from_mvar", "p_to_mw", "q_to_mvar", "p_loss_mw", "q_loss_mvar"):
            assert got[field] == pytest.approx(want[field], abs=1e-9), field
        assert got["loading_pct"] is None
    assert result["provenance"]["input_hash_sha256"] == reference["provenance"]["input_hash_sha256"]


@pytest.mark.parametrize("path", NETWORKS, ids=lambda p: p.parent.name)
def test_same_shape_as_textbook_solver(path):
    ours = run_loadflow_file(path, request())
    theirs = textbook.run_loadflow_file(path, request())
    assert ours.keys() == theirs.keys()
    assert ours["convergence"].keys() == theirs["convergence"].keys()
    assert ours["provenance"].keys() == theirs["provenance"].keys()
    assert ours["provenance"]["input_hash_sha256"] == theirs["provenance"]["input_hash_sha256"]
    assert [b["bus_id"] for b in ours["bus_results"]] == [b["bus_id"] for b in theirs["bus_results"]]
    assert [b["branch_id"] for b in ours["branch_results"]] == [b["branch_id"] for b in theirs["branch_results"]]
    for a, b in zip(ours["branch_results"], theirs["branch_results"], strict=True):
        assert a.keys() == b.keys()


def test_nonconverging_file_returns_result(tmp_path):
    network = json.loads((FIXTURES / "two_bus_analytic" / "network.json").read_text())
    # Far beyond the line's maximum transfer: no load-flow solution exists.
    network["loads"][0]["p_mw"] = 500
    path = tmp_path / "network.json"
    path.write_text(json.dumps(network))
    result = run_loadflow_file(path, request())
    assert not validate(result, "power/loadflow-result")
    assert result["convergence"]["converged"] is False
    assert result["convergence"]["iterations"] == 30
    codes = [d["code"] for d in result["diagnostics"]]
    assert "NON_CONVERGENCE" in codes
    message = next(d["message"] for d in result["diagnostics"] if d["code"] == "NON_CONVERGENCE")
    assert "voltage collapse" in message


def test_unsupported_fields_are_reported(tmp_path):
    network = json.loads((FIXTURES / "five_bus_original" / "network.json").read_text())
    network["buses"][2]["vm_pu"] = 0.99
    network["shunts"] = [{"shunt_id": "cap", "bus_id": "bus-5", "p_mw": 0.0, "q_mvar": -0.1}]
    path = tmp_path / "network.json"
    path.write_text(json.dumps(network))
    result = run_loadflow_file(path, request())
    refs = {(d["code"], d["element_ref"]["element_id"], d["element_ref"]["field"]) for d in result["diagnostics"]}
    assert ("REFERENCE_NOT_INITIALIZATION", "bus-3", "vm_pu") in refs
    assert ("SHUNT_MODEL", "cap", "q_mvar") in refs
    assert ("TRANSFORMER_MODEL", "transformer-3-4", "magnetizing") in refs
    for gen in network["generators"]:
        for field in ("p_min_mw", "p_max_mw"):
            assert ("LIMIT_NOT_ENFORCED", gen["generator_id"], field) in refs


def test_invalid_file_raises_diagnostics(tmp_path):
    path = tmp_path / "network.json"
    path.write_text("{not json")
    with pytest.raises(LoadflowInputError) as error:
        run_loadflow_file(path, request())
    assert error.value.diagnostics[0].code == "INPUT_READ"
    network = json.loads((FIXTURES / "two_bus_analytic" / "network.json").read_text())
    network["external_grids"].clear()
    path.write_text(json.dumps(network))
    with pytest.raises(LoadflowInputError) as error:
        run_loadflow_file(path, request())
    assert {d.code for d in error.value.diagnostics} >= {"SLACK_COUNT", "BUS_CONTROL"}
