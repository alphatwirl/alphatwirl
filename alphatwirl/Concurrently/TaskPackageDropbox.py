# Tai Sakuma <tai.sakuma@cern.ch>
import logging

from .WorkingArea import WorkingArea

##__________________________________________________________________||
class TaskPackageDropbox(object):
    """A drop box for task packages.

    It puts task packages in a working area and dispatches runners
    that execute the tasks.

    """
    def __init__(self, workingArea, dispatcher):
        self.workingArea = workingArea
        self.dispatcher = dispatcher

    def open(self):
        self.workingArea.open()
        self.package_indices = [ ]

    def put(self, package):
        package_index, package_path = self.workingArea.put_package(package)
        self.package_indices.append(package_index)
        self.dispatcher.run(self.workingArea.path, package_path)

    def receive(self):
        try:
            self.dispatcher.wait()
        except KeyboardInterrupt:
            logger = logging.getLogger(__name__)
            logger.warning('received KeyboardInterrupt')
            self.dispatcher.terminate()

        results = [self.workingArea.collect_result(i) for i in self.package_indices]
        self.package_indices[:] = [ ]
        return results

    def close(self):
        self.dispatcher.terminate()
        self.workingArea.close()

##__________________________________________________________________||
