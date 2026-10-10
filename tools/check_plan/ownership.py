"""Check the complete committed branch diff against merge-base permissions."""

import fnmatch
import re
import subprocess
from pathlib import PurePosixPath

from .plan import BRANCH, parse_plan


def git(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    if result.returncode:
        raise ValueError("git " + args[0] + ": " + result.stderr.decode(errors="replace").strip())
    return result.stdout


def resolve(root, ref):
    # Resolve first: arbitrary CLI refs cannot be interpreted as Git options later.
    return git(root, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}").decode().strip()


def matches(path, pattern):
    """Anchored path globs: * matches one segment; ** matches zero or more segments."""
    parts, patterns = path.split("/"), pattern.lstrip("/").split("/")

    def match(a, b):
        if not b:
            return not a
        if b[0] == "**":
            return match(a, b[1:]) or bool(a) and match(a[1:], b)
        return bool(a) and fnmatch.fnmatchcase(a[0], b[0]) and match(a[1:], b[1:])

    return match(parts, patterns)


def plan_permission(wp):
    """An explicit PLAN.md grant can be whole-file or section-scoped."""
    entry = re.search(r"`PLAN\.md`([^,\n]*)", wp.value("Owned paths"))
    if not entry:
        return None
    annotation = entry[1].strip()
    if not annotation:
        return "all"
    match = re.fullmatch(r"\(section (\d+) only\)", annotation)
    if not match:
        raise ValueError(f"{wp.id}: unsupported PLAN.md ownership restriction: {annotation}")
    return match[1]


def mask_section(plan, section):
    starts = [(i, level) for i, level, title in plan.headings
              if level == 2 and re.match(re.escape(section) + r"\.\s", title)]
    if len(starts) != 1:
        raise ValueError(f"PLAN.md: expected exactly one section {section}")
    start = starts[0][0]
    end = next((i for i, level, _ in plan.headings if i > start and level <= 2), len(plan.lines))
    return "".join(plan.lines[:start] + ["<owned section>\n"] + plan.lines[end:])


def mask_wp(plan, wp_id):
    wp = plan.packages[wp_id]
    status_line = wp.fields["Status"][0][0]
    change_line = wp.fields["Change record"][0][0]
    lines = plan.lines.copy()
    lines[status_line] = "<own status>\n"
    lines[change_line:wp.change_end] = ["<own change record>\n"]
    return "".join(lines)


def check_plan_edit(before, after, wp_id):
    permission = plan_permission(before.packages[wp_id])
    if permission == "all":
        return []
    if wp_id not in after.packages:
        return [f"{wp_id}: PLAN.md cannot remove its WP"]
    errors = []
    old_masked, new_masked = mask_wp(before, wp_id), mask_wp(after, wp_id)
    if permission:
        # Section ownership supplements the standing permission for own fields.
        old_masked = mask_section(parse_plan(old_masked), permission)
        new_masked = mask_section(parse_plan(new_masked), permission)
    if old_masked != new_masked and permission:
        errors.append(f"{wp_id}: PLAN.md changes outside owned section {permission}")
    elif old_masked != new_masked:
        errors.append(f"{wp_id}: PLAN.md edits must be limited to own Status and Change record")
    old, new = before.packages[wp_id], after.packages[wp_id]
    old_record = "".join(before.lines[old.fields["Change record"][0][0]:old.change_end])
    new_record = "".join(after.lines[new.fields["Change record"][0][0]:new.change_end])
    if old_record.strip() not in {"Change record: none", "Change record:"}:
        if not new_record.rstrip().startswith(old_record.rstrip()):
            errors.append(f"{wp_id}: Change record is permanent; append rather than rewrite")
    return errors


def check_ownership(root, branch, base="origin/main", head="HEAD"):
    match = BRANCH.fullmatch(branch)
    if not match:
        raise ValueError("ownership requires branch wp-<id>-<short-name>; got " + repr(branch))
    wp_id = "WP-" + match[1]
    base_sha, head_sha = resolve(root, base), resolve(root, head)
    ancestor = git(root, "merge-base", base_sha, head_sha).decode().strip()
    before = parse_plan(git(root, "show", f"{ancestor}:PLAN.md").decode("utf-8"))
    after = parse_plan(git(root, "show", f"{head_sha}:PLAN.md").decode("utf-8"))
    if before.errors or after.errors:
        return ["base: " + e for e in before.errors] + ["head: " + e for e in after.errors]
    if wp_id not in before.packages:
        return [f"{wp_id}: absent from base PLAN.md; a branch cannot approve its own WP"]
    wp = before.packages[wp_id]
    patterns = re.findall(r"`([^`]+)`", wp.value("Owned paths"))
    # .gitkeep is prose in the historical skeleton WP, not an unrestricted grant.
    patterns = [p for p in patterns if p != ".gitkeep"]
    for pattern in patterns:
        if ".." in pattern.split("/") or "\\" in pattern:
            raise ValueError(f"{wp_id}: unsafe Owned paths pattern {pattern!r}")
    learning = re.findall(r"`([^`]+)`", wp.value("Learning note"))
    note = learning[0] if learning else None
    modes = {}
    for record in git(root, "ls-tree", "-rz", head_sha).split(b"\0"):
        if record:
            meta, path = record.split(b"\t", 1)
            modes[path.decode("utf-8")] = meta.split()[0]
    # No renames: a move is a deletion plus addition, so both paths are checked.
    changes = git(root, "diff", "--name-status", "-z", "--no-renames",
                  ancestor, head_sha, "--").split(b"\0")
    errors = []
    for index in range(0, len(changes) - 1, 2):
        status, raw_path = changes[index:index + 2]
        path = raw_path.decode("utf-8")
        if modes.get(path) in {b"120000", b"160000"}:
            errors.append(f"{wp_id}: {path!r}: symlink/submodule requires explicit manual review")
            continue
        if path == "PLAN.md":
            errors.extend(check_plan_edit(before, after, wp_id))
        elif path.startswith(("docs/log/", "docs/sources/entries/")):
            if status != b"A":
                errors.append(f"{wp_id}: {path!r}: only new log/source files are allowed")
        elif path == note or any(matches(path, pattern) for pattern in patterns):
            continue
        else:
            errors.append(f"{wp_id}: {str(PurePosixPath(path))!r}: outside Owned paths")
    return errors
