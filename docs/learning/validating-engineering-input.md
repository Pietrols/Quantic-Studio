# Validating engineering input

A JSON file can be syntactically valid and still describe an impossible or ambiguous
network. Validation is a sequence: read bytes, parse JSON, check the contract, check
relationships, and only then construct a usable project. The loader returns either a
Project or diagnostics; it never hands a solver a partly validated network.

JSON Schema checks local shape: a bus needs a positive nominal voltage, and a line
needs endpoint identifiers. Relationship checks answer a different question: do those
endpoints exist, and are identifiers unique? If bus-load has a negative vn_kv, the
error identifies bus-load and buses.1.vn_kv, so a future editor can highlight it.

Paths are also input. The manifest's relative paths are resolved inside the project,
including symlinks. A project cannot read an arbitrary neighboring file by using a
parent directory or a symlink. Schema references resolve from a local registry; a
network file does not cause a download of a remote schema.

The core validates at load time instead of generating Python schema classes. Project,
Network and Study are typed containers around validated dictionaries. This keeps the
JSON contracts authoritative while letting callers distinguish successful data from
errors. The objects are not a replacement for solver-specific checks such as whether
an energized component has a slack source.

## Units and bases

Unit conversion is multiplication by a defined scale. For SI prefixes, kilo means
10^3, so V_kV = V_V / 1000. Pint checks dimensional compatibility, preventing a length
from being treated as voltage. The contract specifies the target unit for each field.

Per unit is different: x_pu = x / x_base. A dimensionless number alone cannot tell us
its base. The core therefore does not guess a voltage or power base. Reactive,
apparent and real power share physical dimensions but have distinct engineering
meanings; units alone cannot enforce those meanings.

## Reproducing an input

A hash is a compact identity for bytes, not a proof that the model is correct.
The file hash uses SHA-256 over sorted relative paths and contents. Each part is
prefixed by its byte length so different filename/content splits cannot produce the
same concatenated input. A changed byte, including whitespace, changes this hash.
For in-memory solver data, a separate helper uses canonical JSON with sorted keys.
Provenance adds the solver name, installed version and UTC timestamp.

The tests use synthetic schema examples for validation and SI prefix identities for
units. No equipment rating or engineering tolerance is inferred from memory.

Sources: [jsonschema referencing](https://python-jsonschema.readthedocs.io/en/stable/referencing/),
[Pint tutorial](https://pint.readthedocs.io/en/stable/getting/tutorial.html), and
[BIPM SI Brochure, 9th edition, section 3](https://www.bipm.org/en/publications/si-brochure).
