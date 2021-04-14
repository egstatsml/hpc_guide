## A very simple script that will locally install many of the common
## packages used. If a package you use is not included, just add it
## to the list and run this script again


## ipak function: install and load multiple R packages.
## check to see if packages are installed. Install them if they are not, then load them into the R session.

exit <- function() { invokeRestart("abort") } 

ipak <- function(pkg, lib_dir){
    new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
    print(new.pkg)
    if (length(new.pkg))
        install.packages(new.pkg,
                         dependencies=TRUE,
                         repos="https://cran.csiro.au/",
                         lib=lib_dir)
}


install_packages <- function(lib_dir){
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
                'gbm',
                'XML',
                'RCurl',
                'rlist',
                'ggplot2',
                'brms',
                'rstan')
  ipak(packages, lib_dir)
  
  #install packages with devtools from Github
  devtools::install_github("rstudio/reticulate")
  devtools::install_github("rstudio/tensorflow")
  devtools::install_github("rstudio/keras")
}


main <- function(){
  args <- commandArgs()
  # check command line arg for library directory was supplied
  if length(args) < 6{
    print("Command line arg for path of user libraries needs to be supplied")
    exit()
  }
  else if ~(dir.exists(args[6])){
    print("path for install location for R libraries does not exist")
    print("please make the directory first with: mkdir <library_path>")
    print(args[6])
    exit()
  }
  # if have made it here, run install function
  install_packages(args[6])
}

main()
