"""PDF exports retain engineering meaning, data and diagnostics across interfaces."""
import base64
import io
import json
import re
import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pypdf import PdfReader
from qe_api import create_app
from qe_api.worker import execute
from qe_cli.main import main
from qe_core import load_project
from qe_report import PDFRenderError, render_loadflow_report, render_pdf

ROOT = Path(__file__).resolve().parents[2]


def compact(text):
    return re.sub(r'\s+', '', text)


def pdf_text(data):
    reader = PdfReader(io.BytesIO(data))
    return reader, '\n'.join(p.extract_text() for p in reader.pages)


def assert_report_retained(markdown, text):
    # Compare every displayed cell/paragraph, including exact printed numbers,
    # equations, IDs, units, assumptions and warnings. Pagination can wrap words.
    for line in markdown.splitlines():
        if not line or re.fullmatch(r'\|[-|:]+\|', line):
            continue
        parts = re.split(r'(?<!\\)\|', line[1:-1]) if line.startswith('|') else [line]
        for part in parts:
            part = re.sub(r'^#{1,3} |^> |^- ', '', part.strip())
            part = part.replace('**', '').replace('`', '').replace(r'\|', '|')
            assert compact(part) in compact(text), part


@pytest.mark.parametrize('project,study', [
    ('fourteen_bus', 'loadflow-base'), ('shortcircuit', 'fault'), ('motorstart', 'motorstart'),
    ('multi_domain', 'plant-flow'), ('multi_domain', 'plant-fault'), ('multi_domain', 'motor-start'),
])
def test_cli_authored_pdf_retains_all_report_content(tmp_path, project, study):
    folder = tmp_path / project
    shutil.copytree(ROOT / 'examples' / project, folder, ignore=shutil.ignore_patterns('out'))
    before = {p: p.read_bytes() for p in folder.glob('*.json')}
    assert main(['study', 'run', str(folder), '--study', study, '--report-format', 'pdf']) == 0
    reader, text = pdf_text((folder / 'out/report.pdf').read_bytes())
    markdown = (folder / 'out/report.md').read_text()
    result = json.loads((folder / 'out/results.json').read_text())
    assert_report_retained(markdown, text)
    assert compact(result['provenance']['input_hash_sha256']) in compact(text)
    assert 'Page 1' in text and reader.metadata.author == 'Quantic Studio'
    assert before == {p: p.read_bytes() for p in folder.glob('*.json')}


@pytest.mark.parametrize('study', ['plant-flow', 'plant-fault', 'motor-start'])
def test_real_api_bounded_pdf_worker(tmp_path, study):
    shutil.copytree(ROOT / 'examples/multi_domain', tmp_path / 'mixed', ignore=shutil.ignore_patterns('out'))
    before = {p: p.read_bytes() for p in tmp_path.rglob('*.json')}
    client = TestClient(create_app(tmp_path), base_url='http://127.0.0.1')
    assert client.get('/health').json()['report_formats'] == ['markdown', 'pdf']
    response = client.post('/api/studies/run', json={'project_path': 'mixed', 'study_id': study,
                                                   'report_format': 'pdf'})
    assert response.status_code == 200, response.text
    data = response.json()
    pdf = base64.b64decode(data['report_pdf_base64'], validate=True)
    assert pdf.startswith(b'%PDF-')
    _, text = pdf_text(pdf)
    assert_report_retained(data['report_markdown'], text)
    assert before == {p: p.read_bytes() for p in tmp_path.rglob('*.json')}
    assert not list(tmp_path.rglob('out'))
    bad = client.post('/api/studies/run', json={'project_path': 'mixed', 'study_id': study,
                                               'report_format': 'html'})
    assert bad.status_code == 422 and 'diagnostics' in bad.json()


@pytest.mark.parametrize('project,mode,study', [
    ('motorstart', 'failed', 'motorstart'), ('motorstart', 'limit', 'motorstart'),
    ('shortcircuit', 'partial', 'fault'),
])
def test_incomplete_calculation_and_compliance_are_visible(tmp_path, project, mode, study):
    shutil.copytree(ROOT / 'examples' / project, tmp_path, dirs_exist_ok=True, ignore=shutil.ignore_patterns('out'))
    path = tmp_path / ('motorstart-request.json' if project == 'motorstart' else 'shortcircuit-request.json')
    request = json.loads(path.read_text())
    request[{'failed': 'max_iterations', 'limit': 'dip_limit_percent', 'partial': 'frequency_hz'}[mode]] = {
        'failed': 1, 'limit': 1, 'partial': 60}[mode]
    path.write_text(json.dumps(request))
    assert main(['study', 'run', str(tmp_path), '--study', study, '--report-format', 'pdf']) == 1
    _, text = pdf_text((tmp_path / 'out/report.pdf').read_bytes())
    assert_report_retained((tmp_path / 'out/report.md').read_text(), text)
    assert {'failed': 'UNKNOWN', 'limit': 'FAIL', 'partial': 'PARTIAL'}[mode] in text
    if mode != 'limit':
        assert 'n/a' in text
    if mode == 'partial':
        assert 'THERMAL_FREQUENCY_UNAVAILABLE' in compact(text)


