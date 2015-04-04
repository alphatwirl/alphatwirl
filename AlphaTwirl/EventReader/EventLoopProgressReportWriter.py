# Tai Sakuma <tai.sakuma@cern.ch>
from AlphaTwirl.ProgressBar import ProgressReport

##____________________________________________________________________________||
class EventLoopProgressReportWriter(object):
    def write(self, component, event):
        return ProgressReport(name = component.name, done = event.iEvent + 1, total = event.nEvents)

##____________________________________________________________________________||
