# Tai Sakuma <tai.sakuma@cern.ch>
from ..misc import mkdir_p
from ..misc import list_to_aligned_text
import os
from operator import itemgetter
import ROOT

##__________________________________________________________________||
def IsROOTNullPointer(tobject):
    try:
        tobject.GetName()
        return False
    except ReferenceError:
        return True

##__________________________________________________________________||
class TblBranch(object):
    def __init__(self, analyzerName, fileName, treeName, outPath,
                 addType = True, addSize = False, addTitle = False, sortBySize = False
    ):
        self.analyzerName = analyzerName
        self.fileName = fileName
        self.treeName = treeName
        self.outPath = outPath

        self.addType = addType
        self.addSize = addSize
        self.addTitle = addTitle

        self.sortBySize = sortBySize

        self.branchOrder = [ ]
        self.branchDict = { }

    def begin(self): pass

    def read(self, component):

        inputPath = os.path.join(getattr(component, self.analyzerName).path, self.fileName)
        file = ROOT.TFile.Open(inputPath)
        tree = file.Get(self.treeName)

        for leaf in tree.GetListOfLeaves():
            leaf_info = self._inspect_leaf(leaf)
            leaf_def = {k:leaf_info[k] for k in ('name', 'type', 'isarray', 'countname', 'title')}
            branchName = leaf_def['name']
            if not branchName in self.branchDict:
                self.branchOrder.append(branchName)
                leaf_def['components'] = [ ]
                self.branchDict[branchName] = leaf_def
            leaf_size = {k:leaf_info[k] for k in ('size', 'uncompressed_size', 'compression_factor')}
            leaf_size['name'] = component.name
            self.branchDict[branchName]['components'].append(leaf_size)

    def _inspect_leaf(self, leaf):
        ret = { }
        ret.update(self._inspect_leaf_definition(leaf))
        ret.update(self._inspect_leaf_size(leaf))
        return ret

    def _inspect_leaf_definition(self, leaf):
        leafcount = leaf.GetLeafCount()
        isArray = not IsROOTNullPointer(leafcount)
        ret = { }
        ret['name'] = leaf.GetName()
        ret['type'] = leaf.GetTypeName()
        ret['isarray'] = '1' if isArray else '0'
        ret['countname'] = leafcount.GetName() if isArray else None
        ret['title'] = leaf.GetBranch().GetTitle()
        return ret

    def _inspect_leaf_size(self, leaf):
        ret = { }
        zipbytes = leaf.GetBranch().GetZipBytes()/1024.0/1024.0 # MB
        totalsize = leaf.GetBranch().GetTotalSize()/1024.0/1024.0 # MB
        ret['size'] = zipbytes
        ret['uncompressed_size'] = totalsize
        ret['compression_factor'] = totalsize/zipbytes if zipbytes > 0 else 0
        return ret

    def end(self):

        results = [ ]

        for n in self.branchOrder:
            bentry = self.branchDict[n]
            centry = bentry['components']
            size = sum([e['size'] for e in centry])
            usize = sum([e['uncompressed_size'] for e in centry])
            cf = usize/size if size > 0 else 0
            row = [ ]
            row.append(bentry['name'])
            if self.addType:
                row.append(bentry['type'])
                row.append(bentry['isarray'])
                row.append(bentry['countname'])
            if self.addSize:
                row.append(size)
                row.append(usize)
                row.append(cf)
            if self.addTitle:
                row.append(bentry['title'])
            results.append(row)

        columns = ['name']
        if self.addType: columns.extend(['type', 'isarray', 'countname'])
        if self.addSize: columns.extend(['size', 'uncompressed_size', 'compression_factor'])
        if self.addTitle: columns.extend(['title'])

        if self.addSize and self.sortBySize:
            results = sorted(results, key = lambda x: float(itemgetter(columns.index('size'))(x)), reverse = True)

        results.insert(0, columns)

        format_dict = { }
        if self.addSize:
            format_dict.update({
                'size':'{:.6f}',
                'uncompressed_size':'{:.6f}',
                'compression_factor':'{:.2f}'
            })

        left_align_last_column = False
        if self.addTitle:
            left_align_last_column = True

        f = self._open(self.outPath)
        f.write(list_to_aligned_text(results, format_dict, left_align_last_column))
        self._close(f)

    def _open(self, path):
        mkdir_p(os.path.dirname(path))
        return open(path, 'w')

    def _close(self, file): file.close()

##__________________________________________________________________||
