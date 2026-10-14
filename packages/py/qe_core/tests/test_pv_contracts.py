"""Original hypothetical fixtures and handwritten dimensional/calendar oracles.

No datasheets, downloaded weather or engine-generated expected values.
100 W for two hours = 200 Wh. Gregorian leap 2024: 366 * 24 = 8784 h.
PVWatts rating identity: 1000 W DC * 0.9 = 900 W AC (pvlib parameter docs).
"""

import copy
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from qe_core import load_project, validate
from qe_core.pv_contracts import (
    pv_output_units,
    validate_pv_request,
    validate_pv_result,
    validate_pv_site,
    validate_pv_weather,
)

ROOT = Path(__file__).resolve().parents[4]


def site():
    return {
        "schema_version": "0.1.0",
        "site_id": "test-site",
        "name": "Authored hypothetical site",
        "latitude_deg": 0,
        "longitude_deg": 0,
        "elevation_m": 0,
        "orientation_convention": "north_clockwise_tilt_from_horizontal",
        "albedo": 0.2,
        "modules": [
            {
                "module_id": "module",
                "reference_dc_power_w": 300,
                "reference_cell_temperature_c": 25,
                "power_temperature_coefficient_per_k": -0.004,
                "temperature": {"model": "ross", "noct_c": 45},
            }
        ],
        "inverters": [
            {
                "inverter_id": "inverter",
                "dc_input_limit_w": 1000,
                "ac_rating_w": 900,
                "nominal_efficiency": 0.9,
                "reference_efficiency": 0.95,
            }
        ],
        "arrays": [
            {
                "array_id": "array",
                "mount": "fixed_tilt",
                "tilt_deg": 0,
                "azimuth_deg": 180,
                "module_id": "module",
                "module_count": 5,
                "inverter_id": "inverter",
            }
        ],
        "losses": [
            {
                "loss_id": "soiling",
                "name": "Hypothetical soiling",
                "stage": "irradiance",
                "fraction": 0.01,
            }
        ],
    }


# Independent frozen inventory, deliberately not produced by pv_output_units().
OUTPUTS = {
    "site.ac_power_w": "W",
    **{
        "array." + k: u
        for k, u in {
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
            "loss.soiling": "W/m^2",
        }.items()
    },
}


def signal(sid, unit, direction="output"):
    return {
        "schema_version": "0.1.0",
        "signal_id": sid,
        "model_id": "solar",
        "name": sid,
        "data_type": "real",
        "unit": unit,
        "causality": direction,
    }


def cell(value):
    return {"value": value, "status": "valid", "diagnostics": []}


def iso(t):
    return t.isoformat().replace("+00:00", "Z")


def request(duration=7200):
    return {
        "schema_version": "0.1.0",
        "model_file": "solar.json",
        "execution": {
            "schema_version": "0.1.0",
            "request_id": "yield",
            "study_id": "yield-study",
            "model_id": "solar",
            "time_axis": {"kind": "utc", "unit": "s", "origin": "2024-01-01T00:00:00Z"},
            "clock": "fixed_s",
            "start_time_s": 0,
            "stop_time_s": duration,
            "step_size_s": 3600 if duration == 7200 else duration,
            "signals": [signal(k, u) for k, u in OUTPUTS.items()],
            "input_series_file": "weather.json",
        },
        "weather": {
            "sha256": "0" * 64,
            "classification": "synthetic",
            "citation": "Original hypothetical fixture, CC-5 tests",
            "licence": "CC0-1.0",
            "timezone": "UTC",
            "calendar": "proleptic_gregorian",
            "channels": {
                "ghi": "ghi",
                "dni": "dni",
                "dhi": "dhi",
                "temperature": "temp",
            },
            "temperature_kind": "air",
        },
        "solar_position": {
            "model": "nrel_spa",
            "pressure_pa": 100000,
            "air_temperature_c": 20,
            "delta_t_s": 60,
            "atmospheric_refraction_deg": 0,
        },
        "irradiance_model": "isotropic",
        "dc_model": "pvwatts_v5",
        "inverter_model": "pvwatts_v5",
        "solar_sampling": "interval_midpoint",
    }


