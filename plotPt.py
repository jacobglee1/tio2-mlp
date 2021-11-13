import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import os
import matplotlib as mpl
from scipy.ndimage.filters import uniform_filter1d

def getData(f):
    
    i = 0
    times = []
    Ts = []
    Ns = []
    Ps = []
    Vs = []
    Ks = []
    Es = []
    Hs = []
    volumes = []
    initial = 0
    ending = 0
    ending2 = 0

    for line in open(f):
        lst = line.split()
        if len(lst) > 0 and lst[0] == 'Step':
            if initial == 0:
                initial = i
            else:
                initial2 = i
        if len(lst) > 0 and line.split()[0] == 'Loop':
            if ending == 0:
                ending = i
            else:
                ending2 = i
        if i == 23:
            numAtoms = int(lst[0])
        if i == 53:
            targetT = int(lst[3])
        i += 1

    if initial2 == 0:
        print('ERROR: No second run')
    if ending2 == 0:
        ending2 = i-1

    j = 0

    inpt2 = open(f)
    for line in inpt2:
        if initial < j < ending or initial2 < j < ending2:
            lst = line.split()
            if lst[0] != '###' and lst[0] != 'WARNING:' and len(lst) == 9:
                times.append(float(lst[1]))
                Ts.append(float(lst[2]))
                Ps.append(float(lst[3])/9869.23)
                Vs.append(float(lst[4])*0.043*3/numAtoms)
                Ks.append(float(lst[5])*0.043*3/numAtoms)
                Es.append(float(lst[6])*0.043*3/numAtoms)
                Hs.append(float(lst[7])*0.043*3/numAtoms)
                volumes.append(float(lst[8])*3/numAtoms)
        j += 1
    
    return [times, Ts, Ps, Hs, volumes]

#Ts = [300, 500, 800, 1000, 1500, 2000]
Ts = [300, 2000]
linewidth = 0.5
for i in range(len(Ts)):
    print('Fetching results for T = ' + str(Ts[i]))
    
    cotData = getData('cotunnite-P-30-T-' + str(Ts[i]) + '-R-1')   # cotunnite
    badData = getData('baddeleyite-P-20-T-' + str(Ts[i]) + '-R-1') # baddeleyite
    cotData = np.array(cotData)
    badData = np.array(badData)
    anaAllData = []
    prefix = ['', 'm-', 'l-']
    for k in range(3):
        for r in range(1,13):
            anaData = getData(prefix[k] + 'anatase-T-' + str(Ts[i]) + '-R-' + str(r))
            anaData = np.array(anaData)
            anaAllData.append(anaData)
    #print(anaAllData)
    #anaAllData = np.array(anaAllData)

    # Plotting
    fig = plt.figure(figsize=(5,7))
    gs = fig.add_gridspec(2, 1, hspace=0)
    cmap = mpl.cm.get_cmap('tab20')
    (ax1, ax2) = gs.subplots(sharex='col', sharey='row')
    
    width = 100
    
    coeffs = np.polyfit(np.linspace(cotData[2,999], cotData[2, -1], len(cotData[2, 999:])), (cotData[3,999:]), 1)
    a, b = coeffs[0], coeffs[1] # y = a*P + b
    size = ['128 f.u.', '432 f.u.', '1024 f.u.']
    
    ax1.plot([], [], color=cmap(6/20),  label='baddeleyite')
    ax1.plot([], [], color=cmap(8/20),  label='cotunnite')

    for j in range(3):
        ax1.plot([], [], color=cmap(2*j/21),  label='anatase (' + size[j] +')')
        for r in range(0,12):
            ax1.plot(np.linspace(np.mean(anaAllData[j*12+r][2,0:100]), np.mean(anaAllData[j*12+r][2,-100:-1]), len(anaAllData[j*12+r][2, 999:])), uniform_filter1d(anaAllData[j*12+r][4,999:], width), color=cmap(j*2/21), linewidth=linewidth)#, label='anatase (' + str(size(i)) +')')
            length = min(len(anaAllData[j*12+r][2,:]), len(cotData[2,:]))
            ax2.plot(np.linspace(np.mean(anaAllData[j*12+r][2,0:100]), np.mean(anaAllData[j*12+r][2,-100:-1]), length-999), uniform_filter1d(anaAllData[j*12+r][3,999:length], width) - a*np.linspace(np.mean(anaAllData[j*12+r][2,0:100]), np.mean(anaAllData[j*12+r][2,-100:-1]), length-999) - b, color=cmap(j*2/21), linewidth=linewidth)#, label='anatase (' + str(r) +')')
    
    ax1.plot(np.linspace(20,70,len(badData[4,999:])), uniform_filter1d(badData[4,999:], width), color=cmap(6/20), linewidth=linewidth*2, alpha=0.7)
    ax2.plot(np.linspace(20,70,len(badData[4,999:])), uniform_filter1d(badData[3,999:] - a*np.linspace(20,70,len(badData[4,999:])) - b, width), color=cmap(6/20), linewidth=linewidth, alpha=0.7)
    ax1.plot(np.linspace(30,70,len(cotData[4,999:])), uniform_filter1d(cotData[4,999:], width), color=cmap(8/20), linewidth=linewidth*2, alpha=0.7)
    ax2.plot(np.linspace(30,70,len(cotData[4,999:])), uniform_filter1d(cotData[3,999:] - a*np.linspace(30,70,len(cotData[4,999:])) - b, width), color=cmap(8/20), linewidth=linewidth, alpha=0.7)
    
    letter = ['a', 'b']

    plt.xlim(0, 70)
    ax1.legend(loc='upper right', fontsize=8, edgecolor='black')
    ax2.set_xlabel('Pressure / GPa')
    ax2.set_ylabel('Enthapy / eV/f.u.')
    ax1.set_ylabel(r'Volume / $\AA^3$/f.u.')
    ax2.set_ylim(-0.8,1.7)
    ax1.set_ylim(21,39)
    ax1.text(0,20,'(' + letter[i] + ') ' + str(Ts[i]) + ' K')
    plt.savefig('anatase-T-' + str(Ts[i]) + '.png', bbox_inches='tight', dpi=400)
