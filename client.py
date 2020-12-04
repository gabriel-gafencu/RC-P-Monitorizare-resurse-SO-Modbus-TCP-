import socket
import struct

TCP_IP = '192.168.56.1'
TCP_PORT = 2407


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((TCP_IP, TCP_PORT))
    unitId = 1
    functionCode = 5
    print("\nSwitching on")
    coilId = 5
    req = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, int(unitId), int(functionCode), 0x00, int(coilId),
                      0xff,
                      0x00)
    s.sendall(req)
    data = s.recv(1024)
    print('Received', repr(data))
