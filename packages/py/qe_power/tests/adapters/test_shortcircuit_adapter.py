"""Independent authored networks, no solver output used as expected values.

Source provenance: docs/sources/entries/pandapower-three-phase-reference.yaml.
Equations: shortcircuit/ikss.html (c table and Thevenin circuit),
branch_elements.html (KT), ip.html (radial kappa), ith.html (m, n=1),
voltage_source.html (grid and synchronous impedance). All data are synthetic.
"""
from __future__ import annotations

import copy
import json
import math
from pathlib import Path

import pytest
from qe_core import validate
from qe_core.provenance import hash_inputs
from qe_power.adapters.pandapower import (
    ShortcircuitInputError,
    run_shortcircuit_file,
    solve_shortcircuit,
)
from qe_power.adapters.pandapower import shortcircuit as adapter

REPO = Path(__file__).resolve().parents[5]
EXAMPLE = REPO / "examples" / "shortcircuit"


@pytest.fixture
def inputs():
    return (json.loads((EXAMPLE / "transformer" / "network.json").read_text()),
            json.loads((EXAMPLE / "shortcircuit-request.json").read_text()))


def solved(network, request):
    outcome = solve_shortcircuit(network, request)
    assert outcome.value is not None, outcome.diagnostics
    assert validate(outcome.value, "power/shortcircuit-result") == []
    return outcome.value


def duties(z, voltage, c, duration, frequency=50):
    ik = c * voltage / (math.sqrt(3) * abs(z))
    kappa = 1.02 + 0.98 * math.exp(-3 * z.real / z.imag)
    a = math.log(kappa - 1)
    m = math.expm1(4 * frequency * duration * a) / (2 * frequency * duration * a)
    return (ik, math.sqrt(2) * kappa * ik, ik * math.sqrt(1 + m))


def transformer_reference(network, request, case, infinite=False):
    # Original 20/0.4-kV, 1-MVA transformer; r=.01, x=.05 on its own rating.
    # IK table: cHV max=1.10/min=1, cLV at 6% max=1.05/min=.95.
    # KT uses cmax on LV for maximum faults. Minimum transformer duties
    # are unavailable because the public page omits the engine case distinction.
    trafo, grid = network["transformers"][0], network["external_grids"][0]
    c_hv, c_lv = (1.1, 1.05) if case == "max" else (1, 0.95)
    kt = 0.95 * 1.05 / (1 + 0.6 * trafo["x_pu"])
    zt = kt * complex(trafo["r_pu"], trafo["x_pu"]) * trafo["vn_lv_kv"]**2 / trafo["sn_mva"]
    rx = grid[f"rx_{case}"]
    # External-grid impedance, referred to LV through the squared nominal ratio.
    magnitude = c_hv * trafo["vn_lv_kv"]**2 / grid[f"s_sc_{case}_mva"]
    zq = magnitude * complex(rx, 1) / math.sqrt(1 + rx**2)
    return duties(zt if infinite else zt + zq, trafo["vn_lv_kv"], c_lv, request["fault_duration_s"])


@pytest.mark.parametrize("case", ["max"])
def test_transformer_matches_independent_finite_and_infinite_reference(inputs, case):
    network, request = inputs
    request["cases"] = [case]
    result = solved(network, request)
    assert result["status"] == "success"
    row = result["case_results"][0]["bus_results"][1]
    assert [row[k] for k in adapter.CURRENTS] == pytest.approx(
        transformer_reference(network, request, case), rel=1e-10, abs=1e-10)
    # Increasing finite source strength must approach the infinite-source
    # hand derivation. This is convergence, not a loosened solver tolerance.
    target = transformer_reference(network, request, case, infinite=True)
    errors = []
    for strength in (1e4, 1e6, 1e8, 1e12):
        n = copy.deepcopy(network)
        n["external_grids"][0]["s_sc_max_mva"] = strength
        n["external_grids"][0]["s_sc_min_mva"] = strength
        row = solved(n, request)["case_results"][0]["bus_results"][1]
        actual = [row[k] for k in adapter.CURRENTS]
        assert actual == pytest.approx(transformer_reference(n, request, case), rel=1e-9)
        errors.append(abs(actual[0] - target[0]))
    assert all(a > b for a, b in zip(errors, errors[1:]))
    assert actual == pytest.approx(target, rel=1e-9)


