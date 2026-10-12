"""Killable, bounded worker processes instead of unbounded background threads."""
import json
import subprocess
import sys
import threading


class WorkerError(Exception):
    def __init__(self, code, message, status=500):
        self.code, self.message, self.status = code, message, status


class Runner:
    def __init__(self, timeout_s=30, max_workers=2, command=None):
        if timeout_s <= 0 or max_workers < 1:
            raise ValueError('Positive timeout and worker count required')
        self.timeout_s = timeout_s
        self.slots = threading.BoundedSemaphore(max_workers)
        self.command = command or [sys.executable, '-m', 'qe_api.worker']

    def run(self, payload):
        if not self.slots.acquire(blocking=False):
            raise WorkerError('STUDY_BUSY', 'All study workers are busy; retry later', 429)
        try:
            with subprocess.Popen(self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, text=True) as process:
                try:
                    out, _ = process.communicate(json.dumps(payload, allow_nan=False), timeout=self.timeout_s)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.communicate()
                    raise WorkerError('STUDY_TIMEOUT', 'Study exceeded the configured execution limit', 504) from None
                if process.returncode != 0:
                    raise WorkerError('WORKER_FAILURE', 'Study worker exited unsuccessfully')
                try:
                    value = json.loads(out)
                    if not isinstance(value, dict) or not ('result' in value or value.get('error')):
                        raise ValueError('Invalid worker envelope')
                    return value
                except ValueError as exc:
                    raise WorkerError('WORKER_FAILURE', 'Study worker returned invalid JSON') from exc
        except OSError as exc:
            raise WorkerError('WORKER_FAILURE', 'Could not start study worker') from exc
        finally:
            self.slots.release()
