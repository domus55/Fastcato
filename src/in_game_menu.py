from enum import Enum

import pygame

from src import game_info, level_manager, main_menu, screen
from src.project_common import PATH, loadImage
from src.result import Result


class InGameMenu:
    class State(Enum):
        CLOSED = 0
        OPEN = 1

    state = State.CLOSED
    SCALE = game_info.GameInfo.HUD_SCALE

    DEFAULT = loadImage(f"{PATH}images/gui/inGameMenu/default.png", (400 * SCALE, 405 * SCALE))
    RESUME = loadImage(f"{PATH}images/gui/inGameMenu/resumeActive.png", (400 * SCALE, 405 * SCALE))
    RESTART = loadImage(f"{PATH}images/gui/inGameMenu/restartActive.png", (400 * SCALE, 405 * SCALE))
    EXIT = loadImage(f"{PATH}images/gui/inGameMenu/exitActive.png", (400 * SCALE, 405 * SCALE))

    hitboxResume = pygame.Rect(800 - 167 * SCALE, 450 - 170 * SCALE, 335 * SCALE, 96 * SCALE)
    hitboxRestart = pygame.Rect(800 - 167 * SCALE, 450 - 49 * SCALE, 335 * SCALE, 96 * SCALE)
    hitboxExit = pygame.Rect(800 - 167 * SCALE, 450 + 72 * SCALE, 335 * SCALE, 96 * SCALE)

    image = DEFAULT

    @staticmethod
    def open():
        if Result.state is Result.State.OPEN:
            return
        InGameMenu.state = InGameMenu.State.CLOSED if InGameMenu.state is InGameMenu.State.OPEN else InGameMenu.State.OPEN
        main_menu.MainMenu.SOUND_CLICK.set_volume(game_info.GameInfo.getSound())

    @staticmethod
    def update(keyPressed):
        if keyPressed[pygame.K_r]:
            level_manager.LevelManager.restartLevel()
            InGameMenu.state = InGameMenu.State.CLOSED

    @staticmethod
    def render():
        screen.screen.blit(InGameMenu.image, (800 - 200 * InGameMenu.SCALE, 450 - 203 * InGameMenu.SCALE))
        #pygame.draw.rect(Screen.screen, (255, 0, 0), InGameMenu.hitboxResume)

    @staticmethod
    def mouseButtonDown():
        if InGameMenu.state == InGameMenu.State.OPEN:
            mousePos = pygame.mouse.get_pos()

            if InGameMenu.hitboxResume.collidepoint(mousePos):
                InGameMenu.image = InGameMenu.RESUME
                main_menu.MainMenu.SOUND_CLICK.play()
            elif InGameMenu.hitboxRestart.collidepoint(mousePos):
                InGameMenu.image = InGameMenu.RESTART
                main_menu.MainMenu.SOUND_CLICK.play()
            elif InGameMenu.hitboxExit.collidepoint(mousePos):
                InGameMenu.image = InGameMenu.EXIT
                main_menu.MainMenu.SOUND_CLICK.play()

    @staticmethod
    def mouseButtonUp():
        if InGameMenu.state == InGameMenu.State.OPEN:
            mousePos = pygame.mouse.get_pos()

            if InGameMenu.hitboxResume.collidepoint(mousePos) and InGameMenu.image == InGameMenu.RESUME:
                InGameMenu.state = InGameMenu.State.CLOSED
            elif (InGameMenu.hitboxRestart.collidepoint(mousePos) and
                  InGameMenu.image == InGameMenu.RESTART and
                  level_manager.LevelManager.currentLevel != 7):
                level_manager.LevelManager.restartLevel()
                InGameMenu.state = InGameMenu.State.CLOSED
            elif InGameMenu.hitboxExit.collidepoint(mousePos) and InGameMenu.image == InGameMenu.EXIT:
                main_menu.MainMenu.open()
                InGameMenu.state = InGameMenu.State.CLOSED

            InGameMenu.image = InGameMenu.DEFAULT
