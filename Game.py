import pygame

from Block import Block
from Camera import Camera
from InnerTimer import Timer
from LevelManager import LevelManager
from Obstacles.ObstacleManager import ObstacleManager
from Screen import screen, screenRender, screenUpdate


class Game:
    isRunning = True
    keyPressed = None

    def __init__(self):
        self._maxFps = 60
        self._clock = clock = pygame.time.Clock()
        LevelManager.Initialize()

    def update(self):
        Timer.update()
        screenUpdate()
        ObstacleManager.updateAll()
        LevelManager.player.update(Game.keyPressed)
        Camera.update(LevelManager.player) #must be after player update


    def render(self):
        screen.fill((0, 0, 0))
        LevelManager.player.render()
        ObstacleManager.renderAll()
        Block.renderAll()
        screenRender()


    def delay(self):
        self._clock.tick(self._maxFps)


    def exit(self):
        pygame.quit()
