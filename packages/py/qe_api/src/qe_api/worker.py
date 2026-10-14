"""Isolated solver worker, JSON in/out, no project file writes."""

from __future__ import annotations

import base64
import contextlib
import io
import json
import sys

from qe_core import validate
from qe_power.adapters import pandapower as adapter
from qe_report import (
    PDFRenderError,
    render_pdf,
    render_study_report,
)


def execute(payload):
    kind = payload["study_type"]
    if kind in ("pv.yield", "plc.scan"):
        from .handlers import HANDLERS

        key = (payload["model_type"], kind, payload["model"].get("schema_version"))
        if key not in HANDLERS:
            raise ValueError("Unregistered model/study contract")
        with contextlib.redirect_stdout(io.StringIO()):
            return HANDLERS[key](payload)
    solve = {
        "loadflow": adapter.solve,
        "shortcircuit": adapter.solve_shortcircuit,
        "motorstart": adapter.solve_motorstart,
    }[kind]
    # Some external solvers print progress; stdout is reserved for JSON transport.
    with contextlib.redirect_stdout(io.StringIO()):
        outcome = solve(payload["network"], payload["request"])
    if outcome.value is None:
        return {
            "error": True,
            "diagnostics": [d.to_dict() for d in outcome.diagnostics],
        }
    result = outcome.value
    problems = validate(result, f"power/{kind}-result")
    if result["network_id"] != payload["network"]["network_id"]:
        raise ValueError("Solver returned a different network")
    expected = {b["bus_id"] for b in payload["network"]["buses"]}
    rows = (
        [c["bus_results"] for c in result["case_results"]]
        if kind == "shortcircuit"
        else [result["bus_results"]]
    )
    converged = kind != "loadflow" or result["convergence"]["converged"]
    if converged and any({r["bus_id"] for r in row} != expected for row in rows):
        raise ValueError("Solver omitted requested buses")
    if problems:
        return {"error": True, "diagnostics": [d.to_dict() for d in problems]}
    report = render_study_report(
        kind,
        project_name=payload["project_name"],
        network=payload["network"],
        request=payload["request"],
        result=result,
    )
    response = {
        "study_type": kind,
        "model_id": payload["model_id"],
        "result": result,
        "report_markdown": report,
    }
    if payload.get("report_format", "markdown") == "pdf":
        try:
            response["report_pdf_base64"] = base64.b64encode(render_pdf(report)).decode(
                "ascii"
            )
        except PDFRenderError as exc:
            return {
                "error": True,
                "diagnostics": [
                    {
                        "code": "REPORT_EXPORT",
                        "severity": "error",
                        "message": str(exc),
                        "element_ref": {
                            "element_type": "study",
                            "element_id": payload["request"]["request_id"],
                            "field": "report_format",
                        },
                    }
                ],
            }
    return response


def main():
    try:
        response = execute(json.load(sys.stdin))
    except (ValueError, TypeError, KeyError, ArithmeticError) as exc:
        response = {
            "error": True,
            "diagnostics": [
                {
                    "code": "SOLVER_FAILURE",
                    "severity": "error",
                    "message": str(exc),
                    "element_ref": {
                        "element_type": "study",
                        "element_id": "worker",
                        "field": "solver",
                    },
                }
            ],
        }
    print(json.dumps(response, allow_nan=False))


if __name__ == "__main__":
    main()
