import serial
import time
import asyncio
import filter_anomalies
import features
import pandas as pd
from joblib import load

import sklearn
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

globalArray = []
counter = 0

def get_curr_arrayX():
    return curr_arrayX

def get_curr_arrayY():
    return curr_arrayY

def get_curr_arrayZ():
    return curr_arrayZ

def filtering():
    filtered_x = filter_anomalies.filter(curr_arrayX)
    filtered_y = filter_anomalies.filter(curr_arrayY)
    filtered_z = filter_anomalies.filter(curr_arrayZ)

    print(filtered_x)
    print(filtered_y)
    print(filtered_z)

    get_data(filtered_x,filtered_y,filtered_z)

def  get_data(x,y,z):

    global counter
    global globalArray

    x_max = features.get_max(x)
    y_max = features.get_max(y)
    z_max = features.get_max(z)

    x_min = features.get_min(x)
    y_min = features.get_min(y)
    z_min = features.get_min(z)

    x_std = features.get_std(x)
    y_std = features.get_std(y)
    z_std = features.get_std(z)

    x_mean = features.get_mean(x)
    y_mean = features.get_mean(y)
    z_mean = features.get_mean(z)

    """

    magnitude = features.get_magnitude(x,y,z)
    magnitude_max = features.get_max(magnitude)
    magnitude_min = features.get_min(magnitude)
    magnitude_std = features.get_std(magnitude)
    magnitude_mean = features.get_mean(magnitude)

   

    energy = features.get_energy(magnitude)

     """

    zerocrossing_x = features.get_zero_crossing_rates(x)
    zerocrossing_y = features.get_zero_crossing_rates(y)
    zerocrossing_z = features.get_zero_crossing_rates(z)

    peaks_x = features.get_peak_count(x)
    peaks_y = features.get_peak_count(y)
    peaks_z = features.get_peak_count(z)

       # Wrap the result array as a list of lists (2D data)
    result_array = [[x_max,y_max,z_max,x_min, y_min, z_min, x_std, y_std, z_std, x_mean, y_mean, z_mean,
                     zerocrossing_x, zerocrossing_y, zerocrossing_z, peaks_x, peaks_y, peaks_z]]

    classifier = load('TremorSeverityPrediction.joblib')
    level_prediction = classifier.predict(result_array)


    print("Tremor level is ")
    print(level_prediction[0])

    #counter += 1

    #globalArray.append(result_array)


    #if counter == 3:
    #   save_data()

    

def save_data():

    df = pd.DataFrame(globalArray, columns=["x_max","y_max","z_max","x_min", "y_min", "z_min", "x_std", "y_std", "z_std", "x_mean", "y_mean", "z_mean",
                                             "zerocross_x", "zerocross_y", "zerocross_z", "peaks_x", "peaks_y", "peaks_z"])

    # Save to CSV
    df.to_csv("output.csv", index=False)
    

    print("DataFrame saved to output.csv")





    

# Configure the serial port
ser = serial.Serial(
    port='COM5',         # Replace with your serial port
    baudrate=9600,       # Match the baud rate of your microcontroller
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1            # Timeout in seconds
)

print("Listening on", ser.port)

data_arrayX = []
data_arrayY = []
data_arrayZ = []

curr_arrayX = []
curr_arrayY = []
curr_arrayZ = []

duration = 5
start_time = time.time()

try:
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time < duration:
            if ser.in_waiting:  # Check if data is available
                try:
                    data = ser.readline().decode('utf-8').strip()  # Read a line and decode
                    split_data = data.split(",")
                    data_arrayX.append(int("".join(split_data[0].split())))
                    data_arrayY.append(int("".join(split_data[1].split())))
                    data_arrayZ.append(int("".join(split_data[2].split())))
                    #print("Received:", data)
                except:
                    print("Error.")
        else:
            curr_arrayX = data_arrayX
            curr_arrayY = data_arrayY
            curr_arrayZ = data_arrayZ
            start_time = time.time()

            filtering()

            data_arrayX = []
            data_arrayY = []
            data_arrayZ = []
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    ser.close()  # Close the port when done





