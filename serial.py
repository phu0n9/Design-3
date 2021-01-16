import serial
import time

# change COM6 to /dev/ttyAMA0 in raspberry pi
ser = serial.Serial('COM6', 9600, timeout = 1, write_timeout=1)

def keyboardControl(key):
    serial.Serial.flush(ser)
    serial.Serial.flushOutput(ser)
    serial.Serial.flushInput(ser)
    # ser.write(key.encode())
    time.sleep(0.05)

def data_display():
    serial.Serial.flush(ser)
    serial.Serial.flushOutput(ser)
    serial.Serial.flushInput(ser)
    compass = ""
    data = ser.read_until()
    decode_data = data.decode('utf-8', 'strict')
    sensor = decode_data.split()
    power = sensor[0]
    velocity = float(sensor[1])*2.04/60 #cm/s
    orientation = float(sensor[2])
    if(orientation < 45 or orientation >= 315):
        compass = "North"
        # print(orientation)
    elif(orientation >= 45  and orientation < 135):
        compass = "West"
        # print(orientation)
    elif(orientation >= 135  and orientation < 225):
        compass = "South"
        # print(orientation)
    elif(orientation >= 225  and orientation < 315):
        compass = "East"
        # print(orientation)
    return velocity,compass,power
    # print(power," ",velocity," ",compass)
