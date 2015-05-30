# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class ProgressReport(object):
    """A progress report

    Args:
        name (str): the name of the task. if ``taskid`` is ``None``, used to identify the task
        done (int): the number of the iterations done so far
        total (int): the total iterations to be done
        taskid (immutable, optional): if given, used to identify the task. useful if multiple tasks have the same name
    """

    def __init__(self, name, done, total, taskid = None):
        self.taskid = taskid if taskid is not None else name
        self.name = name
        self.done = done
        self.total = total

##__________________________________________________________________||
