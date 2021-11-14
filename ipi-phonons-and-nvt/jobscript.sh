#!/bin/bash
#SBATCH --account ###PROJECT###
#SBATCH --partition cclake
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --time 24:00:00
module purge
module load rhel7/default-peta4
module load python/2.7
module load python/3.5
p=SPRESS
prefix=SYS
source ~/.bashrc
# cd ${prefix}-P-$p-T-100
sed -e "s/PRESSURE/$p/g" -e "s/PREFIX/${prefix}/" ../in.lmp > ${prefix}-P-$p-nnp.lmp
sed -e "s/PRESSURE/$p/g" -e "s/PREFIX/${prefix}/" ../input.xml > ${prefix}-P-$p.xml
i-pi ${prefix}-P-$p.xml &> log-ipi & 
sleep 10
mpirun -np 1 n2p2-dir/src/interface/lammps-nnp/src/lmp_mpi < ${prefix}-P-$p-nnp.lmp &> log-lmp &  
wait
rm /tmp/log-lmp.${prefix}-P-$p* /tmp/log-ipi.${prefix}-P-$p
# cd ..
