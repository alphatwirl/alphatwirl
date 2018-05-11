# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import logging

import pytest

try:
   import cPickle as pickle
except:
   import pickle

from alphatwirl.misc.deprecation import _deprecated_func_option
from alphatwirl.misc.deprecation import _deprecated_class_method_option

##__________________________________________________________________||
@_deprecated_func_option('B')
def func_01(A=123, B=456, C=None):
    pass

def test_func_option_not_used(caplog):

    with caplog.at_level(logging.WARNING, logger='alphatwirl'):
        func_01(A=490)

    assert len(caplog.records) == 0

def test_func_option_used(caplog):

    with caplog.at_level(logging.WARNING, logger='alphatwirl'):
        func_01(B=789)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name
    assert 'func_01(): the option "B" is deprecated.' in caplog.records[0].msg

def test_func_pickle():
    pickle.dumps(func_01)

##__________________________________________________________________||
@_deprecated_func_option('C')
def func_02(A=123, B=456, C=None):
    pass

def test_func_option_used_none(caplog):

    with caplog.at_level(logging.WARNING, logger='alphatwirl'):
        func_02(C=None)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name
    assert 'func_02(): the option "C" is deprecated.' in caplog.records[0].msg

##__________________________________________________________________||
@_deprecated_func_option('B')
@_deprecated_func_option('C')
def func_03(A=123, B=456, C=None):
    pass

def test_func_option_used_double_B(caplog):

    with caplog.at_level(logging.WARNING, logger='alphatwirl'):
        func_03(B=4)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name
    assert 'func_03(): the option "B" is deprecated.' in caplog.records[0].msg

def test_func_option_used_double_C(caplog):

    with caplog.at_level(logging.WARNING, logger='alphatwirl'):
        func_03(C=None)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name
    assert 'func_03(): the option "C" is deprecated.' in caplog.records[0].msg

def test_func_option_used_double_BC(caplog):

    with caplog.at_level(logging.WARNING, logger='alphatwirl'):
        func_03(B=1, C=3)

    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == 'WARNING'
    assert caplog.records[1].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name
    assert 'test_deprecation' in caplog.records[1].name
    assert 'func_03(): the option "B" is deprecated.' in caplog.records[0].msg
    assert 'func_03(): the option "C" is deprecated.' in caplog.records[1].msg

##__________________________________________________________________||
class Class(object):
    @_deprecated_class_method_option('B')
    def __init__(A=123, B=456, C=None):
        pass

def test_class_init_option_used(caplog):

    with caplog.at_level(logging.WARNING, logger='alphatwirl'):
        Class(B=1)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name
    assert 'tests.unit.misc.test_deprecation_option.Class.__init__(): the option "B" is deprecated.' in caplog.records[0].msg

def test_class_pickle():
    c = Class()
    pickle.dumps(c)
##__________________________________________________________________||
