import sys
import numpy as np
from scipy import stats
import os.path

go0kDir     = '../geom-opt-T-0'
goT0Dir     = '../geom-opt-T-100'
nptMdDir    = '../npt-md/md90-'
ipiDir      = '../ipi-phonons-and-nvt'
tiDir       = '.'

def main(PHASE, PRESSURE):
    # Compute the Gibbs free energy for PHASE at PRESSURE for all temperatures.
    kb      = 3.1668105e-06 # Boltzmann const in Hartree
    ha2ev   = 27.211386
    kbev    = kb*ha2ev # Boltzmann const in eV
    T0      = 100

    # The energy units are eV and eV/fu, unless specified otherwise.
    # A is the Helmholtz free energy (denoted F in the paper).
    # Factors of 3/N are for converting values to values per formula unit

    # 0K Enthalpy
    i = 0
    goFile = open(go0kDir + '/TiO2_' + PRESSURE + 'p0-' + PHASE + '.res')
    P0 = float(PRESSURE)*1.0e9
    for line in goFile:
        if i == 0:
            lst = line.split()
            H0tot = float(lst[4])
            Ngo = float(lst[7])
            V0 = float(lst[3])*1.0e-30
        i += 1
    U0 = (H0tot - (V0*P0/1.60e-19))*3/Ngo
    H0 = H0tot*3/Ngo
    # h Matrix
    hf = open(goT0Dir + '/' + PHASE + '-P-' + PRESSURE + '-T-100/' + PHASE + '-P-' + PRESSURE + '-last.lammpstrj')
    i =0
    for line in hf:
        if i == 3:
            nlst = line.split()
            Nipi = int(nlst[0])
        if i == 5:
            nlst = line.split()
            xlo_bound = float(nlst[0])
            xhi_bound = float(nlst[1])
            xy = float(nlst[2])
        if i == 6:
            nlst = line.split()
            ylo_bound = float(nlst[0])
            yhi_bound = float(nlst[1])
            xz = float(nlst[2])
        if i == 7:
            nlst    = line.split()
            zlo     = float(nlst[0])
            zhi     = float(nlst[1])
            yz      = float(nlst[2])
        i +=1
    xlo = xlo_bound - min(0.0,xy,xz,xy+xz)
    xhi = xhi_bound - max(0.0,xy,xz,xy+xz)
    ylo = ylo_bound - min(0.0,yz)
    yhi = yhi_bound - max(0.0,yz)
    lx = xhi - xlo
    ly = yhi - ylo
    lz = zhi - zlo
    h = [[lx, xy, xz], [0, ly, yz], [0, 0, lz]]
    
    volf = open(nptMdDir + PHASE + '-P-' + PRESSURE + '-T-' + str(T0) + '/' + PHASE + '-P-' + PRESSURE + '-T-' + str(T0) + '-last.lammpstrj')
    i =0
    for line in volf:
        if i == 3:
            nlst = line.split()
            Nmd = int(nlst[0])
        i += 1

    # The free energy of the reference harmonic system with fixed center of mass at 100K
    ### $A_h(T_0)=k_B T_0\sum_{i=1}^{3N-3}\ln(\frac{\hbar \omega_i}{k_B T_0})$

    phononModes = np.loadtxt(ipiDir + '/' + PHASE + '-P-' + PRESSURE + '-T-100/phonon.phonon-fd.eigval')
    Nipi = int(len(phononModes)/3)
    # The square root of the eigenvalues of the phonon modes is the frequency in Hartrees
    AharmT0 = kbev*T0*np.log(np.sqrt(phononModes[3:])/(kb*T0)).sum()*3.0/Nipi
    #print('AharmT0 = ' + str(AharmT0))

    # Anharmonic correction to A at T0 = 100K
    ### $A(T_0) = A_h(T_0) + U(0) - k_B T_0 \ln\left<\exp\left[\frac{-(U - U_\text{h} - U(0))}{k_B T_0}\right]\right>_{V,T_0,\lambda=0}$
    ### Here we first compute $A_{anh} = -k_B T_0 \ln\left<\exp\left[\dfrac{-(U - U_\text{h} - U(0))}{k_B T_0}\right]\right>_{V,T_0,\lambda=0}$
    
    anhdata = np.loadtxt(ipiDir + '/' + PHASE + '-P-' + PRESSURE + '-T-100/perfect.out')[100:,5:7]*3.0/Nipi # the ipi outputs are in Hartrees
    autocorrtime = 2 # autocorrelation time in units of timestep
    mean = np.exp(-(anhdata[:,1] - anhdata[:,0] - U0/ha2ev)/(T0*kb), dtype=np.float128).mean()
    error = np.sqrt(autocorrtime)*stats.sem(np.exp(-(anhdata[:,1] - anhdata[:,0] - U0/ha2ev)/(T0*kb), dtype=np.float128), axis=None, ddof=0)
    AanhT0 = -kbev*T0*np.log(mean)*3.0/float(Nipi)
    #AanhT0error = (3.0/float(Nipi))*T0*kbev*(np.log(mean+error)-np.log(mean-error))/2
    AanhT0error = (3.0/float(Nipi))*T0*kbev*error/mean
    AT0 = AharmT0 + U0 + AanhT0
    #print('AharmT0 = ' + str(AharmT0))
    #print('AanhT0 = ' str(AanhT0) ' +/- ' + str(AanhT0error))

    # Transform the Helmholtz free energy to the Gibbs free energy
    #### Used the isothermal-isobaric ensemble (NPT) and allowed the 3 dimensions of the triclinic simulation cell are allowed to fluctuate independently. In this case we have:
    #### $G(P,T) = A (\textbf{h},T) + P \text{det}(\textbf{h}) + k_B T \ln \rho(\textbf{h}|P,T)$.

    rhoF = open(nptMdDir + PHASE + '-P-' + PRESSURE + '-T-' + str(T0) + '/stats.txt')
    rhoInfo = [line.split() for line in rhoF]
    
    Vol         = float(rhoInfo[0][1])*1.0e-30 # per formula unit
    ErrVol      = float(rhoInfo[3][1])*np.sqrt(2*float(rhoInfo[9][1]))*1.0e-30
    Press       = float(rhoInfo[11][1])*1.0e5
    ErrPress    = float(rhoInfo[13][1])*1.0e5
    PVerror     = np.sqrt((Vol*ErrPress)**2 + (Press*ErrVol)**2)/1.60e-19

    rho     = float(rhoInfo[4][1])
    ErrRho  = float(rhoInfo[5][1])
    
    A2GT0 = [kbev*T0*np.log(rho)*(3.0/float(Nmd)), (3.0/float(Nmd))*kbev*T0*ErrRho/rho]
    #GT0 = AT0 + A2GT0[0] + (Press*Vol/1.60e-19)
    GT0 = AT0 + A2GT0[0] + (Press*np.linalg.det(h)*1.0e-30*3/(Nipi*1.60e-19))
    
    GT0error = np.sqrt(AanhT0error**2 + A2GT0[1]**2 + PVerror**2)
    #print('constituent errors: ' + str(AanhT0error) + ' ' + str(A2GT0[1]) + ' ' + str(PVerror))
    #print('GT0 = ' + str(GT0) + ' +/- ' + str(GT0error))

    T1s = np.linspace(100, 1500, 15)
    tiData = np.zeros(len(T1s))
    tiFile = open(tiDir + PHASE + '-ti.res')
    for line in tiFile:
        lst = line.split()
        if int(float(lst[0])) == int(float(PRESSURE)):
            tiData[int(float(lst[1])/100)-1] = float(lst[2])
    
    for i in range(len(T1s)):
        G = GT0*T1s[i]/100.0 + T1s[i]*tiData[i]
        print(PHASE + ' ' + PRESSURE + ' ' + str(int(T1s[i])) + ' ' + str(G))




if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])

