# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:03:24 2023

@author: Iván Villegas Pérez

This Python script defines six functions: median_filter, best_fit_func,
best_fit, get_period, time_convert and characterization.

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

The get_period function calculates the period of a periodic signal in the input
flux data. It first calculates the periodogram using the SciPy signal processing
library's periodogram function. Then, it finds the frequency with the highest
power (i.e. the dominant frequency) and calculates the period corresponding to
that frequency. Finally, it plots the periodogram and saves the plot as
'Periodogram.pdf' in the 'Plots' folder.

The time_convert function takes a single argument, seconds, which is the total
number of seconds to be converted into days, hours, minutes, and seconds. The
function first computes the complete number of days by dividing the total number
of seconds by the number of seconds in a day, which is 246060. It then computes
the remaining number of seconds that cannot be expressed as complete days by
using the operator '%'. It does the same operation until it the reamining time
can only be expressed as seconds.

The characterization function characterizes an exoplanet based on its light
curve, taking into account the stellar variability. The function then uses
get_period to obtain the period of the planet's orbit. It prompts the user for
the star's radius and mass to compute the planet's radius and distance from the
star, respectively. It also calculates the orbital inclination of the planet.
The function does not return anything; it only prints the computed results.

The functions use various modules such as numpy, matplotlib, and scipy. In
summary, these functions can be used to process and analyze data from a star's
light curve, including smoothing out noise, fitting the data to a user-defined
function, and calculating the period of a periodic signal in the data.
"""

# Do all the imports
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc

def median_filter(time: np.array(float), flux: np.array(float),\
                  window_size: int):

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
    The plot is saved in 'Plots' as 'Flux Comparison.pdf'
    Generates a plot of the filtered flux data.
    The plot is saved in 'Plots' as 'Filtered Flux.pdf'
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
    plt.savefig('../Plots/Flux Comparison.pdf')
    
    # Plot the filtered flux data
    plt.figure()
    plt.plot(time, filtered_flux, marker='.')
    plt.xlabel('Time (days)')
    plt.ylabel('Flux')
    plt.title('Filtered flux')
    plt.grid(True)
    plt.savefig('../Plots/Filtered Flux.pdf')

    return filtered_flux

def best_fit_func(x, a, b, c, d):#, t0, p, dur, dep, m):
    """
    A function that models the light curve of a star with a transit and a
    sinusoidal signal.

    Parameters:
    - x (1D array): The array of time values for the light curve.
    - a (float): The amplitude of the sinusoidal signal.
    - b (float): The period of the sinusoidal signal.
    - c (float): The phase of the sinusoidal signal.
    - d (float): The offset of the stellar flux.
    
    Returns:
    - f (1D array): The modeled light curve.
    """
   
    return a*np.sin(2*np.pi*x/b+c*np.pi)+d

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
    The plot is saved in 'Plots' as 'Best Fit.pdf'.
    """
    
    # Use curve_fit to find the best fit
    popt, pcov = sc.optimize.curve_fit(best_fit_func, x, y,\
                                       p0=np.array([2, 7, 1, 0]))

    # Plot data and its best fit
    plt.figure()
    plt.plot(x, y, 'o', label='Data')
    plt.plot(x, best_fit_func(x, *popt), label='Best fit')
    plt.xlabel('Time (days)')
    plt.ylabel('Flux')
    plt.title("Star's light curve w/ best fit for stellar varibility")
    plt.legend()
    plt.grid(True)
    plt.savefig('../Plots/Best Fit.pdf')
    
    return popt

def get_period(flux, sampling_f):
    """
    Calculates the period of a periodic signal in the input flux data. It first
    calculates the periodogram using the SciPy signal processing library's
    periodogram function. Then, it finds the frequency with the highest power
    (i.e. the dominant frequency) and calculates the period corresponding to
    that frequency. Finally, it plots the periodogram and saves the plot as
    'Periodogram.pdf' in the 'Plots' folder.

    Parameters:
    - flux (1D array): Flux values.
    - sampling_f (float): Sampling frequency.

    Returns:
    - period (float): The period of the periodic signal in the flux data.

    Plots:
    Generates a plot of the power spectrum. The plot is saved in 'Plots' as
    'Periodogram.pdf'.
    """
    
    # Calculate the periodogram
    frequencies, power_spectrum = sc.signal.periodogram(flux, sampling_f)
    
    # Plot the periodogram
    plt.figure()
    plt.plot(frequencies, power_spectrum)
    plt.grid(True)
    plt.xlabel(r'Frequency [days$^{-1}$]')
    plt.ylabel('Power Spectrum')
    plt.title('Periodogram')
    plt.savefig('../Plots/Periodogram.pdf')
    
    # Find the frequency with the highest power (i.e. the dominant frequency)
    dominant_frequency = frequencies[np.argmax(power_spectrum)]
    
    # Calculate the period corresponding to the dominant frequency
    period = 1/dominant_frequency
    
    return period

def characterization(time, flux):
    
    """
    This function characterizes an exoplanet based on its light curve, taking
    into account the stellar variability.

    Parameters:
    - time (1D array): Time array of the light curve.
    - flux (1D array): Flux array of the light curve.

    Returns:
    - None
    
    Uses:   
    - get_period():
    """
    
    period: float = get_period(flux, 1/(time[1]-time[0]))

    # Computes the planet's radius using transits's law
    stellar_radius: float
    stellar_radius = float(input(r"Star's radius (R☉): "))
    transit_depth: float = (np.max(flux) - np.min(flux))/np.mean(flux)
    planet_radius: float = np.sqrt(transit_depth)*stellar_radius*6.957e5/6371
    
    # Computes the planet-star distance using Kepler's law
    G = 6.67430e-11 # Gravitational constant
    M_star: float
    M_star = float(input(r"Star's mass (M☉): "))
    a = ((period*24*60*60/(2*np.pi))**2*G*M_star)**(1/3)
    distance_to_star = a*149.6e6 # Distance in km
    
    # Orbital inclination determination
    inclination = np.arccos(np.sqrt(abs(np.max(flux)+np.min(flux))/\
                                    (2*np.mean(flux))))/np.pi    
    if str(inclination)=='nan':
        
        inclination = 0.5
    
    # Computes the planet's temperature
    stellar_temp: float
    stellar_temp = float(input(r"Star's temperature (K): "))
    planet_temp = stellar_temp*np.sqrt(stellar_radius*6.957e5/\
                                       (2*distance_to_star))
    
    # Print results
    print(f'\nPeriod: {period:.2f} days.')
    print(f"Planet's radius: {planet_radius:.2f} R🜨.")
    print(f'Planet-Star distance: {distance_to_star:.2f} km.')
    print(f'Orbit inclination: {inclination:.2f}π rad.')
    print(f"Planet's temperature: {planet_temp:.2f} K.")
