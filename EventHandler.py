import pygame

import Icons
import Game
import MainMenu
import InGameMenu
import Music
import Result
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
            Result.Result.mouseButtonDown()
        if event.type == pygame.MOUSEBUTTONUP:
            MainMenu.MainMenu.mouseButtonUp()
            InGameMenu.InGameMenu.mouseButtonUp()
            Result.Result.mouseButtonUp()
        if event.type == MUSIC_ENDED:
            Music.Music.start()
        if event.type == pygame.KEYDOWN:
            Icons.Icons.buttonDown(pygame.key.get_pressed())
        if event.type == pygame.KEYUP:
            Icons.Icons.buttonDown(pygame.key.get_pressed())

    Game.Game.keyPressed = pygame.key.get_pressed()

