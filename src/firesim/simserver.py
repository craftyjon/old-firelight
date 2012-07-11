from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver


class SimServer(LineReceiver):

    def __init__(self, simObject):
        self.simObject = simObject
        print "SimServer created"

    def connectionMade(self):
        print "Connection opened"

    def connectionLost(self, reason):
        print "Connection closed"

    def lineReceived(self, data):
        self.handle_command(data)

    def handle_command(self, data):
        cmd = ord(data[0])
        if cmd == 0x41:
            self.sendLine(chr(self.simObject.numLights))


class SimServerFactory(Factory):

    def __init__(self, simObject):
        self.simObject = simObject

    def buildProtocol(self, addr):
        return SimServer(self.simObject)
