import serial
import time
import json

# change COM6 to /dev/ttyAMA0 in raspberry pi
ser = serial.Serial('COM6', 9600, timeout = 1, write_timeout=1)

data = {}
def keyboardControl(key):
    serial.Serial.flush(ser)
    serial.Serial.flushOutput(ser)
    serial.Serial.flushInput(ser)
    # ser.write(key.encode())
    time.sleep(0.05)

def nth_repl(s, sub, repl, n):
    find = s.find(sub)
    # If find is not -1 we have found at least one match for the substring
    i = find != -1
    # loop util we find the nth or we find no match
    while find != -1 and i != n:
        # find + 1 means we start searching from after the last match
        find = s.find(sub, find + 1)
        i += 1
    # If i is equal to n we found nth match so replace
    if i == n:
        return s[:find] + repl + s[find+len(sub):]
    return s
def data_display():
    arr = []
    count = 0
    velocity = 0
    compass = ""
    power = 0
    while ser.isOpen():
        try:
            serial.Serial.flush(ser)
            serial.Serial.flushOutput(ser)
            serial.Serial.flushInput(ser)
            data = ser.read_until()
            decode_data = data.decode('utf-8', 'strict')
            sensor = decode_data.split()
            power = sensor[0]
            if sensor[1].count('.') == 1:
                velocity = float(sensor[1]) * 2.04 / 60  # cm/s
            else:
                velocity = 0

            if sensor[2].count('.') <= 1:
                orientation = float(sensor[2])
            else:
                print("sensor[2] ", sensor[2])
                nth_repl(sensor[2], ".", 2)
                orientation = float(sensor[2])

            if orientation < 45 or orientation >= 315:
                compass = "North"
                # print(orientation)
                print(compass)
            elif 45 <= orientation < 135:
                compass = "West"
                # print(orientation)
                print(compass)
            elif 135 <= orientation < 225:
                compass = "South"
                # print(orientation)
                print(compass)
            elif 225 <= orientation < 315:
                compass = "East"
                print(compass)
            data = {'velocity': velocity, 'power': power, 'direction': compass}
            return data

        except IndexError:
            print("index error", compass,velocity,power)
            data = {'velocity': 0.0, 'power': 0.0, 'direction': "thisError"}
            return data
           
        except ValueError:
            print("value error", compass,velocity,power)
            data = {'velocity': 0.0, 'power': 0.0, 'direction': "Error"}
            return data

def data_display():
    direction_var = ""
    velocity_var = 0
    power_var = 0
    velocity = 0
    compass = ""
    power = 0
    while ser.isOpen():
        serial.Serial.flush(ser)
        serial.Serial.flushOutput(ser)
        serial.Serial.flushInput(ser)
        data = ser.read_until()
        decode_data = data.decode('utf-8', 'strict')
        sensor = decode_data.split()
        try:
            power = sensor[0]
            velocity = float(sensor[1]) * 2.04 / 60  # cm/s
            orientation = float(sensor[2])

            if orientation < 45 or orientation >= 315:
                compass = "North"
                # print(orientation)
                # print(compass)
            elif 45 <= orientation < 135:
                compass = "West"
                # print(orientation)
                # print(compass)
            elif 135 <= orientation < 225:
                compass = "South"
                # print(orientation)
                # print(compass)
            elif 225 <= orientation < 315:
                compass = "East"
                # print(compass)
            direction_var = compass
            power_var = power
            velocity_var = velocity
            data = {'velocity': velocity, 'power': power, 'direction': compass}
            return data

        except IndexError:
            compass = direction_var
            power = power_var
            velocity = velocity_var
            # print("index error", compass,power,velocity)
            data = {'velocity': velocity, 'power': power, 'direction': compass}
            return data

        except ValueError:
            compass = direction_var
            power = power_var
            velocity = velocity_var
            # print("value error", compass,velocity,power)
            data = {'velocity': velocity, 'power': power, 'direction': compass}
            return data
