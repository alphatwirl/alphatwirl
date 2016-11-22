# Tai Sakuma <tai.sakuma@cern.ch>
from ..ProgressBar import ProgressReport

##__________________________________________________________________||
class EventLoopProgressReportWriter(object):
    """A progress report writer of an event loop

    """
    def write(self, taskid, chunk, event):
        return ProgressReport(
            name = chunk.name,
            done = event.iEvent + 1,
            total = event.nEvents,
            taskid = taskid
        )

##__________________________________________________________________||
