# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class ReaderComposite(object):

    """A composite of event readers"

    This class is a composite in the composite pattern.

    Examples of event readers are instances of `Summarizer` and this
    class.

    When `event()` is called, it calls `event()` of each reader in the
    order in which the readers are added. If a reader returns `False`,
    it won't call the remaining readers.

    """

    def __init__(self):
        self.readers = []

    def __repr__(self):
        return '{}({!r})'.format(
            self.__class__.__name__,
            self.readers
        )

    def add(self, reader):
        self.readers.append(reader)

    def begin(self, event):
        for reader in self.readers:
            if not hasattr(reader, 'begin'): continue
            reader.begin(event)

    def event(self, event):
        for reader in self.readers:
            if reader.event(event) is False: break

    def merge(self, other):
        for r, o in zip(self.readers, other.readers):
            if not hasattr(r, 'merge'): continue
            r.merge(o)

    def end(self):
        for reader in self.readers:
            if not hasattr(reader, 'end'): continue
            reader.end()

##__________________________________________________________________||
