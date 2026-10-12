import time
import threading
import os

CHECK_INTERVAL = 3
WORKER_NAMES = ['worker-1','worker-2','worker-3']

class Worker(threading.Thread):
    def __init__(self, name):
        super().__init__(daemon=True)
        self.name = name
        self.alive = True
        self.pid = os.getpid()

    def run(self):
        print(f'[{self.name}] starting pid={self.pid}', flush=True)
        while self.alive:
            print(f'[{self.name}] alive pid={self.pid}', flush=True)
            time.sleep(2)
        print(f'[{self.name}] exiting', flush=True)

class Overseer:
    def __init__(self):
        self.workers = {}

    def start_worker(self, name):
        w = Worker(name)
        w.start()
        self.workers[name] = w
        print(f'[OVERSEER] started {name}', flush=True)
        return w

    def kill_worker(self, name):
        w = self.workers.get(name)
        if w:
            w.alive = False
            print(f'[OVERSEER] killed {name}', flush=True)

    def ensure_workers(self):
        for name in WORKER_NAMES:
            w = self.workers.get(name)
            if w is None or not w.is_alive():
                print(f'[OVERSEER] {name} dead/missing, restarting', flush=True)
                self.start_worker(name)

    def monitor(self):
        for name in WORKER_NAMES:
            self.start_worker(name)

        time.sleep(5)
        self.kill_worker('worker-1')

        try:
            while True:
                self.ensure_workers()
                print('[OVERSEER] heartbeat', flush=True)
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print('[OVERSEER] shutting down', flush=True)
            for w in self.workers.values():
                w.alive = False
            time.sleep(1)

if __name__ == '__main__':
    Overseer().monitor()

