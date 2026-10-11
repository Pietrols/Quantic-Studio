import json
import shutil
from pathlib import Path

import pytest
from qe_cli.main import main
from qe_core import validate

ROOT = Path(__file__).resolve().parents[4]


@pytest.mark.parametrize('mode,exit_code', [('pass', 0), ('limit', 1), ('failed', 1), ('invalid', 2), ('textbook', 2)])
def test_motorstart_cli(tmp_path, mode, exit_code):
    shutil.copytree(ROOT / 'examples/motorstart', tmp_path, dirs_exist_ok=True, ignore=shutil.ignore_patterns('out'))
    path = tmp_path / 'motorstart-request.json'
    request = json.loads(path.read_text())
    if mode == 'limit':
        request['dip_limit_percent'] = 1
    elif mode == 'failed':
        request['max_iterations'] = 1
    elif mode == 'invalid':
        request['motor']['efficiency'] = 0
    path.write_text(json.dumps(request))
    solver = 'textbook' if mode == 'textbook' else 'pandapower'
    assert main(['study', 'run', str(tmp_path), '--study', 'motorstart', '--solver', solver]) == exit_code
    if exit_code == 2:
        assert not (tmp_path / 'out').exists()
        return
    data = json.loads((tmp_path / 'out/results.json').read_text())
    assert not validate(data, 'power/motorstart-result')
    assert {row['bus_id'] for row in data['bus_results']} == {'source', 'motor_bus'}
    report = (tmp_path / 'out/report.md').read_text()
    assert 'Pre-start (pu)' in report and 'Locked rotor (pu)' in report
    assert data['provenance']['input_hash_sha256'] in report
    assert 'Shaft rating (kW)' in report and 'not acceleration' in report
    assert ('**FAIL**' if mode == 'limit' else '**UNKNOWN**' if mode == 'failed' else '**PASS**') in report
    if mode == 'failed':
        assert 'n/a' in report
