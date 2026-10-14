"""PV interface seed only. WP-2.5 supplies the actual yield engine."""

from .engine import UnavailablePVEngine

__version__ = "0.1.0"
__all__ = ["UnavailablePVEngine"]
