import pygame

import CloudManager
import Game
import GameInfo
import LevelManager
import Screen
from MainMenu import MainMenu


class InGameMenu:
    isOpen = False

    DEFAULT = pygame.transform.scale(pygame.image.load("images/gui/inGameMenu/default.png"), (400, 405)).convert_alpha()
    RESUME = pygame.transform.scale(pygame.image.load("images/gui/inGameMenu/resumeActive.png"), (400, 405)).convert_alpha()
    RESTART = pygame.transform.scale(pygame.image.load("images/gui/inGameMenu/restartActive.png"), (400, 405)).convert_alpha()
    EXIT = pygame.transform.scale(pygame.image.load("images/gui/inGameMenu/exitActive.png"), (400, 405)).convert_alpha()

    CLICK_SOUND = pygame.mixer.Sound("sounds/click.wav")

    hitboxResume = pygame.Rect(633, 280, 335, 96)
    hitboxRestart = pygame.Rect(633, 401, 335, 96)
    hitboxExit = pygame.Rect(633, 522, 335, 96)

    image = DEFAULT

    @staticmethod
    def open():
        InGameMenu.isOpen = not InGameMenu.isOpen
        MainMenu.CLICK_SOUND.set_volume(GameInfo.GameInfo.getSound())

    @staticmethod
    def update(keyPressed):
        if keyPressed[pygame.K_r]:
            LevelManager.LevelManager.restartLevel()
            InGameMenu.isOpen = False

    @staticmethod
    def render():
        Screen.screen.blit(InGameMenu.image, (600, 247))

    @staticmethod
    def mouseButtonDown():
        if InGameMenu.isOpen:
            mousePos = pygame.mouse.get_pos()

            if InGameMenu.hitboxResume.collidepoint(mousePos):
                InGameMenu.image = InGameMenu.RESUME
                MainMenu.CLICK_SOUND.play()
            elif InGameMenu.hitboxRestart.collidepoint(mousePos):
                InGameMenu.image = InGameMenu.RESTART
                MainMenu.CLICK_SOUND.play()
            elif InGameMenu.hitboxExit.collidepoint(mousePos):
                InGameMenu.image = InGameMenu.EXIT
                MainMenu.CLICK_SOUND.play()

    @staticmethod
    def mouseButtonUp():
        if InGameMenu.isOpen:
            mousePos = pygame.mouse.get_pos()

            if InGameMenu.hitboxResume.collidepoint(mousePos) and InGameMenu.image == InGameMenu.RESUME:
                InGameMenu.isOpen = False
            elif InGameMenu.hitboxRestart.collidepoint(mousePos) and InGameMenu.image == InGameMenu.RESTART:
                LevelManager.LevelManager.restartLevel()
                InGameMenu.isOpen = False
            elif InGameMenu.hitboxExit.collidepoint(mousePos) and InGameMenu.image == InGameMenu.EXIT:
                InGameMenu.isOpen = False
                MainMenu.isOpen = True

            InGameMenu.image = InGameMenu.DEFAULT



