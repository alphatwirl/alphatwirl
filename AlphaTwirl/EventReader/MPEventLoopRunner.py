# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class MPEventLoopRunner(object):
    def __init__(self, communicationChannel):
        self.communicationChannel = communicationChannel
        self._original_readers = [ ]

    def begin(self): pass

    def run(self, eventLoop):
        self._original_readers.append(eventLoop.reader)
        self.communicationChannel.put(eventLoop)

    def end(self):
        returned_readers = self.communicationChannel.receive()
        for original, returned in zip(self._original_readers, returned_readers):
            if original is returned: continue
            original.setResults(returned.results())

##__________________________________________________________________||
