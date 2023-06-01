import pygame

import EventHandler
from BirdCounter import BirdCounter
from Buttons import Buttons
from CloudManager import CloudManager
from Deadline import Deadline
from Bird import Bird
from Block import Block
from Camera import Camera
from Decorations import Decorations
from GameInfo import GameInfo
from InGameMenu import InGameMenu
from InnerTimer import InnerTime
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
        LevelManager.initialize()
        screenInitialize()
        CloudManager.initialize()

    def update(self):
        InnerTime.update()
        #Timer.showFps()
        EventHandler.update()
        if MainMenu.state is not MainMenu.state.closed:
            MainMenu.update()
        else:
            if InGameMenu.state == InGameMenu.State.open:
                InGameMenu.update(Game.keyPressed)
            LevelManager.update()
            ObstacleManager.updateAll()
            Player.getInstance().update(Game.keyPressed)
            Bird.updateAll()
            Camera.update(Player.getInstance()) #must be called after player update
            Background.getInstance().update()
            CloudManager.update()
            Deadline.update(Game.keyPressed)

    def render(self):
        if MainMenu.state is not MainMenu.state.closed:
            MainMenu.render()
        else:
            Background.getInstance().render()
            Buttons.renderAll()
            Decorations.renderAll()
            Player.getInstance().render()
            ObstacleManager.renderAll()
            Bird.renderAll()
            Block.renderAll()
            Deadline.render()
            BirdCounter.render()
            if InGameMenu.state == InGameMenu.State.open:
                InGameMenu.render()
        screenRender()


    def delay(self):
        self._clock.tick(self._maxFps)


    def exit(self):
        pygame.quit()
