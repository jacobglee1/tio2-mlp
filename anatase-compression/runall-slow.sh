prefix='anatase'
for t in 300 5000 1000; do 
for r in 1 2 3 4; do
cp -r slow-inputs slow-$prefix-T-$t-R-$r; 
sed -i -e "s/TTTTT/$t/" -e "s/PREFIX/${prefix}/" -e "s/RRRRR/$r/" slow-$prefix-T-$t-R-$r/TiO2.in; 
cd slow-$prefix-T-$t-R-$r
sbatch singlerun.sh
cd ..
done
done