def line_network(network, temperature=20):
    n = copy.deepcopy(network)
    n["buses"][1]["vn_kv"] = 20
    n["transformers"] = []
    n["lines"] = [{"line_id": "feeder", "from_bus": "hv", "to_bus": "lv",
                   "length_km": 2, "r_ohm_per_km": 0.2, "x_ohm_per_km": 0.4,
                   "end_temperature_celsius": temperature}]
    return n


@pytest.mark.parametrize("case", ["max", "min"])
def test_line_at_explicit_20c_has_hand_derived_duties(inputs, case):
    network, request = inputs
    network = line_network(network)
    request["cases"] = [case]
    c = 1.1 if case == "max" else 1
    grid = network["external_grids"][0]
    magnitude = c * 20**2 / grid[f"s_sc_{case}_mva"]
    zgrid = magnitude * complex(0.1, 1) / math.sqrt(1.01)
    zline = 2 * complex(0.2, 0.4)  # K_L=1 at explicit 20 C for both formulas.
    row = solved(network, request)["case_results"][0]["bus_results"][1]
    assert [row[k] for k in adapter.CURRENTS] == pytest.approx(
        duties(zgrid + zline, 20, c, request["fault_duration_s"]), rel=1e-10)


def minimum_transformer_reference(network, request):
    # Minimum case, 20/0.4 kV: c_HV = 1.0, c_LV = 0.95 (D10, Kasikci Table 1.1 p. 8), K_T = 1
    # (Kasikci ch. 9 p. 75). Z_Q on LV = 1.0 * 0.4^2 / 500 = 0.00032 ohm at R/X 0.1;
    # Z_T = (0.01 + j0.05) * 0.4^2 / 1 = 0.0016 + j0.008 ohm; |Z_k| = 0.00847696 ohm, so
    # Ik'' = 0.95 * 0.4 / (sqrt(3) * 0.00847696) = 25.8811 kA.
    zq = 0.4**2 / network["external_grids"][0]["s_sc_min_mva"] * complex(0.1, 1) / math.sqrt(1.01)
    zt = complex(0.01, 0.05) * 0.4**2 / 1
    return duties(zq + zt, 0.4, 0.95, request["fault_duration_s"])


@pytest.mark.parametrize("tolerance", [6, 10])
def test_lv_minimum_uses_c_min_095_for_both_tolerance_classes(inputs, tolerance):
    network, request = inputs
    request["lv_tolerance_percent"] = tolerance
    request["cases"] = ["max", "min"]
    result = solved(network, request)
    assert [c["status"] for c in result["case_results"]] == ["success", "success"]
    row = result["case_results"][1]["bus_results"][1]
    assert row["voltage_factor"] == 0.95
    assert [row[k] for k in adapter.CURRENTS] == pytest.approx(minimum_transformer_reference(network, request), rel=1e-10)
    assert row["ikss_ka"] == pytest.approx(25.8811, rel=1e-5)
    # Maximum c follows the tolerance class: 1.05 (+6%) or 1.10 (+10%).
    assert result["case_results"][0]["bus_results"][1]["voltage_factor"] == (1.05 if tolerance == 6 else 1.1)


