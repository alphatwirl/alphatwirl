
##__________________________________________________________________||
class EventSelectionAll(object):
    """select events that meet all conditions

    """

    def __init__(self, name = None):
        self.name = name if name is not None else 'All'
        self.selections = [ ]

    def __repr__(self):
        return '{}(name = {!r}, selections = {!r})'.format(
            self.__class__.__name__,
            self.name,
            self.selections
        )

    def add(self, selection):
        self.selections.append(selection)

    def begin(self, event):
        for s in self.selections:
            if hasattr(s, 'begin'): s.begin(event)

    def event(self, event):
        for s in self.selections:
            if not s(event): return False
        return True

    def __call__(self, event):
        return self.event(event)

    def end(self):
        for s in self.selections:
            if hasattr(s, 'end'): s.end()

##__________________________________________________________________||
