import pygame
from Player import *
from Screen import *
import LevelManager
from Camera import *
import InnerTimer


class Game:
    isRunning = True
    keyPressed = None

    def __init__(self):
        self._maxFps = 60
        self._clock = clock = pygame.time.Clock()
        self.lvlManager = LevelManager.LevelManager()

    def update(self):
        InnerTimer.Timer.update()
        screenUpdate()
        self.lvlManager.player.update(Game.keyPressed)
        Camera.update(self.lvlManager.player) #must be after player update


    def render(self):
        screen.fill((0, 0, 0))
        self.lvlManager.player.render()
        Block.Block.renderAll()
        screenRender()


    def delay(self):
        self._clock.tick(self._maxFps)


    def exit(self):
        pygame.quit()
