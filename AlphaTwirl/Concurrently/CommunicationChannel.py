# Tai Sakuma <tai.sakuma@cern.ch>
from ..ProgressBar import NullProgressMonitor
import multiprocessing
from operator import itemgetter

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
class CommunicationChannel(object):
    """A communication channel with workers in other processes.

    You can send tasks to workers through this channel. The workers,
    running in other processes, execute the tasks in the background.
    You can receive the results of the tasks also through this
    channel.

    An instance of this class can be created with two optional
    arguments: ``nprocesses``, the number of workers to be created,
    and ``progressMonitor``::

        progressBar = ProgressBar()
        progressMonitor = BProgressMonitor(progressBar)
        channel = CommunicationChannel(nprocesses = 10, progressMonitor = progressMonitor)

    Workers will be created when ``begin()`` is called::

        channel.begin()

    In ``begin()``, this class gives each worker a
    ``progressReporter``, which is created by the ``progressMonitor``.

    Now, you are ready to send a task. A task is a function or any
    object which is callable and picklable and which takes the only
    argument ``progressReporter``. A value that a task returns is the
    result of the task and must be picklable. For example, an instance
    of ``EventLoop`` can be a task. You can send a task with the
    method ``put``::

        channel.put(task1)

    This class sends the task to a worker. The worker which receives
    the task will call the task with the ``progressReporter``.


    You can send multiple tasks::

        channel.put(task2)
        channel.put(task3)
        channel.put(task4)
        channel.put(task5)

    They will be executed by workers.

    You can receive the results of the tasks with the method
    ``receive()``::

        results = channel.receive()

    This method will wait until all tasks are finished. If a task
    gives a ``progressReport`` to the ``progressReporter``, the report
    will be used, for example, to update progress bars on the screen.

    When all tasks end, results will be returned. The return value
    ``results`` is a list of results of the tasks. They are sorted in
    the order in which the tasks are originally put.

    After receiving the results, you can put more tasks::

        channel.put(task6)
        channel.put(task7)

    And you can receive the results of them::

        results = channel.receive()

    If there are no more tasks to be done, you should call the method
    ``end``::

        channel.end()

    This will end all background processes.

    """

    def __init__(self, nprocesses = 16, progressMonitor = None):

        if nprocesses <= 0:
            raise ValueError("nprocesses must be at least one: " + str(nprocesses) + " is given")


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
            worker = Worker(
                task_queue = self.task_queue,
                result_queue = self.result_queue,
                progressReporter = self.progressMonitor.createReporter(),
                lock = self.lock
            )
            worker.start()
            self.nCurrentProcesses += 1

    def put(self, task, *args, **kwargs):
        self.task_queue.put((self.taskNo, task, args, kwargs))
        self.taskNo += 1
        self.nRunningTasks += 1

    def receive(self):
        messages = [ ] # a list of (taskNo, result)
        while self.nRunningTasks >= 1:
            if self.result_queue.empty(): continue
            message = self.result_queue.get()
            messages.append(message)
            self.nRunningTasks -= 1

        # sort in the order of taskNo
        messages = sorted(messages, key = itemgetter(0))

        results = [result for taskNo, result in messages]
        return results

    def end(self):
        for i in xrange(self.nCurrentProcesses):
            self.task_queue.put(None) # end workers
        self.task_queue.join()
        self.nCurrentProcesses = 0

##__________________________________________________________________||
