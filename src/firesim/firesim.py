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
colorshift = 0.0


class FireSim:

    def __init__(self, settings_file=None):
        self.world = None
        self.settings = FireSimSettings(settings_file)
        self.config = self.settings.config


def redraw():
    global colorshift, sim
    strands = sim.world.surfaces[0].strands
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
                pygame.draw.circle(ts, (r, g, b), (x, y), 1, 0)
                n += 1

            tlx, tly = fixture.position
            angle = float(fixture.angle)
            scale = float(fixture.scale)

            positions[fixture.id] = [tlx, tly, angle, scale]
            render_surfaces[fixture.id] = ts
    colorshift += 0.0075


def tick():
    event = pygame.event.poll()

    if event.type == pygame.QUIT:
        reactor.stop()

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
            reactor.stop()

    redraw()

    for key, s in render_surfaces.iteritems():

        s = pygame.transform.rotozoom(s, positions[key][2], positions[key][3])
        s.set_colorkey((0, 0, 0))
        sc.blit(s, (positions[key][0], positions[key][1]))

    screen.blit(sc, sc.get_rect())

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

    (width, height) = sim.world.surfaces[0].dimensions

    pygame.init()

    size = width, height
    screen = pygame.display.set_mode(size)
    pygame.event.set_allowed([QUIT, KEYDOWN, USEREVENT])

    sc = pygame.Surface((width, height))

    render_surfaces = {}
    positions = {}
    clock = pygame.time.Clock()

    tickCall = LoopingCall(tick)
    tickCall.start(1.0 / 30.0)

    reactor.listenTCP(sim.config['listen_port'], SimServerFactory(sim))
    reactor.run()
