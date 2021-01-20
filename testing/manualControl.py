import serial
import time

# change COM6 to /dev/ttyAMA0 in raspberry pi

import serial
import time

ser = serial.Serial('COM10', 115200)
time.sleep(1)

power = []
velocity = []
compass = []

def flush_data():
    serial.Serial.flush(ser)
    serial.Serial.flushOutput(ser)
    serial.Serial.flushInput(ser)

def count_white_space(data):
    if data.count(' ') == 2: 
        return data

def data_display():
    flush_data()
    buffer = []
    data_compass = ""
    data_string = ""
    waiting = ser.in_waiting
    buffer += [chr(c) for c in ser.read(waiting)]
    print("buffer",buffer)
    data_string = data_string.join(buffer)
    data_string = data_string.split("\r\n")
    filter_data = count_white_space(data_string[0])
    try:
        split_data = filter_data.split()
        data_power = split_data[0]
        data_velocity = split_data[1]
        orientation = float(split_data[2])
        if orientation <= 45 or orientation > 315:
            data_compass = "North"
        elif orientation > 45 and orientation <= 135:
            data_compass = "West"
        elif orientation > 135 and orientation <= 225:
            data_compass = "South"   
        elif orientation > 225 and orientation <= 315:
            data_compass = "East"
        power.append(data_power)
        velocity.append(data_velocity)
        compass.append(data_compass)
        print("line",power)
        return power,velocity,compass
    except AttributeError:
        print("new line",power)
        return power,velocity,compass
    # except AttributeError:
    #     split_data = ""
    #     print("hello",power)
    #     return power,velocity,compass

    # print("this",power)
    # return power,velocity,compass
