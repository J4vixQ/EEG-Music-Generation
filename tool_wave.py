# FFT - Filter - IFFT

import numpy as np
from statistics import mean
from statistics import median

def brain_fft(time, track_brain):
    # time -> frequency
    freqs = np.fft.fftfreq( len(time), (max(time)-min(time))/len(time) )    # actually fftfreq(length, 1/samplerate)
    complex_arry = np.fft.fft(track_brain)
    pows = np.abs(complex_arry)
    return freqs, complex_arry, pows

def brain_bandpass(freqs, complex_arry, low, high):
    # cut frequency
    toolow = np.where(freqs<low)[0]
    toohigh = np.where(freqs>high)[0]
    complex_arry[toolow] = 0
    complex_arry[toohigh] = 0
    pows = np.abs(complex_arry)
    return freqs, complex_arry, pows

def brain_ifft(complex_arry):
    # frequency -> time
    filter_sigs = np.fft.ifft(complex_arry)
    waveS = np.real(filter_sigs)
    return waveS

def get_wave(time, track_brain, low, high):
    # fft-cut-ifft
    freqs, complex_arry, pows = brain_fft(time, track_brain)
    freqs, complex_arry, pows = brain_bandpass(freqs, complex_arry, low, high)
    waveS = brain_ifft(complex_arry)
    return waveS