def test_60hz_thermal_current_uses_the_requested_frequency(inputs):
    # Kasikci eq. 13.2 p. 117 with f = 60 Hz; pandapower's own Ith is fixed at 50 Hz and is not used.
    network, request = inputs
    request["frequency_hz"] = 60
    request["cases"] = ["max"]
    result = solved(network, request)
    assert result["status"] == "success"
    row = result["case_results"][0]["bus_results"][1]
    ik, ip, ith = duties(complex(row["trace"]["zk_r_ohm"], row["trace"]["zk_x_ohm"]), 0.4, 1.05,
                         request["fault_duration_s"], frequency=60)
    assert (row["ikss_ka"], row["ip_ka"], row["ith_ka"]) == pytest.approx((ik, ip, ith), rel=1e-10)
    assert row["ith_ka"] != pytest.approx(duties(complex(row["trace"]["zk_r_ohm"], row["trace"]["zk_x_ohm"]),
                                                 0.4, 1.05, request["fault_duration_s"])[2], rel=1e-6)


def test_line_at_80c_raises_minimum_resistance_by_factor_124(inputs):
    # Kasikci p. 12: R = R_20 (1 + 0.004 (80 - 20)) = 1.24 R_20.
    network, request = inputs
    network = line_network(network, temperature=80)
    request["cases"] = ["min"]
    zgrid = 1.0 * 20**2 / network["external_grids"][0]["s_sc_min_mva"] * complex(0.1, 1) / math.sqrt(1.01)
    zline = complex(0.4 * 1.24, 0.8)
    row = solved(network, request)["case_results"][0]["bus_results"][1]
    assert [row[k] for k in adapter.CURRENTS] == pytest.approx(duties(zgrid + zline, 20, 1.0, 1), rel=1e-10)
    assert row["trace"]["elements"][1]["inputs"]["temperature_factor"] == pytest.approx(1.24, rel=1e-12)


@pytest.mark.parametrize("temperature", [None])
def test_missing_line_temperature_blocks_min_only(inputs, temperature):
    # The network contract already rejects end temperatures below 20 C.
    network, request = inputs
    network = line_network(network)
    if temperature is None:
        del network["lines"][0]["end_temperature_celsius"]
    else:
        network["lines"][0]["end_temperature_celsius"] = temperature
    result = solved(network, request)
    assert [c["status"] for c in result["case_results"]] == ["success", "failed"]
    code = "MISSING_FAULT_DATA" if temperature is None else "TEMPERATURE_CORRECTION_UNAVAILABLE"
    assert any(d["code"] == code for d in result["case_results"][1]["diagnostics"])


def test_missing_grid_data_is_case_specific(inputs):
    network, request = inputs
    network = line_network(network)
    del network["external_grids"][0]["rx_min"]
    result = solved(network, request)
    assert [c["status"] for c in result["case_results"]] == ["success", "failed"]
    missing = [d for d in result["case_results"][1]["diagnostics"] if d["code"] == "MISSING_FAULT_DATA"]
    assert missing[0]["element_ref"] == {"element_type": "external_grids", "element_id": "grid", "field": "rx_min"}


def test_disconnected_bus_keeps_coverage_and_healthy_results(inputs):
    network, request = inputs
    network = line_network(network)
    network["buses"].append({"bus_id": "island", "vn_kv": 20, "bus_type": "pq"})
    result = solved(network, request)
    for case in result["case_results"]:
        assert case["status"] == "partial"
        assert [b["bus_id"] for b in case["bus_results"]] == ["hv", "lv", "island"]
        assert case["bus_results"][0]["ikss_ka"] > 0
        assert case["bus_results"][2]["ikss_ka"] is None
        assert any(d["code"] == "DISCONNECTED_BUS" for d in case["diagnostics"])


def test_bad_equipment_in_one_component_does_not_block_another(inputs):
    network, request = inputs
    network = line_network(network)
    network["buses"].append({"bus_id": "other", "vn_kv": 20, "bus_type": "slack"})
    network["external_grids"].append({"external_grid_id": "bad-grid", "bus_id": "other",
                                      "vm_setpoint_pu": 1, "va_setpoint_degree": 0})
    result = solved(network, request)
    assert result["status"] == "partial"
    assert all(c["bus_results"][0]["ikss_ka"] > 0 and c["bus_results"][2]["ikss_ka"] is None
               for c in result["case_results"])