def test_large_network_table_repeats_headers_and_retains_last_row():
    # Repeat independently referenced two-bus values only to exercise pagination.
    # This is a presentation fixture, not a new solved physical network.
    fixture = ROOT / 'tests/fixtures/power/two_bus_analytic'
    network = json.loads((fixture / 'network.json').read_text())
    result = json.loads((fixture / 'reference.json').read_text())
    network['buses'] = [{**network['buses'][0], 'bus_id': f'bus-{i:04d}'} for i in range(500)]
    result['bus_results'] = [{**result['bus_results'][0], 'bus_id': f'bus-{i:04d}'} for i in range(500)]
    request = {'request_id': 'pagination', 'tolerance_mva': 0.0001, 'max_iterations': 20}
    markdown = render_loadflow_report(project_name='Pagination fixture', network=network,
                                      request=request, result=result)
    reader, text = pdf_text(render_pdf(markdown))
    assert len(reader.pages) > 10
    assert_report_retained(markdown, text)
    for page in reader.pages:
        page_text = page.extract_text()
        if re.search(r'bus-\d{4}', page_text):
            # Both bus tables (voltages, and the WP-1.11 power balance) repeat their headers.
            assert ('Nominal kV' in page_text and 'V (pu)' in page_text) or 'P residual (MW)' in page_text
    assert f'Page {len(reader.pages)}' in reader.pages[-1].extract_text()


def test_escaped_user_text_and_long_diagnostics_survive():
    message = ('Detailed diagnostic with element_id ' + 'a' * 100 + ' ') * 250
    report = '# Safe <report> & data\n\n| Code | Message |\n|---|---|\n| X | ' + message + r' left\|right |'
    reader, text = pdf_text(render_pdf(report))
    assert len(reader.pages) > 1
    content = '\n'.join(line for line in text.splitlines() if line.strip() not in {
        'QUANTIC STUDIO | ENGINEERING STUDY',
        'Inputs, assumptions and solver provenance included in this report', 'Code', 'Message'
    } and not re.fullmatch(r'Page \d+', line))
    assert compact(message) in compact(content)
    assert 'left|right' in text and '<report> & data' in text


def test_export_failure_is_explicit_cli_and_api_diagnostic(tmp_path, capsys):
    shutil.copytree(ROOT / 'examples/motorstart', tmp_path / 'motor', ignore=shutil.ignore_patterns('out'))
    path = tmp_path / 'motor/manifest.json'
    manifest = json.loads(path.read_text())
    manifest['name'] = 'Unsupported glyph \U0001f600'
    path.write_text(json.dumps(manifest))
    assert main(['study', 'run', str(path.parent), '--study', 'motorstart', '--report-format', 'pdf']) == 2
    assert 'REPORT_EXPORT' in capsys.readouterr().err
    assert not (path.parent / 'out').exists()
    client = TestClient(create_app(tmp_path), base_url='http://127.0.0.1')
    response = client.post('/api/studies/run', json={'project_path': 'motor', 'study_id': 'motorstart',
                                                   'report_format': 'pdf'})
    assert response.status_code == 422
    assert response.json()['diagnostics'][0]['code'] == 'REPORT_EXPORT'
    # Markdown remains available even when a font cannot represent a label.
    loaded = load_project(path.parent).value
    selected = loaded.studies[0]
    data = execute({'study_type': selected.study_type, 'network': loaded.model(selected.model_id).data,
                    'request': selected.request, 'project_name': loaded.name, 'model_id': selected.model_id})
    assert not data.get('error') and 'report_pdf_base64' not in data


def test_markdown_rerun_removes_stale_pdf(tmp_path):
    shutil.copytree(ROOT / 'examples/motorstart', tmp_path, dirs_exist_ok=True)
    args = ['study', 'run', str(tmp_path), '--study', 'motorstart']
    assert main([*args, '--report-format', 'pdf']) == 0
    assert (tmp_path / 'out/report.pdf').exists()
    assert main(args) == 0
    assert not (tmp_path / 'out/report.pdf').exists()


@pytest.mark.parametrize('report', ['', '| A | B |\n|---|---|\n| one |', '# Unknown \U0001f600'])
def test_render_failures_are_named(report):
    with pytest.raises(PDFRenderError):
        render_pdf(report)
