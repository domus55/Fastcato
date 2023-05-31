import pygame

import Game
import MainMenu
import InGameMenu
import Music
from Music import MUSIC_ENDED


def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.Game.isRunning = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and MainMenu.MainMenu.state is MainMenu.MainMenu.state.closed:
            InGameMenu.InGameMenu.open()
        if event.type == pygame.MOUSEBUTTONDOWN:
            MainMenu.MainMenu.mouseButtonDown()
            InGameMenu.InGameMenu.mouseButtonDown()
        if event.type == pygame.MOUSEBUTTONUP:
            MainMenu.MainMenu.mouseButtonUp()
            InGameMenu.InGameMenu.mouseButtonUp()
        if event.type == MUSIC_ENDED:
            Music.Music.start()

    Game.Game.keyPressed = pygame.key.get_pressed()