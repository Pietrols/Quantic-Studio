"""PDF presentation of our authored Markdown reports; no engineering recomputation.

ReportLab Platypus LongTable repeats headers and splits rows across pages:
https://docs.reportlab.com/reportlab/userguide/ch7_tables/
This intentionally supports our report dialect, not arbitrary HTML or Markdown.
"""
from __future__ import annotations

import io
import re
import threading
from pathlib import Path
from xml.sax.saxutils import escape

import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import LongTable, Paragraph, SimpleDocTemplate, Spacer, TableStyle


class PDFRenderError(ValueError):
    """Presentation failed; callers must expose REPORT_EXPORT, never a partial PDF."""


_FONT_LOCK = threading.Lock()
_INK = colors.HexColor('#17354a')
_BLUE = colors.HexColor('#eaf1f5')


def _fonts():
    # Bundled Bitstream Vera fonts avoid a machine-specific system-font dependency.
    with _FONT_LOCK:
        if 'QEReport' not in pdfmetrics.getRegisteredFontNames():
            root = Path(reportlab.__file__).parent / 'fonts'
            pdfmetrics.registerFont(TTFont('QEReport', str(root / 'Vera.ttf')))
            pdfmetrics.registerFont(TTFont('QEReportBold', str(root / 'VeraBd.ttf')))
            pdfmetrics.registerFontFamily('QEReport', normal='QEReport', bold='QEReportBold')


def _inline(text):
    # Escape user-supplied text before adding only our own Paragraph markup.
    parts = re.split(r'(`[^`]*`|\*\*[^*]+\*\*)', text)
    return ''.join('<b>' + escape(p[2:-2]) + '</b>' if p.startswith('**') and p.endswith('**')
                   else escape(p[1:-1]) if p.startswith('`') and p.endswith('`')
                   else escape(p) for p in parts).replace('\n', '<br/>')


def _cells(line):
    return [p.strip().replace(r'\|', '|') for p in re.split(r'(?<!\\)\|', line.strip()[1:-1])]


def _table(lines, width, body, header):
    rows = [_cells(line) for line in lines]
    if len(rows) < 2 or any(not re.fullmatch(r':?-{3,}:?', cell) for cell in rows[1]):
        raise PDFRenderError('Malformed report table separator')
    columns = len(rows[0])
    rows = [rows[0], *rows[2:]]
    if any(len(row) != columns for row in rows):
        raise PDFRenderError('Report table has inconsistent column counts')
    weights = [1.0] * columns
    if columns == 2:
        weights = [1, 3]
    elif rows[0][-1] == 'Message':
        weights[-1] = 4
    if 'Equation with inputs' in rows[0]:
        weights[rows[0].index('Equation with inputs')] = 4
    widths = [width * weight / sum(weights) for weight in weights]
    data = [[Paragraph(_inline(cell), header if n == 0 else body) for cell in row]
            for n, row in enumerate(rows)]
    return LongTable(data, colWidths=widths, repeatRows=1, splitInRow=1,
                     hAlign='LEFT', spaceAfter=10, style=TableStyle([
                         ('BACKGROUND', (0, 0), (-1, 0), _INK),
                         ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, _BLUE]),
                         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                         ('LEFTPADDING', (0, 0), (-1, -1), 6),
                         ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                         ('TOPPADDING', (0, 0), (-1, -1), 5),
                         ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                         ('LINEBELOW', (0, 0), (-1, 0), 0.5, _INK),
                     ]))


def render_pdf(markdown: str) -> bytes:
    """Return a complete PDF or raise PDFRenderError, retaining report text and values.

Unsupported glyphs are an explicit export error instead of invisible missing text.
Landscape A4 accommodates the 11-column load-flow branch table at readable 8 pt.
"""
    try:
        if not isinstance(markdown, str) or not markdown.strip():
            raise PDFRenderError('Report text is empty')
        _fonts()
        supported = set(pdfmetrics.getFont('QEReport').face.charToGlyph)
        supported &= set(pdfmetrics.getFont('QEReportBold').face.charToGlyph)
        missing = sorted({ord(c) for c in markdown if not c.isspace() and ord(c) not in supported})
        if missing:
            raise PDFRenderError('Report font cannot represent ' + ', '.join(f'U+{c:04X}' for c in missing))
        stream = io.BytesIO()
        doc = SimpleDocTemplate(stream, pagesize=landscape(A4), leftMargin=36, rightMargin=36,
                                topMargin=42, bottomMargin=36, title='Quantic Studio study report',
                                author='Quantic Studio')
        body = ParagraphStyle('Body', fontName='QEReport', fontSize=9, leading=13,
                              textColor=_INK, spaceAfter=7, splitLongWords=True)
        cell = ParagraphStyle('Cell', parent=body, fontSize=8, leading=11, spaceAfter=0)
        header = ParagraphStyle('Header', parent=cell, fontName='QEReportBold', textColor=colors.white)
        headings = [ParagraphStyle(f'H{i}', parent=body, fontName='QEReportBold',
                                   fontSize=size, leading=size + 4, spaceBefore=10,
                                   spaceAfter=8, keepWithNext=True)
                    for i, size in enumerate((19, 13, 10))]
        warning = ParagraphStyle('Warning', parent=body, backColor=_BLUE, borderPadding=7)
        story = []
        lines = markdown.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            if line.startswith('|'):
                start = i
                while i < len(lines) and lines[i].startswith('|'):
                    i += 1
                story.append(_table(lines[start:i], doc.width, cell, header))
                continue
            heading = re.match(r'^(#{1,3}) (.*)', line)
            if heading:
                story.append(Paragraph(_inline(heading[2]), headings[len(heading[1]) - 1]))
            elif line.startswith('- '):
                story.append(Paragraph(_inline(line[2:]), body, bulletText='-'))
            elif line.startswith('> '):
                story.append(Paragraph(_inline(line[2:]), warning))
            else:
                story.append(Paragraph(_inline(line), body))
            i += 1
        story.append(Spacer(1, 4))

        def page(canvas, document):
            canvas.saveState()
            canvas.setFont('QEReport', 8)
            canvas.setFillColor(_INK)
            canvas.drawString(36, document.pagesize[1] - 24, 'QUANTIC STUDIO | ENGINEERING STUDY')
            canvas.drawString(36, 20, 'Inputs, assumptions and solver provenance included in this report')
            canvas.drawRightString(document.pagesize[0] - 36, 20, f'Page {document.page}')
            canvas.restoreState()

        doc.build(story, onFirstPage=page, onLaterPages=page)
        return stream.getvalue()
    except PDFRenderError:
        raise
    except Exception as exc:
        raise PDFRenderError(f'Could not render study report: {exc}') from exc
