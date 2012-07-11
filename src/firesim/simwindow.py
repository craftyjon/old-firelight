import pygame
import math
import numpy as np
from random import randint
from pygame.locals import *


class SimWindow:

    def __init__(self, simObject):
        self.simObject = simObject
        pygame.init()
        self.screen = pygame.display.set_mode((480, 480))
        self.surface = pygame.Surface((480, 480))

        self.lw = int(math.sqrt(self.simObject.numLights))
        self.lh = int((self.simObject.numLights / self.lw) + 0.5)

        self.lightBuffer = np.zeros((self.lw, self.lh, 3), dtype=int)
        self.lightSurface = pygame.Surface((self.lw, self.lh))
        print "SimWindow created"

    def tick(self):
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            return False

        self.update()

        pygame.surfarray.blit_array(self.lightSurface, self.lightBuffer)
        self.surface = pygame.transform.smoothscale(self.lightSurface, (480, 480))
        self.screen.blit(self.surface, self.surface.get_rect())
        pygame.display.flip()
        return True

    def update(self):
        rowWidth = int(math.sqrt(self.simObject.numLights))

        for i in range(self.lw):
            for j in range(self.lh):
                el = self.lightBuffer[i][j]
                el[0] = randint(0, 255)
                el[1] = randint(0, 255)
                el[2] = randint(0, 255)
