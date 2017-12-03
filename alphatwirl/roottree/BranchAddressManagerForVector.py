# Tai Sakuma <tai.sakuma@gmail.com>
import ROOT
import re

##__________________________________________________________________||
class BranchAddressManagerForVector(object):
    """The branch address manager for ROOT TTree

    This class manages ROOT.vector objects used for branch addresses
    of ROOT TTree. The main purpose of this class is to prevent
    multiple objects from being created for the same branch.

    All instances of this class share the data.
    """

    addressDict = { }

    def getVector(self, tree, branchName):
        """return the ROOT.vector object for the branch.

        """

        if (tree, branchName) in self.__class__.addressDict:
            return self.__class__.addressDict[(tree, branchName)]

        itsVector = self._getVector(tree, branchName)
        self.__class__.addressDict[(tree, branchName)] = itsVector

        return itsVector

    def _getVector(self, tree, branchName):

        leafNames = [l.GetName() for l in tree.GetListOfLeaves()]
        if branchName not in leafNames:
            return None

        leaf = tree.GetLeaf(branchName)
        typename = leaf.GetTypeName() # e.g., "vector<string>"
        match = re.search(r'^(.*)<(.*)>$', typename)
        if not match: return None
        if match.group(1) != 'vector': return None
        elementtypename = match.group(2) # e.g., "string", "int"

        tree.SetBranchStatus(leaf.GetName(), 1)
        itsVector = ROOT.vector(elementtypename)()
        tree.SetBranchAddress(leaf.GetName(), itsVector)

        return itsVector

##__________________________________________________________________||
