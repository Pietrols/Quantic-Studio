"""Explicit, per-head Codex review request through an already authenticated gh CLI."""
import argparse
import json
import re
import subprocess


def gh(*args):
    return subprocess.check_output(["gh", *args], text=True)


def request(repo, pr, dry_run=False):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo) or pr < 1:
        raise ValueError("valid owner/repository and positive PR number required")
    info = json.loads(gh("api", f"repos/{repo}/pulls/{pr}"))
    if info.get("state") != "open" or info.get("draft"):
        raise ValueError("PR must be open and ready for review")
    sha = info["head"]["sha"]
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("invalid head SHA")
    marker = f"<!-- quantic-review-request:{sha} -->"
    pages = json.loads(gh("api", "--paginate", "--slurp", f"repos/{repo}/issues/{pr}/comments"))
    actor = json.loads(gh("api", "user"))["login"]
    if any(marker in c.get("body", "") and c.get("user", {}).get("login") == actor
           for page in pages for c in page):
        return f"Already requested by {actor} for {sha}"
    body = f"@codex review\n\nReview head {sha}; follow AGENTS.md and docs/delivery/.\n\n{marker}"
    if dry_run:
        return body
    # Recheck immediately before posting; serialized manager invocation still required.
    latest = json.loads(gh("api", f"repos/{repo}/pulls/{pr}"))
    if latest["head"]["sha"] != sha or latest.get("state") != "open" or latest.get("draft"):
        raise ValueError("PR changed during preparation; inspect and retry")
    gh("api", f"repos/{repo}/issues/{pr}/comments", "-f", "body=" + body)
    return f"Requested review for {sha}; completion is not yet confirmed"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        print(request(args.repo, args.pr, args.dry_run))
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Review request failed: {error}\n")


if __name__ == "__main__":
    main()