@pytest.mark.parametrize("base_mva", [1, 10, 100])
def test_synchronous_ikss_matches_hand_derived_machine_and_withholds_near_duties(inputs, base_mva):
    network, request = inputs
    network["base_mva"] = base_mva
    network["buses"] = [network["buses"][0]]
    network["buses"][0]["bus_type"] = "pv"
    network["external_grids"] = []
    network["transformers"] = []
    network["generators"] = [{"generator_id": "g1", "bus_id": "hv", "p_mw": 1,
        "vm_setpoint_pu": 1, "sn_mva": 10, "vn_kv": 20, "xdss_pu": 0.2,
        "rdss_ohm": 0.4, "cos_phi": 0.8, "voltage_control_range_percent": 0}]
    z = complex(0.4, 0.2 * 20**2 / 10) * (1.1 / (1 + 0.2 * 0.6))
    result = solved(network, request)
    assert result["status"] == "partial"
    for case in result["case_results"]:
        row = case["bus_results"][0]
        c = 1.1 if case["case"] == "max" else 1
        assert row["ikss_ka"] == pytest.approx(c * 20 / (math.sqrt(3) * abs(z)), rel=1e-10)
        assert row["ip_ka"] is None and row["ith_ka"] is None
        assert any(d["code"] == "NEAR_GENERATOR_DUTY" for d in case["diagnostics"])


def test_mesh_peak_and_thermal_by_method_c_match_hand_derivation(inputs):
    # Two unlike parallel lines: a = (0.2 + j0.4) * 2 km, b = (0.5 + j0.3) * 1 km.
    # Method C (Kasikci p. 99): scale reactances by fc/f = 20/50 = 0.4, reduce, then
    # R/X = (R_c / X_c) * 0.4 and kappa = 1.02 + 0.98 exp(-3 R/X).
    network, request = inputs
    network = line_network(network)
    second = {**copy.deepcopy(network["lines"][0]), "line_id": "parallel",
              "length_km": 1, "r_ohm_per_km": 0.5, "x_ohm_per_km": 0.3}
    network["lines"].append(second)
    result = solved(network, request)

    def parallel(a, b):
        return a * b / (a + b)
    for case in result["case_results"]:
        grid = network["external_grids"][0]
        c = 1.1 if case["case"] == "max" else 1
        zq = c * 20**2 / grid[f"s_sc_{case['case']}_mva"] * complex(.1, 1) / math.sqrt(1.01)
        za, zb = complex(.4, .8), complex(.5, .3)
        z = zq + parallel(za, zb)

        def at_fc(w):
            return complex(w.real, 0.4 * w.imag)
        zc = at_fc(zq) + parallel(at_fc(za), at_fc(zb))
        rx = zc.real / zc.imag * 0.4
        kappa = 1.02 + 0.98 * math.exp(-3 * rx)
        ik = c * 20 / (math.sqrt(3) * abs(z))
        a = math.log(kappa - 1)
        m = math.expm1(4 * 50 * 1 * a) / (2 * 50 * 1 * a)
        row = case["bus_results"][1]
        assert row["ikss_ka"] == pytest.approx(ik, rel=1e-10)
        assert row["ip_ka"] == pytest.approx(kappa * math.sqrt(2) * ik, rel=1e-10)
        assert row["ith_ka"] == pytest.approx(ik * math.sqrt(1 + m), rel=1e-10)
        assert row["trace"]["kappa_method"] == "method-C"
        # Method C differs from applying the fault-impedance R/X directly.
        assert abs(kappa - (1.02 + 0.98 * math.exp(-3 * z.real / z.imag))) > 1e-3


def test_mesh_with_transformer_keeps_duties_unavailable(inputs):
    network, request = inputs
    second = {**copy.deepcopy(network["transformers"][0]), "transformer_id": "t2"}
    network["transformers"].append(second)
    request["cases"] = ["max"]
    row = solved(network, request)["case_results"][0]["bus_results"][1]
    assert row["ikss_ka"] > 0 and row["ip_ka"] is None and row["ith_ka"] is None


