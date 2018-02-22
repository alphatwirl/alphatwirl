# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class EventLoopRunner(object):
    """This class runs instances of `EventLoop` and keeps the results. It
    will return the results when `end()` is called.

    """
    def __init__(self):
        self.results = [ ]

    def __repr__(self):
        return '{}(results={!r})'.format(
            self.__class__.__name__,
            self.results
        )

    def begin(self):
        self.results = [ ]

    def run(self, eventLoop):
        self.results.append(eventLoop())

    def run_multiple(self, eventLoops):
        for eventLoop in eventLoops:
            self.run(eventLoop)

    def end(self):
        return self.results

##__________________________________________________________________||
