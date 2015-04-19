
#### A simple example of analysis with data frame

This directory contains a set of files that demonstrate a simple example of analysis with data frame. It contains four data frames each in a text file and two scripts. The two scripts do the same thing. One script is written in R and the other in Python.


#### How to check out and run the scripts

This section describes how to check out and run the scripts. The software requirement to run the scripts are written below in this page.

Check out the branch `v0.2.x` of this repo:

    git clone --branch v0.2.x git@github.com:CMSRA1/AlphaTwirl.git

Move to this directory, the directory in which this `README.md` file is:

    cd AlphaTwirl/examples/dataframe/

Run the R script

    ./yield.R

It will create the output file `tbl_out_R.txt`.

Run the Python script

    ./yield.py

It will create the output file `tbl_out_python.txt`.

The contents of the two output files are the same but in slightly different formats.


#### Requirement to run the R script

It requires [R](http://www.r-project.org/) to run.

 - R 3.1 (or 3.2)

It requires two R packages.

 - dplyr
 - gdata

##### How to install R and the R packages

###### Install R

Go to one of the [CRAN mirror sites](http://cran.r-project.org/mirrors.html), for example,

 - http://www.stats.bris.ac.uk/R/

Choose your OS and donwload R 3.1.3.

The script in this directory has been tested with R 3.1.3. However, it probably works as well in R 3.2.0 (which was released only a few days ago and has not been propagated to all mirror sites).

Follow the instruction and install R.

The installation is generally simple. For example, in case of OS X Mavericks, it is as simple as to double click R-3.1.3-mavericks.pkg and follow the instruction on the screen.

###### Install the R packages

We will install two R packages: dplyr and gdata. Start R. You can start R by typing "R" in the terminal.

    R

Set a [CRAN mirror site](http://cran.r-project.org/mirrors.html).

    r = getOption("repos")
    r["CRAN"] = "http://www.stats.bris.ac.uk/R/"
    options(repos = r)

Then, install the packages with the following commands.

    install.packages("dplyr")
    install.packages("gdata")


Then, quit R

    q()


#### Requirement to run the python script

It runs with Python 2.7.

 - Python 2.7

(It might run with Python 3 but has not been tested.)


It requires a package.

 - [pandas](http://pandas.pydata.org/)


##### How to install pandas

The installation of pandas could be easy but could be also difficult. It varies with your Python environment. For example, if the [PyPI](https://pypi.python.org) environment of the Python package management is set up, you can install pandas with one line of command.

    pip install pandas Otherwise,

It could be as easy with other package management systems. The installation is detailed here:

 - http://pandas.pydata.org/pandas-docs/stable/install.html

In addition to how to install pandas, this website explains how to try using pandas without the installation at an online web service.
