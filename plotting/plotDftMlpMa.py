import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import os
import matplotlib as mpl


### DFT ###

dftData = {}
phases = ['anatase', 'baddeleyite', 'brookite', 'columbite', 'cotunnite', 'C2c', 'fluorite', 'hollandite', 'OIphase', 'Pca21', 'pyrite', 'ramsdellite', 'rutile', 'TiO2B']
for phase in phases:
    dftData[phase] = [np.zeros(8), np.zeros(8)]

for P in range(0, 71, 10):
    f= open('../dft/Enthalpy-PBEsol/Enthalpy-PBEsol/good_castep/PBEsol-P-' + str(P) + 'GPa/PBEsol-P-' + str(P) + 'GPa-ranking.dat')
    i = 0
    baseH = 0
    for line in f:
        lst = line.split()
        phase = lst[0]
        if i == 0:
            baseH = float(lst[3])
            dftData[phase][0][int(P/10)] = int(P)
            dftData[phase][1][int(P/10)] = float(lst[3])
        elif phase in phases:
            dftData[phase][0][int(P/10)] = int(P)
            dftData[phase][1][int(P/10)] = baseH + float(lst[3])
        i += 1

normalisation = dftData['OIphase'][1][:].copy()
for phase in dftData:
    for i in range(len(dftData[phase][0])):
        dftData[phase][1][i] -= normalisation[i]
    dftData[phase][1] = list(dftData[phase][1])
    dftData[phase][0] = list(dftData[phase][0])

# Remove points where the structure is different

for P in range(7,2,-1):
    dftData['brookite'][0].pop(P)
    dftData['brookite'][1].pop(P)

for P in range(2,-1,-1):
    dftData['ramsdellite'][0].pop(P)
    dftData['ramsdellite'][1].pop(P)

for P in range(7,4,-1):
    dftData['hollandite'][0].pop(P)
    dftData['hollandite'][1].pop(P)


### MLP ###

Ps = np.linspace(0,70,8)
smoothP = np.linspace(min(Ps), max(Ps), 200)

mlpData = {}
for phase in phases:
    mlpData[phase] = [np.linspace(0, 70, 8), np.empty(8)]
    mlpData[phase][1][:] = np.nan
    for i in range(len(Ps)):
        P = int(Ps[i])
        if os.path.isfile('workdir/TiO2_' + str(P) + 'p0-' + phase + '.res'):
            f = open('workdir/TiO2_' + str(P) + 'p0-' + phase + '.res').readlines()
            info = [line.split() for line in f]
            H = float(info[0][4]) / (int(info[0][7])/3)
            mlpData[phase][1][i] = H

normalisation = mlpData['OIphase'][1].copy()

for phase in mlpData:
    i = 0
    mlpData[phase][1][:] -= normalisation

for phase in mlpData:
    mlpData[phase][1] = list(mlpData[phase][1])
    mlpData[phase][0] = list(mlpData[phase][0])
    for i in range(len(mlpData[phase][1])-1,0,-1):
        if np.isnan(mlpData[phase][1][i]):
            mlpData[phase][1].pop(i)
            mlpData[phase][0].pop(i)

# Remove points where the structure is different

for P in range(7,3,-1):
    mlpData['anatase'][0].pop(P)
    mlpData['anatase'][1].pop(P)

for P in range(7,1,-1):
    mlpData['C2c'][0].pop(P)
    mlpData['C2c'][1].pop(P)

for P in range(7,1,-1):
    mlpData['TiO2B'][0].pop(P)
    mlpData['TiO2B'][1].pop(P)

for P in range(7,1,-1):
    mlpData['hollandite'][0].pop(P)
    mlpData['hollandite'][1].pop(P)

for P in range(3,-1,-1):
    mlpData['ramsdellite'][0].pop(P)
    mlpData['ramsdellite'][1].pop(P)

for P in [7]:
    mlpData['pyrite'][0].pop(P)
    mlpData['pyrite'][1].pop(P)


### MA ###

f = open('enthalpy-MA-0K-in-kcal-per-formula-unit.dat')
phasesMa = ['anatase', 'baddeleyite', 'brookite', 'columbite', 'cotunnite', 'C2c', 'fluorite', 'hollandite', 'OIphase', 'pyrite', 'ramsdellite', 'rutile', 'TiO2B']

maData = {}
for phase in phases:
    maData[phase] = [np.linspace(0, 70, 141), np.empty(141)]
    maData[phase][1][:] = np.nan
i = 0
for line in f:
    if i >= 2:
        lst = line.split()[1:9] + line.split()[24:29]
        for j in range(0, len(lst)):
            if lst[j] == 'NaN':
                maData[phasesMa[j]][1][i-2] = np.nan
            else:
                maData[phasesMa[j]][1][i-2] = float(lst[j])/23.061
    i += 1

normalisation = maData['OIphase'][1][:].copy()
for phase in maData:
    for i in range(len(maData[phase][0])):
        maData[phase][1][i] -= normalisation[i]

phases = ['anatase', 'baddeleyite', 'brookite', 'columbite', 'cotunnite', 'C2c', 'fluorite', 'hollandite', 'OI', 'Pca21', 'pyrite', 'ramsdellite', 'rutile', 'TiO2B']

# Rename OIphase to OI
dftData['OI'] = dftData.pop('OIphase')
mlpData['OI'] = mlpData.pop('OIphase')
maData['OI']  = maData.pop('OIphase')


### PLOTTING ###

fig = plt.figure(figsize=(11,4))
mpl.rc('image', cmap='gray')
plt.rcParams["axes.prop_cycle"] = plt.cycler("color",plt.cm.tab20(np.linspace(0,1,20)))#len(phases)+1)))
gs = fig.add_gridspec(1, 3, wspace=0)
(ax1, ax2, ax3) = gs.subplots(sharex='col', sharey='row')
for phase in phases:
    ax1.plot(maData[phase][0], maData[phase][1],label=phase)
    ax2.plot(mlpData[phase][0], mlpData[phase][1],label=phase)
    ax3.plot(dftData[phase][0], dftData[phase][1],label=phase)
plt.ylim(-0.6,2)
ax2.legend(phases, loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=7, frameon=False)
ax2.set_xlabel('Pressure / GPa')
ax1.set_ylabel('Enthapy / eV/f.u.')
ax1.text(4,1.8,'(a) MA')
ax2.text(4,1.8,'(b) MLP')
ax3.text(4,1.8,'(c) DFT')
ax1.set_xlim(0,70)
ax2.set_xlim(0,70)
ax3.set_xlim(0,70)
plt.savefig('allH6.png', bbox_inches='tight', dpi=400)