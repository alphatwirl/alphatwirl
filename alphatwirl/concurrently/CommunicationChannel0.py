# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class CommunicationChannel0(object):
    """A communication channel for the single process mode

    An alternative to `CommunicationChannel`. However, unlike
    `CommunicationChannel`, this class does not send tasks to workers.
    Instead, it directly executes tasks.

    This class has the same interface as the class
    `CommunicationChannel`. When this class is used as a substitute
    for `CommunicationChannel`, the tasks will be sequentially
    executed in the foreground.

    """

    def __init__(self):
        self.results = [ ]

    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__,
        )

    def begin(self):
        pass

    def put(self, task, *args, **kwargs):
        result = task(*args, **kwargs)
        self.results.append(result)

    def put_multiple(self, task_args_kwargs_list):
        for t in task_args_kwargs_list:
            try:
                task = t['task']
                args = t.get('args', ())
                kwargs = t.get('kwargs', {})
                self.put(task, *args, **kwargs)
            except TypeError:
                self.put(t)

    def receive(self):
        ret = self.results[:]
        del self.results[:]
        return ret

    def terminate(self):
        pass

    def end(self):
        pass

##__________________________________________________________________||
