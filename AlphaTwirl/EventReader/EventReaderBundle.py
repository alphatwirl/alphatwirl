# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class EventLoop(object):
    def __init__(self, eventBuilder, component, readers):
        self.eventBuilder = eventBuilder
        self.component = component
        self.readers = readers

    def __call__(self):
        events = self.eventBuilder.build(self.component)
        for event in events:
            for reader in self.readers:
                reader.event(event)
        return self.readers

##____________________________________________________________________________||
class EventLoopRunner(object):
    def begin(self): pass

    def read(self, eventBuilder, component, readers):
        task = EventLoop(eventBuilder, component, readers)
        task()

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
        self._eventLoopRunner.read(self._eventBuilder, component, readers)

    def end(self):
        self._eventLoopRunner.end()

        for package in self._packages:
            package.collect()

##____________________________________________________________________________||
