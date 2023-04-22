# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:03:24 2023

@author: Iván Villegas Pérez

This Python script defines four functions: median_filter, best_fit_func, best_fit
and discard_variability.

The median_filter function applies a median filter of a given window size to a
flux array. It takes three parameters: time (an array of time values), flux (an
array of flux values), and window_size (the size of the window used for the
median filter). The function returns an array of filtered flux values. The
function also generates two plots: one of the original and filtered flux data
and one of the filtered flux data.

The best_fit_func function models the light curve of a star with a transit and
a sinusoidal signal. It takes eight parameters: x (an array of time values for 
the light curve), a (the amplitude of the sinusoidal signal), b (the period of
the sinusoidal signal), c (the phase of the sinusoidal signal), d (the offset of
the sinusoidal signal), t0 (the time of the center of the transit), p (the
period of the transit), dur (the duration of the transit), and dep (the depth of
the transit). The function returns an array of the modeled light curve.

The best_fit function fits a set of data (x,y) to a user-defined function using
the curve_fit function from scipy.optimize. It takes two parameters: x (an array
of independent variable values, i.e., time) and y (an array of dependent variable
values, i.e., flux). The function returns the parameters of the best fit. The
function also generates a plot of the filtered flux data and its best fit.

The discard_variability function subtracts the variability of the light curve
from the flux values. It also prints the transit parameters. The function takes
three parameters: time (an array of time values), flux (an array of flux values)
and params (an array of variability and transit parameters). The function returns
an array of flux values with the variability subtracted. The function also
generates a plot of the filtered flux data without the stellar variability.
"""

# Do all the imports
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc

def median_filter(time: np.array(float), flux: np.array(float),\
                  window_size: int) -> np.array(float):

    """
    Applies a median filter of a given window size to a flux array.

    Parameters:
    - time (1D array): Array of time values.
    - flux (1D array):  Array of flux values.
    - window_size (int): Size of the window used for the median filter.

    Returns:
    - filtered_flux (np.array(float)): Array of filtered flux values.

    Plots:
    Generates a plot of the original flux data and the filtered flux data.
    The plot is saved in 'Plots' as 'Flux Comparison.png'
    Generates a plot of the filtered flux data.
    The plot is saved in 'Plots' as 'Filtered Flux.png'
    """

    # Apply median filter to flux array
    filtered_flux: np.array(float)
    filtered_flux = sc.signal.medfilt(flux, kernel_size=window_size)

    # Plot the filtered and unfiltered flux
    plt.figure()
    plt.plot(time, flux, marker='.', label='Original data', ls='none')
    plt.plot(time, filtered_flux, marker='.', label='Filtered data', ls='none')
    plt.xlabel('Time (days)')
    plt.ylabel('Flux')
    plt.title('Flux comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('../Plots/Flux Comparison.png')
    
    # Plot the filtered flux data
    plt.figure()
    plt.plot(time, filtered_flux, marker='.')
    plt.xlabel('Time (days)')
    plt.ylabel('Flux')
    plt.title('Filtered flux')
    plt.grid(True)
    plt.savefig('../Plots/Filtered Flux.png')

    return filtered_flux

def best_fit_func(x, a, b, c, d, t0, p, dur, dep, m):
    """
    A function that models the light curve of a star with a transit and a
    sinusoidal signal.

    Parameters:
    - x (1D array): The array of time values for the light curve.
    - a (float): The amplitude of the sinusoidal signal.
    - b (float): The period of the sinusoidal signal.
    - c (float): The phase of the sinusoidal signal.
    - d (float): The offset of the sinusoidal signal.
    - t0 (float): The time of the center of the transit.
    - p (float): The period of the transit.
    - dur (float): The duration of the transit.
    - dep (float): The depth of the transit.
    
    Returns:
    - f (1D array): The modeled light curve.
    """

    # Calculate the phase of the transit
    phase: np.array(float) = ((x - t0 + 0.5*p) % p) - 0.5*p
    
    # Calculate the depth of the transit as a function of phase
    f: np.array(float) = dep * (1 - 4 * phase**2 / dur**2)
    
    # Loop over each data point and apply the transit model to the sinusoidal model
    for i in range(len(f)):
        
        if f[i]<0:
            
            # If the transit depth is negative, return only the sinusoidal
            # signal
            return a*np.sin(x/b+c)+d
            
        else:
            
            # If the transit depth is positive, add the transit model to the
            # sinusoidal model
            return a*np.sin(x/b+c)+d-dep*(1-4*((x-t0+0.5*p)%p)-0.5*p**2/dur**2)


def best_fit(x, y):
    """
    A function that fits a set of data (x,y) to a user-defined function using
    the curve_fit function from scipy.optimize.
    
    Parameters:
    - x (1D array): Independent variable values (time).
    - y (1D array): Dependent variable values (flux).
    
    Returns:
    - popt (1D array): The parameters of the best fit.
    
    Uses:
    - best_fit_func()
    
    Plots:
    Generates a plot of the filtered flux data and its best fit.
    The plot is saved in 'Plots' as 'Best Fit.png'
    """
    
    # Use curve_fit to find the best fit
    popt, pcov = sc.optimize.curve_fit(best_fit_func, x, y)

    # Plot data and its best fit
    plt.figure()
    plt.plot(x, y, 'o', label='Data')
    plt.plot(x, best_fit_func(x, *popt), label='Best fit')
    plt.legend()
    plt.grid(True)
    plt.savefig('../Plots/Best Fit.png')
    
    return popt

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
    The plot is saved in 'Plots' as 'Discarded Variability.png'
    """
    
    # Variability amplitude
    A: float = params[0]
    
    # Variability period
    P_v: float = params[1]
    
    # Variability phase
    Phase_v: float = params[2]
    
    # Variability offset
    Offset_v: float = params[3]
    
    # Print planet's period
    print(f"\nThe planet period is {params[5]} days.")
    
    # Print planet's half-time transit
    print(f"The planet half-time transit is {params[4]} days.")
    
    # Print planet's transit duration
    print(f"The planet's transit duration is {params[6]} days.")
    
    # Print planet's transit depth
    print(f"The planet's transit depth is {params[7]}.")
    
    # Compute the variability
    variability: np.array(float)
    variability = A*np.sin(time/P_v+Phase_v)+Offset_v
    
    # Compute the flux values with the variability subtracted
    flux_nv: np.array(float)
    flux_nv = flux-variability
    
    # Plot the star's light curve without variability
    plt.figure()
    plt.plot(time, flux_nv, marker='.')
    plt.xlabel('Time (days)')
    plt.ylabel('Flux')
    plt.title("Star's light curve w/o stellar varibility")
    plt.grid(True)
    plt.savefig('../Plots/Discarded Variability.png')
    
    # Return the flux values with the variability subtracted
    return flux_nv
