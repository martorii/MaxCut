#!/bin/bash
#SBATCH -J SC_N_0_RG_GBF_Serial
#SBATCH -o ./%x.%j.%N.out
#SBATCH -D ./
#SBATCH --clusters=inter
#SBATCH --partition=teramem_inter
#SBATCH --get-user-env
#SBATCH --mail-type=end
#SBATCH --cpus-per-task=1
#SBATCH --mem=10000mb
#SBATCH --export=NONE
#SBATCH --cpus-per-task=16
#SBATCH --mail-user=erik.martori@tum.de
#SBATCH --time=3-00:00:00

module load slurm_setup
module load python
python SC_N_0_RG_GBF_Serial.py
