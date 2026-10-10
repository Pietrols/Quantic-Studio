import os
import subprocess
import sys
from pathlib import Path

import pytest

from ..ownership import check_ownership, git
from .test_plan import sample

TOOLS = Path(__file__).resolve().parents[2]


def write(root, name, content="test\n"):
    target = root / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)


def commit(root):
    git(root, "add", "--all")
    git(root, "commit", "-qm", "fixture")


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "config", "user.name", "Test")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    write(tmp_path, "PLAN.md", sample())
    write(tmp_path, "docs/log/old.md")
    write(tmp_path, "docs/sources/entries/old.yaml")
    write(tmp_path, "tools/check_plan/existing.py")
    write(tmp_path, "outside.txt")
    commit(tmp_path)
    git(tmp_path, "update-ref", "refs/remotes/origin/main", "HEAD")
    git(tmp_path, "checkout", "-qb", "wp-0.3-plan-guard")
    return tmp_path


def check(repo):
    return check_ownership(repo, "wp-0.3-plan-guard")


def cli(repo, *args, env=None):
    environment = {key: value for key, value in os.environ.items() if not key.startswith("GITHUB_")}
    environment["PYTHONPATH"] = str(TOOLS)
    environment.update(env or {})
    return subprocess.run([sys.executable, "-m", "check_plan", *args], cwd=repo,
                          env=environment, capture_output=True, text=True)


def test_owned_paths_note_new_records_and_status_are_allowed(repo):
    for name in ["tools/check_plan/new file.py", "docs/learning/parsing-and-validation.md",
                 "docs/log/new.md", "docs/sources/entries/new.yaml"]:
        write(repo, name)
    write(repo, "PLAN.md", sample("[~] In progress | ChatGPT | branch wp-0.3-plan-guard | started 2026-10-10"))
    commit(repo)
    assert check(repo) == []
    result = cli(repo, "PLAN.md")
    assert result.returncode == 0 and "Owned paths valid" in result.stdout


@pytest.mark.parametrize("path", ["outside.txt", "tools/check_plan_extra/code.py",
                                 "docs/learning/wrong.md", "line\nbreak.txt"])
def test_unowned_files_rejected_with_path(repo, path):
    write(repo, path, "changed")
    commit(repo)
    errors = check(repo)
    assert any(repr(path) in error and "WP-0.3" in error for error in errors)


@pytest.mark.parametrize("path", ["docs/log/old.md", "docs/sources/entries/old.yaml"])
@pytest.mark.parametrize("action", ["modify", "delete", "rename"])
def test_existing_logs_and_sources_are_immutable(repo, path, action):
    if action == "modify":
        write(repo, path, "changed")
    elif action == "delete":
        (repo / path).unlink()
    else:
        (repo / path).rename(repo / (path + ".new"))
    commit(repo)
    assert any(path in error and "only new" in error for error in check(repo))


@pytest.mark.parametrize("old,new", [("outside.txt", "tools/check_plan/moved.py"),
                                    ("tools/check_plan/existing.py", "outside-new.py")])
def test_rename_checks_both_paths(repo, old, new):
    (repo / old).rename(repo / new)
    commit(repo)
    assert any("outside" in error for error in check(repo))


@pytest.mark.parametrize("replacement", [
    lambda p: p.replace("# Plan", "# Altered rules"),
    lambda p: p.replace("Lane: B", "Lane: A"),
    lambda p: p.replace("Check the plan.", "Change the acceptance."),
    lambda p: p.replace("WP-0.4 Contracts", "WP-0.4 Rewritten title"),
    lambda p: p.replace("Owned paths: `tools/check_plan/**`", "Owned paths: `**`"),
    lambda p: p.replace("Learning note: `docs/learning/parsing-and-validation.md`.", "Learning note: `outside.txt`"),
    lambda p: p.replace("Status: [ ] Not started\nLane: A", "Status: [x] Done | implemented by Me | commit abc1234 | 2026-10-10\nLane: A"),
])
def test_plan_cannot_change_other_fields_or_grant_itself_paths(repo, replacement):
    write(repo, "PLAN.md", replacement(sample()))
    write(repo, "outside.txt", "unauthorized")
    commit(repo)
    errors = check(repo)
    assert any("PLAN.md edits" in error for error in errors)
    assert any("outside.txt" in error for error in errors)


