# Tai Sakuma <tai.sakuma@gmail.com>
from ..progressbar import ProgressReport

##__________________________________________________________________||
class EventLoopProgressReportWriter(object):
    """A progress report writer of an event loop

    """
    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__
        )

    def write(self, taskid, config, event):
        return ProgressReport(
            name = config.name,
            done = event.iEvent + 1,
            total = event.nEvents,
            taskid = taskid
        )

##__________________________________________________________________||
