# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class EventLoopRunner(object):
    """This class runs instances of `EventLoop` and keeps the results. It
    will return the results when `end()` is called.

    """
    def __init__(self):
        self.idx = -1 # so it starts from 0
        self.idx_result_pairs = [ ]

    def __repr__(self):
        return '{}()'.format(
            self.__class__.__name__,
        )

    def begin(self):
        self.idx_result_pairs = [ ]

    def run(self, eventLoop):
        self.idx += 1
        result = eventLoop()
        self.idx_result_pairs.append((self.idx, result))
        return self.idx

    def run_multiple(self, eventLoops):
        idxs = [ ]
        for eventLoop in eventLoops:
            idxs.append(self.run(eventLoop))
        return idxs

    def poll(self):
        return self.receive()

    def receive_one(self):
        if self.idx_result_pairs:
            return self.idx_result_pairs.pop(0)
        return None

    def receive(self):
        ret = self.idx_result_pairs[:]
        del self.idx_result_pairs[:]
        return ret

    def end(self):
        return [r for _, r in self.receive()]

##__________________________________________________________________||
