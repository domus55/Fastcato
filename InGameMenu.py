from enum import Enum
import pygame

import GameInfo
import LevelManager
import Screen
import MainMenu


class InGameMenu:
    class State(Enum):
        closed = 0
        open = 1

    state = State.closed

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
        InGameMenu.state = InGameMenu.State.closed if InGameMenu.state is InGameMenu.State.open else InGameMenu.State.open
        MainMenu.MainMenu.SOUND_CLICK.set_volume(GameInfo.GameInfo.getSound())

    @staticmethod
    def update(keyPressed):
        if keyPressed[pygame.K_r]:
            LevelManager.LevelManager.restartLevel()
            InGameMenu.state = InGameMenu.State.closed

    @staticmethod
    def render():
        Screen.screen.blit(InGameMenu.image, (600, 247))

    @staticmethod
    def mouseButtonDown():
        if InGameMenu.state == InGameMenu.State.open:
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
        if InGameMenu.state == InGameMenu.State.open:
            mousePos = pygame.mouse.get_pos()

            if InGameMenu.hitboxResume.collidepoint(mousePos) and InGameMenu.image == InGameMenu.RESUME:
                InGameMenu.state = InGameMenu.State.closed
            elif InGameMenu.hitboxRestart.collidepoint(mousePos) and InGameMenu.image == InGameMenu.RESTART:
                LevelManager.LevelManager.restartLevel()
                InGameMenu.state = InGameMenu.State.closed
            elif InGameMenu.hitboxExit.collidepoint(mousePos) and InGameMenu.image == InGameMenu.EXIT:
                MainMenu.MainMenu.open()
                InGameMenu.state = InGameMenu.State.closed

            InGameMenu.image = InGameMenu.DEFAULT