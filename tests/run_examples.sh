#!/bin/bash
# Tai Sakuma <sakuma@cern.ch>

##____________________________________________________________________________||
function echo_and_excecute {
    command=$1
    echo + $command >&2
    $command
    }

##____________________________________________________________________________||
heppydir=/Users/sakuma/work/cms/c150130_RA1_data/c150130_01_PHYS14/20150331_SingleMu

##____________________________________________________________________________||
thisdir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
alphatwirldir=$(dirname ${thisdir})
export PYTHONPATH=$alphatwirldir:$PYTHONPATH
scriptdir=${alphatwirldir}/examples/development

nevents=1000
processes=8

##____________________________________________________________________________||
# create a temporary directory (this command works on linux and osx)
# http://unix.stackexchange.com/questions/30091/fix-or-alternative-for-mktemp-in-os-x
outtopdir=`mktemp -d 2>/dev/null || mktemp -d -t 'tmp'`
echo "output directory: " $outtopdir

##____________________________________________________________________________||
scriptnums="030 040 050 060 070 080 090 100 110 120 130 140 150 160 170 180 190 200 210 220 230 240 250 260 270 280"

##____________________________________________________________________________||
for num in $scriptnums
do
    scriptname=print_${num}.py
    scriptpath=${scriptdir}/${scriptname}
    outdir=${outtopdir}/${num}
    echo_and_excecute "mkdir -p ${outdir}"
    echo_and_excecute "${scriptpath} -i ${heppydir} -n ${nevents} -o ${outdir}"
    exitcode=$?
    if (($exitcode > 0)); then
	exit $exitcode
    fi
done

##____________________________________________________________________________||
scriptnums="290"

##____________________________________________________________________________||
for num in $scriptnums
do
    scriptname=print_${num}.py
    scriptpath=${scriptdir}/${scriptname}

    outdir=${outtopdir}/${num}_sp
    echo_and_excecute "mkdir -p ${outdir}"
    echo_and_excecute "${scriptpath} -i ${heppydir} -n ${nevents} -o ${outdir}"
    exitcode=$?
    if (($exitcode > 0)); then
	exit $exitcode
    fi

    outdir=${outtopdir}/${num}_mp
    echo_and_excecute "mkdir -p ${outdir}"
    echo_and_excecute "${scriptpath} -i ${heppydir} -n ${nevents} -o ${outdir} -p ${processes} --force"
    exitcode=$?
    if (($exitcode > 0)); then
	exit $exitcode
    fi
done

##____________________________________________________________________________||
