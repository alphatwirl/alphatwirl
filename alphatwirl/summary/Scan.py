# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
import numpy as np
import copy

##__________________________________________________________________||
class Scan(object):
    def __init__(self, val = None, weight = 1, contents = None):

        if contents is not None:
            self.contents = contents
            return

        if val is None:
            self.contents = [ ]
            return

        self.contents = [val]

    def __add__(self, other):
        contents = self.contents + other.contents
        return self.__class__(contents = contents)

    def __radd__(self, other):
        # is called with other = 0 when e.g. sum([obj1, obj2])
        if other == 0:
            return self.__class__() + self
        raise TypeError('unsupported: {!r} + {!r}'.format(other, self))

    def __repr__(self):
        return '{}(contents = {})'.format(self.__class__.__name__, self.contents)

    def __eq__(self, other):
        return self.contents == other.contents

    def __copy__(self):
        contents = list(self.contents)
        return self.__class__(contents = contents)

##__________________________________________________________________||
