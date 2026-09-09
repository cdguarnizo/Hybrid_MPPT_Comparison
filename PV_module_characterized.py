import numpy as np
from matplotlib import pyplot as plt  #NOW LETS MAKE SOME PLOTS.
from pvmismatch import *  #THIS IMPORTS EVERYTHING WE NEED.

plt.style.use("ggplot") #USED FOR HAVE A GRID IN THE PLOT.

pvconst=pvconstants.PVconstants(npts=500) #DEFINITION OF THE NUMBER OF POINTS.
pvcell = pvcell.PVcell(Rs=2.63810001e-04, Rsh= 2.13008168e+01, Isat1_T0=2.74125847e-06, 
                       Isat2_T0=5.51382460e-10, Isc0_T0=10.61 , 
                       aRBD=0.0001036748445065697, bRBD=0.0, VRBD=-5.527260068445654, 
                       nRBD=3.284628553041425, Eg=1.1, alpha_Isc=0.0003551, Tcell=298.15, 
                       Ee=1.0, pvconst=pvconst) #THE PV CELL IS DEFINED WITH ITS CHARACTERISTIC PARAMETERS.
cell_pos = pvmodule.standard_cellpos_pat(20, [2,2,2]) #THE NUMBER OF CELLS AND THE WAY THEY ARE ORDERED ARE DEFINED.
pv_mod = pvmodule.PVmodule(cell_pos=cell_pos, pvcells = pvcell) #THE PHOTOVOLTAIC MODULE IS GENERATED FROM THE DEFINED CELLS.
pv_str = pvstring.PVstring(numberMods=1, pvmods = pv_mod, pvconst = pvconst) #THE PV ARRANGEMENT IS DEFINED AND GENERATED.
pvsys = pvsystem.PVsystem(numberStrs=1, numberMods=1, pvstrs = pv_str) #THE PV SYSTEM IS GENERATED.


def pvsim(params):
    #THIS FUNCTION RECEIVES A PROFILE OF 3 IRRADIANCES, TEMPERATURE AND VOLTAGE.
    #RETURN A DICTIONARY THAT CONTAINS THE POWER, VOLTAGE AND CURRENT CURVES, THE 
    #MAXIMUM POWER AND CURRENT VALUES AND THE CURRENT CORRESPONDING TO THE DELIVERED VOLTAGE.
    G1, G2, G3, T, Vr = params

    #THE CORRECT IRRADIANCE AND TEMPERATURE IS ENTERED FOR EACH PV CELL.
    pvsys.setSuns({0: {0: [(G1/1000., ) * 40, tuple(range(40))]}})
    pvsys.setSuns({0: {0: [(G2/1000., ) * 40, tuple(range(40,80))]}})
    pvsys.setSuns({0: {0: [(G3/1000., ) * 40, tuple(range(80,120))]}})
    pvsys.setTemps(T + 273.15)
    
    P = pvsys.Psys #THE CURRENT CURVE OBTAINED FROM A VOLTAGE SWEEP IS SAVED FROM THE GIVEN IRRADIANCE.
    indP0 = P>=0. #THE INDICES OF THE ELEMENTS THAT CONTAIN VALUES GREATER OR EQUAL TO ZERO ARE SAVED.
    P = P[indP0] #THE POWER CURVE IS SAVED.
    Vvec = pvsys.Vsys[indP0] #THE VOLTAGE CURVE IS SAVED.
    Ivec = pvsys.Isys[indP0] #THE CURRENT CURVE IS SAVED.
    ind = np.where(Vvec<Vr)[0][-1] #THE INDEX IS OBTAINED WHERE THE VOLTAGE IS EQUAL TO THE ONE ENTERED.
    Ir = Ivec[ind] #THE CURRENT CORRESPONDING TO THE ENTERED VOLTAGE IS OBTAINED.
    indm = np.argmax(P) #THE INDEX THAT CONTAINS THE MAXIMUM POWER VALUE IS OBTAINED.
    Pmax = P[indm] #MAXIMUM POWER IS OBTAINED.
    Vmax = Vvec[indm] #MAXIMUM POWER VOLTAGE IS OBTAINED.
    data = {'Ir': Ir, 'Pmax': Pmax, 'Vmax': Vmax, 'Vvec':Vvec, 'Pvec': P, 'Ivec':Ivec} #THE DICTIONARY CONTAINING THE DATA IS CREATED.
    return data

