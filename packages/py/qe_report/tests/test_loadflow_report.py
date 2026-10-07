from __future__ import annotations

import json
from pathlib import Path

import pytest
from qe_report import VoltageLimits, render_loadflow_report, summarise

REPO = Path(__file__).resolve().parents[4]
TWO_BUS = REPO / "tests" / "fixtures" / "power" / "two_bus_analytic"
REQUEST = {"schema_version": "0.1.0", "request_id": "r1", "network_file": "network.json",
           "tolerance_mva": 0.0001, "max_iterations": 20, "initialization": "flat"}


def two_bus():
    network = json.loads((TWO_BUS / "network.json").read_text(encoding="utf-8"))
    result = json.loads((TWO_BUS / "reference.json").read_text(encoding="utf-8"))
    return network, result


def test_voltage_limits_flag_and_reject_bad_band():
    limits = VoltageLimits(0.95, 1.05)
    assert limits.flag(0.94) == "LOW"
    assert limits.flag(1.0) == "ok"
    assert limits.flag(1.06) == "HIGH"
    with pytest.raises(ValueError):
        VoltageLimits(1.05, 0.95)


def test_summary_uses_reference_values():
    network, result = two_bus()
    facts = summarise(network, result, VoltageLimits())
    assert facts["loss_p_mw"] == pytest.approx(0.015372484322862423)
    assert facts["load_p_mw"] == pytest.approx(2.0)
    assert facts["violations"] == []


def test_grid_supply_equals_load_plus_losses():
    # Power balance at the source bus: the grid supplies the load and the series loss.
    network, result = two_bus()
    grid = summarise(network, result, VoltageLimits())["sources"][0]
    assert grid["kind"] == "grid"
    assert grid["p_mw"] == pytest.approx(2.0 + 0.015372484322862423, abs=1e-12)
    assert grid["q_mvar"] == pytest.approx(1.0 + 0.030744968645724846, abs=1e-12)


def test_tight_band_flags_receiving_bus_low():
    network, result = two_bus()
    report = render_loadflow_report(project_name="t", network=network, request=REQUEST,
                                    result=result, limits=VoltageLimits(0.99, 1.01))
    assert "| receiving |" in report and "LOW" in report
    assert "| Buses outside limits | 1 |" in report


def test_report_has_every_required_section():
    network, result = two_bus()
    report = render_loadflow_report(project_name="Two bus", network=network, request=REQUEST,
                                    result=result)
    for heading in ["Summary", "Assumptions", "Sources", "Branch flows", "Losses",
                    "Convergence", "Diagnostics", "Provenance"]:
        assert f". {heading}" in report
    assert chr(0x2014) not in report


def test_generator_reactive_limit_breach_is_warned():
    network, result = two_bus()
    network = json.loads(json.dumps(network))
    # Move the source onto a generator with a tight reactive range.
    grid = network["external_grids"][0]
    network["generators"].append({"generator_id": "g1", "bus_id": "receiving", "p_mw": 0.0,
                                  "vm_setpoint_pu": 0.99, "q_min_mvar": 0.5,
                                  "q_max_mvar": 0.6})
    report = render_loadflow_report(project_name="t", network=network, request=REQUEST,
                                    result=result)
    # The receiving bus only absorbs Q, so the generator there sits at 0 and breaches q_min.
    assert "BELOW Q MIN" in report and "**Warning:**" in report
    assert grid["external_grid_id"] in report
