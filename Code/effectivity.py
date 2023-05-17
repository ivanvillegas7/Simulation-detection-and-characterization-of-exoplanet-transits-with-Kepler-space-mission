# -*- coding: utf-8 -*-
"""
Created on Thu May 11 14:16:15 2023

@author: Iván
"""

import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from typing import List

import analize
import remove

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

def sim_flux(A:float, amplitude:float, period:float, phase:float, t_period:float):
    
    t_duration: float = 0.5
    t0: float = 0.25
    depth: float = 5
    t_start: float = 0
    t_end: float = 50

    time: np.array(float) = np.linspace(t_start, t_end, 100000)

    # Generate transit model
    flux_p: np.array(float)
    flux_p = generate_parabolic_transit(t_period, t0, t_duration, depth, time)
    
    # Simulate noise
    df: float  
    df = 3
    
    nc: float
    nc = 1

    loc: float
    loc = 0

    scale: float
    scale = 1

    params: List[float]
    
    params = [A, df, nc, loc, scale]
    
    noise: np.array(float)
    noise = simulate_noise(len(flux_p), params)

    # Generate sinusoidal variability
    offset: float = 500

    variability: np.array(float)
    variability = sinusoidal_variability(time, amplitude, period, phase*np.pi,\
                                         offset)

    # Combine flux with variability and noise
    flux: np.array(float)
    flux = flux_p + variability + noise

    return(time, flux)

def efficiency(i: int):
    
    if i==0:
        
        A: np.array(float) = np.linspace(0, 1, 100)
        
        amplitude: float = 2
        
        period: float = 7
        
        phase: float = 1
        
        t_period: float = 2.5*np.ones(100)
                
    elif i==1:
        
        A: float = 0.3
        
        amplitude: np.array(float) = np.linspace(0, 5, 100)
        
        period: float = 7
        
        phase: float = 1
        
        t_period: float = 2.5*np.ones(100)

    elif i==2:
        
        A: float = 0.3
        
        amplitude: float = 2
        
        period: np.array(float) = np.linspace(4, 9, 100)
        
        phase: float = 1
        
        t_period: float = 2.5*np.ones(100)
        
    elif i==3:
        
        A: float = 0.3
        
        amplitude: float = 2
        
        period: float = 7
        
        phase: np.array(float) = np.linspace(0, 2, 100)
        
        t_period: float = 2.5*np.ones(100)
        
    elif i==4:
        
        A: float = 0.3
        
        amplitude: float = 2
        
        period: float = 7
        
        phase: float = 1
        
        t_period: np.array(float) = np.linspace(0.01, 45, 100)
        
    err_mean: List[float] = []
    
    with open('datos.dat', 'w') as f:
        
        f.write('Amplitude  Relative Error')
        
        for j in range(100):
            
            err: List[float] = []
            
            for _ in range(100):
                
                time: np.array(float)
                flux: np.array(float)
                
                if i==0:
                
                    time, flux = sim_flux(A[j], amplitude, period, phase,\
                                          t_period[j])
                    
                elif i==1:
                
                    time, flux = sim_flux(A, amplitude[j], period, phase,\
                                          t_period[j])
                    
                elif i==2:
                
                    time, flux = sim_flux(A, amplitude, period[j], phase,\
                                          t_period[j])
                    
                elif i==3:
                
                    time, flux = sim_flux(A, amplitude, period, phase[j],\
                                          t_period[j])
                    
                elif i==4:
                
                    time, flux = sim_flux(A, amplitude, period, phase,\
                                          t_period[j])
                    
                filtered_flux: np.array(float)
                filtered_flux = analize.median_filter(time, flux, 101)
                
                best_fit_params: np.array(float)
                best_fit_params = analize.best_fit(time, filtered_flux)
                
                flux_nv: np.array(float)
                flux_nv = remove.discard_variability(time, filtered_flux,\
                                                     best_fit_params)
                
                result: float = analize.get_period(flux_nv, 1/(time[1]-time[0]))
                
                err.append(np.abs(t_period[j]-result)/t_period[j])
                
            f.write(f'\n{amplitude[j]} {err}')
                
            err_mean.append(np.mean(err))
            
        f.close()
        
    plt.figure()
    plt.ylabel('Relative error on the transit period determination')
    plt.grid(True)
    
    if i==0:
        
        plt.plot(A, err_mean, marker='.')
        plt.xlabel('Outlier fraction')
        plt.title('Relative error against outlier fraction')
        plt.savefig('../Plots/Efficiency/REvsOF.pdf')
        
    elif i==1:
        
        plt.plot(amplitude, err_mean, marker='.')
        plt.xlabel('Variability amplitude')
        plt.title('Relative error against variability amplitude')
        plt.savefig('../Plots/Efficiency/REvsVA.pdf')
        
    elif i==2:
    
        plt.plot(period, err_mean, marker='.')
        plt.xlabel('Variability period')
        plt.title('Relative error against variability period')
        plt.savefig('../Plots/Efficiency/REvsVP.pdf')
        
    elif i==3:
    
        plt.plot(phase, err_mean, marker='.')
        plt.xlabel('Variability phase')
        plt.title('Relative error against variability phase')
        plt.savefig('../Plots/Efficiency/REvsVPh.pdf')
        
    elif i==4:
    
        plt.plot(t_period, err_mean, marker='.')
        plt.xlabel('Transit period')
        plt.title('Relative error against transit period')
        plt.savefig('../Plots/Efficiency/REvsTP.pdf')
        
def get_efficiency():
    
    for i in range(5):
        
        efficiency(i)
