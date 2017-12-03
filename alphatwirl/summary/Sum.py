# Tai Sakuma <tai.sakuma@gmail.com>

import numpy as np
import copy

##__________________________________________________________________||
class Sum(object):

    def __init__(self, val = None, weight = 1, contents = None):

        if contents is not None:
            self.contents = contents
            return

        if val is None:
            self.contents = [np.array([0])] # will be broadcasted when
                                            # added with more than 1
                                            # element
            return

        self.contents = [np.array(val)*weight]

    def __add__(self, other):
        contents = [self.contents[0] + other.contents[0]]
        return self.__class__(contents = contents)

    def __radd__(self, other):
        # is called with other = 0 when e.g. sum([obj1, obj2])
        if other == 0:
            return self.__class__() + self
        raise TypeError('unsupported: {!r} + {!r}'.format(other, self))

    def __repr__(self):
        return '{}(contents = {!r})'.format(self.__class__.__name__, self.contents)

    def __eq__(self, other):
        if len(self.contents) != len(other.contents): return False
        return all([np.all(self.contents[i] == other.contents[i]) for i in range(len(self.contents))])

    def __copy__(self):
        contents = [np.copy(self.contents[0])]
        return self.__class__(contents = contents)

##__________________________________________________________________||
