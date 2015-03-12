# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class EventLooper(object):
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
class EventLooperRunner(object):
    def begin(self): pass

    def read(self, eventBuilder, component, readers):
        task = EventLooper(eventBuilder, component, readers)
        task()

    def end(self): pass

##____________________________________________________________________________||
class EventReaderBundle(object):

    def __init__(self, eventBuilder, eventLooperRunner):
        self._eventBuilder = eventBuilder
        self._eventLooperRunner = eventLooperRunner
        self._packages = [ ]

    def addReaderPackage(self, package):
        self._packages.append(package)

    def begin(self):
        self._eventLooperRunner.begin()

    def read(self, component):
        readers = [package.make(component.name) for package in self._packages]
        self._eventLooperRunner.read(self._eventBuilder, component, readers)

    def end(self):
        self._eventLooperRunner.end()

        for package in self._packages:
            package.collect()

##____________________________________________________________________________||
