# Tai Sakuma <tai.sakuma@cern.ch>
from NullProgressMonitor import NullProgressMonitor
import multiprocessing

##__________________________________________________________________||
class Worker(multiprocessing.Process):
    def __init__(self, task_queue, result_queue, progressReporter, lock):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.lock = lock
        self.progressReporter = progressReporter

    def run(self):
        while True:
            task = self.task_queue.get()
            if task is None:
                self.task_queue.task_done()
                break
            results = task(self.progressReporter)
            self.task_queue.task_done()
            self.result_queue.put(results)

##__________________________________________________________________||
class CommunicationChannel(object):
    def __init__(self, nprocesses = 16, progressMonitor = None):
        self.progressMonitor = NullProgressMonitor() if progressMonitor is None else progressMonitor
        self.nprocesses = nprocesses
        self._ntasks = 0

    def begin(self):
        self.start_workers(self.nprocesses, self.progressMonitor)

    def put(self, task):
        self.task_queue.put(task)
        self._ntasks += 1

    def receive(self):
        results = [ ]
        while self._ntasks >= 1:
            self.progressMonitor.monitor()
            if self.result_queue.empty(): continue
            result = self.result_queue.get()
            results.append(result)
            self._ntasks -= 1
        self.progressMonitor.last()
        return results

    def end(self):
        self.end_workers()

    def start_workers(self, nprocesses, progressMonitor):
        self._nworkers = 0
        self.task_queue = multiprocessing.JoinableQueue()
        self.result_queue = multiprocessing.Queue()
        self.lock = multiprocessing.Lock()
        for i in xrange(nprocesses):
            worker = Worker(self.task_queue, self.result_queue, progressMonitor.createReporter(), self.lock)
            worker.start()
            self._nworkers += 1

    def end_workers(self):
        for i in xrange(self._nworkers):
            self.task_queue.put(None) # end workers
        self.task_queue.join()

##__________________________________________________________________||
