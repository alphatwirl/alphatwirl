# Tai Sakuma <tai.sakuma@cern.ch>
import logging
from operator import itemgetter

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

    def __repr__(self):
        return '{}(workingArea = {!r}, dispatcher = {!r})'.format(
            self.__class__.__name__,
            self.workingArea,
            self.dispatcher
        )

    def open(self):
        self.workingArea.open()
        self.runid_package_index_map = { }

    def put(self, package):
        package_index = self.workingArea.put_package(package)
        runid = self.dispatcher.run(self.workingArea, package_index)
        self.runid_package_index_map[runid] = package_index

    def receive(self):
        package_index_result_pairs = [ ] # a list of (package_index, _result)
        try:
            while self.runid_package_index_map:
                finished_runid = self.dispatcher.poll()
                package_indices = [self.runid_package_index_map.pop(i) for i in finished_runid]
                pairs = [(i, self.workingArea.collect_result(i)) for i in package_indices]
                package_index_result_pairs.extend(pairs)
        except KeyboardInterrupt:
            logger = logging.getLogger(__name__)
            logger.warning('received KeyboardInterrupt')
            self.dispatcher.terminate()

        # sort in the order of package_index
        package_index_result_pairs = sorted(package_index_result_pairs, key = itemgetter(0))

        results = [result for i, result in package_index_result_pairs]
        return results

    def close(self):
        self.dispatcher.terminate()
        self.workingArea.close()

##__________________________________________________________________||
