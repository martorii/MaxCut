#!/bin/bash
#SBATCH -J SC_N_0_RG_GBF_parallel
#SBATCH -o ./%x.%j.%N.out
#SBATCH -D ./
#SBATCH --get-user-env
#SBATCH --clusters=mpp3
#SBATCH --nodes=1-1
#SBATCH --cpus-per-task=64
# 256 is the maximum reasonable value for CooLMUC-3
#SBATCH --mail-type=end
#SBATCH --mail-user=erik.martori@gmail.com
#SBATCH --export=NONE
#SBATCH --time=00:00:40
module load slurm_setup
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
 
module load slurm_setup
module load python
python SC_N_0_RG_GBF_parallel.py