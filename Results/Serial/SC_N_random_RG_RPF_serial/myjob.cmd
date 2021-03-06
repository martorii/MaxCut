#!/bin/bash
#SBATCH -J SC_N_random_RG_RPF_Serial
#SBATCH -o ./%x.%j.%N.out
#SBATCH -D ./
#SBATCH --clusters=serial
#SBATCH --partition=serial_std
#SBATCH --get-user-env
#SBATCH --mail-type=end
#SBATCH --cpus-per-task=1
#SBATCH --mem=10000mb
#SBATCH --export=NONE
#SBATCH --mail-user=erik.martori@tum.de
#SBATCH --time=24:00:00

module load slurm_setup
module load python
python SC_N_random_RG_RPF_Serial.py
