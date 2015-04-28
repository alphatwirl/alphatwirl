# Tai Sakuma <tai.sakuma@cern.ch>
import array

##____________________________________________________________________________||
class EventsWithBranchAddressAccess(object):
    def __init__(self, tree, brancheNames, maxEvents = -1):
        self.file = tree.GetDirectory() # so a file won't close
        self.tree = tree
        self.nEvents = min(self.tree.GetEntries(), maxEvents) if (maxEvents > -1) else self.tree.GetEntries()
        self.iEvent = -1
        self.arrays = setBranchAddresses(brancheNames, tree)

    def __iter__(self):
        for self.iEvent in xrange(self.nEvents):
            if self.tree.GetEntry(self.iEvent) <= 0: break
            yield self
        self.iEvent = -1

    def __getattr__(self, name):
        return getattr(self.tree, name)

##____________________________________________________________________________||
def setBranchAddresses(brancheNames, tree):

    leafinfo = [inspectLeaf(tree, b) for b in brancheNames]
    leafCountNames = [l['countname'] for l in leafinfo if l['isarray']]
    leafCountInfo = [inspectLeaf(tree, l) for l in leafCountNames]

    ret = { }
    for l in leafCountInfo:
        a = array.array(l['arraytype'], [ 0 ])
        tree.SetBranchAddress(l['name'], a)
        ret[l['name']] = dict(array = a, countname = None, countarray = None)

    for l in leafinfo:
        if l['name'] in ret: continue
        if l['countmax'] is None or l['countmax'] == 0:
            a = array.array(l['arraytype'], [ 0 ])
        else:
            maxn = l['countmax']
            a = array.array(l['arraytype'], maxn*[ 0 ])
        tree.SetBranchAddress(l['name'], a)
        ret[l['name']] = dict(
            array = a,
            countname = l['countname'],
            countarray = ret[l['countname']]['array'] if l['countname'] is not None else None
        )

    return ret

##____________________________________________________________________________||
def inspectLeaf(tree, bname):

    typedic = dict(
        Double_t = 'd',
        Int_t = 'i',
    )

    leaf = tree.GetLeaf(bname)
    leafcount = leaf.GetLeafCount()
    isArray = not IsROOTNullPointer(leafcount)

    return dict(
        name = leaf.GetName(),
        ROOTtype = leaf.GetTypeName(),
        arraytype = typedic[leaf.GetTypeName()],
        isarray = isArray,
        countname = leafcount.GetName() if isArray else None,
        countROOTtype = leafcount.GetTypeName() if isArray else None,
        countarraytype = typedic[leafcount.GetTypeName()] if isArray else None,
        countmax = leafcount.GetMaximum() if isArray else None
        )

##____________________________________________________________________________||
def IsROOTNullPointer(tobject):
    try:
        tobject.GetName()
        return False
    except ReferenceError:
        return True

##____________________________________________________________________________||
