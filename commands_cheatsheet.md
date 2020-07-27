# QUT HPC Command Cheatsheet 

## Login, logout

- `ssh <username>@lyra.qut.edu.au`

- `exit`

## Submit jobs

- `qsub <jobscript>.sh`

- `qsub -I -S /bin/bash`
  - 1 hour interactive job.

## Check jobs

- `qstat -u $USER`
  - List all your jobs I.

- `qjobs -u $USER -r`
  - List all your jobs II. 

- `qpeek <jobnumber>.pbs`
  - Peek at output from one job.

## Module

- `module load <modulename>`

- `module avail <modulename>`
  - Search for available modules (e.g. a particular R version)




