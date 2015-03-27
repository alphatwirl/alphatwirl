# Tai Sakuma <tai.sakuma@cern.ch>
from AlphaTwirl.ProgressBar import ProgressReport
from ProgressReportWriter import ProgressReportWriter
from EventLoop import EventLoop

##____________________________________________________________________________||
class AllEvents(object):
    def __call__(self, event): return True

##____________________________________________________________________________||
class EventReaderBundle(object):

    def __init__(self, eventBuilder, eventLoopRunner, eventSelection = None, progressBar = None):
        self._eventBuilder = eventBuilder
        self._eventLoopRunner = eventLoopRunner
        self._packages = [ ]
        self.progressBar = progressBar
        self.eventSelection = eventSelection if eventSelection is not None else AllEvents()

        self.EventLoop = EventLoop

    def addReaderPackage(self, package):
        self._packages.append(package)

    def begin(self):
        self._eventLoopRunner.begin()

    def read(self, component):
        readers = [package.make(component.name) for package in self._packages]
        eventLoop = self.EventLoop(self._eventBuilder, self.eventSelection, component, readers)
        self._eventLoopRunner.run(eventLoop)

    def end(self):
        self._eventLoopRunner.end()
        self._collectResults()

    def _collectResults(self):
        for i, package in enumerate(self._packages):
            if self.progressBar is not None:
                report = ProgressReport(name = "collecting results", done = i + 1, total = len(self._packages))
                self.progressBar.present(report)
            package.collect()

##____________________________________________________________________________||
