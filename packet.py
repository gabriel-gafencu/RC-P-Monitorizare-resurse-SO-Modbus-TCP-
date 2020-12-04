import struct

class Packet:

    def __init__(self, unit_id, length, function_code, register_id, data):
        self.unit_id = unit_id
        self.function_code = function_code
        self.register_id = register_id
        self.data = data
        self.length = length
        self.packet = struct.pack('12B', 0x00, 0x00, 0x00, 0x00, 0x00, int(self.length), int(self.function_code), 0x00, int(self.register_id), int(self.data))