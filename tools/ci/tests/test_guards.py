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
    return subprocess.run(
        [sys.executable, str(SCRIPT), check, "--root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )


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


@pytest.mark.parametrize(
    "owner,source",
    [
        ("qe_core", "import qe_power"),
        ("qe_core", "from qe_report import report"),
        ("qe_power", "from qe_pv.solar import model"),
        ("qe_power", "import pandapower"),
        ("qe_api", "import pandapower"),
        ("qe_api", "import qe_cli"),
        ("qe_core", "importlib.import_module('qe_power')"),
    ],
)
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
        "qe_api/src/qe_api/service.py": "import qe_power\nimport qe_report",
        "qe_report/src/qe_report/report.py": "import qe_power",
    }.items():
        add(repo, "packages/py/" + name, source.encode())
    assert run(repo, "boundaries").returncode == 0


def test_typescript_boundary(repo):
    add(repo, "packages/ts/ui.ts", b"import x from '../../py/qe_core/core.py';")
    assert run(repo, "boundaries").returncode == 1


@pytest.mark.parametrize(
    "owner,target",
    [
        ("qe_pv", "qe_power"),
        ("qe_pv", "qe_plc"),
        ("qe_plc", "qe_pv"),
        ("qe_circuit", "qe_power"),
        ("qe_pv", "qe_report"),
        ("qe_pv", "qe_api"),
    ],
)
def test_domains_cannot_import_other_packages(repo, owner, target):
    name = f"packages/py/{owner}/src/{owner}/invalid.py"
    add(repo, name, f"import {target}".encode())
    assert run(repo, "boundaries").returncode == 1


@pytest.mark.parametrize(
    "owner,source",
    [
        ("qe_pv", "import pvlib"),
        ("qe_power", "from pvlib import solarposition"),
        ("qe_core", "__import__('pvlib')"),
        ("qe_api", "importlib.import_module('pvlib')"),
    ],
)
def test_pvlib_only_in_its_named_adapter(repo, owner, source):
    name = f"packages/py/{owner}/src/{owner}/invalid.py"
    add(repo, name, source.encode())
    assert run(repo, "boundaries").returncode == 1


def test_new_domain_allowed_boundaries(repo):
    for name, source in {
        "qe_pv/src/qe_pv/engine.py": "from qe_core.stepping import Session",
        "qe_plc/src/qe_plc/scan.py": "from qe_core import validate",
        "qe_pv/src/qe_pv/adapters/pvlib/solar.py": "import pvlib\nfrom pvlib import solarposition",
        "qe_cli/src/qe_cli/pv/runner.py": "import qe_pv",
        "qe_report/src/qe_report/pv/report.py": "import qe_pv",
    }.items():
        add(repo, "packages/py/" + name, source.encode())
    assert run(repo, "boundaries").returncode == 0


@pytest.mark.parametrize(
    "owner,dependency", [("qe_pv", "qe-plc"), ("qe_plc", "qe-pv"), ("qe_core", "qe-pv")]
)
def test_internal_dependency_metadata_is_guarded(repo, owner, dependency):
    add(
        repo,
        f"packages/py/{owner}/pyproject.toml",
        f'[project]\nname="{owner}"\ndependencies=["{dependency}>=0.1"]\n'.encode(),
    )
    assert run(repo, "boundaries").returncode == 1