def test_high_kappa_thermal_uses_book_equation_not_engine_shortcut(inputs):
    # R/X = 0.001: kappa = 1.02 + 0.98 exp(-0.003) = 1.02 + 0.98 * 0.9970045 = 1.997064 > 1.99, where
    # pandapower sets m = 0. Kasikci eq. 13.2: ln(0.997064) = -0.0029399;
    # m = expm1(200 * -0.0029399) / (100 * -0.0029399) = -0.444550 / -0.293990 = 1.5121.
    network, request = inputs
    network["transformers"] = []
    network["buses"] = network["buses"][:1]
    for field in ("rx_max", "rx_min"):
        network["external_grids"][0][field] = 0.001
    result = solved(network, request)
    assert result["status"] == "success"
    for case in result["case_results"]:
        row = case["bus_results"][0]
        assert row["trace"]["kappa"] == pytest.approx(1.997064, rel=1e-6)
        assert row["trace"]["m"] == pytest.approx(1.5121, rel=1e-4)
        assert row["ith_ka"] == pytest.approx(row["ikss_ka"] * math.sqrt(1 + row["trace"]["m"]), rel=1e-12)


@pytest.mark.parametrize("field,value", [("power_station_unit", True), ("oltc", True), ("x_pu", 0)])
def test_unsupported_transformer_is_diagnosed(inputs, field, value):
    network, request = inputs
    network["transformers"][0][field] = value
    result = solved(network, request)
    assert result["status"] == "failed"
    assert any(d["element_ref"]["element_id"] == "t1" and d["element_ref"]["field"] == field
               for d in result["case_results"][0]["diagnostics"])


def test_operating_loads_shunts_and_taps_are_explained_and_not_fault_inputs(inputs):
    network, request = inputs
    original = solved(network, request)
    network["loads"] = [{"load_id": "l1", "bus_id": "lv", "p_mw": 0.5, "q_mvar": 0.1}]
    network["shunts"] = [{"shunt_id": "s1", "bus_id": "lv", "p_mw": 0, "q_mvar": -0.1}]
    network["transformers"][0]["tap_ratio"] = 1.1
    changed = solved(network, request)
    assert changed["case_results"] == original["case_results"]
    assert len(changed["diagnostics"]) == 3


def test_invalid_documents_have_no_result_and_file_wrapper_has_diagnostics(inputs, tmp_path):
    network, request = inputs
    request["fault_duration_s"] = 0
    outcome = solve_shortcircuit(network, request)
    assert outcome.value is None
    assert outcome.diagnostics
    path = tmp_path / "network.json"
    path.write_text(json.dumps(network))
    with pytest.raises(ShortcircuitInputError) as caught:
        run_shortcircuit_file(path, request)
    assert caught.value.diagnostics
    with pytest.raises(ShortcircuitInputError):
        run_shortcircuit_file(tmp_path / "missing.json", request)


@pytest.mark.parametrize("exception", [ValueError, UserWarning])
def test_solver_exception_returns_valid_failed_result(inputs, monkeypatch, exception):
    network, request = inputs
    network = line_network(network)

    def fail(*args, **kwargs):
        raise exception("synthetic singular network")

    monkeypatch.setattr(adapter, "calc_sc", fail)
    result = solved(network, request)
    assert result["status"] == "failed"
    assert all(d["code"] == "SOLVER_FAILURE" for c in result["case_results"] for d in c["diagnostics"])


def test_provenance_covers_network_request_and_reordered_keys(inputs):
    network, request = inputs
    original = copy.deepcopy((network, request))
    first = solved(network, request)["provenance"]
    assert first["solver_name"] == "pandapower" and first["solver_version"] == "3.5.6"
    assert first["input_hash_sha256"] == hash_inputs({"network": network, "request": request})
    reordered = dict(reversed(list(network.items())))
    assert solved(reordered, request)["provenance"]["input_hash_sha256"] == first["input_hash_sha256"]
    request["fault_duration_s"] = 0.1
    assert solved(network, request)["provenance"]["input_hash_sha256"] != first["input_hash_sha256"]
    assert network == original[0]


