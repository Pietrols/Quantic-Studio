import json
import shutil
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from qe_api import create_app
from qe_api.runner import Runner
from qe_core import validate

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def workspace(tmp_path):
    for name in ['multi_domain', 'fourteen_bus', 'shortcircuit', 'motorstart']:
        shutil.copytree(ROOT / 'examples' / name, tmp_path / name, ignore=shutil.ignore_patterns('out'))
    return tmp_path


def client(workspace, **kwargs):
    return TestClient(create_app(workspace, **kwargs), base_url='http://127.0.0.1')


@pytest.mark.parametrize('project,study,kind,network', [
    ('multi_domain', 'plant-flow', 'loadflow', 'mixed-plant'),
    ('multi_domain', 'plant-fault', 'shortcircuit', 'mixed-plant'),
    ('multi_domain', 'motor-start', 'motorstart', 'mixed-motor-feeder'),
    ('fourteen_bus', 'loadflow-base', 'loadflow', None),
    ('shortcircuit', 'fault', 'shortcircuit', None),
    ('motorstart', 'motorstart', 'motorstart', None),
])
def test_real_bounded_worker_returns_contract(workspace, project, study, kind, network):
    before = {p: p.read_bytes() for p in workspace.rglob('*.json')}
    response = client(workspace).post('/api/studies/run', json={'project_path': project, 'study_id': study})
    assert response.status_code == 200, response.text
    data = response.json()
    assert not validate(data['result'], f'power/{kind}-result')
    assert data['result']['provenance']['input_hash_sha256'] in data['report_markdown']
    if network:
        assert data['result']['network_id'] == network
    assert before == {p: p.read_bytes() for p in workspace.rglob('*.json')}
    assert not list(workspace.rglob('out'))


@pytest.mark.parametrize('path', ['../outside', '/tmp', 'C:\\other', 'escape'])
def test_project_paths_confined(workspace, path):
    (workspace / 'escape').symlink_to(workspace.parent, target_is_directory=True)
    response = client(workspace).get('/api/project', params={'project_path': path})
    assert response.status_code == 422
    assert response.json()['diagnostics'][0]['code'] == 'PROJECT_PATH'


def test_broken_project_and_unknown_study(workspace):
    c = client(workspace)
    assert c.get('/api/project', params={'project_path': 'missing'}).status_code == 404
    for sid,code in [('missing', 'UNKNOWN_STUDY'), ('control-scan', 'UNSUPPORTED_STUDY')]:
        response = c.post('/api/studies/run', json={'project_path':'multi_domain','study_id':sid})
        assert response.json()['diagnostics'][0]['code'] == code
    (workspace / 'multi_domain/plant-flow.json').unlink()
    assert c.get('/api/project', params={'project_path':'multi_domain'}).status_code == 422


def test_save_preserves_other_models_and_rejects_stale_or_invalid(workspace):
    c = client(workspace)
    before = {p: p.read_bytes() for p in (workspace/'multi_domain').glob('*.json')}
    opened = c.get('/api/model', params={'project_path':'multi_domain','model_id':'motor-feeder'}).json()
    opened['data']['buses'][1]['name'] = 'Edited label'
    body = {k: opened[k] for k in ['model_id','etag','data']}
    body['project_path'] = 'multi_domain'
    response = c.post('/api/model/save', json=body)
    assert response.status_code == 200, response.text
    assert response.json()['etag'] != opened['etag']
    assert all(p.read_bytes() == content for p,content in before.items() if p.name != 'motor-feeder.json')
    assert c.post('/api/model/save', json=body).status_code == 409
    body['etag'] = response.json()['etag']
    body['data']['buses'][1]['vn_kv'] = -1
    assert c.post('/api/model/save', json=body).status_code == 422
    assert json.loads((workspace/'multi_domain/motor-feeder.json').read_text())['buses'][1]['vn_kv'] == .4


def test_asset_and_motor_references_protect_deleted_elements(workspace):
    c = client(workspace)
    opened = c.get('/api/model', params={'project_path':'multi_domain','model_id':'motor-feeder'}).json()
    body = {k: opened[k] for k in ['model_id','etag','data']}
    body['project_path']='multi_domain'
    body['data']['lines'] = []
    response = c.post('/api/model/save', json=body)
    assert response.status_code == 422 and response.json()['diagnostics'][0]['code'] == 'UNKNOWN_ELEMENT'
    body['data']['buses'] = body['data']['buses'][:1]
    assert c.post('/api/model/save', json=body).status_code == 422


def test_timeout_and_failure_are_structured(workspace):
    for command,code,status in [([sys.executable,'-c','import time; time.sleep(5)'],'STUDY_TIMEOUT',504),
                                ([sys.executable,'-c','print("broken")'],'WORKER_FAILURE',500)]:
        runner = Runner(timeout_s=.1 if status==504 else 10, command=command)
        response = client(workspace,runner=runner).post('/api/studies/run',json={'project_path':'motorstart','study_id':'motorstart'})
        assert response.status_code == status
        assert response.json()['diagnostics'][0]['code'] == code
        assert runner.slots.acquire(blocking=False)
        runner.slots.release()


def test_busy_and_limits(workspace):
    runner = Runner(max_workers=1)
    runner.slots.acquire()
    c = client(workspace,runner=runner)
    response = c.post('/api/studies/run',json={'project_path':'motorstart','study_id':'motorstart'})
    assert response.status_code==429
    runner.slots.release()
    assert client(workspace,max_buses=1).get('/api/project',params={'project_path':'motorstart'}).status_code==413
    assert client(workspace,max_file_bytes=100).post('/api/studies/run',content='x'*101,
        headers={'content-type':'application/json'}).status_code==413


def test_origin_host_and_bad_request(workspace):
    c = client(workspace)
    assert c.get('/health',headers={'origin':'https://untrusted.invalid'}).status_code==403
    assert c.get('/health',headers={'host':'untrusted.invalid'}).status_code==400
    assert c.post('/api/studies/run',json={}).status_code==422
    assert c.get('/health').status_code==200


def test_failed_solve_still_returns_result_and_report(workspace):
    path=workspace/'motorstart/motorstart-request.json'
    request=json.loads(path.read_text())
    request['max_iterations']=1
    path.write_text(json.dumps(request))
    response=client(workspace).post('/api/studies/run',json={'project_path':'motorstart','study_id':'motorstart'})
    assert response.status_code==200,response.text
    assert response.json()['result']['status']=='failed'
    assert 'UNKNOWN' in response.json()['report_markdown']


def test_declared_files_are_bounded_without_json_extension(workspace):
    path = workspace/'multi_domain/manifest.json'
    data = json.loads(path.read_text())
    data['models'][2]['file'] = 'large.txt'
    path.write_text(json.dumps(data))
    (workspace/'multi_domain/large.txt').write_text('x'*100_001)
    response = client(workspace,max_file_bytes=100_000).get('/api/project',params={'project_path':'multi_domain'})
    assert response.status_code == 413
