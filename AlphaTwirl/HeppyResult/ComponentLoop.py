# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class ComponentLoop(object):

    def __init__(self, reader):
        self.reader = reader

    def __call__(self, components):
        self.reader.begin()
        for component in components:
            self.reader.read(component)
        return self.reader.end()

##____________________________________________________________________________||
