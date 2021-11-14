from ase.io import read, write

tmp = read('PREFIX.xyz')
write('T-TEMPERATURE-s-PREFIX.data',tmp,format='lammps-data')
write('TiO2-T-TEMPERATURE-s-PREFIX.res',tmp)
