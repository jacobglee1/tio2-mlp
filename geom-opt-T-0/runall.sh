for a in $(awk '!/#/{print $1}' ../newphases.list); do 
	#bash singlerun.sh $a $p; wait; 
#if [ ! -e TiO2_${p}p0-${a}.res ]; then
sed -e "s/NNNNN/$a/" -e "s/PPPPP/$p/" singlerun.sh | sbatch	
#fi

done
