rm *.res
module load python/3.7
for a in $(cat ../knownphase.list); do
echo $a
python3 ./tiOnly2.py $a >> $a-ti.res
done
