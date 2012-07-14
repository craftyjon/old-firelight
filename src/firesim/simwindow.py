#import pygame
import math
import numpy as np
from random import randint
#from pygame.locals import *

import kivy
kivy.require('1.0.6')

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty


class SimWindow(FloatLayout):

    label_wid = ObjectProperty()
    info = StringProperty()

    def do_action(self):
        self.label_wid.text = 'My label after button press'
        self.info = 'New info text'


class SimGUI(App):

    def __init__(self, simObject):
        App.__init__(self)
        self.simObject = simObject
#        pygame.init()
#        self.screen = pygame.display.set_mode((480, 480))
#        self.surface = pygame.Surface((480, 480))

        self.lw = int(math.sqrt(self.simObject.numLights))
        self.lh = int((self.simObject.numLights / self.lw) + 0.5)

        self.lightBuffer = np.zeros((self.lw, self.lh, 3), dtype=int)
#        self.lightSurface = pygame.Surface((self.lw, self.lh))
        print "SimWindow created"

    def build(self):
        return SimWindow()

    def tick(self):
#        e = pygame.event.poll()
#        if e.type == pygame.QUIT:
#            return False

        self.update()

#        pygame.surfarray.blit_array(self.lightSurface, self.lightBuffer)
#        self.surface = pygame.transform.smoothscale(self.lightSurface, (480, 480))
#        self.screen.blit(self.surface, self.surface.get_rect())
#        pygame.display.flip()
        return True

    def update(self):
#        rowWidth = int(math.sqrt(self.simObject.numLights))

        for i in range(self.lw):
            for j in range(self.lh):
                el = self.lightBuffer[i][j]
                el[0] = randint(0, 255)
                el[1] = randint(0, 255)
                el[2] = randint(0, 255)
