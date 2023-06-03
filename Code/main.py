# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 12:06:59 2023

@author: Iván Villegas Pérez

This Python script defines a main function that serves as the entry point for
the program. It imports three other modules: numpy, simulate, read, analize and
remove.

The program starts by prompting the user to choose whether to simulate or read
real data. If the user chooses to simulate, it calls the simulate.data_maker()
function to generate a time array and a flux array for the star's light curve.
If the user chooses to read real data, it prompts the user to enter the name of
the file containing the data and then calls the read.read_data() function to
read the data from the file.

The program then applies a median filter to the flux data using the
analize.median_filter() function, which takes as input the time and flux arrays
and the size of the filter window.

Next, it fits the filtered flux data to a curve using the analize.best_fit()
function, which returns an array of the best-fit parameters.

Finally, it discards the variability from the star's light curve using the
remove.discard_variability() function, which takes as input the time array, the
filtered flux array, and the best-fit parameters, and returns a new flux array
that represents the transit without the stellar variability.
"""

# Do all the imports
import numpy as np
import simulate
import read
import analize
import remove
import effectivity

def main():
    """
    Executes the main program for filtering and analyzing star's light curve.
    
    · It offers the posibility of checking how effective the proposed method is.
    
    · It calls the 'data_maker' function to generate simulated data or the
      'read_data' function to read real data depending if the user want to analize
      simulated or real data. It prompts the user to enter a window size for the
      median filter (using the 'median_filter' function), and then applies the
      filter to the simulated data. It finds the best parameters fitting the
      plottered curve and computes the transit without the stellar variability
      (printing the values of the transit main parameters).

    Parameters:
    - None

    Returns:
    - None
    
    Uses:
    - data_maker() from simulate.py
    - read_data() from read.py
    - median_filter() from analize.py
    - best_fit() from analize.py
    - discard_variability() from remove.py
    - get_effectivity() from effectivity.py
    """
    
    option: str
    option = input('Do you want to check how effective the method is? (Y or N): ')
    
    # Make sure the user chooses a valid option
    while option != 'Y' and option != 'N':
        
        print('')
        print('Thats not an option. Please enter a valid option (Y or N).')
        option = input("Do you want to check how effective the method is? (Y or N): ")
    
    if option == 'Y':
        
        print('This will take arround 18 hours.')
        
        option: str
        option = input('Do you want to ocntinue? (Y or N): ')
        
        if option=='Y':

            effectivity.get_effectivity()
    
    # Define the time and flux arrays for data_maker()
    time: np.array(float)
    flux: np.array(float)
    
    # Ask to know i fthe program has to simulate or read the data
    option: str
    option = input("Do you want to simulate (S) or to read (R) real data? ")
    
    # Make sure the user chooses a valid option
    while option != 'S' and option != 'R':
        
        print('')
        print('Thats not an option. Please enter a valid option (S or R).')
        option = input("Do you want to simulate (S) or to use real (R) data? ")
    
    if option == 'S':

        # Generate the time and flux data for the star's light curve
        time, flux = simulate.data_maker()
        
    else:
        
        # Ask for the file name
        file: str
        file = input("Which file dou you want to read? ")
        
        # Read the time and flux data for the star's light curve
        time, flux = read.read_data(f'../Data/{file}')
        
    # Apply a median filter to the flux data
    filtered_flux: np.array(float)
    window_size: int = int(input('Window size for the median filter (~101): '))
    filtered_flux = analize.median_filter(time, flux, window_size)
    
    # Fit the filtered flux data to a curve
    best_fit_params: np.array(float)
    best_fit_params = analize.best_fit(time, filtered_flux)
    
    # Discard the variability from the star's light curve
    flux_nv: np.array(float)
    flux_nv = remove.discard_variability(time, filtered_flux, best_fit_params)
    
    period: float = analize.get_period(flux_nv, 1/(time[1]-time[0]))
    
    analize.characterization(time, flux, period)
