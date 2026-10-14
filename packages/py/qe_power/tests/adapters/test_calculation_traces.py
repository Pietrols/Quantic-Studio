"""CC-7 calculation traces checked against hand arithmetic (WP-1.11, decision D11).

Every expected number below is worked out by hand from the example inputs, with
the arithmetic in the comment beside it, not taken from the solver. Equations:
Kasikci, Short Circuits in Power Systems, 1st ed 2002: eq. 8.1 p. 48 (grid),
eq. 8.2 p. 48 (referral by rated ratio), eq. 9.14 p. 79 (K_T), eq. 9.3 p. 76 (K_G),
section 11.2 p. 92 (Ik''), eqs. 11.22 and 11.23 p. 98 (kappa, ip), eqs. 13.1 and
13.2 p. 117 (m, n). Motor start: Fitzgerald, Electric Machinery, 6th ed 2003,
section 6.6.2 pp. 333 to 334.
"""
from __future__ import annotations

import copy
import json
import math
from pathlib import Path

import pytest
from qe_core import validate
from qe_power.adapters.pandapower import shortcircuit as adapter
from qe_power.adapters.pandapower import solve_shortcircuit
from qe_power.adapters.pandapower.motorstart import solve_motorstart

REPO = Path(__file__).resolve().parents[5]
FEEDER = REPO / "examples" / "shortcircuit"
MOTOR = REPO / "examples" / "motorstart"


def load(folder, request="shortcircuit-request.json"):
    return (json.loads((folder / "network.json").read_text()),
            json.loads((folder / request).read_text()))


def rows(result, case):
    return {r["bus_id"]: r for c in result["case_results"] if c["case"] == case for r in c["bus_results"]}


def solved(network, request):
    outcome = solve_shortcircuit(network, request)
    assert outcome.value is not None, outcome.diagnostics
    assert validate(outcome.value, "power/shortcircuit-result") == []
    assert outcome.value["schema_version"] == "0.3.0"
    return outcome.value


def test_feeder_maximum_trace_matches_hand_calculation():
    result = solved(*load(FEEDER))
    lv = rows(result, "max")["lv"]["trace"]
    grid, line = lv["elements"]
    # Z_Q = 1.1 * 20^2 / 1000 = 0.44 ohm; R/X = 0.1, so R = 0.44 * 0.1 / sqrt(1.01) = 0.0437816,
    # X = 0.44 / sqrt(1.01) = 0.437816.
    assert grid["inputs"] == {"c": 1.1, "un_kv": 20, "s_sc_mva": 1000, "rx": 0.1}
    assert (grid["r_ohm"], grid["x_ohm"]) == pytest.approx((0.0437816, 0.437816), rel=1e-6)
    # Z_L = (0.2 + j0.4) ohm/km * 2 km = 0.4 + j0.8 ohm.
    assert (line["r_ohm"], line["x_ohm"]) == pytest.approx((0.4, 0.8), rel=1e-12)
    # Z_k = 0.443782 + j1.237816, |Z_k| = 1.314964 ohm.
    assert (lv["zk_r_ohm"], lv["zk_x_ohm"], lv["zk_ohm"]) == pytest.approx((0.443782, 1.237816, 1.314964), rel=1e-6)
    assert lv["impedance_basis"] == "radial-sum"
    row = rows(result, "max")["lv"]
    # Ik'' = 1.1 * 20 / (sqrt(3) * 1.314964) = 9.65935 kA.
    assert row["ikss_ka"] == pytest.approx(9.65935, rel=1e-6)
    # R/X = 0.358520; kappa = 1.02 + 0.98 exp(-1.07556) = 1.35428; ip = 1.35428 sqrt(2) 9.65935 = 18.5001 kA.
    assert lv["kappa"] == pytest.approx(1.35428, rel=1e-5)
    assert row["ip_ka"] == pytest.approx(18.5001, rel=1e-5)
    # ln(0.35428) = -1.03765; exp(-207.5) is negligible, so m = 1 / 103.765 = 0.0096372;
    # Ith = 9.65935 sqrt(1.0096372) = 9.70579 kA.
    assert lv["m"] == pytest.approx(0.0096372, rel=1e-4)
    assert lv["n"] == 1
    assert row["ith_ka"] == pytest.approx(9.70579, rel=1e-6)


def test_feeder_minimum_trace_uses_minimum_grid_and_c():
    result = solved(*load(FEEDER))
    lv = rows(result, "min")["lv"]
    # Z_Q = 1.0 * 20^2 / 500 = 0.8 ohm -> 0.0796030 + j0.796030; plus the line 0.4 + j0.8.
    assert lv["trace"]["elements"][0]["inputs"]["c"] == 1.0
    assert (lv["trace"]["zk_r_ohm"], lv["trace"]["zk_x_ohm"]) == pytest.approx((0.479603, 1.596030), rel=1e-6)
    # |Z_k| = 1.666533; Ik'' = 20 / (sqrt(3) * 1.666533) = 6.92876 kA.
    assert lv["ikss_ka"] == pytest.approx(6.92876, rel=1e-5)


