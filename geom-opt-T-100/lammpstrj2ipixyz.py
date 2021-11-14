import numpy as np
import glob,sys
from math import pi

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
    names = np.zeros(natoms,dtype=str)
    q = np.zeros((natoms,3),float)
    for i in range(natoms):
        line = filedesc.readline().split()
        names[i] = line[1]
        q[i] = line[2:5]
    return [natoms, cell, names, q]

def output(op, natom, cell, names, q):
    # output
    # compute the angles
    # mode is 'abcABC', then 'cell' takes an array of 6 floats
    # the first three being the length of the sides of the system parallelopiped, and the last three being the angles (in degrees) between those sides.
    # Angle A corresponds to the angle between sides b and c, and so on for B and C.
    supercell = np.zeros(3,float)
    angles = np.zeros(3,float)

    """
    for i in range(3):
        supercell[i] = np.linalg.norm(cell[i,:])

    angles[0] = np.arccos(np.dot(cell[1],cell[2])/supercell[1]/supercell[2])/pi*180.
    angles[1] = np.arccos(np.dot(cell[0],cell[2])/supercell[0]/supercell[2])/pi*180.
    angles[2] = np.arccos(np.dot(cell[0],cell[1])/supercell[0]/supercell[1])/pi*180.
    """

    """
    xlo_bound = xlo + MIN(0.0,xy,xz,xy+xz)
    xhi_bound = xhi + MAX(0.0,xy,xz,xy+xz)
    ylo_bound = ylo + MIN(0.0,yz)
    yhi_bound = yhi + MAX(0.0,yz)
    zlo_bound = zlo
    zhi_bound = zhi
    """
    cell[0,0] -= (max(0, cell[0,1], cell[0,2], cell[0,1]+cell[0,2])-min(0, cell[0,1], cell[0,2], cell[0,1]+cell[0,2]))
    cell[1,1] -= (max(0, cell[1,2])-min(0, cell[1,2]))
    supercell[0] = cell[0,0]
    supercell[1] = np.sqrt(cell[1,1]**2.+cell[0,1]**2.)
    supercell[2] = np.sqrt(cell[2,2]**2+cell[0,2]**2.+cell[1,2]**2.)
    angles[0] = 180./pi*np.arccos((cell[0,1]*cell[0,2]+cell[1,1]*cell[1,2])/(supercell[1]*supercell[2]))
    angles[1] = 180./pi*np.arccos(cell[0,2]/supercell[2])
    angles[2] = 180./pi*np.arccos(cell[0,1]/supercell[1])
    # write
    op.write("%d\n# CELL(abcABC):     %4.8f     %4.8f     %4.8f     %4.5f     %4.5f     %4.5f   cell{angstrom}  Traj: positions{angstrom}\n" % (natom,supercell[0],supercell[1],supercell[2],angles[0],angles[1],angles[2]))
    #op.write("%d\n# CELL(abcABC):     %4.8f     %4.8f     %4.8f     %4.5f     %4.5f     %4.5f   cell{angstrom}  Traj: positions{angstrom}\n" % (natom,supercell[0],supercell[1],supercell[2], 90.0, 90.0, 90.0))
    for i in range(natom):
        #print (names[i],q[i*3],q[i*3+1],q[i*3+2])
        op.write("%s %s %s %s\n" % (names[i],q[i,0],q[i,1],q[i,2]))
    return 0

def main(prefix):
    # input file
    ixyz = open(prefix + '-last.lammpstrj',"r")
    # Output position
    opfile = open(prefix+".xyz","w")

    frames = []
    while True:
        try:
            [ na, cell, names, pos] = read_frame(ixyz)
            if np.sum(cell) > 0:
                pbc = [True, True, True]
            else:
                pbc = [False,False,False]
            #print(pbc)
            output(opfile, na, cell, names, pos)
        except:
            opfile.close()
            sys.exit()

if __name__ == '__main__':
    main(sys.argv[1])
