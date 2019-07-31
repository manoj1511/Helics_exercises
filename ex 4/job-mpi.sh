#!/bin/bash
#PBS -N test_run           
#PBS -l select=1:ncpus=6:mem=10gb:mpiprocs=5
#PBS -l place=excl
#PBS -l walltime=00:05:00
#PBS -j oe
#PBS -P eest

cd $PBS_O_WORKDIR
module load OpenMPI
module load python/3.7-anaconda
python init-mpi.py
