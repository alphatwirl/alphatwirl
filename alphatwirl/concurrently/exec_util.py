# Tai Sakuma <sakuma@cern.ch>
from .condor import exec_util

from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='use alphatwirl.concurrently.condor.exec_util.try_executing_until_succeed() instead')
def try_executing_until_succeed(*args, **kwargs):
    return exec_util.try_executing_until_succeed(*args, **kwargs)

##__________________________________________________________________||
@_deprecated(msg='use alphatwirl.concurrently.condor.exec_util.exec_command() instead')
def exec_command(*args, **kwargs):
    return exec_util.exec_command(*args, **kwargs)

##__________________________________________________________________||
@_deprecated(msg='use alphatwirl.concurrently.condor.exec_util.compose_shortened_command_for_logging() instead')
def compose_shortened_command_for_logging(*args, **kwargs):
    return exec_util.compose_shortened_command_for_logging(*args, **kwargs)

##__________________________________________________________________||
