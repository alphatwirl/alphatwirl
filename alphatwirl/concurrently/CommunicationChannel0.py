# Tai Sakuma <tai.sakuma@gmail.com>
import atpbar

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

    Parameters
    ----------
    progressbar : bool
        Progress bars from atpbar will be turned off if False.

    """

    def __init__(self, progressbar=True):
        self.progressbar = progressbar

        self.taskidx = -1 # so it starts from 0
        self.taskidx_result_pairs = [ ]

        self._repr_pairs = [
            ('progressbar', progressbar),
        ]

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in self._repr_pairs]),
        )

    def begin(self):
        if not self.progressbar:
            atpbar.funcs._do_not_start_pickup = True

    def put(self, task, *args, **kwargs):
        self.taskidx += 1
        result = task(*args, **kwargs)
        self.taskidx_result_pairs.append((self.taskidx, result))
        return self.taskidx

    def put_multiple(self, task_args_kwargs_list):
        task_idxs = [ ]
        for t in task_args_kwargs_list:
            try:
                task = t['task']
                args = t.get('args', ())
                kwargs = t.get('kwargs', {})
                task_idx = self.put(task, *args, **kwargs)
            except TypeError:
                task_idx = self.put(t)
            task_idxs.append(task_idx)
        return task_idxs

    def receive_finished(self):
        return self.receive_all()

    def receive_one(self):
        if self.taskidx_result_pairs:
            return self.taskidx_result_pairs.pop(0)
        return None

    def receive_all(self):
        ret = self.taskidx_result_pairs[:]
        del self.taskidx_result_pairs[:]
        return ret

    def receive(self):
        ret = [r for _, r in self.receive_all()]
        return ret

    def terminate(self):
        pass

    def end(self):
        pass

##__________________________________________________________________||
