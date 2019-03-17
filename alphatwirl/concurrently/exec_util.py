#!/usr/bin/env python
import logging
import subprocess
import time

##__________________________________________________________________||
def try_executing_until_succeed(procargs, input_=None, cwd=None, sleep=2):
    while True:
        try:
            ret = exec_command(procargs=procargs, input_=input_, cwd=cwd)
            break
        except RuntimeError:
            logger = logging.getLogger(__name__)
            logger.warning('will try again in {} seconds'.format(sleep))
        time.sleep(sleep)
    return ret

##__________________________________________________________________||
def exec_command(procargs, input_=None, cwd=None):
    logger = logging.getLogger(__name__)

    command_display = compose_shortened_command_for_logging(procargs)
    logger.debug('execute: {}'.format(command_display))

    if input_ is not None:
        logger.debug('stdin: {!r}'.format(input_))

    try:
        proc = subprocess.Popen(
            procargs,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            encoding='utf-8'
        )
    except TypeError:
        # no `encoding` option in Python 2
        proc = subprocess.Popen(
            procargs,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd
        )

    stdout, stderr = proc.communicate(input_)
    logger.debug('stdout: {!r}'.format(stdout.strip()))
    logger.debug('stderr: {!r}'.format(stderr.strip()))

    success = not (proc.returncode or stderr)
    if not success:
        logger.warning('the command failed: {!r}'.format(command_display))
        raise RuntimeError(stderr)

    if not stdout:
        return [ ]

    return stdout.rstrip().split('\n')

##__________________________________________________________________||
def compose_shortened_command_for_logging(procargs):
    ellipsis = '...(({} letters))...'
    nfirst = 50
    nlast = 50
    command_display = subprocess.list2cmdline(procargs)
    if len(command_display) > nfirst + len(ellipsis) + nlast:
        command_display = '{}...(({} letters))...{}'.format(
            command_display[:nfirst],
            len(command_display) - (nfirst + nlast),
            command_display[-nlast:]
        )
    return command_display

##__________________________________________________________________||
