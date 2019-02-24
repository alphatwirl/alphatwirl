[![PyPI version](https://badge.fury.io/py/alphatwirl.svg)](https://badge.fury.io/py/alphatwirl) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.597010.svg)](https://doi.org/10.5281/zenodo.597010) [![Build Status](https://travis-ci.org/alphatwirl/alphatwirl.svg?branch=master)](https://travis-ci.org/alphatwirl/alphatwirl) [![codecov](https://codecov.io/gh/alphatwirl/alphatwirl/branch/master/graph/badge.svg)](https://codecov.io/gh/alphatwirl/alphatwirl)

<br />

<img src="https://raw.githubusercontent.com/alphatwirl/alphatwirl/v0.11.0/images/AlphaTwirl_logo_black.png" width="500">

---

A python library for summarizing event data into multivariate categorical data

### Description
_AlphaTwirl_ is a python library that summarizes event data into multivariate categorical data as data frames. Event data, input to AlphaTwirl, are data with one entry (or row) for one event: for example, data in [ROOT](https://root.cern.ch/) [TTrees](https://root.cern.ch/doc/master/classTTree.html) with one entry per collision event of an [LHC](https://home.cern/topics/large-hadron-collider) experiment at [CERN](http://home.cern/). Event data are often large&mdash;too large to be loaded in memory&mdash;because they have as many entries as events. Multivariate categorical data, the output of AlphaTwirl, have one row for one category. They are usually small&mdash;small enough to be loaded in memory&mdash;because they only have as many rows as categories. Users can, for example, import them as data frames into [R](https://www.r-project.org/) and [pandas](http://pandas.pydata.org/), which usually load all data in memory, and can perform categorical data analyses with a rich set of data operations available in R and pandas.

****

### Quick start

- Jupyter Notebook: [*Quick start of AlphaTwirl*](https://github.com/alphatwirl/notebook-tutorial-2019-02)<br />

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/alphatwirl/notebook-tutorial-2019-02/master?filepath=tutorial_01.ipynb)

****

### CHEP 2018

- Tai Sakuma, *"AlphaTwirl: a python library for summarizing event data into
  multi-dimensional categorical data"*, **CHEP 2018**, 9-13 July 2018
  Sofia, Bulgaria, ([indico](https://indico.cern.ch/event/587955/contributions/2937634/))

[<img src="https://raw.githubusercontent.com/alphatwirl/alphatwirl/v0.18.6/images/tai_20180709_CHEP2018_corrected_01_1900.png" width="200">](https://indico.cern.ch/event/587955/contributions/2937634/attachments/1680105/2731035/tai_20180709_CHEP2018_corrected_01.pdf)

****

### Features

#### Input format

- **Event data:** input data of alphatwirl are event data in general
    - Event data are any data with one entry (row) for one event.
    - Data in ROOT trees are typically event data
        -  e.g., one entry for one proton-proton collision event
    - Event data are often large because they have as many entries as
      events
        - e.g., they are often stored in many files in a server
          machine or a dedicated storage system
- [**ROOT trees:**](https://root.cern.ch/root/html/guides/users-guide/Trees.html) the main input format of alphatwirl
    - **Flat trees:** ROOT trees with only primitive
      types such as _int_ and _float_ and an array of those.
        - [Delphes trees](https://cp3.irmp.ucl.ac.be/projects/delphes/wiki/WorkBook/RootTreeDescription)
        - [Heppy trees](https://github.com/cbernet/heppy)
        - [CMS NanoAOD](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD)
    - With additional code to access each class, it is also possible to read
      trees with persistent objects
        - [CMS EDM formats](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCMSSWFramework)
- Users can write modules to support other formats

#### Output format

- **Multivariate categorical data**: output data of alphatwirl
  are multivariate categorical data
    - They are usually small because they only have as many entries as categories.
        - Often small enough to be stored as text files in a laptop computer.
- **Fixed width format**: text files with fixed width format have been
  primarily used as output format 
    - This format is convenient as long as the data size is small. You
      can browse it with a text editor. You can import it in
      [R](https://www.r-project.org/) and
      [pandas](http://pandas.pydata.org/) as a data frame.
    - An example output file looks like
  
```
process htbin njetbin minChi         n
    QCD   400       2      0  8.15e+05
    QCD   400       2   0.05  3.49e+05
    QCD   400       2    0.1  1.18e+05
    QCD   400       2   0.15  3.78e+04
                   ⋮
 TTJets  1200       6   1.45      0.00
 TTJets  1200       6    1.5      0.00
```

- There are plans to support [_feather_](https://github.com/wesm/feather).
- Users can write modules to support other formats


#### Split-apply-combine strategy

- The general idea of alphatwirl is to employ the [_split-apply-combine
  strategy_](https://www.jstatsoft.org/article/view/v040i01) on event data.
    -  _split_ event data into groups by categories, _apply_ a
       function to data in each group, and _combine_ the results as a
       **table** of multivariate categorical data.
    - Histograms can be created in this strategy&mdash;split data into
      bins, count the number of entries in each bin, and combine the
      results as a table.
    - Summarizing events in alphatwirl is generalization of creating
      histograms.
      
      
#### Keys and values

- **Keys:** categories are defined in terms of keys
- **Values:** values are summarized in each group defined by
  categories
- Keys and values are attributes of the event object, they are either
    - stored in the input file
    - or created by _scribllers_
    
#### Table configuration

- Tables can be configured by a list of python dictionaries.
    - The example code below configures five tables
       
```python
htbin = Binning(boundaries=(0, 200, 400, 800))
njetbin = Binning(boundaries=(1, 2, 3, 4, 5))
tblcfg = [
  dict(keyAttrNames=('mht40', ),
       binnings=(Round(10, 0), ),
       keyOutColumnNames=('mht', )),
  dict(keyAttrNames=('ht40', ‘mht40'),
       binnings=(htbin, Round(10, 0)),
       keyOutColumnNames=('ht', 'mht')),
  dict(keyAttrNames=('ht40', 'nJet40', ‘mht40'),
       binnings=(htbin, njetbin, Round(10, 0)),
       keyOutColumnNames=('ht', 'njet', 'mht')),
  dict(keyAttrNames=('ht40', ‘jet_pt'),
       binnings=(htbin, RoundLog(0.1, 100)),
       keyIndices=(None, 0),
       keyOutColumnNames=('ht', 'jet_pt')),
  dict(keyAttrNames=('ht40', ‘jet_pt'),
       binnings=(htbin, RoundLog(0.1, 100)),
       keyIndices=(None, ‘*'),
       keyOutColumnNames=('ht', 'jet_pt')),
]
```

- A more complex example

```python
dict(
    keyAttrNames=('ieta', 'iphi', 'depth', 'QIE10_index'),
    keyIndices=('(*)', '\\1', '\\1', '\\1'),
    binnings=(echo, echo, echo, echo),
    valAttrNames=('QIE10_energy', ),
    valIndices=('\\1', ),
    keyOutColumnNames=('ieta', 'iphi', 'depth', 'idxQIE10'),
    valOutColumnNames=('energy', ),
    summaryClass=alphatwirl.Summary.Sum
)
```

##### Indices

- Variables are scalar or arrays. Indices specify elements of an array
- Indices can be flexibly configured
    - a simple example:<br />
      `dict(keyAttrNames=('ht40', 'jet_pt'), keyIndices=(None, 0), ⋯ )`<br />
      `ht40` is scalar; the index is `None`. `jet_pt` is an array; `0`
      specifies the first element of `jet_pt`.
    - inclusive:<br />
     `dict(keyAttrNames=('ht40', 'jet_pt'), keyIndices=(None, '*'), ⋯ )`<br />
     `'*'` means all elements. all pairs of `ht40` and an element of
     `jet_pt`.
    - all combinations:<br />
      `dict(keyAttrNames=('jet_pt', 'muon_pt'), keyIndices=('*' '*'), ⋯ )`<br />
      all combinations of `jet_pt` and `muon_pt`
    - back reference:<br />
      `dict(keyAttrNames=('jet_pt', ‘jet_eta'), keyIndices = ('(*)', '\\1'), ⋯ )`<br />
      pairs of `jet_pt` and `jet_eta` with same index.
      The parenthesis in `'(*)'` indicates to remember the index.
      `'\\1'` refers the index in the first parenthesis.
    - a more complex example:<br />
       `dict(keyAttrNames=('jet_pt', 'jet_eta', 'muon_pt', 'muon_eta'), keyIndices=('(*)', '\\1', '(*)', '\\2'), ⋯ )`

##### Binnings

- Four binnigs classes are implemented
    - **Binning:** bin boundaries are manually specified by a user<br />
      `Binning(boundaries=(0, 200, 400, 800))`
    - **Round:** equal bin width<br />
      `Round(10, 0)`<br />
      `10` is the bin width and `0` is a boundary. The lower edge of a
      bin is included. The upper edge belongs to the next bin.
    - **RoundLog:** equal bin width in logarithm<br />
      `RoundLog(0.1, 100)`<br />
    - **Echo:** the value itself<br />
      `Echo(0.1, 100)`<br />
- Users can write own custom binning classes
    
##### Scribblers

- If variables necessary for table configuration or event selection are not in
  the input file, users can write _scribblers_ to create them on the fly
- The variables stored in the input files and the variables created by
  scribblers can be used as keys and values in the same way in the
  table configuration and event selection


#### Event selection

- Conditions of event selections can be specified by nested tuples and dictionaries.

```python
dict(All=(
  'ev : ev.ht[0] >= 400',
  'ev : ev.mht[0] >= 200',
  dict(Any=(
    'ev : ev.nJet[0] == 1',
    dict(All=(
      'ev : ev.nJet[0] >= 2',
      'ev : ev.minChi[0] >= 0.7’))
))))

```

- A nested combination of _all_ and _any_
    - **All:** all conditions need to be met
    - **Any:** at least one of the conditions needs to be met
- Users can write their own implementation of All and Any to add
  functionalities, for example, to count number of events that satisfy
  each condition

#### Dependency injection

- Classes in alphatwirl generally operate on abstract classes (in
  python, abstract classes don’t actually need to exist. duck typing
  is used instead).
- Particular implementations of most operations are determined at run
  time: input formats, output formats, a concurrency method, event
  selections, object selections, categorization, event summarizing
  methods, summary collecting methods, delivery methods, and even
  progress bars.
    - Furthermore, each particular implementation doesn’t generally
      depend on the framework either. In fact, the same event
      selection code can be used in Heppy.
- Particular implementations are specified by configuration.

#### Fast branch access by addresses

- Although using [PyROOT](https://root.cern.ch/pyroot), instead of
  accessing to branches by attributes of a tree object, alphatwirl
  uses `SetBranchAddress()`, which is much faster&mdash;can be more
  than ten times faster.

#### Multiprocessing

- [Multiprocessing](https://docs.python.org/3.6/library/multiprocessing.html)
  can be used to concurrently process events
- Progress bars grow in parallel on terminal screen to indicate the progress of each process.

```
  25.10% ::::::::::                               |      753 /     3000 |:  WJetsToLNu_HT1200to2500_madgraph 
  30.47% ::::::::::::                             |      914 /     3000 |:  WJetsToLNu_HT1200to2500_madgraph 
  29.30% :::::::::::                              |      879 /     3000 |:  WJetsToLNu_HT1200to2500_madgraph 
  85.40% ::::::::::::::::::::::::::::::::::       |      854 /     1000 |:  WJetsToLNu_HT1200to2500_madgraph 
  27.57% :::::::::::                              |      827 /     3000 |:  WJetsToLNu_HT2500toInf_madgraphM 
  25.47% ::::::::::                               |      764 /     3000 |:  WJetsToLNu_HT2500toInf_madgraphM 
  79.60% :::::::::::::::::::::::::::::::          |      796 /     1000 |:  WJetsToLNu_HT2500toInf_madgraphM 
  25.50% ::::::::::                               |      765 /     3000 |:  WJetsToLNu_HT2500toInf_madgraphM
```
  
#### Batch system

- Instead of multiprocessing, a batch system can be also used
- Currently, the interface to
  [HTCondor](https://research.cs.wisc.edu/htcondor/) is implemented.
- Users can write modules to use other batch system.
- While jobs are running in a batch system, the main process is
  running in the foreground, monitoring the progress of the jobs, and
  collecting the results as the jobs finish.
- Failed jobs are automatically resubmitted.
- Jobs can be split in terms of the number of input files and events.
    - one input file can be split into multiple jobs
    - one job can include multiple input files
