import os
import sys
import colorsys

import pygame
from pygame.locals import *
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from lib.worldloader import WorldLoader
from simserver import SimServerFactory
from settings import FireSimSettings


sim = None
world = None


class FireSim:

    def __init__(self, settings_file=None):
        self.world = None
        self.settings = FireSimSettings(settings_file)
        self.config = self.settings.config

        self.colorshift = 0.0
        self.render_surfaces = {}
        self.positions = {}
        self.sc = None
        self.width = -1
        self.height = -1

    def setup(self):
        (self.width, self.height) = self.world.surfaces[0].dimensions
        self.sc = pygame.Surface((self.width, self.height))

    def redraw(self):
        strands = self.world.surfaces[0].strands
        for strand in strands:

            for fixture in strand.fixtures:

                (bbox_x, bbox_y) = fixture.type.boundbox

                ts = pygame.Surface((bbox_x, bbox_y))
                ts.fill((50, 50, 50))

                np = len(fixture.type.pixel_locations) / 0.5
                n = 0

                for pixel in fixture.type.pixel_locations:
                    (x, y) = pixel.position
                    h = (float(n) / np) + self.colorshift
                    (r, g, b) = map(lambda f: int(255.0 * f), colorsys.hsv_to_rgb(h, 1.0, 1.0))
                    pygame.draw.circle(ts, (r, g, b), (x, y), 1, 0)
                    n += 1

                tlx, tly = fixture.position
                angle = float(fixture.angle)
                scale = float(fixture.scale)

                self.positions[fixture.id] = [tlx, tly, angle, scale]
                self.render_surfaces[fixture.id] = ts
        self.colorshift += 0.0075

    def tick(self):
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            reactor.stop()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                reactor.stop()

        self.redraw()

        for key, s in self.render_surfaces.iteritems():

            s = pygame.transform.rotozoom(s, self.positions[key][2], self.positions[key][3])
            s.set_colorkey((0, 0, 0))
            self.sc.blit(s, (self.positions[key][0], self.positions[key][1]))

        screen.blit(self.sc, self.sc.get_rect())

        clock.tick(30)  # Limit FPS if desired to reduce CPU usage

        pygame.display.set_caption('FireSim - %d fps' % clock.get_fps())
        pygame.display.flip()


if __name__ == '__main__':

    sim = FireSim(os.getcwd() + "\\settings.conf")

    loader = WorldLoader(os.getcwd() + "\\" + sim.config['world'])

    sim.world = loader.load()

    if sim.world is None:
        print "Exiting..."
        sys.exit(1)

    sim.setup()
    pygame.init()

    screen = pygame.display.set_mode((sim.width, sim.height))
    pygame.event.set_allowed([QUIT, KEYDOWN, USEREVENT])

    clock = pygame.time.Clock()

    tickCall = LoopingCall(sim.tick)
    tickCall.start(1.0 / 30.0)

    reactor.listenTCP(sim.config['listen_port'], SimServerFactory(sim))
    reactor.run()
