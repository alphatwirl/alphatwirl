
#### Files in this directory

This directory contains a series of python scripts. Starting from print_010.py, the script progressively changes as the number in the file name incremented. The first three scripts, print_010.py, print_020.py, print_030.py, don't use AlphaTwirl. The fourth script, print_040.py, imports one class from AlphaTwirl. The next script, print_050.py, imports two classes from AlphaTwirl. The following scripts use more and more AlphaTwirl classes. The actual development of AlphaTwirl took a similar path. These example scripts illustrate how the library AlphaTwirl can be used.


#### Requirement to run the scripts

##### Software

Running these script requires the following software.

 - Python 2.7
 - ROOT 5 or 6

You should be able to run the scripts on nearly any computer with the software.

You can run on your local desktop or laptop computer if the software is installed.

How to run on [lxplus](http://information-technology.web.cern.ch/services/lxplus-service) is explained below on this page.


##### Input files

The scripts access to files stored in the AFS locker:


  - /afs/cern.ch/work/a/aelwood/public/alphaT/cmgtools/PHYS14/20150331_SingleMu/


If you have an AFS accees to these files, the scripts can directly read these files.

The total size of the input files is about 1.5G. If you copy them to where you have an accees, you can run without the AFS access. It is often convenient to have data locally when it is possible.

#### How to check out and run the scripts

Check out the branch `v0.2.x` of this repo:

    git clone --branch v0.2.x git@github.com:CMSRA1/AlphaTwirl.git

Set an environmental variable:

    export PYTHONPATH=$PWD/AlphaTwirl:$PYTHONPATH

The above `export` command is for bash user. tcsh users need to use `setenv` as usual.


Move to this directory, the directory in which this `README.md` file is:

    cd AlphaTwirl/examples/development/


The scripts write thier output files in the directory `tmp`. Please create it.


    mkdir -p tmp

You can run the first script.

    ./print_010.py

It creates the output file `tmp/tbl_met.txt`.

Run the second script.

    ./print_020.py

This takes longer because it loops over all events in all components.

The third script and after have an option to specify the maximum number of events to process.

    ./print_030.py -n 1000

You can speficy the input directory by the `-i` option. Also you can change the output directory with the `-o` option.

You can continue with the same options up to the second last script.

    ./print_280.py -n 1000


The last script has defferent options and different default values.

    ./print_290.py -p 8 -n 1000 -o tmp -i /afs/cern.ch/work/a/aelwood/public/alphaT/cmgtools/PHYS14/20150331_SingleMu

The default input and output directories for the last script are different. You might need to specify them with `-i` and `-o` options. By default, the last script runs as a single process. You can run with multiple processes with `-p` option. The number after `-p` specifies the maximum number of the processes to run in parallel.



#### Running on lxplus

You can run these scripts on [lxplus](http://information-technology.web.cern.ch/services/lxplus-service). Using AlphaTwirl doesn't require the CMS environment. But, it is possible to use in the CMS environment as well.


##### How to set up Python and ROOT environment without the CMS environment

The default versions or Python and ROOT on lxplus are somewhat outdated. You can use more recent versions if you set up environment variables, for example, as follows.

For bash users:


    export PATH=/opt/rh/python27/root/usr/bin:$PATH
    export LD_LIBRARY_PATH=/opt/rh/python27/root/usr/lib64:$LD_LIBRARY_PATH
    source /afs/cern.ch/sw/lcg/external/gcc/4.9.2/x86_64-slc6/setup.sh
    cd /afs/cern.ch/sw/lcg/app/releases/ROOT/6.02.08/x86_64-slc6-gcc49-opt/root/
    source bin/thisroot.sh
    cd -


For tcsh users:

    setenv PATH /opt/rh/python27/root/usr/bin:$PATH
    setenv LD_LIBRARY_PATH /opt/rh/python27/root/usr/lib64:$LD_LIBRARY_PATH
    source /afs/cern.ch/sw/lcg/external/gcc/4.9.2/x86_64-slc6/setup.csh
    cd /afs/cern.ch/sw/lcg/app/releases/ROOT/6.02.08/x86_64-slc6-gcc49-opt/root/
    source bin/thisroot.csh
    cd -

If the 2nd command in the above causes the following message:

    LD_LIBRARY_PATH: Undefined variable.

you need to repace the 2nd command with

    setenv LD_LIBRARY_PATH /opt/rh/python27/root/usr/lib64

After the environment variables are set, you can continue with `git clone ...` command above.

##### How to set up the CMS environment


The CMS environment includes recent versions of ROOT and Python. You can use those versions to use AlphaTwirl as well.

For example, you can create and enter the CMS environment as follows.

    cmsrel CMSSW_7_4_0_patch1
    cd CMSSW_7_4_0_patch1/src/
    cmsenv

After you enter the CMS environment, you can continue with `git clone ...` command above.

