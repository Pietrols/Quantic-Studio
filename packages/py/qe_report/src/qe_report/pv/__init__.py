"""Pure PV report seam, filled by the suite WP."""


def render_report(**inputs):
    from qe_report.registry import ReportUnavailable

    raise ReportUnavailable(
        "PV report is unavailable until its study engine is connected"
    )
