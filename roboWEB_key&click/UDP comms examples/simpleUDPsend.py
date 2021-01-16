import socket
import time
PORTNUM = 10001

stuff = True

while stuff == True:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    data='12'
    s.sendto(data, ('192.168.4.1', PORTNUM))
    time.sleep(0.1)

