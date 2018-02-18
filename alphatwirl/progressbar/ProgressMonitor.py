# Tai Sakuma <tai.sakuma@gmail.com>
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
        self.presentation = presentation
        self.queue = Queue(presentation=presentation)

    def begin(self): pass

    def end(self): pass

    def createReporter(self):
        reporter = ProgressReporter(queue = self.queue)
        return reporter

##__________________________________________________________________||
