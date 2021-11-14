import numpy as np
from thermodynamic_integration import *
import sys
import os
import scipy.integrate

def main(phase):
    nptMdDir = '../npt-md/md90-'
    T0 = 100
    Ps = np.linspace(0, 70, 8)
    Ts = np.linspace(100, 1500, 15)
    PTVH = []
    for P in Ps:
        Hs = []
        for i in range(len(Ts)):
            if os.path.isfile(nptMdDir + phase + '-P-' + str(int(P)) + '-T-' + str(int(Ts[i])) + '/stats.txt'):
                nptFile = open(nptMdDir + phase + '-P-' + str(int(P)) + '-T-' + str(int(Ts[i])) + '/stats.txt')
                nptInfo = np.asarray([line.split() for line in nptFile])
                Hs.append(float(nptInfo[7][1])*0.043363)
                dG_T = scipy.integrate.trapz(np.array([-Hs[j]/Ts[j]**2 for j in range(len(Hs))]), dx=100)
                print(str(int(P)) + ' ' + str(int(Ts[i])) + ' ' + str(dG_T))
            else:
                #print(str(Ts[i]) + '-' + str(P) + 'not available')
                break
    

    
    

if __name__ == '__main__':
    main(sys.argv[1])
