# Tai Sakuma <tai.sakuma@cern.ch>
from EventLoop import EventLoop
from EventReaderPackageBundle import EventReaderPackageBundle

##____________________________________________________________________________||
class AllEvents(object):
    def __call__(self, event): return True

##____________________________________________________________________________||
class EventReaderBundle(object):

    def __init__(self, eventBuilder, eventLoopRunner, eventSelection = None, progressBar = None):
        self._eventBuilder = eventBuilder
        self._eventLoopRunner = eventLoopRunner
        self._packageBundle = EventReaderPackageBundle(progressBar)
        self.progressBar = progressBar
        self.eventSelection = eventSelection if eventSelection is not None else AllEvents()

        self.EventLoop = EventLoop

    def addReaderPackage(self, package):
        self._packageBundle.add(package)

    def begin(self):
        self._eventLoopRunner.begin()

    def read(self, component):
        readers = self._packageBundle.make(component.name)
        eventLoop = self.EventLoop(self._eventBuilder, self.eventSelection, component, readers)
        self._eventLoopRunner.run(eventLoop)

    def end(self):
        self._eventLoopRunner.end()
        self._collectResults()

    def _collectResults(self):
        self._packageBundle.collect()

##____________________________________________________________________________||
