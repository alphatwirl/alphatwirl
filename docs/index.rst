.. AlphaTwirl documentation master file, created by
   sphinx-quickstart on Sat May 23 14:38:44 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

|
|

.. image:: ../images/AlphaTwirl.png
    :width: 300px
    :alt: alphatwirl

|

The library contains a set of Python classes which can be used to loop over
event data, summarize them, and store the results for further analysis or
visualization. Event data here are defined as any data with one row (or entry)
for one event; for example, data in `ROOT <https://root.cern.ch/>`_
`TTrees <https://root.cern.ch/doc/master/classTTree.html>`_ are event data when
they have one entry for one proton-proton collision event. Outputs of this
library are typically not event data but multi-dimensional categorical data,
which have one row for one category. Therefore, the outputs can be imported into
`R <https://www.r-project.org/>`_ or `pandas <http://pandas.pydata.org/>`_ as
data frames. Then, users can continue a multi-dimensional categorical analysis
with R, pandas, and other modern data analysis tools.


Contents:

.. toctree::
   :maxdepth: 4

   alphatwirl


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

