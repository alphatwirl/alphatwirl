from Events import Events
from BranchAddressManager import BranchAddressManager
from Branch import Branch

hasROOT = False
try:
    import ROOT
    hasROOT = True
except ImportError:
    pass

if hasROOT:
    from BEvents import BEvents
    from BranchBuilder import BranchBuilder
    from BranchAddressManagerForVector import BranchAddressManagerForVector
