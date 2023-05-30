# -*- coding: utf-8 -*-
"""
Created on Wed May 24 14:43:26 2023

@author: Diego Herranz Muñoz
"""

import numpy as np

from scipy.special import erf

#%%    BASIC STATISTICS

def normal_confidence_interval(nsigmas):

    """
    Returns the confidence interval corresponding to a given sigma value
    in a Gaussian distribution.

    Parameters
    ----------
    nsigmas : float
        The sigma level.

    Returns
    -------
    float
        The corresponding confidence interval. It is a value between 0 and 1.

    """
    return erf(nsigmas/np.sqrt(2.0))

def confidence_limits(array,cl):

    """
      For a given array, gets the lower and upper values corresponding to
      a confidence limit cl. This confidence limit takes value 0.0<=cl<=1.0
    """

    x = array.copy()
    x.sort()
    p = (1.0-cl)/2
    lower = int(p*len(x))
    upper = len(x)-lower
    return np.array([x[lower],x[upper]])

