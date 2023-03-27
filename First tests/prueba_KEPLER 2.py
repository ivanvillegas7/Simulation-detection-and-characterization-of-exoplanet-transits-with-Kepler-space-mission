# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 19:07:04 2023

@author: Iván Villegas Pérez
"""

'''

This program is a test on how to read KEPLER satelletite data.

'''

import numpy as np

from typing import List

import matplotlib.pyplot as plt

j: int = 0

time: List[float] = []

cadence: List[int] = []

init_flux : List[float] = []

init_flux_err : List[float] = []

model: List[float] = []

residual_flux : List[float] = []

residual_flux_err : List[float] = []

rest_dm: List[float] = []

rest_dr: List[float] = []

rest: List[float] = []

with open("kplr000757450_q1_q16_tce_01_dvt_lc.tbl", "r") as infile:
    
    lines = infile.readlines()
    
    #Read the data.
    
    for line in lines:
        
        vals = line.split()
        
        if j <= 34:
            
            if j == 8:
                
                print('')
                
                print(f'This planet/star corresponds to (KEPLER ID): {vals[2]}\n')
            
            j+=1
            
        else:
            
            time.append(float(vals[0]))
            
            cadence.append(int(vals[1]))
            
            init_flux.append(float(vals[2]))
            
            init_flux_err.append(float(vals[3]))
            
            model.append(float(vals[4]))
            
            residual_flux.append(float(vals[5]))
            
            residual_flux_err.append(float(vals[6]))
            
            rest_dm.append(float(vals[2])-float(vals[4]))
            
            rest_dr.append(float(vals[2])-float(vals[5]))
            
            rest.append(float(vals[2])-float(vals[4])-float(vals[5]))
            
suma_xy = 0

suma_x = 0

suma_y = 0

suma_xx = 0

n: int = 0

for i in range(0, len(time)):
    
    if str(init_flux[i]) != "nan":
    
        suma_xy = suma_xy + time[i]*init_flux[i]
        
        suma_x = suma_x + time[i]
        
        suma_y = suma_y + init_flux[i]
        
        suma_xx = suma_xx + time[i]**2
        
        n+=1
        
a = (n*suma_xy-suma_x*suma_y)/(n*suma_xx-suma_x**2)

b = (suma_y-a*suma_x)/n

suma_sigma: float = 0

for i in range(0, len(time)):
    
    if str(init_flux[i]) != "nan":
    
        suma_sigma = suma_sigma+(init_flux[i]-a*time[i]-b)**2

sigma: float =  np.sqrt(suma_sigma/(n-2))

err_a: float = np.sqrt(n)*sigma/np.sqrt(n*suma_xx-suma_x**2)

err_b: float = err_a*np.sqrt(suma_xx/n)

flux: List[float] = []

time_f: List[float] = []

f: List[float] = []

delta_f: List[float] = []

for i in range(0, len(init_flux)):
    
    f.append(a*time[i]+b)
    
    delta_f.append(np.sqrt((time[i]*err_a)**2+err_b**2))
    
    #if init_flux[i]<=(b+400*err_b) and init_flux[i]>=(b-400*err_b):
        
    if init_flux[i]<=(f[i]+200*delta_f[i]) and init_flux[i]>=(f[i]-200*delta_f[i]):
        
        flux.append(init_flux[i])
        
        time_f.append(time[i])


plt.figure()

plt.plot(time_f, flux, marker='.', label='Observed (filtered) data', color='red', ls='none')
  
plt.xlabel(r'$t$ [s]')

plt.ylabel(r'$\phi$ [lm]')

plt.title('Flux vs time')

plt.grid(True)

plt.legend()

#plt.ylim(-0.025, 0.010)

plt.savefig('filtered_test.pdf')

#%%
    
plt.figure()

plt.plot(time, model, marker='.', label='Model data', color='blue', ls='none')
  
plt.xlabel(r'$t$ [s]')

plt.ylabel(r'$\phi$ [lm]')

plt.title('Flux vs time')

plt.grid(True)

plt.legend()

plt.savefig('model_test.pdf')

#%%

plt.figure()

plt.plot(time, init_flux, marker='.', label='Observed data', color='red', ls='none')
'''
for i in range(0, len(time)):
    
    plt.vlines(time[i], init_flux[i]-init_flux_err[i], init_flux[i]+init_flux_err[i], color='red')
'''        
plt.xlabel(r'$t$ [s]')

plt.ylabel(r'$\phi$ [lm]')

plt.title('Flux vs time')

plt.grid(True)

plt.legend()
'''
plt.xlim(875, 895)

plt.ylim(-0.025, 0.0010)
'''
plt.savefig('data_test.pdf')

#%%

plt.figure()

plt.plot(time, residual_flux, marker='.', label='Residual data', color='black', ls='none')
'''
for i in range(0, len(time)):

    plt.vlines(time[i], residual_flux[i]-residual_flux_err[i], residual_flux[i]+residual_flux_err[i], color='black')
'''
plt.xlabel(r'$t$ [s]')

plt.ylabel(r'$\phi$ [lm]')

plt.title('Flux vs time')

plt.grid(True)

plt.legend()

plt.savefig('residual_test.pdf')

#%%

plt.figure()

plt.plot(time, init_flux, marker='.', label='Observed data', color='red', ls='none')

plt.plot(time, model, marker='.', label='Model data', color='blue', ls='none')

plt.plot(time, residual_flux, marker='.', label='Residual data', color='black', ls='none')
'''
for i in range(0, len(time)):
    
    plt.vlines(time[i], init_flux[i]-init_flux_err[i], init_flux[i]+init_flux_err[i], color='red')
    
    plt.vlines(time[i], residual_flux[i]-residual_flux_err[i], residual_flux[i]+residual_flux_err[i], color='black')
'''  
plt.xlabel(r'$t$ [s]')

plt.ylabel(r'$\phi$ [lm]')

plt.title('Flux vs time')

plt.grid(True)

plt.legend()

plt.savefig('all_test.pdf')

#%%

plt.figure()

plt.plot(time, rest_dm, label='Observed data - Model data', color='green')
'''
for i in range(0, len(time)):
    
    plt.vlines(time[i], init_flux[i]-init_flux_err[i], init_flux[i]+init_flux_err[i], color='red')
'''
plt.xlabel(r'$t$ [s]')

plt.ylabel(r'$\phi$ [lm]')

plt.title('Flux vs time')

plt.grid(True)

plt.legend()

plt.savefig('rest_dm_test.pdf')

#%%

plt.figure()

plt.plot(time, rest_dr, label='Observed data - Residual data', color='purple')
'''
for i in range(0, len(time)):
    
    plt.vlines(time[i], init_flux[i]-init_flux_err[i], init_flux[i]+init_flux_err[i], color='red')
    
    plt.vlines(time[i], residual_flux[i]-residual_flux_err[i], residual_flux[i]+residual_flux_err[i], color='black')
'''
plt.xlabel(r'$t$ [s]')

plt.ylabel(r'$\phi$ [lm]')

plt.title('Flux vs time')

plt.grid(True)

plt.legend()

plt.savefig('rest_dr_test.pdf')

#%%

plt.figure()

plt.plot(time, rest, label='Observed data - Model data - Residual data', color='orange')
'''
for i in range(0, len(time)):
    
    plt.vlines(time[i], init_flux[i]-init_flux_err[i], init_flux[i]+init_flux_err[i], color='red')
    
    plt.vlines(time[i], residual_flux[i]-residual_flux_err[i], residual_flux[i]+residual_flux_err[i], color='black')
'''
plt.xlabel(r'$t$ [s]')

plt.ylabel(r'$\phi$ [lm]')

plt.title('Flux vs time')

plt.grid(True)

plt.legend()

plt.savefig('rest_test.pdf')
