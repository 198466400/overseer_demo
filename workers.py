import time, os, sys
def worker_main(name):
    pid = os.getpid()
    print(f'[{name}] starting pid={pid}')
    try:
        while True:
            print(f'[{name}] alive pid={pid}')
            time.sleep(2)
    except KeyboardInterrupt:
        print(f'[{name}] exiting')
        sys.exit(0)
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python workers.py <worker-name>')
        sys.exit(1)
    worker_main(sys.argv[1])
