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
            reader = task(self.progressReporter)
            self.task_queue.task_done()
            self.result_queue.put(reader)

##____________________________________________________________________________||
class MPEventLoopRunner(object):
    def __init__(self, nprocesses = 16, progressMonitor = None):
        self._nprocesses = nprocesses
        self._ntasks = 0
        self._nworkers = 0
        self._progressMonitor = NullProgressMonitor() if progressMonitor is None else progressMonitor

    def begin(self):
        self._allReaders = { }
        self._tasks = multiprocessing.JoinableQueue()
        self._results = multiprocessing.Queue()
        self._lock = multiprocessing.Lock()
        for i in xrange(self._nprocesses):
            worker = Worker(self._tasks, self._results, self._progressMonitor.createReporter(), self._lock)
            worker.start()
            self._nworkers += 1

    def run(self, eventLoop):

        # add id so can collect later
        reader = eventLoop.reader
        reader.id = id(reader)
        self._allReaders[id(reader)] = reader

        self._tasks.put(eventLoop)
        self._ntasks += 1

    def end(self):
        for i in xrange(self._nworkers):
            self._tasks.put(None) # end workers

        while self._ntasks >= 1:
            self._progressMonitor.monitor()
            if self.collectTaskResults():
                self._ntasks -= 1

        self._progressMonitor.last()
        self._tasks.join()

    def collectTaskResults(self):
        if self._results.empty(): return False
        reader = self._results.get()
        self._allReaders[reader.id].setResults(reader.results())
        return True

##____________________________________________________________________________||
