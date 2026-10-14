"""Pure static report dispatch. This module does not run or import any engine."""

from . import plc, pv
from .loadflow import render_loadflow_report
from .motorstart import render_motorstart_report
from .shortcircuit import render_shortcircuit_report


class ReportUnavailable(ValueError):
    code = "ENGINE_UNAVAILABLE"


REPORTS = {
    "loadflow": render_loadflow_report,
    "shortcircuit": render_shortcircuit_report,
    "motorstart": render_motorstart_report,
    "pv.yield": pv.render_report,
    "plc.scan": plc.render_report,
}


def render_study_report(study_type, **inputs):
    try:
        renderer = REPORTS[study_type]
    except KeyError:
        raise ReportUnavailable(f"No registered report for {study_type}") from None
    return renderer(**inputs)
