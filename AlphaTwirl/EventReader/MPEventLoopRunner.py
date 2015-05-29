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
        # If eventLoops were executed in other processes, the readers
        # in the main process do not read the events; therefore, they
        # don't have the results. The readers in other processes read
        # the events. They have the results. The readers in other
        # process are pickled and sent back to the main process.
        # However, these returned readers are no longer the same
        # objects as the original readers in the main process.

        # The following lines of the code copy the results in the
        # returned readers to the original readers if they are
        # different objects.

        returned_readers = self.communicationChannel.receive()
        for original, returned in zip(self._original_readers, returned_readers):
            if original is returned: continue
            original.setResults(returned.results())

##__________________________________________________________________||
