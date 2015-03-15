# Tai Sakuma <sakuma@fnal.gov>
from AlphaTwirl.ProgressBar import ProgressReport

##____________________________________________________________________________||
class ProgressReportWriter(object):
    def write(self, component, event):
        return ProgressReport(name = component.name, done = event.iEvent + 1, total = event.nEvents)

##____________________________________________________________________________||
class EventLoop(object):
    def __init__(self, eventBuilder, component, readers):
        self.eventBuilder = eventBuilder
        self.component = component
        self.readers = readers
        self.progressReportWriter = ProgressReportWriter()

    def __call__(self, progressReporter = None):
        events = self.eventBuilder.build(self.component)
        for event in events:
            self.reportProgress(progressReporter, event)
            for reader in self.readers:
                reader.event(event)
        return self.readers

    def reportProgress(self, progressReporter, event):
        if progressReporter is None: return
        report = self.progressReportWriter.write(self.component, event)
        progressReporter.report(report)

##____________________________________________________________________________||
class EventReaderBundle(object):

    def __init__(self, eventBuilder, eventLoopRunner):
        self._eventBuilder = eventBuilder
        self._eventLoopRunner = eventLoopRunner
        self._packages = [ ]

    def addReaderPackage(self, package):
        self._packages.append(package)

    def begin(self):
        self._eventLoopRunner.begin()

    def read(self, component):
        readers = [package.make(component.name) for package in self._packages]
        eventLoop = EventLoop(self._eventBuilder, component, readers)
        self._eventLoopRunner.run(eventLoop)

    def end(self):
        self._eventLoopRunner.end()

        for package in self._packages:
            package.collect()

##____________________________________________________________________________||
