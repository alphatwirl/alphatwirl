# Tai Sakuma <tai.sakuma@cern.ch>
from .ProgressReporter import ProgressReporter

##__________________________________________________________________||
class Queue(object):

    def __init__(self, presentation):
        self.presentation = presentation

    def put(self, report):
        self.presentation.present(report)

##__________________________________________________________________||
class ProgressMonitor(object):
    def __init__(self, presentation):
        self.queue = Queue(presentation = presentation)

    def begin(self): pass

    def end(self): pass

    def createReporter(self):
        reporter = ProgressReporter(self.queue)
        return reporter

##__________________________________________________________________||
