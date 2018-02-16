# Tai Sakuma <tai.sakuma@gmail.com>
import logging

from alphatwirl.misc.deprecation import atdeprecated

##__________________________________________________________________||
@atdeprecated(msg='extra message')
def func():
    pass

##__________________________________________________________________||
def test_func_logging(caplog):
    with caplog.at_level(logging.WARNING, logger='alphatwirl'):
        func()

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'WARNING'
    assert 'test_deprecation' in caplog.records[0].name
    assert 'func() is deprecated. extra message' == caplog.records[0].msg

def test_func_name():
    assert  'func' == func.__name__

##__________________________________________________________________||
