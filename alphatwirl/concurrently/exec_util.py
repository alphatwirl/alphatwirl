#!/usr/bin/env python
import logging
import subprocess
import time

##__________________________________________________________________||
def try_executing_until_succeed(procargs):

    sleep = 2
    logger = logging.getLogger(__name__)

    while True:

        # logging
        ellipsis = '...(({} letters))...'
        nfirst = 50
        nlast = 50
        command_display = '{} {}'.format(procargs[0], ' '.join([repr(a) for a in procargs[1:]]))
        if len(command_display) > nfirst + len(ellipsis) + nlast:
            command_display = '{}...(({} letters))...{}'.format(
                command_display[:nfirst],
                len(command_display) - (nfirst + nlast),
                command_display[-nlast:]
            )
        logger.debug('execute: {}'.format(command_display))

        #
        proc = subprocess.Popen(
            procargs,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr =  proc.communicate()
        success = not (proc.returncode or stderr)

        #
        if success: break

        #
        if stderr: logger.warning(stderr.strip())
        logger.warning('the command failed: {}. will try again in {} seconds'.format(command_display, sleep))

        #
        time.sleep(sleep)

    if not stdout: return [ ]
    return stdout.rstrip().split('\n')

##__________________________________________________________________||
