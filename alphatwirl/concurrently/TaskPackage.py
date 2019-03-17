# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class TaskPackage(object):
    """A task package

    Note: This class will be replaced with `functools.partial`

    """
    def __init__(self, task, args, kwargs):
        self.task = task
        self.args = args
        self.kwargs = kwargs
    def __call__(self):
        return self.task(*self.args, **self.kwargs)

##__________________________________________________________________||
