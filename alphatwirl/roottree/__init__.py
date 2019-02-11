from .Events import Events
from .Branch import Branch

hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

if hasROOT:
    from .build import BuildEvents
    from .BEvents import BEvents
    from .BranchBuilder import BranchBuilder
    from .BranchAddressManager import BranchAddressManager
    from .BranchAddressManagerForVector import BranchAddressManagerForVector
    from .inspect import inspect_tree
    from .removed import EventBuilder
    from .removed import BEventBuilder