def test_minimum_transformer_case_uses_kt_one(inputs):
    network, request = inputs
    request["cases"] = ["min"]
    result = solved(network, request)
    assert result["status"] == "success"
    row = result["case_results"][0]["bus_results"][1]
    assert row["trace"]["elements"][1]["inputs"]["k_t"] == 1.0
    assert [row[k] for k in adapter.CURRENTS] == pytest.approx(minimum_transformer_reference(network, request), rel=1e-10)


def test_missing_machine_data_is_not_defaulted(inputs):
    network, request = inputs
    network = line_network(network)
    network["generators"] = [{"generator_id": "incomplete", "bus_id": "lv", "p_mw": 1, "vm_setpoint_pu": 1}]
    result = solved(network, request)
    assert result["status"] == "failed"
    missing = {d["element_ref"]["field"] for d in result["case_results"][0]["diagnostics"]
               if d["code"] == "MISSING_FAULT_DATA"}
    assert missing == {"sn_mva", "vn_kv", "xdss_pu", "rdss_ohm", "cos_phi", "voltage_control_range_percent"}


def test_exact_1kv_boundary_is_not_inferred(inputs):
    # Both owned books put 1000 V in LV, but the engine applies MV factors at vn_kv = 1.
    network, request = inputs
    network = line_network(network)
    for bus in network["buses"]:
        bus["vn_kv"] = 1
    result = solved(network, request)
    assert result["status"] == "failed"
    assert all(b["voltage_factor"] is None for c in result["case_results"] for b in c["bus_results"])


def test_near_generator_duties_are_withheld_for_remote_buses_too(inputs):
    network, request = inputs
    network = line_network(network)
    network["generators"] = [{"generator_id": "g1", "bus_id": "lv", "p_mw": 1,
        "vm_setpoint_pu": 1, "sn_mva": 10, "vn_kv": 20, "xdss_pu": 0.2,
        "rdss_ohm": 0.4, "cos_phi": 0.8, "voltage_control_range_percent": 0}]
    result = solved(network, request)
    for case in result["case_results"]:
        assert all(b["ikss_ka"] > 0 and b["ip_ka"] is None and b["ith_ka"] is None
                   for b in case["bus_results"])


def test_zero_resistance_source_takes_the_m_equals_2_limit(inputs):
    # R = 0: kappa = 2 exactly, ln(kappa - 1) = 0 and m -> 2 (Kasikci Fig. 13.3a p. 118), so
    # ip = 2 sqrt(2) Ik'' and Ith = Ik'' sqrt(3); no non-finite value can leak.
    network, request = inputs
    network["buses"] = network["buses"][:1]
    network["transformers"] = []
    network["external_grids"][0].update(rx_max=0, rx_min=0)
    result = solved(network, request)
    assert result["status"] == "success"
    for case in result["case_results"]:
        row = case["bus_results"][0]
        assert row["ip_ka"] == pytest.approx(2 * math.sqrt(2) * row["ikss_ka"], rel=1e-12)
        assert row["ith_ka"] == pytest.approx(math.sqrt(3) * row["ikss_ka"], rel=1e-12)
        assert row["trace"]["m"] == 2.0


def test_extremely_short_duration_is_not_certified_after_engine_cancellation(inputs):
    network, request = inputs
    network = line_network(network)
    request["fault_duration_s"] = 1e-20
    result = solved(network, request)
    assert result["status"] == "partial"
    assert all(b["ith_ka"] is None for c in result["case_results"] for b in c["bus_results"])
    assert any(d["code"] == "THERMAL_EQUATION_MISMATCH" for d in result["case_results"][0]["diagnostics"])
