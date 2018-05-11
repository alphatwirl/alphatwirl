# Tai Sakuma <tai.sakuma@gmail.com>
from ..misc import mkdir_p
from ..misc import list_to_aligned_text
import os

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='heppyresult has been moved to https://github.com/alphatwirl/atheppy.')
class TblComponentConfig(object):
    def __init__(self, outPath, columnNames, keys):
        self._outPath = outPath
        self.columnNames = columnNames
        self._rows = [['component'] + list(columnNames)]
        self._keys = keys

    def begin(self): pass

    def read(self, component):

        cfg = component.config()
        if cfg is None: return
        if not all([k in cfg for k in self._keys]): return

        vals =  [cfg[k] for k in self._keys]
        self._rows.append([component.name] + vals)

    def end(self):
        if len(self._rows) == 1: return

        f = self._open(self._outPath)
        f.write(list_to_aligned_text(self._rows).encode())
        self._close(f)

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
