import pygame

import EventHandler
from CloudManager import CloudManager
from FinishPoint import FinishPoint
from Block import Block
from Camera import Camera
from GameInfo import GameInfo
from InGameMenu import InGameMenu
from InnerTimer import Timer
from LevelManager import LevelManager
from MainMenu import MainMenu
from Music import Music
from Obstacles.ObstacleManager import ObstacleManager
from Player import Player
from Screen import screen, screenRender, screenInitialize
from Background import Background

class Game:
    isRunning = True
    keyPressed = None

    def __init__(self):
        self._maxFps = 10005
        self._clock = clock = pygame.time.Clock()
        GameInfo.load()
        Music.start()
        LevelManager.Initialize()
        screenInitialize()
        CloudManager.initialize()

    def update(self):
        Timer.update()
        #Timer.showFps()
        EventHandler.update()
        if MainMenu.isOpen:
            MainMenu.update()
        elif InGameMenu.isOpen:
            InGameMenu.update(Game.keyPressed)
        else:
            ObstacleManager.updateAll()
            Player.getInstance().update(Game.keyPressed)
            FinishPoint.update()
            Camera.update(Player.getInstance()) #must be called after player update
            Background.getInstance().update()
            CloudManager.update()

    def render(self):
        if MainMenu.isOpen:
            MainMenu.render()
        elif InGameMenu.isOpen:
            InGameMenu.render()
        else:
            Background.getInstance().render()
            Player.getInstance().render()
            ObstacleManager.renderAll()
            FinishPoint.render()
            Block.renderAll()
        screenRender()


    def delay(self):
        self._clock.tick(self._maxFps)


    def exit(self):
        pygame.quit()