def intervals(req):
    run = req["execution"]
    origin = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return [
        (
            iso(origin + timedelta(seconds=t)),
            iso(origin + timedelta(seconds=t + run["step_size_s"])),
        )
        for t in range(0, run["stop_time_s"], run["step_size_s"])
    ]


def weather(req):
    return {
        "schema_version": "0.1.0",
        "series_id": "weather",
        "time_axis": req["execution"]["time_axis"],
        "sampling": "interval_mean",
        "signals": [
            signal(k, u, "input")
            for k, u in [
                ("ghi", "W/m^2"),
                ("dni", "W/m^2"),
                ("dhi", "W/m^2"),
                ("temp", "degC"),
            ]
        ],
        "samples": [
            {
                "time": a,
                "end_time": b,
                "values": {
                    k: cell(v)
                    for k, v in [("ghi", 500), ("dni", 600), ("dhi", 100), ("temp", 20)]
                },
            }
            for a, b in intervals(req)
        ],
        "diagnostics": [],
    }


def energy(a, b, amount):
    return {"start": a, "end": b, "complete": True, "ac_energy_wh": amount}


def result(req):
    run = req["execution"]
    bounds = intervals(req)
    h = run["step_size_s"]
    duration = run["stop_time_s"]

    def operation(op, before, after, current, target):
        return {
            "schema_version": "0.1.0",
            "session_id": "session",
            "operation": op,
            "state_before": before,
            "state_after": after,
            "current_time_s": current,
            "requested_time_s": target,
            "reached_time_s": target,
            "status": "success",
            "inputs": {},
            "outputs": {},
            "diagnostics": [],
        }

    steps = [operation("initialise", "instantiated", "initialized", 0, 0)]
    steps += [
        operation(
            "step_to", "initialized" if t == 0 else "running", "running", t, t + h
        )
        for t in range(0, duration, h)
    ]
    series = {
        "schema_version": "0.1.0",
        "series_id": "yield",
        "time_axis": run["time_axis"],
        "sampling": "interval_mean",
        "signals": run["signals"],
        "diagnostics": [],
        "samples": [
            {
                "time": a,
                "end_time": b,
                "values": {
                    key: cell(100 if key == "site.ac_power_w" else 0) for key in OUTPUTS
                },
            }
            for a, b in bounds
        ],
    }
    # Test inputs with explicitly authored power. No physics engine is used.
    execution = {
        "schema_version": "0.1.0",
        "result_id": "result",
        "request_id": "yield",
        "study_id": "yield-study",
        "model_id": "solar",
        "status": "complete",
        "requested_end_time_s": duration,
        "reached_time_s": duration,
        "series": series,
        "steps": steps,
        "working": [
            {
                "equation": "E=P*dt",
                "source": {
                    "citation": "Original constant-power derivation",
                    "locator": "100 W for two hours gives 200 Wh",
                },
                "substitutions": {
                    "P": {"value": 100, "unit": "W"},
                    "dt": {"value": 2, "unit": "h"},
                },
                "result": {"value": 200, "unit": "Wh"},
            }
        ],
        "model_versions": {"solar": "0.1.0"},
        "input_files": [
            {"path": "solar.json", "role": "model", "sha256": "1" * 64},
            {"path": "yield.json", "role": "request", "sha256": "2" * 64},
            {
                "path": "weather.json",
                "role": "data",
                "sha256": req["weather"]["sha256"],
            },
        ],
        "provenance": {
            "solver_name": "authored-reference",
            "solver_version": "1",
            "input_hash_sha256": "3" * 64,
            "timestamp": "2026-10-14T00:00:00Z",
        },
        "diagnostics": [],
    }
    return {
        "schema_version": "0.1.0",
        "execution": execution,
        "weather": copy.deepcopy(req["weather"]),
        "coverage": {
            "start": bounds[0][0],
            "end": bounds[-1][1],
            "expected_intervals": len(bounds),
            "valid_intervals": len(bounds),
            "missing_intervals": 0,
            "invalid_intervals": 0,
        },
        "period": energy(bounds[0][0], bounds[-1][1], 200),
        "monthly": [energy(bounds[0][0], bounds[-1][1], 200)],
        "annual": None,
    }


