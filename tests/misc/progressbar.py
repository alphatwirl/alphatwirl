#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import sys
import time, random
import uuid

import alphatwirl

##__________________________________________________________________||
class Task(object):
    def __init__(self, name):
        self.name = name
    def __call__(self):
        progressReporter = alphatwirl.progressbar.progressReporter
        n = random.randint(5, 1000000)
        taskid = uuid.uuid4()
        time.sleep(random.randint(0, 3))
        for i in range(n):
            time.sleep(0.0001)
            report = alphatwirl.progressbar.ProgressReport(name=self.name, done=i + 1, total=n, taskid=taskid)
            progressReporter.report(report)
        return None

##__________________________________________________________________||
progressBar = alphatwirl.progressbar.ProgressBar() if sys.stdout.isatty() else alphatwirl.progressbar.ProgressPrint()

##__________________________________________________________________||
progressMonitor = alphatwirl.progressbar.BProgressMonitor(presentation=progressBar)
dropbox = alphatwirl.concurrently.MultiprocessingDropbox(nprocesses=10, progressMonitor=progressMonitor)
channel = alphatwirl.concurrently.CommunicationChannel(dropbox)
progressMonitor.begin()
channel.begin()
channel.put(Task("loop"))
channel.put(Task("another loop"))
channel.put(Task("more loop"))
channel.put(Task("loop loop loop"))
channel.put(Task("l"))
channel.put(Task("loop6"))
channel.put(Task("loop7"))
channel.put(Task("loop8"))
channel.put(Task("loop6"))
channel.receive()
channel.end()
progressMonitor.end()

##__________________________________________________________________||
