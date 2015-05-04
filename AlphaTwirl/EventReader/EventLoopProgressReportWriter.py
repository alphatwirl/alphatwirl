# Tai Sakuma <tai.sakuma@cern.ch>
from ..ProgressBar import ProgressReport

##____________________________________________________________________________||
class EventLoopProgressReportWriter(object):
    def write(self, taskid, component, event):
        return ProgressReport(
            name = component.name,
            done = event.iEvent + 1,
            total = event.nEvents,
            taskid = taskid
        )

##____________________________________________________________________________||
