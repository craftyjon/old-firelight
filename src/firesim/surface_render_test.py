import pygame
from pygame.locals import *
import sys
import json
import colorsys

config_surface = {}
colorshift = 0.0


def redraw():
    global colorshift, config_surface6
    strands = config_surface["strands"]
    for strand in strands:

        for fixture in strand["fixtures"]:

            fixture_type = config_fixture_types[next(index for (index, d) in enumerate(config_fixture_types) if d["name"] == fixture["type"])]
            (bbox_x, bbox_y) = map(int, fixture_type["boundbox"].split(','))

            ts = pygame.Surface((bbox_x, bbox_y))
            ts.fill((50, 50, 50))

            np = len(fixture_type["pixel_locations"]) / 2.0
            n = 0

            for loc in fixture_type["pixel_locations"]:
                x, y = map(int, loc.split(','))
                h = (float(n) / np) + colorshift
                (r, g, b) = map(lambda f: int(255.0 * f), colorsys.hsv_to_rgb(h, 1.0, 1.0))
                pygame.draw.circle(ts, (r, g, b), (x, y), 1, 0)
                n += 1

            tlx, tly = map(int, fixture["tl"].split(','))
            angle = float(fixture["angle"])
            scale = float(fixture["scale"])

            positions[fixture["id"]] = [tlx, tly, angle, scale]
            render_surfaces[fixture["id"]] = ts
    colorshift += 0.016

if __name__ == '__main__':
    json_data = open("test_surface.json")

    data = json.load(json_data)

    config_fixture_types = data.get("fixture_types", None)

    if config_fixture_types is None:
        print "Error: no fixture types found in config file"
        sys.exit(1)

    config_surface = data.get("surface", None)
    if config_surface is None:
        print "Error: no surface found in config file"
        sys.exit(1)

    width, height = map(int, config_surface.get("dimensions", "200,200").split(','))

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
