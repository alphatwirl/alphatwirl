
#### A simple example of analysis with data frame

This directory contains a set of files that demonstrate a simple example of analysis with data frame. It contains four data frames each in a text file and two scripts. The two scripts do the same thing. One script is written in R and the other in Python.


#### How to check out and run the scripts

This section describes how to check out and run the scripts. The software requirement to run the scripts are written below in this page.

Check out the branch `v0.9.x` of this repo:

```bash
git clone --branch v0.9.x git@github.com:CMSRA1/AlphaTwirl.git
```

Move to this directory, the directory in which this `README.md` file is:

```bash
cd AlphaTwirl/examples/dataframe/
```

Run the R script

```bash
./yield.R
```

It will create the output file `tbl_out_R.txt`.

Run the Python script

```bash
./yield.py
```

It will create the output file `tbl_out_python.txt`.

The contents of the two output files are the same but in slightly different formats.

#### Requirement to run the R script

It requires [R](http://www.r-project.org/) to run.

 - R 3.1 or later

It requires two R packages.

 - dplyr
 - gdata

#### Requirement to run the python script

It runs with Python 2.7.

 - Python 2.7

(It might run with Python 3 but has not been tested.)

It requires a package.

 - [pandas](http://pandas.pydata.org/)
