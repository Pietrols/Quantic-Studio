import copy
import json
from pathlib import Path

import pytest
from qe_core import load_project, validate
from qe_core.provenance import provenance
from qe_core.validation import diagnostic

ROOT = Path(__file__).resolve().parents[4]
EXAMPLE = ROOT / 'examples/shortcircuit'


def data(name):
    return json.loads((EXAMPLE / (name + '.json')).read_text())


def result():
    return {'schema_version': '0.2.0', 'result_id': 'test', 'network_id': 'test', 'fault_type': '3ph',
            'fault_duration_s': 1, 'frequency_hz': 50, 'lv_tolerance_percent': 10, 'status': 'success',
            'case_results': [{'case': 'max', 'status': 'success', 'diagnostics': [],
                              'bus_results': [{'bus_id': 'b', 'voltage_factor': 1.1,
                                               'ikss_ka': 1, 'ip_ka': 2, 'ith_ka': 1.1}]}],
            'assumptions': ['Synthetic schema values, not numerical verification.'], 'diagnostics': [],
            'provenance': provenance('schema-test', '1', 'a' * 64)}


def test_old_and_new_projects_load():
    assert load_project(ROOT / 'examples/fourteen_bus').ok
    loaded = load_project(EXAMPLE)
    assert loaded.ok, loaded.diagnostics
    assert loaded.value.studies[0].study_type == 'shortcircuit'


def test_version_dispatch_is_strict():
    network = data('network')
    assert not validate(network, 'power/network')
    network['schema_version'] = '0.1.0'
    assert validate(network, 'power/network')  # Fault fields cannot masquerade as v0.1.
    network['schema_version'] = '9.0.0'
    assert validate(network, 'power/network')[0].code == 'SCHEMA_VERSION'
    request = data('shortcircuit-request')
    request['schema_version'] = '0.1.0'
    assert validate(request, 'power/shortcircuit-request')


@pytest.mark.parametrize('field,value', [('fault_duration_s', 0), ('frequency_hz', 0),
    ('lv_tolerance_percent', 7), ('cases', ['max', 'max']), ('cases', []), ('fault_type', '1ph')])
def test_invalid_requests(field, value):
    request = data('shortcircuit-request')
    request[field] = value
    assert validate(request, 'power/shortcircuit-request')


@pytest.mark.parametrize('field,value', [('s_sc_max_mva', 0), ('s_sc_min_mva', -1),
                                         ('rx_max', -1), ('rx_min', float('inf'))])
def test_invalid_grid_inputs(field, value):
    network = data('network')
    network['external_grids'][0][field] = value
    errors = validate(network, 'power/network')
    assert errors and errors[0].element_ref['element_id'] == 'grid'


def test_generator_and_temperature_fields():
    network = data('network')
    network['generators'] = [{'generator_id': 'g', 'bus_id': 'lv', 'p_mw': 0,
        'vm_setpoint_pu': 1, 'sn_mva': 1, 'vn_kv': 0.4, 'xdss_pu': 0.2,
        'rdss_ohm': 0.01, 'cos_phi': 0.8, 'voltage_control_range_percent': 5}]
    assert not validate(network, 'power/network')
    for field in ['sn_mva', 'vn_kv', 'xdss_pu', 'cos_phi']:
        bad = copy.deepcopy(network)
        bad['generators'][0][field] = 0
        assert validate(bad, 'power/network')
    network['lines'] = [{'line_id': 'l', 'from_bus': 'hv', 'to_bus': 'lv', 'length_km': 1,
                         'r_ohm_per_km': 1, 'x_ohm_per_km': 1, 'end_temperature_celsius': 19}]
    assert validate(network, 'power/network')


def test_partial_and_failed_results_require_diagnostics():
    value = result()
    assert not validate(value, 'power/shortcircuit-result')
    case = value['case_results'][0]
    value['status'] = case['status'] = 'partial'
    case['bus_results'][0]['ip_ka'] = None
    assert validate(value, 'power/shortcircuit-result')
    case['diagnostics'].append(diagnostic('UNAVAILABLE', 'Unsupported duty', 'buses', 'b', 'ip_ka').to_dict())
    assert not validate(value, 'power/shortcircuit-result')
    value['status'] = case['status'] = 'failed'
    for field in ['ikss_ka', 'ith_ka']:
        case['bus_results'][0][field] = None
        case['diagnostics'].append(diagnostic('UNAVAILABLE', 'Calculation failed', 'buses', 'b', field).to_dict())
    assert not validate(value, 'power/shortcircuit-result')
    case['bus_results'][0]['ip_ka'] = 0
    assert validate(value, 'power/shortcircuit-result')


def test_duplicate_cases_buses_and_false_partial_rejected():
    value = result()
    value['case_results'].append(copy.deepcopy(value['case_results'][0]))
    assert any(d.code == 'DUPLICATE_CASE' for d in validate(value, 'power/shortcircuit-result'))
    value = result()
    value['case_results'][0]['bus_results'] *= 2
    assert any(d.code == 'DUPLICATE_ID' for d in validate(value, 'power/shortcircuit-result'))
    value = result()
    value['status'] = 'partial'
    assert any(d.code == 'RESULT_STATUS' for d in validate(value, 'power/shortcircuit-result'))
