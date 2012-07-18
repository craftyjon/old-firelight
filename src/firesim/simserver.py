from twisted.internet.protocol import Factory
from twisted.protocols import amp

from lib.ampcommands import *

SIMULATOR_VERSION = 1
PROTOCOL_VERSION = 1


class SimServerProtocol(amp.AMP):

    def get_node_info(self):
        """Returns information about this node to the server"""
        return {'node_type': 'FireSim',
                'node_version': SIMULATOR_VERSION,
                'protocol_version': PROTOCOL_VERSION,
                'num_lights': self.factory.sim.world.total_pixels}

    GetNodeInfo.responder(get_node_info)


class SimServerFactory(Factory):

    def __init__(self, sim):
        self.sim = sim
        self.protocol = SimServerProtocol
