# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 17:21:07 2023

@author: Iván
"""

from typing import List

import matplotlib.pyplot as plt

def plot_data(x: List[float], y: List[float], star: str):
    
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
    
    plt.plot(x, y, marker='.', label=f'{star} un-normlaised data', ls='none')
      
    plt.xlabel(r'$t$ [days]')
    
    plt.ylabel(r'$\phi$ [e$^-$/s]')
    
    plt.title(f'Un-normalised flux vs time for {star}')
    
    plt.grid(True)
    
    plt.legend()
    
    plt.savefig(f'../Plots/un-normalised {star}.jpg')

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
    
    plt.ylabel(r'$\phi_{norm}$ [e$^-$/s]')
    
    plt.title(f'Normalised flux vs time for {star}')
    
    plt.grid(True)
    
    plt.legend()
    
    plt.savefig(f'../Plots/normlaised {star}.jpg')
