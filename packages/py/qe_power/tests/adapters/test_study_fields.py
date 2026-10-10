import copy
import json
from pathlib import Path

import pytest
from qe_power.adapters.pandapower import solve
from test_pandapower import request


@pytest.mark.parametrize('subproject', ['', 'transformer'])
def test_fault_fields_do_not_change_loadflow(subproject):
    root = Path(__file__).resolve().parents[5]
    network = json.loads((root / 'examples/shortcircuit' / subproject / 'network.json').read_text())
    baseline = copy.deepcopy(network)
    baseline['schema_version'] = '0.1.0'
    for field in ['s_sc_max_mva', 's_sc_min_mva', 'rx_max', 'rx_min']:
        baseline['external_grids'][0].pop(field)
    for line in baseline['lines']:
        line.pop('end_temperature_celsius', None)
    old, new = solve(baseline, request()), solve(network, request())
    assert old.ok and new.ok
    assert [b['vm_pu'] for b in old.value['bus_results']] == pytest.approx(
        [b['vm_pu'] for b in new.value['bus_results']], abs=1e-12)
    notes = [d for d in new.diagnostics if d.code == 'STUDY_ONLY_FIELD']
    expected = {'s_sc_max_mva', 's_sc_min_mva', 'rx_max', 'rx_min'}
    if network['lines']:
        expected.add('end_temperature_celsius')
    assert {d.element_ref['field'] for d in notes} == expected
    assert all(d.severity == 'info' for d in notes)
