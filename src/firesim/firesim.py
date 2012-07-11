from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from simserver import *
from simwindow import *


class FireSim:

    def __init__(self, numLights=64):
        self.numLights = numLights
        self.lights = [[0 for i in range(3)] for j in range(numLights)]
        self.gui = SimWindow(self)

    def guiTick(self):
        if not self.gui.tick():
            reactor.stop()


if __name__ == '__main__':
    sim = FireSim()

    tick = LoopingCall(sim.guiTick)
    tick.start(1.0 / 30.0)

    reactor.listenTCP(5200, SimServerFactory(sim))
    reactor.run()

    print "Exiting"
