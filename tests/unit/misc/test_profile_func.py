# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import os

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from alphatwirl.misc import profile_func, print_profile_func

##__________________________________________________________________||
def test_profile_func():
    func = mock.Mock()
    profile_func(func)

##__________________________________________________________________||
def test_print_profile_func(tmpdir_factory):
    tmpdir = str(tmpdir_factory.mktemp(''))
    func = mock.Mock()
    print(tmpdir)
    profile_out_path = os.path.join(tmpdir, 'profile.txt')
    print_profile_func(func, profile_out_path=profile_out_path)

##__________________________________________________________________||
