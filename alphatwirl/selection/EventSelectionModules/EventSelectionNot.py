# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class EventSelectionNot(object):
    """select events that do NOT pass the selection

    """

    def __init__(self, selection, name = None):
        self.name = name if name is not None else 'Not'
        self.selection = selection

    def __repr__(self):
        return '{}(name = {!r}, selection = {!r})'.format(
            self.__class__.__name__,
            self.name,
            self.selection
        )

    def begin(self, event):
        if hasattr(self.selection, 'begin'): self.selection.begin(event)

    def event(self, event):
        return not self.selection(event)

    def __call__(self, event):
        return self.event(event)

    def end(self):
        if hasattr(self.selection, 'begin'): self.selection.end()

##__________________________________________________________________||
