import serial
import time
import asyncio
import filter_anomalies
import features

def get_curr_arrayX():
    return curr_arrayX

def get_curr_arrayY():
    return curr_arrayY

def get_curr_arrayZ():
    return curr_arrayZ

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
                    print("Received:", data)
                except:
                    print("Error.")
        else:
            curr_arrayX = data_arrayX
            curr_arrayY = data_arrayY
            curr_arrayZ = data_arrayZ
            start_time = time.time()

            filtered_X = filter_anomalies.filter(curr_arrayX)
            filtered_Y = filter_anomalies.filter(curr_arrayY)
            filtered_Z = filter_anomalies.filter(curr_arrayZ)

            print(filtered_X)
            print(filtered_Y)
            print(filtered_Z)

            data_arrayX = []
            data_arrayY = []
            data_arrayZ = []
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    ser.close()  # Close the port when done
