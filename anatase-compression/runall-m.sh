prefix='anatase'
for t in 300 500 800 1000 1500 2000; do 
for r in 8 9 10 11; do
cp -r medium-inputs m-$prefix-T-$t-R-$r; 
sed -i -e "s/TTTTT/$t/" -e "s/PREFIX/${prefix}/" -e "s/RRRRR/$r/" m-$prefix-T-$t-R-$r/TiO2.in; 
cd m-$prefix-T-$t-R-$r
sbatch singlerun.sh
cd ..
done
done