def test_own_change_record_can_be_added(repo):
    write(repo, "PLAN.md", sample(change="\n\n- due to new policy, while original was old, as it was better for clarity"))
    commit(repo)
    assert check(repo) == []


def test_change_record_cannot_be_rewritten(repo):
    write(repo, "PLAN.md", sample(change="\n\n- Original permanent decision."))
    commit(repo)
    git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    write(repo, "PLAN.md", sample(change="\n\n- Replacement decision."))
    commit(repo)
    assert any("permanent" in error for error in check(repo))


def test_explicit_plan_section_grant_is_respected(repo):
    plan = sample(owned="`PLAN.md` (section 8 only)") + "\n## 8. Next phase\n\nOriginal.\n\n## 9. Other\nProtected.\n"
    write(repo, "PLAN.md", plan)
    commit(repo)
    git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    updated = plan.replace("Original.", "Updated.").replace(
        "Status: [ ] Not started", "Status: [x] Done | implemented by Me | commit abc1234 | 2026-10-10", 1)
    write(repo, "PLAN.md", updated)
    commit(repo)
    assert check(repo) == []
    write(repo, "PLAN.md", plan.replace("Protected.", "Unauthorized."))
    commit(repo)
    assert any("outside owned section 8" in error for error in check(repo))


def test_explicit_whole_plan_grant(repo):
    write(repo, "PLAN.md", sample(owned="`PLAN.md`"))
    commit(repo)
    git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    write(repo, "PLAN.md", sample(owned="`PLAN.md`").replace("# Plan", "# Revised plan"))
    commit(repo)
    assert check(repo) == []


def test_new_wp_cannot_approve_itself(repo):
    write(repo, "PLAN.md", sample() + sample().replace("WP-0.3", "WP-9.3").replace("WP-0.4", "WP-9.4"))
    commit(repo)
    assert "absent from base" in " ".join(check_ownership(repo, "wp-9.3-self-approved"))


def test_missing_base_fails_closed(repo):
    result = cli(repo, "--check-paths", "--base", "missing/ref")
    assert result.returncode == 1 and "git rev-parse" in result.stderr


def test_summary_is_read_only_and_does_not_require_git(tmp_path):
    write(tmp_path, "PLAN.md", sample())
    result = cli(tmp_path, "--summary", "PLAN.md")
    assert result.returncode == 0 and "WP-0.3" in result.stdout


def test_malformed_sample_cli_and_missing_file(repo):
    write(repo, "bad.md", sample("[x] Done"))
    result = cli(repo, "bad.md")
    assert result.returncode == 1 and "WP-0.3: Status:" in result.stderr
    assert cli(repo, "missing.md").returncode == 1


def test_uncommitted_files_are_not_claimed_as_checked(repo):
    write(repo, "outside.txt", "working tree edit")
    assert check(repo) == []
    assert "committed changes" in cli(repo).stdout


def test_detached_head_explicit_branch(repo):
    git(repo, "checkout", "--detach", "-q")
    assert cli(repo, "--check-paths").returncode == 1
    assert cli(repo, "--check-paths", "--branch", "wp-0.3-plan-guard").returncode == 0


def test_pull_request_uses_actual_head_and_branch(repo):
    import json

    write(repo, "outside.txt", "bad")
    commit(repo)
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    event = repo / "event.json"
    event.write_text(json.dumps({"pull_request": {"head": {"sha": head}}}))
    git(repo, "checkout", "--detach", "-q", "origin/main")
    result = cli(repo, env={"GITHUB_EVENT_NAME": "pull_request", "GITHUB_HEAD_REF": "wp-0.3-plan-guard",
                            "GITHUB_EVENT_PATH": str(event)})
    assert result.returncode == 1 and "outside.txt" in result.stderr


def test_main_push_validates_without_branch_ownership(repo):
    git(repo, "checkout", "-q", "main")
    assert cli(repo, env={"GITHUB_EVENT_NAME": "push"}).returncode == 0


def test_merge_base_excludes_unrelated_main_changes(repo):
    git(repo, "checkout", "-q", "main")
    write(repo, "other-agent.txt")
    commit(repo)
    git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    git(repo, "checkout", "-q", "wp-0.3-plan-guard")
    write(repo, "tools/check_plan/own.py")
    commit(repo)
    assert check(repo) == []


def test_symlink_under_owned_path_requires_review(repo):
    (repo / "tools/check_plan/link").symlink_to("../../outside.txt")
    commit(repo)
    assert any("symlink" in error for error in check(repo))
