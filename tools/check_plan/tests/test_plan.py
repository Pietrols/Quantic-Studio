import pytest

from ..ownership import matches
from ..plan import parse_plan, summary


def sample(status="[ ] Not started", owned="`tools/check_plan/**`", change="none"):
    return f"""# Plan

## 7. Packages

### WP-0.3 Plan checker

Status: {status}
Lane: B
Depends on: WP-0.1
Owned paths: {owned}

Steps:

1. Check the plan.

Learning note: `docs/learning/parsing-and-validation.md`.
Change record: {change}

---

### WP-0.4 Contracts

Status: [ ] Not started
Lane: A
Depends on: WP-0.1
Owned paths: `contracts/**`
Learning note: none.
Change record: none
"""


@pytest.mark.parametrize("status", [
    "[ ] Not started",
    "[~] In progress | ChatGPT | branch wp-0.3-plan-guard | started 2026-10-10",
    "[~] In progress | ChatGPT | branch wp-0.3-plan-guard | started 2026-10-10 | blocked by owner",
    "[x] Done | implemented by ChatGPT | commit abc1234 | 2026-10-10",
    "[x] Done | implemented by Codex and Claude | commit abc1234 | 2026-10-10",
    "[x] Done | implemented by Peter | verified by Claude | commit bootstrap | 2026-10-10",
])
def test_current_and_historical_formats(status):
    assert parse_plan(sample(status)).errors == []


def test_changed_design_requires_persistent_explanation():
    reason = "due to new rules, while original was old rules, as it was better for clarity"
    status = f"[!] Changed design | {reason} | ChatGPT | 2026-10-10"
    assert parse_plan(sample(status, change=reason)).errors == []
    assert "Change record" in "\n".join(parse_plan(sample(status)).errors)


@pytest.mark.parametrize("status", [
    "[x] Done", "[ ] Not started extra", "[x] Done | implemented by | commit abc1234 | 2026-10-10",
    "[x] Done | implemented by ChatGPT | commit abc1234 | 2026-02-30",
    "[~] In progress | ChatGPT | branch wp-0.4-wrong | started 2026-10-10",
    "[~] In progress | ChatGPT | branch arbitrary | started 2026-10-10",
    "[!] Changed design | due to changes | ChatGPT | 2026-10-10",
    "[!] Changed design | due to , while original was old, as it was better for us | ChatGPT | 2026-10-10",
])
def test_bad_status_names_wp_and_rule(status):
    errors = parse_plan(sample(status)).errors
    assert errors and all("WP-0.3" in error and "Status" in error for error in errors)


@pytest.mark.parametrize("field", ["Status", "Lane", "Depends on", "Owned paths", "Learning note", "Change record"])
def test_missing_and_duplicate_fields(field):
    lines = sample().splitlines(keepends=True)
    index = next(i for i, line in enumerate(lines) if line.startswith(field + ":"))
    missing = "".join(lines[:index] + lines[index + 1:])
    duplicate = "".join(lines[:index] + [lines[index]] + lines[index:])
    for value in [missing, duplicate]:
        assert any("WP-0.3" in e and field in e for e in parse_plan(value).errors)


def test_markdown_examples_are_not_packages_or_fields():
    fenced = "```md\n### WP-9.9 Example\nStatus: nonsense\n```\n"
    plan = parse_plan(fenced + sample().replace("Steps:\n", "Steps:\n" + fenced))
    assert plan.errors == []
    assert list(plan.packages) == ["WP-0.3", "WP-0.4"]


def test_section_boundary_prevents_fields_leaking_into_last_wp():
    plan = parse_plan(sample() + "\n## 8. Notes\nStatus: this is prose\n")
    assert plan.errors == []


def test_duplicate_and_malformed_headings_and_empty_plan():
    assert "duplicate" in " ".join(parse_plan(sample() + sample()).errors)
    assert "malformed" in " ".join(parse_plan(sample() + "\n### WP-oops Broken\n").errors)
    assert parse_plan("No work packages").errors


def test_summary_includes_every_wp_and_title():
    output = summary(parse_plan(sample()))
    assert "WP-0.3" in output and "WP-0.4" in output
    assert "Plan checker" in output and "Not started" in output


@pytest.mark.parametrize("path,pattern,expected", [
    ("README.md", "/*", True), ("nested/README.md", "/*", False),
    ("tools/check_plan/a.py", "tools/check_plan/**", True),
    ("tools/check_plan/tests/a.py", "tools/check_plan/**", True),
    ("tools/check_plan_extra/a.py", "tools/check_plan/**", False),
    ("x/tools/check_plan/a.py", "tools/check_plan/**", False),
    ("tools/a.py", "tools/*.py", True), ("tools/tests/a.py", "tools/*.py", False),
    ("tools/a.py", "tools/**/*.py", True), ("tools/tests/a.py", "tools/**/*.py", True),
])
def test_anchored_globs(path, pattern, expected):
    assert matches(path, pattern) == expected
