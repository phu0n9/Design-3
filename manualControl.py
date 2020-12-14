import serial
import time

# change COM6 to /dev/ttyAMA0 in raspberry pi
ser = serial.Serial('COM6', 9600, timeout = 1, write_timeout=1)

def keyboardControl(key):
    serial.Serial.flush(ser)
    serial.Serial.flushOutput(ser)
    # if(key == 'w'):
    ser.write(key.encode())
    # elif (key == 's'):
    #     ser.write(key.encode())
    # elif (key == 'a'):
    #     ser.write(key.encode())    
    # elif (key == 'd'):
    #     ser.write(key.encode())
    time.sleep(0.05)
