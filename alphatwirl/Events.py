# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class Events(object):
    def __init__(self, tree, maxEvents = -1):
        self.file = tree.GetDirectory() # so a file won't close
        self.tree = tree
        self.nEvents = min(self.tree.GetEntries(), maxEvents) if (maxEvents > -1) else self.tree.GetEntries()

    def __iter__(self):
        return self._next()

    def _next(self):
        iEvent = 0
        while iEvent < self.nEvents:
            if self.tree.GetEntry(iEvent) <= 0: return
            iEvent += 1
            yield self

    def __getattr__(self, name):
        return getattr(self.tree, name)

##____________________________________________________________________________||
if __name__ == '__main__':
    pass
