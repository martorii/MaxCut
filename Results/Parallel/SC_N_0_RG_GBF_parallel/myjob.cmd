#!/bin/bash
#SBATCH -J SC_N_0_RG_GBF_parallel
#SBATCH -o ./%x.%j.%N.out
#SBATCH -D ./
#SBATCH --clusters=cm2
#SBATCH --partition=cm2_std
#SBATCH --get-user-env
#SBATCH --nodes=8
#SBATCH --mail-type=end
#SBATCH --mem=10000mb
#SBATCH --export=NONE
#SBATCH --cpus-per-task=4
#SBATCH --mail-user=erik.martori@tum.de
#SBATCH --time=00:10:00

module load slurm_setup
module load python
python SC_N_0_RG_GBF_parallel.py
