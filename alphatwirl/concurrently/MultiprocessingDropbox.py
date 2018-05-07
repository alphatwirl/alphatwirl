# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import logging
import multiprocessing
import threading

from operator import itemgetter
from collections import deque

from ..progressbar import NullProgressMonitor
from .TaskPackage import TaskPackage

from .Worker import Worker

##__________________________________________________________________||
# https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes
def logger_thread(queue):
    while True:
        record = queue.get()
        if record is None:
            break
        logger = logging.getLogger(record.name)
        logger.handle(record)

##__________________________________________________________________||
class MultiprocessingDropbox(object):
    def __init__(self, nprocesses=16, progressMonitor=None):

        if nprocesses <= 0:
            raise ValueError("nprocesses must be at least one: {} is given".format(nprocesses))

        self.progressMonitor = NullProgressMonitor() if progressMonitor is None else progressMonitor

        self.n_max_workers = nprocesses
        self.workers = [ ]
        self.task_queue = multiprocessing.JoinableQueue()
        self.result_queue = multiprocessing.Queue()
        self.logging_queue = multiprocessing.Queue()
        self.lock = multiprocessing.Lock()
        self.n_ongoing_tasks = 0
        self.task_idx = -1 # so it starts from 0

    def __repr__(self):
        return '{}(progressMonitor={!r}, n_max_workers={!r}, n_ongoing_tasks={!r}, task_idx={!r})'.format(
            self.__class__.__name__,
            self.progressMonitor,
            self.n_max_workers,
            self.n_ongoing_tasks,
            self.task_idx
        )

    def open(self):

        if len(self.workers) >= self.n_max_workers:
            # workers already created
            return

        # start logging listener
        self.loggingListener = threading.Thread(
            target=logger_thread, args=(self.logging_queue,)
        )
        self.loggingListener.start()

        # start workers
        for i in range(self.n_max_workers):
            worker = Worker(
                task_queue=self.task_queue,
                result_queue=self.result_queue,
                logging_queue=self.logging_queue,
                progressReporter=self.progressMonitor.createReporter(),
                lock=self.lock
            )
            worker.start()
            self.workers.append(worker)

        self.to_return = deque()

    def put(self, package):
        self.task_idx += 1
        self.task_queue.put((self.task_idx, package))
        self.n_ongoing_tasks += 1
        return self.task_idx

    def put_multiple(self, packages):
        task_idxs = [ ]
        for package in packages:
            task_idxs.append(self.put(package))
        return task_idxs

    def poll(self):
        """Return pairs of task indices and results of finished tasks.
        """

        messages = list(self.to_return) # a list of (task_idx, result)
        self.to_return.clear()

        messages.extend(self._receive_finished())

        # sort in the order of task_idx
        messages = sorted(messages, key=itemgetter(0))

        return messages

    def receive_one(self):
        """Return a pair of a package index and a result.

        This method waits until a task finishes.
        This method returns None if no task is running.
        """

        if self.to_return:
            return self.to_return.popleft()

        if self.n_ongoing_tasks == 0:
            return None

        while not self.to_return:
            self.to_return.extend(self._receive_finished())

        return self.to_return.popleft()


    def receive(self):
        """Return pairs of task indices and results.

        This method waits until all tasks finish.
        """

        messages = list(self.to_return) # a list of (task_idx, result)
        self.to_return.clear()

        while self.n_ongoing_tasks >= 1:
            messages.extend(self._receive_finished())

        # sort in the order of task_idx
        messages = sorted(messages, key=itemgetter(0))

        return messages

    def _receive_finished(self):
        messages = [ ] # a list of (task_idx, result)
        while not self.result_queue.empty():
            message = self.result_queue.get()
            messages.append(message)
            self.n_ongoing_tasks -= 1
        return messages

    def terminate(self):
        for worker in self.workers:
            worker.terminate()

        # wait until all workers are terminated.
        while any([w.is_alive() for w in self.workers]):
            pass

        self.workers = [ ]

    def close(self):

        # end workers
        if self.workers:
            for i in range(len(self.workers)):
                self.task_queue.put(None)
            self.task_queue.join()
            self.workers = [ ]

        # end logging listener
        self.logging_queue.put(None)
        self.loggingListener.join()

##__________________________________________________________________||
