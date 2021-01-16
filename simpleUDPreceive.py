import socket
UDP_PORT = 10001
UDP_IP = "0.0.0.0"
sock = socket.socket(socket.AF_INET, # Internet
socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    if data.decode("utf-8") == 'fw':
        print("Go forward command received")
    elif data.decode("utf-8") == 'bk':
        print("Go backward command received")
    elif data.decode("utf-8") == 'rt':
        print("Turn right command received")
    elif data.decode("utf-8") == 'lt':
        print("Turn Left command received")
    elif data.decode("utf-8") == 'up':
        print("Forklift up command received")
    elif data.decode("utf-8") == 'dn':
        print("Forklift down command received")
    elif data.decode("utf-8") == 'manual':
        print("Manual Mode Activated!!!")
    elif data.decode("utf-8") == 'init':
        print("Autonomous mode activated!")
    else:
        print("Invalid Command")

