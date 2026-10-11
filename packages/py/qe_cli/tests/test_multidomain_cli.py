import json
import shutil
from pathlib import Path

import pytest
from qe_cli.main import main
from qe_core import validate

ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture
def project(tmp_path):
    shutil.copytree(ROOT / 'examples/multi_domain', tmp_path, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('out'))
    return tmp_path


@pytest.mark.parametrize('study,kind,network', [('plant-flow', 'loadflow', 'mixed-plant'),
    ('plant-fault', 'shortcircuit', 'mixed-plant'), ('motor-start', 'motorstart', 'mixed-motor-feeder')])
def test_selects_bound_model_and_preserves_inputs(project, study, kind, network):
    before = {p.name: p.read_bytes() for p in project.glob('*.json')}
    assert main(['study', 'run', str(project), '--study', study]) == 0
    result = json.loads((project / 'out/results.json').read_text())
    assert result['network_id'] == network
    assert not validate(result, f'power/{kind}-result')
    assert {p.name: p.read_bytes() for p in project.glob('*.json')} == before
    assert network in (project / 'out/results.json').read_text()


def test_deferred_execution_is_explicit(project, capsys):
    assert main(['study', 'run', str(project), '--study', 'control-scan']) == 2
    assert 'UNSUPPORTED_STUDY' in capsys.readouterr().err
    assert not (project / 'out').exists()


def test_model_order_never_selects_first_power(project):
    path = project / 'manifest.json'
    data = json.loads(path.read_text())
    data['models'].reverse()
    path.write_text(json.dumps(data))
    assert main(['study', 'run', str(project), '--study', 'plant-flow']) == 0
    result = json.loads((project / 'out/results.json').read_text())
    assert result['network_id'] == 'mixed-plant'


def test_multiple_studies_same_type_requires_id(project, capsys):
    path = project / 'manifest.json'
    data = json.loads(path.read_text())
    duplicate = dict(data['studies'][0], study_id='another-flow')
    data['studies'].append(duplicate)
    path.write_text(json.dumps(data))
    assert main(['study', 'run', str(project), '--study', 'loadflow']) == 2
    assert 'STUDY_SELECTION' in capsys.readouterr().err


def test_wrong_result_network_is_rejected(project, capsys):
    from qe_cli.main import run_study
    from qe_power.adapters.pandapower import run_loadflow_file
    from qe_report import VoltageLimits
    request = json.loads((project / 'plant-flow.json').read_text())
    result = run_loadflow_file(project / 'plant.json', request)
    result['network_id'] = 'wrong-network'
    assert run_study(project, 'plant-flow', 'pandapower', VoltageLimits(),
                     lambda solver: lambda path, req: result) == 2
    assert 'RESULT_COVERAGE' in capsys.readouterr().err
    assert not (project / 'out').exists()
