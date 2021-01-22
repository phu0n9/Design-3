import serial
import time

# change COM6 to /dev/ttyAMA0 in raspberry pi
ser = serial.Serial('/dev/tty/ACM0', 9600, timeout = 0.5, write_timeout=0.5)

velocity = 0
compass = ""
power = 0
stage = 0

data = {}
def flush_data():
    serial.Serial.flush(ser)
    serial.Serial.flushOutput(ser)
    serial.Serial.flushInput(ser)

def data_display():
    tmp_velocity =0
    tmp_power = 0
    tmp_direction =""
    global stage
    global compass 
    global power
    global velocity
    while ser.isOpen():
        try:
            flush_data()
            data = ser.readline()
            decode_data = data.decode('utf-8', 'ignore')
            sensor = decode_data.split()
            power = float(sensor[0]) // 1000
            velocity = float(sensor[1]) * 2.04 / 60  # cm/s
            orientation = float(sensor[2])
            stage = sensor[3]
            
            if orientation < 45 or orientation >= 315:
                compass = "North"
            elif 45 <= orientation < 135:
                compass = "West"
            elif 135 <= orientation < 225:
                compass = "South"
            elif 225 <= orientation < 315:
                compass = "East"
            tmp_direction = compass
            tmp_power = power
            tmp_velocity = velocity
            data = {'velocity': velocity, 'power': power, 'direction': compass}
            return data
        except IndexError:
            data = {'velocity': tmp_velocity, 'power': tmp_power, 'direction': tmp_direction}
            return data
           
        except ValueError:
            data = {'velocity': tmp_velocity, 'power': tmp_power, 'direction': tmp_direction}
            return data


def get_stage():
    return stage
