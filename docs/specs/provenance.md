# Provenance

Schema: `../../contracts/common/provenance.schema.json`

Every result records the solver name and version, a SHA-256 hash of the complete input used for the run, and a timestamp in RFC 3339 date-time form. The hash is 64 hexadecimal characters. This makes it possible to identify which inputs and solver produced a result.

The following synthetic example illustrates the shape only. The solver and hash values are placeholders, not a real run.

```json
{
  "solver_name": "example-solver",
  "solver_version": "0.1.0",
  "input_hash_sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "timestamp": "2026-01-01T00:00:00Z"
}
```
