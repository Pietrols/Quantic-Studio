"""Exercise guards against real tracked files in isolated Git repositories."""
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "check_repository.py"


@pytest.fixture
def repo(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    return tmp_path


def add(repo, path, contents):
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(contents)
    subprocess.run(["git", "add", "--", path], cwd=repo, check=True)


def run(repo, check):
    return subprocess.run([sys.executable, str(SCRIPT), check, "--root", str(repo)],
                          capture_output=True, text=True, check=False)


def test_text_tracks_hidden_files_but_ignores_untracked(repo):
    (repo / "scratch").write_text(chr(0x2014))
    assert run(repo, "text").returncode == 0
    add(repo, ".hidden", ("line\n" + chr(0x2014)).encode())
    result = run(repo, "text")
    assert result.returncode == 1
    assert ".hidden:2:" in result.stdout
    add(repo, ".hidden", b"line\nplain")
    assert run(repo, "text").returncode == 0


@pytest.mark.parametrize("name", ["book.pdf", "folder/book.EPUB", "book.djvu"])
def test_reference_guard(repo, name):
    add(repo, "docs/assets/own.pdf", b"own report")
    assert run(repo, "references").returncode == 0
    add(repo, name, b"synthetic acceptance fixture, no book content")
    result = run(repo, "references")
    assert result.returncode == 1 and name in result.stdout


@pytest.mark.parametrize("owner,source", [
    ("qe_core", "import qe_power"),
    ("qe_core", "from qe_report import report"),
    ("qe_power", "from qe_pv.solar import model"),
    ("qe_power", "import pandapower"),
    ("qe_core", "importlib.import_module('qe_power')"),
])
def test_forbidden_imports(repo, owner, source):
    name = f"packages/py/{owner}/src/{owner}/bad.py"
    add(repo, name, source.encode())
    result = run(repo, "boundaries")
    assert result.returncode == 1 and name in result.stdout


def test_allowed_dependencies(repo):
    for name, source in {
        "qe_core/src/qe_core/core.py": "import pathlib",
        "qe_power/src/qe_power/model.py": "from qe_core import units",
        "qe_power/src/qe_power/adapters/pandapower/run.py": "import pandapower",
        "qe_cli/src/qe_cli/cli.py": "import qe_power",
        "qe_report/src/qe_report/report.py": "import qe_power",
    }.items():
        add(repo, "packages/py/" + name, source.encode())
    assert run(repo, "boundaries").returncode == 0


def test_typescript_boundary(repo):
    add(repo, "packages/ts/ui.ts", b"import x from '../../py/qe_core/core.py';")
    assert run(repo, "boundaries").returncode == 1
