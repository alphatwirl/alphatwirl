
#### A simple example of analysis with data frame

This directory contains a set of files that demonstrate a simple example of analysis with data frame. It contains four data frames each in a text file and one R script.


#### Requirement to run the script

The script is written in [R](http://www.r-project.org/). It requires R to run.

 - R 3.1 (or 3.2)

It requires two R packages.

 - dplyr
 - gdata

##### How to install R and the R packages

###### Install R

Go to one of the [CRAN mirror sites](http://cran.r-project.org/mirrors.html), for example,

 - http://www.stats.bris.ac.uk/R/
 - http://cran.ma.imperial.ac.uk/

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

#### How to check out and run the script

Check out the branch `v0.2.x` of this repo:

    git clone --branch v0.2.x git@github.com:CMSRA1/AlphaTwirl.git

Move to this directory, the directory in which this `README.md` file is:

    cd AlphaTwirl/examples/dataframe/

Run the script

    ./yield.R

It will create the output file `tbl_out.txt`.
