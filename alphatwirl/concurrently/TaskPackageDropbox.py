# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import time
from operator import itemgetter
from collections import deque

from .WorkingArea import WorkingArea

##__________________________________________________________________||
class TaskPackageDropbox(object):
    """A drop box for task packages.

    It puts task packages in a working area and dispatches runners
    that execute the tasks.

    """
    def __init__(self, workingArea, dispatcher, sleep=5):
        self.workingArea = workingArea
        self.dispatcher = dispatcher
        self.sleep = sleep

    def __repr__(self):
        name_value_pairs = (
            ('workingArea', self.workingArea),
            ('dispatcher', self.dispatcher),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def open(self):
        self.workingArea.open()
        self.runid_pkgidx_map = { }
        self.to_return = deque() # pairs of pkgidxs and results

    def put(self, package):
        """Put a package. Return a package index.
        """

        pkgidx = self.workingArea.put_package(package)

        logger = logging.getLogger(__name__)
        logger.info('submitting {}'.format(self.workingArea.package_path(pkgidx)))

        runid = self.dispatcher.run(self.workingArea, pkgidx)
        self.runid_pkgidx_map[runid] = pkgidx

        return pkgidx

    def put_multiple(self, packages):
        """Put multiple packages. Return package indices.
        """
        pkgidxs = [self.workingArea.put_package(p) for p in packages ]

        logger = logging.getLogger(__name__)
        logger.info('submitting {}'.format(
            ', '.join(['{}'.format(self.workingArea.package_path(i)) for i in pkgidxs])
        ))
        runids = self.dispatcher.run_multiple(self.workingArea, pkgidxs)
        self.runid_pkgidx_map.update(zip(runids, pkgidxs))

        return pkgidxs

    def poll(self):
        """Return pairs of package indices and results of finished tasks.
        """

        pairs = list(self.to_return)
        self.to_return.clear()
        pairs.extend(self._collect_pkgidx_result_pairs_of_finished_tasks())
        pairs = sorted(pairs, key=itemgetter(0))
        return pairs

    def receive_one(self):
        """Return a pair of a package index and result.

        This method waits until a task finishes.
        This method returns None if no task is running.
        """

        if self.to_return:
            return self.to_return.popleft()

        if not self.runid_pkgidx_map:
            return None

        while not self.to_return:
            pairs = self._collect_pkgidx_result_pairs_of_finished_tasks()
            self.to_return.extend(pairs)

            time.sleep(self.sleep)

        return self.to_return.popleft()

    def receive(self):
        """Return pairs of package indices and results.

        This method waits until all tasks finish.
        """

        pkgidx_result_pairs = list(self.to_return)
        self.to_return.clear()
        while self.runid_pkgidx_map:

            pairs = self._collect_pkgidx_result_pairs_of_finished_tasks()
            pkgidx_result_pairs.extend(pairs)

            time.sleep(self.sleep)

        # sort in the order of pkgidx
        pkgidx_result_pairs = sorted(pkgidx_result_pairs, key=itemgetter(0))

        return pkgidx_result_pairs

    def _collect_pkgidx_result_pairs_of_finished_tasks(self):

        finished_runid = self.dispatcher.poll()
        # e.g., [1001, 1003]

        runid_pkgidx = [(i, self.runid_pkgidx_map.pop(i)) for i in finished_runid]
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
            self.runid_pkgidx_map[runid] = pkgidx

        pairs = [(pkgidx, result) for runid, pkgidx, result in succeeded]
        # e.g., [(0, result0)] # only successful ones

        return pairs

    def terminate(self):
        self.dispatcher.terminate()

    def close(self):
        self.workingArea.close()

##__________________________________________________________________||
