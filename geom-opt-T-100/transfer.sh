module load python/3.5
t=100
for p in {0..70..10}; do
for a in $(cat ./knownphase.list); do
echo $a-P-$p-T-$t
cd $a-P-$p-T-100
python3 ../final-struct.py $a-P-$p
python3 ../lammpstrj2ipixyz.py $a-P-$p
python3 ../name-el.py $a-P-$p
mkdir ../../ipi-phonons-and-nvt/$a-P-$p-T-$t
cp $a-P-$p-fixed.xyz ../../ipi-phonons-and-nvt/$a-P-$p-T-$t/start.xyz # COPY THE 100K GEOM-OPT TO ALL THE EMPTY IPI FILES
cp $a-P-$p-last.lammpstrj ../../ipi-phonons-and-nvt/$a-P-$p-T-$t/start.lammpstrj
cd ../../ipi-phonons-and-nvt/$a-P-$p-T-$t
python3 ../remove-el.py $a-P-$p-T-$t
cd ../../geom-opt-T-100
done; done
