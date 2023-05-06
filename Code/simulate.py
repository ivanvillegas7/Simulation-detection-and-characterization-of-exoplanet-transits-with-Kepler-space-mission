# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 13:00:23 2023

@author: Iván Villegas Pérez

This Pyhton script simulates a transit light curve with sinusoidal variability
and noise. The user is prompted to input the transit period, phase, and duration,
as well as the amplitude, period, phase, and offset of the sinusoidal variability.
The code generates a simulated transit using the input transit parameters and
generates a sinusoidal variability using the input variability parameters. The
code then generates noise using a Gaussian and noncentral Student's t
distribution with user-specified parameters. The final light curve is obtained
by adding the transit, variability, and noise together.

The sinusoidal_variability function generates a sinusoidal variability given the
amplitude, period and phase of the variability, and the stellar flux offset.
The function returns an array of flux values corresponding to the input time
values.

The generate_parabolic_transit function generates a parabolic transit signal
that repeats every period. The parabolic transit is specified by the transit
period, time of the center of the transit, duration of the transit, and depth
of the transit. The function returns an array of flux values corresponding to
the input time values.

The sim_flux function prompts the user to input the transit period, phase, and
duration, as well as the amplitude, period, phase, and offset of the sinusoidal
variability. The function then generates a simulated transit using the
simulate_transit function and generates a sinusoidal variability using the
sinusoidal_variability function. The function generates noise using a Gaussian
and noncentral Student's t distribution with user-specified parameters. The
final light curve is obtained by adding the transit, variability, and noise
together. The function returns an array of time values and an array of simulated
flux values. The function also generates a plot of the simulated transit flux
data and a plot of the simulated flux data.

