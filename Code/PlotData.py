# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 17:21:07 2023

@author: Iván
"""

from typing import List

import matplotlib.pyplot as plt

def plot(text: str):
    
    '''
    
    This function reads the data from a file and plot the data.
    
    Parameters:
        
        text: name of the file (w/o file extension)        
        
    Returns:
        
        none
    
    '''

    with open(f'{text}.tbl', "r") as infile:
        
        i: int = 0
        
        time: List[float] = []
    
        flux : List[float] = []
        
        lines = infile.readlines()
        
        #Reads the data.
        
        for line in lines:
            
            vals = line.split()
            
            if i < 3:
                
                i+=1
                
            else:
                
                time.append(float(vals[1]))
                
                flux.append(float(vals[2])*1e-3)
           
    #Plots the data

    plt.figure()
    
    plt.plot(time, flux, marker='.', label=f'{text} data', ls='none')
      
    plt.xlabel(r'$t$ [s]')
    
    plt.ylabel(r'$10^{-3}\phi$ [e$^-$/s]')
    
    plt.title(f'Flux vs time for {text}')
    
    plt.grid(True)
    
    plt.legend()
    
    #plt.savefig(f'{text}.pdf')

def plot_norm_data(x: List[float], y: List[float], star: str):
    
    '''
    
    This function plots the data you give.
    
    Parameters:
        
        x: x data
        
        y: y data
        
        star: name of the studied star
        
    Returns:
        
        none
    
    '''
    
    #Plots the data

    plt.figure()
    
    plt.plot(x, y, marker='.', label=f'{star} normlaised data', ls='none')
      
    plt.xlabel(r'$t$ [days]')
    
    plt.ylabel(r'$\phi_\text{norm}$ [e$^-$/s]')
    
    plt.title(f'Normalised flux vs time for {star}')
    
    plt.grid(True)
    
    plt.legend()
    
    #plt.savefig(f'normlaised {text}.pdf')

'''

print('')

text: str = input('Which exoplanet dou you want to plot (TrES2b, Kepler75b): ')

plot(text)

'''