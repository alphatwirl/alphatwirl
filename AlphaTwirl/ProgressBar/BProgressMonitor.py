# Tai Sakuma <tai.sakuma@cern.ch>
from .ProgressReporter import ProgressReporter
from .ProgressReportPickup import ProgressReportPickup

import multiprocessing

##__________________________________________________________________||
class BProgressMonitor(object):
    def __init__(self, presentation):
        self.queue = multiprocessing.Queue()
        self.presentation = presentation

    def begin(self):
        self.bg = ProgressReportPickup(self.queue, self.presentation)
        self.bg.start()

    def end(self):
        self.queue.put(None)
        self.bg.join()

    def createReporter(self):
        return ProgressReporter(self.queue)

##__________________________________________________________________||
