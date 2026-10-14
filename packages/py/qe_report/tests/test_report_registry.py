"""Report registry dispatch must remain pure and preserve the power adapters."""

import pytest
from qe_report import (
    render_loadflow_report,
    render_motorstart_report,
    render_shortcircuit_report,
)
from qe_report.registry import REPORTS, ReportUnavailable, render_study_report


@pytest.mark.parametrize("kind", ["pv.yield", "plc.scan", "unregistered.module"])
def test_unavailable_report_is_explicit(kind):
    with pytest.raises(ReportUnavailable) as caught:
        render_study_report(kind, result={})
    assert caught.value.code == "ENGINE_UNAVAILABLE"


def test_power_dispatch_is_exact():
    assert REPORTS["loadflow"] is render_loadflow_report
    assert REPORTS["shortcircuit"] is render_shortcircuit_report
    assert REPORTS["motorstart"] is render_motorstart_report


def test_registered_report_has_no_engine_execution(monkeypatch):
    monkeypatch.setitem(REPORTS, "pv.yield", lambda **inputs: inputs["result"]["trace"])
    assert render_study_report("pv.yield", result={"trace": "authored"}) == "authored"
