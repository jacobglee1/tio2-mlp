t=$1

for a in {0..10000}; do

if [ -e ${a}.xyz ]; then 
sed -e "s/PREFIX/$a/" -e "s/TEMPERATURE/$t/" ../xyz2lammpsdata.py | python;  
fi
done
