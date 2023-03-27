# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 13:20:37 2023

@author: Iván Villegas Pérez
"""
import numpy as np

from typing import List

from typing import Tuple

def first_filter(x: List[float], y: List[float]) -> Tuple[List[float],\
                                                          List[float]]:
    
    '''
    
    This function applys a first filter by adjusting the dat apoint to a first
    order polynom and ignores the data above 3 sigma (but not under because we
    want to preserve the minimums).
    
    Parameters:
        
        x: x coordinate of the data (time).
        
        y: y coordinate of the data (flux).
        
    Returns:
        
        time: selected time points for the study.
        
        flux: selected flux points for the study.
    
    '''
    
    suma_xy = 0

    suma_x = 0

    suma_y = 0

    suma_xx = 0

    n: int = 0

    for i in range(len(x)):
        
        if str(y[i]) != "nan":
        
            suma_xy = suma_xy + x[i]*y[i]
            
            suma_x = suma_x + x[i]
            
            suma_y = suma_y + y[i]
            
            suma_xx = suma_xx + x[i]**2
            
            n+=1
            
    a = (n*suma_xy-suma_x*suma_y)/(n*suma_xx-suma_x**2)

    b = (suma_y-a*suma_x)/n

    suma_sigma: float = 0

    for j in range(len(x)):
        
        if str(y[i]) != "nan":
        
            suma_sigma = suma_sigma+(y[i]-a*x[i]-b)**2

    sigma: float =  np.sqrt(suma_sigma/(n-2))

    err_a: float = np.sqrt(n)*sigma/np.sqrt(n*suma_xx-suma_x**2)

    err_b: float = err_a*np.sqrt(suma_xx/n)
    
    time: List[float] = []
    
    flux: List[float] = []
    
    for k in range(len(x)):
        
        if y[k]-(a*x[k]+b)<=3*np.sqrt(x[j]**2*err_a**2+err_b**2):
            
            time.append(x[k])
            
            flux.append(y[k])
    
    return (time, flux)

def normalize(flux: List[float]) -> List[float]:
    
    '''
    
    This function normalises the flux with respect to the maximum value.
    
    Parameters:
        
        flux: un-normalised flux.
        
    Returns:
        
        return_flux: normlaised flux.
    
    '''
    
    #Selects the maximum value
    
    div: float = max(flux)
    
    return_flux: List[float] = []
    
    #Normalises the flux
    
    for i in range(0, len(flux)):
        
        return_flux.append(flux[i]/div)
        
    return return_flux

def read_long_data(star: str, quarter: str) -> Tuple[List[float], List[float]]:
    
    '''
    
    This function reads the data from each individual quarter (long cadence).
    
    Parameters:
        
        star: star (or planet) name.
        
        quarter: number of the quarter (Q#).
                                        
    Returns:
        
        time: list containing time values.
        
        flux: list containing flux values.
    
    '''
    
    with open(f'../{star}/Long/Long{quarter}.tbl', "r") as infile:
        
        i: int = 0
        
        time: List[float] = []
    
        flux : List[float] = []
        
        lines = infile.readlines()
        
        #Reads the data.
        
        for line in lines:
            
            vals = line.split()
            
            if i < 3:
                
                i+=1
                
            else:
                
                time.append(float(vals[1]))
                
                flux.append(float(vals[2])*1e-3)
                
    filtered_time: List[float]
    
    filtered_flux: List[float]
    
    #Apply the first filter
    
    filtered_time, filtered_flux = first_filter(time, flux)
                
    return (filtered_time, normalize(filtered_flux))

def read_short_data(star: str, quarter: str) -> Tuple[List[float], List[float]]:
    
    '''
    
    This function reads the data from each individual quarter (short cadence).
    
    Parameters:
        
        star: star (or planet) name.
        
        quarter: number of the quarter (Q#).
                                        
    Returns:
        
        time: list containing time values.
        
        flux: list containing flux values.
    
    '''
    
    with open(f'../{star}/Short/Short{quarter}.tbl', "r") as infile:
        
        i: int = 0
        
        time: List[float] = []
    
        flux : List[float] = []
        
        lines = infile.readlines()
        
        #Reads the data.
        
        for line in lines:
            
            vals = line.split()
            
            #Skip the first 3 lines
            
            if i < 3:
                
                i+=1
                
            else:
                
                time.append(float(vals[1]))
                
                flux.append(float(vals[2])*1e-3)
                
    filtered_time: List[float]
    
    filtered_flux: List[float]
    
    #Apply the first filter
    
    filtered_time, filtered_flux = first_filter(time, flux)
                
    return (filtered_time, normalize(filtered_flux))
