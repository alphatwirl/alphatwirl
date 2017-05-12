# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class All(object):
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
class Any(object):
    """select events that meet any of the conditions

    """

    def __init__(self, name = None):
        self.name = name if name is not None else 'Any'
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
            if s(event): return True
        return False

    def __call__(self, event):
        return self.event(event)

    def end(self):
        for s in self.selections:
            if hasattr(s, 'end'): s.end()

##__________________________________________________________________||
class Not(object):
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
