module load python/2.7
for p in {0..70..10}; do
for t in {100..1500..100}; do
for a in $(cat ./knownphase.list); do
cd md90-$a-P-$p-T-$t
echo $a-$p-$t
python ../vol-stats.py a p t
cd ..
done; done; done
