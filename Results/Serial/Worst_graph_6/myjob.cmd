#!/bin/bash
#SBATCH -J Worst_graph_6
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
python Worst_graph_6.py
