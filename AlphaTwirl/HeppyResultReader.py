# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class HeppyResultReader(object):
    def __init__(self):
        self.readers = [ ]

    def addReader(self, reader):
        self.readers.append(reader)

    def read(self, heppyResult):
        self._begin()
        for component in heppyResult.components():
            self._read_component(component)
        self._end()

    def _begin(self):
        for reader in self.readers:
            reader.begin()

    def _read_component(self, component):
        for reader in self.readers:
            reader.read(component)

    def _end(self):
        for reader in self.readers:
            reader.end()


##____________________________________________________________________________||
