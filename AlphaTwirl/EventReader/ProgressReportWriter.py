# Tai Sakuma <sakuma@fnal.gov>
from AlphaTwirl.ProgressBar import ProgressReport

##____________________________________________________________________________||
class ProgressReportWriter(object):
    def write(self, component, event):
        return ProgressReport(name = component.name, done = event.iEvent + 1, total = event.nEvents)

##____________________________________________________________________________||
