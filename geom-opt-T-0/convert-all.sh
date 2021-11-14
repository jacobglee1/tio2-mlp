for name in $(cat ../knownphase.list); do 

for pp in {0..70..10}; do

bash ../res2lmpin.sh TiO2_${pp}p0-${name}.res > $name-P-$pp.conf

done
done
