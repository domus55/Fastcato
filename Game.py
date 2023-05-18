import pygame

from FinishPoint import FinishPoint
from Block import Block
from Camera import Camera
from InnerTimer import Timer
from LevelManager import LevelManager
from Obstacles.ObstacleManager import ObstacleManager
from Player import Player
from Screen import screen, screenRender, screenUpdate
from Background import Background

class Game:
    isRunning = True
    keyPressed = None

    def __init__(self):
        self._maxFps = 10003
        self._clock = clock = pygame.time.Clock()
        Player.instance = Player()
        LevelManager.Initialize()

    def update(self):
        Timer.update()
        Timer.showFps()
        screenUpdate()
        ObstacleManager.updateAll()
        Player.instance.update(Game.keyPressed)
        FinishPoint.update()
        Camera.update(Player.instance) #must be after player update
        Background.getInstance().update()


    def render(self):
        screen.fill((0, 0, 0))
        Background.getInstance().render()
        Player.instance.render()
        ObstacleManager.renderAll()
        FinishPoint.render()
        Block.renderAll()
        screenRender()


    def delay(self):
        self._clock.tick(self._maxFps)


    def exit(self):
        pygame.quit()
