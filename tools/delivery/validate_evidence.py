"""Validate review handoff structure; this does not attest test execution."""
import argparse
import json
import re
from pathlib import Path

SHA = re.compile(r"[0-9a-f]{40}")
REVIEW_ROLES = {"code-quality", "engineering", "implementation-quality"}


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["evidence must be an object"]
    for field in ("wp", "tested_commit", "provider_model", "cli_version"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"{field}: required nonempty string")
    if not SHA.fullmatch(str(data.get("tested_commit", ""))):
        errors.append("tested_commit: full 40-character Git SHA required")
    if not re.fullmatch(r"WP-\d+\.\d+", str(data.get("wp", ""))):
        errors.append("wp: expected WP-number.number")
    workers = data.get("implementer_sessions")
    if not isinstance(workers, list) or not workers or any(
        not isinstance(x, str) or not x.strip() for x in workers
    ):
        errors.append("implementer_sessions: nonempty session IDs required")
        workers = []
    for field in ("requirements", "artifacts"):
        values = data.get(field)
        if not isinstance(values, list) or not values or any(
            not isinstance(x, str) or not x.strip() for x in values
        ):
            errors.append(f"{field}: nonempty string list required")
    checks = data.get("checks")
    if not isinstance(checks, list) or not checks:
        errors.append("checks: at least one executed check required")
        checks = []
    for i, check in enumerate(checks):
        if not isinstance(check, dict):
            errors.append(f"checks[{i}]: object required")
            continue
        if not isinstance(check.get("command"), str) or not check["command"].strip():
            errors.append(f"checks[{i}]: command required")
        if type(check.get("exit_code")) is not int or check["exit_code"] != 0:
            errors.append(f"checks[{i}]: successful integer exit_code required")
        if check.get("commit") != data.get("tested_commit"):
            errors.append(f"checks[{i}]: stale or missing commit")
        if not isinstance(check.get("output"), str) or not check["output"].strip():
            errors.append(f"checks[{i}]: output artifact or CI URL required")
    reviews = data.get("reviews")
    if not isinstance(reviews, list):
        errors.append("reviews: list required")
        reviews = []
    seen = set()
    sessions = set()
    for i, review in enumerate(reviews):
        if not isinstance(review, dict):
            errors.append(f"reviews[{i}]: object required")
            continue
        role, session = review.get("role"), review.get("session")
        if not isinstance(role, str) or role not in REVIEW_ROLES or role in seen:
            errors.append(f"reviews[{i}]: unknown or duplicate role")
        else:
            seen.add(role)
        if not isinstance(session, str) or not session.strip():
            errors.append(f"reviews[{i}]: session required")
        elif session in workers or session in sessions:
            errors.append(f"reviews[{i}]: reviewer session must be separate")
        else:
            sessions.add(session)
        if review.get("commit") != data.get("tested_commit"):
            errors.append(f"reviews[{i}]: stale or missing commit")
        if review.get("verdict") != "pass":
            errors.append(f"reviews[{i}]: unresolved review")
    if seen != REVIEW_ROLES:
        errors.append("reviews: all three internal review roles required")
    if data.get("open_blockers") != []:
        errors.append("open_blockers: must be an explicit empty list")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        errors = validate(json.loads(args.path.read_text()))
    except (OSError, ValueError) as error:
        errors = [str(error)]
    print("\n".join(errors) if errors else "Structure ready; verify evidence independently.")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
