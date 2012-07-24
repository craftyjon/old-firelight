"""TCP protocol for server->node communication"""
import struct


MAX_MESSAGE_LENGTH = 1024   # Bytes


class TCPMessage:
    """
    Container for a TCP message to send or receive.
    Typical message:
        Network byte order (big-endian)
        0x00 0x03           A command of length 0x03 follows
        0x10 0x00 0x03      Command 0x10, data length 0x0003
        0x0A 0x0B 0x0C      Three data bytes
    """

    def __init__(self, command=None, data_length=0, data=[]):
        """Pass in a string to decode (optional)"""
        if command is not None:
            self.command = command
            self.data_length = data_length
            self.data = data
            self.encode()
        else:
            self.message_length = 0
            self.command = 0
            self.data_length = 0
            self.data = []
            self.string = ""

    def serialized(self):
        if self.string == "":
            self.encode()
        return self.string

    def decode(self, string=None):
        if string is not None:
            self.string = string
        if self.string is None:
            return False

        expected_length = len(self.string) - 1
        encoded_length = struct.unpack("!H", self.string[0:2])[0]

        if expected_length != encoded_length:
            print "Error: bad packet header: got %d, expected %d" % (encoded_length, expected_length)
            return False

        self.command = struct.unpack("B", self.string[2:3])[0]
        self.data_length = struct.unpack("!H", self.string[3:5])[0]

        for char in self.string[5:]:
            self.data.append(struct.unpack("B", char)[0])

    def encode(self):
        length = 3 + self.data_length
        self.string = struct.pack("!H", length)
        self.string += struct.pack("!BH", self.command, self.data_length)
        for char in self.data:
            self.string += struct.pack("B", char)
        #self.string += struct.pack("H", 0x0000)

    def __repr__(self):
        s = "Command: 0x%0.2X\tLength: 0x%0.4X\r\n" % (self.command, self.data_length)
        s += "Encoded: "
        for char in self.string:
            s += "0x%0.2X " % ord(char)
        return s


if __name__ == "__main__":
    m = TCPMessage(0x01, 0x03, [0x0A, 0x0B, 0x0C])
    print m
