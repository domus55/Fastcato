import pygame

from src import game, icons, in_game_menu, level_manager, main_menu, music, result
from src.music import MUSIC_ENDED


def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.Game.isRunning = False
        if (event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
                and main_menu.MainMenu.state is main_menu.MainMenu.state.CLOSED
                and level_manager.LevelManager.current_level != 7):
            in_game_menu.InGameMenu.open()
        if event.type == pygame.MOUSEBUTTONDOWN:
            main_menu.MainMenu.mouseButtonDown()
            in_game_menu.InGameMenu.mouseButtonDown()
            result.Result.mouseButtonDown()
        if event.type == pygame.MOUSEBUTTONUP:
            main_menu.MainMenu.mouseButtonUp()
            in_game_menu.InGameMenu.mouseButtonUp()
            result.Result.mouseButtonUp()
        if event.type == pygame.FINGERDOWN:
            x = event.x * 1600
            y = event.y * 900
            game.Game.fingers[event.finger_id] = x, y
        if event.type == pygame.FINGERUP:
            game.Game.fingers.pop(event.finger_id, None)
        if event.type == MUSIC_ENDED:
            music.Music.start()
        if event.type == pygame.KEYDOWN:
            icons.Icons.buttonDown(pygame.key.get_pressed())
        if event.type == pygame.KEYUP:
            icons.Icons.buttonDown(pygame.key.get_pressed())

    return pygame.key.get_pressed()


