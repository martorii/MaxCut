#!/bin/bash
#SBATCH -J SC_N_0_RG_GBF
#SBATCH -o ./%x.%j.%N.out
#SBATCH -D ./
#SBATCH --clusters=serial
#SBATCH --partition=serial_std
#SBATCH --get-user-env
#SBATCH --cpus-per-task=28
#SBATCH --mail-type=end
#SBATCH --mem=10000mb
#SBATCH --export=NONE
#SBATCH --mail-user=erik.martori@tum.de
#SBATCH --time=3-00:00:00

module load slurm_setup
module load python
python SC_N_0_RG_GBF.py
