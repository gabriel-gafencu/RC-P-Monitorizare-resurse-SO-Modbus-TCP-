import struct
import socket

# list of defaults for initializing the modbus client.
DEFAULT_IP = '192.168.100.10'
DEFAULT_PORT = 502
DEFAULT_ID = 0x00  # or 0xFF standard for Modbus TCP/IP


# Modbus TCP/IP ADU is encoded in Big-Endian,
# hence why the order of the bytes in the sent packets will always be H first -> L second.

class Modbus_Client:
    # transaction identifier (2B), protocol identifier (2B) are both set to 0 (only 1 single client-server connection)
    # length of the ADU + (unit identifier) is always going to be 6 bytes
    transaction_id_h = 0x00
    transaction_id_l = 0x00
    protocol_id_h = 0x00
    protocol_id_l = 0x00
    length_h = 0x00
    length_l = 0x06

    read_coils_function_code = 1
    read_holding_registers_function_code = 3
    read_input_registers_function_code = 4
    write_single_coil_function_code = 5
    write_single_register_function_code = 6
    write_multiple_coils_function_code = 15
    write_multiple_registers_function_code = 16

    def __init__(self, id=DEFAULT_ID, ip=DEFAULT_IP, port=DEFAULT_PORT):
        self.tcp_ip = ip
        self.tcp_port = port
        self.unit_id = id
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 10000, 3000))
        self.established_connection = False

    def initialize_connection(self):
        # need to authorize access to slave by sending something like write ON
        # to coils 7, 77, 777, 7777 as first messages
        self.tcp_socket.connect((self.tcp_ip, self.tcp_port))
        # 7
        sent_packet = self.write_single_coil(True, 0x00, 0x07)
        returned_packet = self.tcp_socket.recv(1024)
        if sent_packet != returned_packet:
            print(sent_packet, " != ", returned_packet)
        # 77
        sent_packet = self.write_single_coil(True, 0x00, 0x4D)
        returned_packet = self.tcp_socket.recv(1024)
        if sent_packet != returned_packet:
            print(sent_packet, " != ", returned_packet)
        # 777
        sent_packet = self.write_single_coil(True, 0x03, 0x09)
        returned_packet = self.tcp_socket.recv(1024)
        if sent_packet != returned_packet:
            print(sent_packet, " != ", returned_packet)
        # 7777
        sent_packet = self.write_single_coil(True, 0x1E, 0x61)
        returned_packet = self.tcp_socket.recv(1024)
        if sent_packet != returned_packet:
            print(sent_packet, " != ", returned_packet)
        self.established_connection = True
        print("Connection established: ", self.established_connection)

    def read_coils(self, addr_h, addr_l, no_of_coils_h, no_of_coils_l):
        # function code 1
        packet = struct.pack('12B', self.transaction_id_h, self.transaction_id_l, self.protocol_id_h,
                             self.protocol_id_l, self.length_h, self.length_l, self.unit_id,
                             int(self.read_coils_function_code), addr_h,
                             addr_l, no_of_coils_h, no_of_coils_l)
        self.tcp_socket.sendall(packet)

    def read_discrete_inputs(self):
        # TODO
        # function code 2
        pass

    def read_holding_registers(self, addr_h, addr_l, no_of_reg_h, no_of_reg_l):
        # function code 3
        packet = struct.pack('12B', self.transaction_id_h, self.transaction_id_l, self.protocol_id_h,
                             self.protocol_id_l, self.length_h, self.length_l, self.unit_id,
                             int(self.read_holding_registers_function_code), addr_h, addr_l, no_of_reg_h, no_of_reg_l)
        self.tcp_socket.sendall(packet)

    def read_input_registers(self, addr_h, addr_l, no_of_reg_h, no_of_reg_l):
        # function code 4
        packet = struct.pack('12B', self.transaction_id_h, self.transaction_id_l, self.protocol_id_h,
                             self.protocol_id_l, self.length_h, self.length_l, self.unit_id,
                             int(self.read_input_registers_function_code), addr_h, addr_l, no_of_reg_h, no_of_reg_l)
        self.tcp_socket.sendall(packet)

    def write_single_coil(self, state=True, addr_h=0x00, addr_l=0x01):
        # function code 5
        # for last 2 bytes on = 0xff and 0x00, off = 0x00 and 0x00
        if state:
            value = 0xff
        else:
            value = 0x00

        packet = struct.pack('12B', self.transaction_id_h, self.transaction_id_l, self.protocol_id_h,
                             self.protocol_id_l, self.length_h, self.length_l, self.unit_id,
                             int(self.write_single_coil_function_code), addr_h, addr_l, value, 0x00)
        self.tcp_socket.sendall(packet)
        return packet

    def write_single_register(self, addr_h, addr_l, data_h, data_l):
        # function code 6
        packet = struct.pack('12B', self.transaction_id_h, self.transaction_id_l, self.protocol_id_h,
                             self.protocol_id_l, self.length_h, self.length_l, self.unit_id,
                             int(self.write_single_register_function_code), addr_h, addr_l, data_h, data_l)
        self.tcp_socket.sendall(packet)

    def write_multiple_coils(self, addr_h, addr_l, no_of_coils_h, no_of_coils_l, byte_count, force_data_h):
        # TODO
        # needs to be refactored
        # function code 15
        # write multiple coils has a different length compared to the previous operations,
        # requiring 8 bytes after its own field
        packet = struct.pack('12B', self.transaction_id_h, self.transaction_id_l, self.protocol_id_h,
                             self.protocol_id_l, 0x00, 0x08, self.unit_id,
                             int(self.write_multiple_coils_function_code), addr_h, addr_l, no_of_coils_h, no_of_coils_l,
                             byte_count, force_data_h)
        self.tcp_socket.sendall(packet)

    def write_multiple_registers(self):
        # TODO
        # function code 16
        pass

    def request_cpu(self):
        # cpu % usage is mapped to input registers 1 and 2 (whole and fractionary, will have to calculate it together)
        # self.tcp_socket.connect((self.tcp_ip, self.tcp_port))
        self.read_input_registers(0x00, 0x01, 0x00, 0x02)
        initial_data = self.tcp_socket.recv(1024)
        unpacked_data = struct.unpack('13B', initial_data)
        cpu_percentage_whole = unpacked_data[8] * 256 + unpacked_data[9]
        cpu_percentage_frac = unpacked_data[10] * 256 + unpacked_data[11]
        return cpu_percentage_whole + (cpu_percentage_frac / 100)

    def request_memory(self):
        pass

    def request_disk(self):
        pass


if __name__ == '__main__':
    client = Modbus_Client()
    client.initialize_connection()
    print(client.request_cpu())