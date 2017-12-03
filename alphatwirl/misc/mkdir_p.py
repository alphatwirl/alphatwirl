# Tai Sakuma <tai.sakuma@gmail.com>

import os, errno
import logging

##__________________________________________________________________||
def mkdir_p(path):

    logger = logging.getLogger(__name__)

    # http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    try:
        os.makedirs(path)
        logger.info('created a directory, {}'.format(path))

    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            loglevel = logging.getLevelName('DEBUG') - 1 # one level below DEBUG
            logger.log(loglevel, 'tried to create a directory, {}. already existed'.format(path))
            pass
        else: raise

##__________________________________________________________________||
