# Tai Sakuma <sakuma@fnal.gov>
from __future__ import print_function
import sys

##____________________________________________________________________________||
class EventReadProgress(object):
    def __init__(self, pernevents = 1000, out = sys.stdout):
        self.pernevents = pernevents
        self.first = True
        self.out = out

    def event(self, event):
        if self.first:
            self.first = False
            self.nEvents = event.nEvents
            self.length = len(str(self.nEvents))

        iEvent = event.iEvent + 1 # add 1 because event.iEvent starts from 0
        if iEvent % self.pernevents == 0 or iEvent == self.nEvents:
            print("{0:{1}} / {2}".format(iEvent, self.length, self.nEvents), file = self.out)

##____________________________________________________________________________||
class EventReadProgressBuilder(object):
    def __init__(self, pernevents = 1000, out = sys.stdout):
        self.pernevents = pernevents
        self.out = out

    def __call__(self):
        return EventReadProgress(pernevents = self.pernevents, out = self.out)

##____________________________________________________________________________||
class EventReadProgressB(object):
    def __init__(self, pernevents = 1000, out = sys.stdout):
        self.pernevents = pernevents
        self.first = True
        self.out = out

    def event(self, event):
        if self.first:
            self.first = False
            self.nEvents = event.nEvents
            self.length = len(str(self.nEvents))
            self.length2 = 2*self.length + len(' / ')
            print("{0:{1}} / {2}".format(1, self.length, self.nEvents), file = self.out, end = '')
            self.out.flush()

        iEvent = event.iEvent + 1 # add 1 because event.iEvent starts from 0
        if iEvent % self.pernevents == 0 or iEvent == self.nEvents:
            print('\b'*self.length2, file = self.out, end = '')
            print("{0:{1}} / {2}".format(iEvent, self.length, self.nEvents), file = self.out, end = '')
            self.out.flush()

        if iEvent == self.nEvents:
            print("", file = self.out)

##____________________________________________________________________________||
class EventReadProgressBBuilder(object):
    def __init__(self, pernevents = 1000, out = sys.stdout):
        self.pernevents = pernevents
        self.out = out

    def __call__(self):
        return EventReadProgressB(pernevents = self.pernevents, out = self.out)

##____________________________________________________________________________||
