from enum import Enum
import pygame

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

    DEFAULT = pygame.transform.scale(pygame.image.load("images/gui/inGameMenu/default.png"), (400, 405)).convert_alpha()
    RESUME = pygame.transform.scale(pygame.image.load("images/gui/inGameMenu/resumeActive.png"), (400, 405)).convert_alpha()
    RESTART = pygame.transform.scale(pygame.image.load("images/gui/inGameMenu/restartActive.png"), (400, 405)).convert_alpha()
    EXIT = pygame.transform.scale(pygame.image.load("images/gui/inGameMenu/exitActive.png"), (400, 405)).convert_alpha()

    hitboxResume = pygame.Rect(633, 280, 335, 96)
    hitboxRestart = pygame.Rect(633, 401, 335, 96)
    hitboxExit = pygame.Rect(633, 522, 335, 96)

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
        Screen.screen.blit(InGameMenu.image, (600, 247))

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
