#!/usr/bin/env python
import logging
import subprocess
import time

##__________________________________________________________________||
def try_executing_until_succeed(procargs, sleep=2):

    logger = logging.getLogger(__name__)

    while True:

        #
        command_display = compose_shortened_command_for_logging(procargs)
        logger.debug('execute: {!r}'.format(command_display))

        #
        proc = subprocess.Popen(
            procargs,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        success = not (proc.returncode or stderr)

        #
        if success: break

        #
        if stderr: logger.warning(stderr.strip())
        logger.warning('the command failed: {!r}. will try again in {} seconds'.format(command_display, sleep))

        #
        time.sleep(sleep)

    if not stdout: return [ ]
    return stdout.rstrip().split(b'\n')

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