def codes(errors):
    return {e.code for e in errors}


def test_positive_and_independent_output_inventory():
    model = site()
    req = request()
    data = weather(req)
    res = result(req)
    assert pv_output_units(model) == OUTPUTS
    assert not validate_pv_site(model)
    assert not validate_pv_request(req, site=model)
    assert not validate_pv_weather(data, request=req, site=model)
    assert not validate_pv_result(res, request=req, site=model)
    for item, kind in [(model, "site"), (req, "yield-request"), (res, "yield-result")]:
        assert not validate(item, "pv/" + kind)
        assert item == json.loads(json.dumps(item))


@pytest.mark.parametrize(
    "field",
    [
        "latitude_deg",
        "longitude_deg",
        "elevation_m",
        "albedo",
        "orientation_convention",
        "modules",
        "inverters",
        "losses",
    ],
)
def test_missing_inputs_name_field(field):
    model = site()
    del model[field]
    errors = validate_pv_site(model)
    assert any(field in d.element_ref["field"] for d in errors)


@pytest.mark.parametrize(
    "field",
    [
        "reference_dc_power_w",
        "reference_cell_temperature_c",
        "power_temperature_coefficient_per_k",
        "temperature",
    ],
)
def test_missing_module_inputs(field):
    model = site()
    del model["modules"][0][field]
    assert any(field in d.element_ref["field"] for d in validate_pv_site(model))


@pytest.mark.parametrize("target", ["modules", "inverters", "arrays", "losses"])
def test_duplicate_equipment(target):
    model = site()
    model[target].append(copy.deepcopy(model[target][0]))
    assert "DUPLICATE_ID" in codes(validate_pv_site(model))


def test_rating_distinction_and_broken_references():
    model = site()
    assert (
        model["modules"][0]["reference_dc_power_w"] * 5 == 1500
    )  # independent array nameplate
    assert model["inverters"][0]["dc_input_limit_w"] == 1000  # unequal is legal
    model["inverters"][0]["ac_rating_w"] = 1500
    assert "PV_RATING" in codes(validate_pv_site(model))
    model = site()
    model["arrays"][0]["module_id"] = "absent"
    assert "UNKNOWN_ELEMENT" in codes(validate_pv_site(model))


@pytest.mark.parametrize("unit", ["A", "W", "nonsense"])
def test_weather_incompatible_units(unit):
    req = request()
    data = weather(req)
    data["signals"][0]["unit"] = unit
    assert codes(validate_pv_weather(data, request=req, site=site())) & {
        "PV_WEATHER_UNIT",
        "SIGNAL_UNIT",
    }


def test_temperature_and_output_bindings():
    req = request()
    req["weather"]["temperature_kind"] = "cell"
    assert "PV_TEMPERATURE" in codes(validate_pv_request(req, site=site()))
    model = site()
    model["modules"][0]["temperature"] = {"model": "supplied_cell"}
    assert not validate_pv_request(req, site=model)
    req["execution"]["signals"][0]["unit"] = "Wh"
    assert "PV_OUTPUTS" in codes(validate_pv_request(req, site=model))


def test_weather_hash_time_and_negative():
    req = request()
    data = weather(req)
    assert "PV_WEATHER_HASH" in codes(
        validate_pv_weather(data, request=req, site=site(), raw_bytes=b"{}")
    )
    data["samples"][0]["values"]["dni"]["value"] = -1
    assert "PV_IRRADIANCE" in codes(validate_pv_weather(data, request=req, site=site()))
    data = weather(req)
    data["samples"][0]["end_time"] = "2024-01-01T00:30:00Z"
    assert "PV_TIME" in codes(validate_pv_weather(data, request=req, site=site()))


