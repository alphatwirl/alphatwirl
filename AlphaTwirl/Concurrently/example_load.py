#!/usr/bin/env python
# Tai Sakuma <sakuma@fnal.gov>
import os, sys
import argparse
import pickle

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('pickle', help = 'path to a pickle file')
args = parser.parse_args()


##__________________________________________________________________||
sys.path.insert(1, './bdphi-scripts')
sys.path.insert(1, './bdphi-scripts/bdphiROC')

##__________________________________________________________________||
f = open(args.pickle, 'rb')
package = pickle.load(f)

print package

##__________________________________________________________________||
