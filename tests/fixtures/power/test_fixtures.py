from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import pytest
from qe_core import validate
from verify import verify_loadflow_result

FIXTURE_ROOT = Path(__file__).parent
NETWORK_PATHS = sorted(FIXTURE_ROOT.glob("*/network.json"))


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_all_original_networks_validate_against_contract() -> None:
    assert len(NETWORK_PATHS) == 5
    for network_path in NETWORK_PATHS:
        diagnostics = validate(_read_json(network_path), "power/network")
        assert diagnostics == [], f"{network_path}: {diagnostics}"


def test_fourteen_bus_example_manifest_validates() -> None:
    manifest_path = FIXTURE_ROOT.parents[2] / "examples" / "fourteen_bus" / "manifest.json"
    diagnostics = validate(_read_json(manifest_path), "project/manifest")
    assert diagnostics == []


def test_two_bus_reference_validates_and_matches_closed_form() -> None:
    fixture_path = FIXTURE_ROOT / "two_bus_analytic"
    network = _read_json(fixture_path / "network.json")
    result = _read_json(fixture_path / "reference.json")
    assert validate(result, "power/loadflow-result") == []
    input_hash = hashlib.sha256((fixture_path / "network.json").read_bytes()).hexdigest()
    assert result["provenance"]["input_hash_sha256"] == input_hash

    line = network["lines"][0]
    base_mva = network["base_mva"]
    voltage_base_kv = network["buses"][0]["vn_kv"]
    impedance_base_ohm = voltage_base_kv**2 / base_mva
    impedance_pu = complex(
        line["r_ohm_per_km"] * line["length_km"],
        line["x_ohm_per_km"] * line["length_km"],
    ) / impedance_base_ohm
    load = network["loads"][0]
    p_pu = load["p_mw"] / base_mva
    q_pu = load["q_mvar"] / base_mva
    coefficient_a = impedance_pu.real * p_pu + impedance_pu.imag * q_pu
    coefficient_b = impedance_pu.imag * p_pu - impedance_pu.real * q_pu
    discriminant = (1.0 - 2.0 * coefficient_a) ** 2 - 4.0 * (
        coefficient_a**2 + coefficient_b**2
    )
    voltage_squared_pu = (
        1.0 - 2.0 * coefficient_a + math.sqrt(discriminant)
    ) / 2.0
    receiving_real_pu = voltage_squared_pu + coefficient_a
    receiving_imag_pu = -coefficient_b
    expected_vm_pu = math.hypot(receiving_real_pu, receiving_imag_pu)
    expected_va_degree = math.degrees(math.atan2(receiving_imag_pu, receiving_real_pu))
    receiving_result = next(
        item for item in result["bus_results"] if item["bus_id"] == "receiving"
    )
    assert math.isclose(receiving_result["vm_pu"], expected_vm_pu, abs_tol=1e-14)
    assert math.isclose(receiving_result["va_degree"], expected_va_degree, abs_tol=1e-14)

    verification = verify_loadflow_result(network, result)
    assert verification.max_bus_mismatch_pu < 1e-8
    assert abs(verification.energy_balance_error_mw) < 1e-7


def test_verifier_rejects_bus_mismatch() -> None:
    fixture_path = FIXTURE_ROOT / "two_bus_analytic"
    network = _read_json(fixture_path / "network.json")
    result = _read_json(fixture_path / "reference.json")
    next(item for item in result["bus_results"] if item["bus_id"] == "receiving")[
        "vm_pu"
    ] += 1e-4
    with pytest.raises(AssertionError, match="mismatch"):
        verify_loadflow_result(network, result)


def test_verifier_rejects_energy_imbalance() -> None:
    fixture_path = FIXTURE_ROOT / "two_bus_analytic"
    network = _read_json(fixture_path / "network.json")
    result = _read_json(fixture_path / "reference.json")
    result["branch_results"][0]["p_loss_mw"] += 0.1
    with pytest.raises(AssertionError, match="loss"):
        verify_loadflow_result(network, result)
