import pygame

from src import event_handler
from src.cat_small import CatSmall
from src.credits import Credits
from src.hud.buttons import Buttons
from src.hud.tutorial import Tutorial
from src.icons import Icons
from src.cloud_manager import CloudManager
from src.bird import Bird
from src.block import Block
from src.camera import Camera
from src.decorations import Decorations
from src.game_info import GameInfo, BuildType
from src.hud.bird_counter import BirdCounter
from src.hud.deadline import Deadline
from src.in_game_menu import InGameMenu
from src.inner_timer import InnerTime
from src.level_manager import LevelManager
from src.main_menu import MainMenu
from src.music import Music
from src.obstacles.obstacle_manager import ObstacleManager
from src.player import Player
from src.result import Result
from src.screen import screenRender, screenInitialize
from src.background import Background


class Game:
    isRunning = True
    keyPressed = None
    fingers = {}

    def __init__(self):
        self._maxFps = 60
        self._clock = pygame.time.Clock()
        GameInfo.load()
        Music.start()
        LevelManager.initialize()
        screenInitialize()
        CloudManager.initialize()

    def update(self):
        InnerTime.update()
        # InnerTime.showFps()
        Game.keyPressed = event_handler.update()
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
                Tutorial.render(Game.keyPressed)
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
