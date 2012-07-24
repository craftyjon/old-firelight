from twisted.internet import reactor, defer
from twisted.internet.protocol import ClientCreator
from twisted.protocols import amp
from lib.ampcommands import *


class Node:

    def __init__(self, ip_addr="", port=0):
        self.ip_addr = ip_addr
        self.port = port
        self.node_type = ""
        self.num_pixels = 0

    def connect(self):
        pass

    def update(self):
        pass

    def GetNodeInfo(self):

        d = ClientCreator(reactor, amp.AMP).connectTCP(
            self.ip_addr, self.port).addCallback(
                lambda p: p.callRemote(GetNodeInfo))

        def done(result):
            try:
                self.node_type = result[0][1]['node_type']
                self.num_pixels = result[0][1]['num_pixels']
                print "num_pixels: ", self.num_pixels
            except TypeError:
                print "Invalid return from GetNodeInfo", result

        defer.DeferredList([d]).addCallback(done)

    def SetAll(self, pixel_list):

        d = ClientCreator(reactor, amp.AMP).connectTCP(
            self.ip_addr, self.port).addCallback(
                lambda p: p.callRemote(SetAll, values=pixel_list))

        def done(result):
            pass

        defer.DeferredList([d]).addCallback(done)
