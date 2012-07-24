"""FireServe is the backend server for FireLight"""

import threading
import sys
import time
import colorsys

from lib.util import *
from lib.loopingthread import LoopingThread

from node import Node


n = None
pixels = []
colorshift = 0.0
exit_flag = False


class NodeUpdater(threading.Thread):
    def __init__(self, node_list):
        threading.Thread.__init__(self)
        self.node_list = node_list

    def connect(self):
        for node in self.node_list:
            node.connect()

    def run(self):
        global exit_flag, pixels
        print "nodeupdater run"
        while not exit_flag:
            try:
                self.node_list[0].set_all(pixels)
                #self.conn.send(serialize(pixels))
                time.sleep(1.0 / 1.0)
            except:  # TODO: add specific exceptions
                e = sys.exc_info()[0]
                print "Error sending!", e
                self.connect()
                time.sleep(1.0 / 1.0)

    def stop(self):
        for node in self.node_list:
            node.disconnect()


def rainbow_tick():
    global colorshift, pixels

    print "rainbow tick"

    for i in range(512):
        h = (float(i) / 128) + colorshift
        (r, g, b) = map(lambda f: int(255.0 * f), colorsys.hsv_to_rgb(h, 1.0, 1.0))
        pixels[i] = [r, g, b]

    colorshift += 0.0075


def tick():
    global n, pixels

    rainbow_tick()


if __name__ == "__main__":

    #reactor.listenTCP(5100)
    #reactor.run().

    n = Node(ip_addr="127.0.0.1", port=5200)

    #print "Getting node info..."
    #n.GetNodeInfo()

    #tickCall = LoopingCall(tick)
    #tickCall.start(1.0 / 30.0)

    #reactor.run()
    pixels = [[100, 64, 32] for i in range(24)]

    #updater = NodeUpdater([n])
    #updater.connect()
    #updater.start()

    #rainbow_loop = LoopingThread((1.0 / 2.0), tick)
    #rainbow_loop.start()

    n.connect()
    n.set_all(pixels)
    n.disconnect()
