# Tai Sakuma <tai.sakuma@gmail.com>

import numpy as np
import copy

##__________________________________________________________________||
class Count(object):
    """
    Args:
        val : If None, initialize with 0. i.e., not counted. Otherwise,
              typically an empty tuple, counted with the weight. Ignored
              if contents are given.
        weight (float) : The weight
        contents : Specified contents unless None
    """

    def __init__(self, val=None, weight=1, contents=None):

        if contents is not None:
            ## self.contents = copy.deepcopy(contents)
            self.contents = contents
            return

        if val is None:
            self.contents = [np.array((0, 0))]
            return

        self.contents = [np.array((weight, weight**2))]

    def __add__(self, other):
        contents = [self.contents[0] + other.contents[0]]
        return self.__class__(contents=contents)

    def __radd__(self, other):
        # is called with other=0 when e.g. sum([obj1, obj2])
        if other == 0:
            return self.__class__() + self
        raise TypeError('unsupported: {!r} + {!r}'.format(other, self))

    def __repr__(self):
        return '{}(contents={!r})'.format(self.__class__.__name__, self.contents)

    def __eq__(self, other):
        if len(self.contents) != len(other.contents):
            return False
        cmps = [np.all(self.contents[i] == other.contents[i]) for i in range(len(self.contents))]
        return all(cmps)

    def __copy__(self):
        contents = [np.copy(self.contents[0])]
        return self.__class__(contents=contents)

##__________________________________________________________________||

