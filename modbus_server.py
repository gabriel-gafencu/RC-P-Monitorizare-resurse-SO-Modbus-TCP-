import struct
import socket
import threading
import time
import psutil
import math

DEFAULT_IP = '192.168.100.10'
DEFAULT_PORT = 502
DEFAULT_ID = 0x00  # or 0xFF standard for Modbus TCP/IP


class Modbus_Server:
    # effective addresses for Modbus tcp go from 0 to 65553, but for the sake of simplicity
    # and proof of concept, we use a 10000 address space
    coils = [0] * 10000
    discrete_inputs = [0] * 10000
    input_registers = [0] * 10000
    holding_registers = [0] * 10000

    conn = None
    addr = None

    def __init__(self, ip=DEFAULT_IP, port=DEFAULT_PORT):
        self.tcp_ip = ip
        self.tcp_port = port
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.awaiting_pin = True
        self.established_connection = False

    def initialize_connection(self):
        # connection is authorized once the client requests coils 7, 77, 777 and 7777 to be turned ON
        # after receiving a write_single_coil operation, the server simply echoes back the packet
        # first coil(pin) to check is 7
        current_pin = 7
        self.tcp_socket.bind((self.tcp_ip, self.tcp_port))
        self.tcp_socket.listen()
        self.conn, self.addr = self.tcp_socket.accept()
        with self.conn:
            print("Connected by", self.addr)
            while self.awaiting_pin:
                initial_data = self.conn.recv(1024)
                unpacked_data = struct.unpack('12B', initial_data)
                coil_addr = unpacked_data[8] * 256 + unpacked_data[9]
                function_code = unpacked_data[7]
                if unpacked_data[10] == 255:
                    state = 1
                else:
                    state = 0
                if current_pin == coil_addr and function_code == 5 and state == 1:
                    self.coils[coil_addr] = 1
                    self.conn.sendall(initial_data)
                    # calculating the next pin(coil) to check
                    current_pin = current_pin * 10 + 7
                if self.coils[7] and self.coils[77] and self.coils[777] and self.coils[7777]:
                    self.awaiting_pin = False
                    self.established_connection = True
                    print("Connection established: ", self.established_connection)

    # this function is started by a different thread once a connection has been established
    # it simply updates the OS resources mapped to all the different data structures of the Modbus Server
    # every 0.5 seconds
    def update_info(self):
        while True:
            # mapping the whole and the fractionary part of the cpu percent to the 1st and 2nd input registers
            frac, whole = math.modf(psutil.cpu_percent())
            self.input_registers[1] = whole
            self.input_registers[2] = int(frac) * 100

            # mapping the whole and fractionary part of the memory usage (in %) to the 1st and 2nd holding registers
            frac, whole = math.modf(psutil.virtual_memory()[2])
            self.holding_registers[1] = whole
            self.holding_registers[2] = int(frac) * 100

            # mapping the whole and fractionary part of disk usage (in %) to the 11th and 12th holding registers
            frac, whole = math.modf(psutil.disk_usage('/')[3])
            self.holding_registers[11] = whole
            self.holding_registers[12] = int(frac) * 100

            # print("CPU: ", self.input_registers[1] + self.input_registers[2])
            # print("Memory: ", self.holding_registers[1] + self.holding_registers[2])
            # print("Disk: ", self.holding_registers[11] + self.holding_registers[12])
            time.sleep(0.5)

    def run(self):
        update_thread = threading.Thread(target=self.update_info())
        update_thread.start()
        initial_data = self.conn.recv(1024)
        unpacked_data = struct.unpack('12B', initial_data)
        print(unpacked_data)
        function_code = unpacked_data[7]
        if function_code == 3:
            # reading holding registers, need to echo back
            starting_register = unpacked_data[8] * 256 + unpacked_data[9]
            no_of_registers = unpacked_data[10] * 256 + unpacked_data[11]
            # currently hard-coded 12 bytes packets, might require refactoring
            packet = struct.pack('13B', unpacked_data[0], unpacked_data[1], unpacked_data[2], unpacked_data[3],
                                 unpacked_data[4], unpacked_data[5], unpacked_data[6], function_code,
                                 int(no_of_registers * 2), 0x00,
                                 int(self.holding_registers[starting_register]), 0x00,
                                 int(self.holding_registers[starting_register + no_of_registers - 1]))
            self.conn.sendall(packet)
        else:
            if function_code == 4:
                # reading input registers, need to echo back
                starting_register = unpacked_data[8] * 256 + unpacked_data[9]
                no_of_registers = unpacked_data[10] * 256 + unpacked_data[11]
                packet = struct.pack('13B', unpacked_data[0], unpacked_data[1], unpacked_data[2], unpacked_data[3],
                                     unpacked_data[4], unpacked_data[5], unpacked_data[6], function_code,
                                     int(no_of_registers * 2), 0x00,
                                     int(self.holding_registers[starting_register]), 0x00,
                                     int(self.holding_registers[starting_register + no_of_registers - 1]))
                self.conn.sendall(packet)
        # TODO
        # complete for the other function codes, currently unnecessary


if __name__ == '__main__':
    server = Modbus_Server()
    server.initialize_connection()
    server.run()
