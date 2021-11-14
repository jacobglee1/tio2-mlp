module load python/3.7
for a in $(cat ../knownphase.list); do
for p in {0..70..10}; do
python3 ti1d5.py $a $p >> all-GT1.res
done; done
