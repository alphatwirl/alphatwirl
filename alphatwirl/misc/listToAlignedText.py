# Tai Sakuma <tai.sakuma@gmail.com>

import functools
import logging

from .list_to_aligned_text import list_to_aligned_text

##__________________________________________________________________||
def atdeprecated(msg):
    def atdeprecated_imp(f):
        @functools.wraps(f)
        def g(*args, **kwargs):
            logger = logging.getLogger(__name__)
            text = '{}() is deprecated.'.format(f.__name__)
            if msg:
                text += ' ' + msg
            logger.warning(text)
            return f(*args, **kwargs)
        return g
    return atdeprecated_imp

##__________________________________________________________________||
@atdeprecated(msg='use list_to_aligned_text() instead.')
def listToAlignedText(src, formatDict = None, leftAlignLastColumn = False):
    return list_to_aligned_text(
        src = src,
        format_dict = formatDict,
        left_align_last_column = leftAlignLastColumn
    )
##__________________________________________________________________||
