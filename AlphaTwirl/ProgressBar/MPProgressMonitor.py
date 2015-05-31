# Tai Sakuma <tai.sakuma@cern.ch>
import multiprocessing
import time
from ProgressReporter import ProgressReporter

##__________________________________________________________________||
class MPProgressMonitor(object):
    """A progress monitor of tasks concurrently executed

    This class has been deprecated and replaced with `BProgressMonitor`.

    """
    def __init__(self, presentation):
        self.queue = multiprocessing.Queue()
        self._presentation = presentation
        self.interval = 0.1 # [second]
        self.lastWaitTime = 1.0 # [second]
        self._readTime()

    def monitor(self):
        if self._time() - self.lastTime < self.interval: return
        self._readTime()
        self._present()

    def last(self):
        start = self._time()
        while self._presentation.nreports() > 0:
            if self._time() - start > self.lastWaitTime: break
            self._present()

    def _present(self):
        while not self.queue.empty():
            report = self.queue.get()
            self._presentation.present(report)

    def _time(self):
        return time.time()

    def _readTime(self):
        self.lastTime = self._time()

    def createReporter(self):
        return ProgressReporter(self.queue)

##__________________________________________________________________||
