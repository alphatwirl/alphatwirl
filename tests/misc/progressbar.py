#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import sys
import time, random
import uuid

import argparse

import alphatwirl

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('--parallel-mode', default='multiprocessing', choices=['multiprocessing', 'subprocess', 'htcondor'], help='mode for concurrency')
parser.add_argument('-p', '--process', default=16, type=int, help='number of processes to run in parallel')
parser.add_argument('-q', '--quiet', default=False, action='store_true', help='quiet mode')
args = parser.parse_args()

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
parallel = alphatwirl.parallel.build_parallel(
    parallel_mode=args.parallel_mode,
    quiet=args.quiet,
    processes=args.process
)

##__________________________________________________________________||
parallel.begin()
parallel.communicationChannel.put(Task("loop"))
parallel.communicationChannel.put(Task("another loop"))
parallel.communicationChannel.put(Task("more loop"))
parallel.communicationChannel.put(Task("loop loop loop"))
parallel.communicationChannel.put(Task("l"))
parallel.communicationChannel.put(Task("loop6"))
parallel.communicationChannel.put(Task("loop7"))
parallel.communicationChannel.put(Task("loop8"))
parallel.communicationChannel.put(Task("loop6"))
parallel.communicationChannel.receive()
parallel.end()

##__________________________________________________________________||
