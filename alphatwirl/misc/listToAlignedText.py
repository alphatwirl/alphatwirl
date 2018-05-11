# Tai Sakuma <tai.sakuma@gmail.com>
from .list_to_aligned_text import list_to_aligned_text
from alphatwirl.misc.deprecation import _deprecated

##__________________________________________________________________||
@_deprecated(msg='use list_to_aligned_text() instead.')
def listToAlignedText(src, formatDict=None, leftAlignLastColumn=False):
    return list_to_aligned_text(
        src=src,
        format_dict=formatDict,
        left_align_last_column=leftAlignLastColumn
    )
##__________________________________________________________________||
