import itertools
import copy

from .Count import Count

##__________________________________________________________________||
class AllwCount(object):
    """select events that meet all conditions

    """

    def __init__(self, name = None):
        self.name = name if name is not None else 'All'
        self.selections = [ ]
        self.count = Count()

    def __repr__(self):
        return '{}(name = {!r}, selections = {!r}), count = {!r}'.format(
            self.__class__.__name__,
            self.name,
            self.selections,
            self.count
        )

    def add(self, selection):
        self.selections.append(selection)
        self.count.add(selection)

    def begin(self, event):
        for s in self.selections:
            if hasattr(s, 'begin'): s.begin(event)

    def event(self, event):
        ret = True
        pass_ = [ ]
        for s in self.selections:
            pass_.append(s(event))
            if not pass_[-1]:
                ret = False
                break
        self.count.count(pass_)
        return ret

    def __call__(self, event):
        return self.event(event)

    def end(self):
        for s in self.selections:
            if hasattr(s, 'end'): s.end()

    def results(self, increment = False):

        ret = self.count.copy()

        # reversed enumerate
        for i, s in zip(reversed(range(len(self.selections))), reversed(self.selections)):
            if hasattr(s, 'results'):
                ret.insert(i, s.results(increment = True))

        if increment:
            ret.increment_depth(by = 1)

        return ret

##__________________________________________________________________||
class AnywCount(object):
    """select events that meet all conditions

    """

    def __init__(self, name = None):
        self.name = name if name is not None else 'Any'
        self.selections = [ ]
        self.count = Count()

    def __repr__(self):
        return '{}(name = {!r}, selections = {!r}), count = {!r}'.format(
            self.__class__.__name__,
            self.name,
            self.selections,
            self.count
        )

    def add(self, selection):
        self.selections.append(selection)
        self.count.add(selection)

    def begin(self, event):
        for s in self.selections:
            if hasattr(s, 'begin'): s.begin(event)

    def event(self, event):
        ret = False
        pass_ = [ ]
        for s in self.selections:
            pass_.append(s(event))
            if pass_[-1]:
                ret = True
                break
        self.count.count(pass_)
        return ret

    def __call__(self, event):
        return self.event(event)

    def end(self):
        for s in self.selections:
            if hasattr(s, 'end'): s.end()

    def results(self, increment = False):

        ret = self.count.copy()

        # reversed enumerate
        for i, s in zip(reversed(range(len(self.selections))), reversed(self.selections)):
            if hasattr(s, 'results'):
                ret.insert(i, s.results(increment = True))

        if increment:
            ret.increment_depth(by = 1)

        return ret

##__________________________________________________________________||
class NotwCount(object):
    """select events that do NOT pass the selection

    """

    def __init__(self, selection, name = None):
        self.name = name if name is not None else 'Not'
        self.selection = selection
        self.count = Count()
        self.count.add(selection)

    def __repr__(self):
        return '{}(name = {!r}, selection = {!r}), count = {!r}'.format(
            self.__class__.__name__,
            self.name,
            self.selection,
            self.count
        )

    def begin(self, event):
        if hasattr(self.selection, 'begin'): self.selection.begin(event)

    def event(self, event):
        pass_ = self.selection(event)
        self.count.count([pass_])
        return not pass_

    def __call__(self, event):
        return self.event(event)

    def end(self):
        if hasattr(self.selection, 'begin'): self.selection.end()

    def results(self, increment = False):
        ret = self.count.copy()
        if hasattr(self.selection, 'results'):
            ret.insert(0, self.selection.results(increment = True))
        if increment:
            ret.increment_depth(by = 1)
        return ret

##__________________________________________________________________||
