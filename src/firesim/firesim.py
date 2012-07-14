import numpy as np

from kivy.support import install_twisted_reactor
install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from simserver import SimServerFactory
from simwindow import SimGUI


class FireSim:

    def __init__(self, numLights=64):
        self.numLights = numLights
        self.lights = np.zeros((numLights, 3), dtype=int)
        #self.gui = SimWindow(self)

    def guiTick(self):
        pass


if __name__ == '__main__':
    install_twisted_reactor()
    sim = FireSim()

    reactor.listenTCP(5200, SimServerFactory(sim))

    SimGUI(sim).run()

    tick = LoopingCall(sim.guiTick)
    tick.start(1.0 / 30.0)

    print "Exiting"
