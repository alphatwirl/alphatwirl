# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class ReaderComposite(object):

    """A composite of event readers"

    This class is a composite in the composite pattern.

    Examples of event readers are instances of `Counter`,
    `ReaderWithEventSelection`, and this class.

    When `event()` is called, it calls `event()` of each reader in the
    order in which the readers are added. If a reader returns `False`,
    it won't call the remaining readers.

    """

    def __init__(self):
        self.readers = []

    def add(self, reader):
        self.readers.append(reader)

    def begin(self, event):
        for reader in self.readers: reader.begin(event)

    def event(self, event):
        for reader in self.readers:
            if reader.event(event) is False: break

    def end(self):
        for reader in self.readers: reader.end()

    def copyFrom(self, src):
        for d, s in zip(self.readers, src.readers):
            if not hasattr(d, 'copyFrom'): continue
            d.copyFrom(s)

##__________________________________________________________________||
