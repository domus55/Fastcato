import pygame
from Player import *
from Screen import *
from LevelManager import *
import InnerTimer

class Game:
    isRunning = True
    keyPressed = None

    def __init__(self):
        self._maxFps = 300
        self._clock = clock = pygame.time.Clock()
        self.lvlManager = levelManager()

    def update(self):
        InnerTimer.Timer.update()
        screenUpdate()
        self.lvlManager.player.update(Game.keyPressed)
        Camera.update(self.lvlManager.player) #must be after player update


    def render(self):
        screen.fill((0, 0, 0))
        self.lvlManager.player.render()
        screenRender()


    def delay(self):
        self._clock.tick(self._maxFps)


    def exit(self):
        pygame.quit()
