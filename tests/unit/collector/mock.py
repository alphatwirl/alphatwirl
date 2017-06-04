import copy

##__________________________________________________________________||
class MockReader(object):
    def __init__(self, summarizer):
        self.summarizer = summarizer

    def results(self):
        return self.summarizer

    def __repr__(self):
        return '{}(summarizer = {!r})'.format(
            self.__class__.__name__,
            self.summarizer
        )

##__________________________________________________________________||
class MockSummarizer(object):
    def __init__(self, results):
        self._results = results

    def __repr__(self):
        return '{}({!r})'.format(
            self.__class__.__name__,
            self._results
        )

    def __add__(self, other):
        if other == 0:
            res = copy.copy(self._results)
        else:
            res = copy.copy(self._results) + copy.copy(other._results)
        return self.__class__(res)

    def __radd__(self, other):
        return self.__add__(other)

    def to_tuple_list(self):
        return self._results

##__________________________________________________________________||
