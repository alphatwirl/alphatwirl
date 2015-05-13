# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class ReadVersionInfo(object):
    def __call__(self, path):
        file = open(path)
        return self._readImp(file)

    def _readImp(self, file):
        full = file.read()
        tag = full.split('\n')[1]
        return dict(full = full, tag = tag)

##____________________________________________________________________________||
