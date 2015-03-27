# Tai Sakuma <tai.sakuma@cern.ch>
from ProgressReportWriter import ProgressReportWriter

##____________________________________________________________________________||
class EventLoop(object):
    def __init__(self, eventBuilder, eventSelection, component, readers):
        self.eventBuilder = eventBuilder
        self.component = component
        self.readers = readers
        self.progressReportWriter = ProgressReportWriter()
        self.eventSelection = eventSelection

    def __call__(self, progressReporter = None):
        events = self.eventBuilder.build(self.component)
        for event in events:
            self.reportProgress(progressReporter, event)
            if not self.eventSelection(event): continue
            for reader in self.readers:
                reader.event(event)
        return self.readers

    def reportProgress(self, progressReporter, event):
        if progressReporter is None: return
        report = self.progressReportWriter.write(self.component, event)
        progressReporter.report(report)

    def firstReportProgress(self, progressReporter):
        if progressReporter is None: return
        events = self.eventBuilder.build(self.component)
        self.reportProgress(progressReporter, events)

##____________________________________________________________________________||
