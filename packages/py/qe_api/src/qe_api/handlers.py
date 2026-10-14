"""Static contract dispatch, never module names from project data."""

from qe_core.plc_contracts import (
    plc_elements,
    validate_plc_events,
    validate_plc_model,
    validate_plc_request,
)
from qe_core.pv_contracts import (
    pv_elements,
    validate_pv_request,
    validate_pv_site,
    validate_pv_weather,
)

from . import plc, pv

# Exact model, study and schema versions are allowlisted.
HANDLERS = {
    ("pv.site", "pv.yield", "0.1.0"): pv.execute,
    ("automation.plc", "plc.scan", "0.1.0"): plc.execute,
}


def handler(model, study):
    if model.data.get("schema_version") != study.request.get("schema_version"):
        return None
    return HANDLERS.get(
        (model.model_type, study.study_type, model.data.get("schema_version"))
    )


def validate_model(model_type, data):
    return {"pv.site": validate_pv_site, "automation.plc": validate_plc_model}[
        model_type
    ](data)


def elements(model_type, data):
    return {"pv.site": pv_elements, "automation.plc": plc_elements}[model_type](data)


def validate_context(model_type, context):
    model, request, series = (context[k] for k in ("model", "request", "series"))
    if model_type == "pv.site":
        return [
            *validate_pv_request(request, site=model),
            *validate_pv_weather(series, request=request, site=model),
        ]
    return [
        *validate_plc_request(request, model=model),
        *validate_plc_events(series, request=request),
    ]
