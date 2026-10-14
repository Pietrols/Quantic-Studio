"""plc.scan suite seam, filled by its end-to-end WP."""

from qe_core.validation import diagnostic


def execute(payload):
    return {
        "error": True,
        "diagnostics": [
            diagnostic(
                "ENGINE_UNAVAILABLE",
                "plc.scan execution is not yet connected",
                "study",
                payload["request"]["execution"]["study_id"],
                "execution",
            ).to_dict()
        ],
    }
