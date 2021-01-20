import struct
import socket
import threading
import psutil
import math
import logging
from datetime import date
from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from slaveui import Ui_Slave

DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 502
DEFAULT_ID = 0x00  # or 0xFF standard for Modbus TCP/IP


class Modbus_S(QDialog):
    # effective addresses for Modbus tcp go from 0 to 65553, but for the sake of simplicity
    # and proof of concept, we use a 10000 address space
    coils = [0] * 10000
    discrete_inputs = [0] * 10000
    input_registers = [0] * 10000
    holding_registers = [0] * 10000

    slave_failure = False
    slave_busy = False
    conn = None
    addr = None
    msglist = []

    def __init__(self, ip=DEFAULT_IP, port=DEFAULT_PORT):
        super(Modbus_S, self).__init__()
        self.ui = Ui_Slave()
        self.ui.setupUi(self)
        self.show()

        self.tcp_ip = ip
        self.tcp_port = port
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 10000, 3000))
        self.awaiting_pin = True
        self.established_connection = False

        logging.basicConfig(filename="log_" + str(date.today()) + ".log", level=logging.INFO)

        self.ui.save_btn.clicked.connect(self.log_list)
        x = threading.Thread(target=self.run)
        x.start()

    def initialize_connection(self, conn):
        # connection is authorized once the client requests coils 7, 77, 777 and 7777 to be turned ON
        # after receiving a write_single_coil operation, the server simply echoes back the packet
        # first coil(pin) to check is 7
        current_pin = 7
        while self.awaiting_pin:
            # print("Am here")
            initial_data = conn.recv(1024)
            unpacked_data = struct.unpack('12B', initial_data)
            coil_addr = unpacked_data[8] * 256 + unpacked_data[9]
            function_code = unpacked_data[7]
            if unpacked_data[10] == 255:
                state = 1
            else:
                state = 0
            if current_pin == coil_addr and function_code == 5 and state == 1:
                self.coils[coil_addr] = 1
                conn.sendall(initial_data)
                # calculating the next pin(coil) to check
                current_pin = current_pin * 10 + 7
            if self.coils[7] and self.coils[77] and self.coils[777] and self.coils[7777]:
                self.awaiting_pin = False
                self.established_connection = True
                self.afterconn()

    def write_status(self, message):
        self.msglist.append(message)

    def afterconn(self):
        if self.established_connection:
            self.write_status("(" + str(datetime.now().strftime("%H:%M:%S")) +
                              ")Connection established: " + str(self.established_connection))
            self.ui.statusbar.showMessage(self.msglist[-1])
            self.ui.led.value = True

    def log_list(self):
        for msg in self.msglist:
            logging.info(msg)

    def set_tables(self):
        idx = ind = 0
        self.ui.tcoils.setRowCount(30)
        for row in self.coils:
            if row == 0:
                ind += 1
            else:
                self.ui.tcoils.setItem(idx, 0, QtWidgets.QTableWidgetItem(str(ind)))
                self.ui.tcoils.setItem(idx, 1, QtWidgets.QTableWidgetItem(str(row)))
                idx += 1
                ind += 1
        idx = ind = 0
        self.ui.tdinp.setRowCount(30)
        for row in self.discrete_inputs:
            if row == 0:
                ind += 1
            else:
                self.ui.tdinp.setItem(idx, 0, QtWidgets.QTableWidgetItem(str(ind + 10000)))
                self.ui.tdinp.setItem(idx, 1, QtWidgets.QTableWidgetItem(str(row)))
                idx += 1
                ind += 1

        idx = ind = 0
        self.ui.tinreg_2.setRowCount(30)
        for row in self.input_registers:
            if row == 0:
                ind += 1
            else:
                self.ui.tinreg_2.setItem(idx, 0, QtWidgets.QTableWidgetItem(str(ind + 30000)))
                self.ui.tinreg_2.setItem(idx, 1, QtWidgets.QTableWidgetItem(str(row)))
                idx += 1
                ind += 1
        idx = ind = 0
        self.ui.tholreg.setRowCount(30)
        for row in self.holding_registers:
            if row == 0:
                ind += 1
            else:
                self.ui.tholreg.setItem(idx, 0, QtWidgets.QTableWidgetItem(str(ind + 40000)))
                self.ui.tholreg.setItem(idx, 1, QtWidgets.QTableWidgetItem(str(row)))
                idx += 1
                ind += 1

    # this function is started by a different thread once a connection has been established
    # it simply updates the OS resources mapped to all the different data structures of the Modbus Server
    # every 0.5 seconds

    def update_info(self):
        # mapping the whole and the fractionary part of the cpu percent to the 1st and 2nd input registers
        frac, whole = math.modf(psutil.cpu_percent(interval=0.1))
        self.input_registers[1] = whole
        self.input_registers[2] = int(frac * 100)

        # mapping the whole and fractionary part of the memory usage (in %) to the 1st and 2nd holding registers
        frac, whole = math.modf(psutil.virtual_memory()[2])
        self.holding_registers[1] = whole
        self.holding_registers[2] = int(frac * 100)

        # mapping the whole and fractionary part of disk usage (in %) to the 11th and 12th holding registers
        frac, whole = math.modf(psutil.disk_usage('/')[3])
        self.holding_registers[11] = whole
        self.holding_registers[12] = int(frac * 100)

        self.set_tables()

    # error functions
    def except_illegal_function(self, pack):
        fc = pack[7]
        if fc in [1, 2, 3, 4, 5, 6, 15, 16]:
            return None
        else:
            packet = struct.pack('13B', pack[0], pack[1], pack[2], pack[3], pack[4], 0x07, pack[6],
                                 (fc + 128), 0x01, 0x00, 0x00, 0x00, 0x00)
            return packet

    def except_illegal_data_address(self, pack):
        fc = pack[7]
        if fc in [1, 2, 3, 4, 15, 16]:
            start = pack[8] * 256 + pack[9]
            number = pack[10] * 256 + pack[11]
            if (1 <= start <= 10000) and (1 <= (start + number - 1) <= 10000):
                return None
            else:
                packet = struct.pack('13B', pack[0], pack[1], pack[2], pack[3], pack[4], 0x07, pack[6],
                                     (fc + 128), 0x02, 0x00, 0x00, 0x00, 0x00)
                return packet
        if fc in [5, 6]:
            start = pack[8] * 256 + pack[9]
            if 1 <= start < 10000:
                return None
            else:
                packet = struct.pack('13B', pack[0], pack[1], pack[2], pack[3], pack[4], 0x07, pack[6],
                                     (fc + 128), 0x02, 0x00, 0x00, 0x00, 0x00)
                return packet

    def except_illegal_data_value(self, pack):
        fc = pack[7]
        if fc in [1, 2, 3, 4]:
            number = pack[10] * 256 + pack[11]
            if 1 <= number <= 255:
                return None
            else:
                packet = struct.pack('13B', pack[0], pack[1], pack[2], pack[3], pack[4], 0x07, pack[6],
                                     (fc + 128), 0x03, 0x00, 0x00, 0x00, 0x00)
                return packet

    def except_slave_device_failure(self, pack):
        fc = pack[7]
        if not self.slave_failure:
            return None
        else:
            packet = struct.pack('13B', pack[0], pack[1], pack[2], pack[3], pack[4], 0x03, pack[6],
                                 (fc + 128), 0x04, 0x00, 0x00, 0x00, 0x00)
            return packet

    def except_slave_device_busy(self, pack):
        fc = pack[7]
        if not self.slave_busy:
            return None
        else:
            packet = struct.pack('13B', pack[0], pack[1], pack[2], pack[3], pack[4], 0x03, pack[6],
                                 (fc + 128), 0x06, 0x00, 0x00, 0x00, 0x00)
            return packet

    def pack_verify(self, pack):
        err1 = self.except_illegal_function(pack)
        if err1 is not None:
            return err1
        err2 = self.except_illegal_data_address(pack)
        if err2 is not None:
            return err2
        err3 = self.except_illegal_data_value(pack)
        if err3 is not None:
            return err3
        err4 = self.except_slave_device_failure(pack)
        if err4 is not None:
            return err4
        err6 = self.except_slave_device_busy(pack)
        if err6 is not None:
            return err6
        return None

    def run(self):
        self.tcp_socket.bind((self.tcp_ip, self.tcp_port))
        self.tcp_socket.listen()
        self.conn, self.addr = self.tcp_socket.accept()
        with self.conn:
            self.write_status("(" + str(datetime.now().strftime("%H:%M:%S")) +
                              ")Connected by" + str(self.addr))
            self.ui.statusbar.showMessage(self.msglist[-1])
            self.initialize_connection(self.conn)
            while True:
                self.update_info()
                initial_data = self.conn.recv(1024)
                unpacked_data = struct.unpack('12B', initial_data)
                exception = self.pack_verify(unpacked_data)
                self.write_status("(" + str(datetime.now().strftime("%H:%M:%S")) +
                                  ")Received " + str(unpacked_data))
                if exception is None:
                    function_code = unpacked_data[7]
                    if function_code == 3:
                        # reading holding registers, need to echo back
                        starting_register = unpacked_data[8] * 256 + unpacked_data[9]
                        no_of_registers = unpacked_data[10] * 256 + unpacked_data[11]
                        # currently hard-coded 13 bytes packets, might require refactoring
                        packet = struct.pack('13B', unpacked_data[0], unpacked_data[1], unpacked_data[2],
                                             unpacked_data[3],
                                             unpacked_data[4], unpacked_data[5], unpacked_data[6], function_code,
                                             int(no_of_registers * 2), 0x00,
                                             int(self.holding_registers[starting_register]), 0x00,
                                             int(self.holding_registers[starting_register + no_of_registers - 1]))

                        self.conn.sendall(packet)
                        self.write_status("(" + str(datetime.now().strftime("%H:%M:%S")) +
                                          ")Sent " + str(struct.unpack('13B', packet)))
                    elif function_code == 4:
                        # reading input registers, need to echo back
                        starting_register = unpacked_data[8] * 256 + unpacked_data[9]
                        no_of_registers = unpacked_data[10] * 256 + unpacked_data[11]

                        packet = struct.pack('13B', unpacked_data[0], unpacked_data[1], unpacked_data[2],
                                             unpacked_data[3],
                                             unpacked_data[4], unpacked_data[5], unpacked_data[6], function_code,
                                             int(no_of_registers * 2), 0x00,
                                             int(self.input_registers[starting_register]), 0x00,
                                             int(self.input_registers[starting_register + no_of_registers - 1]))

                        self.conn.sendall(packet)
                        self.write_status("(" + str(datetime.now().strftime("%H:%M:%S")) +
                                          ")Sent " + str(struct.unpack('13B', packet)))
                    elif function_code == 5:
                        self.conn.sendall(initial_data)
                        self.write_status("(" + str(datetime.now().strftime("%H:%M:%S")) +
                                          ")Sent " + str(struct.unpack('13B', packet)))

                else:
                    self.conn.sendall(exception)
                    self.write_status("(" + str(datetime.now().strftime("%H:%M:%S")) +
                                      ")Exception " + str(struct.unpack('13B', packet)))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ms = Modbus_S()
    sys.exit(app.exec_())
