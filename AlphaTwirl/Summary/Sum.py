# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import numpy as np

##__________________________________________________________________||
class Sum(object):

    def __init__(self, val = None, weight = 1, contents = None):

        if contents is not None:
            self.contents = np.array(contents)
            return

        self.contents = np.array(val)*weight

    def __add__(self, other):
        contents = self.contents + other.contents
        return self.__class__(contents = contents)

    def __repr__(self):
        return '{}(contents = {!r})'.format(self.__class__.__name__, self.contents)

##__________________________________________________________________||
