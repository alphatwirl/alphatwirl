#!/usr/bin/env python
# Tai Sakuma <sakuma@cern.ch>
from __future__ import print_function
import os
import argparse

from HTCondorJobSubmitter import HTCondorJobSubmitter

##__________________________________________________________________||
import logging
logging.basicConfig(level = logging.DEBUG)

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('paths', nargs = argparse.REMAINDER, help = 'paths to task packages')
args = parser.parse_args()

##__________________________________________________________________||
def main():

    jobrunner = HTCondorJobSubmitter()

    for package_path_org in args.paths:
        package_path_abs = os.path.abspath(package_path_org)
        taskdir = os.path.dirname(package_path_abs)
        package_path_rel = os.path.basename(package_path_abs)

        jobrunner.run(taskdir, package_path_rel)

    try:
        jobrunner.wait()
    except KeyboardInterrupt:
        print('received KeyboardInterrupt')
        jobrunner.terminate()

##__________________________________________________________________||
if __name__ == '__main__':
    main()
