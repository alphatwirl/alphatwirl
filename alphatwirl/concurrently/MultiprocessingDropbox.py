# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function

import mantichora

from alphatwirl.misc.deprecation import _deprecated_class_method_option

##__________________________________________________________________||
class MultiprocessingDropbox(object):
    """A drop box for task packages.

    The tasks will be executed in multiprocessing

    The original implementation of this class has been released as an
    independent package: https://github.com/alphatwirl/mantichora

    The current implementation uses mantichora.

    Parameters
    ----------
    nprocesses : int
        The number of processes

    """
    @_deprecated_class_method_option('progressbar', msg='use atpbar.disable() instead to turn off progress bars') # after v0.23.3 (2019-03-13)
    @_deprecated_class_method_option('progressMonitor')
    def __init__(self, nprocesses=16, progressMonitor=None, progressbar=True):

        if nprocesses <= 0:
            raise ValueError("nprocesses must be at least one: {} is given".format(nprocesses))

        self.nprocesses = nprocesses
        self.mcore = None

        self._repr_pairs = [
            ('nprocesses', nprocesses),
        ]

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in self._repr_pairs]),
        )

    def open(self):
        if self.mcore is not None:
            # already open
            return
        self.mcore = mantichora.mantichora(nworkers=self.nprocesses)

    def terminate(self):
        if self.mcore is None:
            return
        self.mcore.terminate()

    def close(self):
        if self.mcore is None:
            return
        self.mcore.end()
        self.mcore = None

    def put(self, package):
        return self.mcore.run(package)

    def put_multiple(self, packages):
        task_idxs = [ ]
        for p in packages:
            task_idxs.append(self.mcore.run(p))
        return task_idxs

    def poll(self):
        return self.mcore.receive_finished()

    def receive_one(self):
        return self.mcore.receive_one()

    def receive(self):
        return self.mcore.receive_all()

##__________________________________________________________________||
