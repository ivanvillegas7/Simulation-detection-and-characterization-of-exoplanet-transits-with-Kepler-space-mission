# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 11:49:51 2023

@author: Iván Villegas Pérez

This code has been developed in a first attemp to apply a first filter,
normalise and plot the data downloaded from Nasa Exoplanet Archive for TrES-2 b
or Kepler-1 b (https://exoplanetarchive.ipac.caltech.edu/overview/K00001.01), in
a future, it will also contain data from Kepler-75 b. The downloaded data can
be found in the folder with the same name as the studied object, in the
short/long cadence folder with names Q#, which identifies the quarter of
observation (for different file of the same quarter, letters a, b and c denote
observation was earlier).

Run the main code and the whole project will be run. Once it is run, it will
ask the user to type the studied star. Since the only available data are from
TrES-2 b, the user must type 'TrES2b', otherwise, it will keep asking for the
object name.

"""

#Imports the code to read, normalise and appply the first filter

import ReadData as RD

#Imports the code to plot the data

import PlotData as PD

#Imports 'List'

from typing import List

def main(star: str, f_filter: bool):
    
    '''
    This is the main function of the program. For a given star, it calls the
    different functions, which reads, normalises and plot the data for that
    star.
    
    Parameters:
        
        star: name of the studied star
        
    Returns:
    
        none
    '''
    
    #Selection of the star 
    
    if star=='TrES2b':
        
        #Save the data files (w/o extension, which is '.tbl')
    
        files_long: List[str] = ['Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6',\
                                 'Q7', 'Q9', 'Q10', 'Q11', 'Q13', 'Q14', 'Q15',\
                                 'Q17']
            
        files_short: List[str] = ['Q0', 'Q1', 'Q2a', 'Q2b', 'Q2c', 'Q3a', 'Q3b',\
                                  'Q3c', 'Q4', 'Q5', 'Q6a', 'Q6b', 'Q6c', 'Q7a',\
                                  'Q7b', 'Q7c', 'Q9a', 'Q9b', 'Q9c', 'Q10a',\
                                  'Q10b', 'Q10c', 'Q11a', 'Q11b', 'Q11c', 'Q13a',\
                                  'Q13b', 'Q13c', 'Q14a', 'Q14b', 'Q14c', 'Q15a',\
                                  'Q15b', 'Q15c', 'Q17a', 'Q17b']
        
    elif star=='Kepler75b':
        
        #Save the data files (w/o extension, which is '.tbl')
        
        files_long: List[str] = []
        
        files_short: List[str] = []

    #Create list to save the data    
        
    time: List[float] = []
    
    final_flux: List[float] = []
    
    #Save the data
    
    for i in range(len(files_long)):
        
        read_time: List [float]
        
        read_flux: List[float]
        
        read_time, read_flux = RD.read_long_data(star,files_long[i], f_filter)
        
        for j in range(len(read_flux)):
            
            time.append(read_time[j])
            
            final_flux.append(read_flux[j])
            
    for k in range(len(files_short)):
        
        read_time: List [float]
        
        read_flux: List[float]
        
        read_time, read_flux = RD.read_short_data(star,files_short[k], f_filter)
        
        for l in range(len(read_flux)):
            
            time.append(read_time[l])
            
            final_flux.append(read_flux[l])
            
    #Plot the data
    
    if f_filter==True:
        
        PD.plot_norm_data(time, final_flux, star)
        
    else:
        
        PD.plot_data(time, final_flux, star)
    
print('')

#Asks for the star name

star: str = input('Type the star you want to study (TrES2b or Kepler75): ')

print('')

#Checks if the star is among the stars we have data of
    
while star != 'TrES2b':
    
    if star == 'Kepler75b':
        
        print('Data not available. Plesa try with another star.')
        
        print('')
    
    else:
        
        print('Try one of the mentioned stars (TrES2b or Kepler75).')
    
        print('')

    #Reasks for the star name

    star: str = input('Type the star you want to study (TrES2b or Kepler75): ')

    print('')

f: str = input('Do you want to apply the first filter? (It wiil be applied\
               unless specified): ')
    
if f.lower()=='no':
    
    f_filter: bool = False
    
else:
    
    f_filter: bool = True

#Runs the program
    
main(star, f_filter)