import sys
import numpy as np

def main(phase,P,T):
    
    log = open('log.lammps',"r")
    i = 0
    times = []
    #Ts = []
    Ps = []
    #Vs = []
    #Ks = []
    #Es = []
    Hs = []
    volumes = []
    ending = 0
    for line in log:
        lst = line.split()
        if len(lst) > 0 and lst[0] == 'Step':
            initial = i
        if len(lst) > 0 and line.split()[0] == 'Loop':
            ending = i
            break
        i += 1
    if ending == 0:
        ending = i-2
    j = 0
    log2 = open('log.lammps')
    for line in log2:
        if initial < j < ending:
            lst = line.split()
            if lst[0] != '###' and lst[0] != 'WARNING:':
                times.append(float(lst[1]))
                #Ts.append(float(lst[3]))
                Ps.append(float(lst[4]))
                #Vs.append(float(lst[5]))
                #Ks.append(float(lst[6]))
                #Es.append(float(lst[7]))
                Hs.append(float(lst[8]))
                volumes.append(float(lst[9]))
                natom = float(lst[2])
        j += 1
    
    aveVol = np.mean(volumes[int(len(volumes)*0.8):])
    initialVol = volumes[0]
    scaleLength = (aveVol / initialVol)**(1/3)

    # probability density function (histogram) of volumes (/fu) 
    hist 	= np.histogram(volumes[int(len(volumes)*0.8):],bins=20)
    dVol 	= hist[1][1] - hist[1][0]
    volBins 	= hist[1][:len(hist[1])-1]*3/natom
    n 		= sum(hist[0])
    pdf 	= [hist[0][i]/(dVol*n) for i in range(len(hist[0]))] 
    aveVolfu 	= aveVol*3/natom
    sdVol 	= np.std(volumes[int(len(volumes)*0.8):])*1/np.sqrt(n)
    sdVolfu 	= sdVol*3/natom

    for i in range(len(volBins)-1):
        if volBins[i] <= aveVolfu < volBins[i+1]:
            rho 	 = pdf[i]
            binnedAveVol = volBins[i]
            #err 	  = (mapdf[i-1:i+2]) - min(pdf[i-1:i+2]))/2
        if volBins[i] <= aveVolfu - sdVolfu < volBins[i+1]:
            ll = i
        if volBins[i] <= aveVolfu + sdVolfu < volBins[i+1]:
            ul = i
    err    = (max(pdf[ll:ul+1]) - min(pdf[ll:ul+1]))/2
    statsf = open('stats.txt',"w")
    statsf.write('aveVolume/fu: ' + str(aveVolfu) + ' \n')
    statsf.write('binnedAveVol/fu: ' + str(binnedAveVol) + ' \n')
    statsf.write('binSize: ' + str(dVol*3/natom) + ' \n')
    statsf.write('sdVol/fu: ' + str(sdVolfu) + ' \n')
    statsf.write('rho: ' + str(rho) + ' \n')
    statsf.write('rhoErr: ' + str(err) + ' \n')
    statsf.write('numSamples: ' + str(n) + ' \n')

    aveHfu = np.mean(Hs)*(3/natom)
    sdHfu  = np.std(Hs)*(3/natom)*1/np.sqrt(n)
    statsf.write('aveH/fu: ' + str(aveHfu) + ' \n')
    statsf.write('sdH/fu: ' + str(sdHfu) + ' \n')

    # AUTOCORRELATION TIME (very similar for volume, pressure, enthalpy, etc)
    eqHs 	= np.array(Hs[int(len(Hs)*0.8):])
    aveH 	= np.mean(eqHs)
    normHs 	= eqHs - aveH
    ac 		= np.correlate(normHs,normHs,'same')
    chi 	= ac[ac.size//2:]/max(ac)
    for i in range(len(chi)):
        if chi[i] < 0.368: # e^-1 = 0.368
            autoCorrTime = i
            break

    errHfu = sdHfu * np.sqrt(2*autoCorrTime)
    statsf.write('autoCorrTime: ' + str(autoCorrTime) + ' \n')
    statsf.write('ACenthalpyErrfu: ' + str(errHfu) + ' \n')

    # PRESSURE
    aveP   = np.mean(Ps[int(len(Hs)*0.8):])
    sderrP = np.std(Ps[int(len(Hs)*0.8):])/np.sqrt(n)
    ACerrP = sderrP*np.sqrt(2*autoCorrTime)
    statsf.write('aveP: ' + str(aveP) + '\n')
    statsf.write('sderrP: ' + str(sderrP) + '\n')
    statsf.write('ACerrP: ' + str(ACerrP) + '\n')

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3])
