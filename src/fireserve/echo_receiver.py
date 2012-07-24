import SocketServer

from lib.util import deserialize


class EchoServer(SocketServer.BaseRequestHandler):

    def handle(self):

        self.data = self.request.recv(8192).strip()
        print deserialize(self.data)
        #self.request.sendall(self.data)


if __name__ == "__main__":

    server = SocketServer.TCPServer(("localhost", 5200), EchoServer)
    server.serve_forever()
