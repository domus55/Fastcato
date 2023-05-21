import pygame

import Game
import InGameMenu
import MainMenu


def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.Game.isRunning = False
        # TODO: remove
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not MainMenu.MainMenu.isOpen:
            InGameMenu.InGameMenu.open()
        if event.type == pygame.MOUSEBUTTONDOWN:
            MainMenu.MainMenu.mouseButtonDown()
            InGameMenu.InGameMenu.mouseButtonDown()
        elif event.type == pygame.MOUSEBUTTONUP:
            MainMenu.MainMenu.mouseButtonUp()
            InGameMenu.InGameMenu.mouseButtonUp()

    Game.Game.keyPressed = pygame.key.get_pressed()