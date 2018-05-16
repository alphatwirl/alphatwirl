from .Events import Events
from .Branch import Branch
from .EventBuilderConfig import EventBuilderConfig

hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

if hasROOT:
    from .build import BuildEvents
    from .BEvents import BEvents
    from .BEventBuilder import BEventBuilder
    from .BranchBuilder import BranchBuilder
    from .EventBuilder import EventBuilder
    from .BranchAddressManager import BranchAddressManager
    from .BranchAddressManagerForVector import BranchAddressManagerForVector
    from .inspect import inspect_tree
