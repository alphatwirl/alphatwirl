# Tai Sakuma <tai.sakuma@gmail.com>
from alphatwirl.misc.deprecation import _renamed_class_method_option
from atpbar import atpbar

##__________________________________________________________________||
class EventLoop(object):
    """An event loop

    Args:
        build_events: A picklable function to create events.
        reader: An event reader. This must be picklable before
            `begin()` is called and after `end` is called.
        progressbar_label (optional): a label shown by the progress
            bar

    """
    @_renamed_class_method_option(old='name', new='progressbar_label')
    def __init__(self, build_events, reader, progressbar_label=None):
        self.build_events = build_events
        self.reader = reader

        ##
        if progressbar_label is None:
            self.progressbar_label = self.__class__.__name__
        else:
            self.progressbar_label = progressbar_label

        ##
        name_value_pairs = (
            ('build_events', self.build_events),
            ('reader', self.reader),
            ('progressbar_label', self.progressbar_label),
        )
        self._repr = '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]))

    def __repr__(self):
        return self._repr

    def __call__(self):
        events = self.build_events()
        self.reader.begin(events)
        for event in atpbar(events, name=self.progressbar_label):
            self.reader.event(event)
        self.reader.end()
        return self.reader

##__________________________________________________________________||
