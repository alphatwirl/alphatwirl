#!/usr/bin/env python
# Tai Sakuma <tai.sakuma@gmail.com>
from __future__ import print_function
import os, sys
import argparse
import gzip

try:
   import cPickle as pickle
except:
   import pickle

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('pickle', help = 'path to a pickle file')
args = parser.parse_args()


##__________________________________________________________________||
pickle_path = os.path.abspath(args.pickle)

##__________________________________________________________________||
os.chdir(os.path.dirname(pickle_path))

##__________________________________________________________________||
dirname = 'python_modules'
tarname = dirname + '.tar.gz'
if os.path.exists(tarname) and not os.path.exists(dirname):
    tar = tarfile.open(tarname)
    tar.extractall()
    tar.close()
sys.path.insert(0, dirname)

##__________________________________________________________________||
f = gzip.open(os.path.basename(pickle_path), 'rb')
package = pickle.load(f)

print(package)

##__________________________________________________________________||
