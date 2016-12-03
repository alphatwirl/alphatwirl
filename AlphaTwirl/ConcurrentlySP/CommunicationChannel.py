# Tai Sakuma <tai.sakuma@cern.ch>
import logging

from ..ProgressBar import NullProgressMonitor
from .TaskPackage import TaskPackage

##__________________________________________________________________||
class CommunicationChannel(object):
    """A communication channel to a concurrent task running system.

    """
    def __init__(self, dropbox, progressMonitor = None):
        self.progressMonitor = NullProgressMonitor() if progressMonitor is None else progressMonitor
        self.dropbox = dropbox
        self.isopen = False

    def begin(self):
        if self.isopen: return
        self.dropbox.open()
        self.isopen = True

    def put(self, task, *args, **kwargs):
        if not self.isopen:
            logger = logging.getLogger(__name__)
            logger.warning('the drop box is not open')
            return

        package = TaskPackage(
            task = task,
            progressReporter = self.progressMonitor.createReporter(),
            args = args,
            kwargs =  kwargs
        )
        self.dropbox.put(package)

    def receive(self):
        if not self.isopen:
            logger = logging.getLogger(__name__)
            logger.warning('the drop box is not open')
            return

        results = self.dropbox.receive()
        return results

    def end(self):
        if not self.isopen: return
        self.dropbox.close()
        self.isopen = False

##__________________________________________________________________||