def test_transformer_trace_refers_grid_by_rated_ratio_and_applies_kt():
    network, request = load(FEEDER / "transformer")
    lv = rows(solved(network, request), "max")["lv"]["trace"]
    grid, trafo = lv["elements"]
    # Grid referred to 0.4 kV: factor (0.4/20)^2 = 0.0004; 0.0437816 * 0.0004 = 1.75126e-5 ohm.
    assert grid["referral_factor"] == pytest.approx(0.0004, rel=1e-12)
    assert grid["r_referred_ohm"] == pytest.approx(1.75126e-5, rel=1e-5)
    # K_T = 0.95 * 1.05 / (1 + 0.6 * 0.05) = 0.9975 / 1.03 = 0.968447.
    assert trafo["inputs"]["k_t"] == pytest.approx(0.968447, rel=1e-6)
    # Z_T = 0.968447 * (0.01 + j0.05) * 0.4^2 / 1 = 0.00154951 + j0.00774757 ohm.
    assert (trafo["r_ohm"], trafo["x_ohm"]) == pytest.approx((0.00154951, 0.00774757), rel=1e-5)
    # Z_k = 0.00156703 + j0.00792270; Ik'' = 1.05 * 0.4 / (sqrt(3) * 0.00807619) = 30.0250 kA.
    assert (lv["zk_r_ohm"], lv["zk_x_ohm"]) == pytest.approx((0.00156703, 0.00792270), rel=1e-5)
    assert lv["voltage_factor"] == 1.05


def test_off_nominal_transformer_rating_is_referred_by_rated_ratio():
    network, request = load(FEEDER / "transformer")
    network["transformers"][0]["vn_lv_kv"] = 0.42
    lv = rows(solved(network, request), "max")["lv"]["trace"]
    # Grid factor (0.42/20)^2 = 0.000441; Z_T on 0.42 kV: 0.968447 * (0.01 + j0.05) * 0.1764 = 0.00170834 + j0.00854170.
    assert lv["elements"][0]["referral_factor"] == pytest.approx(0.000441, rel=1e-12)
    assert lv["zk_r_ohm"] == pytest.approx(0.0017276, rel=1e-4)
    assert lv["zk_x_ohm"] == pytest.approx(0.0087348, rel=1e-4)


def test_generator_trace_shows_kg():
    network, _ = load(FEEDER / "transformer")
    _, request = load(FEEDER)  # both cases
    network["buses"] = [dict(network["buses"][0], bus_type="pv")]
    network["external_grids"], network["transformers"] = [], []
    network["generators"] = [{"generator_id": "g1", "bus_id": "hv", "p_mw": 1, "vm_setpoint_pu": 1,
                              "sn_mva": 10, "vn_kv": 20, "xdss_pu": 0.2, "rdss_ohm": 0.4, "cos_phi": 0.8,
                              "voltage_control_range_percent": 0}]
    result = solved(network, request)
    for case in ("max", "min"):
        trace = rows(result, case)["hv"]["trace"]
        gen = trace["elements"][0]
        # K_G = (20/20) * 1.1 / (1 + 0.2 * 0.6) = 0.982143 (pandapower uses c_max in both cases);
        # Z_GK = 0.982143 * (0.4 + j0.2 * 20^2 / 10) = 0.392857 + j7.85714 ohm.
        assert gen["inputs"]["k_g"] == pytest.approx(0.982143, rel=1e-6)
        assert (gen["r_ohm"], gen["x_ohm"]) == pytest.approx((0.392857, 7.85714), rel=1e-6)
        assert trace["kappa"] is None and trace["m"] is None


def test_mesh_trace_uses_engine_thevenin_and_still_checks_ikss():
    network, request = load(FEEDER)
    second = copy.deepcopy(network["lines"][0])
    second["line_id"] = "parallel"
    network["lines"].append(second)
    trace = rows(solved(network, request), "max")["lv"]["trace"]
    # Parallel lines halve the line impedance: Z_k = 0.0437816 + 0.2 + j(0.437816 + 0.4).
    assert trace["impedance_basis"] == "engine-thevenin" and trace["elements"] == []
    assert (trace["zk_r_ohm"], trace["zk_x_ohm"]) == pytest.approx((0.2437816, 0.837816), rel=1e-6)


def test_disagreeing_hand_sum_makes_values_unavailable(monkeypatch):
    original = adapter._branch_entry

    def wrong(*args):
        entry = original(*args)
        return {**entry, "x_ohm": entry["x_ohm"] * 1.001}
    monkeypatch.setattr(adapter, "_branch_entry", wrong)
    lv = rows(solved(*load(FEEDER)), "max")["lv"]
    assert lv["ikss_ka"] is None and lv["trace"] is None


def test_motor_trace_matches_hand_calculation():
    network, request = load(MOTOR, "motorstart-request.json")
    outcome = solve_motorstart(network, request)
    assert validate(outcome.value, "power/motorstart-result") == []
    assert outcome.value["schema_version"] == "0.4.0"
    t = outcome.value["motor_trace"]
    # I_r = 30 / (sqrt(3) * 0.4 * 0.9 * 0.85) = 30 / 530.03 = 0.0566030 kA; I_LR = 6 * I_r = 0.339618 kA.
    assert t["rated_current_ka"] == pytest.approx(0.0566030, rel=1e-5)
    assert t["locked_rotor_current_ka"] == pytest.approx(0.339618, rel=1e-5)
    # |Z| = 0.4 / (sqrt(3) * 0.339618) = 0.68 ohm; acos(0.3) = 72.5424 deg; R = 0.204, X = 0.68 * 0.953939 = 0.648679.
    assert (t["z_lr_ohm"], t["locked_rotor_angle_deg"]) == pytest.approx((0.68, 72.5424), rel=1e-5)
    assert (t["r_lr_ohm"], t["x_lr_ohm"]) == pytest.approx((0.204, 0.648679), rel=1e-5)
    # S = 0.16 / (0.204 - j0.648679) = 0.16 (0.204 + j0.648679) / 0.4624 = 0.0705882 + j0.224456 MVA.
    assert (t["shunt_p_mw"], t["shunt_q_mvar"]) == pytest.approx((0.0705882, 0.224456), rel=1e-5)
    assert math.isclose(t["bus_kv"], 0.4)
