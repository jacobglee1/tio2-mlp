for p in {0..70..10}; do
for t in {100..1500.100}; do
for a in $(cat ./knownphase.list); do
echo $a-$p-$t
cd md90-$a-P-$p-T-$t
python ../final-struct.py $a-P-$p-T-$t
rm *00.lammpstrj slurm* machine*
cd ..
done; done; done

