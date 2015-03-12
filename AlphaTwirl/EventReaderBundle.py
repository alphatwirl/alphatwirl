# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class EventLooper(object):
    def read(self, eventBuilder, component, readers):
        events = eventBuilder.build(component)
        for event in events:
            for reader in readers:
                reader.event(event)

    def end(self): pass

##____________________________________________________________________________||
class EventReaderBundle(object):

    def __init__(self, eventBuilder):
        self._eventBuilder = eventBuilder
        self._packages = [ ]

    def addReaderPackage(self, package):
        self._packages.append(package)

    def begin(self):
        self._eventLooper = EventLooper()

    def read(self, component):
        readers = [package.make(component.name) for package in self._packages]
        self._eventLooper.read(self._eventBuilder, component, readers)

    def end(self):
        self._eventLooper.end()

        for package in self._packages:
            package.collect()

##____________________________________________________________________________||
