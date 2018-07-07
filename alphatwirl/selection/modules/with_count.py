import itertools
import copy

from .Count import Count

##__________________________________________________________________||
class WithCountBase(object):
    """The base class of the classes AllwCount and AnywCount

    """

    def __init__(self, name, selections):
        self.name = name
        self.selections = list(selections)
        self.count = Count()

        self._repr_pairs = [
            ('name', self.name),
            ('selections', self.selections),
            ('count', self.count),
        ]

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in self._repr_pairs]),
        )

    def __str__(self):
        nwidth = max(len(n) for n, _ in self._repr_pairs)
        nwidth += 4
        nwidth_nested = 12
        lines = [
            '{}:'.format(self.__class__.__name__),
            '{:>{}}: {!r}'.format('name', nwidth, self.name),
            '{:>{}}: {!r}'.format('count', nwidth, self.count),
            '{:>{}}:'.format('selections', nwidth),
        ]
        nested_lines = list(itertools.chain(*[str(s).split('\n') for s in self.selections]))
        lines.extend(
            ['{}{}'.format(' '*nwidth_nested, str(l)) for l in nested_lines]
        )
        return '\n'.join(lines)

    def add(self, selection):
        self.selections.append(selection)
        self.count.add(selection)

    def begin(self, event):
        for s in self.selections:
            if hasattr(s, 'begin'): s.begin(event)

    def event(self, event):
        return self(event)

    def end(self):
        for s in self.selections:
            if hasattr(s, 'end'): s.end()

    def merge(self, other):
        self.count += other.count
        for s, o in zip(self.selections, other.selections):
            if not hasattr(s, 'merge'):
                continue
            s.merge(o)

    def results(self, increment=False):

        ret = self.count.copy()

        # reversed enumerate
        for i, s in zip(reversed(range(len(self.selections))), reversed(self.selections)):
            if hasattr(s, 'results'):
                ret.insert(i, s.results(increment=True))

        if increment:
            ret.increment_depth(by=1)

        return ret

##__________________________________________________________________||
class AllwCount(WithCountBase):
    """select events that meet all conditions

    """

    def __init__(self, name='All', selections=[ ]):
        if name is None:
            name = 'All'
        super(AllwCount, self).__init__(name, selections)

    def __call__(self, event):
        ret = True
        pass_ = [ ]
        for s in self.selections:
            pass_.append(s(event))
            if not pass_[-1]:
                ret = False
                break
        self.count.count(pass_)
        return ret

##__________________________________________________________________||
class AnywCount(WithCountBase):
    """select events that meet any of the conditions

    """

    def __init__(self, name='Any', selections=[ ]):
        if name is None:
            name = 'Any'
        super(AnywCount, self).__init__(name, selections)

    def __call__(self, event):
        ret = False
        pass_ = [ ]
        for s in self.selections:
            pass_.append(s(event))
            if pass_[-1]:
                ret = True
                break
        self.count.count(pass_)
        return ret

##__________________________________________________________________||
class NotwCount(object):
    """select events that do NOT pass the selection

    """

    def __init__(self, selection, name='Not'):
        if name is None:
            name = 'Not'
        self.name = name
        self.selection = selection
        self.count = Count()
        self.count.add(selection)

    def __repr__(self):
        return '{}(name={!r}, selection={!r}), count={!r}'.format(
            self.__class__.__name__,
            self.name,
            self.selection,
            self.count
        )

    def begin(self, event):
        if hasattr(self.selection, 'begin'): self.selection.begin(event)

    def __call__(self, event):
        pass_ = self.selection(event)
        self.count.count([pass_])
        return not pass_

    def event(self, event):
        return self(event)

    def end(self):
        if hasattr(self.selection, 'end'): self.selection.end()

    def merge(self, other):
        self.count += other.count
        if not hasattr(self.selection, 'merge'):
            return
        self.selection.merge(other.selection)

    def results(self, increment=False):
        ret = self.count.copy()
        if hasattr(self.selection, 'results'):
            ret.insert(0, self.selection.results(increment=True))
        if increment:
            ret.increment_depth(by=1)
        return ret

##__________________________________________________________________||
