for p in {0..70..10}; do
for a in $(cat ./knownphase.list); do
cd $a-P-$p-T-100
sed -e "s/SPRESS/$p/g" -e "s/SYS/${a}/" ../jobscript.sh > $a-P-$p-phonon.job
chmod +x $a-P-$p-phonon.job
sbatch $a-P-$p-phonon.job
cd ..
done; done
