"""Killable processes with bounded transport, deadline and concurrent worker slots."""

import json
import subprocess
import sys
import tempfile
import threading
import time


class WorkerError(Exception):
    def __init__(self, code, message, status=500):
        self.code, self.message, self.status = code, message, status


class Runner:
    def __init__(
        self,
        timeout_s=30,
        max_workers=2,
        command=None,
        max_input_bytes=10_000_000,
        max_output_bytes=64_000_000,
        max_stderr_bytes=1_000_000,
    ):
        # Resource policy, not engineering constants. Override for local capacity/tests.
        if (
            timeout_s <= 0
            or max_workers < 1
            or min(max_input_bytes, max_output_bytes, max_stderr_bytes) < 1
        ):
            raise ValueError("Positive timeout, worker count and byte limits required")
        self.timeout_s = timeout_s
        self.slots = threading.BoundedSemaphore(max_workers)
        self.command = command or [sys.executable, "-m", "qe_api.worker"]
        self.max_input_bytes, self.max_output_bytes = max_input_bytes, max_output_bytes
        self.max_stderr_bytes = max_stderr_bytes

    def run(self, payload):
        if not self.slots.acquire(blocking=False):
            raise WorkerError(
                "STUDY_BUSY", "All study workers are busy; retry later", 429
            )
        try:
            encoded = json.dumps(payload, allow_nan=False).encode("utf-8")
            if len(encoded) > self.max_input_bytes:
                raise WorkerError(
                    "INPUT_LIMIT", "Study transport exceeds configured byte limit", 413
                )
            # Temporary transport avoids deadlocked pipes and unbounded communicate buffers.
            # It never writes project data. Output is monitored and killed at the byte limit.
            with (
                tempfile.TemporaryFile() as source,
                tempfile.TemporaryFile() as output,
                tempfile.TemporaryFile() as errors,
            ):
                source.write(encoded)
                source.seek(0)
                deadline = time.monotonic() + self.timeout_s
                with subprocess.Popen(
                    self.command, stdin=source, stdout=output, stderr=errors
                ) as process:
                    while True:
                        output.seek(0, 2)
                        errors.seek(0, 2)
                        if (
                            output.tell() > self.max_output_bytes
                            or errors.tell() > self.max_stderr_bytes
                        ):
                            process.kill()
                            process.wait()
                            raise WorkerError(
                                "RESULT_LIMIT",
                                "Study worker exceeded transport byte limit",
                                413,
                            )
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            process.kill()
                            process.wait()
                            raise WorkerError(
                                "STUDY_TIMEOUT",
                                "Study exceeded the configured execution limit",
                                504,
                            )
                        try:
                            process.wait(timeout=min(remaining, 0.02))
                            break
                        except subprocess.TimeoutExpired:
                            pass
                    output.seek(0, 2)
                    errors.seek(0, 2)
                    if (
                        output.tell() > self.max_output_bytes
                        or errors.tell() > self.max_stderr_bytes
                    ):
                        raise WorkerError(
                            "RESULT_LIMIT",
                            "Study worker exceeded transport byte limit",
                            413,
                        )
                    if process.returncode != 0:
                        raise WorkerError(
                            "WORKER_FAILURE", "Study worker exited unsuccessfully"
                        )
                    output.seek(0)
                    try:
                        value = json.loads(output.read(self.max_output_bytes + 1))
                        if not isinstance(value, dict) or not (
                            "result" in value or value.get("error")
                        ):
                            raise ValueError("Invalid worker envelope")
                        return value
                    except (ValueError, UnicodeError) as exc:
                        raise WorkerError(
                            "WORKER_FAILURE", "Study worker returned invalid JSON"
                        ) from exc
        except OSError as exc:
            raise WorkerError("WORKER_FAILURE", "Could not start study worker") from exc
        finally:
            self.slots.release()
