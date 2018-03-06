# Tai Sakuma <tai.sakuma@gmail.com>
from .Events import Events
from .BranchBuilder import BranchBuilder

##__________________________________________________________________||
class BEvents(Events):
    def __init__(self, tree, maxEvents=-1, start=0):
        super(BEvents, self).__init__(tree, maxEvents, start)
        self.branches = { }
        self.buildBranch = BranchBuilder()
        self.buildBranch.register_tree(tree)

    def __repr__(self):
        return '{}({}, branches={!r})'.format(
            self.__class__.__name__,
            super(BEvents, self)._repr_contents(),
            self.branches
        )

    def __getattr__(self, name):

        if name in self.branches:
            return self.branches[name]

        branch = self.buildBranch(self.tree, name)

        if branch is None:
            raise AttributeError('{!r} has no attribute "{}"'.format(self, name))

        self.branches[name] = branch

        if self.iEvent >= 0:
            self.tree.GetEntry(self.start + self.iEvent)

        return self.branches[name]

##__________________________________________________________________||
