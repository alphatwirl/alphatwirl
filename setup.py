from setuptools import setup, find_packages
import os
import versioneer

long_description = """
*AlphaTwirl* is a python library that loops over event data and
summarizes them into multi-dimensional categorical data as data
frames. Event data, input to AlphaTwirl, are data with one entry (or
row) for one event: for example, data in `ROOT
<https://root.cern.ch/>`__ `TTrees
<https://root.cern.ch/doc/master/classTTree.html>`__ with one entry
per collision event of an `LHC
<https://home.cern/topics/large-hadron-collider>`__ experiment at
`CERN <http://home.cern/>`__. Event data are often large---too large
to be loaded in memory---because they have as many entries as events.
Multi-dimensional categorical data, the output of AlphaTwirl, have one
row for one category. They are usually small---small enough to be
loaded in memory---because they only have as many rows as categories.
Users can, for example, import them as data frames into `R
<https://www.r-project.org/>`__ and `pandas
<http://pandas.pydata.org/>`__, which usually load all data in memory,
and can perform categorical data analyses with a rich set of data
operations available in R and pandas.
"""

setup(
    name='alphatwirl',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='A Python library for summarizing event data',
    long_description=long_description,
    author='Tai Sakuma',
    author_email='tai.sakuma@gmail.com',
    url='https://github.com/alphatwirl/alphatwirl',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['docs', 'images', 'tests']),
)
