# Tai Sakuma <tai.sakuma@gmail.com>
import logging

import alphatwirl

##__________________________________________________________________||
def test_logger_exist():
    assert 'alphatwirl' in logging.Logger.manager.loggerDict

def test_len_handlers():
    logger = logging.getLogger('alphatwirl')
    assert len(logger.handlers) >= 1

def test_logging():
    logger = logging.getLogger('alphatwirl')
    logger.error('test message')

##__________________________________________________________________||
def test_example():
    logger_names = logging.Logger.manager.loggerDict.keys()
    loglevel_dict = {l: logging.getLogger(l).getEffectiveLevel() for l in logger_names}

    # a dict of names and levels of loggers
    # e.g.,
    # {
    #     'alphatwirl': 40,
    #     'alphatwirl.delphes': 40,
    #     'alphatwirl.loop': 40,
    #     'pandas': 0,
    # }
    #
    # https://docs.python.org/3/library/logging.html#logging-levels
    #   Level Numeric value
    #   CRITICAL 50
    #   ERROR 40
    #   WARNING 30
    #   INFO 20
    #   DEBUG 10
    #   NOTSET 0

##__________________________________________________________________||
