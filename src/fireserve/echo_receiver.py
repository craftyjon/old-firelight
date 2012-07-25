import SocketServer
import struct

from lib.tcpmessage import TCPMessage


class EchoServer(SocketServer.BaseRequestHandler):

    def handle(self):

        # Try to get the message length (2 bytes)

        len_buf = self.read(self.request, 2)
        msg_len = struct.unpack("!H", len_buf)[0]

        data = self.read(self.request, msg_len).strip()
        m = TCPMessage()
        m.decode(data)
        print m

    def read(self, socket, length):
        buf = ""
        while length > 0:
            data = socket.recv(length)
            if data == "":
                raise RuntimeError("Connection closed!")
            buf += data
            length -= len(data)
        return buf


if __name__ == "__main__":

    server = SocketServer.TCPServer(("localhost", 5200), EchoServer)
    server.serve_forever()
