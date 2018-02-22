# Tai Sakuma <tai.sakuma@gmail.com>

##__________________________________________________________________||
class Events(object):
    """An iterative object for events.

    You can use this class to iterate over entries in a ROOT TTree.

    You can instantiate this class with a TTree object and an
    optionally a maximum number of entries to loop over::

        inputFile = ROOT.TFile.Open(inputPath)
        tree = inputFile.Get(treeName)
        events = Events(tree)

    Then, the "for" loop for the tree entries can be::

        for event in events:

    Note: "event" and "events" are the same object. In each iteration,
    "event" (and "events") is loaded with the next entry in the tree.

    A content of the tree, e.g., a branch, can be accessed as an
    attribute of "event"::

          event.jet_pt

    In order to access to a particular entry, you can use an index.
    For example, to get 11th entry (the index for the first entry is
    0)::

        event = events[10]

    Note: Again "event" and "events" are the same object.

    """

    def __init__(self, tree, maxEvents=-1, start=0):

        if start < 0:
            raise ValueError("start must be greater than or equal to zero: {} is given".format(start))

        self.tree = tree
        nEventsInTree = self.tree.GetEntries()
        start = min(nEventsInTree, start)
        if maxEvents > -1:
            self.nEvents = min(nEventsInTree - start, maxEvents)
        else:
            self.nEvents = nEventsInTree - start
        self.maxEvents = maxEvents
        self.start = start
        self.iEvent = -1

    def __len__(self):
        return self.nEvents

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self._repr_contents()
        )

    def _repr_contents(self):
        return 'tree = {!r}, maxEvents={!r}, start={!r}, nEvents={!r}, iEvent={!r}'.format(
            self.tree,
            self.maxEvents,
            self.start,
            self.nEvents,
            self.iEvent
        )

    def __getitem__(self, i):
        if i >= self.nEvents:
            self.iEvent = -1
            raise IndexError("the index is out of range: " + str(i))
        self.iEvent = i
        self.tree.GetEntry(self.start + self.iEvent)
        return self

    def __iter__(self):
        for self.iEvent in range(self.nEvents):
            self.tree.GetEntry(self.start + self.iEvent)
            yield self
        self.iEvent = -1

    def __getattr__(self, name):
        return getattr(self.tree, name)

##__________________________________________________________________||
