# Motor-starter scan fixture (authored)

Original scenario written for WP-2.9 by Claude on 2026-10-14. It is not a measured
plant, a manufacturer's program or a standard example. Contracts: CC-6
(`docs/specs/plc-program-and-scan.md`).

- `model.json`: `automation.plc` controller with a seal-in starter, a 200 ms feedback
  supervision timer (TON) and a start counter (CTU, PV 2), wired to the authored
  motor-starter process.
- `scan.json`: `plc.scan` request, 100 ms period, 1.2 s run (12 scans).
- `events.json`: input events. Its SHA-256 is pinned in `scan.json`.

The expected scan-by-scan table is handwritten in
`packages/py/qe_plc/tests/test_scan_study.py`, worked from the spec, not produced by
the engine.
