"""Readable motor-start result, separating calculation and compliance."""
from .loadflow import _fmt, _table
from .shortcircuit import _diagnostics


def _compliance(value):
    return 'UNKNOWN' if value is None else 'PASS' if value else 'FAIL'


def render_motorstart_report(*, project_name, network, request, result):
    out = [f'# Motor-start study: {project_name}', '',
           f"Calculation: **{result['status'].upper()}**. Dip limit: **{_compliance(result['passes_limit'])}**.", '',
           f"User-selected dip limit: {result['dip_limit_percent']:g}% (equality passes).", '',
           'Dip (%) = 100 * (pre-start voltage - locked-rotor voltage) / pre-start voltage. '
           'Voltage rise is negative dip. Voltages use each bus nominal line-to-line kV base. '
           'Unavailable values are n/a and compliance is UNKNOWN.', '',
           '## Motor inputs', '']
    labels = {'motor_id': 'Motor ID', 'bus_id': 'Bus ID', 'shaft_rated_kw': 'Shaft rating (kW)',
              'efficiency': 'Efficiency (fraction)', 'rated_power_factor': 'Rated power factor (lagging)',
              'rated_voltage_kv': 'Rated line-to-line voltage (kV)',
              'locked_rotor_current_ratio': 'Locked-rotor / rated current',
              'locked_rotor_power_factor': 'Locked-rotor power factor (lagging)'}
    out += _table(['Input', 'Value'], [[labels[k], str(v)] for k, v in result['motor'].items()])
    out += ['', '## Bus voltage and compliance', '']
    nominal = {b['bus_id']: b['vn_kv'] for b in network['buses']}
    out += _table(['Bus', 'Nominal kV', 'Pre-start (pu)', 'Locked rotor (pu)', 'Dip (%)', 'Limit'], [
        [r['bus_id'], _fmt(nominal[r['bus_id']], 3), _fmt(r['prestart_vm_pu'], 8),
         _fmt(r['locked_rotor_vm_pu'], 8), _fmt(r['dip_percent'], 6), _compliance(r['passes_limit'])]
        for r in result['bus_results']])
    out += ['', '## Assumptions', '', *[f'- {a}' for a in result['assumptions']], '',
            '## Diagnostics', '', *_diagnostics(result['diagnostics']), '', '## Provenance', '']
    out += _table(['Item', 'Value'], [[k, str(v)] for k, v in result['provenance'].items()])
    out += ['', f"Request: {request['request_id']}. Result: {result['result_id']}.",
            'The SHA-256 covers canonical network and complete request, including motor inputs and dip limit.', '']
    return '\n'.join(out)
