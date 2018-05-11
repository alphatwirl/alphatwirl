# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
import os
from .ReadComponentConfig import ReadComponentConfig
from .Analyzer import Analyzer

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='heppyresult has been moved to https://github.com/alphatwirl/atheppy.')
class Component(object):
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.analyzerNames = [n for n in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, n))]

        self._anaDict = { }
        self._cfg = None
        self._readConfig = ReadComponentConfig()

    def __repr__(self):
        name_value_pairs = (
            ('name', self.name),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __getattr__(self, name):
        if name not in self._anaDict:
            if name not in self.analyzerNames:
                raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))
            path = os.path.join(self.path, name)
            self._anaDict[name] = Analyzer(path)
        return self._anaDict[name]

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, dict):
        self.__dict__ = dict

    def analyzers(self):
        return [getattr(self, n) for n in self.analyzerNames]

    def config(self):
        if self._cfg is None:
            path = os.path.join(self.path, 'config.txt')
            self._cfg = self._readConfig(path)
        return self._cfg

##__________________________________________________________________||
