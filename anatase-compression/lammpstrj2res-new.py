import numpy as np
import glob,sys
from math import pi
from ase.io import read,write
from ase import Atoms as atom

def main(prefix, sstep):
    # input file
    ixyz = read(prefix,':')
    step = int(sstep)
    ifr = 0


    for ifr in range(step,len(ixyz),step):
        frtemp = ixyz[ifr]
        print(ifr, frtemp)
        print("write...", ifr)
        write(str(ifr)+'.res', frtemp)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
