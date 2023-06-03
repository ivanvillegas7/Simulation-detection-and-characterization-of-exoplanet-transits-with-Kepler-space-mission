# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 20:13:37 2023

@author: Iván Villegas Pérez

This script is part of a pipeline for analyzing transit light curves of
exoplanets which are obtained by measuring the brightness of a star over time as
a planet passes in front of it. The code consists of one function:
discard_variability().

The discard_variability function takes as input the time values time, the flux
values flux and an array params that contains the variability and transit
parameters. It subtracts the stellar variability from the flux values and
returns the resulting flux values. The parameters in params are as follows:

    ·params[0]: variability amplitude A
    ·params[1]: variability period P_v
    ·params[2]: variability phase Phase_v (in units of pi)
    ·params[3]: variability offset Offset_v
    
The function computes the variability of the star using a sinusoidal model with
the specified parameters, and subtracts it from the flux values to obtain the
flux values with the variability removed. It then generates a plot of the
filtered flux data without the stellar variability.
"""

# Do all the imports
import numpy as np
import matplotlib.pyplot as plt

def discard_variability(time, flux, params):
    """
    Subtracts the variability of the light curve from the flux values.
    It also prints the transit parameters.

    Parameters:
    - time (1D array): Time values.
    - flux (1D array): Flux values.
    - params (1D array): Variability and transit parameters.

    Returns:
    - flux_nv (1D array): Flux values with the variability subtracted.
    
    Plots:
    Generates a plot of the filtered flux data w/o the stellar variability.
    The plot is saved in 'Plots' as 'Discarded Variability.pdf'
    """
    
    # Variability amplitude
    A: float = params[0]
    
    # Variability period
    P_v: float = params[1]
    
    # Variability phase
    Phase_v: float = params[2]
    
    # Compute the variability
    variability: np.array(float)
    variability = A*np.sin(2*np.pi*time/P_v+Phase_v*np.pi)
    
    # Compute the flux values with the variability subtracted
    flux_nv: np.array(float)
    flux_nv = flux-variability
    '''
    # Plot the star's cleaned light curve (without variability)
    plt.figure()
    plt.plot(time, flux_nv, marker='.')
    plt.xlabel('Time (days)')
    plt.ylabel('Signal (a.u.)')
    plt.title("Star's cleaned light curve (w/o stellar varibility)")
    plt.grid(True)
    plt.savefig('../Plots/Cleaned Light Curve.pdf')
    '''
    # Return the flux values with the variability subtracted
    return flux_nv
