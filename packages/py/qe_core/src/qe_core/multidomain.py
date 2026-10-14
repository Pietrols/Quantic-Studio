"""Engine-free project binding and physical asset identity validation."""
from __future__ import annotations

import json
from pathlib import Path

from .project import Model, Project, Study, read_json, safe_path, validate_network
from .validation import Diagnostic, Outcome, diagnostic, validate

POWER_STUDIES = {'loadflow', 'shortcircuit', 'motorstart'}
# CC-6 validates a PLC payload that declares a CC-6 version. Any other declared version
# (for example the CC-3 placeholder) stays stored, unvalidated and not executable, with an
# info note, so foreign and future files are preserved byte for byte.
PLC_VERSIONS = ('0.1.0',)


def _plc_version(data):
    return data.get('schema_version') in PLC_VERSIONS
POWER_IDS = {'buses': 'bus_id', 'lines': 'line_id', 'transformers': 'transformer_id',
             'loads': 'load_id', 'generators': 'generator_id', 'external_grids': 'external_grid_id',
             'shunts': 'shunt_id'}


def load_models(root: Path, manifest: dict) -> Outcome[Project]:
    errors, notes, files = [], [], [root / 'manifest.json']
    models, paths, studies = {}, {}, []
    identifiers = set()

    def read(name, kind, identifier, field):
        try:
            path = safe_path(root, name)
        except ValueError as exc:
            errors.append(diagnostic('PROJECT_PATH', str(exc), kind, identifier, field))
            return None, None
        outcome = read_json(path)
        errors.extend(outcome.diagnostics)
        if outcome.diagnostics:
            return None, path
        value = outcome.value
        if not isinstance(value, dict):
            errors.append(diagnostic('MODEL_OBJECT', 'Project payload must be a JSON object', kind, identifier, field))
            return None, path
        try:
            json.dumps(value, allow_nan=False)
        except ValueError:
            errors.append(diagnostic('NONFINITE', 'Payload numbers must be finite', kind, identifier, field))
            return None, path
        files.append(path)
        return value, path

    for entry in manifest['models']:
        mid = entry['model_id']
        if mid in identifiers:
            errors.append(diagnostic('DUPLICATE_ID', 'Model ID must be unique', 'model', mid, 'model_id'))
            continue
        identifiers.add(mid)
        data, path = read(entry['file'], 'model', mid, 'file')
        if data is None:
            continue
        if path in paths.values() or path == (root / 'manifest.json').resolve():
            errors.append(diagnostic('MODEL_FILE_ALIAS', 'Each model needs a distinct payload file', 'model', mid, 'file'))
            continue
        if entry['model_type'] == 'power.network':
            problems = validate_network(data)
            errors.extend(problems)
            if problems:
                continue
        elif entry['model_type'] == 'pv.site':
            from .pv_contracts import validate_pv_site

            problems = validate_pv_site(data)
            errors.extend(problems)
            if problems:
                continue
        elif entry['model_type'] == 'automation.plc' and _plc_version(data):
            from .plc_contracts import validate_plc_model

            problems = validate_plc_model(data)
            errors.extend(problems)
            if problems:
                continue
        else:
            notes.append(Diagnostic('DEFERRED_MODEL_VALIDATION',
                f"Stored {entry['model_type']} payload has no implemented domain validator or engine",
                {'element_type': 'model', 'element_id': mid, 'field': 'model_type'}, 'info'))
        models[mid] = Model(mid, entry['model_type'], entry['file'], data)
        paths[mid] = path

    identifiers = set()
    for entry in manifest['studies']:
        sid, mid, kind = entry['study_id'], entry['model_id'], entry['study_type']
        if sid in identifiers:
            errors.append(diagnostic('DUPLICATE_ID', 'Study ID must be unique', 'study', sid, 'study_id'))
            continue
        identifiers.add(sid)
        if mid not in models:
            errors.append(diagnostic('UNKNOWN_MODEL', 'Study model is missing or invalid', 'study', sid, 'model_id'))
            continue
        data, path = read(entry['request_file'], 'study', sid, 'request_file')
        if data is None:
            continue
        if path in paths.values() or path == (root / 'manifest.json').resolve():
            errors.append(diagnostic('REQUEST_FILE_ALIAS', 'Request must be separate from model/manifest files',
                                     'study', sid, 'request_file'))
            continue
        model = models[mid]
        if kind in POWER_STUDIES:
            if model.model_type != 'power.network':
                errors.append(diagnostic('STUDY_MODEL_TYPE', 'Power study must bind to power.network', 'study', sid, 'model_id'))
                continue
            problems = validate(data, f'power/{kind}-request')
            errors.extend(problems)
            if problems:
                continue
            try:
                if safe_path(root, data['network_file']) != paths[mid]:
                    errors.append(diagnostic('NETWORK_MISMATCH', 'Request must name its bound model file',
                                             'study', sid, 'network_file'))
            except ValueError as exc:
                errors.append(diagnostic('PROJECT_PATH', str(exc), 'study', sid, 'network_file'))
            if kind == 'motorstart' and data['motor']['bus_id'] not in {b['bus_id'] for b in model.data['buses']}:
                errors.append(diagnostic('UNKNOWN_BUS', 'Motor bus does not exist in bound network',
                                         'motor', data['motor']['motor_id'], 'bus_id'))
        elif kind == 'pv.yield':
            from .pv_contracts import validate_pv_request, validate_pv_weather

            if model.model_type != 'pv.site':
                errors.append(diagnostic('STUDY_MODEL_TYPE', 'PV study must bind to pv.site',
                                         'study', sid, 'model_id'))
                continue
            problems = validate_pv_request(data, site=model.data)
            errors.extend(problems)
            if problems:
                continue
            run = data['execution']
            if run['study_id'] != sid or run['model_id'] != mid:
                errors.append(diagnostic('PV_BINDING', 'Request must identify its bound study and model',
                                         'study', sid, 'execution'))
            try:
                if safe_path(root, data['model_file']) != paths[mid]:
                    errors.append(diagnostic('PV_BINDING', 'Request must name its bound model file',
                                             'study', sid, 'model_file'))
            except ValueError as exc:
                errors.append(diagnostic('PROJECT_PATH', str(exc), 'study', sid, 'model_file'))
            weather_name = run['input_series_file']
            weather, weather_path = read(weather_name, 'study', sid, 'execution.input_series_file')
            request_paths = {path, (root / 'manifest.json').resolve()}
            for other in manifest['studies']:
                try:
                    request_paths.add(safe_path(root, other['request_file']))
                except ValueError:
                    pass  # The regular study loop reports the unsafe request path.
            if weather_path in paths.values() or weather_path in request_paths:
                errors.append(diagnostic('PV_FILE_ALIAS', 'Weather must be separate from model/request/manifest',
                                         'study', sid, 'execution.input_series_file'))
            elif weather is not None:
                errors.extend(validate_pv_weather(weather, request=data, site=model.data,
                                                  raw_bytes=weather_path.read_bytes()))
        elif kind == 'plc.scan' and _plc_version(data):
            from .plc_contracts import validate_plc_events, validate_plc_request

            if model.model_type != 'automation.plc' or not _plc_version(model.data):
                errors.append(diagnostic('STUDY_MODEL_TYPE', 'PLC scan must bind to a CC-6 automation.plc model',
                                         'study', sid, 'model_id'))
                continue
            problems = validate_plc_request(data, model=model.data)
            errors.extend(problems)
            if problems:
                continue
            run = data['execution']
            if run['study_id'] != sid or run['model_id'] != mid:
                errors.append(diagnostic('PLC_BINDING', 'Request must identify its bound study and model',
                                         'study', sid, 'execution'))
            try:
                if safe_path(root, data['model_file']) != paths[mid]:
                    errors.append(diagnostic('PLC_BINDING', 'Request must name its bound model file',
                                             'study', sid, 'model_file'))
            except ValueError as exc:
                errors.append(diagnostic('PROJECT_PATH', str(exc), 'study', sid, 'model_file'))
            events, events_path = read(run['input_series_file'], 'study', sid, 'execution.input_series_file')
            taken = {path, (root / 'manifest.json').resolve(), *paths.values()}
            for other in manifest['studies']:
                try:
                    taken.add(safe_path(root, other['request_file']))
                except ValueError:
                    pass  # The regular study loop reports the unsafe request path.
            if events_path in taken:
                errors.append(diagnostic('PLC_FILE_ALIAS', 'Events must be separate from model/request/manifest',
                                         'study', sid, 'execution.input_series_file'))
            elif events is not None:
                errors.extend(validate_plc_events(events, request=data, raw_bytes=events_path.read_bytes()))
        else:
            notes.append(Diagnostic('DEFERRED_STUDY_VALIDATION',
                f'Stored study type {kind} has no implemented request validator or execution support',
                {'element_type': 'study', 'element_id': sid, 'field': 'study_type'}, 'info'))
        studies.append(Study(sid, kind, data, mid))

    asset_ids, representations = set(), set()
    assets = manifest['asset_registry']['assets']
    for asset in assets:
        aid = asset['asset_id']
        if aid in asset_ids:
            errors.append(diagnostic('DUPLICATE_ID', 'Asset ID must be unique', 'asset', aid, 'asset_id'))
        asset_ids.add(aid)
        for ref in asset['representations']:
            key = (ref['model_id'], ref['element_type'], ref['element_id'])
            if key in representations:
                errors.append(diagnostic('DUPLICATE_REPRESENTATION', 'Representation already belongs to an asset',
                                         'asset', aid, 'representations'))
            representations.add(key)
            model = models.get(ref['model_id'])
            if model is None:
                errors.append(diagnostic('UNKNOWN_MODEL', 'Asset representation model is missing or invalid',
                                         'asset', aid, 'representations.model_id'))
            elif model.model_type == 'power.network':
                id_field = POWER_IDS.get(ref['element_type'])
                if id_field is None or ref['element_id'] not in {e[id_field] for e in model.data[ref['element_type']]}:
                    errors.append(diagnostic('UNKNOWN_ELEMENT', 'Asset representation does not name a power element',
                                             'asset', aid, 'representations.element_id'))
            elif model.model_type == 'pv.site':
                from .pv_contracts import pv_elements

                if ref['element_id'] not in pv_elements(model.data).get(ref['element_type'], set()):
                    errors.append(diagnostic('UNKNOWN_ELEMENT', 'Asset representation must name a PV element',
                                             'asset', aid, 'representations.element_id'))
            elif model.model_type == 'automation.plc' and _plc_version(model.data):
                from .plc_contracts import plc_elements

                if ref['element_id'] not in plc_elements(model.data).get(ref['element_type'], set()):
                    errors.append(diagnostic('UNKNOWN_ELEMENT', 'Asset representation must name a PLC element',
                                             'asset', aid, 'representations.element_id'))
            else:
                notes.append(Diagnostic('DEFERRED_ASSET_VALIDATION',
                    'Model binding checked; element reference requires its future domain contract',
                    {'element_type': 'asset', 'element_id': aid, 'field': 'representations'}, 'info'))
    if errors:
        return Outcome(diagnostics=[*errors, *notes])
    return Outcome(Project(manifest['name'], tuple(models.values()), tuple(studies),
                           tuple(dict.fromkeys(files)), tuple(assets)), notes)
