# A BRAG Guide To HPC

This repo provides a quick reference guide on how to access and use the HPC facilities at QUT. Example scripts are supplied to install relevent packages, and demonstrate how to submit jobs to HPC.

The complegte guide can be found in the PDF file listed above, and the associated TeX files in the [./tex](https://github.com/ethangoan/hpc_guide/tree/master/tex) directory. They are there if you want to add your own notes or edit anything. If you want to have access to this repo to make changes or add some examples, please let me know. This will be a living document that I will update periodically as I am always finding out new tips and tricks.

## Installing R Packages

The [install_packages_batch.sh](./install_r_packages/install_packages_batch.sh) script will submit a job to call the  [install_r_packages.R](./install_r_packages/install_r_packages.R) script, which will install the following packages:
```
              'tidyverse',
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
              'gbm'

```

If you want to install more packages, simply add the name of the package to the vector of package names in this install script, and submit the batch script  [install_packages_batch.sh](./install_r_packages/install_packages_batch.sh) again.


## Examples

Some example jobs are listed in the [./bt_examples](https://github.com/ethangoan/hpc_guide/tree/master/bt_examples) for a boosted regression tree problem to predict the presence of breast cancer based in biopsy measurements. Data is from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Original)). In there are 10 seperate batch scripts for submitting jobs to the PBS queue. Each of these jobs will load in the required modules needed, and call the [breast_cancer_bt.R](./bt_examples/breast_cancer_bt.R) script with a different command line argument, indicating how many trees to use for each model. Please refer to the PDF guide for more info.


Any questions, queries, suggestions, or if you me want to add to this guide, please just let me know.

Ethan
ej.goan@qut.edu.au