"""Two steady operating points with one initially disconnected, locked-rotor motor."""
from __future__ import annotations

import copy
import json
import math
from pathlib import Path

from qe_core import Diagnostic, Outcome, validate
from qe_core.project import validate_network
from qe_core.provenance import hash_inputs, provenance
from qe_core.validation import diagnostic

from . import solver as loadflow


class MotorstartInputError(ValueError):
    def __init__(self, diagnostics):
        self.diagnostics = diagnostics
        super().__init__('; '.join(f'{d.code} {d.element_ref}: {d.message}' for d in diagnostics))


def _motor_shunt(motor, bus_kv):
    # Original derivation: docs/learning/motor-start-voltage-dip.md.
    # I_rated=P_shaft/(sqrt(3)*U*eta*pf); Z=U/(sqrt(3)*I_locked).
    rated_ka = motor['shaft_rated_kw'] / 1000 / (
        math.sqrt(3) * motor['rated_voltage_kv'] * motor['efficiency'] * motor['rated_power_factor'])
    z_abs = motor['rated_voltage_kv'] / (math.sqrt(3) * rated_ka * motor['locked_rotor_current_ratio'])
    pf = motor['locked_rotor_power_factor']
    impedance = z_abs * complex(pf, math.sqrt(1 - pf * pf))
    # pandapower v3.5.6 elements/shunt.html: nominal P/Q consumption scales as V^2.
    # S_nominal=U_bus^2/conj(Z), with kV^2/ohm giving MVA. Bus and motor bases may differ.
    power = bus_kv**2 / impedance.conjugate()
    if not all(math.isfinite(v) for v in (rated_ka, z_abs, power.real, power.imag)) or power.real <= 0:
        raise ValueError('Nameplate conversion is outside finite numerical range')
    return power


def solve_motorstart(network, request) -> Outcome[dict]:
    errors = validate_network(network) + validate(request, 'power/motorstart-request')
    if errors:
        return Outcome(diagnostics=errors)
    motor = request['motor']
    buses = {b['bus_id']: b for b in network['buses']}
    if motor['bus_id'] not in buses:
        return Outcome(diagnostics=[diagnostic('UNKNOWN_BUS', 'Motor bus does not exist',
                                              'motor', motor['motor_id'], 'bus_id')])
    notes = []
    lf_request = {key: request[key] for key in ('request_id', 'network_file', 'tolerance_mva', 'max_iterations')}
    lf_request['schema_version'] = '0.1.0'

    def stage(data, label):
        outcome = loadflow.solve(data, lf_request)
        for note in outcome.diagnostics:
            ref = note.element_ref
            if ref and ref.get('element_id') == shunt_id and ref.get('element_type') == 'shunts':
                ref = {'element_type': 'motor', 'element_id': motor['motor_id'], 'field': 'locked_rotor_current_ratio'}
            notes.append(Diagnostic(note.code, f'{label}: {note.message}', ref, note.severity))
        if outcome.value is None or not outcome.value['convergence']['converged']:
            return {}
        return {row['bus_id']: row['vm_pu'] for row in outcome.value['bus_results']}

    shunt_id = '__motorstart__' + motor['motor_id']
    existing = {s['shunt_id'] for s in network['shunts']}
    while shunt_id in existing:
        shunt_id += '_'
    pre = stage(network, 'Pre-start')
    starting = {}
    if pre:
        try:
            power = _motor_shunt(motor, buses[motor['bus_id']]['vn_kv'])
            connected = copy.deepcopy(network)
            connected['shunts'].append({'shunt_id': shunt_id, 'bus_id': motor['bus_id'],
                                        'p_mw': power.real, 'q_mvar': power.imag})
            starting = stage(connected, 'Locked rotor')
        except (ArithmeticError, ValueError) as exc:
            notes.append(diagnostic('MOTOR_NUMERICAL_RANGE', str(exc), 'motor',
                                    motor['motor_id'], 'nameplate'))
    rows = []
    for bus in buses:
        before, during = pre.get(bus), starting.get(bus)
        before = before if before is not None and math.isfinite(before) and before > 0 else None
        during = during if during is not None and math.isfinite(during) and during >= 0 else None
        dip = 100 * (before - during) / before if before is not None and during is not None else None
        if dip is not None and not math.isfinite(dip):
            during, dip = None, None
        row = {'bus_id': bus, 'prestart_vm_pu': before, 'locked_rotor_vm_pu': during,
               'dip_percent': dip, 'passes_limit': dip <= request['dip_limit_percent'] if dip is not None else None}
        for field, value in row.items():
            if value is None:
                notes.append(diagnostic('UNAVAILABLE', 'No verified voltage pair; see stage diagnostics',
                                        'buses', bus, field))
        if row['passes_limit'] is False:
            notes.append(Diagnostic('DIP_LIMIT_EXCEEDED',
                f"Dip {dip:.12g}% exceeds selected limit {request['dip_limit_percent']:g}%",
                {'element_type': 'buses', 'element_id': bus, 'field': 'dip_percent'}, 'warning'))
        rows.append(row)
    success = all(row['dip_percent'] is not None for row in rows)
    result = {'schema_version': '0.3.0', 'result_id': request['request_id'] + '-pandapower',
              'network_id': network['network_id'], 'motor': copy.deepcopy(motor),
              'dip_limit_percent': request['dip_limit_percent'],
              'dip_definition': '100*(prestart_vm_pu-locked_rotor_vm_pu)/prestart_vm_pu',
              'status': 'success' if success else 'failed',
              'passes_limit': all(row['passes_limit'] for row in rows) if success else None,
              'bus_results': rows, 'diagnostics': [d.to_dict() for d in notes],
              'assumptions': [
                  'Balanced steady locked-rotor snapshot, not acceleration, torque, thermal or run-up verification.',
                  'One initially disconnected motor is added; it must not also appear as a pre-existing load.',
                  'Lagging locked-rotor constant impedance; all other loads and generator Q limits are retained.',
                  'External grids impose ideal voltage; source impedance must be explicit network branches. Fault-level fields are not used.',
                  'Voltage magnitudes use each bus nominal kV base; signed relative dip can be negative for a rise.',
                  'Dip limit is selected by the user, not supplied by a standard. Equality passes.',
              ], 'provenance': provenance('pandapower', loadflow.pp.__version__,
                                          hash_inputs({'network': network, 'request': request}))}
    problems = validate(result, 'power/motorstart-result')
    return Outcome(diagnostics=problems) if problems else Outcome(result, notes)


def run_motorstart_file(network_path: str | Path, request: dict) -> dict:
    path = Path(network_path)
    try:
        network = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError, UnicodeError) as exc:
        raise MotorstartInputError([diagnostic('INPUT_READ', str(exc), 'file', path.name, 'content')]) from exc
    outcome = solve_motorstart(network, request)
    if outcome.value is None:
        raise MotorstartInputError(outcome.diagnostics)
    return outcome.value
