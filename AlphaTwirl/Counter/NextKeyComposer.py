# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class NextKeyComposer(object):
    def __init__(self, binnings):
        self._binnings = binnings

    def __call__(self, key):
        """returns a list of the next keys

        e.g.,
        If key = (11, 8, 20)
        it returns ((12, 8, 20), (11, 9, 20), (11, 8, 21))

        When the next bin is None, it won't be included.

        When the next bin is the same, it won't be included.

        """
        ret = [ ]
        for i in range(len(self._binnings)):
            keyc = list(key)
            thisbin = keyc[i]
            nextbin = self._binnings[i].next(thisbin)
            if nextbin is None: continue
            if nextbin == thisbin: continue
            keyc[i] = nextbin
            ret.append(tuple(keyc))
        return tuple(ret)

##____________________________________________________________________________||
class NextKeyComposerBuilder(object):
    def __init__(self, binnings):
        self.binnings = binnings

    def __call__(self):
        return NextKeyComposer(binnings = self.binnings)

##____________________________________________________________________________||
