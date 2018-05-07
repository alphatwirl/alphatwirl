# Tai Sakuma <tai.sakuma@gmail.com>
import logging

from .TaskPackage import TaskPackage

##__________________________________________________________________||
class CommunicationChannel(object):
    """A communication channel with workers in other processes.

    (This docstring is outdated.)

    You can send tasks to workers through this channel. The workers,
    running in other processes, execute the tasks in the background.
    You can receive the results of the tasks also through this
    channel.

    An instance of this class can be created with two optional
    arguments: ``nprocesses``, the number of workers to be created,
    and ``progressMonitor``::

        progressBar = ProgressBar()
        progressMonitor = BProgressMonitor(progressBar)
        channel = CommunicationChannel(nprocesses=10, progressMonitor=progressMonitor)

    Workers will be created when ``begin()`` is called::

        channel.begin()

    In ``begin()``, this class gives each worker a
    ``progressReporter``, which is created by the ``progressMonitor``.

    Now, you are ready to send a task. A task is a function or any
    object which is callable and picklable. A task can take any number
    of arguments. If a task takes a named argument
    ``progressReporter``, the worker will give the
    ``progressReporter`` to the task. A value that a task returns is
    the result of the task and must be picklable. For example, an
    instance of ``EventLoop`` can be a task. You can send a task with
    the method ``put``::

        channel.put(task1, 10, 20, A=30)

    Here, 10, 20, A=30 are the arguments to the task.

    This class sends the task to a worker. The worker which receives
    the task will first try to call the task with the
    ``progressReporter`` in addition to the arguments. If the task
    doesn't take the ``progressReporter``, it calls only with the
    arguments.

    You can send multiple tasks::

        channel.put(task2)
        channel.put(task3, 100, 200)
        channel.put(task4, A='abc')
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

    def __init__(self, dropbox):
        self.dropbox = dropbox
        self.isopen = False

    def __repr__(self):
        return '{}(dropbox={!r}, isopen={!r})'.format(
            self.__class__.__name__,
            self.dropbox,
            self.isopen
        )

    def begin(self):
        if self.isopen: return
        self.dropbox.open()
        self.isopen = True

    def put(self, task, *args, **kwargs):
        if not self.isopen:
            logger = logging.getLogger(__name__)
            logger.warning('the drop box is not open')
            return
        package = TaskPackage(task=task, args=args, kwargs=kwargs)
        return self.dropbox.put(package)

    def put_multiple(self, task_args_kwargs_list):
        if not self.isopen:
            logger = logging.getLogger(__name__)
            logger.warning('the drop box is not open')
            return

        packages = [ ]
        for t in task_args_kwargs_list:
            try:
                task = t['task']
                args = t.get('args', ())
                kwargs = t.get('kwargs', {})
                package = TaskPackage(task=task, args=args, kwargs=kwargs)
            except TypeError:
                package = TaskPackage(task=t, args=(), kwargs={})
            packages.append(package)
        return self.dropbox.put_multiple(packages)

    def receive_finished(self):
        if not self.isopen:
            logger = logging.getLogger(__name__)
            logger.warning('the drop box is not open')
            return
        return self.dropbox.poll()

    def receive_one(self):
        if not self.isopen:
            logger = logging.getLogger(__name__)
            logger.warning('the drop box is not open')
            return
        return self.dropbox.receive_one()

    def receive_all(self):
        if not self.isopen:
            logger = logging.getLogger(__name__)
            logger.warning('the drop box is not open')
            return
        return self.dropbox.receive()

    def receive(self):
        pkgidx_result_pairs = self.receive_all()
        if pkgidx_result_pairs is None:
            return
        results = [r for _, r in pkgidx_result_pairs]
        return results

    def terminate(self):
        self.dropbox.terminate()

    def end(self):
        if not self.isopen: return
        self.dropbox.close()
        self.isopen = False

##__________________________________________________________________||
