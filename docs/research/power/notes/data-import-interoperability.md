# Data import and interoperability (matrix D16; WP-2.10)

Switching cost is a buying barrier. A mine's existing study sits in ETAP or
PowerFactory, and a utility's in PSS/E or CGMES. Quantic must **read** those formats,
convert to its JSON contract, and report what was lost. Checked 2026-10-15.

## What the open libraries already read

| Format | pandapower converters (docs) | VeraGrid file operations (docs) |
| --- | --- | --- |
| MATPOWER / PYPOWER | import and export | import and export (MATPOWER export skips HVDC and VSC) |
| CGMES / CIM | CGMES import | CIM 16, CGMES 2.4.15 and 3.0 import and export (export needs a boundary set) |
| PSS/E RAW | not listed | **RAW/RAWX versions 29 to 35**, import and export (snapshot only) |
| PSS/E DYR (dynamics) | not listed | not listed |
| PowerFactory | import from Python (needs PowerFactory running) | **DGS import and export** (not fully lossless) |
| UCTE-DEF | import | import and export (regulation rows flattened) |
| OpenDSS | `from_opendss()` import | not listed |
| PSLF, ANAREDE, Eurostag, IIDM | not listed | import (PSLF not fully lossless) |
| pandapower, PyPSA | native | import (optional packages) |
| ETAP | none | none |

Sources: https://pandapower.readthedocs.io/en/latest/converter.html and
https://veragrid.readthedocs.io/en/latest/md_source/file_operations.html (both read
2026-10-15). VeraGrid is MPL-2.0 and pandapower is BSD-3 (`open-source-foundations.md`).

## Gaps and plan

1. **ETAP projects:** no open reader exists. ETAP exports to Excel and other formats
   (dossier). The practical route is an ETAP Excel/CSV export template that Quantic
   imports, with a mapping table per element type. Verify with a real export from a
   client.
2. **PowerFactory:** DGS through VeraGrid's reader (MPL-2.0; usable as a library). We
   test losslessness on our own cases and list the dropped attributes in the import
   report.
3. **PSS/E RAW:** through VeraGrid. **DYR** (dynamic models) is needed for T1 reuse.
   ANDES reads DYR but is GPL (separate process only), so the DYR parser should be ours.
4. **Import report:** every import produces a diagnostics list (element, field, "not
   mapped" or "approximated") using our existing diagnostic format. Silent loss is the
   main complaint about converters.
5. **Export:** Quantic contract to MATPOWER, CGMES and PSS/E through VeraGrid, so clients
   can hand models to utilities (Zambian connection studies may require a ZESCO
   format; ask ZESCO which one).
