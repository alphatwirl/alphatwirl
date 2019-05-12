# Tai Sakuma <tai.sakuma@gmail.com>
import functools

##__________________________________________________________________||
def simple_repr(func):
    def _wrap(func):
        return simple_repr_(func)
    return _wrap

class simple_repr_(object):
    """simplify repr of a function

    The default repr of a function includes an address,
    e.g., `<function func at 0x103f0ef28>`.

    This class simplifies it to only a function name,
    i.e., `func`

    An example usage as a decorator follows.

       >>> @simple_repr
       ... def func():
       ...     pass
       ...
       >>> print(func)
       func

    The implementation is inspired by
    https://stackoverflow.com/questions/20093811/how-do-i-change-the-representation-of-a-python-function/20094262#20094262
    https://stackoverflow.com/a/10875517/7309855

    Parameters
    ----------
    functor : callable
        A function whose repr to be modified

    """

    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)
        # self.__name__ = func.__name__
        # self.__doc__ = func.__doc__

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __repr__(self):
        return self.func.__name__

##__________________________________________________________________||
