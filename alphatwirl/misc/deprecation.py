# Tai Sakuma <tai.sakuma@gmail.com>

import functools
import logging

##__________________________________________________________________||
def atdeprecated(msg):
    def atdeprecated_imp(f):
        @functools.wraps(f)
        def g(*args, **kwargs):
            logger = logging.getLogger(f.__module__)
            text = '{}() is deprecated.'.format(f.__name__)
            if msg:
                text += ' ' + msg
            logger.warning(text)
            return f(*args, **kwargs)
        return g
    return atdeprecated_imp

##__________________________________________________________________||
