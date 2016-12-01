# Tai Sakuma <tai.sakuma@cern.ch>
import multiprocessing

##__________________________________________________________________||
class Worker(multiprocessing.Process):
    def __init__(self, task_queue, result_queue, lock, progressReporter):
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
            taskNo, task, args, kwargs = message
            try:
                result = task(progressReporter = self.progressReporter, *args, **kwargs)
            except TypeError:
                result = task(*args, **kwargs)
            self.task_queue.task_done()
            self.result_queue.put((taskNo, result))

##__________________________________________________________________||
