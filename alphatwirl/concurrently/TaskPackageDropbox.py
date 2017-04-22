# Tai Sakuma <tai.sakuma@cern.ch>
import logging
import time
from operator import itemgetter

from .WorkingArea import WorkingArea

##__________________________________________________________________||
class TaskPackageDropbox(object):
    """A drop box for task packages.

    It puts task packages in a working area and dispatches runners
    that execute the tasks.

    """
    def __init__(self, workingArea, dispatcher, sleep = 5):
        self.workingArea = workingArea
        self.dispatcher = dispatcher
        self.sleep = sleep

    def __repr__(self):
        return '{}(workingArea = {!r}, dispatcher = {!r}, sleep = {!r})'.format(
            self.__class__.__name__,
            self.workingArea,
            self.dispatcher,
            self.sleep
        )

    def open(self):
        self.workingArea.open()
        self.runid_package_index_map = { }

    def put(self, package):
        package_index = self.workingArea.put_package(package)
        runid = self.dispatcher.run(self.workingArea, package_index)
        self.runid_package_index_map[runid] = package_index

    def receive(self):
        pkgidx_result_pairs = [ ] # a list of (package_index, _result)
        try:
            while self.runid_package_index_map:

                finished_runid = self.dispatcher.poll()
                # e.g., [1001, 1003]

                runid_pkgidx = [(i, self.runid_package_index_map.pop(i)) for i in finished_runid]
                # e.g., [(1001, 0), (1003, 2)]

                runid_pkgidx_result = [(ri, pi, self.workingArea.collect_result(pi)) for ri, pi in runid_pkgidx]
                # e.g., [(1001, 0, result0), (1003, 2, None)] # None indicates the job failed

                failed = [e for e in runid_pkgidx_result if e[2] is None]
                # e.g., [(1003, 2, None)]

                succeeded = [e for e in runid_pkgidx_result if e not in failed]
                # e.g., [(1001, 0, result0)]

                # let the dispatcher know the failed runid
                failed_runid = [e[0] for e in failed]
                self.dispatcher.failed_runids(failed_runid)

                # rerun failed jobs
                for _, pkgidx, _ in failed:
                    logger = logging.getLogger(__name__)
                    logger.warning('resubmitting {}'.format(self.workingArea.package_path(pkgidx)))

                    runid = self.dispatcher.run(self.workingArea, pkgidx)
                    self.runid_package_index_map[runid] = pkgidx

                pairs = [(pkgidx, result) for runid, pkgidx, result in succeeded]
                # e.g., [(0, result0)] # only successful ones

                pkgidx_result_pairs.extend(pairs)

                time.sleep(self.sleep)

        except KeyboardInterrupt:
            logger = logging.getLogger(__name__)
            logger.warning('received KeyboardInterrupt')
            self.dispatcher.terminate()

        # sort in the order of package_index
        pkgidx_result_pairs = sorted(pkgidx_result_pairs, key = itemgetter(0))

        results = [result for i, result in pkgidx_result_pairs]
        return results

    def close(self):
        self.dispatcher.terminate()
        self.workingArea.close()

##__________________________________________________________________||
