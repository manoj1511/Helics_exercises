#!/bin/bash
#PBS -N test_run           
#PBS -l select=1:mem=1gb
#PBS -l place=excl
#PBS -l walltime=00:05:00
#PBS -j oe
#PBS -P eest

cd $PBS_O_WORKDIR
module load python/3.7-anaconda
source activate manoj
python init.py

