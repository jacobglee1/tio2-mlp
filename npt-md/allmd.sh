n=90
for p in {0..70..10}; do
for t in {1100..1500..100}; do
for a in $(cat ./knownphase.list); do
        mkdir md$n-$a-P-$p-T-$t
        cd md$n-$a-P-$p-T-$t
        sed -e "s/NAMENOW/$a/g" -e "s/PRESSURE/$p/" -e "s/TEMPERATURE/$t/g" ../TiO2.in > $a-P-$p-T-$t.in
        sed -e "s/NAMENOW/$a/g" -e "s/PRESSURE/$p/" -e "s/TEMPERATURE/$t/g" ../template-jobscript > $a-P-$p-T-$t.jobscript
        sbatch $a-P-$p-T-$t.jobscript
        cd ..
done   
done
done
