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

        elif cmd == 0x42:   # Get firmware version
            self.sendLine("Sim")

        elif cmd == 0x43:   # Get protocol version
            self.sendLine(chr(1) + chr(0))

        elif cmd == 0x44:   # Get all lights as array
            pass

        elif cmd == 0x45:   # Set single light
            index = ord(data[1:2])
            r = ord(data[3])
            g = ord(data[4])
            b = ord(data[5])

            self.simObject.lights[index][0] = r
            self.simObject.lights[index][1] = g
            self.simObject.lights[index][2] = b

        elif cmd == 0x46:   # Set all lights to color
            r = ord(data[1])
            g = ord(data[2])
            b = ord(data[3])

            for i in range(self.simObject.numLights):
                self.simObject.lights[i][0] = r
                self.simObject.lights[i][1] = g
                self.simObject.lights[i][2] = b

        elif cmd == 0x47:   # set all lights to array
            pass


class SimServerFactory(Factory):

    def __init__(self, simObject):
        self.simObject = simObject

    def buildProtocol(self, addr):
        return SimServer(self.simObject)
