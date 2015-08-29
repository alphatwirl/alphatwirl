# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class ComponentLoop(object):

    def __init__(self, heppyResult, reader):
        self.reader = reader
        self.heppyResult = heppyResult
    def __call__(self):
        self.reader.begin()
        for component in self.heppyResult.components():
            self.reader.read(component)
        return self.reader.end()

##__________________________________________________________________||
