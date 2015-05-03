# Tai Sakuma <tai.sakuma@cern.ch>
from EventLoopProgressReportWriter import EventLoopProgressReportWriter
import uuid

##____________________________________________________________________________||
class EventLoop(object):
    def __init__(self, eventBuilder, eventSelection, component, readers):
        self.eventBuilder = eventBuilder
        self.component = component
        self.readers = readers
        self.progressReportWriter = EventLoopProgressReportWriter()
        self.eventSelection = eventSelection

        # assign a random unique id to be used by progress bar
        self.taskid = uuid.uuid4()

    def __call__(self, progressReporter = None):
        events = self.eventBuilder.build(self.component)
        self.reportProgress(progressReporter, events)
        for event in events:
            self.reportProgress(progressReporter, event)
            if not self.eventSelection(event): continue
            for reader in self.readers:
                reader.event(event)
        return self.readers

    def reportProgress(self, progressReporter, event):
        if progressReporter is None: return
        report = self.progressReportWriter.write(self.taskid, self.component, event)
        progressReporter.report(report)

##____________________________________________________________________________||
