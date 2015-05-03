#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>
from AlphaTwirl.ProgressBar import ProgressBar, MPProgressMonitor, ProgressReport
from AlphaTwirl.EventReader import MPEventLoopRunner
import time, random
import uuid

##____________________________________________________________________________||
class EventLoop(object):
    def __init__(self, name):
        self.name = name
        self.readers = [ ]
    def __call__(self, progressReporter = None):
        n = random.randint(5, 1000000)
        taskid = uuid.uuid4()
        time.sleep(random.randint(0, 3))
        for i in xrange(n):
            time.sleep(0.0001)
            report = ProgressReport(name = self.name, done = i + 1, total = n, taskid = taskid)
            progressReporter.report(report)
        return self.readers
    def firstReportProgress(self, progressReporter): pass

##____________________________________________________________________________||
progressBar = ProgressBar()
progressMonitor = MPProgressMonitor(presentation = progressBar)
runner = MPEventLoopRunner(progressMonitor = progressMonitor)
runner.begin()
runner.run(EventLoop("loop"))
runner.run(EventLoop("another loop"))
runner.run(EventLoop("more loop"))
runner.run(EventLoop("loop loop loop"))
runner.run(EventLoop("l"))
runner.run(EventLoop("loop6"))
runner.run(EventLoop("loop7"))
runner.run(EventLoop("loop8"))
runner.run(EventLoop("loop6"))
runner.end()

##____________________________________________________________________________||
