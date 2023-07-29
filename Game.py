import pygame

import EventHandler
from CatSmall import CatSmall
from Credits import Credits
from HUD.Buttons import Buttons
from Icons import Icons
from CloudManager import CloudManager
from Bird import Bird
from Block import Block
from Camera import Camera
from Decorations import Decorations
from GameInfo import GameInfo, BuildType
from HUD.BirdCounter import BirdCounter
from HUD.Deadline import Deadline
from InGameMenu import InGameMenu
from InnerTimer import InnerTime
from LevelManager import LevelManager
from MainMenu import MainMenu
from Music import Music
from Obstacles.ObstacleManager import ObstacleManager
from Player import Player
from Result import Result
from Screen import screenRender, screenInitialize
from Background import Background


class Game:
    isRunning = True
    keyPressed = None
    fingers = {}

    def __init__(self):
        self._maxFps = 104
        self._clock = pygame.time.Clock()
        GameInfo.load()
        Music.start()
        LevelManager.initialize()
        screenInitialize()
        CloudManager.initialize()

    def update(self):
        InnerTime.update()
        #InnerTime.showFps()
        Game.keyPressed = EventHandler.update()
        if GameInfo.BUILD_TYPE == BuildType.ANDROID:
            Buttons.update(Game.fingers)
        if MainMenu.state is not MainMenu.state.CLOSED:
            MainMenu.update()
        else:
            if InGameMenu.state == InGameMenu.State.OPEN:
                InGameMenu.update(Game.keyPressed)
                Game.keyPressed = None
            if Result.state == Result.State.OPEN:
                Game.keyPressed = None
            LevelManager.update()
            ObstacleManager.updateAll()
            Player.getInstance().update(Game.keyPressed)
            CatSmall.getInstance().update()
            Bird.updateAll()
            Camera.update(Player.getInstance())  # must be called after player update
            Background.getInstance().update()
            Deadline.update(Game.keyPressed)

    def render(self):
        if MainMenu.state is not MainMenu.state.CLOSED:
            MainMenu.render()
        else:
            Background.getInstance().render()
            if LevelManager.currentLevel == 7:
                Credits.renderText()
            Block.renderBackground()
            Icons.renderAll()
            Decorations.renderAll()
            Player.getInstance().render()
            CatSmall.getInstance().render()
            ObstacleManager.renderAll()
            Bird.renderAll()
            Block.renderBlocks()
            if LevelManager.currentLevel == 7:
                Credits.renderFade()
            if Result.state == Result.State.CLOSED:
                Deadline.render()
                BirdCounter.render()
                if InGameMenu.state == InGameMenu.State.CLOSED and GameInfo.BUILD_TYPE == BuildType.ANDROID:
                    Buttons.render()
            if InGameMenu.state == InGameMenu.State.OPEN:
                InGameMenu.render()
            elif Result.state == Result.State.OPEN:
                Result.render()
        screenRender()

    def delay(self):
        self._clock.tick(self._maxFps)

    def exit(self):
        pygame.quit()
