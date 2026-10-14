"""Explicit unavailable engine implementing the common CC-4 interface."""

from copy import deepcopy

from qe_core.stepping import EngineError
from qe_core.validation import diagnostic


class UnavailablePVEngine:
    solver_name = "qe_pv"
    solver_version = "0.1.0"
    output_sampling = "interval_mean"

    def __init__(self, signals):
        self.signals = deepcopy(list(signals))

    def _unavailable(self):
        model_id = self.signals[0]["model_id"] if self.signals else "pv"
        raise EngineError(
            [
                diagnostic(
                    "ENGINE_UNAVAILABLE",
                    "PV yield engine is not implemented; WP-2.5 supplies the numerical adapter",
                    "model",
                    model_id,
                    "engine",
                )
            ]
        )

    def initialise(self, time_s):
        self._unavailable()

    def set_inputs(self, values):
        self._unavailable()

    def step_to(self, time_s):
        self._unavailable()

    def get_outputs(self):
        self._unavailable()

    def terminate(self):
        self._unavailable()

    def reset(self):
        self._unavailable()
