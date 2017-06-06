import logging
import threading
import time
import pytest

import opmutex

logging.basicConfig(
    level=logging.DEBUG,
    format="%(threadName)s: %(message)s")


def test_same_operation():
    m = opmutex.OperationMutex()

    def worker(n):
        with m.locked("operation"):
            time.sleep(1.0)

    elapsed = run_threads(worker, 50)

    assert elapsed < 2.0


@pytest.mark.parametrize("run", range(10))
def test_refresh_flow(run):
    count = 50
    m = opmutex.OperationMutex()
    cache = ["old"] * count

    def worker(n):
        with m.locked("invalidate"):
            cache[n] = "invalid"
        with m.locked("reload"):
            time.sleep(1.0)
            cache[n] = "new"

    elapsed = run_threads(worker, count)

    assert elapsed < 2.0
    assert cache == ["new"] * count


def run_threads(func, count):
    threads = []
    start = time.time()
    try:
        for i in range(count):
            t = threading.Thread(target=func,
                                 args=(i,),
                                 name="worker-%02d" % i)
            t.daemon = True
            t.start()
            threads.append(t)
    finally:
        for t in threads:
            t.join()
    return time.time() - start
