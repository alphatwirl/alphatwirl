# Tai Sakuma <sakuma@fnal.gov>

##____________________________________________________________________________||
import abc

##____________________________________________________________________________||
class CountsBase(object):
    __metaclass__ = abc.ABCMeta

    def setKeyComposer(self, keyComposer):
        self.keyComposer = keyComposer

    @abc.abstractmethod
    def count(self): pass

    @abc.abstractmethod
    def valNames(self): pass

    @abc.abstractmethod
    def setResults(self): pass

    @abc.abstractmethod
    def results(self): pass

##____________________________________________________________________________||
