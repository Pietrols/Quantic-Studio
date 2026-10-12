"""Local project/study service, confined to one configured project root."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import threading
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict
from qe_core import load_project
from qe_core.multidomain import POWER_IDS
from qe_core.project import safe_path, validate_network
from qe_core.validation import diagnostic
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .runner import Runner, WorkerError


class RunRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    project_path: str
    study_id: str
    solver: str = 'pandapower'


class SaveRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    project_path: str
    model_id: str
    etag: str
    data: dict[str, Any]


class ApiError(Exception):
    def __init__(self, status, diagnostics):
        self.status, self.diagnostics = status, diagnostics


def error(code, message, status=422, kind='project', identifier='request', field='input'):
    return ApiError(status, [diagnostic(code, message, kind, identifier, field).to_dict()])


def create_app(project_root: str | Path, *, runner=None, max_file_bytes=2_000_000,
               max_buses=2000, max_iterations=1000, allowed_origins=None):
    root = Path(project_root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Project root must be a directory')
    engine = runner or Runner()
    save_lock = threading.RLock()
    origins = allowed_origins or ['http://localhost:5173', 'http://127.0.0.1:5173',
                                 'http://127.0.0.1:8765', 'http://localhost:8765']
    app = FastAPI(title='Quantic Studio project API', version='0.1.0')
    app.state.project_root = root
    app.add_middleware(CORSMiddleware, allow_origins=origins,
                       allow_methods=['GET', 'POST'], allow_headers=['Content-Type'])
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=['127.0.0.1', 'localhost'])

    @app.middleware('http')
    async def request_boundary(request: Request, call_next):
        origin = request.headers.get('origin')
        if origin and origin not in origins:
            return JSONResponse({'diagnostics': [diagnostic('ORIGIN_DENIED', 'Browser origin is not allowed',
                                'request', 'http', 'origin').to_dict()]}, status_code=403)
        # Bound the body before Pydantic parses it; ASGI chunked bodies are bounded too.
        if request.method == 'POST':
            body = bytearray()
            async for chunk in request.stream():
                body.extend(chunk)
                if len(body) > max_file_bytes:
                    return JSONResponse({'diagnostics': [diagnostic('INPUT_LIMIT', 'Request body exceeds configured size',
                                        'request', 'http', 'body').to_dict()]}, status_code=413)
            request._body = bytes(body)
        return await call_next(request)

    @app.exception_handler(ApiError)
    async def api_error(request, exc):
        return JSONResponse({'diagnostics': exc.diagnostics}, status_code=exc.status)

    @app.exception_handler(RequestValidationError)
    async def request_error(request, exc):
        return JSONResponse({'diagnostics': [diagnostic('REQUEST_INVALID', e['msg'], 'request', 'http',
                              '.'.join(str(x) for x in e['loc'])).to_dict() for e in exc.errors()]}, status_code=422)

    def folder(name):
        try:
            path = safe_path(root, name)
            if not path.is_dir():
                raise error('PROJECT_NOT_FOUND', 'Project folder does not exist', 404)
            # Trusted local project directory, but prevent accidentally reading enormous files.
            files = list(path.rglob('*.json'))
            manifest = safe_path(path, 'manifest.json')
            if manifest.is_file() and manifest.stat().st_size <= max_file_bytes:
                try:
                    metadata = json.loads(manifest.read_bytes())
                except (ValueError, UnicodeError):
                    metadata = {}
                if isinstance(metadata, dict):
                    names = [metadata.get('network_file')]
                    for collection, field in [('models', 'file'), ('studies', 'request_file')]:
                        entries = metadata.get(collection, [])
                        if isinstance(entries, list):
                            names.extend(e.get(field) for e in entries if isinstance(e, dict))
                    files.extend(safe_path(path, n) for n in names if isinstance(n, str))
            if len(files) > 500 or any(p.is_file() and p.stat().st_size > max_file_bytes for p in files):
                raise error('INPUT_LIMIT', 'Project exceeds configured file count or size', 413)
            return path
        except (OSError, ValueError) as exc:
            raise error('PROJECT_PATH', 'Path must remain inside the configured root', 422) from exc

    def project(name):
        path = folder(name)
        outcome = load_project(path)
        if not outcome.ok:
            raise ApiError(422, [d.to_dict() for d in outcome.diagnostics])
        for model in outcome.value.models:
            if model.model_type == 'power.network' and len(model.data['buses']) > max_buses:
                raise error('INPUT_LIMIT', 'Power model exceeds configured bus count', 413)
        return path, outcome.value, [d.to_dict() for d in outcome.diagnostics]

    def selected_model(value, mid):
        try:
            return value.model(mid)
        except KeyError as exc:
            raise error('UNKNOWN_MODEL', 'Model does not exist', 404, 'model', mid, 'model_id') from exc

    @app.get('/health')
    def health():
        return {'status': 'ok', 'report_formats': ['markdown']}

    @app.get('/api/projects')
    def projects():
        candidates = ['.'] if (root / 'manifest.json').is_file() else []
        candidates += [p.relative_to(root).as_posix() for p in sorted(root.iterdir())
                       if p.is_dir() and (p / 'manifest.json').is_file() and p.resolve().is_relative_to(root)]
        return {'projects': candidates}

    @app.get('/api/project')
    def read_project(project_path: str):
        _, value, notes = project(project_path)
        return {'name': value.name, 'models': [{'model_id': m.model_id, 'model_type': m.model_type, 'file': m.file}
                    for m in value.models], 'studies': [{'study_id': s.study_id, 'study_type': s.study_type,
                    'model_id': s.model_id} for s in value.studies], 'assets': value.assets, 'diagnostics': notes}

    @app.get('/api/model')
    def read_model(project_path: str, model_id: str):
        path, value, notes = project(project_path)
        model = selected_model(value, model_id)
        raw = safe_path(path, model.file).read_bytes()
        if json.loads(raw) != model.data:
            raise error('EDIT_CONFLICT', 'Model changed while opening; reload', 409)
        etag = hashlib.sha256(raw).hexdigest()
        return {'model_id': model.model_id, 'model_type': model.model_type, 'data': model.data,
                'etag': etag, 'diagnostics': notes}

    @app.post('/api/model/save')
    def save_model(body: SaveRequest):
        with save_lock:
            path, value, _ = project(body.project_path)
            model = selected_model(value, body.model_id)
            if model.model_type != 'power.network':
                raise error('UNSUPPORTED_MODEL', 'Editing this model type is not implemented')
            target = safe_path(path, model.file)
            if hashlib.sha256(target.read_bytes()).hexdigest() != body.etag:
                raise error('EDIT_CONFLICT', 'Model changed since it was opened; reload before saving', 409)
            problems = validate_network(body.data)
            for study in value.studies:
                if study.model_id == model.model_id and study.study_type == 'motorstart' and not problems:
                    if study.request['motor']['bus_id'] not in {b['bus_id'] for b in body.data['buses']}:
                        problems.append(diagnostic('UNKNOWN_BUS', 'Motor study still references this bus',
                                                   'motor', study.request['motor']['motor_id'], 'bus_id'))
            for asset in value.assets:
                for ref in asset['representations']:
                    if ref['model_id'] == model.model_id and not problems:
                        items = body.data.get(ref['element_type'], [])
                        if not any(item[POWER_IDS[ref['element_type']]] == ref['element_id'] for item in items):
                            problems.append(diagnostic('UNKNOWN_ELEMENT', 'Asset still references the removed element',
                                                       'asset', asset['asset_id'], 'representations'))
            if problems:
                raise ApiError(422, [d.to_dict() for d in problems])
            content = (json.dumps(body.data, indent=2, allow_nan=False) + '\n').encode()
            if len(content) > max_file_bytes or len(body.data['buses']) > max_buses:
                raise error('INPUT_LIMIT', 'Edited model exceeds configured size', 413)
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as stream:
                    temporary = Path(stream.name)
                    stream.write(content)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary, target)
            except OSError as exc:
                raise error('MODEL_WRITE', 'Model could not be saved', 500) from exc
            finally:
                if temporary:
                    temporary.unlink(missing_ok=True)
            return {'model_id': model.model_id, 'etag': hashlib.sha256(content).hexdigest(), 'diagnostics': []}

    @app.post('/api/studies/run')
    def run_study(body: RunRequest):
        _, value, notes = project(body.project_path)
        matches = [s for s in value.studies if s.study_id == body.study_id]
        if len(matches) != 1:
            raise error('UNKNOWN_STUDY', 'Select one study ID', 404, 'study', body.study_id, 'study_id')
        study = matches[0]
        model = selected_model(value, study.model_id)
        if study.study_type not in ('loadflow', 'shortcircuit', 'motorstart') or model.model_type != 'power.network':
            raise error('UNSUPPORTED_STUDY', 'This stored study has no implemented engine', 422, 'study', study.study_id, 'study_type')
        if body.solver != 'pandapower':
            raise error('UNSUPPORTED_SOLVER', 'API studies currently use pandapower', 422, 'study', study.study_id, 'solver')
        if study.request.get('max_iterations', 0) > max_iterations:
            raise error('INPUT_LIMIT', 'Study exceeds configured iteration limit', 413)
        try:
            response = engine.run({'study_type': study.study_type, 'network': model.data,
                'request': study.request, 'project_name': value.name, 'model_id': model.model_id})
        except WorkerError as exc:
            raise error(exc.code, exc.message, exc.status, 'study', study.study_id, 'execution') from exc
        if response.get('error'):
            raise ApiError(422, response['diagnostics'])
        response['project_diagnostics'] = notes
        return response

    return app
