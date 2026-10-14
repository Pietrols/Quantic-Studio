"""Decision D11: reports state each equation, its substituted values and its result.

The expected strings carry hand-calculated values (see the comments); they are
the same values as in qe_power/tests/adapters/test_calculation_traces.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from qe_power.adapters.pandapower import run_shortcircuit_file
from qe_power.adapters.pandapower.motorstart import run_motorstart_file
from qe_power.adapters.pandapower.solver import run_loadflow_file
from qe_report import (
    render_loadflow_report,
    render_motorstart_report,
    render_pdf,
    render_shortcircuit_report,
)

REPO = Path(__file__).resolve().parents[4]


def _inputs(folder, request):
    folder = REPO / "examples" / folder
    return json.loads((folder / "network.json").read_text()), json.loads((folder / request).read_text()), folder


@pytest.fixture(scope="module")
def shortcircuit_report():
    network, request, folder = _inputs("shortcircuit", "shortcircuit-request.json")
    result = run_shortcircuit_file(folder / "network.json", request)
    return render_shortcircuit_report(project_name="Feeder", network=network, request=request, result=result)


def test_shortcircuit_report_states_method_with_sources(shortcircuit_report):
    method = shortcircuit_report.split("## Method", 1)[1].split("## Equipment inputs", 1)[0]
    for text in ("Z_Q = c U_nQ^2 / S''_kQ", "eq. 8.1, p. 48", "K_T = 0.95 c_max / (1 + 0.6 x_T)", "eq. 9.14, p. 79",
                 "Ik'' = c Un / (sqrt(3) |Z_k|)", "kappa = 1.02 + 0.98 exp(-3 R/X)", "eqs. 11.22",
                 "Ith = Ik'' sqrt(m + n)", "eqs. 13.1 and 13.2, p. 117", "decision D10"):
        assert text in method


def test_shortcircuit_report_shows_worked_numbers(shortcircuit_report):
    block = shortcircuit_report.split("### Worked calculation: bus lv, maximum case", 1)[1].split("###", 1)[0]
    # Z_Q = 1.1 * 20^2 / 1000 = 0.44 ohm; line 0.4 + j0.8; Z_k = 0.443782 + j1.23782; Ik'' = 9.65935 kA;
    # kappa 1.35428; ip 18.5001 kA; m 0.00963712; Ith 9.70579 kA.
    for text in ("1.1 * 20^2 / 1000 = 0.44 ohm", "(0.2 + j0.4) ohm/km * 2 km", "0.443782 + j1.23782 ohm",
                 "1.1 * 20 / (sqrt(3) * 1.31496) = 9.65935 kA", "= 1.35428", "= 18.5001 kA",
                 "m = 0.00963712", "= 9.70579 kA"):
        assert text in block
    assert "### Worked calculation: bus lv, minimum case" in shortcircuit_report


def test_motorstart_report_shows_worked_numbers():
    network, request, folder = _inputs("motorstart", "motorstart-request.json")
    result = run_motorstart_file(folder / "network.json", request)
    report = render_motorstart_report(project_name="Motor", network=network, request=request, result=result)
    # I_r = 56.603 A, I_LR = 339.618 A, |Z_LR| = 0.68 ohm, angle 72.5424 deg, S = 0.0705882 + j0.224456 MVA.
    for text in ("= 56.603 A", "= 339.618 A", "= 0.68 ohm", "acos(0.3) = 72.5424 deg",
                 "= 0.0705882 + j0.224456 MVA", "section 6.6.2, pp. 333 to 334", "Bus motor_bus: dip = 100 *"):
        assert text in report


def test_loadflow_report_states_method_and_closes_power_balance():
    network, request, folder = _inputs("fourteen_bus", "loadflow-request.json")
    result = run_loadflow_file(folder / "network.json", request)
    report = render_loadflow_report(project_name="14", network=network, request=request, result=result)
    assert "eqs. 6.6.2 and 6.6.3, p. 354" in report and "## 11. Power balance check" in report
    assert "not enforced by the solver" not in report  # pandapower enforces Q limits since WP-1.1
    balance = report.split("## 11. Power balance check", 1)[1]
    residuals = [float(cell) for line in balance.splitlines() if line.startswith("| bus-")
                 for cell in line.strip("|").split("|")[4:6] if cell.strip() not in ("n/a",)]
    assert residuals and max(abs(r) for r in residuals) < 1e-6


def test_worked_reports_render_to_pdf(shortcircuit_report):
    assert render_pdf(shortcircuit_report).startswith(b"%PDF")