@pytest.mark.parametrize(
    "field", ["period", "monthly", "annual", "working", "hash", "coverage"]
)
def test_result_rejects_unearned_claims(field):
    req = request()
    res = result(req)
    if field == "period":
        res["period"]["ac_energy_wh"] = 201
    elif field == "monthly":
        res["monthly"] = []
    elif field == "annual":
        res["annual"] = copy.deepcopy(res["period"])
    elif field == "working":
        res["execution"]["working"] = []
    elif field == "hash":
        res["weather"]["sha256"] = "f" * 64
    else:
        res["coverage"]["valid_intervals"] = 1
    assert validate_pv_result(res, request=req, site=site())


def test_leap_year_full_coverage_and_month_boundaries():
    # Hand reference: 100 W * 8784 hours = 878400 Wh, 29-day February = 69600 Wh.
    req = request(31622400)
    res = result(req)
    res["period"]["ac_energy_wh"] = 878400
    working = res["execution"]["working"][0]
    working["source"]["locator"] = "100 W for leap-year 8784 hours gives 878400 Wh"
    working["substitutions"]["dt"]["value"] = 8784
    working["result"]["value"] = 878400
    a = datetime(2024, 1, 1, tzinfo=timezone.utc)
    days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    res["monthly"] = []
    for d in days:
        b = a + timedelta(days=d)
        res["monthly"].append(energy(iso(a), iso(b), d * 2400))
        a = b
    res["annual"] = copy.deepcopy(res["period"])
    assert res["monthly"][1]["ac_energy_wh"] == 69600
    assert not validate_pv_result(res, request=req, site=site())
    res["monthly"][1]["ac_energy_wh"] = 67200  # 28-day assumption is incorrect in 2024
    assert "PV_ENERGY" in codes(validate_pv_result(res, request=req, site=site()))


def test_unavailable_interval_is_not_zero_or_annual():
    req = request()
    res = result(req)
    run = res["execution"]
    run["status"] = "partial"
    run["reached_time_s"] = 3600
    run["series"]["samples"] = run["series"]["samples"][:1]
    run["steps"] = run["steps"][:2]
    run["diagnostics"] = [
        {
            "code": "WEATHER_GAP",
            "severity": "warning",
            "message": "Authored missing interval",
            "element_ref": {
                "element_type": "pv",
                "element_id": "solar",
                "field": "weather",
            },
        }
    ]
    res["coverage"].update(valid_intervals=1, missing_intervals=1)
    for entry in [res["period"], *res["monthly"]]:
        entry.update(complete=False, ac_energy_wh=100)
    assert not validate_pv_result(res, request=req, site=site())
    res["annual"] = copy.deepcopy(res["period"])
    assert "PV_ANNUAL_COVERAGE" in codes(
        validate_pv_result(res, request=req, site=site())
    )


@pytest.fixture
def mixed(tmp_path):
    shutil.copytree(ROOT / "examples/multi_domain", tmp_path, dirs_exist_ok=True)
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    req = request()
    raw = json.dumps(weather(req)).encode()
    req["weather"]["sha256"] = hashlib.sha256(raw).hexdigest()
    (tmp_path / "weather.json").write_bytes(raw)
    (tmp_path / "solar.json").write_text(json.dumps(site()))
    (tmp_path / "yield.json").write_text(json.dumps(req))
    manifest["models"].append(
        {"model_id": "solar", "model_type": "pv.site", "file": "solar.json"}
    )
    manifest["studies"].append(
        {
            "study_id": "yield-study",
            "study_type": "pv.yield",
            "model_id": "solar",
            "request_file": "yield.json",
        }
    )
    for kind, eid in [
        ("site", "test-site"),
        ("arrays", "array"),
        ("modules", "module"),
        ("inverters", "inverter"),
    ]:
        manifest["asset_registry"]["assets"].append(
            {
                "asset_id": "solar-" + kind,
                "name": kind,
                "representations": [
                    {"model_id": "solar", "element_type": kind, "element_id": eid}
                ],
            }
        )
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    return tmp_path


