# Tai Sakuma <tai.sakuma@gmail.com>
import uuid

import alphatwirl

from ..progressbar import ProgressReport

##__________________________________________________________________||
class EventLoop(object):
    """An event loop
    """
    def __init__(self, build_events, reader, name=None):
        self.build_events = build_events
        self.reader = reader

        if name is None:
            self.name = self.__class__.__name__
        else:
            self.name = name

        # assign a random unique id to be used by progress bar
        self.taskid = uuid.uuid4()

    def __repr__(self):
        name_value_pairs = (
            ('build_events', self.build_events),
            ('reader',       self.reader),
            ('name',         self.name),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __call__(self):
        events = self.build_events()
        self.nevents = len(events)
        self._report_progress(0)
        self.reader.begin(events)
        for i, event in enumerate(events):
            self._report_progress(i+1)
            self.reader.event(event)
        self.reader.end()
        return self.reader

    def _report_progress(self, i):
        try:
            report = ProgressReport(
                name=self.name, done=(i),
                total=self.nevents, taskid=self.taskid
            )
            alphatwirl.progressbar.report_progress(report)
        except:
            pass

##__________________________________________________________________||
