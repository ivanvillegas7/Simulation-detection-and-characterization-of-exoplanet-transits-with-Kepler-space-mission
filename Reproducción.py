# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 11:16:50 2023

@author: Iván
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import nct as noncentralT
import scipy as sc
import pandas as pd
from scipy.stats import boxcox
from scipy.stats import normaltest

'''
data = np.loadtxt('../Python/TrES2b/Short/ShortQ0.tbl', skiprows=3)
time = data[:, 1] 
flux = data[:, 2]
'''
cut = 3 #for normalisation
sigma_correction = 0.9865783925581086 # = np.sqrt(scipy.special.gammainc(1.5, 0.5* cut**2)/scipy.special.gammainc(0.5, 0.5* cut**2)), computed for cut = 3, it is chosen such that: STD[{N(x, sigma=1) | x < cut}]


def discard_planet(Time, Flux, period, phase, half_time_transit):
    """eliminates flux where there was a planet. That is:
        Flux[k*period + start: k*period + end] = 0
        Variance[k*period + start: k*period + end] = inf
        for k natural number"""
    ne_prehodna_tocka = np.array([(math.fmod(t - phase, period) <\
    period - half_time_transit) and (math.fmod(t-phase, period)>half_time_transit)\
    for t in Time]) #true if a point is not during a time of transit
    return np.copy(Time[ne_prehodna_tocka]), np.copy(Flux[ne_prehodna_tocka])



def normalization(Flux):
    """iterates to get the right sigma of Flux and normalizes Flux to sigma = 1"""
    sigma = np.std(Flux)
    average= np.median(Flux)
    
    for i in range(20):
        
        flux_no_outliers = np.copy(Flux[ np.abs(Flux - average) < cut * sigma])  # ~ negates mask_outliers
        average = np.median(flux_no_outliers)
        sigma = np.std(flux_no_outliers) / sigma_correction
        
    return average, sigma



def normalize_identify_holes(all_time, all_flux):
    for i in range(len(all_time)):
        all_flux[i] = (all_flux[i] / np.median(all_flux[i])) - 1

    Time = all_time#np.concatenate(all_time)
    Flux = all_flux#np.concatenate(all_flux)

    average, sigma = normalization(Flux)
    Flux = (Flux - average) / sigma

    Time -= Time[0]

    return Time, Flux, sigma
    #df = pd.DataFrame(data={'Flux': Flux, 'Time': Time})
    #df.to_csv(home + 'data/time_flux_holes_' + str(id) + '.txt', index=False)
    
def fit_pdf(concatenated_fluxes):
    """fits pdf noise model and returns parameters of distribution"""
    N = norm.pdf(concatenated_fluxes, scale=1.0)

    def minus_logp_nc(parameters):
        """noise is modeled as a combination of gaussian majority and noncentral student t distribution modeling outliers
        fit is performed with no gradient as gradient of noncentral T is complicated. We use Powell method which does not accept bounds,
        therefore parameters are bijected on a suitable interval"""
        A = 0.5 * np.exp(-np.abs(parameters[0]))  # (-inf, inf) -> (0, 0.5]
        probabilities = (1 - A) * N + A * noncentralT.pdf(concatenated_fluxes, *np.abs(parameters[1:]))
        return - np.sum(np.log(probabilities))

    initial_guess = [0.409055969, 1.60403835, 0.85777229, 1.93993457, 0.74511898]
    optimize = sc.optimize.minimize(minus_logp_nc, initial_guess, method='Powell')
    params = optimize['x']
    params = np.abs(params)
    params[0] = 0.5 * np.exp(-np.abs(params[0]))
    return params

def fit_pdf_per_era():
    eight_planet_id = 11442793
    file = 'kepler_short' + str(eight_planet_id)
    df = pd.read_csv('../joint_fit_and_preprocessing//data/'+file+'.txt')
    Identificator = np.array(df["Identificator"])
    flux = np.load('../joint_fit_and_preprocessing//flux_ttv_sc.npy')
    num_eras = Identificator[-1] + 1
    distribution_array = np.zeros(shape = (num_eras, 5))
    t = np.linspace(-15, 15, 100)
    for era in range(num_eras):
        distribution_array[era, :] = fit_pdf(flux[Identificator == era])
        plt.plot(t, pdf_noise(t, *distribution_array[era, :]), label = str(era))

    np.savetxt('distribution_array.txt', distribution_array)
    plt.legend()
    plt.yscale('log')
    plt.show()
    
