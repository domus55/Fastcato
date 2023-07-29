from enum import Enum
import pygame

from ProjectCommon import loadImage, PATH
import GameInfo
import LevelManager
import Result
import Screen
import MainMenu


class InGameMenu:
    class State(Enum):
        CLOSED = 0
        OPEN = 1

    state = State.CLOSED
    SCALE = GameInfo.GameInfo.HUD_SCALE

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
        if Result.Result.state is Result.Result.State.OPEN:
            return
        InGameMenu.state = InGameMenu.State.CLOSED if InGameMenu.state is InGameMenu.State.OPEN else InGameMenu.State.OPEN
        MainMenu.MainMenu.SOUND_CLICK.set_volume(GameInfo.GameInfo.getSound())

    @staticmethod
    def update(keyPressed):
        if keyPressed[pygame.K_r]:
            LevelManager.LevelManager.restartLevel()
            InGameMenu.state = InGameMenu.State.CLOSED

    @staticmethod
    def render():
        Screen.screen.blit(InGameMenu.image, (800 - 200 * InGameMenu.SCALE, 450 - 203 * InGameMenu.SCALE))
        #pygame.draw.rect(Screen.screen, (255, 0, 0), InGameMenu.hitboxResume)

    @staticmethod
    def mouseButtonDown():
        if InGameMenu.state == InGameMenu.State.OPEN:
            mousePos = pygame.mouse.get_pos()

            if InGameMenu.hitboxResume.collidepoint(mousePos):
                InGameMenu.image = InGameMenu.RESUME
                MainMenu.MainMenu.SOUND_CLICK.play()
            elif InGameMenu.hitboxRestart.collidepoint(mousePos):
                InGameMenu.image = InGameMenu.RESTART
                MainMenu.MainMenu.SOUND_CLICK.play()
            elif InGameMenu.hitboxExit.collidepoint(mousePos):
                InGameMenu.image = InGameMenu.EXIT
                MainMenu.MainMenu.SOUND_CLICK.play()

    @staticmethod
    def mouseButtonUp():
        if InGameMenu.state == InGameMenu.State.OPEN:
            mousePos = pygame.mouse.get_pos()

            if InGameMenu.hitboxResume.collidepoint(mousePos) and InGameMenu.image == InGameMenu.RESUME:
                InGameMenu.state = InGameMenu.State.CLOSED
            elif InGameMenu.hitboxRestart.collidepoint(mousePos) and InGameMenu.image == InGameMenu.RESTART and LevelManager.LevelManager.currentLevel != 7:
                LevelManager.LevelManager.restartLevel()
                InGameMenu.state = InGameMenu.State.CLOSED
            elif InGameMenu.hitboxExit.collidepoint(mousePos) and InGameMenu.image == InGameMenu.EXIT:
                MainMenu.MainMenu.open()
                InGameMenu.state = InGameMenu.State.CLOSED

            InGameMenu.image = InGameMenu.DEFAULT
