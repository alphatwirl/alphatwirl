# Tai Sakuma <tai.sakuma@gmail.com>
import logging
import time
from operator import itemgetter
from collections import deque

##__________________________________________________________________||
class TaskPackageDropbox(object):
    """A drop box for task packages.

    This class puts task packages in a working area and have
    dispatchers execute the tasks.

    Parameters
    ----------
    workingArea :
        A working area, an instance of `WorkingArea`
    dispatcher :
        A dispatcher
    sleep : float
        A time interval between each query while waiting a task to
        finish.

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
        logger.info('submitting {}'.format(self.workingArea.package_relpath(pkgidx)))

        runid = self.dispatcher.run(self.workingArea, pkgidx)
        self.runid_pkgidx_map[runid] = pkgidx
        return pkgidx

    def put_multiple(self, packages):
        """Put multiple packages. Return package indices.
        """
        pkgidxs = [self.workingArea.put_package(p) for p in packages]

        logger = logging.getLogger(__name__)
        logger.info('submitting {}'.format(
            ', '.join(['{}'.format(self.workingArea.package_relpath(i)) for i in pkgidxs])
        ))

        runids = self.dispatcher.run_multiple(self.workingArea, pkgidxs)
        self.runid_pkgidx_map.update(zip(runids, pkgidxs))
        return pkgidxs

    def receive(self):
        """Return pairs of package indices and results.

        This method waits until all tasks finish.
        """

        ret = [ ] # a list of (pkgid, result)
        while True:

            if self.runid_pkgidx_map:
                self.runid_to_return.extend(self.dispatcher.poll())
                ret.extend(self._collect_all_finished_pkgidx_result_pairs())

            if not self.runid_pkgidx_map:
                break
            time.sleep(self.sleep)

        ret = sorted(ret, key=itemgetter(0))

        return ret

    def poll(self):
        """Return pairs of package indices and results of finished tasks.
        """
        self.runid_to_return.extend(self.dispatcher.poll())
        ret = self._collect_all_finished_pkgidx_result_pairs()
        return ret

    def receive_one(self):
        """Return a pair of a package index and result.

        This method waits until a task finishes.
        This method returns None if no task is running.
        """
        if not self.runid_pkgidx_map:
            return None

        while True:

            if not self.runid_to_return:
                self.runid_to_return.extend(self.dispatcher.poll())

            ret = self._collect_next_finished_pkgidx_result_pair()

            if ret is not None:
                break

            if self.runid_pkgidx_map:
                time.sleep(self.sleep)

        return ret

    def _collect_all_finished_pkgidx_result_pairs(self):
        ret = [ ]
        while self.runid_to_return:
            pairs = self._collect_next_finished_pkgidx_result_pair()
            if pairs is None:
                continue
            ret.append(pairs)
        return ret

    def _collect_next_finished_pkgidx_result_pair(self):

        while self.runid_to_return:
            runid = self.runid_to_return.popleft()
            pkgidx = self.runid_pkgidx_map.pop(runid)
            result = self.workingArea.collect_result(pkgidx)

            if result is not None:
                break

            logger = logging.getLogger(__name__)
            logger.warning('resubmitting {}'.format(
                self.workingArea.package_relpath(pkgidx)
            ))
            self.dispatcher.failed_runids([runid])
            runid = self.dispatcher.run(self.workingArea, pkgidx)
            self.runid_pkgidx_map[runid] = pkgidx
        else:
            return None

        return pkgidx, result

    def terminate(self):
        self.dispatcher.terminate()

    def close(self):
        self.workingArea.close()

##__________________________________________________________________||
