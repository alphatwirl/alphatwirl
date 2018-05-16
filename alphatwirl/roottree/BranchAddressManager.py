# Tai Sakuma <tai.sakuma@gmail.com>
import array

import ROOT

from .inspect import is_ROOT_null_pointer

##__________________________________________________________________||
class BranchAddressManager(object):
    """The branch address manager for ROOT TTree

    This class manages array.array objects used for branch addresses
    of ROOT TTree. The main purpose of this class is to prevent
    multiple arrays from being created for the same branch.


    All instances of this class share the data.
    """

    arrayDict = { }
    counterArrayDict = { }

    def getArrays(self, tree, branchName):
        """return the array.array objects for the branch and its counter branch

        This method returns a pair of the array.array objects. The first one is
        for the given tree and branch name. The second one is for its counter
        branch. The second one will be None when the branch does not have a
        counter. A pair of None will be returned when the tree does not have
        the branch.

        """
        itsArray = self._getArray(tree, branchName)
        if itsArray is None: return None, None
        itsCountArray = self._getCounterArray(tree, branchName)
        return itsArray, itsCountArray

    def _getArray(self, tree, branchName):

        if (tree, branchName) in self.__class__.arrayDict:
            return self.__class__.arrayDict[(tree, branchName)]

        self._createArraysForBranchAndCounter(tree, branchName)
        return self.__class__.arrayDict[(tree, branchName)]

    def _getCounterArray(self, tree, branchName):
        if (tree, branchName) in self.__class__.counterArrayDict:
            return self.__class__.counterArrayDict[(tree, branchName)]
        return None

    def _createArraysForBranchAndCounter(self, tree, branchName):

        leafNames = [l.GetName() for l in tree.GetListOfLeaves()]
        if branchName not in leafNames:
            self.__class__.arrayDict[(tree, branchName)] = None
            return

        leafInfo = inspectLeaf(tree, branchName)
        if leafInfo['arraytype'] is None:
            self.__class__.arrayDict[(tree, branchName)] = None
            return

        tree.SetBranchStatus(leafInfo['name'], 1)
        if leafInfo['countname'] is not None: tree.SetBranchStatus(leafInfo['countname'], 1)

        maxn = 1 if leafInfo['countmax'] is None or leafInfo['countmax'] == 0 else leafInfo['countmax']
        itsArray = array.array(leafInfo['arraytype'], maxn*[ 0 ])
        tree.SetBranchAddress(leafInfo['name'], itsArray)

        if leafInfo['countname'] is not None:
            itsCountArray = self._getArray(tree, leafInfo['countname'])
        else:
            itsCountArray = None

        self.__class__.arrayDict[(tree, branchName)] = itsArray
        self.__class__.counterArrayDict[(tree, branchName)] = itsCountArray

##__________________________________________________________________||
def inspectLeaf(tree, bname):


    # This dict maps a ROOT type to a type code of the python array
    # https://root.cern.ch/root/html/RtypesCore.h
    # https://docs.python.org/2/library/array.html
    typedic = dict(
        Char_t='b',
        UChar_t='B',
        Short_t='h',
        UShort_t='H',
        Int_t='i',
        UInt_t='I',
        Float_t='f',
        Double_t='d',
        Long64_t='l',
        ULong64_t='L',
        Bool_t='b',
    )

    leaf = tree.GetLeaf(bname)
    leafcount = leaf.GetLeafCount()
    isArray = not is_ROOT_null_pointer(leafcount)

    countmax = None
    if isArray:
        countmax = _get_countmax(leafcount, tree, bname)

    return dict(
        name=leaf.GetName(),
        ROOTtype=leaf.GetTypeName(),
        arraytype=typedic[leaf.GetTypeName()] if leaf.GetTypeName() in typedic else None,
        isarray=isArray,
        countname=leafcount.GetName() if isArray else None,
        countROOTtype=leafcount.GetTypeName() if isArray else None,
        countarraytype=typedic[leafcount.GetTypeName()] if isArray else None,
        countmax=countmax,
        )

def _get_countmax(leafcount, tree, bname):
    # If the tree is a chain, leafcount.GetMaximum() only returns the
    # maximum in the current file. The `countmax` needs to be the
    # maximum in all files. Not very efficient or elegant, the current
    # implementation opens all files in the chain and finds the
    # maximum.

    try:
        tobjarray_files = tree.GetListOfFiles()
    except AttributeError:
        # the tree is not a chain
        return leafcount.GetMaximum()

    if 0 == tobjarray_files.GetLast():
        # the chain has only one file
        return leafcount.GetMaximum()

    filepahts = (f.GetTitle() for f in tobjarray_files)
    files = (ROOT.TFile.Open(p) for p in filepahts)
    trees = (f.Get(tree.GetName()) for f in files)
    leaves = (t.GetLeaf(bname) for t in trees)
    leafcounts = (l.GetLeafCount() for l in leaves)
    countmaxs = (l.GetMaximum() for l in leafcounts)
    countmax = max(countmaxs)
    return countmax

##__________________________________________________________________||
