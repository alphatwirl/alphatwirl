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
        self.runid_to_return = deque() # finished runids

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
        pkgidxs = [self.workingArea.put_package(p) for p in packages]

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
        pkgidx_result_pairs = self._collect_all_finished_pkgidx_result_pairs()

        # remove failed results and sort in the order of pkgidx
        pkgidx_result_pairs = filter(itemgetter(1), pkgidx_result_pairs)
        pkgidx_result_pairs = sorted(pkgidx_result_pairs, key=itemgetter(0))

        return pkgidx_result_pairs

    def receive_one(self):
        """Return a pair of a package index and result.

        This method waits until a task finishes.
        This method returns None if no task is running.
        """
        if not self.runid_pkgidx_map:
            return None

        pkgidx_result_pair = None
        while not pkgidx_result_pair:

            pkgidx_result_pair = self._collect_next_finished_pkgidx_result_pair()

            if pkgidx_result_pair and not pkgidx_result_pair[1]:
                pkgidx_result_pair = None

            # Only sleep if there are no pending runs
            if not self.runid_to_return and self.runid_pkgidx_map:
                time.sleep(self.sleep)

        return pkgidx_result_pair

    def receive(self):
        """Return pairs of package indices and results.

        This method waits until all tasks finish.
        """

        pkgidx_result_pairs = []
        while self.runid_pkgidx_map:
            pkgidx_result_pairs.extend(
                self._collect_all_finished_pkgidx_result_pairs()
            )

            # Only sleep if we're waiting for runs
            if self.runid_pkgidx_map:
                time.sleep(self.sleep)

        # remove failed results and sort in the order of pkgidx
        pkgidx_result_pairs = filter(itemgetter(1), pkgidx_result_pairs)
        pkgidx_result_pairs = sorted(pkgidx_result_pairs, key=itemgetter(0))

        return pkgidx_result_pairs

    def _collect_all_finished_pkgidx_result_pairs(self):
        pkgidx_result_pairs = []

        pairs = self._collect_next_finished_pkgidx_result_pair()
        while self.runid_to_return:
            if pairs: pkgidx_result_pairs.append(pairs)
            pairs = self._collect_next_finished_pkgidx_result_pair()
        if pairs: pkgidx_result_pairs.append(pairs)

        return pkgidx_result_pairs

    def _collect_next_finished_pkgidx_result_pair(self):
        if not self.runid_to_return:
            self.runid_to_return.extend(self.dispatcher.poll())

        # No finished runs remaining
        if not self.runid_to_return:
            return None

        runid = self.runid_to_return.popleft()
        pkgidx = self.runid_pkgidx_map.pop(runid)
        result = self.workingArea.collect_result(pkgidx)

        # rerun failed job
        if result is None:
            logger = logging.getLogger(__name__)
            logger.warning('resubmitting {}'.format(
                self.workingArea.package_path(pkgidx)
            ))
            self.dispatcher.failed_runids([runid])
            runid = self.dispatcher.run(self.workingArea, pkgidx)
            self.runid_pkgidx_map[runid] = pkgidx

        return (pkgidx, result)

    def terminate(self):
        self.dispatcher.terminate()

    def close(self):
        self.workingArea.close()

##__________________________________________________________________||
