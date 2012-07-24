"""FireServe is the backend server for FireLight"""

import colorsys
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from lib.util import *

from node import Node

n = None
pixels = []
colorshift = 0.0


def rainbow_tick():
    global colorshift, pixels

    for i in range(512):
        h = (float(i) / 128) + colorshift
        (r, g, b) = map(lambda f: int(255.0 * f), colorsys.hsv_to_rgb(h, 1.0, 1.0))
        pixels[i] = [r, g, b]

    colorshift += 0.0075


def tick():
    global n, pixels
    if n.num_pixels > 0:
        #for pixel in range(512):
        #    pixels[pixel] = [127, 25, 200]
        rainbow_tick()
        n.SetAll(pixels)
    else:
        pixels = [[0, 0, 0] for i in range(512)]


if __name__ == "__main__":

    #reactor.listenTCP(5100)
    #reactor.run().

    n = Node(ip_addr="127.0.0.1", port=5200)

    print "Getting node info..."
    n.GetNodeInfo()

    tickCall = LoopingCall(tick)
    tickCall.start(1.0 / 30.0)

    reactor.run()
