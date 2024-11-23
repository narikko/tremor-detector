import numpy as np
from scipy.signal import find_peaks

def get_min(data):
    min = np.min(data)

    return min

def get_max(data):
    max = np.max(data)

    return max

def get_mean(data):
    mean = np.mean(data)

    return mean

def get_std(data):
    std = np.std(data)

    return std

def get_magnitude(dataX, dataY, dataZ):

    dataX = np.array(dataX)
    dataY = np.array(dataY)
    dataZ = np.array(dataZ)

    magnitude = np.sqrt(dataX**2 + dataY**2 + dataZ**2)

    return magnitude

def get_energy(magnitude):

    data = np.array(magnitude)
    energy = np.sum(magnitude**2)

    return energy

def get_zero_crossing_rates(data):

    data = np.array(data)
    return (data[:-1] * data[1:] < 0).sum()

def get_peak_count(data):
    
    data = np.array(data)
    return len(find_peaks(data)[0])

def get_absval(data):
    return np.abs(data)