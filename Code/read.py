# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:29:00 2023

@author: Iván Villegas Pérez

This Python script defines a function called read_data which reads time and flux
data from a file. It also plots the light's curve of the star.
"""
# Do all the imports
import numpy as np
import matplotlib.pyplot as plt

def read_data(file):
    """
    Reads time and flux data from a file.
    
    Parameters:
    - file (str): The name of the file containing the data.
    
    Returns:
    - time (1D array): Time data
    - time (1D array): Flux data.
    
    Plots:
    Generates a plot of the read transit flux data.
    The plot is saved in 'Plots' as 'Read Transit.pdf'
    """
    
    # Read the data from the file
    data = np.loadtxt(file, skiprows=3)
    
    # Assign the data
    time: np.array(float) = data[:, 1] 
    flux: np.array(float) = data[:, 2]
    
    # Plot read flux
    plt.figure()
    plt.plot(time, flux, marker='.', ls='none')
    plt.xlabel('Time (days)')
    plt.ylabel('Signal (a.u.)')
    plt.title('Read Flux')
    plt.grid(True)
    plt.savefig('../Plots/Total Flux.pdf')
    
    # Return the time and flux values
    return(time, flux)
