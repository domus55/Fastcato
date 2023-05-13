import pygame
from Player import *
from Screen import *

class Game:
    isRunning = True

    def __init__(self):
        self._maxFps = 300
        self._clock = clock = pygame.time.Clock()

    def update(self):
        screenUpdate()



    def render(self):
        p = Player()
        p.render()

        screenRender()


    def delay(self):
        self._clock.tick(self._maxFps)


    def exit(self):
        pygame.quit()