import serial
import time

def get_def_arrayX():
    return data_arrayX

def get_def_arrayY():
    return data_arrayY

def get_def_arrayZ():
    return data_arrayZ

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
                data = ser.readline().decode('utf-8').strip()  # Read a line and decode
                split_data = data.split(",")
                data_arrayX.append(split_data[0])
                data_arrayY.append(split_data[1])
                data_arrayZ.append(split_data[2])
                print("Received:", data)
        else:
            curr_arrayX = data_arrayX
            curr_arrayY = data_arrayY
            curr_arrayZ = data_arrayZ
            start_time = time.time()
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    ser.close()  # Close the port when done