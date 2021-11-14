prefix='anatase'
#for t in 300 500 800 1000 1500 2000; do 
for t in 2000; do
cp -r huge-inputs xl-$prefix-T-$t; 
sed -i -e "s/TTTTT/$t/" -e "s/PREFIX/${prefix}/" xl-$prefix-T-$t/TiO2.in; 
cd xl-$prefix-T-$t
sbatch singlerun.sh
cd ..
done
