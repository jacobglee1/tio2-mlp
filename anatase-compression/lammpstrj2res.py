import numpy as np
import glob,sys
from math import pi
from ase.io import read,write
from ase import Atoms as atom

def read_frame(filedesc):
    # 1-3
    comment = filedesc.readline()
    comment = filedesc.readline()
    comment = filedesc.readline()
    # 4
    natoms = int(filedesc.readline())
    #print(natoms)
    # 5
    comment = filedesc.readline()
    # 6,7,8
    cell = np.zeros((3,3),float)
    # line 1
    size = filedesc.readline().split()
    cell[0,0] = abs(float(size[1])-float(size[0]))
    cell[1,0] = cell[0,1] = float(size[2])
    # line 2
    size = filedesc.readline().split()
    cell[1,1] = abs(float(size[1])-float(size[0]))
    cell[0,2] = cell[2,0] = float(size[2])
    # line 1
    size = filedesc.readline().split()
    cell[2,2] = abs(float(size[1])-float(size[0]))
    cell[1,2] = cell[2,1] = float(size[2])
 
    #print(cell)
    # 9
    comment = filedesc.readline()
    # ITEM: ATOMS type x y z
    names = []
    q = np.zeros((natoms,3),float)
    for i in range(natoms):
        line = filedesc.readline().split()
        if line[1] == '1':
            names.append('O')
        else:
            names.append('Ti')
        q[i] = line[2:5]
    #print(names)
    return [natoms, cell, names, q]

def main(prefix, sstep):
    # input file
    ixyz = open(prefix,"r")
    step = int(sstep)
    ifr = 0

    frames = []
    while True:
        try:
            [ na, cell, names, pos] = read_frame(ixyz)
            if np.sum(cell) > 0:
                pbc = [True, True, True]
            else:
                pbc = [False,False,False]
            frtemp = atom(symbols=names,cell=cell,positions=pos,pbc=pbc)
            #print(frtemp)
            #frtemp.wrap()
            ifr += 1
            frames.append(frtemp)
            if ifr % step == 0:
                print(ifr, frtemp)
                print("write...", ifr)
                write(str(ifr)+'.res', frtemp)
        except:
            sys.exit()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
