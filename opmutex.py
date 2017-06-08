import logging
import threading
import time
from contextlib import contextmanager

log = logging.getLogger("storage")


class OperationMutex(object):

    def __init__(self):
        self._cond = threading.Condition(threading.Lock())
        self._operation = None
        self._holders = 0

    @contextmanager
    def locked(self, operation):
        self._acquire(operation)
        try:
            # Give other threads chance to get in.
            time.sleep(0.01)
            yield self
        finally:
            self._release()

    def _acquire(self, operation):
        with self._cond:
            while self._operation not in (operation, None):
                log.debug("Operation %r is holding the "
                          "mutex, waiting...",
                          self._operation)
                self._cond.wait()
            if self._operation == operation:
                log.debug("Operation %r entered the mutex",
                          operation)
            else:
                log.debug("Operation %r acquired the mutex",
                          operation)
                self._operation = operation
            self._holders += 1

    def _release(self):
        with self._cond:
            self._holders -= 1
            if self._holders == 0:
                log.debug("Operation %r released the mutex",
                          self._operation)
                self._operation = None
                self._cond.notify_all()
            else:
                log.debug("Operation %r exited the mutex",
                          self._operation)
