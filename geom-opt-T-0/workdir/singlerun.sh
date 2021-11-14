#!/bin/bash
#SBATCH --account T2-CS061-CPU
#SBATCH --partition cclake
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --time 02:00:00

module purge
module load rhel7/default-peta4

source ~/.bashrc

name=NNNNN
#pp=PPPPP

for pp in {70..0..-5}; do

if [ -e ../TiO2_now-${name}.res ]; then
bash ../res2lmpin.sh ../TiO2_now-${name}.res > $name-P-$pp.conf
else
bash ../res2lmpin.sh ../TiO2_20p0-${name}.res > $name-P-$pp.conf
fi

sed -e "s/NAMENOW/${name}/g" -e "s/PRESSURE/$pp/" TiO2.in > $name-P-$pp.in
mpirun -np 1 lmp_nnp_plumed < ${name}-P-$pp.in
wait

# Construct a fake Castep output file

grep Pressure: ${name}-P-$pp.lammps | tail -1 | awk '{print " *  Pressure: "$2}' > ${name}-P-$pp.castep
grep Enthalpy: ${name}-P-$pp.lammps | tail -1 | awk '{print " PP3: Final Enthalpy     = "$2}' >> ${name}-P-$pp.castep
grep Volume:   ${name}-P-$pp.lammps | tail -1 | awk '{print "Current cell volume = "$2}' >> ${name}-P-$pp.castep

# Save the final structure in Castep -out.cell format

lammps2cell ${name}-P-$pp > ${name}-P-$pp-out.cell

castep2res ${name}-P-$pp | sed -e "s/${name}-P-$pp/TiO2_${pp}p0-$name/" > TiO2_${pp}p0-${name}.res  -e "s/LAMM/O/" -e "s/data/Ti/" -e "s/LAMdat/O Ti/" > TiO2_${pp}p0-${name}.res

sym=$(symm TiO2_${pp}p0-${name} | sed 's/\//SLASH/')
sed -i "s/(P1)/$sym/" TiO2_${pp}p0-${name}.res
sed -i 's/SLASH/\//' TiO2_${pp}p0-${name}.res 

cp TiO2_${pp}p0-${name}.res ../TiO2_now-${name}.res
rm ${name}-P-$pp.castep ${name}-P-$pp.conf ${name}-P-$pp.in ${name}-P-$pp.lammps ${name}-P-$pp.lammpstrj ${name}-P-$pp-out.cell

done
