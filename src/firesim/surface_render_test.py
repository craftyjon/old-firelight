import pygame
from pygame.locals import *
import sys
import colorsys

from configloader import ConfigLoader


config = None
colorshift = 0.0


def redraw():
    global colorshift, config
    strands = config.surfaces[0].strands
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


if __name__ == '__main__':

    loader = ConfigLoader('test_surface.json')

    config = loader.load()

    if config is None:
        print "Exiting..."
        sys.exit(1)

    (width, height) = config.surfaces[0].dimensions

    pygame.init()

    size = width, height
    screen = pygame.display.set_mode(size)
    pygame.event.set_allowed([QUIT, KEYDOWN, USEREVENT])

    sc = pygame.Surface((width, height))

    render_surfaces = {}
    positions = {}
    clock = pygame.time.Clock()

    while True:

        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            sys.exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                sys.exit(0)

        redraw()

        for key, s in render_surfaces.iteritems():

            s = pygame.transform.rotozoom(s, positions[key][2], positions[key][3])
            s.set_colorkey((0, 0, 0))
            sc.blit(s, (positions[key][0], positions[key][1]))

        screen.blit(sc, sc.get_rect())

        clock.tick(30)  # Limit FPS if desired to reduce CPU usage

        pygame.display.set_caption('FireSim - %d fps' % clock.get_fps())
        pygame.display.flip()