#BUILD ARRAY OF 220 SHADING PATTERNS WITH VALUES BETWEEN 0 AND 1, AND AVOIDING REPEATED CASES.
spc = np.linspace(1,10,10)*0.1
spc_mat = np.zeros((1,3))
for sp1 in spc:
    for sp2 in spc:
        for sp3 in spc:
            spc_mat = np.append(spc_mat, [[sp1, sp2, sp3]], axis = 0)
            
spc_mat = spc_mat[1:]
spc_mat = np.sort(spc_mat, axis = 1)
spc_mat = np.unique(spc_mat, axis = 0)

localMaxV = np.zeros((spc_mat.shape[0],3))
localMaxP = np.zeros((spc_mat.shape[0],3))
MaxInd = np.zeros((spc_mat.shape[0],1), dtype=int)

V_t = [] #values of voltage of the panel
Pm_t = []
Pc_t = []
Va_t = []
Ir_t = []
T = 25.0
V = 38.0

params = np.append(spc_mat[0]*1000., [T, V])
data = pvsim(params.tolist())
Ir = data['Ir']

plt.figure()
colores = ['ob','xg','1k']
dataset = []
for k in range(spc_mat.shape[0]):
    spc = spc_mat[k]   #Select k-th pattern
     
    params = np.append(spc*1000., [T, V])
    #Evaluate panel for current Voltage
    data = pvsim(params.tolist())
    Ir = data['Ir']
    Vmax = data['Vmax']
    Pmax = data['Pmax']
    Pc = Ir*V
    Pk = Pc
    Va_t.append(V)
    V_t.append(Vmax)
    Pm_t.append(Pmax)
    Pc_t.append(Pc)
    Ir_t.append(Ir)
    plt.plot(Vmax,Pmax,'+r')
    if Vmax < 15. and Vmax > 10.:
        maxCol = 0
    elif Vmax < 30.:
        maxCol = 1
    elif Vmax >= 30.:
        maxCol = 2
    MaxInd[k] = maxCol
    #Detect all maximum values
    maxs = np.where(np.convolve([-1,1],np.diff(data['Pvec']) > 0.)==1)[0]
    maxind = np.argmax(data['Pvec'])
    maxs = np.delete(maxs, np.where(maxs == maxind)[0])
    maxs = np.delete(maxs, np.where(data['Vvec'][maxs] < 10.)[0])
    #print(maxs.size)
    if maxs.size > 1:
        for m in maxs:
            if (data['Vvec'][m] < 15. ):
                col = 0
            elif (data['Vvec'][m] < 30.):
                col = 1
            elif (data['Vvec'][m] >= 30.):
                col = 2
            localMaxV[k,col] = data['Vvec'][m]
            localMaxP[k,col] = data['Pvec'][m]
            #if (col < 2 and Vmax > 35.) or (col == 0 and (Vmax < 27. and Vmax > 21.)) or (col==1 and Vmax<13.):
                #plt.plot(data['Vvec'][maxs], data['Pvec'][maxs], colores[maxCol], mfc='none')
    #plt.plot(data['Vvec'],data['Pvec'])
    
    
    #indV1 = data['Vvec']>20.
    #V1m = np.max(data['Vvec'][indV1])
    #P1m = np.max(data['Vvec'][indV1])
    dataset.append([Vmax, Pmax])

dataset = np.array(dataset)
dataset = np.block([spc_mat, MaxInd, dataset, localMaxV, localMaxP])
np.savetxt("dataset.csv", dataset, delimiter=",")

plt.xlim([0,450]) #10-13,21-27,35-45
plt.xlabel("Voltage [V]")
plt.ylabel("Power [W]")
#plt.savefig('AllCurves.pdf')
plt.show()
