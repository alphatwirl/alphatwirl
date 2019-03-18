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
        """open the drop box

        You need to call this method before starting putting packages.

        Returns
        -------
        None

        """

        self.workingArea.open()
        self.runid_pkgidx_map = { }
        self.runid_to_return = deque() # finished runids

    def terminate(self):
        """terminate the drop box

        Returns
        -------
        None

        """
        self.dispatcher.terminate()

    def close(self):
        """close the drop box

        Returns
        -------
        None

        """
        self.workingArea.close()

    def put(self, package):
        """put a task

        This method places a task in the working area and have the
        dispatcher execute it.

        If you need to put multiple tasks, it can be much faster to
        use `put_multiple()` than to use this method multiple times
        depending of the dispatcher.

        Parameters
        ----------
        package : callable
            A task

        Returns
        -------
        int
            A package index assigned by the working area

        """

        pkgidx = self.workingArea.put_package(package)

        logger = logging.getLogger(__name__)
        logger.info('submitting {}'.format(self.workingArea.package_relpath(pkgidx)))

        runid = self.dispatcher.run(self.workingArea, pkgidx)
        self.runid_pkgidx_map[runid] = pkgidx
        return pkgidx

    def put_multiple(self, packages):
        """put tasks

        This method places multiple tasks in the working area and have
        the dispatcher execute them.

        Parameters
        ----------
        packages : list(callable)
            A list of tasks

        Returns
        -------
        list(int)
            Package indices assigned by the working area

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
        """return pairs of package indices and results of all tasks

        This method waits until all tasks finish.

        Returns
        -------
        list
            A list of pairs of package indices and results

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
        """return pairs of package indices and results of finished tasks

        This method does not wait for tasks to finish.

        Returns
        -------
        list
            A list of pairs of package indices and results

        """

        self.runid_to_return.extend(self.dispatcher.poll())
        ret = self._collect_all_finished_pkgidx_result_pairs()
        return ret

    def receive_one(self):
        """return a pair of a package index and result of a task

        This method waits until a tasks finishes. It returns `None` if
        no task is running.

        Returns
        -------
        tuple or None
            A pair of a package index and result. `None` if no tasks
            is running.

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

##__________________________________________________________________||
