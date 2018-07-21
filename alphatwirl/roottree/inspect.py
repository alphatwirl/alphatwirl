# Tai Sakuma <tai.sakuma@gmail.com>
import logging

import ROOT

##__________________________________________________________________||
def is_ROOT_null_pointer(tobject):
    try:
        tobject.GetName()
        return False
    except ReferenceError:
        return True

##__________________________________________________________________||
def get_entries_in_tree_in_file(path, tree_name):

    ##
    file_ = ROOT.TFile.Open(path)
    if is_ROOT_null_pointer(file_) or file_.IsZombie():
        logger = logging.getLogger(__name__)
        logger.warning('cannot open {}'.format(path))
        return None

    ##
    tree = file_.Get(tree_name)
    if is_ROOT_null_pointer(tree):
        logger = logging.getLogger(__name__)
        logger.warning(
            'cannot find tree "{}" '
            'in {}'.format(tree_name, path))
        return None

    ##
    ret = tree.GetEntriesFast()
    file_.Close()
    return ret

##__________________________________________________________________||
def inspect_tree(tree):
    ret = { }
    ret['leaves'] = [inspect_leaf(leaf) for leaf in tree.GetListOfLeaves()]
    return ret

##__________________________________________________________________||
def inspect_leaf(leaf):
    ret = { }
    ret.update(inspect_leaf_definition(leaf))
    ret.update(inspect_leaf_size(leaf))
    return ret

##__________________________________________________________________||
def inspect_leaf_definition(leaf):
    leafcount = leaf.GetLeafCount()
    isArray = not is_ROOT_null_pointer(leafcount)
    ret = { }
    ret['name'] = leaf.GetName()
    ret['type'] = leaf.GetTypeName()
    ret['isarray'] = '1' if isArray else '0'
    ret['countname'] = leafcount.GetName() if isArray else None
    ret['title'] = leaf.GetBranch().GetTitle()
    return ret

##__________________________________________________________________||
def inspect_leaf_size(leaf):
    ret = { }
    zipbytes = leaf.GetBranch().GetZipBytes()/1024.0/1024.0 # MB
    totalsize = leaf.GetBranch().GetTotalSize()/1024.0/1024.0 # MB
    ret['size'] = zipbytes
    ret['uncompressed_size'] = totalsize
    ret['compression_factor'] = totalsize/zipbytes if zipbytes > 0 else 0
    return ret

##__________________________________________________________________||
