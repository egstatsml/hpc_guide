#!/usr/bin/env R

## A very simple script that will locally install many of the common
## packages used. If a package you use is not included, just add it
## to the list and run this script again


## ipak function: install and load multiple R packages.
## check to see if packages are installed. Install them if they are not, then load them into the R session.

ipak <- function(pkg){
    new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
    print(new.pkg)
    if (length(new.pkg))
        install.packages(new.pkg,
                         dependencies = TRUE,
                         repos= "https://cran.csiro.au/",
                         lib='~/R/library')
    #sapply(pkg, require, character.only = TRUE)
}

                                        # usage
packages <- c('tidyverse',
              'lme4',
              'randomForest',
              'Rcpp',
              'devtools',
              'lubridate',
              'readxl',
              'broom',
              'testthat',
              'stringr',
              'magrittr',
              'mlbench',
              'optparse',
              'gbm')
ipak(packages)
