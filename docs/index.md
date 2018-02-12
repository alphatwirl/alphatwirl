
# Home

```eval_rst
.. image:: ../images/AlphaTwirl_logo_black.png
    :width: 300px
    :alt: alphatwirl
```

_AlphaTwirl_ is a python library that loops over event data and summarizes them
into multi-dimensional categorical data as data frames. Event data, input to
AlphaTwirl, are data with one entry (or row) for one event: for example, data in
[ROOT](https://root.cern.ch/)
[TTrees](https://root.cern.ch/doc/master/classTTree.html) with one entry per
collision event of an [LHC](https://home.cern/topics/large-hadron-collider)
experiment at [CERN](http://home.cern/). Event data are often large---too large
to be loaded in memory---because they have as many entries as events.
Multi-dimensional categorical data, the output of AlphaTwirl, have one row for
one category. They are usually small---small enough to be loaded in
memory---because they only have as many rows as categories. Users can, for
example, import them as data frames into [R](https://www.r-project.org/) and
[pandas](http://pandas.pydata.org/), which usually load all data in memory, and
can perform categorical data analyses with a rich set of data operations
available in R and pandas.

