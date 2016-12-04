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
            task_idx, package = message
            result = self._run_task(package)
            self.task_queue.task_done()
            self.result_queue.put((task_idx, result))

    def _run_task(self, package):
        try:
            result = package.task(progressReporter = self.progressReporter, *package.args, **package.kwargs)
        except TypeError:
            result = package.task(*package.args, **package.kwargs)
        return result

##__________________________________________________________________||
