"""Small worker supervisor with bounded, reliable child-process cleanup."""
from __future__ import annotations

import signal
import subprocess
import sys
import time
from pathlib import Path

CHECK_INTERVAL = 3
SHUTDOWN_TIMEOUT = 5
WORKER_NAMES = ("worker-1", "worker-2", "worker-3")
SCRIPT_DIR = Path(__file__).resolve().parent


class Overseer:
    def __init__(self) -> None:
        self.workers: dict[str, subprocess.Popen[bytes]] = {}
        self.stopping = False

    def start_worker(self, name: str) -> subprocess.Popen[bytes]:
        # Use the active interpreter and an absolute script path; do not depend
        # on the caller's working directory or PATH selecting a different Python.
        process = subprocess.Popen(
            [sys.executable, str(SCRIPT_DIR / "workers.py"), name],
            cwd=SCRIPT_DIR,
            stdin=subprocess.DEVNULL,
            close_fds=True,
        )
        self.workers[name] = process
        print(f"[OVERSEER] started {name} pid={process.pid}", flush=True)
        return process

    def ensure_workers(self) -> None:
        for name in WORKER_NAMES:
            process = self.workers.get(name)
            if process is None or process.poll() is not None:
                if process is not None:
                    print(
                        f"[OVERSEER] {name} exited (code={process.returncode}); restarting",
                        flush=True,
                    )
                else:
                    print(f"[OVERSEER] {name} missing; starting", flush=True)
                self.start_worker(name)

    def shutdown(self) -> None:
        self.stopping = True
        children = list(self.workers.values())
        for process in children:
            if process.poll() is None:
                process.terminate()

        deadline = time.monotonic() + SHUTDOWN_TIMEOUT
        for process in children:
            remaining = max(0.0, deadline - time.monotonic())
            try:
                process.wait(timeout=remaining)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

        self.workers.clear()
        print("[OVERSEER] all workers stopped", flush=True)

    def monitor(self) -> None:
        for name in WORKER_NAMES:
            self.start_worker(name)
        try:
            while not self.stopping:
                self.ensure_workers()
                time.sleep(CHECK_INTERVAL)
        except (KeyboardInterrupt, SystemExit):
            print("[OVERSEER] shutting down", flush=True)
        finally:
            self.shutdown()


if __name__ == "__main__":
    supervisor = Overseer()

    def request_shutdown(_signum: int, _frame: object) -> None:
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, request_shutdown)
    signal.signal(signal.SIGINT, request_shutdown)
    supervisor.monitor()
