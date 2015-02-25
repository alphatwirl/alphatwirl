# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
class EventReaderBundle(object):

    def __init__(self, eventBuilder):
        self._eventBuilder = eventBuilder
        self._packages = [ ]

    def addReaderPackage(self, package):
        self._packages.append(package)

    def begin(self):
        pass

    def read(self, component):

        readers = [ ]
        for package in self._packages:
            reader = package.make(component.name)
            readers.append(reader)

        events = self._eventBuilder.build(component)
        for event in events:
            for reader in readers:
                reader.event(event)

    def end(self):
        for package in self._packages:
            package.collect()

##____________________________________________________________________________||
