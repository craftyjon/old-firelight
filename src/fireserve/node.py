import socket
import struct

from lib.tcpmessage import TCPMessage, MAX_MESSAGE_LENGTH
from lib.tcpcommands import *


class Node:

    def __init__(self, ip_addr="", port=0):
        self.ip_addr = ip_addr
        self.port = port
        self.node_type = ""
        self.num_pixels = 512
        self.conn = None

    def connect(self):
        if self.conn is None:
            try:
                self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.conn.connect((self.ip_addr, self.port))
            except socket.error:
                self.conn = None
                print "Node connection failed: " + self.ip_addr + ":" + str(self.port)
                return False
        #else:
            #self.disconnect()
            #return self.connect()
        return True

    def disconnect(self):
        if self.conn:
            #self.conn.shutdown()
            self.conn.close()

    def set_all(self, pixels):
        messages = []
        flat_pixels = [item for sublist in pixels for item in sublist]

        max_array_length = MAX_MESSAGE_LENGTH - 10

        if len(flat_pixels) < max_array_length:
            m = TCPMessage(CMD_SET_ALL, len(flat_pixels), flat_pixels)
            messages.append(m)

        else:
            offset = 0
            while (len(flat_pixels) - offset) > 0:
                sublist = flat_pixels[offset:(offset + max_array_length)]
                (a, b) = struct.unpack("BB", struct.pack("!H", offset))
                sublist.insert(0, b)
                sublist.insert(0, a)

                m = TCPMessage(CMD_SET, len(sublist), sublist)
                messages.append(m)
                offset += max_array_length

        for message in messages:
            totalsent = 0
            buf = message.serialized()
            len_str = struct.pack("!H", len(buf))
            self.conn.send(len_str)
            while totalsent < len(buf):
                sent = self.conn.send(buf[totalsent:])
                if sent == 0:
                    print "Error while sending"
                totalsent += sent


if __name__ == "__main__":
    n = Node('127.0.0.1', 5200)
    pix = [[126, 50, 210] for i in range(32)]
    n.set_all(pix)
