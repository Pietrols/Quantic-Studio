from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
IMPORT_PATHS = (
    REPOSITORY_ROOT / "packages" / "py" / "qe_power" / "src",
    REPOSITORY_ROOT / "tests" / "fixtures" / "power",
)
for import_path in IMPORT_PATHS:
    if str(import_path) not in sys.path:
        sys.path.insert(0, str(import_path))
