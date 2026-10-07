import copy
import math

import pytest
from qe_core import validate
from qe_power.adapters.pandapower import solve


def network():
    # Synthetic analytical reference, derived in this WP's learning note.
    return {"schema_version": "0.1.0", "network_id": "resistive-two-bus", "base_mva": 1,
            "buses": [{"bus_id": "s", "vn_kv": 1, "bus_type": "slack"}, {"bus_id": "l", "vn_kv": 1, "bus_type": "pq"}],
            "lines": [{"line_id": "r", "from_bus": "s", "to_bus": "l", "length_km": 1,
                       "r_ohm_per_km": 0.1, "x_ohm_per_km": 0, "max_current_ka": 1}],
            "loads": [{"load_id": "d", "bus_id": "l", "p_mw": 0.9, "q_mvar": 0}],
            "external_grids": [{"external_grid_id": "g", "bus_id": "s", "vm_setpoint_pu": 1, "va_setpoint_degree": 0}],
            "transformers": [], "generators": [], "shunts": []}


def request(**updates):
    return {"schema_version": "0.1.0", "request_id": "lf", "network_file": "network.json",
            "tolerance_mva": 1e-10, "max_iterations": 30, **updates}


def test_analytical_two_bus():
    result = solve(network(), request())
    assert result.ok, result.diagnostics
    data = result.value
    assert data["convergence"]["converged"]
    assert data["bus_results"][1]["vm_pu"] == pytest.approx(0.9, abs=1e-9)
    assert data["branch_results"][0]["p_loss_mw"] == pytest.approx(0.1, abs=1e-9)
    assert data["convergence"]["largest_mismatch_mva"] <= 1e-10
    assert not validate(data, "power/loadflow-result")


def test_nonconvergence_has_contract_result():
    # Above Pmax = Vs^2/(4R) = 2.5 pu there is no real two-bus solution.
    data = network()
    data["loads"][0]["p_mw"] = 3
    result = solve(data, request(max_iterations=1))
    assert result.value is not None, result.diagnostics
    assert not result.value["convergence"]["converged"]
    assert result.value["convergence"]["iterations"] == 1
    assert result.value["convergence"]["largest_mismatch_mva"] > 0
    assert any(d.code == "LOADFLOW_NOT_CONVERGED" for d in result.diagnostics)
    assert not validate(result.value, "power/loadflow-result")


def test_no_load_transformer_ratio_phase():
    data = network()
    data["lines"] = []
    data["loads"] = []
    data["transformers"] = [{"transformer_id": "t", "hv_bus": "s", "lv_bus": "l", "sn_mva": 1,
        "vn_hv_kv": 1, "vn_lv_kv": 1, "r_pu": 0, "x_pu": 0.1, "tap_ratio": 1.1, "phase_shift_degree": 10}]
    result = solve(data, request())
    assert result.ok, result.diagnostics
    assert result.value["bus_results"][1]["vm_pu"] == pytest.approx(1/1.1, abs=1e-9)
    assert result.value["bus_results"][1]["va_degree"] == pytest.approx(-10, abs=1e-8)


def test_line_charging_and_shunt_cancel():
    data = network()
    data["loads"] = []
    # At 1 kV, B=1 uS consumes -1e-6 Mvar per terminal for total B=2 uS.
    data["lines"][0]["b_us_per_km"] = 2
    data["shunts"] = [{"shunt_id": "c", "bus_id": "l", "p_mw": 0, "q_mvar": 1e-6}]
    result = solve(data, request())
    assert result.ok, result.diagnostics
    assert result.value["bus_results"][1]["vm_pu"] == pytest.approx(1, abs=1e-9)
    assert result.value["bus_results"][1]["va_degree"] == pytest.approx(0, abs=1e-9)


@pytest.mark.parametrize("mutation,code", [
    (lambda n: n["buses"][1].update(vn_kv=-1), "SCHEMA_INVALID"),
    (lambda n: n["external_grids"].clear(), "SLACK_COUNT"),
    (lambda n: n["lines"].clear(), "SLACK_COUNT"),
    (lambda n: n["lines"][0].update(r_ohm_per_km=0), "UNSUPPORTED_IMPEDANCE"),
])
def test_invalid_input(mutation, code):
    data = network()
    mutation(data)
    result = solve(data, request())
    assert result.value is None and any(d.code == code for d in result.diagnostics)


def test_unsupported_initialization():
    result = solve(network(), request(initialization="previous_result"))
    assert result.value is None and result.diagnostics[0].code == "UNSUPPORTED_INITIALIZATION"


def test_inputs_unchanged_and_provenance_changes():
    data = network()
    original = copy.deepcopy(data)
    first = solve(data, request()).value
    assert data == original
    second = solve(data, request(tolerance_mva=1e-9)).value
    assert first["provenance"]["input_hash_sha256"] != second["provenance"]["input_hash_sha256"]
    assert math.isfinite(first["convergence"]["largest_mismatch_mva"])
