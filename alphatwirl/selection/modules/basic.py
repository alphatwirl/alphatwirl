# Tai Sakuma <tai.sakuma@gmail.com>
import itertools

##__________________________________________________________________||
class Base(object):
    """The base class of the classes All and Any

    """

    def __init__(self, name, selections):
        self.name = name
        self.selections = list(selections)

        self._repr_pairs = [
            ('name', self.name),
            ('selections', self.selections),
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
            '{:>{}}:'.format('selections', nwidth),
        ]
        nested_lines = list(itertools.chain(*[str(s).split('\n') for s in self.selections]))
        lines.extend(
            ['{}{}'.format(' '*nwidth_nested, str(l)) for l in nested_lines]
        )
        return '\n'.join(lines)

    def add(self, selection):
        self.selections.append(selection)

    def begin(self, event):
        for s in self.selections:
            if hasattr(s, 'begin'): s.begin(event)

    def event(self, event):
        return self(event)

    def end(self):
        for s in self.selections:
            if hasattr(s, 'end'): s.end()

##__________________________________________________________________||
class All(Base):
    """select events that meet all conditions

    """

    def __init__(self, name='All', selections=[ ]):
        if name is None:
            name = 'All'
        super(All, self).__init__(name, selections)

    def __call__(self, event):
        for s in self.selections:
            if not s(event):
                return False
        return True

##__________________________________________________________________||
class Any(Base):
    """select events that meet any of the conditions

    """

    def __init__(self, name='Any', selections=[ ]):
        if name is None:
            name = 'Any'
        super(Any, self).__init__(name, selections)

    def __call__(self, event):
        for s in self.selections:
            if s(event):
                return True
        return False

##__________________________________________________________________||
class Not(object):
    """select events that do NOT pass the selection

    """

    def __init__(self, selection, name='Not'):
        if name is None:
            name = 'Not'
        self.name = name
        self.selection = selection

    def __repr__(self):
        return '{}(name={!r}, selection={!r})'.format(
            self.__class__.__name__,
            self.name,
            self.selection
        )

    def begin(self, event):
        if hasattr(self.selection, 'begin'):
            self.selection.begin(event)

    def __call__(self, event):
        return not self.selection(event)

    def event(self, event):
        return self(event)

    def end(self):
        if hasattr(self.selection, 'end'):
            self.selection.end()

##__________________________________________________________________||
