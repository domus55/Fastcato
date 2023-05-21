import pygame

import Game
import MainMenu


def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.Game.isRunning = False
        # TODO: remove
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Game.Game.isRunning = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            MainMenu.MainMenu.mouseButtonDown()
        elif event.type == pygame.MOUSEBUTTONUP:
            MainMenu.MainMenu.mouseButtonUp()

    Game.Game.keyPressed = pygame.key.get_pressed()