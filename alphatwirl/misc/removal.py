# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import inspect
import functools
import logging

##__________________________________________________________________||
def _removed(msg=''):
    def _decorate_class(c, msg):
        module_name = c.__module__
        logger = logging.getLogger(module_name)
        class_name = c.__name__
        name = '{}.{}'.format(module_name, class_name)
        text = '{} is removed.'.format(name)
        if msg:
            text += ' ' + msg

        def init(*args, **kwargs):
            logger.error(text)
            raise RuntimeError(msg)

        c.__init__ = init
        return c

    def _decorate_func(f, msg):
        module_name = f.__module__
        logger = logging.getLogger(module_name)
        name = f.__name__
        name = '{}.{}'.format(module_name, name)
        text = '{}() is removed.'.format(name)
        if msg:
            text += ' ' + msg

        @functools.wraps(f)
        def g(*args, **kwargs):
            logger.error(text)
            raise RuntimeError(msg)
        return g

    def _imp(f):
        if inspect.isclass(f):
            return _decorate_class(f, msg)
        return _decorate_func(f, msg)
    return _imp

##__________________________________________________________________||
