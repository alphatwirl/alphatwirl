# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class EventSelectionAll(object):
    """select events that meet all conditions

    """

    def __init__(self):
        self.selections = [ ]

    def add(self, selection):
        self.selections.append(selection)

    def __call__(self, event):
        for s in self.selections:
            if not s(event): return False
        return True

##__________________________________________________________________||
