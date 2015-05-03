# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class Events(object):
    """An iterative object for events.


    Examples
    --------

    inputFile = ROOT.TFile.Open(inputPath)
    tree = inputFile.Get(treeName)
    events = Events(tree)
    for event in events:
        event.jet_pt # a branch can be accessed as an attribute

    """

    def __init__(self, tree, maxEvents = -1):
        self.file = tree.GetDirectory() # so a file won't close
        self.tree = tree
        self.nEvents = min(self.tree.GetEntries(), maxEvents) if (maxEvents > -1) else self.tree.GetEntries()
        self.iEvent = -1

    def __iter__(self):
        for self.iEvent in xrange(self.nEvents):
            self.tree.GetEntry(self.iEvent)
            yield self
        self.iEvent = -1

    def __getattr__(self, name):
        return getattr(self.tree, name)

##____________________________________________________________________________||
