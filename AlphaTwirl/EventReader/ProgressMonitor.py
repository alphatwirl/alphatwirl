# Tai Sakuma <sakuma@fnal.gov>
import multiprocessing
import time

from ProgressReport import ProgressReport

##____________________________________________________________________________||
class ProgressReporter(object):
    def __init__(self, queue, pernevents = 1000):
        self.queue = queue
        self.pernevents = pernevents
        self.lastReportTime = time.time()

    def report(self, event, component):
        if not self.needToReport(event, component): return
        done = event.iEvent + 1
        report = ProgressReport(name = component.name, done = done, total = event.nEvents)
        self.queue.put(report)
        self.lastReportTime = time.time()

    def needToReport(self, event, component):
        iEvent = event.iEvent + 1 # add 1 because event.iEvent starts from 0
        if time.time() - self.lastReportTime > 0.02: return True
        if iEvent % self.pernevents == 0: return True
        if iEvent == event.nEvents: return True
        return False

##____________________________________________________________________________||
class Queue(object):

    def __init__(self, presentation):
        self.presentation = presentation

    def put(self, report):
        self.presentation.present(report)

##____________________________________________________________________________||
class ProgressMonitor(object):
    def __init__(self, presentation):
        self.queue = Queue(presentation = presentation)

    def monitor(self): pass

    def createReporter(self):
        reporter = ProgressReporter(self.queue)
        return reporter

##____________________________________________________________________________||
class MPProgressMonitor(object):
    def __init__(self, presentation):
        self.queue = multiprocessing.Queue()
        self._workers = [ ]
        self._presentation = presentation

    def addWorker(self, worker):
        self._workers.append(worker)

    def monitor(self):
        while any(i.is_alive() for i in self._workers):
            time.sleep(0.1)
            while not self.queue.empty():
                report = self.queue.get()
                self._presentation.present(report)

    def createReporter(self):
        return ProgressReporter(self.queue)

##____________________________________________________________________________||