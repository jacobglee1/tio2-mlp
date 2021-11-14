#!/bin/bash
#SBATCH --account T2-CS061-CPU
#SBATCH --partition cclake    
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --time 12:00:00
module purge
module load rhel7/default-peta4
module load python/2.7
module load python/3.5
p=SPRESS
prefix=SYS
source ~/.bashrc
# cd ${prefix}-P-$p-T-100
n=$(head -n 1 start.xyz)
dim=$((3*n))
sed -e "s/PRESSURE/$p/g" -e "s/PREFIX/${prefix}/" ../in-har.lmp > ${prefix}-P-$p-har.lmp
sed -e "s/PRESSURE/$p/g" -e "s/PREFIX/${prefix}/" -e "s/MATRIXDIM/${dim}/g" ../input-har.xml > ${prefix}-P-$p-har.xml
i-pi ${prefix}-P-$p-har.xml &> log-ipi-har &
sleep 60
mpirun -np 1 n2p2-dir/src/interface/lammps-nnp/src/lmp_mpi < ${prefix}-P-$p-har.lmp &> log-lmp-har &
wait
# cd ..
