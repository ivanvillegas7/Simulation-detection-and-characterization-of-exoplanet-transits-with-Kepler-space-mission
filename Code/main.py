# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 11:49:51 2023

@author: Iván
"""

import ReadData as RD

import PlotData as PD

from typing import List

def main(star: str):
    
    '''
    This is the main function of the program. For a given star, it calls the
    different functions, which reads, normalises and plot the data for that
    star.
    
    Parameters:
        
        star: name of the studied star
        
    Returns:
    
        none
    '''
    
    if star=='TrES2b':
    
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
        
        files_long: List[str] = []
        
        files_short: List[str] = []
            
    time: List[float] = []
    
    norm_flux: List[float] = []
    
    for i in range(len(files_long)):
        
        read_time: List [float]
        
        read_flux: List[float]
        
        read_time, read_flux = RD.read_long_data(star,files_long[i])
        
        for j in range(len(read_flux)):
            
            time.append(read_time[j])
            
            norm_flux.append(read_flux[j])
            
    for k in range(len(files_short)):
        
        read_time: List [float]
        
        read_flux: List[float]
        
        read_time, read_flux = RD.read_short_data(star,files_short[k])
        
        for l in range(len(read_flux)):
            
            time.append(read_time[l])
            
            norm_flux.append(read_flux[l])
        
    PD.plot_norm_data(time, norm_flux, star)
    
print('')

star: str = input('Type the star you want to study (TrES2b or Kepler75): ') #Asks for the star name

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

    star: str = input('Type the star you want to study (TrES2b or Kepler75): ') #Asks for the star name

    print('')
    
main(star)