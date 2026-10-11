"""CLI used by the existing CI hook and by developers with PYTHONPATH=tools."""

import argparse
import os
import sys
from pathlib import Path

from .ownership import check_ownership, git
from .plan import parse_plan, summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", nargs="?", default="PLAN.md")
    parser.add_argument("--summary", action="store_true", help="validate and print WP status table")
    parser.add_argument("--check-paths", action="store_true", help="require committed ownership check")
    parser.add_argument("--branch", help="WP branch name, including for detached checkouts")
    parser.add_argument("--base", default="origin/main", help="ownership comparison base ref")
    parser.add_argument("--head", default="HEAD", help="commit to check")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    args = parser.parse_args(argv)
    try:
        plan = parse_plan((args.root / args.plan).read_text(encoding="utf-8"))
        if plan.errors:
            print("\n".join(plan.errors), file=sys.stderr)
            return 1
        if args.summary:
            print(summary(plan))
        else:
            print(f"Plan valid: {len(plan.packages)} work packages")
        # CI runs on a synthetic merge checkout. Use the actual PR head for ownership.
        pr = os.environ.get("GITHUB_EVENT_NAME") == "pull_request"
        branch = args.branch or os.environ.get("GITHUB_HEAD_REF")
        if not branch and not args.summary:
            try:
                branch = git(args.root, "branch", "--show-current").decode().strip()
            except ValueError:
                branch = ""
        check = args.check_paths or (not args.summary and (pr or (branch or "").startswith("wp-")))
        if check:
            if Path(args.plan) != Path("PLAN.md"):
                raise ValueError("ownership always uses repository PLAN.md, not a sample plan")
            head = args.head
            if pr and head == "HEAD":
                import json

                event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
                head = event["pull_request"]["head"]["sha"]
            errors = check_ownership(args.root, branch or "", args.base, head)
            if errors:
                print("\n".join(errors), file=sys.stderr)
                return 1
            print(f"Owned paths valid: {branch} (committed changes against {args.base})")
        elif not args.summary:
            print("Ownership not requested: use --check-paths --branch wp-<id>-<name> on detached heads")
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f"check_plan: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
