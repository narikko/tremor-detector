import serial
import time
import queue
import pandas as pd
from joblib import load
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

import filter_anomalies
import features

import sklearn
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

globalArray = []
counter = 0
xyz_queue = queue.Queue()  # Queue for x, y, z data
index_queue = queue.Queue()  # Queue for prediction indices

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

def get_data(x,y,z):

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

    index_queue.put({'type': 'index', 'index': int(level_prediction[0])})
    
    
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



curr_arrayX = []
curr_arrayY = []
curr_arrayZ = []



def start_serial_reading():
    global curr_arrayX, curr_arrayY, curr_arrayZ, data_queue

    data_arrayX = []
    data_arrayY = []
    data_arrayZ = []

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
                        x = int("".join(split_data[0].split()))+53
                        y = int("".join(split_data[1].split()))-4
                        z = int("".join(split_data[2].split()))+985

                        # Add data to live arrays
                        data_arrayX.append(x)
                        data_arrayY.append(y)
                        data_arrayZ.append(z)

                        # Optional: Put raw data into the queue for live display
                        xyz_queue.put({'type': 'xyz', 'x': x, 'y': y, 'z': z})

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





