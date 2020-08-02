#!/bin/bash
#SBATCH -J Ratios_gurobi
#SBATCH -o ./%x.%j.%N.out
#SBATCH -D ./
#SBATCH --clusters=cm2_tiny
#SBATCH --partition=cm2_tiny
#SBATCH --get-user-env
#SBATCH --mail-type=end
#SBATCH --export=NONE
#SBATCH --cpus-per-task=28
#SBATCH --mail-user=erik.martori@tum.de
#SBATCH --time=3-00:00:00

module load slurm_setup
module load python
source activate py36
python Ratios_gurobi.py
