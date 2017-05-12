# Tai Sakuma <tai.sakuma@cern.ch>

import copy

from .Count import Count

##__________________________________________________________________||
class EventSelectionNotCount(object):
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

    def copy_from(self, src):
        src = copy.deepcopy(src)
        self.count = src.count
        if hasattr(self.selection, 'copy_from'):
            self.selection.copy_from(src.selection)

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