def test_mixed_roundtrip_preserves_foreign_and_power_bytes(mixed):
    before = {p.name: p.read_bytes() for p in mixed.glob("*.json")}
    loaded = load_project(mixed)
    assert loaded.ok, loaded.diagnostics
    assert len(loaded.value.models) == 4
    assert mixed / "weather.json" in loaded.value.files
    assert loaded.value.model("solar").data == site()
    assert loaded.value.model("control").data == json.loads(before["control.json"])
    assert all(p.read_bytes() == before[p.name] for p in mixed.glob("*.json"))


@pytest.mark.parametrize(
    "case",
    [
        "asset",
        "model",
        "study",
        "missing-weather",
        "hash",
        "parent",
        "absolute",
        "symlink",
        "alias",
    ],
)
def test_mixed_invalid_binding(mixed, case):
    mp = mixed / "manifest.json"
    manifest = json.loads(mp.read_text())
    rp = mixed / "yield.json"
    req = json.loads(rp.read_text())
    if case == "asset":
        manifest["asset_registry"]["assets"][-1]["representations"][0]["element_id"] = (
            "missing"
        )
    elif case == "model":
        req["model_file"] = "plant.json"
    elif case == "study":
        req["execution"]["model_id"] = "plant"
    elif case == "missing-weather":
        (mixed / "weather.json").unlink()
    elif case == "hash":
        req["weather"]["sha256"] = "f" * 64
    elif case == "alias":
        req["execution"]["input_series_file"] = "solar.json"
    else:
        outside = mixed.parent / "external.json"
        outside.write_text("{}")
        if case == "symlink":
            (mixed / "escape.json").symlink_to(outside)
        req["execution"]["input_series_file"] = {
            "parent": "../external.json",
            "absolute": str(outside),
            "symlink": "escape.json",
        }[case]
    mp.write_text(json.dumps(manifest))
    rp.write_text(json.dumps(req))
    loaded = load_project(mixed)
    assert not loaded.ok
    assert any(d.element_ref and d.element_ref["field"] for d in loaded.diagnostics)


def test_old_contracts_and_public_types_unchanged():
    base = "98e322e"
    names = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", base, "contracts/"], cwd=ROOT, text=True
    ).splitlines()
    names += [
        "packages/ts/contracts/src/generated.ts",
        "packages/ts/contracts/src/legacy.ts",
    ]
    for name in names:
        assert (ROOT / name).read_bytes() == subprocess.check_output(
            ["git", "show", f"{base}:{name}"], cwd=ROOT
        )


@pytest.mark.parametrize("field", ["start_time_s", "stop_time_s", "step_size_s"])
def test_submicrosecond_grid_diagnosed(field):
    req = request()
    req["execution"][field] += 0.0000001
    assert "PV_TIME" in codes(validate_pv_request(req, site=site()))


def test_missing_and_invalid_weather_cells_remain_visible():
    req = request()
    data = weather(req)
    note = {
        "code": "AUTHORED_GAP",
        "message": "Original missing weather case",
        "severity": "warning",
        "element_ref": {
            "element_type": "signal",
            "element_id": "ghi",
            "field": "value",
        },
    }
    data["samples"][0]["values"]["ghi"] = {
        "value": None,
        "status": "missing",
        "diagnostics": [note],
    }
    assert not validate_pv_weather(data, request=req, site=site())
    assert data["samples"][0]["values"]["ghi"]["value"] is None
    data["samples"][0]["values"]["ghi"]["diagnostics"] = []
    assert validate_pv_weather(data, request=req, site=site())


def test_weather_cannot_alias_another_study_request(mixed):
    path = mixed / "yield.json"
    req = json.loads(path.read_text())
    req["execution"]["input_series_file"] = "scan.json"
    path.write_text(json.dumps(req))
    assert "PV_FILE_ALIAS" in codes(load_project(mixed).diagnostics)
