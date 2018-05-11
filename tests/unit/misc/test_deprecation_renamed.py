# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import logging

import pytest

try:
    import cPickle as pickle
except:
    import pickle

from alphatwirl.misc.deprecation import _renamed_class_method_option
from alphatwirl.misc.deprecation import _renamed_func_option

##__________________________________________________________________||
@_renamed_func_option(old='B', new='C')
def func_01(A=123, C=None):
    return dict(A=A, C=C)

def test_func_option_used(caplog):

    with caplog.at_level(logging.WARNING):
        r = func_01(B=455)

    assert r['C'] == 455

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name
    assert 'renamed' in caplog.records[0].msg

def test_func_option_notused(caplog):

    with caplog.at_level(logging.WARNING):
        r = func_01(C=455)

    assert r['C'] == 455

    assert len(caplog.records) == 0

def test_class_pickle():
    c = Class()
    pickle.dumps(c)

##__________________________________________________________________||

##__________________________________________________________________||
class Class(object):
    @_renamed_class_method_option(old='B', new='C')
    def __init__(self, A=123, C=None):
        self.A = A
        self.C = C

def test_class_init_option_used(caplog):

    with caplog.at_level(logging.WARNING):
        c = Class(B=455)

    assert c.C == 455

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name
    assert 'renamed' in caplog.records[0].msg

def test_class_init_option_notused(caplog):

    with caplog.at_level(logging.WARNING):
        c = Class(C=455)

    assert c.C == 455

    assert len(caplog.records) == 0

def test_class_pickle():
    c = Class()
    pickle.dumps(c)

##__________________________________________________________________||
