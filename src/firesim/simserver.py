import SocketServer
import struct
import threading
from Queue import Queue

from lib.tcpmessage import TCPMessage


# TODO: Find a way to not have this global
global_sim_queue = Queue()


class SimSocketServer(SocketServer.BaseRequestHandler):

        def handle(self):
            print "SimServer handling request"
            len_buf = self.read(self.request, 2)
            msg_len = struct.unpack("!H", len_buf)[0]

            data = self.read(self.request, msg_len).strip()
            m = TCPMessage()
            m.decode(data)
            # TODO: Is infinite blocking the best behavior?
            global_sim_queue.put(m, block=True, timeout=None)

        def read(self, socket, length):
            buf = ""
            while length > 0:
                data = socket.recv(length)
                if data == "":
                    raise RuntimeError("Connection closed!")
                buf += data
                length -= len(data)
            return buf


class SimServer(threading.Thread):

    def __init__(self, ip_addr="127.0.0.1", port=5200):
        threading.Thread.__init__(self)
        self.conn = None
        self.ip_addr = ip_addr
        self.port = port
        self.exit_flag = False
        self.server = None

    def get_queue(self):
        global global_sim_queue
        return global_sim_queue

    def run(self):
        print "SimServer starting up..."
        self.server = SocketServer.TCPServer((self.ip_addr, self.port), SimSocketServer)
        self.server.serve_forever()

    def stop(self):
        print "SimServer stopping..."
        self.server.shutdown()