def pdf_noise(x, A, df, nc, loc, scale):
    """noise is modeled as a combination of gaussian majority and non central student t distribution model fot outliers"""
    return norm.pdf(x) + A * noncentralT.pdf(x, df, nc, loc= loc, scale = scale)




def simulate_noise(N, params):
    """Generates noise signal according to our noise distribution = Gauss + noncentral Student`s t
    N = number of realizations
    params =[A, df, nc, loc, scale] see: https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.stats.nct.html
    """
    N_outliers = int(params[0]*N) #number of outliers
    
    Gaussian = np.random.normal(loc = 0.0, scale = 1.0, size= N - N_outliers)
    
    outliers = noncentralT.rvs(*params[1:], size=N_outliers)
    
    fluxi = np.concatenate([Gaussian, outliers])
    
    np.random.shuffle(fluxi)
    
    return fluxi

def probability_x_is_outlier(x, A, df, nc, loc, scale):
    PN, PO = norm.pdf(x), noncentralT.pdf(x, df, nc, loc=loc, scale=scale)
    return A*PO/(A*PO + (1-A)*PN)

def simulate_transit(period, phase, transit_duration, t_start, t_end, t_step):
    
    # Generate time array
    time = np.arange(t_start, t_end + t_step, t_step)
    
    # Calculate phase for each time step
    phase_arr = (time / period - phase) % 1.0
    
    # Calculate transit model
    transit_model = 10*np.ones_like(phase_arr)
    transit_model[np.abs(phase_arr - 0.5) < transit_duration / 2.0] = 7.5
    
    # Plot the transit model
    plt.figure()
    plt.plot(time, transit_model)
    plt.xlabel('Time (days)')
    plt.ylabel('Flux')
    plt.title('Simulated Transit')
    plt.show()
    
    return(time, transit_model)

def main():
    
    time, flux_p = simulate_transit(2.5, 0.2, 0.1, 0, 50, 0.01)
    
    params = [0.3, 3, 1, 0, 1]
    
    flux = flux_p + simulate_noise(len(flux_p), params)
    
    plt.figure()
    
    plt.plot(time, flux)
    
    #Time, Flux = discard_planet(time, flux, 2.5, 0.2, 0.1)
    
    mu, sigma = normalization(flux)
    
    print(mu, sigma)
    
    print('')
    
    #time, flux, sigma = normalize_identify_holes(time, flux)
    
    parameters = fit_pdf(flux)
    
    print(parameters)
        
    #plt.figure()
    
    #plt.plot(time, flux)
        
    #fit_pdf_per_era()
    
    print('')
    
    statistic, pvalue = normaltest(np.array(flux - flux_p), 0)
    
    print(statistic, pvalue)
    
def mainGPT():

    time, flux_p = simulate_transit(2.5, 0.2, 0.1, 0, 50, 0.01)

    # Generar ruido no gaussiano
    params = [0.3, 3, 1, 0, 1]
    noise = simulate_noise(5001, params)
    
    for i in range(len(noise)):
        
        if noise[i] < -flux_p[i]:
            
            noise[i]=abs(noise[i])
    
    flux = flux_p + noise
    
    plt.figure()
    
    plt.plot(time, flux)
    
    mu, sigma = normalization(flux)
    
    print(mu, sigma)
    
    print('')
    
    # Aplicar transformación de Box-Cox
    lmbda, transformed = boxcox(flux)
    
    resta = transformed-flux_p
    
    mu, sigma = normalization(resta)
    
    print(mu, sigma)
    
    # Calcular parámetros de distribución gaussiana
    mu, std = np.mean(resta), np.std(resta)
    
    print('')
    
    print(mu, std)
    
    # Graficar distribución resultante
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    axs[0].hist(noise, bins=50, alpha=0.5)
    axs[0].set_title('Distribución original')
    axs[1].hist(resta, bins=50, alpha=0.5)
    axs[1].set_title('Distribución transformada (Box-Cox)')
    axs[1].axvline(mu, color='r', linestyle='--', label='media')
    axs[1].axvline(mu+std, color='g', linestyle='--', label='1 sigma')
    axs[1].axvline(mu-std, color='g', linestyle='--')
    axs[1].legend()
    plt.show()
    
    
    print('')
    
    statistic, pvalue = normaltest(np.array(resta), 0)
    
    print(statistic, pvalue)

print('')

print('Simulación 1')

mainGPT()

print('')

print('Simulación 2')

main()
