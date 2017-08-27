# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
def IsROOTNullPointer(tobject):
    try:
        tobject.GetName()
        return False
    except ReferenceError:
        return True

##__________________________________________________________________||
def inspect_tree(tree):
    ret = {  }
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
    isArray = not IsROOTNullPointer(leafcount)
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
