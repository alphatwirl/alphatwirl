# Tai Sakuma <tai.sakuma@cern.ch>
from ..ProgressBar import NullProgressMonitor
import multiprocessing
from operator import itemgetter

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
            message = self.task_queue.get()
            if message is None:
                self.task_queue.task_done()
                break
            taskNo, task = message
            result = task(self.progressReporter)
            self.task_queue.task_done()
            self.result_queue.put((taskNo, result))

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
        self.taskNo = 0

    def begin(self):
        if self.nCurrentProcesses >= self.nMaxProcesses: return
        for i in xrange(self.nCurrentProcesses, self.nMaxProcesses):
            worker = Worker(self.task_queue, self.result_queue, self.progressMonitor.createReporter(), self.lock)
            worker.start()
            self.nCurrentProcesses += 1

    def put(self, task):
        self.task_queue.put((self.taskNo, task))
        self.taskNo += 1
        self.nRunningTasks += 1

    def receive(self):
        messages = [ ] # a list of (taskNo, result)
        while self.nRunningTasks >= 1:
            self.progressMonitor.monitor()
            if self.result_queue.empty(): continue
            message = self.result_queue.get()
            messages.append(message)
            self.nRunningTasks -= 1

        # sort in the order of taskNo
        messages = sorted(messages, key = itemgetter(0))

        results = [result for taskNo, result in messages]
        self.progressMonitor.last()
        return results

    def end(self):
        for i in xrange(self.nCurrentProcesses):
            self.task_queue.put(None) # end workers
        self.task_queue.join()
        self.nCurrentProcesses = 0

##__________________________________________________________________||
