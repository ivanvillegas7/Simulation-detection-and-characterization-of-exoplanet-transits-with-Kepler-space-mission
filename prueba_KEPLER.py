# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 19:07:04 2023

@author: Iván Villegas Pérez
"""

'''

This program is a test on how to read KEPLER satelletite data.

'''

from typing import List

j: int = 0

k: int = 0

KEPLER_id: List[str] = []

degree_ra: List[float] = []

ra_err: List[float] = []

ra_str: List[str] = []

degree_dec: List[float] = []

dec_err: List[float] = []

dec_str: List[str] = []

koi_gmag: List[float] = []

koi_gmag_err: List[float] = []

koi_rmag: List[float] = []

with open("koi_tabdelimited_dr25_27mar17.txt", "r") as infile:
    
    lines = infile.readlines()
    
    #Check how many columns can contain some kind of data.
    
    '''

    for  line in  lines:

        vals = line.split()

        col: int = len(vals)
        
        if j == 0:
        
            for i in range(0, len(vals)):
                
                print(f'{vals[i]}\n')
            
            j+=1
            
            print(col)
            
        break
    
    '''
    
    #Read the data.
    
    for line in lines:
        
        vals = line.split()
        
        if k == 0:
            
            k+=1
            
        else:
        
            KEPLER_id.append(str(vals[0]))
            
            if 'Kepler-' in vals[2]:
                
                if 'b' in vals[4] or 'c' in vals[4] or 'd' in vals[4]:
                    
                    degree_ra.append(float(vals[5]))
                    
                    ra_err.append(float(vals[6]))
                    
                    ra_str.append(str(vals[7]))
                    
                    degree_dec.append(float(vals[8]))
                    
                    dec_err.append(float(vals[9]))
                    
                    dec_str.append(str(vals[10]))
                    
                    koi_gmag.append(float(vals[11]))
                    
                    koi_gmag_err.append(float(vals[12]))
                    
                    koi_rmag.append(float(vals[13]))
                    
                else:
                
                    degree_ra.append(float(vals[4]))
                    
                    ra_err.append(float(vals[5]))
                    
                    ra_str.append(str(vals[6]))
                    
                    degree_dec.append(float(vals[7]))
                    
                    dec_err.append(float(vals[8]))
                    
                    dec_str.append(str(vals[9]))
                    
                    koi_gmag.append(float(vals[10]))
                    
                    koi_gmag_err.append(float(vals[11]))
                    
                    koi_rmag.append(float(vals[12]))
               
            else:
                
                degree_ra.append(float(vals[2]))
                
                ra_err.append(float(vals[3]))
                
                ra_str.append(str(vals[4]))
                
                degree_dec.append(float(vals[5]))
                
                dec_err.append(float(vals[6]))
                
                dec_str.append(str(vals[7]))
                
                koi_gmag.append(float(vals[8]))
                
                koi_gmag_err.append(float(vals[9]))
                
                koi_rmag.append(float(vals[10]))