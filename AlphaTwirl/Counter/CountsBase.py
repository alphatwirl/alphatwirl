# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
import abc

##____________________________________________________________________________||
class CountsBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def count(self): pass

    @abc.abstractmethod
    def valNames(self): pass

    @abc.abstractmethod
    def setResults(self): pass

    @abc.abstractmethod
    def results(self): pass

##____________________________________________________________________________||
