# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class TblXsec(object):
    def __init__(self, outPath):
        self._outPath = outPath
        self._rows = [['component', 'xsec']]

    def begin(self): pass

    def read(self, component):
        xsec = component.config()['xSection']
        self._rows.append([component.name, xsec])

    def end(self):
        transposed = [[r[i] for r in self._rows] for i in range(len(self._rows[0]))]
        transposed = [[int(e) if isinstance(e, float) and e.is_integer() else e for e in r] for r in transposed]
        transposed = [[str(e) for e in r] for r in transposed]
        columnWidths = [max([len(e) for e in r]) for r in transposed]
        format = " {:>" + "s} {:>".join([str(e) for e in columnWidths]) + "s}"
        f = self._open(self._outPath)
        for row in zip(*transposed):
            f.write(format.format(*row))
            f.write("\n")
        self._close(f)

    def _open(self, path): return open(path, 'w')
    def _close(self, file): file.close()

##____________________________________________________________________________||
