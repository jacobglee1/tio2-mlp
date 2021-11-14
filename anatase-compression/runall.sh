prefix='TiO2B' #'columbite' #'anatase' #'cotunnite'
for t in 300 500 800 1000 1500 2000; do 
for r in 1 2; do
cp -r inputs $prefix-T-$t-R-$r; 
#cp -r inputs-p20 $prefix-T-$t-R-$r-p20; 
sed -i -e "s/TTTTT/$t/" -e "s/PREFIX/${prefix}/" -e "s/RRRRR/$r/" $prefix-T-$t-R-$r/TiO2.in; 
#sed -i -e "s/TTTTT/$t/" -e "s/PREFIX/${prefix}/" -e "s/RRRRR/$r/" $prefix-T-$t-R-$r-p20/TiO2.in; 
cd $prefix-T-$t-R-$r
#cd $prefix-T-$t-R-$r-p20
sbatch singlerun.sh
cd ..
done
done
