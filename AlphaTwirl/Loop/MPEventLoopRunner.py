# Tai Sakuma <tai.sakuma@cern.ch>

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

        runner.end()

    If workers are in the background, this method will wait until
    workers finish running all event loops. If the worker is in the
    foreground, this method immediately returns.

    """

    def __init__(self, communicationChannel):
        self.communicationChannel = communicationChannel
        self._original_readers = [ ]

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

        self._original_readers.append(eventLoop.reader)
        self.communicationChannel.put(eventLoop)

    def end(self):
        """wait until all event loops end

        In addition, if necessary, this method also carries out a
        somewhat complex copying operation because of the duplication
        of objects that occurs in multiprocessing.

        If eventLoops were executed in other processes, the readers in
        the main process did not read the events; therefore, they
        don't have the results. The readers in other processes read
        the events. They have the results. The readers in other
        process are pickled and sent back to the main process.
        However, these returned readers are no longer the same objects
        as the original readers in the main process.

        The method copies the returned readers to the original readers
        if they are different objects.

        """

        returned_readers = self.communicationChannel.receive()

        if len(self._original_readers) != len(returned_readers):
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(
                'the same number of the readers were not received: {} readers put, {} readers received'.format(
                    len(self._original_readers),
                    len(returned_readers)
                ))

        for original, returned in zip(self._original_readers, returned_readers):
            if original is returned: continue
            original.copy_from(returned)

##__________________________________________________________________||
