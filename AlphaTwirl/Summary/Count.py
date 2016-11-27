# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import numpy as np
import copy

##__________________________________________________________________||
class Count(object):
    """
    Args:
        val : Unused, typically an empty tuple unless contents are given
        weight (float) : The weight
        contents : Specified contents unless None
    """

    def __init__(self, val = None, weight = 1, contents = None):

        if contents is not None:
            self.contents = np.array(contents)
            return

        self.contents = np.array((weight, weight**2))

    def __add__(self, other):
        contents = self.contents + other.contents
        return self.__class__(contents = contents)

##__________________________________________________________________||
