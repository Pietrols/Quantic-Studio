"""Reject misleading handoffs and duplicate/stale review requests."""
import copy
import importlib.util
import json
from pathlib import Path

import pytest


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


validator = module("validate_evidence")
reviewer = module("request_review")
SHA = "a" * 40


def evidence():
    return {
        "wp": "WP-3.1", "tested_commit": SHA, "provider_model": "recorded-provider/model",
        "cli_version": "recorded", "implementer_sessions": ["worker-1"],
        "requirements": ["R-006"], "artifacts": ["ci/artifacts"],
        "checks": [{"command": "pytest", "exit_code": 0, "commit": SHA, "output": "ci/log"}],
        "reviews": [{"role": role, "session": role, "commit": SHA, "verdict": "pass"}
                    for role in sorted(validator.REVIEW_ROLES)], "open_blockers": [],
    }


def test_valid_structure():
    assert validator.validate(evidence()) == []


@pytest.mark.parametrize("mutation", [
    lambda d: d["checks"][0].update(exit_code=False),
    lambda d: d["checks"][0].update(exit_code=1),
    lambda d: d["checks"][0].update(commit="b" * 40),
    lambda d: d["reviews"][0].update(session="worker-1"),
    lambda d: d["reviews"][0].update(commit="b" * 40),
    lambda d: d["reviews"][0].update(role=["malformed"]),
    lambda d: d["reviews"].pop(),
    lambda d: d.update(open_blockers=["unresolved"]),
])
def test_reject_false_readiness(mutation):
    data = copy.deepcopy(evidence())
    mutation(data)
    assert validator.validate(data)


def test_template_incomplete():
    assert validator.validate(json.loads(Path(__file__).with_name("evidence-template.json").read_text()))


def fake(monkeypatch, comments=None, draft=False, changed=False):
    calls = []
    reads = 0

    def run(*args):
        nonlocal reads
        calls.append(args)
        if args == ("api", "user"):
            return json.dumps({"login": "manager"})
        if "--slurp" in args:
            return json.dumps([comments or []])
        if args[1].endswith("/pulls/83"):
            reads += 1
            return json.dumps({"state": "open", "draft": draft,
                               "head": {"sha": "b" * 40 if changed and reads > 1 else SHA}})
        return "{}"
    monkeypatch.setattr(reviewer, "gh", run)
    return calls


def test_post_and_idempotency(monkeypatch):
    calls = fake(monkeypatch)
    assert "Requested" in reviewer.request("Pietrols/Quantic-Studio", 83)
    assert sum("-f" in c for c in calls) == 1
    calls = fake(monkeypatch, [{"body": f"<!-- quantic-review-request:{SHA} -->",
                                "user": {"login": "manager"}}])
    assert "Already" in reviewer.request("Pietrols/Quantic-Studio", 83)
    assert not any("-f" in c for c in calls)


def test_unrelated_marker_does_not_suppress(monkeypatch):
    calls = fake(monkeypatch, [{"body": f"<!-- quantic-review-request:{SHA} -->",
                                "user": {"login": "someone-else"}}])
    reviewer.request("Pietrols/Quantic-Studio", 83)
    assert any("-f" in c for c in calls)


def test_dry_run(monkeypatch):
    calls = fake(monkeypatch)
    assert "@codex review" in reviewer.request("Pietrols/Quantic-Studio", 83, True)
    assert not any("-f" in c for c in calls)


@pytest.mark.parametrize("options", [{"draft": True}, {"changed": True}])
def test_no_post_to_unready_or_changed_pr(monkeypatch, options):
    calls = fake(monkeypatch, **options)
    with pytest.raises(ValueError):
        reviewer.request("Pietrols/Quantic-Studio", 83)
    assert not any("-f" in c for c in calls)
