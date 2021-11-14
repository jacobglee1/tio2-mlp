n=90
module load python/3.5
t=100
for p in {0..70..10}; do
for a in $(cat ./knownphase.list); do
echo $a-$p-$t
mkdir $a-P-$p-T-$t
cd $a-P-$p-T-$t
cp /home/jgl43/rds/hpc-work/mlp-md/md$n-$a-P-$p-T-$t/$a-P-$p-T-$t-last.lammpstrj .
sed -e "s/NAMENOW/$a/g" -e "s/PRESSURE/$p/" -e "s/TEMPERATURE/$t/" ../TiO2.in > $a-P-$p-T-$t.in
sed -e "s/NAMENOW/$a/g" -e "s/PRESSURE/$p/" -e "s/TEMPERATURE/$t/" ../template-jobscript > jobscript
sbatch jobscript
cd ..
done; done
