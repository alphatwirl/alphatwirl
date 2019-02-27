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
def func_deprecated():
    return 'run'

@_deprecated()
def func_deprecated_without_msg():
    return 'run'

@pytest.mark.parametrize('func, func_name, msg', [
    (func_deprecated, 'func_deprecated', 'extra message'),
    (func_deprecated_without_msg, 'func_deprecated_without_msg', ''),
])
def test_func_deprecated_logging(caplog, func, func_name, msg):
    with caplog.at_level(logging.WARNING):
        assert 'run' == func()

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name

    module_name = 'tests.unit.misc.test_deprecation'
    if sys.version_info >= (3, 0):
        expected_msg = '{}.{}() is deprecated.'.format(module_name, func_name)
    else: # python 2
        expected_msg = '{}() is deprecated.'.format(func_name)

    if msg:
        expected_msg += ' ' + msg

    assert expected_msg in caplog.records[0].msg

def test_func_deprecated_name():
    assert 'func_deprecated' == func_deprecated.__name__

def test_func_deprecated_pickle():
    p = pickle.dumps(func_deprecated)
    o = pickle.loads(p)
    assert 'run' == o()

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
    assert isinstance(c, Class)
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name
    expected = 'tests.unit.misc.test_deprecation.{} is deprecated. extra message'.format(Class.__name__)
    assert expected in caplog.records[0].msg

@pytest.mark.parametrize('Class', (ClassWithInitNoMsg, ClassWithoutInitNoMsg))
def test_class_logging_no_msg(Class, caplog):
    with caplog.at_level(logging.WARNING):
        c = Class()
    assert isinstance(c, Class)
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
    p = pickle.dumps(c)
    o = pickle.loads(p)

##__________________________________________________________________||
class ClassWithDeprecatedMethod(object):
    @_deprecated(msg='extra message')
    def method(self):
        return 'run'

def test_method_logging(caplog):
    c = ClassWithDeprecatedMethod()
    with caplog.at_level(logging.WARNING):
        assert 'run' == c.method()

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
