# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class EventReaderComposite(object):

    """A composite of event readers"

    This class is a composite in the composite pattern.

    Examples of event readers are instances of `Counter`, and this
    class.

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

    def copyFrom(self, src):
        for d, s in zip(self.readers, src.readers):
            d.copyFrom(s)

##__________________________________________________________________||
