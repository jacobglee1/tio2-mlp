for t in 300 500 800 1000 1500 2000; do 
for r in `seq 1 12`; do 
for s in 2000 4000 6000 8000 10000; do 
cp anatase-T-$t-R-$r/$s.res geop/anatase-T-$t-S-$s-R-$r.res; 
done; done; done
