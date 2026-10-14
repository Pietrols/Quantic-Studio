"""CC-5 engine-free PV bindings and energy accounting, never equipment defaults.

References: Gilman, NREL/TP-6A20-64102 (2015), pp. 18-19, 56;
pvlib 0.16.1 pvwatts_dc, inverter.pvwatts and temperature.ross parameter docs.
"""

from __future__ import annotations

import hashlib
import math
import re
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from .time_series import (
    _safe_semantics,
    units_compatible,
    validate_time_series,
    validate_time_stepped_request,
    validate_time_stepped_result,
)
from .validation import diagnostic, validate


def problem(code, field, message):
    return diagnostic(code, message, "pv", "pv", field)


def _local(path):
    return bool(path) and not (
        path.startswith("/") or "\\" in path or ":" in path or ".." in path.split("/")
    )


def pv_elements(site):
    return {
        "site": {site["site_id"]},
        **{
            kind: {v[key] for v in site[kind]}
            for kind, key in [
                ("arrays", "array_id"),
                ("modules", "module_id"),
                ("inverters", "inverter_id"),
            ]
        },
    }


@_safe_semantics
def validate_pv_site(value):
    errors = validate(value, "pv/site")
    if errors:
        return errors
    ids = []
    for kind, key in [
        ("arrays", "array_id"),
        ("modules", "module_id"),
        ("inverters", "inverter_id"),
        ("losses", "loss_id"),
    ]:
        group = [row[key] for row in value[kind]]
        ids.extend(group)
        if len(group) != len(set(group)):
            errors.append(
                problem(
                    "DUPLICATE_ID", kind, "IDs must be unique within their collection"
                )
            )
    # Dots delimit output signal IDs; do not permit ambiguous asset names.
    if any("." in item for item in [value["site_id"], *ids]):
        errors.append(
            problem(
                "PV_ID",
                "id",
                "PV IDs cannot contain the output namespace delimiter dot",
            )
        )
    elements = pv_elements(value)
    used = set()
    for row in value["arrays"]:
        for kind, field in [("modules", "module_id"), ("inverters", "inverter_id")]:
            if row[field] not in elements[kind]:
                errors.append(
                    problem(
                        "UNKNOWN_ELEMENT",
                        f"arrays.{row['array_id']}.{field}",
                        "Array must reference declared equipment",
                    )
                )
        if row["inverter_id"] in used:
            errors.append(
                problem(
                    "PV_TOPOLOGY",
                    "arrays.inverter_id",
                    "CC-5 fixed-tilt subset assigns one inverter to each array",
                )
            )
        used.add(row["inverter_id"])
    for row in value["inverters"]:
        # PVWatts pdc0 = pac0 / eta_nom, not the module reference rating.
        if not math.isclose(
            row["dc_input_limit_w"] * row["nominal_efficiency"],
            row["ac_rating_w"],
            rel_tol=1e-12,
            abs_tol=0,
        ):
            errors.append(
                problem(
                    "PV_RATING",
                    f"inverters.{row['inverter_id']}.ac_rating_w",
                    "PVWatts AC rating must equal DC input limit times nominal efficiency",
                )
            )
    return errors


def pv_output_units(site):
    """Frozen output IDs, units and per-array named loss trace; no solver call."""
    result = {"site.ac_power_w": "W"}
    for row in site["arrays"]:
        prefix = row["array_id"] + "."
        result.update(
            {
                prefix + key: unit
                for key, unit in {
                    "sun_zenith_deg": "degree",
                    "sun_azimuth_deg": "degree",
                    "poa_beam_w_m2": "W/m^2",
                    "poa_sky_w_m2": "W/m^2",
                    "poa_ground_w_m2": "W/m^2",
                    "poa_global_w_m2": "W/m^2",
                    "poa_effective_w_m2": "W/m^2",
                    "cell_temperature_c": "degC",
                    "dc_gross_w": "W",
                    "dc_net_w": "W",
                    "ac_gross_w": "W",
                    "ac_net_w": "W",
                    "inverter_loss_w": "W",
                }.items()
            }
        )
        for loss in site["losses"]:
            result[prefix + "loss." + loss["loss_id"]] = (
                "W/m^2" if loss["stage"] == "irradiance" else "W"
            )
    return result


