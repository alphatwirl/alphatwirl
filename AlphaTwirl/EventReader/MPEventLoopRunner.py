# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class MPEventLoopRunner(object):
    def __init__(self, communicationChannel):
        self.communicationChannel = communicationChannel

    def begin(self):
        self._allReaders = { }

    def run(self, eventLoop):

        # add id so can collect later
        reader = eventLoop.reader
        reader.id = id(reader)
        self._allReaders[id(reader)] = reader

        self.communicationChannel.put(eventLoop)

    def end(self):

        readers = self.communicationChannel.receive()
        for reader in readers:
            self._allReaders[reader.id].setResults(reader.results())

##__________________________________________________________________||
