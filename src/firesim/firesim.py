import os
import sys
import signal
import Queue
import pygame
from pygame.locals import *

from lib.worldloader import WorldLoader
from lib.loopingthread import LoopingThread
from lib.tcpcommands import *

from settings import FireSimSettings
from simserver import SimServer


global_sim_queue = None
server = None
tick_loop = None


class FireSim:

    def __init__(self, settings_file=None):
        self.world = None
        self.settings = FireSimSettings(settings_file)
        if self.settings:
            self.config = self.settings.config
        else:
            self.config = None

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
        font = pygame.font.SysFont(None, 11)
        for strand in strands:

            for idx, fixture in enumerate(strand.fixtures):

                (bbox_x, bbox_y) = fixture.type.boundbox

                ts = pygame.Surface((bbox_x, bbox_y))
                cs = pygame.Surface((bbox_x, bbox_y + 10))
                ts.fill((50, 50, 50))
                pygame.draw.line(ts, (255, 255, 255), (0, 0), (0, bbox_y))

                for pixel in fixture.type.pixels:
                    (x, y) = pixel.position
                    (r, g, b) = pixel.get()
                    pygame.draw.circle(ts, (r, g, b), (x, y), 1, 0)

                tlx, tly = fixture.position
                angle = float(fixture.angle)
                scale = float(fixture.scale)

                text = font.render("%d" % idx, True, (255, 255, 255), (0, 0, 0))
                r = text.get_rect()
                r.centery = bbox_y + 5
                r.centerx = bbox_x / 2

                cs.blit(ts, ts.get_rect())
                cs.blit(text, r)

                self.positions[fixture.id] = [tlx, tly, angle, scale]
                self.render_surfaces[fixture.id] = cs

    def tick(self):
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            self.shutdown()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                self.shutdown()

        try:
            message = global_sim_queue.get(False)
            self.process_message(message)
        except Queue.Empty:
            pass

        self.redraw()

        for key, s in self.render_surfaces.iteritems():

            s = pygame.transform.rotozoom(s, self.positions[key][2], self.positions[key][3])
            s.set_colorkey((0, 0, 0))
            self.sc.blit(s, (self.positions[key][0], self.positions[key][1]))

        screen.blit(self.sc, self.sc.get_rect())

        clock.tick(30)  # Limit FPS if desired to reduce CPU usage

        pygame.display.set_caption('FireSim - %d fps' % clock.get_fps())
        pygame.display.flip()

    def shutdown(self):
        global server, tick_loop
        if server:
            server.stop()
        tick_loop.stop()
        sys.exit(0)

    def process_message(self, message):
        """Processes an incoming TCPMessage"""
        #print "Command: 0x%0.2X\tDataLength: 0x%0.4X\r\n" % (message.command, message.data_length)

        if message.command == CMD_SET_ALL:
            if (message.data_length % 3) != 0:
                print "Error: bad data length: must be multiple of 3"
                return

            processed_data = []
            for x in range(len(message.data) / 3):
                tl = [message.data[3 * x], message.data[(3 * x) + 1], message.data[(3 * x) + 2]]
                processed_data.append(tl)

            #print "Got %d pixels" % len(processed_data)

            strand = self.world.surfaces[0].strands[0]
            strand.set_all(processed_data)


def signal_handler(signum, frame):
    global updater, tick_loop
    print "Caught signal, exiting..."
    if server:
        server.stop()
    if tick_loop:
        tick_loop.stop()
    sys.exit(0)


if __name__ == '__main__':

    sim = FireSim(os.getcwd() + "/settings.conf")

    loader = WorldLoader(os.getcwd() + "/" + sim.config['world'])

    sim.world = loader.load()

    if sim.world is None:
        print "No world loaded. Exiting..."
        sys.exit(1)

    sim.setup()
    pygame.init()

    screen = pygame.display.set_mode((sim.width, sim.height))
    pygame.event.set_allowed([QUIT, KEYDOWN, USEREVENT])

    clock = pygame.time.Clock()
    signal.signal(signal.SIGINT, signal_handler)

    server = SimServer(sim.config['listen_addr'], sim.config['listen_port'])
    global_sim_queue = server.get_queue()
    server.start()

    tick_loop = LoopingThread((1.0 / 40.0), sim.tick)
    tick_loop.run()
