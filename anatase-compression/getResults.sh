for a in cotunnite baddeleyite; do
for t in 300 500 800 1000 1500 2000; do
for n in 1 2; do
for p in 20 30; do
cp $a-T-$t-R-$n-p$p/log.lammps dnld/$a-P-$p-T-$t-R-$n
done; done; done; done
