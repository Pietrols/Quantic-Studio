import copy
import json
import shutil
from pathlib import Path

import pytest
from qe_core import load_project, validate

ROOT = Path(__file__).resolve().parents[4]
EXAMPLE = ROOT / 'examples/multi_domain'


@pytest.fixture
def project(tmp_path):
    shutil.copytree(EXAMPLE, tmp_path, dirs_exist_ok=True, ignore=shutil.ignore_patterns('out'))
    return tmp_path


def change(folder, mutate):
    path = folder / 'manifest.json'
    data = json.loads(path.read_text())
    mutate(data)
    path.write_text(json.dumps(data))


def codes(folder):
    outcome = load_project(folder)
    assert not outcome.ok
    return {d.code for d in outcome.diagnostics}


def test_multi_domain_and_legacy(project):
    loaded = load_project(project)
    assert loaded.ok, loaded.diagnostics
    assert len(loaded.value.models) == 3 and len(loaded.value.studies) == 4
    assert loaded.value.model('plant').network.network_id == 'mixed-plant'
    assert loaded.value.studies[2].model_id == 'motor-feeder'
    assert {d.code for d in loaded.diagnostics} == {
        'DEFERRED_MODEL_VALIDATION', 'DEFERRED_STUDY_VALIDATION', 'DEFERRED_ASSET_VALIDATION'}
    assert len(loaded.value.assets) == 1
    with pytest.raises(ValueError, match='exactly one'):
        _ = loaded.value.network
    with pytest.raises(ValueError, match='not a power'):
        _ = loaded.value.model('control').network
    for folder in ['fourteen_bus', 'shortcircuit', 'motorstart']:
        legacy = load_project(ROOT / 'examples' / folder)
        assert legacy.ok
        assert len(legacy.value.models) == 1
        assert all(s.model_id == legacy.value.models[0].model_id for s in legacy.value.studies)
        assert legacy.value.network == legacy.value.models[0].network


@pytest.mark.parametrize('target', ['models', 'studies', 'assets', 'representations'])
def test_duplicate_identifiers(project, target):
    def mutate(data):
        items = data.get(target) if target in ('models', 'studies') else data['asset_registry']['assets']
        if target == 'representations':
            items = items[0]['representations']
        items.append(copy.deepcopy(items[0]))
    change(project, mutate)
    assert ('DUPLICATE_REPRESENTATION' if target == 'representations' else 'DUPLICATE_ID') in codes(project)


@pytest.mark.parametrize('target,expected', [
    ('study-model', 'UNKNOWN_MODEL'), ('asset-model', 'UNKNOWN_MODEL'),
    ('asset-element', 'UNKNOWN_ELEMENT'), ('asset-kind', 'UNKNOWN_ELEMENT'),
    ('study-kind', 'STUDY_MODEL_TYPE'),
])
def test_dangling_and_mismatched_bindings(project, target, expected):
    def mutate(data):
        if target == 'study-model':
            data['studies'][0]['model_id'] = 'missing'
        elif target == 'study-kind':
            data['studies'][0]['model_id'] = 'control'
        else:
            ref = data['asset_registry']['assets'][0]['representations'][0]
            ref[{'asset-model': 'model_id', 'asset-element': 'element_id', 'asset-kind': 'element_type'}[target]] = 'missing'
    change(project, mutate)
    assert expected in codes(project)


def test_request_must_match_bound_model(project):
    path = project / 'motor-start.json'
    data = json.loads(path.read_text())
    data['network_file'] = 'plant.json'
    path.write_text(json.dumps(data))
    assert 'NETWORK_MISMATCH' in codes(project)


@pytest.mark.parametrize('target', ['model', 'request', 'request-network'])
@pytest.mark.parametrize('mode', ['parent', 'absolute', 'symlink'])
def test_confined_paths(project, target, mode):
    outside = project.parent / 'outside.json'
    outside.write_text('{}')
    bad = '../outside.json' if mode == 'parent' else str(outside) if mode == 'absolute' else 'escape.json'
    if mode == 'symlink':
        (project / bad).symlink_to(outside)
    if target == 'request-network':
        path = project / 'motor-start.json'
        data = json.loads(path.read_text())
        data['network_file'] = bad
        path.write_text(json.dumps(data))
    else:
        change(project, lambda data: data['models' if target == 'model' else 'studies'][0].update(
            **({'file': bad} if target == 'model' else {'request_file': bad})))
    expected = 'SCHEMA_INVALID' if target == 'request-network' and mode != 'symlink' else 'PROJECT_PATH'
    assert expected in codes(project)


def test_manifest_symlink_is_confined(project):
    outside = project.parent / 'outside-manifest.json'
    outside.write_text('{}')
    (project / 'manifest.json').unlink()
    (project / 'manifest.json').symlink_to(outside)
    assert 'PROJECT_PATH' in codes(project)


@pytest.mark.parametrize('target', ['model', 'request'])
def test_file_alias_rejected(project, target):
    def mutate(data):
        if target == 'model':
            data['models'][1]['file'] = data['models'][0]['file']
        else:
            data['studies'][0]['request_file'] = data['models'][0]['file']
    change(project, mutate)
    assert ('MODEL_FILE_ALIAS' if target == 'model' else 'REQUEST_FILE_ALIAS') in codes(project)


@pytest.mark.parametrize('filename', ['control.json', 'scan.json'])
@pytest.mark.parametrize('payload', ['[]', '{', '{"v":NaN}'])
def test_deferred_does_not_mean_invalid_json_allowed(project, filename, payload):
    (project / filename).write_text(payload)
    assert codes(project) & {'MODEL_OBJECT', 'INPUT_READ', 'NONFINITE'}


def test_foreign_project_is_storable_without_engine(project):
    def mutate(data):
        data['models'] = [data['models'][2]]
        data['studies'] = [data['studies'][3]]
        data['asset_registry']['assets'] = []
    change(project, mutate)
    outcome = load_project(project)
    assert outcome.ok
    with pytest.raises(ValueError):
        _ = outcome.value.network


def test_registry_version_and_schema():
    data = json.loads((EXAMPLE / 'manifest.json').read_text())['asset_registry']
    assert not validate(data, 'project/asset-registry')
    data['schema_version'] = '0.3.0'
    assert validate(data, 'project/asset-registry')[0].code == 'SCHEMA_VERSION'


def test_all_legacy_manifest_archives_exact():
    # Historical schema bytes are immutable compatibility boundaries.
    import subprocess
    for version, commit in [('0.1', 'b721c28'), ('0.2', 'b721c28'), ('0.3', 'b721c28')]:
        old_path = f'contracts/v{version}/project/manifest.schema.json' if version != '0.3' else 'contracts/project/manifest.schema.json'
        expected = subprocess.check_output(['git', 'show', f'{commit}:{old_path}'], cwd=ROOT)
        assert (ROOT / f'contracts/v{version}/project/manifest.schema.json').read_bytes() == expected
