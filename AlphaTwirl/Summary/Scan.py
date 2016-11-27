# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import numpy as np
import copy

##__________________________________________________________________||
class Scan(object):
    def __init__(self, val = None, weight = 1, contents = None):

        if contents is not None:
            self.contents = copy.deepcopy(contents)
            return

        if val is not None:
            self.contents = [copy.deepcopy(val)]
            return

        self.contents = [ ]

    def __add__(self, other):
        contents = copy.deepcopy(self.contents)
        contents.extend(other.contents)
        return self.__class__(contents = contents)

    def __repr__(self):
        return '{}(contents = {})'.format(self.__class__, self.contents)

##__________________________________________________________________||
