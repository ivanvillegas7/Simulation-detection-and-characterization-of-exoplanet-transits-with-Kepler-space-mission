# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 19:07:04 2023

@author: Iván Villegas Pérez
"""

'''

This program is a test on how to read KEPLER satelletite data.

'''

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

#%%
    
plt.figure()

plt.plot(time, model, label='Model data', color='blue')
  
plt.xlabel(r'$t$ [s]')

plt.ylabel(r'$\phi$ [lm]')

plt.title('Flux vs time')

plt.grid(True)

plt.legend()

plt.savefig('model_test.pdf')

#%%

plt.figure()

plt.plot(time, init_flux, label='Observed data', color='red')

for i in range(0, len(time)):
    
    plt.vlines(time[i], init_flux[i]-init_flux_err[i], init_flux[i]+init_flux_err[i], color='red')
        
plt.xlabel(r'$t$ [s]')

plt.ylabel(r'$\phi$ [lm]')

plt.title('Flux vs time')

plt.grid(True)

plt.legend()

plt.savefig('data_test.pdf')

#%%

plt.figure()

plt.plot(time, residual_flux, label='Residual data', color='black')

for i in range(0, len(time)):

    plt.vlines(time[i], residual_flux[i]-residual_flux_err[i], residual_flux[i]+residual_flux_err[i], color='black')
   
plt.xlabel(r'$t$ [s]')

plt.ylabel(r'$\phi$ [lm]')

plt.title('Flux vs time')

plt.grid(True)

plt.legend()

plt.savefig('residual_test.pdf')

#%%

plt.figure()

plt.plot(time, init_flux, label='Observed data', color='red')

plt.plot(time, model, label='Model data', color='blue')

plt.plot(time, residual_flux, label='Residual data', color='black')

for i in range(0, len(time)):
    
    plt.vlines(time[i], init_flux[i]-init_flux_err[i], init_flux[i]+init_flux_err[i], color='red')
    
    plt.vlines(time[i], residual_flux[i]-residual_flux_err[i], residual_flux[i]+residual_flux_err[i], color='black')
  
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

#plt.savefig('rest_dm_test.pdf')

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