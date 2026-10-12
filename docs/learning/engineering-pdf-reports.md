# Reproducible engineering study reports

A PDF is the fixed-layout presentation of a study, not another solver. Quantic
Studio converts the same authored Markdown report into PDF. Every printed value,
unit, assumption, warning, identifier and provenance item comes from that report.
There is no separate PDF calculation that could silently disagree with the screen.

An engineering deliverable must identify the network and request, the calculation
status, the inputs and assumptions, results with units, operating limits and
limitations, diagnostics and the solver provenance. The machine-readable results
remain alongside the report so full precision and diagnostics are available.
The SHA-256 identifies canonical engineering inputs and the complete request;
the timestamp and solver version distinguish runs. PDF bytes are not the input
identity: document metadata can differ between exports.

## Calculation and compliance

Convergence means the algorithm solved its equations. It does not prove the
operating point satisfies voltage, equipment or reactive-power limits. Motor-start
reports keep calculation SUCCESS separate from dip PASS/FAIL/UNKNOWN. Their
reported definition remains:

`Dip (%) = 100 * (pre-start voltage - locked-rotor voltage) / pre-start voltage`.

A negative dip is a voltage rise, not a missing result. A null fault duty is `n/a`,
not zero. Partial fault studies retain their case diagnostics and their warning
that they cannot complete equipment-duty verification. The reports retain the
existing source gaps and do not claim standards certification.

## Export and pagination

Run `uv run qe study run examples/motorstart --study motorstart --report-format pdf`.
This writes `out/report.pdf`, `out/report.md` and `out/results.json`. Markdown-only
reruns remove a previous PDF so it cannot be mistaken for the new result. PDF
export failure reports `REPORT_EXPORT` and a nonzero exit; a failed calculation or
failed motor dip check still exports its warnings and retains study exit code 1.

The API advertises `markdown` and `pdf` through `/health`. Send `report_format: pdf`
to `/api/studies/run` to receive `report_pdf_base64` alongside the normal result and
Markdown. The existing editor shows PDF selection/download automatically. Omitting
the option keeps the original Markdown response. PDF rendering happens inside the
same killable, bounded study worker, with no project-file writes.

Landscape A4 gives the eleven-column branch-flow table room for readable labels.
Tables wrap identifiers and messages, repeat their headers on new pages, and split
long rows. Headings remain with following content. Headers and numbered footers
identify every page. Bundled Bitstream Vera fonts make deployment independent of
system fonts. A glyph absent from these fonts produces an explicit export error;
it is never silently replaced with a square. Text is escaped before paragraph
formatting so project labels cannot inject ReportLab markup.

Tests compare extracted PDF text against every displayed cell and paragraph,
including exact formatted numbers, units, equations, input hashes and diagnostics.
A 500-bus presentation fixture repeats independently referenced values to exercise
pagination without inventing a numerical reference. Visual checks of all three
examples complement extraction: text presence alone cannot detect clipping,
overlap, weak contrast or an unreadable table.
