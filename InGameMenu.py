import pygame

import CloudManager
import Game
import LevelManager
import Screen
from MainMenu import MainMenu


class InGameMenu:
    isOpen = False

    DEFAULT = pygame.transform.scale(pygame.image.load("images/gui/inGameMenu/default.png"), (400, 405)).convert_alpha()
    RESUME = pygame.transform.scale(pygame.image.load("images/gui/inGameMenu/resumeActive.png"), (400, 405)).convert_alpha()
    RESTART = pygame.transform.scale(pygame.image.load("images/gui/inGameMenu/restartActive.png"), (400, 405)).convert_alpha()
    EXIT = pygame.transform.scale(pygame.image.load("images/gui/inGameMenu/exitActive.png"), (400, 405)).convert_alpha()

    colliderResume = pygame.Rect(633, 280, 335, 96)
    colliderRestart = pygame.Rect(633, 401, 335, 96)
    colliderExit = pygame.Rect(633, 522, 335, 96)

    image = DEFAULT

    @staticmethod
    def open():
        InGameMenu.isOpen = not InGameMenu.isOpen
        print("Open in game menu!")

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

            if InGameMenu.colliderResume.collidepoint(mousePos):
                InGameMenu.image = InGameMenu.RESUME
            elif InGameMenu.colliderRestart.collidepoint(mousePos):
                InGameMenu.image = InGameMenu.RESTART
            elif InGameMenu.colliderExit.collidepoint(mousePos):
                InGameMenu.image = InGameMenu.EXIT

    @staticmethod
    def mouseButtonUp():
        if InGameMenu.isOpen:
            mousePos = pygame.mouse.get_pos()

            if InGameMenu.colliderResume.collidepoint(mousePos) and InGameMenu.image == InGameMenu.RESUME:
                InGameMenu.isOpen = False
            elif InGameMenu.colliderRestart.collidepoint(mousePos) and InGameMenu.image == InGameMenu.RESTART:
                LevelManager.LevelManager.restartLevel()
                InGameMenu.isOpen = False
            elif InGameMenu.colliderExit.collidepoint(mousePos) and InGameMenu.image == InGameMenu.EXIT:
                InGameMenu.isOpen = False
                MainMenu.isOpen = True

            InGameMenu.image = InGameMenu.DEFAULT



