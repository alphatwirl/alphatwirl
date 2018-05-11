# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import inspect
import functools
import logging

##__________________________________________________________________||
def _deprecated(msg=''):

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
def _deprecated_func_option(option, msg=''):
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
def _deprecated_class_method_option(option, msg=''):
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
def _renamed_func_option(old, new, msg=''):
    def _imp(f):
        module_name = f.__module__
        logger = logging.getLogger(module_name)
        func_name = f.__name__
        def g(*args, **kwargs):
            if old in kwargs:
                name = '{}.{}'.format(module_name, func_name)
                text = '{}(): the option "{}" is renamed "{}".'.format(name, old, new)
                text += ' "{}={}" is given.'.format(old, kwargs[old])
                if msg:
                    text += ' ' + msg
                logger.warning(text)
                kwargs[new] = kwargs.pop(old)
            return f(*args, **kwargs)
        return g
    return _imp

##__________________________________________________________________||
def _renamed_class_method_option(old, new, msg=''):
    def _imp(f):
        module_name = f.__module__
        logger = logging.getLogger(module_name)
        method_name = f.__name__
        def g(*args, **kwargs):
            if old in kwargs:
                name = '{}.{}.{}'.format(module_name, args[0].__class__.__name__, method_name)
                text = '{}(): the option "{}" is renamed "{}".'.format(name, old, new)
                text += ' "{}={}" is given.'.format(old, kwargs[old])
                if msg:
                    text += ' ' + msg
                logger.warning(text)
                kwargs[new] = kwargs.pop(old)
            return f(*args, **kwargs)
        return g
    return _imp

##__________________________________________________________________||
@_deprecated(msg='use _deprecated() instead')
def atdeprecated(*args, **kwargs):
    return _deprecated(*args, **kwargs)

@_deprecated(msg='use _deprecated_func_option() instead')
def atdeprecated_func_option(*args, **kwargs):
    return _deprecated_func_option(*args, **kwargs)

@_deprecated(msg='use _deprecated_class_method_option() instead')
def atdeprecated_class_method_option(*args, **kwargs):
    return _deprecated_class_method_option(*args, **kwargs)

@_deprecated(msg='use _renamed_func_option() instead')
def atrenamed_func_option(*args, **kwargs):
    return _renamed_func_option(*args, **kwargs)

@_deprecated(msg='use _renamed_class_method_option() instead')
def atrenamed_class_method_option(*args, **kwargs):
    return _renamed_class_method_option(*args, **kwargs)

##__________________________________________________________________||
