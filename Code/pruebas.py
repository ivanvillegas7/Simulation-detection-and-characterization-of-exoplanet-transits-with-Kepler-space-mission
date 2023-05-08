# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 13:41:26 2023

@author: Iván
"""

import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('data.txt')

time = data[:, 0]
filtered_flux = data[:, 0]

# calcular la transformada de Fourier de los datos limpios
frequencies = np.fft.fftfreq(len(time), time[1]-time[0])
power_spectrum = np.abs(np.fft.fft(filtered_flux))**2

plt.plot(frequencies, power_spectrum)

# encontrar el pico más alto en el espectro de potencia
peak_frequency = frequencies[np.argmax(power_spectrum)]
period = 1/peak_frequency

print(period)