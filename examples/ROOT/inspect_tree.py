#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@cern.ch>

##__________________________________________________________________||
import argparse
import ROOT

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('args', nargs=argparse.REMAINDER)
args = parser.parse_args()

inputPath = args.args[0]
treeName = 'tree'

##__________________________________________________________________||
def IsROOTNullPointer(tobject):
    try:
        tobject.GetName()
        return False
    except ReferenceError:
        return True

##__________________________________________________________________||
# https://root.cern.ch/root/html/Rtypes.h
# https://docs.python.org/2/library/array.html
typedic = dict(
    Double_t = 'd',
    Int_t = 'i',
    UInt_t = 'I',
    ULong64_t = 'L',
    )

##__________________________________________________________________||
inputFile = ROOT.TFile.Open(inputPath)
tree = inputFile.Get(treeName)

results = [ ]
results.append(('name', 'ROOTtype', 'arraytype', 'isarray', 'countname', 'countROOTtype', 'countarraytype', 'countmax'))

for leaf in tree.GetListOfLeaves():
    leafcount = leaf.GetLeafCount()
    isArray = not IsROOTNullPointer(leafcount)
    row = [ ]
    row.append(leaf.GetName())
    row.append(leaf.GetTypeName())
    row.append(typedic[leaf.GetTypeName()] if leaf.GetTypeName() in typedic else "unknown")
    row.append('yes ' if isArray else 'no')
    row.append(leafcount.GetName() if isArray else None)
    row.append(leafcount.GetTypeName() if isArray else None)
    row.append(typedic[leafcount.GetTypeName()] if isArray else None)
    row.append(leafcount.GetMaximum() if isArray else None)
    results.append(row)

transposed = [[r[i] for r in results] for i in range(len(results[0]))]
transposed = [[str(e) for e in r] for r in transposed]
columnWidths = [max([len(e) for e in r]) for r in transposed]
format = " {:>" + "s} {:>".join([str(e) for e in columnWidths]) + "s}"
for row in zip(*transposed):
    print format.format(*row)

##__________________________________________________________________||