@_safe_semantics
def validate_pv_request(value, *, site=None):
    errors = validate(value, "pv/yield-request")
    if errors:
        return errors
    run = value["execution"]
    errors.extend(validate_time_stepped_request(run))
    if not _local(value["model_file"]):
        errors.append(
            problem(
                "PROJECT_PATH", "model_file", "Use a confined project-relative path"
            )
        )
    if run["time_axis"]["kind"] != "utc" or run["clock"] != "fixed_s":
        errors.append(
            problem(
                "PV_TIME", "execution.time_axis", "PV requires UTC and fixed seconds"
            )
        )
    for field in ("start_time_s", "stop_time_s", "step_size_s"):
        microseconds = Decimal(str(run[field])) * 1000000
        if microseconds != microseconds.to_integral_value():
            errors.append(
                problem(
                    "PV_TIME",
                    "execution." + field,
                    "PV UTC grid must be representable exactly in microseconds",
                )
            )
    if len(set(value["weather"]["channels"].values())) != 4:
        errors.append(
            problem(
                "PV_CHANNEL",
                "weather.channels",
                "Each weather quantity needs its own channel",
            )
        )
    if site is not None:
        site_errors = validate_pv_site(site)
        if site_errors:
            return [*errors, *site_errors]
        expected = pv_output_units(site)
        input_units = {
            sid: "degC" if quantity == "temperature" else "W/m^2"
            for quantity, sid in value["weather"]["channels"].items()
        }
        if set(expected) & set(input_units):
            errors.append(
                problem(
                    "PV_CHANNEL",
                    "weather.channels",
                    "Weather IDs cannot collide with PV output IDs",
                )
            )
        expected.update(input_units)
        actual = {s["signal_id"]: s for s in run["signals"]}
        if set(actual) != set(expected) or any(
            s["unit"] != expected.get(key)
            or s["data_type"] != "real"
            or s["causality"] != ("input" if key in input_units else "output")
            for key, s in actual.items()
        ):
            errors.append(
                problem(
                    "PV_OUTPUTS",
                    "execution.signals",
                    "Declare CC-5 real weather input and output IDs with canonical units and causality",
                )
            )
        modules = {m["module_id"]: m for m in site["modules"]}
        required = {
            "air"
            if modules[a["module_id"]]["temperature"]["model"] == "ross"
            else "cell"
            for a in site["arrays"]
        }
        if required != {value["weather"]["temperature_kind"]}:
            errors.append(
                problem(
                    "PV_TEMPERATURE",
                    "weather.temperature_kind",
                    "Weather temperature must serve every selected array temperature model",
                )
            )
    return errors


def _utc(text):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z", text):
        raise ValueError(
            "PV timestamps require UTC Z and at most microsecond precision"
        )
    time = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if not text.endswith("Z") or time.utcoffset() != timedelta(0):
        raise ValueError("PV timestamps must use explicit UTC Z")
    return time


def _bounds(request):
    run = request["execution"]
    origin = _utc(run["time_axis"]["origin"])
    return tuple(
        origin + timedelta(microseconds=int(Decimal(str(run[k])) * 1000000))
        for k in ("start_time_s", "stop_time_s")
    )


@_safe_semantics
def validate_pv_weather(value, *, request, site, raw_bytes=None):
    errors = validate_pv_request(request, site=site)
    if errors:
        return errors
    errors = validate_time_series(value)
    if errors:
        return errors
    if (
        raw_bytes is not None
        and hashlib.sha256(raw_bytes).hexdigest() != request["weather"]["sha256"]
    ):
        errors.append(
            problem(
                "PV_WEATHER_HASH",
                "weather.sha256",
                "Weather bytes disagree with recorded hash",
            )
        )
    if (
        value["sampling"] != "interval_mean"
        or value["time_axis"] != request["execution"]["time_axis"]
    ):
        return [
            *errors,
            problem(
                "PV_TIME",
                "weather.time_axis",
                "Weather must use the request UTC interval axis",
            ),
        ]
    signals = {s["signal_id"]: s for s in value["signals"]}
    for quantity, sid in request["weather"]["channels"].items():
        target = "degC" if quantity == "temperature" else "W/m^2"
        signal = signals.get(sid)
        if (
            signal is None
            or signal["data_type"] != "real"
            or signal["model_id"] != request["execution"]["model_id"]
            or signal["causality"] != "input"
            or not units_compatible(signal["unit"], target)
        ):
            errors.append(
                problem(
                    "PV_WEATHER_UNIT",
                    "weather.channels." + quantity,
                    "Weather quantity requires a real signal with compatible explicit units",
                )
            )
    start, stop = _bounds(request)
    h = Decimal(str(request["execution"]["step_size_s"]))
    for i, row in enumerate(value["samples"]):
        a, b = _utc(row["time"]), _utc(row["end_time"])
        offset = Decimal(str((a - start).total_seconds()))
        if (
            a < start
            or b > stop
            or offset % h
            or Decimal(str((b - a).total_seconds())) != h
        ):
            errors.append(
                problem(
                    "PV_TIME",
                    f"weather.samples.{i}",
                    "Weather intervals must lie on the request grid within its bounds",
                )
            )
        for quantity in ("ghi", "dni", "dhi"):
            cell = row["values"].get(request["weather"]["channels"][quantity])
            if cell and cell["status"] == "valid" and cell["value"] < 0:
                errors.append(
                    problem(
                        "PV_IRRADIANCE",
                        f"weather.samples.{i}.{quantity}",
                        "Irradiance cannot be negative",
                    )
                )
    # Gaps and unavailable cells remain explicit inputs for partial result diagnostics.
    return errors


def _month_end(time):
    return datetime(
        time.year + (time.month == 12),
        1 if time.month == 12 else time.month + 1,
        1,
        tzinfo=timezone.utc,
    )


