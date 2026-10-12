import subprocess, time, os, signal
def test_worker_restart():
    o = subprocess.Popen(['python3','overseer.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    time.sleep(5)
    pid = None
    start = time.time()
    while time.time() - start < 5:
        line = o.stdout.readline()
        if not line:
            break
        if 'started worker-1 pid=' in line:
            pid = int(line.strip().split('pid=')[-1])
            break
    assert pid is not None
    os.kill(pid, signal.SIGKILL)
    print(f'[TEST] killed worker-1 pid={pid}')
    restarted = False
    start = time.time()
    while time.time() - start < 20:
        line = o.stdout.readline()
        if not line:
            break
        if 'restarting' in line:
            restarted = True
            break
    o.send_signal(signal.SIGINT)
    time.sleep(1)
    assert restarted
    print('[TEST] passed')
if __name__ == '__main__':
    test_worker_restart()
