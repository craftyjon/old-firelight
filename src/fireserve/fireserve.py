"""FireServe is the backend server for FireLight"""

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from lib.util import *

from node import Node

n = None
pixels = []


def demo_preset_tick():
    global colorshift, sim
    strands = sim.config.surfaces[0].strands
    for strand in strands:

        for fixture in strand.fixtures:

            (bbox_x, bbox_y) = fixture.type.boundbox

            ts = pygame.Surface((bbox_x, bbox_y))
            ts.fill((50, 50, 50))

            np = len(fixture.type.pixel_locations) / 0.5
            n = 0

            for pixel in fixture.type.pixel_locations:
                (x, y) = pixel.position
                h = (float(n) / np) + colorshift
                (r, g, b) = map(lambda f: int(255.0 * f), colorsys.hsv_to_rgb(h, 1.0, 1.0))
                n += 1

            tlx, tly = fixture.position
            angle = float(fixture.angle)
            scale = float(fixture.scale)

            positions[fixture.id] = [tlx, tly, angle, scale]
            render_surfaces[fixture.id] = ts
    colorshift += 0.0075


def tick():
    global n, pixels
    if n.num_pixels > 0:
        pixels = [[0, 0, 0] for i in range(512)]
        for pixel in range(512):
            pixels[pixel] = [127, 25, 200]
        n.SetAll(pixels)


if __name__ == "__main__":

    #reactor.listenTCP(5100)
    #reactor.run().

    n = Node(ip_addr="127.0.0.1", port=5200)

    print "Getting node info..."
    n.GetNodeInfo()

    tickCall = LoopingCall(tick)
    tickCall.start(1.0 / 30.0)

    reactor.run()
