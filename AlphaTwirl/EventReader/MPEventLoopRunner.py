# Tai Sakuma <tai.sakuma@cern.ch>
from NullProgressMonitor import NullProgressMonitor
import multiprocessing

##____________________________________________________________________________||
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

##____________________________________________________________________________||
class MPEventLoopRunner(object):
    def __init__(self, nprocesses = 16, progressMonitor = None):
        self._nprocesses = nprocesses
        self._ntasks = 0
        self._progressMonitor = NullProgressMonitor() if progressMonitor is None else progressMonitor
        self.start_workers()

    def begin(self):
        self._allReaders = { }

    def run(self, eventLoop):

        # add id so can collect later
        reader = eventLoop.reader
        reader.id = id(reader)
        self._allReaders[id(reader)] = reader

        self._tasks.put(eventLoop)
        self._ntasks += 1

    def end(self):

        while self._ntasks >= 1:
            self._progressMonitor.monitor()
            if self.collectTaskResults():
                self._ntasks -= 1

        self._progressMonitor.last()

        self.end_workers()

    def collectTaskResults(self):
        if self._results.empty(): return False
        reader = self._results.get()
        self._allReaders[reader.id].setResults(reader.results())
        return True

    def start_workers(self):
        self._nworkers = 0
        self._tasks = multiprocessing.JoinableQueue()
        self._results = multiprocessing.Queue()
        self._lock = multiprocessing.Lock()
        for i in xrange(self._nprocesses):
            worker = Worker(self._tasks, self._results, self._progressMonitor.createReporter(), self._lock)
            worker.start()
            self._nworkers += 1

    def end_workers(self):
        for i in xrange(self._nworkers):
            self._tasks.put(None) # end workers
        self._tasks.join()

##____________________________________________________________________________||
