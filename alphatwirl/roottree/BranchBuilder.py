# Tai Sakuma <tai.sakuma@gmail.com>
import logging

from .Branch import Branch
from .BranchAddressManager import BranchAddressManager
from .BranchAddressManagerForVector import BranchAddressManagerForVector

from .inspect import is_ROOT_null_pointer

##__________________________________________________________________||
branchAddressManager = BranchAddressManager()
branchAddressManagerForVector = BranchAddressManagerForVector()

##__________________________________________________________________||
class BranchBuilder(object):
    """This class builds a branch.

    A branch is an object with data whose address is set in a tree.

    All instances of this class share the data.

    """

    itsdict = { }

    def __repr__(self):
        name_value_pairs = (
            ('itsdict', self.__class__.itsdict),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{}={!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def register_tree(self, tree):
        if not tree in self.__class__.itsdict:
            tree.SetBranchStatus('*', 0)
            self.__class__.itsdict[tree] = { }

    def __call__(self, tree, name):

        if not tree in self.__class__.itsdict:
            logger = logging.getLogger(__name__)
            logger.warning('tree is not registered: {!r}'.format(tree))
            self.__class__.itsdict[tree] = { }

        itsdict_tree = self.__class__.itsdict[tree]
        if name in itsdict_tree:
            return itsdict_tree[name]

        branch = self.imp(tree, name)
        itsdict_tree[name] = branch
        return branch

    def imp(self, tree, name):
        if not self._branch_exist(tree, name): return None

        branch = self._try_ctypes_or_array_of_ctypes(tree, name)
        if branch is not None: return branch

        branch = self._try_std_vector(tree, name)
        if branch is not None: return branch

        self._unknown_type_warning(tree, name)

        return None

    def _branch_exist(self, tree, name):
        leaves = tree.GetListOfLeaves()

        try:
            leafNames = [l.GetName() for l in leaves]
        except TypeError:
            logger = logging.getLogger(__name__)
            logger.warning(
                'cannot get leaf names of the tree: '
                '{!r}'.format(tree))
            if is_ROOT_null_pointer(leaves):
                logger.warning(
                    'tree.GetListOfLeaves() returns null pointer. '
                    'the tree might be a TChain with no files.')
            return False

        if name in leafNames:
            return True
        return False

    def _try_ctypes_or_array_of_ctypes(self, tree, name):
        itsArray, itsCountArray = branchAddressManager.getArrays(tree, name)
        if itsArray is None: return None
        branch = Branch(name, itsArray, itsCountArray)
        return branch

    def _try_std_vector(self, tree, name):
        itsVector = branchAddressManagerForVector.getVector(tree, name)
        return itsVector # this can be used as a branch

    def _unknown_type_warning(self, tree, name):
        leaf = tree.GetLeaf(name)
        typename = leaf.GetTypeName()
        logger = logging.getLogger(__name__)
        logger.warning('unknown leaf type : {}'.format(typename))

##__________________________________________________________________||
