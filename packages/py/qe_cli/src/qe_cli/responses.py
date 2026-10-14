"""Common validated suite response and Markdown transport for suite handlers."""

from qe_core.plc_contracts import validate_plc_result
from qe_core.pv_contracts import validate_pv_result
from qe_core.validation import diagnostic
from qe_report import render_study_report


def study_response(payload, result):
    """Called by suite-local execute after the engine. Never accepts unvalidated results."""
    if payload["study_type"] == "pv.yield":
        problems = validate_pv_result(
            result, request=payload["request"], site=payload["model"]
        )
    elif payload["study_type"] == "plc.scan":
        problems = validate_plc_result(
            result,
            request=payload["request"],
            model=payload["model"],
            events=payload["series"],
        )
    else:
        raise ValueError("Unregistered suite result")
    if problems:
        return {"error": True, "diagnostics": [item.to_dict() for item in problems]}
    expected = sorted(
        payload["input_files"], key=lambda item: (item["role"], item["path"])
    )
    actual = sorted(
        result["execution"]["input_files"],
        key=lambda item: (item["role"], item["path"]),
    )
    if actual != expected:
        return {
            "error": True,
            "diagnostics": [
                diagnostic(
                    "RESULT_PROVENANCE",
                    "Result hashes do not identify the bounded input snapshot",
                    "study",
                    payload["request"]["execution"]["study_id"],
                    "provenance.input_files",
                ).to_dict()
            ],
        }
    report = render_study_report(
        payload["study_type"],
        project_name=payload["project_name"],
        model=payload["model"],
        request=payload["request"],
        result=result,
    )
    response = {
        "study_type": payload["study_type"],
        "model_id": payload["model_id"],
        "result": result,
        "report_markdown": report,
    }
    return response
