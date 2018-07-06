# Tai Sakuma <tai.sakuma@gmail.com>
import logging

from .WeightCalculatorOne import WeightCalculatorOne

##__________________________________________________________________||
class Reader(object):
    def __init__(self, keyValComposer, summarizer, nextKeyComposer=None,
                 weightCalculator=WeightCalculatorOne(),
                 nevents=None):
        self.keyValComposer = keyValComposer
        self.summarizer = summarizer
        self.weightCalculator = weightCalculator
        self.nextKeyComposer = nextKeyComposer

        self.nevents = nevents
        self.ievent = 0

        self._repr_pairs = [
            ('keyValComposer', self.keyValComposer),
            ('summarizer', self.summarizer),
            ('nextKeyComposer', self.nextKeyComposer),
            ('weightCalculator', self.weightCalculator),
            ('nevents', self.nevents),
        ]

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in self._repr_pairs]),
        )

    def __str__(self):
        nwidth = max(len(n) for n, _ in self._repr_pairs)
        nwidth += 4
        return '{}:\n{}'.format(
            self.__class__.__name__,
            '\n'.join(['{:>{}}: {!r}'.format(n, nwidth, v) for n, v in self._repr_pairs]),
        )

    def begin(self, event):
        self.keyValComposer.begin(event)

    def event(self, event):
        if self.nevents is not None and self.nevents <= self.ievent:
            return

        self.ievent += 1

        try:
            keyvals = self.keyValComposer(event)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(e)
            logger.error(self)
            raise

        weight = self.weightCalculator(event)
        for key, val in keyvals:
            self.summarizer.add(key=key, val=val, weight=weight)

    def end(self):
        if self.nextKeyComposer is None:
            return

        for key in sorted(self.summarizer.keys()):
            nextKeys = self.nextKeyComposer(key)
            for nextKey in nextKeys:
                self.summarizer.add_key(nextKey)

    def merge(self, other):
        self.summarizer += other.summarizer

    def results(self):
        return self.summarizer

##__________________________________________________________________||
