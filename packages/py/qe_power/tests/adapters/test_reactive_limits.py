"""Independent authored reference: Q = V(V-1)/X, P=0 across jX.

See docs/learning/generator-reactive-limits.md for the derivation. No solved
outputs or standard tables are used as expected values.
"""
import hashlib
import json
import math
from pathlib import Path

import pytest
from qe_core import validate
from qe_power.adapters.pandapower import run_loadflow_file, solve
from test_pandapower import network, request


def controlled_network(setpoint=1.1, **limits):
    data = network()
    data["loads"] = []
    data["buses"][1]["bus_type"] = "pv"
    data["lines"][0].update(r_ohm_per_km=0, x_ohm_per_km=0.1)
    data["generators"] = [{"generator_id": "gen", "bus_id": "l", "p_mw": 0,
                           "vm_setpoint_pu": setpoint, **limits}]
    return data


@pytest.mark.parametrize("setpoint,limit,field", [(1.1, 0.2, "q_max_mvar"), (0.9, -0.2, "q_min_mvar")])
def test_hand_derived_pq_voltage(setpoint, limit, field):
    data = controlled_network(setpoint, **{field: limit})
    outcome = solve(data, request())
    assert outcome.ok, outcome.diagnostics
    result = outcome.value
    # Positive high-voltage root of V^2 - V - X Q = 0, on 1 MVA/1 kV bases.
    expected = (1 + math.sqrt(1 + 4 * 0.1 * limit)) / 2
    assert result["bus_results"][1]["vm_pu"] == pytest.approx(expected, abs=1e-10)
    assert result["bus_results"][1]["va_degree"] == pytest.approx(0, abs=1e-10)
    assert result["branch_results"][0]["q_to_mvar"] == pytest.approx(limit, abs=1e-10)
    assert result["convergence"]["largest_mismatch_mva"] < 1e-10
    notes = [d for d in outcome.diagnostics if d.code == "GENERATOR_Q_LIMIT"]
    assert len(notes) == 1
    assert notes[0].element_ref == {"element_type": "generators", "element_id": "gen", "field": field}
    assert str(limit) in notes[0].message and "voltage" in notes[0].message
    assert not validate(result, "power/loadflow-result")


@pytest.mark.parametrize("limits", [{}, {"q_min_mvar": -2, "q_max_mvar": 2}, {"q_min_mvar": -2}])
def test_unconstrained_generator_retains_pv(limits):
    outcome = solve(controlled_network(**limits), request())
    assert outcome.ok
    assert outcome.value["bus_results"][1]["vm_pu"] == pytest.approx(1.1, abs=1e-10)
    assert outcome.value["branch_results"][0]["q_to_mvar"] == pytest.approx(1.1, abs=1e-10)
    assert not any(d.code == "GENERATOR_Q_LIMIT" for d in outcome.diagnostics)


def test_reversed_limits_diagnostic():
    outcome = solve(controlled_network(q_min_mvar=1, q_max_mvar=-1), request())
    assert outcome.value is None
    assert any(d.code == "GENERATOR_Q_RANGE" and d.element_ref["element_id"] == "gen"
               and d.element_ref["field"] == "q_min_mvar" for d in outcome.diagnostics)


def test_equal_limits_produce_one_diagnostic():
    outcome = solve(controlled_network(q_min_mvar=0.2, q_max_mvar=0.2), request())
    assert outcome.ok
    assert len([d for d in outcome.diagnostics if d.code == "GENERATOR_Q_LIMIT"]) == 1


def test_original_fourteen_bus_setpoints_in_temporary_copy(tmp_path):
    path = Path(__file__).resolve().parents[5] / "examples/fourteen_bus/network.json"
    original = path.read_bytes()
    data = json.loads(original)
    for gen, voltage in zip(data["generators"], [1.010, 1.005], strict=True):
        gen["vm_setpoint_pu"] = voltage
    temporary = tmp_path / "network.json"
    temporary.write_text(json.dumps(data))
    result = run_loadflow_file(temporary, request())
    assert result["convergence"]["converged"]
    buses = {b["bus_id"]: b for b in result["bus_results"]}
    # Independently recover generator injection from terminal flows and local consumption.
    injections = dict.fromkeys(buses, 0.0)
    for branch, flow in zip([*data["lines"], *data["transformers"]], result["branch_results"], strict=True):
        injections[branch.get("from_bus", branch.get("hv_bus"))] += flow["q_from_mvar"]
        injections[branch.get("to_bus", branch.get("lv_bus"))] += flow["q_to_mvar"]
    for load in data["loads"]:
        injections[load["bus_id"]] += load["q_mvar"]
    for shunt in data["shunts"]:
        injections[shunt["bus_id"]] += shunt["q_mvar"] * buses[shunt["bus_id"]]["vm_pu"]**2
    notes = [d for d in result["diagnostics"] if d["code"] == "GENERATOR_Q_LIMIT"]
    assert len(notes) == 2
    assert {d["element_ref"]["element_id"] for d in notes} == {g["generator_id"] for g in data["generators"]}
    for gen in data["generators"]:
        assert injections[gen["bus_id"]] == pytest.approx(gen["q_max_mvar"], abs=1e-8)
        assert buses[gen["bus_id"]]["vm_pu"] < gen["vm_setpoint_pu"]
    assert result["provenance"]["input_hash_sha256"] == hashlib.sha256(temporary.read_bytes()).hexdigest()
    assert path.read_bytes() == original
