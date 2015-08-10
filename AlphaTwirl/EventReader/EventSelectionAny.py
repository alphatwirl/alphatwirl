# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
class EventSelectionAny(object):
    """select events that meet any of the conditions

    """

    def __init__(self):
        self.selections = [ ]

    def add(self, selection):
        self.selections.append(selection)

    def __call__(self, event):
        for s in self.selections:
            if s(event): return True
        return False

##__________________________________________________________________||
