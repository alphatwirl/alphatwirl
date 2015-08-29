# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
def returnTrue(x): return True

##__________________________________________________________________||
class Round(object):
    def __init__(self, width = 1, aBoundary = None, retvalue = 'lowedge', valid = returnTrue):

        supportedRetvalues = ('center', 'lowedge')
        if retvalue not in supportedRetvalues:
            raise ValueError("The retvalue '%s' is not supported! " % (retvalue, ) + "Supported values are '" + "', '".join(supportedRetvalues)  + "'")

        self.width = width
        self.halfWidth = self.width/2 if self.width % 2 == 0 else float(self.width)/2
        if aBoundary is None: aBoundary = self.halfWidth
        self.boundaries = [aBoundary - width, aBoundary, aBoundary + width]
        self.lowedge = (retvalue == 'lowedge')
        self.valid = valid

    def __call__(self, val):
        if not self.valid(val): return None
        self._updateBoundaries(val)
        bin = self.boundaries[0]
        for b in self.boundaries[1:]:
            if b <= val: bin = b
            else: break
        if not self.lowedge: bin += self.halfWidth
        return bin

    def _updateBoundaries(self, val):
        while val < self.boundaries[0]:
            self.boundaries.insert(0, self.boundaries[0] - self.width)

        while val > self.boundaries[-1]:
            self.boundaries.append(self.boundaries[-1] + self.width)

    def next(self, bin):
        self._updateBoundaries(bin)
        self._updateBoundaries(bin + self.width)
        nbin = self.boundaries[0]
        for b in self.boundaries[1:]:
            if b <= bin: nbin = b
            else: break
        ret = self.boundaries[self.boundaries.index(nbin) + 1]
        if not self.lowedge: ret += self.halfWidth
        return ret

##__________________________________________________________________||
