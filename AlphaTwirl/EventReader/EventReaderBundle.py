# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class NullProgressReporter(object):
    def report(self, event, component): pass

##____________________________________________________________________________||
class NullProgressMonitor(object):
    def createReporter(self): return NullProgressReporter()
    def addWorker(self, worker): pass
    def monitor(self): pass

##____________________________________________________________________________||
class EventLoop(object):
    def __init__(self, eventBuilder, component, readers):
        self.eventBuilder = eventBuilder
        self.component = component
        self.readers = readers

    def __call__(self, progressReporter = NullProgressReporter()):
        events = self.eventBuilder.build(self.component)
        for event in events:
            progressReporter.report(event, self.component)
            for reader in self.readers:
                reader.event(event)
        return self.readers

##____________________________________________________________________________||
class EventLoopRunner(object):
    def __init__(self, progressMonitor = None):
        if progressMonitor is None: progressMonitor = NullProgressMonitor()
        self.progressReporter = progressMonitor.createReporter()

    def begin(self): pass

    def run(self, eventLoop):
        eventLoop(self.progressReporter)

    def end(self): pass

##____________________________________________________________________________||
class EventReaderBundle(object):

    def __init__(self, eventBuilder, eventLoopRunner):
        self._eventBuilder = eventBuilder
        self._eventLoopRunner = eventLoopRunner
        self._packages = [ ]

    def addReaderPackage(self, package):
        self._packages.append(package)

    def begin(self):
        self._eventLoopRunner.begin()

    def read(self, component):
        readers = [package.make(component.name) for package in self._packages]
        eventLoop = EventLoop(self._eventBuilder, component, readers)
        self._eventLoopRunner.run(eventLoop)

    def end(self):
        self._eventLoopRunner.end()

        for package in self._packages:
            package.collect()

##____________________________________________________________________________||
