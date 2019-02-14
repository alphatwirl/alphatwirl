# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import sys
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

    if sys.version_info >= (3, 0):
        assert 'tests.unit.misc.test_deprecation.func() is deprecated. extra message' in caplog.records[0].msg
    else: # python 2
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

    if sys.version_info >= (3, 0):
        assert 'tests.unit.misc.test_deprecation.func_without_msg() is deprecated.' in caplog.records[0].msg
    else: # python 2
        assert 'func_without_msg() is deprecated.' in caplog.records[0].msg

##__________________________________________________________________||
@_deprecated(msg='extra message')
class ClassWithInit(object):
    def __init__(self):
        pass

@_deprecated(msg='extra message')
class ClassWithoutInit(object):
    pass

@_deprecated()
class ClassWithInitNoMsg(object):
    def __init__(self):
        pass

@_deprecated()
class ClassWithoutInitNoMsg(object):
    pass

@pytest.mark.parametrize('Class', (ClassWithInit, ClassWithoutInit))
def test_class_logging(Class, caplog):
    with caplog.at_level(logging.WARNING):
        c = Class()
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name
    expected = 'tests.unit.misc.test_deprecation.{} is deprecated. extra message'.format(Class.__name__)
    assert expected in caplog.records[0].msg

@pytest.mark.parametrize('Class', (ClassWithInitNoMsg, ClassWithoutInitNoMsg))
def test_class_logging_no_msg(Class, caplog):
    with caplog.at_level(logging.WARNING):
        c = Class()
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name
    expected = 'tests.unit.misc.test_deprecation.{} is deprecated'.format(Class.__name__)
    assert expected in caplog.records[0].msg

@pytest.mark.parametrize(
   'Class',
   (ClassWithInit, ClassWithoutInit, ClassWithInitNoMsg, ClassWithoutInitNoMsg))
def test_class_pickle(Class):
    c = Class()
    pickle.dumps(c)

##__________________________________________________________________||
class ClassWithDeprecatedMethod(object):
    @_deprecated(msg='extra message')
    def method(self):
        pass

def test_method_logging(caplog):
    c = ClassWithDeprecatedMethod()
    with caplog.at_level(logging.WARNING):
        c.method()

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name

    if sys.version_info >= (3, 0):
        assert 'tests.unit.misc.test_deprecation.ClassWithDeprecatedMethod.method() is deprecated. extra message' in caplog.records[0].msg
    else: # python 2 - not sure how to distinguish a function from an
          # unbound method
          # print(ClassWithDeprecatedMethod.method) shows
          #   <unbound method ClassWithDeprecatedMethod.method>
          # However, in the decorator, it is just <function method at 0x111ecb9b0>
        assert 'method() is deprecated. extra message' in caplog.records[0].msg

##__________________________________________________________________||
