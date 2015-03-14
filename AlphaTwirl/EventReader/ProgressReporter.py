# Tai Sakuma <sakuma@fnal.gov>
import multiprocessing
import time

from ProgressReport import ProgressReport

##____________________________________________________________________________||
class ProgressReporter(object):
    def __init__(self, queue, pernevents = 1000):
        self.queue = queue
        self.pernevents = pernevents
        self.interval = 0.02 # [second]
        self._readTime()

    def report(self, event, component):
        if not self.needToReport(event, component): return
        done = event.iEvent + 1
        report = ProgressReport(name = component.name, done = done, total = event.nEvents)
        self.queue.put(report)
        self._readTime()

    def needToReport(self, event, component):
        iEvent = event.iEvent + 1 # add 1 because event.iEvent starts from 0
        if self._time() - self.lastTime > self.interval: return True
        if iEvent % self.pernevents == 0: return True
        if iEvent == event.nEvents: return True
        return False

    def _time(self): return time.time()
    def _readTime(self): self.lastTime = self._time()

##____________________________________________________________________________||