@_safe_semantics
def validate_pv_result(value, *, request, site):
    errors = validate(value, "pv/yield-result")
    if errors:
        return errors
    errors.extend(validate_pv_request(request, site=site))
    if errors:
        return errors
    run = value["execution"]
    errors.extend(validate_time_stepped_result(run, request=request["execution"]))
    if errors:
        return errors

    def fail(field, message, code="PV_ENERGY"):
        errors.append(problem(code, field, message))

    if value["weather"] != request["weather"] or not any(
        f["path"] == request["execution"]["input_series_file"]
        and f["role"] == "data"
        and f["sha256"] == request["weather"]["sha256"]
        for f in run["input_files"]
    ):
        fail(
            "weather",
            "Result must preserve weather identity and its hashed input file",
            "PV_WEATHER_HASH",
        )
    if not any(
        f["path"] == request["model_file"] and f["role"] == "model"
        for f in run["input_files"]
    ):
        fail(
            "execution.input_files",
            "Result must identify the bound model file",
            "PV_BINDING",
        )
    if run["series"]["sampling"] != "interval_mean":
        return [
            *errors,
            problem(
                "PV_TIME", "execution.series.sampling", "PV output is interval mean"
            ),
        ]
    start, stop = _bounds(request)
    rows = run["series"]["samples"]
    expected = int(
        (
            Decimal(str(request["execution"]["stop_time_s"]))
            - Decimal(str(request["execution"]["start_time_s"]))
        )
        / Decimal(str(request["execution"]["step_size_s"]))
    )
    valid = [
        r for r in rows if all(c["status"] == "valid" for c in r["values"].values())
    ]
    invalid = sum(
        any(c["status"] == "invalid" for c in r["values"].values()) for r in rows
    )
    missing = expected - len(valid) - invalid
    coverage = value["coverage"]
    if (_utc(coverage["start"]), _utc(coverage["end"])) != (start, stop) or (
        coverage["expected_intervals"],
        coverage["valid_intervals"],
        coverage["missing_intervals"],
        coverage["invalid_intervals"],
    ) != (expected, len(valid), missing, invalid):
        fail(
            "coverage",
            "Coverage counts must include every requested interval and its validity",
            "PV_COVERAGE",
        )
    complete = len(valid) == expected and run["status"] == "complete"

    # Energy is interval mean power times elapsed SI seconds / 3600 s per hour.
    # Gilman (2015), NREL/TP-6A20-64102 p. 56; calendar split is Quantic policy.
    def check_energy(entry, a, b):
        contributions = []
        valid_seconds = 0
        for row in valid:
            left, right = max(a, _utc(row["time"])), min(b, _utc(row["end_time"]))
            if right > left:
                seconds = (right - left).total_seconds()
                valid_seconds += seconds
                contributions.append(
                    row["values"]["site.ac_power_w"]["value"] * seconds / 3600
                )
        energy = math.fsum(contributions)
        full = valid_seconds == (b - a).total_seconds()
        if (_utc(entry["start"]), _utc(entry["end"])) != (a, b) or entry[
            "complete"
        ] != full:
            fail(
                "energy.coverage",
                "Energy interval bounds/completeness disagree with valid samples",
            )
        if entry["ac_energy_wh"] is None or not math.isclose(
            entry["ac_energy_wh"], energy, rel_tol=1e-10, abs_tol=1e-9
        ):
            fail(
                "energy.ac_energy_wh",
                "Energy must equal the sum over valid interval mean AC power",
            )

    check_energy(value["period"], start, stop)
    months = []
    a = start
    while a < stop:
        b = min(_month_end(a), stop)
        months.append((a, b))
        a = b
    if len(value["monthly"]) != len(months):
        fail("monthly", "Report each intersected UTC month exactly once")
    else:
        for entry, (a, b) in zip(value["monthly"], months, strict=True):
            check_energy(entry, a, b)
    year_start = datetime(start.year, 1, 1, tzinfo=timezone.utc)
    year_end = datetime(start.year + 1, 1, 1, tzinfo=timezone.utc)
    annual = complete and start == year_start and stop == year_end
    if annual:
        if value["annual"] is None:
            fail("annual", "A complete UTC calendar year must report its annual total")
        else:
            check_energy(value["annual"], start, stop)
    elif value["annual"] is not None:
        fail(
            "annual", "Incomplete years cannot claim annual yield", "PV_ANNUAL_COVERAGE"
        )
    if valid and not run["working"]:
        fail(
            "execution.working",
            "Calculated output requires D11 equations, sources and substitutions",
            "PV_WORKING",
        )
    if not complete and not run["diagnostics"]:
        fail(
            "execution.diagnostics",
            "Incomplete PV coverage requires diagnostics",
            "PV_COVERAGE",
        )
    if any(r["values"]["site.ac_power_w"]["value"] < 0 for r in valid):
        fail("execution.series", "Generated AC power must be nonnegative")
    return errors
