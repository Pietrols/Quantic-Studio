import copy
import json
import re
import shutil
from pathlib import Path

import pytest
from qe_core import load_project, validate
from qe_core.validation import diagnostic

ROOT = Path(__file__).resolve().parents[4]
EXAMPLE = ROOT / 'examples/motorstart'


def request():
    return json.loads((EXAMPLE / 'motorstart-request.json').read_text())


def result():
    text = (ROOT / 'docs/specs/motorstart-result.md').read_text()
    return json.loads(re.search(r'```json\n(.*?)\n```', text, re.S)[1])


def test_compatibility():
    for folder in ['fourteen_bus', 'shortcircuit', 'motorstart']:
        loaded = load_project(ROOT / 'examples' / folder)
        assert loaded.ok, loaded.diagnostics
    assert not validate(request(), 'power/motorstart-request')
    assert not validate(result(), 'power/motorstart-result')


@pytest.mark.parametrize('field,value', [
    ('shaft_rated_kw', 0), ('efficiency', 0), ('efficiency', 1.01),
    ('rated_power_factor', 0), ('rated_power_factor', 1.01),
    ('rated_voltage_kv', -1), ('locked_rotor_current_ratio', 0),
    ('locked_rotor_power_factor', 0), ('locked_rotor_power_factor', 1.01),
    ('shaft_rated_kw', float('nan')),
])
def test_invalid_nameplate(field, value):
    data = request()
    data['motor'][field] = value
    errors = validate(data, 'power/motorstart-request')
    assert errors
    assert errors[0].element_ref['element_id'] == 'motor-1'
    assert field in errors[0].element_ref['field']


@pytest.mark.parametrize('field', list(request()['motor']))
def test_nameplate_has_no_silent_defaults(field):
    data = request()
    del data['motor'][field]
    assert validate(data, 'power/motorstart-request')


@pytest.mark.parametrize('version', ['0.1.0', '0.2.0', '9.0.0'])
def test_request_version_strict(version):
    data = request()
    data['schema_version'] = version
    assert validate(data, 'power/motorstart-request')[0].code == 'SCHEMA_VERSION'


def test_old_manifest_cannot_claim_motorstart(tmp_path):
    shutil.copytree(EXAMPLE, tmp_path, dirs_exist_ok=True)
    data = json.loads((EXAMPLE / 'manifest.json').read_text())
    for version in ['0.1.0', '0.2.0']:
        data['schema_version'] = version
        (tmp_path / 'manifest.json').write_text(json.dumps(data))
        assert not load_project(tmp_path).ok


@pytest.mark.parametrize('field,value,code', [('bus_id', 'missing', 'UNKNOWN_BUS')])
def test_motor_reference(tmp_path, field, value, code):
    shutil.copytree(EXAMPLE, tmp_path, dirs_exist_ok=True)
    data = request()
    data['motor'][field] = value
    (tmp_path / 'motorstart-request.json').write_text(json.dumps(data))
    errors = load_project(tmp_path).diagnostics
    assert any(d.code == code and d.element_ref['element_id'] == 'motor-1' for d in errors)


def test_request_network_mismatch(tmp_path):
    shutil.copytree(EXAMPLE, tmp_path, dirs_exist_ok=True)
    data = request()
    data['network_file'] = 'other.json'
    (tmp_path / 'motorstart-request.json').write_text(json.dumps(data))
    assert any(d.code == 'NETWORK_MISMATCH' for d in load_project(tmp_path).diagnostics)


def test_noncompliance_is_successful_calculation():
    data = result()
    data['dip_limit_percent'] = 5
    data['passes_limit'] = data['bus_results'][1]['passes_limit'] = False
    assert not validate(data, 'power/motorstart-result')
    data['passes_limit'] = True
    assert validate(data, 'power/motorstart-result')


def test_signed_rise_and_exact_limit():
    data = result()
    row = data['bus_results'][1]
    row.update(locked_rotor_vm_pu=1.25, dip_percent=-25)
    assert not validate(data, 'power/motorstart-result')
    row.update(locked_rotor_vm_pu=.75, dip_percent=25)
    data['dip_limit_percent'] = 25
    assert not validate(data, 'power/motorstart-result')


def test_failed_second_solve_preserves_prestart():
    data = result()
    data.update(status='failed', passes_limit=None)
    row = data['bus_results'][1]
    for field in ['locked_rotor_vm_pu', 'dip_percent', 'passes_limit']:
        row[field] = None
        data['diagnostics'].append(diagnostic('UNAVAILABLE', 'Second solve failed', 'buses',
                                               row['bus_id'], field).to_dict())
    assert not validate(data, 'power/motorstart-result')
    bad = copy.deepcopy(data)
    bad['diagnostics'].pop()
    assert validate(bad, 'power/motorstart-result')
    row['passes_limit'] = True
    assert validate(data, 'power/motorstart-result')


@pytest.mark.parametrize('mutation', ['dip', 'status', 'duplicate', 'null', 'nan'])
def test_inconsistent_results_rejected(mutation):
    data = result()
    if mutation == 'dip':
        data['bus_results'][1]['dip_percent'] = 11
    elif mutation == 'status':
        data['status'] = 'failed'
    elif mutation == 'duplicate':
        data['bus_results'].append(copy.deepcopy(data['bus_results'][0]))
    elif mutation == 'null':
        data['bus_results'][0]['passes_limit'] = None
    else:
        data['bus_results'][0]['prestart_vm_pu'] = float('inf')
    assert validate(data, 'power/motorstart-result')
