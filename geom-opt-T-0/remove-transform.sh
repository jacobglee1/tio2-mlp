ca -r -l > ranking.txt

if [ ! -e transformed ]; then mkdir transformed; fi
nline=$(wc -l ranking.txt | awk '{print $1}')

for nl in `seq 1 $nline`; do
	line=$(head -n $nl ranking.txt | tail -n 1)
	name=$(echo $line | awk '{print $1}')

        system=$(echo $name | sed 's/-/ /' | awk '{print $2}')
        refsym=$(grep $system ../ref-rankings.txt | awk -v s=$system '$1==s{print $7}'| sed -e 's/\///' -e 's/-//')

	sym=$(echo $line | awk '{print $7}' | sed -e 's/\///' -e 's/-//')
	#echo $name $sym $refsym
	
      if [ $sym != $refsym ] ; then
		echo $name $sym $refsym
		mv $name.res transformed
	fi
done
