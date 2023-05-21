import pygame

import CloudManager
import Game
import LevelManager
import Screen

'''You may find it strange that there are no button graphics. 
It's because instead of creating Button class, it's graphics, event handling
and all of this mess I came with a different approach. I use a default menu image
and whenever user clicks a button - image changes. I use 4 images with clicked buttons
assuming that user will never click more than one button at once. Thanks to that
I can handle all click event in here getting rid of unnecessary mess
'''

class MainMenu:
    isOpen = False

    DEFAULT = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/default.png"), (400, 525)).convert_alpha()
    PLAY = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/playActive.png"), (400, 525)).convert_alpha()
    LEVELS = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/levelsActive.png"), (400, 525)).convert_alpha()
    SETTINGS = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/settingActive.png"), (400, 525)).convert_alpha()
    EXIT = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/exitActive.png"), (400, 525)).convert_alpha()

    BACKGROUND1 = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/background/1.png"), (1600, 900)).convert_alpha()
    BACKGROUND2 = pygame.transform.scale(pygame.image.load("images/gui/mainMenu/background/2.png"), (1600, 900)).convert_alpha()

    colliderPlay = pygame.Rect(633, 220, 335, 96)
    colliderLevels = pygame.Rect(633, 341, 335, 96)
    colliderSettings = pygame.Rect(633, 462, 335, 96)
    colliderExit = pygame.Rect(633, 583, 335, 96)

    image = DEFAULT


    @staticmethod
    def open():
        MainMenu.isOpen = True
        CloudManager.CloudManager.initialize()
        print("Main Menu load!")

    @staticmethod
    def update():
        CloudManager.CloudManager.update()

    @staticmethod
    def render():
        Screen.screen.blit(MainMenu.BACKGROUND1, (-800, 0))
        Screen.screen.blit(MainMenu.BACKGROUND1, (800, 0))
        CloudManager.CloudManager.renderBeforeMountains()
        CloudManager.CloudManager.renderAfterMountains()
        Screen.screen.blit(MainMenu.BACKGROUND2, (0, 0))
        Screen.screen.blit(MainMenu.image, (600, 187))

    @staticmethod
    def mouseButtonDown():
        if MainMenu.isOpen:
            mousePos = pygame.mouse.get_pos()

            if MainMenu.colliderPlay.collidepoint(mousePos):
                MainMenu.image = MainMenu.PLAY
            elif MainMenu.colliderLevels.collidepoint(mousePos):
                MainMenu.image = MainMenu.LEVELS
            elif MainMenu.colliderSettings.collidepoint(mousePos):
                MainMenu.image = MainMenu.SETTINGS
            elif MainMenu.colliderExit.collidepoint(mousePos):
                MainMenu.image = MainMenu.EXIT

    @staticmethod
    def mouseButtonUp():
        if MainMenu.isOpen:
            mousePos = pygame.mouse.get_pos()

            if MainMenu.colliderPlay.collidepoint(mousePos) and MainMenu.image == MainMenu.PLAY:
                LevelManager.LevelManager.nextLevel()
                MainMenu.isOpen = False
            elif MainMenu.colliderLevels.collidepoint(mousePos) and MainMenu.image == MainMenu.LEVELS:
                print("Open levels")
            elif MainMenu.colliderSettings.collidepoint(mousePos) and MainMenu.image == MainMenu.SETTINGS:
                print("Open settings")
            elif MainMenu.colliderExit.collidepoint(mousePos) and MainMenu.image == MainMenu.EXIT:
                Game.Game.isRunning = False

            MainMenu.image = MainMenu.DEFAULT



