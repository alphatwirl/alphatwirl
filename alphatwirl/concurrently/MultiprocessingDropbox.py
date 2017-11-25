# Tai Sakuma <tai.sakuma@cern.ch>
import multiprocessing
from operator import itemgetter

from ..progressbar import NullProgressMonitor
from .TaskPackage import TaskPackage

from .Worker import Worker

##__________________________________________________________________||
class MultiprocessingDropbox(object):
    def __init__(self, nprocesses = 16, progressMonitor = None):

        if nprocesses <= 0:
            raise ValueError("nprocesses must be at least one: {} is given".format(nprocesses))

        self.progressMonitor = NullProgressMonitor() if progressMonitor is None else progressMonitor

        self.n_max_workers = nprocesses
        self.n_workers = 0
        self.task_queue = multiprocessing.JoinableQueue()
        self.result_queue = multiprocessing.Queue()
        self.lock = multiprocessing.Lock()
        self.n_ongoing_tasks = 0
        self.task_idx = -1 # so it starts from 0

    def __repr__(self):
        return '{}(progressMonitor = {!r}, n_max_workers = {!r}, n_workers = {!r}, n_ongoing_tasks = {!r}, task_idx = {!r})'.format(
            self.__class__.__name__,
            self.progressMonitor,
            self.n_max_workers,
            self.n_workers,
            self.n_ongoing_tasks,
            self.task_idx
        )

    def open(self):

        if self.n_workers >= self.n_max_workers:
            # workers already created
            return

        # start workers
        for i in range(self.n_workers, self.n_max_workers):
            worker = Worker(
                task_queue = self.task_queue,
                result_queue = self.result_queue,
                progressReporter = self.progressMonitor.createReporter(),
                lock = self.lock
            )
            worker.start()
            self.n_workers += 1

    def put(self, package):
        self.task_idx += 1
        self.task_queue.put((self.task_idx, package))
        self.n_ongoing_tasks += 1

    def receive(self):
        messages = [ ] # a list of (task_idx, result)
        while self.n_ongoing_tasks >= 1:
            if self.result_queue.empty(): continue
            message = self.result_queue.get()
            messages.append(message)
            self.n_ongoing_tasks -= 1

        # sort in the order of task_idx
        messages = sorted(messages, key = itemgetter(0))

        results = [result for task_idx, result in messages]
        return results

    def close(self):
        for i in range(self.n_workers):
            self.task_queue.put(None) # end workers
        self.task_queue.join()
        self.n_workers = 0

##__________________________________________________________________||
