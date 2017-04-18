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
            sleep = 5
            while self.runid_package_index_map:

                finished_runid = self.dispatcher.poll()
                # e.g., [1001, 1003]

                package_indices = [self.runid_package_index_map.pop(i) for i in finished_runid]
                # e.g., [0, 2]

                pairs = [(i, self.workingArea.collect_result(i)) for i in package_indices]
                # e.g., [(0, result0), (2, None)] # None indicates the job failed

                failed_package_indices = [i for i, r in pairs if r is None]
                # e.g., [2]

                pairs = [(i, r) for i, r in pairs if i not in failed_package_indices]
                # e.g., [(0, result0)] # only successful ones

                # rerun failed jobs
                for package_index in failed_package_indices:
                    logger = logging.getLogger(__name__)
                    logger.warning('resubmitting {}'.format(self.workingArea.package_path(package_index)))

                    runid = self.dispatcher.run(self.workingArea, package_index)
                    self.runid_package_index_map[runid] = package_index

                package_index_result_pairs.extend(pairs)

                time.sleep(sleep)

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
