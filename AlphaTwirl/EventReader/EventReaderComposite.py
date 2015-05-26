# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class EventReaderComposite(object):

    """A composite of event readers"

    This class is a composite in the composite pattern.

    An example of event readers is Counter.

    """

    def __init__(self):
        self.readers = []

    def add(self, reader):
        self.readers.append(reader)

    def begin(self, event):
        for reader in self.readers: reader.begin(event)

    def event(self, event):
        for reader in self.readers: reader.event(event)

    def end(self):
        for reader in self.readers: reader.end()

    def setResults(self, results):
        for reader, result in zip(self.readers, results):
            reader.setResults(result)

    def results(self):
        return [reader.results() for reader in self.readers]

##__________________________________________________________________||
