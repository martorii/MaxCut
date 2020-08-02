#!/bin/bash
#SBATCH -J SC_N_0_DA_GBF_Serial
#SBATCH -o ./%x.%j.%N.out
#SBATCH -D ./
#SBATCH --clusters=serial
#SBATCH --partition=serial_long
#SBATCH --get-user-env
#SBATCH --mail-type=end
#SBATCH --mem=10000mb
#SBATCH --export=NONE
#SBATCH --cpus-per-task=4
#SBATCH --mail-user=erik.martori@tum.de
#SBATCH --time=3-00:00:00

module load slurm_setup
module load python
python SC_N_0_DA_GBF_Serial.py
