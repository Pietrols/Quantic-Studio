"""Command line entry point: `qe study run <project-folder> --study loadflow`.

Exit codes:
  0  load flow converged, fault duties available, or motor-start dip check passed
  1  incomplete calculation or failed motor-start dip limit (outputs written)
  2  invalid inputs or report export failure (diagnostics printed)
  3  the requested solver is not installed
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Callable

from qe_core import load_project, validate
from qe_report import (
    PDFRenderError,
    VoltageLimits,
    render_loadflow_report,
    render_motorstart_report,
    render_pdf,
    render_shortcircuit_report,
)

# Each solver module must expose run_loadflow_file(network_path, request) -> loadflow-result.
SOLVERS: dict[str, str] = {
    "pandapower": "qe_power.adapters.pandapower",
    "textbook": "qe_power.textbook",
}
DEFAULT_SOLVER = "pandapower"


def _load_solver(name: str) -> Callable[[Path, dict[str, Any]], dict[str, Any]]:
    module = importlib.import_module(SOLVERS[name])
    return module.run_loadflow_file


def _print_diagnostics(diagnostics: list[Any]) -> None:
    for item in diagnostics:
        # qe_core returns Diagnostic dataclasses; solvers return contract dicts.
        item = asdict(item) if is_dataclass(item) else item
        ref = item.get("element_ref") or {}
        where = ""
        if ref:
            where = f" [{ref.get('element_type')}:{ref.get('element_id')}"
            where += f".{ref['field']}]" if ref.get("field") else "]"
        print(f"{item['severity'].upper()} {item['code']}{where}: {item['message']}",
              file=sys.stderr)


def run_study(
    project_folder: str | Path,
    study: str,
    solver: str,
    limits: VoltageLimits,
    solver_loader: Callable[[str], Callable] = _load_solver,
    report_format: str = "markdown",
) -> int:
    if report_format not in ("markdown", "pdf"):
        print("ERROR REPORT_FORMAT: choose markdown or pdf", file=sys.stderr)
        return 2
    root = Path(project_folder).resolve()
    loaded = load_project(root)
    if not loaded.ok:
        _print_diagnostics(loaded.diagnostics)
        return 2
    _print_diagnostics(loaded.diagnostics)
    project = loaded.value

    # Match by study_id first, then by study_type, so "--study loadflow" works.
    matches = [s for s in project.studies if s.study_id == study]
    matches = matches or [s for s in project.studies if s.study_type == study]
    if len(matches) != 1:
        found = ", ".join(s.study_id for s in project.studies) or "none"
        print(f"ERROR STUDY_SELECTION: expected exactly one study matching '{study}', "
              f"found {len(matches)} (studies in project: {found})", file=sys.stderr)
        return 2
    selected = matches[0]
    model = project.model(selected.model_id)
    if selected.study_type not in ("loadflow", "shortcircuit", "motorstart") or model.model_type != "power.network":
        print(f"ERROR UNSUPPORTED_STUDY: {selected.study_type} on {model.model_type} is stored but cannot execute", file=sys.stderr)
        return 2
    network = model.network

    if selected.study_type in ("shortcircuit", "motorstart") and solver != "pandapower":
        print(f"ERROR UNSUPPORTED_SOLVER: '{solver}' does not implement {selected.study_type}", file=sys.stderr)
        return 2

    try:
        if selected.study_type in ("shortcircuit", "motorstart"):
            run = getattr(importlib.import_module(SOLVERS[solver]), f"run_{selected.study_type}_file")
        else:
            run = solver_loader(solver)
    except ImportError as exc:
        print(f"ERROR SOLVER_UNAVAILABLE: solver '{solver}' is not installed ({exc})",
              file=sys.stderr)
        return 3

    network_path = root / model.file
    try:
        result = run(network_path, selected.request)
    except ValueError as exc:
        # Solvers reject inputs they cannot model (for example zero impedance) before
        # solving. pandapower's LoadflowInputError carries contract diagnostics; the
        # textbook solver raises a plain ValueError with a message.
        diagnostics = getattr(exc, "diagnostics", None)
        if diagnostics:
            _print_diagnostics(diagnostics)
        else:
            print(f"ERROR SOLVER_INPUT: {exc}", file=sys.stderr)
        return 2

    problems = validate(result, f"power/{selected.study_type}-result")
    if not problems and result["network_id"] != network.network_id:
        print("ERROR RESULT_COVERAGE: result network differs from selected model", file=sys.stderr)
        return 2
    if selected.study_type == "shortcircuit" and not problems:
        expected = {b["bus_id"] for b in network.data["buses"]}
        if {c["case"] for c in result["case_results"]} != set(selected.request["cases"]) or any(
                {b["bus_id"] for b in c["bus_results"]} != expected for c in result["case_results"]):
            print("ERROR RESULT_COVERAGE: fault result does not cover requested buses/cases", file=sys.stderr)
            return 2
    if selected.study_type == "motorstart" and not problems:
        expected = {b["bus_id"] for b in network.data["buses"]}
        if ({b["bus_id"] for b in result["bus_results"]} != expected
                or result["motor"] != selected.request["motor"]
                or result["dip_limit_percent"] != selected.request["dip_limit_percent"]
                or result["network_id"] != network.network_id):
            print("ERROR RESULT_COVERAGE: motor result differs from requested network/motor/limit", file=sys.stderr)
            return 2
    if problems:
        print("ERROR RESULT_CONTRACT: solver returned a result that breaks the contract",
              file=sys.stderr)
        _print_diagnostics(problems)
        return 2

    out_dir = root / "out"
    render = {"loadflow": render_loadflow_report, "shortcircuit": render_shortcircuit_report,
              "motorstart": render_motorstart_report}[selected.study_type]
    report = render(
        project_name=project.name,
        network=network.data,
        request=selected.request,
        result=result,
        **({"limits": limits} if selected.study_type == "loadflow" else {}),
    )
    try:
        pdf = render_pdf(report) if report_format == "pdf" else None
        out_dir.mkdir(exist_ok=True)
        # A Markdown-only rerun must not leave a PDF of a different study behind.
        (out_dir / "report.pdf").unlink(missing_ok=True)
        (out_dir / "results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        (out_dir / "report.md").write_text(report, encoding="utf-8")
        if pdf is not None:
            temporary = out_dir / ".report.pdf.tmp"
            try:
                temporary.write_bytes(pdf)
                temporary.replace(out_dir / "report.pdf")
            finally:
                temporary.unlink(missing_ok=True)
            print(f"PDF report: {out_dir / 'report.pdf'}")
    except (PDFRenderError, OSError) as exc:
        print(f"ERROR REPORT_EXPORT [study:{selected.study_id}.report_format]: {exc}", file=sys.stderr)
        return 2

    if selected.study_type == "shortcircuit":
        _print_diagnostics(result["diagnostics"])
        for case in result["case_results"]:
            _print_diagnostics(case["diagnostics"])
        print(f"Short-circuit study {result['status'].upper()} with {solver}. "
              f"Wrote {out_dir / 'results.json'} and {out_dir / 'report.md'}")
        return 0 if result["status"] == "success" else 1

    if selected.study_type == "motorstart":
        _print_diagnostics(result["diagnostics"])
        compliance = "UNKNOWN" if result["passes_limit"] is None else "PASS" if result["passes_limit"] else "FAIL"
        print(f"Motor-start calculation {result['status'].upper()}; dip limit {compliance}. "
              f"Wrote {out_dir / 'results.json'} and {out_dir / 'report.md'}")
        return 0 if result["status"] == "success" and result["passes_limit"] else 1

    converged = result["convergence"]["converged"]
    print(f"{'Converged' if converged else 'DID NOT CONVERGE'} in "
          f"{result['convergence']['iterations']} iterations with {solver}. "
          f"Wrote {out_dir / 'results.json'} and {out_dir / 'report.md'}")
    return 0 if converged else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="qe", description="Quantic Studio command line")
    commands = parser.add_subparsers(dest="command", required=True)
    study = commands.add_parser("study", help="Run engineering studies").add_subparsers(
        dest="study_command", required=True
    )
    run = study.add_parser("run", help="Run one study in a project folder")
    run.add_argument("project_folder", help="Folder containing manifest.json")
    run.add_argument("--study", required=True, help="Study id or type, e.g. loadflow, shortcircuit or motorstart")
    run.add_argument("--solver", choices=sorted(SOLVERS), default=DEFAULT_SOLVER)
    run.add_argument("--report-format", choices=["markdown", "pdf"], default="markdown",
                     help="PDF also retains report.md and results.json")
    run.add_argument("--vmin", type=float, default=0.95, help="Lowest acceptable voltage (pu)")
    run.add_argument("--vmax", type=float, default=1.05, help="Highest acceptable voltage (pu)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        limits = VoltageLimits(args.vmin, args.vmax)
    except ValueError as exc:
        print(f"ERROR VOLTAGE_LIMITS: {exc}", file=sys.stderr)
        return 2
    return run_study(args.project_folder, args.study, args.solver, limits, report_format=args.report_format)


if __name__ == "__main__":
    raise SystemExit(main())
