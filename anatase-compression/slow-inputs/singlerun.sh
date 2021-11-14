#!/bin/bash
#SBATCH --account T2-CS061-CPU
#SBATCH --partition cclake
#SBATCH --nodes 1
#SBATCH --ntasks 32
#SBATCH --time 36:00:00

module purge
module load rhel7/default-peta4

source ~/.bashrc

mpirun -np 32 lmp_nnp_plumed < TiO2.in > lmplog &

wait
