# Tai Sakuma <tai.sakuma@gmail.com>
from ..misc import mkdir_p
from ..misc import list_to_aligned_text
import os

##__________________________________________________________________||
class WriteListToFile(object):
    def __init__(self, outPath):
        self._outPath = outPath

    def __repr__(self):
        return '{}(outPath={!r})'.format(
            self.__class__.__name__,
            self._outPath
        )

    def deliver(self, results):
        if results is None: return
        f = self._open(self._outPath)
        f.write(list_to_aligned_text(results).encode())
        self._close(f)

    def _open(self, path):
        directory = os.path.dirname(path)
        if directory:
            mkdir_p(directory)
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
