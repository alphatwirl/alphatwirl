# Tai Sakuma <tai.sakuma@cern.ch>
from .EventLoopProgressReportWriter import EventLoopProgressReportWriter
import uuid

##__________________________________________________________________||
class EventLoop(object):
    """An event loop
    """
    def __init__(self, build_events, reader):
        self.build_events = build_events
        self.reader = reader
        self.progressReportWriter = EventLoopProgressReportWriter()

        # assign a random unique id to be used by progress bar
        self.taskid = uuid.uuid4()

    def __repr__(self):
        return '{}(build_events = {!r}, reader = {!r}, progressReportWriter = {!r})'.format(
            self.__class__.__name__,
            self.build_events,
            self.reader,
            self.progressReportWriter
        )

    def __call__(self, progressReporter = None):
        events = self.build_events()
        self._reportProgress(progressReporter, events)
        self.reader.begin(events)
        for event in events:
            self._reportProgress(progressReporter, event)
            self.reader.event(event)
        self.reader.end()
        return self.reader

    def _reportProgress(self, progressReporter, event):
        if progressReporter is None: return
        report = self.progressReportWriter.write(self.taskid, event.config, event)
        progressReporter.report(report)

##__________________________________________________________________||
