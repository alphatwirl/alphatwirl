# Tai Sakuma <sakuma@fnal.gov>
from EventReaderBundle import EventLoop
import multiprocessing

##____________________________________________________________________________||
class NullProgressReporter(object):
    def report(self, event): pass

##____________________________________________________________________________||
class NullProgressMonitor(object):
    def createReporter(self): return NullProgressReporter()
    def addWorker(self, worker): pass
    def monitor(self): pass
    def last(self): pass

##____________________________________________________________________________||
class Worker(multiprocessing.Process):
    def __init__(self, task_queue, result_queue, progressReporter, lock):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.lock = lock
        self.progressReporter = progressReporter
        self.progressReporter.worker = self

    def run(self):
        while True:
            task = self.task_queue.get()
            if task is None:
                self.task_queue.task_done()
                break
            readers = task(self.progressReporter)
            self.task_queue.task_done()
            self.result_queue.put(readers)

##____________________________________________________________________________||
class MPEventLoopRunner(object):
    def __init__(self, nprocesses = 16, progressMonitor = NullProgressMonitor()):
        self._nprocesses = nprocesses
        self._ntasks = 0
        self._nworkers = 0
        self._workers = [ ]
        self._progressMonitor = progressMonitor

    def begin(self):
        self._allReaders = { }
        self._tasks = multiprocessing.JoinableQueue()
        self._results = multiprocessing.Queue()
        self._lock = multiprocessing.Lock()
        for i in xrange(self._nprocesses):
            worker = Worker(self._tasks, self._results, self._progressMonitor.createReporter(), self._lock)
            worker.start()
            self._nworkers += 1
            self._workers.append(worker)
            self._progressMonitor.addWorker(worker)

    def run(self, eventLoop):
        # add ids so can collect later
        for reader in eventLoop.readers:
            reader.id = id(reader)
            self._allReaders[id(reader)] = reader

        self._tasks.put(eventLoop)
        self._ntasks += 1

    def end(self):
        for i in xrange(self._nworkers):
            self._tasks.put(None) # end workers

        while self._ntasks >= 1:
            self._progressMonitor.monitor()
            self.collectReaders()

        self._progressMonitor.last()
        self._tasks.join()

    def collectReaders(self):
        if self._results.empty(): return
        readers = self._results.get()
        for reader in readers:
            self._allReaders[reader.id].setResults(reader.results())
        self._ntasks -= 1

##____________________________________________________________________________||
