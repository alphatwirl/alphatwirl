# Tai Sakuma <tai.sakuma@cern.ch>

import logging
from .list_to_aligned_text import list_to_aligned_text

##__________________________________________________________________||
def listToAlignedText(src, formatDict = None, leftAlignLastColumn = False):

    logger = logging.getLogger(__name__)
    logger.warning('the function "{}" is renamed  "{}". The arguments are renamed as well'.format(
        "listToAlignedText", "list_to_aligned_text")
    )

    return list_to_aligned_text(
        src = src,
        format_dict = formatDict,
        left_align_last_column = leftAlignLastColumn
    )
##__________________________________________________________________||
