import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import sys

# Initialise arrays
phases = ['anatase', 'baddeleyite', 'brookite', 'C2c', 'columbite', 'cotunnite', 'fluorite', 'hollandite', 'OIphase', 'Pca21', 'pyrite', 'ramsdellite', 'rutile', 'TiO2B']
Ps = np.linspace(0, 70, 8)
Ts = np.linspace(100, 1500, 15)
pd = np.empty((8, 15))
pd[:,:] = -1
Gs = np.empty((8, 15))
Gs[:,:] = 1e6
data = {}
GData = {}
for i in range(len(phases)):
    data[phases[i]] = i
    GData[phases[i]] = np.zeros((len(Ps), len(Ts)))
    GData[phases[i]][:,:] = 5000*Ts/1500 - 2000

# Get Gibbs free enrgy data
run = 'all-GT2.res'
f = open(run)
for line in f:
    lst = line.split()
    P = int(float(lst[1]))
    G = float(lst[3])
    T = int(float(lst[2]))
    iP = int(P/10)
    iT = int(T/100) - 1
    phase = lst[0]
    GData[phase][iP, iT] = G

    # Exclude structures where a phase transition has occurred
    if G < Gs[iP, iT] and phase not in ['pyrite', 'TiO2B', 'fluorite', 'hollandite'] and not (phase == 'anatase' and iP > 1) and not (phase == 'brookite' and iP > 2):
        Gs[iP, iT] = G
        pd[iP, iT] = int(data[phase])


# Initialise interpolated arrays
P0s = np.linspace(0,70,8)
T0s = np.linspace(100,1500,15)
Ps = np.linspace(0, 70, 701)
Ts = np.linspace(100, 1500, 1401)
GInterp1 = {}
GInterp2 = {}
Gs = np.zeros((len(Ps), len(Ts)))
Gs[:,:] = 1e6

# Do interpolation
for phase in phases:
    GInterp1[phase] = np.empty((len(Ps), len(T0s)))
    GInterp2[phase] = np.empty((len(Ps), len(Ts)))
    for T0 in T0s:
        GInterp1[phase][:, int(T0/100 - 1)] = np.interp(Ps, P0s, GData[phase][:,int(T0/100 - 1)])
        for P in Ps:
            GInterp2[phase][int(P*(len(Ps)-1)/70), :] = np.interp(Ts, T0s, GInterp1[phase][int(P*(len(Ps)-1)/70),:])

pd = np.empty((len(Ps), len(Ts)))
pd[:,:] = -1
for iP in range(len(Ps)):
    for iT in range(len(Ts)):
        for k in range(len(phases)):
            # Exclude structures where a phase transition has occurred
            if GInterp2[phases[k]][iP, iT] < Gs[iP, iT] and not (phases[k] in ['TiO2B', 'pyrite', 'fluorite', 'hollandite']) and not (phases[k] == 'anatase' and Ps[iP] > 10) and not (phases[k] == 'brookite' and Ps[iP] > 20):
                Gs[iP, iT] = GInterp2[phases[k]][iP, iT]
                pd[iP, iT] = int(data[phases[k]])

# Determine phase boundaries
anaBad = []
badCot = []
broBad = []
broAna = []
for iP in range(len(Ps)-1):
    for iT in range(len(Ts)-1):
        if phases[int(pd[iP, iT])] == 'anatase' and phases[int(pd[iP+1, iT])] == 'baddeleyite':
            anaBad.append([(iP+0.5)*70/(len(Ps)-1), (iT+1)*1500/len(Ts)])
        elif phases[int(pd[iP, iT])] == 'baddeleyite' and phases[int(pd[iP+1, iT])] == 'cotunnite':
            badCot.append([(iP+0.5)*70/(len(Ps)-1), (iT+1)*1500/len(Ts)])
        elif phases[int(pd[iP, iT])] == 'brookite' and phases[int(pd[iP+1, iT])] == 'baddeleyite':
            broBad.append([(iP+0.5)*70/(len(Ps)-1), (iT+1)*1500/len(Ts)])
        elif phases[int(pd[iP, iT+1])] == 'brookite' and phases[int(pd[iP, iT])] == 'anatase':
            broAna.append([(iP+0.5)*70/(len(Ps)-1), (iT+1)*1500/len(Ts)])

anaBad = np.array(anaBad)
badCot = np.array(badCot)
broBad = np.array(broBad)
broAna = np.array(broAna)

# Plotting
plt.figure()
plt.plot(anaBad[:,1], anaBad[:,0], 'b')#, label='anaBad')
plt.plot(badCot[:,1], badCot[:,0], 'green')#, label='badCot')
plt.plot(broBad[:,1], broBad[:,0], 'orange')#, label='broBad')
plt.plot(broAna[:,1], broAna[:,0], 'b')#, label='broBad')
plt.ylim(0,70)
plt.xlim(0,1500)
plt.savefig('pdLines.png', dpi=400)