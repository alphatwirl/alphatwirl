# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class MPEventLoopRunner(object):

    """This class (concurrently) runs instances of `EventLoop`.

    An instance of this class needs to be initialized with a
    communication channel with workers that actually run the
    `EventLoop`::

        runner = MPEventLoopRunner(communicationChannel)

    An example of a communication channel is an instance of
    `CommunicationChannel`.

    The method `begin()` does nothing in the current version::

        runner.begin()

    In older versions, multiple processes are forked in this method.

    Then, you can give an `EventLoop` with the method `run()`::

        runner.run(eventLoop1)

    This class will send the `EventLoop` to a worker through the
    communication channel. The worker, then, runs the `EventLoop`.

    You can call the method `run()` mutiple times::

        runner.run(eventLoop2)
        runner.run(eventLoop3)
        runner.run(eventLoop4)

    If workers are in the background, this method immediately returns.
    Worker are concurrently running the event loops in the background.
    If the worker is in the foreground, this method won't return until
    the worker finishes running the event loop. Whether workers are in
    the background or foreground depends on the communication channel
    with which this class is initialized.

    After giving all event loops that you need to run to this class,
    you need to call the method `end()`::

        results = runner.end()

    If workers are in the background, this method will wait until
    workers finish running all event loops. If the worker is in the
    foreground, this method immediately returns. This method returns
    the results, the list of the values eventLoops return, sorted in
    the order given with `run()`.

    """

    def __init__(self, communicationChannel):
        self.communicationChannel = communicationChannel
        self.nruns = 0

    def __repr__(self):
        return '{}(communicationChannel = {!r}'.format(
            self.__class__.__name__,
            self.communicationChannel
        )

    def begin(self):
        """does nothing.

        Older versions of this class had implementations.
        """
        pass

    def run(self, eventLoop):
        """run the event loop in the background.

        Args:
            eventLoop (EventLoop): an event loop to run

        """

        self.nruns += 1
        return self.communicationChannel.put(eventLoop)

    def run_multiple(self, eventLoops):
        """run the event loops in the background.

        Args:
            eventLoops (list): a list of event loops to run

        """

        self.nruns += len(eventLoops)
        return self.communicationChannel.put_multiple(eventLoops)

    def poll(self):
        """Return pairs of run ids and results of finish event loops.
        """
        ret = self.communicationChannel.receive_finished()
        self.nruns -= len(ret)
        return ret

    def receive_one(self):
        """Return a pair of a run id and a result.

        This method waits until an event loop finishes.
        This method returns None if no loop is running.
        """
        if self.nruns == 0:
            return None
        ret = self.communicationChannel.receive_one()
        if ret is not None:
            self.nruns -= 1
        return ret

    def receive(self):
        """Return pairs of run ids and results.

        This method waits until all event loops finish
        """
        ret = self.communicationChannel.receive_all()
        self.nruns -= len(ret)
        if self.nruns > 0:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(
                'too few results received: {} results received, {} more expected'.format(
                    len(ret), self.nruns))
        elif self.nruns < 0:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(
                'too many results received: {} results received, {} too many'.format(
                    len(ret), -self.nruns))
        return ret

    def end(self):
        """wait until all event loops end and returns the results.

        """

        results = self.communicationChannel.receive()

        if self.nruns != len(results):
            import logging
            logger = logging.getLogger(__name__)
            # logger.setLevel(logging.DEBUG)
            logger.warning(
                'too few results received: {} results received, {} expected'.format(
                    len(results),
                    self.nruns
                ))

        return results

##__________________________________________________________________||
