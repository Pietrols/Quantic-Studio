import copy
import json
import math
from pathlib import Path

import pytest
from qe_core import validate
from qe_power.adapters.pandapower import solve_motorstart

ROOT = Path(__file__).resolve().parents[5]


def inputs():
    folder = ROOT / 'examples/motorstart'
    return (json.loads((folder / 'network.json').read_text()),
            json.loads((folder / 'motorstart-request.json').read_text()))


def checked(network, request):
    outcome = solve_motorstart(network, request)
    assert outcome.value is not None, outcome.diagnostics
    assert not validate(outcome.value, 'power/motorstart-result')
    return outcome.value


@pytest.mark.parametrize('base_mva,motor_kv,source_vm,pf', [
    (1, .4, 1, .3), (100, .4, 1, .3), (1, .38, 1.04, .25), (1, .4, 1, 1),
])
def test_independent_complex_voltage_divider(base_mva, motor_kv, source_vm, pf):
    # Original authored reference: motorstart-authored-reference.yaml.
    # No adapter helper or engine output participates in expected values.
    network, request = inputs()
    network['base_mva'] = base_mva
    network['external_grids'][0]['vm_setpoint_pu'] = source_vm
    motor = request['motor']
    motor['rated_voltage_kv'] = motor_kv
    motor['locked_rotor_power_factor'] = pf
    # Three-phase apparent locked-rotor VA from shaft W / eta / rated PF * ratio.
    apparent_va = 30000 / .9 / .85 * 6
    z_modulus = (motor_kv * 1000)**2 / apparent_va
    z_motor = complex(z_modulus * pf, z_modulus * math.sqrt(1-pf**2))
    expected = abs(source_vm * z_motor / (complex(.02, .03) + z_motor))
    before = copy.deepcopy((network, request))
    result = checked(network, request)
    assert (network, request) == before
    assert result['status'] == 'success'
    source, bus = result['bus_results']
    assert source['locked_rotor_vm_pu'] == pytest.approx(source_vm, abs=1e-10)
    assert bus['prestart_vm_pu'] == pytest.approx(source_vm, abs=1e-10)
    assert bus['locked_rotor_vm_pu'] == pytest.approx(expected, abs=1e-9)
    assert bus['dip_percent'] == pytest.approx(100*(source_vm-expected)/source_vm, abs=1e-7)


def test_existing_admittance_retained_independent_reference():
    network, request = inputs()
    network['shunts'] = [dict(shunt_id='__motorstart__motor-1', bus_id='motor_bus', p_mw=.02, q_mvar=.01)]
    z_line = complex(.02, .03)
    y_existing = complex(.02, -.01) / .4**2
    z_motor = .4**2 / (.03/.9/.85*6) * complex(.3, math.sqrt(1-.3**2))
    pre = abs(1 / (1+z_line*y_existing))
    start = abs(1 / (1+z_line*(y_existing+1/z_motor)))
    row = checked(network, request)['bus_results'][1]
    assert row['prestart_vm_pu'] == pytest.approx(pre, abs=1e-9)
    assert row['locked_rotor_vm_pu'] == pytest.approx(start, abs=1e-9)
    assert row['dip_percent'] == pytest.approx(100*(pre-start)/pre, abs=1e-7)


def test_limit_failure_has_success_status_and_changes_hash():
    network, request = inputs()
    good = checked(network, request)
    request['dip_limit_percent'] = 1
    bad = checked(network, request)
    assert bad['status'] == 'success' and bad['passes_limit'] is False
    assert bad['bus_results'][1]['passes_limit'] is False
    assert any(d['code'] == 'DIP_LIMIT_EXCEEDED' for d in bad['diagnostics'])
    assert good['provenance']['input_hash_sha256'] != bad['provenance']['input_hash_sha256']


@pytest.mark.parametrize('kind', ['iterations', 'island', 'zero_impedance', 'range'])
def test_unavailable_outputs(kind):
    network, request = inputs()
    if kind == 'iterations':
        request['max_iterations'] = 1
    elif kind == 'island':
        network['lines'] = []
    elif kind == 'zero_impedance':
        network['lines'][0].update(r_ohm_per_km=0, x_ohm_per_km=0)
    else:
        request['motor']['efficiency'] = 1e-320
    result = checked(network, request)
    assert result['status'] == 'failed'
    assert result['passes_limit'] is None
    assert all(row['dip_percent'] is None and row['passes_limit'] is None for row in result['bus_results'])
    if kind in ('iterations', 'range'):
        assert result['bus_results'][1]['prestart_vm_pu'] == pytest.approx(1)


@pytest.mark.parametrize('field,value', [('efficiency', 0), ('rated_power_factor', 1.1),
    ('shaft_rated_kw', -1), ('locked_rotor_power_factor', None), ('rated_voltage_kv', float('nan')),
    ('locked_rotor_current_ratio', 0), ('bus_id', 'missing')])
def test_invalid_motor_diagnostics(field, value):
    network, request = inputs()
    request['motor'][field] = value
    result = solve_motorstart(network, request)
    assert result.value is None
    assert any(d.element_ref['element_id'] == 'motor-1' and field in d.element_ref['field']
               for d in result.diagnostics)


def test_generator_limits_and_existing_load_are_retained():
    network, request = inputs()
    network['loads'] = [dict(load_id='other', bus_id='motor_bus', p_mw=.01, q_mvar=.005)]
    network['buses'][1]['bus_type'] = 'pv'
    network['generators'] = [dict(generator_id='g', bus_id='motor_bus', p_mw=.001,
        vm_setpoint_pu=1, q_min_mvar=0, q_max_mvar=.001)]
    result = checked(network, request)
    assert result['status'] == 'success'
    notes = [d for d in result['diagnostics'] if d['code'] == 'GENERATOR_Q_LIMIT']
    assert any(d['message'].startswith('Pre-start:') for d in notes)
    assert any(d['message'].startswith('Locked rotor:') for d in notes)
    assert result['bus_results'][1]['prestart_vm_pu'] < 1
