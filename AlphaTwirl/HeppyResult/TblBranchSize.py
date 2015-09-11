# Tai Sakuma <tai.sakuma@cern.ch>
from ..mkdir_p import mkdir_p
from ..listToAlignedText import listToAlignedText
import os
import ROOT

##__________________________________________________________________||
def IsROOTNullPointer(tobject):
    try:
        tobject.GetName()
        return False
    except ReferenceError:
        return True

##__________________________________________________________________||
class TblBranchSize(object):
    def __init__(self, analyzerName, fileName, treeName, outPath):
        self.analyzerName = analyzerName
        self.fileName = fileName
        self.treeName = treeName
        self.outPath = outPath

        self.branchOrder = [ ]
        self.branchDict = { }

    def begin(self): pass

    def read(self, component):

        inputPath = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
        file = ROOT.TFile.Open(inputPath)
        tree = file.Get(self.treeName)

        for leaf in tree.GetListOfLeaves():
            leafcount = leaf.GetLeafCount()
            isArray = not IsROOTNullPointer(leafcount)
            branchName = leaf.GetName()
            if not branchName in self.branchDict:
                self.branchOrder.append(branchName)
                branch_entry = { }
                branch_entry['name'] = branchName
                branch_entry['type'] = leaf.GetTypeName()
                branch_entry['isarray'] = '1' if isArray else '0'
                branch_entry['countname'] = leafcount.GetName() if isArray else None
                branch_entry['components'] = [ ]
                self.branchDict[branchName] = branch_entry
            component_entry = { }
            zipbytes = leaf.GetBranch().GetZipBytes()/1024.0/1024.0 # MB
            totalsize = leaf.GetBranch().GetTotalSize()/1024.0/1024.0 # MB
            component_entry['name'] = component.name
            component_entry['size'] = zipbytes
            component_entry['uncompressed_size'] = totalsize
            component_entry['compression_factor'] = totalsize/zipbytes if zipbytes > 0 else 0
            self.branchDict[branchName]['components'].append(component_entry)

    def end(self):

        results = [ ]
        results.append(['name', 'type', 'isarray', 'countname', 'size', 'uncompressed_size', 'compression_factor'])

        for n in self.branchOrder:
            bentry = self.branchDict[n]
            centry = bentry['components']
            size = sum([e['size'] for e in centry])
            usize = sum([e['uncompressed_size'] for e in centry])
            cf = usize/size if size > 0 else 0
            row = [ ]
            row.append(bentry['name'])
            row.append(bentry['type'])
            row.append(bentry['isarray'])
            row.append(bentry['countname'])
            row.append('{:10.6f}'.format(size))
            row.append('{:10.6f}'.format(usize))
            row.append('{:10.2f}'.format(cf))
            results.append(row)

        f = self._open(self.outPath)
        f.write(listToAlignedText(results))
        self._close(f)

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
