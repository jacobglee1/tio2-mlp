for p in {0..70..10}; do
for a in $(cat ./knownphase.list); do
cd $a-P-$p-T-100
sed -e "s/SPRESS/$p/g" -e "s/SYS/${a}/" ../jobscript-har.sh > $a-P-$p-har.job
chmod +x $a-P-$p-har.job
sbatch $a-P-$p-har.job
cd ..
done; done


