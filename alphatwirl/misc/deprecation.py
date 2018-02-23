# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import inspect
import functools
import logging

##__________________________________________________________________||
def atdeprecated(msg=''):

    def _decorate_class(c, msg):
        module_name = c.__module__
        logger = logging.getLogger(module_name)
        class_name = c.__name__
        name = '{}.{}'.format(module_name, class_name)
        text = '{} is deprecated.'.format(name)
        if msg:
            text += ' ' + msg

            original_init = c.__init__

        def init(*args, **kwargs):
            logger.warning(text)
            return original_init(*args, **kwargs)

        c.__init__ = init
        return c

    def _decorate_func(f, msg):
        module_name = f.__module__
        logger = logging.getLogger(module_name)
        name = f.__name__
        name = '{}.{}'.format(module_name, name)
        text = '{}() is deprecated.'.format(name)
        if msg:
            text += ' ' + msg

        @functools.wraps(f)
        def g(*args, **kwargs):
            logger.warning(text)
            return f(*args, **kwargs)
        return g

    def _imp(f):
        if inspect.isclass(f):
            return _decorate_class(f, msg)
        return _decorate_func(f, msg)
    return _imp

##__________________________________________________________________||
def atdeprecated_func_option(option, msg=''):
    def _imp(f):
        module_name = f.__module__
        logger = logging.getLogger(module_name)
        func_name = f.__name__

        @functools.wraps(f)
        def g(*args, **kwargs):
            if option in kwargs:
                name = '{}.{}'.format(module_name, func_name)
                text = '{}(): the option "{}" is deprecated.'.format(name, option)
                text += ' "{}={}" is given.'.format(option, kwargs[option])
                if msg:
                    text += ' ' + msg
                logger.warning(text)
            return f(*args, **kwargs)
        return g
    return _imp

##__________________________________________________________________||
def atdeprecated_class_method_option(option, msg=''):
    def _imp(f):
        module_name = f.__module__
        logger = logging.getLogger(module_name)
        method_name = f.__name__
        def g(*args, **kwargs):
            if option in kwargs:
                name = '{}.{}.{}'.format(module_name, args[0].__class__.__name__, method_name)
                text = '{}(): the option "{}" is deprecated.'.format(name, option)
                text += ' "{}={}" is given.'.format(option, kwargs[option])
                if msg:
                    text += ' ' + msg
                logger.warning(text)
            return f(*args, **kwargs)
        return g
    return _imp

##__________________________________________________________________||
