#!/usr/bin/env python
# Tai Sakuma <sakuma@fnal.gov>
from AlphaTwirl.ProgressBar import ProgressBar, MPProgressMonitor, ProgressReport
from AlphaTwirl.EventReader import MPEventLoopRunner
import time, random

##____________________________________________________________________________||
class EventLoop(object):
    def __init__(self, name):
        self.name = name
        self.readers = [ ]
    def __call__(self, progressReporter = None):
        n = random.randint(5, 50)
        for i in xrange(n):
            time.sleep(0.1)
            report = ProgressReport(name = self.name, done = i + 1, total = n)
            progressReporter.report(report)
        return self.readers

##____________________________________________________________________________||
progressBar = ProgressBar()
progressMonitor = MPProgressMonitor(presentation = progressBar)
runner = MPEventLoopRunner(progressMonitor = progressMonitor)
runner.begin()
runner.run(EventLoop("loop1"))
runner.run(EventLoop("loop2"))
runner.run(EventLoop("loop3"))
runner.run(EventLoop("loop4"))
runner.run(EventLoop("loop5"))
runner.run(EventLoop("loop6"))
runner.run(EventLoop("loop7"))
runner.run(EventLoop("loop8"))
runner.end()

##____________________________________________________________________________||
