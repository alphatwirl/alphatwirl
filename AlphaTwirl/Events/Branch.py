# Tai Sakuma <tai.sakuma@cern.ch>
import array

##____________________________________________________________________________||
class Branch(object):
    def __init__(self, name, array, countarray):
        self.name = name
        self.array = array
        self.countarray = countarray

    def __getitem__(self, i):
        if self.countarray is None and 0 != i:
            raise IndexError("the index should be zero for this branch: " + self.name + "[" + str(i) + "]")
        if self.countarray is not None and i >= self.countarray[0]:
            raise IndexError("the index is out of range: " + self.name + "[" + str(i) + "]")
        return self.array[i]

    def __len__(self):
        if self.countarray is None: return 1
        return self.countarray[0]

##____________________________________________________________________________||
class BranchManager(object):
    def __init__(self):
        self.branches = { }

    def findBranch(self, tree, name):
        if name in self.branches: return self.branches[name]

        leafNames = [l.GetName() for l in tree.GetListOfLeaves()]
        if name not in leafNames: return None
        leafInfo = inspectLeaf(tree, name)

        tree.SetBranchStatus(leafInfo['name'], 1)
        if leafInfo['countname'] is not None: tree.SetBranchStatus(leafInfo['countname'], 1)

        maxn = 1 if leafInfo['countmax'] is None or leafInfo['countmax'] == 0 else leafInfo['countmax']
        itsArray = array.array(leafInfo['arraytype'], maxn*[ 0 ])
        tree.SetBranchAddress(leafInfo['name'], itsArray)

        if leafInfo['countname'] is not None:
            itsCountBranch = self.findBranch(tree, leafInfo['countname'])
            itsCountArray = itsCountBranch.array
        else:
            itsCountArray = None

        self.branches[name] = Branch(name, itsArray, itsCountArray)
        return self.branches[name]

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
