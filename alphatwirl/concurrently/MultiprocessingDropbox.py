# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import logging
import multiprocessing
import threading

from operator import itemgetter

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

    def put(self, package):
        self.task_idx += 1
        self.task_queue.put((self.task_idx, package))
        self.n_ongoing_tasks += 1

    def put_multiple(self, packages):
        for package in packages:
            self.put(package)

    def receive(self):
        messages = [ ] # a list of (task_idx, result)
        while self.n_ongoing_tasks >= 1:
            if self.result_queue.empty(): continue
            message = self.result_queue.get()
            messages.append(message)
            self.n_ongoing_tasks -= 1

        # sort in the order of task_idx
        messages = sorted(messages, key=itemgetter(0))

        results = [result for task_idx, result in messages]
        return results

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
