# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import sys
import copy
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import alphatwirl

class A(object):
    def __init__(self, a):
        pass

class B(object):
    def __init__(self):
        self._repr = 'B'

    def __repr__(self):
        return self._repr

## In Python 2 with mock 2.0.0, mock.Mock with spec sometimes cannot
## be copied or deep-copied.
## The tests in this file demonstrate.

##__________________________________________________________________||
@pytest.mark.skipif(sys.version_info < (3, 0), reason='require python 3')
def test_copy_a():
    obj = mock.Mock(spec=A)
    copy.deepcopy(obj) # doesn't work in python 2 with mock 2.0.0

@pytest.mark.skipif(sys.version_info < (3, 0), reason='require python 3')
def test_copy_b():
    obj = mock.Mock(spec=B)
    obj_copy = copy.copy(obj)
    repr(obj_copy) # doesn't work in python 2 with mock 2.0.0

##__________________________________________________________________||

