# Tai Sakuma <tai.sakuma@cern.ch>
import time
from ProgressReport import ProgressReport

##__________________________________________________________________||
class ProgressReporter(object):
    def __init__(self, queue):
        self.queue = queue
        self.interval = 0.02 # [second]
        self._readTime()

    def report(self, report):
        if not self.needToReport(report): return
        self._report(report)

    def _report(self, report):
        self.queue.put(report)
        self._readTime()

    def needToReport(self, report):
        if self._time() - self.lastTime > self.interval: return True
        if report.done == report.total: return True
        return False

    def _time(self): return time.time()
    def _readTime(self): self.lastTime = self._time()

##__________________________________________________________________||
