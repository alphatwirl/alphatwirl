# Tai Sakuma <tai.sakuma@cern.ch>
from ..ProgressBar import NullProgressMonitor
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
        self.nMaxProcesses = nprocesses
        self.nCurrentProcesses = 0
        self.task_queue = multiprocessing.JoinableQueue()
        self.result_queue = multiprocessing.Queue()
        self.lock = multiprocessing.Lock()
        self.nRunningTasks = 0

    def begin(self):
        if self.nCurrentProcesses >= self.nMaxProcesses: return
        for i in xrange(self.nCurrentProcesses, self.nMaxProcesses):
            worker = Worker(self.task_queue, self.result_queue, self.progressMonitor.createReporter(), self.lock)
            worker.start()
            self.nCurrentProcesses += 1

    def put(self, task):
        self.task_queue.put(task)
        self.nRunningTasks += 1

    def receive(self):
        results = [ ]
        while self.nRunningTasks >= 1:
            self.progressMonitor.monitor()
            if self.result_queue.empty(): continue
            result = self.result_queue.get()
            results.append(result)
            self.nRunningTasks -= 1
        self.progressMonitor.last()
        return results

    def end(self):
        for i in xrange(self.nCurrentProcesses):
            self.task_queue.put(None) # end workers
        self.task_queue.join()
        self.nCurrentProcesses = 0

##__________________________________________________________________||
