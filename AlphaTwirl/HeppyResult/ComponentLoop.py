# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class ComponentLoop(object):

    def __init__(self, components, reader):
        self.reader = reader
        self.components = components
    def __call__(self):
        self.reader.begin()
        for component in self.components:
            self.reader.read(component)
        return self.reader.end()

##____________________________________________________________________________||
