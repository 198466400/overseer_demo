import subprocess, time, signal
CHECK_INTERVAL = 3
WORKER_NAMES = ['worker-1','worker-2','worker-3']
class Overseer:
    def __init__(self):
        self.workers = {}
    def start_worker(self, name):
        p = subprocess.Popen(['python3','workers.py',name])
        self.workers[name] = p
        print(f'[OVERSEER] started {name} pid={p.pid}')
        return p
    def ensure_workers(self):
        for name in WORKER_NAMES:
            p = self.workers.get(name)
            if p is None or p.poll() is not None:
                print(f'[OVERSEER] {name} dead/missing, restarting')
                self.start_worker(name)
    def monitor(self):
        for name in WORKER_NAMES:
            self.start_worker(name)
        try:
            while True:
                self.ensure_workers()
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print('[OVERSEER] shutting down')
            for p in self.workers.values():
                if p.poll() is None:
                    p.send_signal(signal.SIGINT)
            time.sleep(1)
if __name__ == '__main__':
    Overseer().monitor()
