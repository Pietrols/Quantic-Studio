# Quantic Studio local API

```sh
uv sync --all-packages --locked
uv run qe-api --project-root examples
```

The command binds 127.0.0.1:8765. Interactive request documentation is at /docs.
The configured root contains project folders, or can itself be a project.
Paths in requests are relative to that root. Core validates legacy and multi-domain
manifests; every study ID selects its bound model, never the first network.

| Method and path | Input | Response |
|---|---|---|
| GET /health | none | status and supported report formats |
| GET /api/projects | none | immediate project directory names |
| GET /api/project | project_path query | models, study bindings, assets, diagnostics |
| GET /api/model | project_path, model_id query | payload, SHA-256 etag, diagnostics |
| POST /api/model/save | project_path, model_id, etag, data | new etag or validation/conflict diagnostics |
| POST /api/studies/run | project_path, study_id, solver (optional) | result contract, model_id, Markdown report, project diagnostics |

Example study body:

```json
{"project_path":"multi_domain","study_id":"motor-start","solver":"pandapower"}
```

Studies do not modify input files or write an out directory. Each worker receives
a validated in-memory snapshot and calls the existing solver entry point. Result
coverage and network identity are checked before rendering. Numerical failure,
partial fault duties or a failed dip limit still return HTTP 200 with their
explicit result status/diagnostics. HTTP success does not mean engineering pass.
Invalid inputs/unsupported studies use 422, missing selections 404, stale edits
409, resource limits 413, busy workers 429, timeout 504 and worker failure 500.
Errors contain a diagnostics array, with element/field references.

Saves accept only power networks, run core validation and preserve asset and
motor-study references. They replace only the selected model file atomically.
The etag prevents one API client overwriting another client's newer save. A save
lock protects a single service process; this is not a multi-process transaction
or protection against a trusted user's simultaneous filesystem edits. Loading
and editing future-domain models are deliberately separate capabilities.

Default operational limits: 30 seconds per worker (configurable --timeout), two
concurrent workers, 2 MB per JSON file/request body, 500 JSON files per project,
2000 buses per power model and 1000 load-flow iterations. These are configurable
service resource policies, not engineering criteria. A timed-out worker is killed
and its slot released; no abandoned calculation runs in a background thread.

## Trust boundary

This is a local desktop/development service for trusted project files. The default
CLI has no public bind option, enables no authentication and makes no claim of
multi-user isolation. Trusted hosts are localhost/127.0.0.1; browser origins are
limited to local ports 5173 and 8765. Other origins are rejected, including writes.
Paths and symlinks must remain within the configured root. Use one API process
for edits. A public deployment needs authentication, authorization, TLS, request
quotas, a reviewed filesystem boundary and coordinated write locking before
changing the binding/origin policy. That deployment is outside WP-1.5.

The editor uses these model routes; its presentation layout remains browser-local
and separate from the engineering payload. PDF export is added by WP-1.7.
