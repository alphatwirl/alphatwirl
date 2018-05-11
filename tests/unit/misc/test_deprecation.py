# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import logging

import pytest

try:
   import cPickle as pickle
except:
   import pickle

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='extra message')
def func():
    pass

def test_func_logging(caplog):
    with caplog.at_level(logging.WARNING):
        func()

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name
    assert 'func() is deprecated. extra message' in caplog.records[0].msg

def test_func_name():
    assert  'func' == func.__name__

def test_func_pickle():
    pickle.dumps(func)

@_deprecated()
def func_without_msg():
    pass

def test_func_logging_without_msg(caplog):
    with caplog.at_level(logging.WARNING):
        func_without_msg()

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name
    assert 'func_without_msg() is deprecated.' in caplog.records[0].msg

##__________________________________________________________________||
@_deprecated(msg='extra message')
class ClassWithInit(object):
    def __init__(self):
        pass

@_deprecated(msg='extra message')
class ClassWithoutInit(object):
    pass

@pytest.mark.parametrize('Class', (ClassWithInit, ClassWithoutInit))
def test_class_logging(Class, caplog):
    with caplog.at_level(logging.WARNING):
        c = Class()
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name
    expected = '{} is deprecated. extra message'.format(Class.__name__)
    assert expected in caplog.records[0].msg

@pytest.mark.parametrize('Class', (ClassWithInit, ClassWithoutInit))
def test_class_pickle(Class):
    c = Class()
    pickle.dumps(c)

##__________________________________________________________________||
