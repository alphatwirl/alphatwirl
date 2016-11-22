# Tai Sakuma <tai.sakuma@cern.ch>
from EventLoopProgressReportWriter import EventLoopProgressReportWriter
import uuid

##__________________________________________________________________||
class EventLoop(object):
    """An event loop
    """
    def __init__(self, eventBuilder, chunk, reader):
        self.eventBuilder = eventBuilder
        self.chunk = chunk
        self.reader = reader
        self.progressReportWriter = EventLoopProgressReportWriter()

        # assign a random unique id to be used by progress bar
        self.taskid = uuid.uuid4()

    def __call__(self, progressReporter = None):
        events = self.eventBuilder.build(self.chunk)
        self._reportProgress(progressReporter, events)
        self.reader.begin(events)
        for event in events:
            self._reportProgress(progressReporter, event)
            self.reader.event(event)
        self.reader.end()
        return self.reader

    def _reportProgress(self, progressReporter, event):
        if progressReporter is None: return
        report = self.progressReportWriter.write(self.taskid, self.chunk, event)
        progressReporter.report(report)

##__________________________________________________________________||