The discard_planet function was developed by Jacob Robnik and Uroš Seljak,
published at their article 'Kepler Data Analysis: Non-Gaussian Noise and Fourier
Gaussian Process Analysis of Stellar Variability' and shared in their GitHub
repository (https://github.com/JakobRobnik/Kepler-Data-Analysis) in code named
'noise.py'.
"""

# Do all the imports
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
from typing import List

"""
Function 'simulate_noise' was developed by Jakkob Robnik and Uroš Seljak. This
function has been copy-pasted from their shared code.
"""

def simulate_noise(N, params):
    """Generates noise signal according to our noise distribution = Gauss + noncentral Student`s t
    N = number of realizations
    params =[A, df, nc, loc, scale] see: https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.stats.nct.html
    """
    N_outliers = int(params[0]*N) #number of outliers

    Gaussian = np.random.normal(loc = 0.0, scale = 1.0, size= N - N_outliers)

    outliers = sc.stats.nct.rvs(*params[1:], size=N_outliers)

    fluxi = np.concatenate([Gaussian, outliers])

    np.random.shuffle(fluxi)

    return fluxi

def sinusoidal_variability(time, amplitude, period, phase, offset):
    """
    Defines the sinusoidal variability of a star.

    Parameters:
    - time (np.array(float)): Array of time values.
    - amplitude (float): Amplitude of the variability.
    - period (float): Period of the variability (in days).
    - phase (float): Phase of the variability (in radians).
    - offset (float): Offset of the stellar flux.

    Returns:
    - flux (1D array): Array of flux values corresponding to the input
                       time values.
    """

    flux: np.array(float)

    flux = amplitude*np.sin(2*np.pi/period*time+phase)+offset

    return flux

def generate_parabolic_transit(period, t0, duration, depth, t):
    """
    Generates a parabolic transit signal that repeats every period.

    Parameters:
    - period (float): Period of the transit signal.
    - t0 (float): Time of the center of the transit.
    - duration (float): Duration of the transit.
    - depth (float): Depth of the transit (relative flux drop).
    - t (numpy array): Array of times where the signal will be generated.

    Returns:
    - 1D array: Array of flux values corresponding to the parabolic transit
                   signal.
    """
    
    phase: np.array(float) = ((t-t0+0.5*period)%period)-0.5*period
    
    f: np.array(float) = depth*(1-4*phase**2/duration**2)
    
    f[f<0] = 0
    
    return -f

def sim_flux(noise_params):
    """
    Simulates a transit light curve with sinusoidal variability and noise.

    Parameters:
    - noise_params (List[float]): list of parameters for noise generation.
        noise_params[0]: fraction of outliers in the data.
        noise_params[1]: degrees of freedom for non-central Student's t
                         distribution.
        noise_params[2]: non-central parameter for non-central Student's t
                         distribution.
        noise_params[3]: mean value for non-central Student's t distribution.
        noise_params[4]: scale parameter for non-central Student's t
                         distribution.

    Returns:
    - time (1D array): array of time values.
    - flux (1D array): array of simulated flux values.

    Plots:
    Generates a plot of the simulated transit flux data.
    The plot is saved in 'Plots' as 'Simulated Transit.png'
    Generates a plot of the simulated flux data.
    The plot is saved in 'Plots' as 'Simulated Flux.png'
            
    Uses:
    - generate_parabolic_transit()
    - sinusoidal_variability()
    - simulate_noise()
    """

    t_period: float = float(input('Transit period: '))
    t_duration: float = float(input('Transit duration: '))
    t0: float = float(input('Transit half time: '))
    depth: float = float(input('Transit depth: '))
    t_start: float = float(input('Initial time: '))
    t_end: float = float(input('Ending time: '))

    time: np.array(float) = np.linspace(t_start, t_end, 100000)

    # Generate transit model
    flux_p: np.array(float)
    flux_p = generate_parabolic_transit(t_period, t0, t_duration, depth, time)

    # Plot transit model
    plt.figure()
    plt.plot(time, flux_p, marker='.')
    plt.xlabel('Time (days)')
    plt.ylabel('Flux')
    plt.title('Simulated Transit')
    plt.grid(True)
    plt.savefig('../Plots/Simulated Transit.png')

    # Generate sinusoidal variability
    amplitude: float = float(input('Sinusoidal variability amplitude: '))#2
    period: float = float(input('Sinusoidal variability period: '))#7
    phase: float = float(input('Sinusoidal variability phase (in units of π): '))
    offset: float = float(input('Stellar flux offset (order of magnitude): '))

    variability: np.array(float)
    variability = sinusoidal_variability(time, amplitude, period, phase*np.pi,\
                                         offset)

    # Simulate noise
    noise: np.array(float)
    noise = simulate_noise(len(flux_p), noise_params)

    # Combine flux with variability and noise
    flux: np.array(float)
    flux = flux_p + variability + noise

    # Plot simulated flux
    plt.figure()
    plt.plot(time, flux, marker='.', ls='none')
    plt.xlabel('Time (days)')
    plt.ylabel('Flux')
    plt.title('Simulated Flux')
    plt.grid(True)
    plt.savefig('../Plots/Total Flux.png')

    return(time, flux)


def data_maker():
    """
    Generates simulated time series data with a non-central Student's
    t-distribution and an added outlier fraction.

    Arguments:
    
    - A (float): outlier fraction.
    - df (float): degrees of freedom for non-central Student's t-distribution.
    - nc (float): non-central parameter.
    - loc (float): mean value of non-central Student's t-distribution.
    - scale (float): scale of non-central Student's t-distribution.

    Returns:
    
    - time (1D array): array of time values.
    - flux (1D array): array of simulated flux values.

    Uses:
    
    - sim_flux()
    """

    A: float
    A = float(input('Outlier fraction: '))

    df: float  
    df = float(input("Non-central Student's t distribution degrees of freedom: "))
    
    nc: float
    nc = float(input("Non-central paarameter: "))

    loc: float
    loc = float(input("Non-central Student's t distribution mean value: "))

    scale: float
    scale = float(input("Non-central Student's t distribution scale: "))

    params: List[float]
    params = [A, df, nc, loc, scale]
    
    time: np.array(float)
    flux: np.array(float)
    time, flux = sim_flux(params)

    return(time, flux)
