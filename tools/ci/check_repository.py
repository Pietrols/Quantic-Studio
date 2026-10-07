"""Tracked-file guards for PLAN.md section 3.2 and WP-0.2."""

import argparse
import ast
import subprocess
import sys
import tokenize
from pathlib import Path

# Engine imports must stay behind the corresponding adapter boundary.
ENGINES = {"pandapower"}


def tracked(root):
    output = subprocess.check_output(["git", "ls-files", "-z"], cwd=root)
    return [Path(p.decode()) for p in output.split(b"\0") if p]


def text_guard(root, paths):
    errors = []
    for path in paths:
        data = (root / path).read_bytes()
        if b"\0" in data:
            continue
        # UTF-8 is the repository text encoding; avoid silently skipping a file
        # with an isolated invalid byte before an otherwise valid punctuation mark.
        for line, value in enumerate(data.splitlines(), 1):
            if b"\xe2\x80\x94" in value:
                errors.append(f"{path}:{line}: forbidden U+2014")
    return errors


def reference_guard(root, paths):
    return [f"{p}: reference file must be under docs/assets/" for p in paths
            if p.suffix.lower() in {".pdf", ".epub", ".djvu"}
            and p.parts[:2] != ("docs", "assets")]


def imports(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield node.lineno, alias.name
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            yield node.lineno, node.module or ""
        elif isinstance(node, ast.Call):
            name = ast.unparse(node.func)
            if (name in {"__import__", "importlib.import_module"} and node.args
                    and isinstance(node.args[0], ast.Constant)):
                yield node.lineno, str(node.args[0].value)


def boundary_guard(root, paths):
    errors = []
    for path in paths:
        if path.parts[:2] == ("packages", "ts") and path.suffix in {
            ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"
        }:
            # TS must use the API rather than importing Python package paths.
            import re
            text = (root / path).read_text()
            for match in re.finditer(
                r"(?:from\s*|import\s*\(?|require\s*\()\s*['\"]([^'\"]+)", text
            ):
                target = match.group(1)
                if target.endswith(".py") or "packages/py/" in target or "qe_" in target:
                    errors.append(f"{path}: TypeScript cannot import Python: {target}")
        if path.suffix != ".py" or path.parts[:2] != ("packages", "py"):
            continue
        owner = path.parts[2]
        try:
            with tokenize.open(root / path) as stream:
                tree = ast.parse(stream.read(), filename=str(path))
        except (SyntaxError, UnicodeError) as exc:
            errors.append(f"{path}: cannot inspect imports: {exc}")
            continue
        for line, module in imports(tree):
            target = module.split(".")[0]
            if target.startswith("qe_") and target != owner:
                allowed = owner in {"qe_cli", "qe_report"} or (
                    owner != "qe_core" and target == "qe_core"
                )
                if not allowed:
                    errors.append(f"{path}:{line}: {owner} cannot import {target}")
            if target in ENGINES:
                expected = ("packages", "py", "qe_power", "src", "qe_power",
                            "adapters", target)
                if path.parts[:7] != expected:
                    errors.append(f"{path}:{line}: {target} requires qe_power/adapters/{target}/")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("check", choices=["text", "references", "boundaries"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    guards = {"text": text_guard, "references": reference_guard, "boundaries": boundary_guard}
    try:
        errors = guards[args.check](args.root, tracked(args.root))
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"{args.check}: cannot inspect repository: {exc}", file=sys.stderr)
        return 1
    for error in errors:
        print(error)
    print(f"{args.check}: {'FAIL' if errors else 'PASS'}")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
